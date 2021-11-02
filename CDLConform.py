
import re
import xml.etree.ElementTree as ET
import os
import shutil
import sys
import os

###env initialization
from sys import platform
if platform == "linux" or platform == "linux2":
    env = "linux"
    Resolve_Loc = r'/opt/resolve/Developer/Scripting/Modules'
    print("Linux OS")
elif platform == "darwin":
    env = "mac"
    Resolve_Loc=r'/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules'
    print("System is mac OS")
elif platform == "win32":
    env = "win"
    Resolve_Loc=r'C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules'
    print("Windows OS")
else:
    print("error getting system platform")
sys.path.insert(1,Resolve_Loc)
import DaVinciResolveScript as dvr_script
import DaVinciResolveScript as bmd

ScriptDir = os.path.dirname(os.path.realpath(sys.argv[0]))
fu = bmd.scriptapp('Fusion')
resolve = bmd.scriptapp('Resolve')
ui = fu.UIManager
disp = bmd.UIDispatcher(ui)

###Config block
NodeNum = 1 ###1 is first node
defPath = os.path.abspath(r'C:\Users\myusername\CDLFolder') #default search path for CDL
ReelMatching = 'vfx' #choices are arri or vfx for now. Arri will match filenames in the style of A001C001 to cdl named the same way.
###

trackType = "Video"
ScriptDir = os.path.dirname(os.path.realpath(sys.argv[0]))
projectManager = resolve.GetProjectManager()
project = projectManager.GetCurrentProject()
timeline = project.GetCurrentTimeline()
startFrame = timeline.GetStartFrame()
fps = timeline.GetSetting('timelineFrameRate')
mediapool = project.GetMediaPool()
bin = mediapool.GetCurrentFolder()
Clips = timeline.GetItemListInTrack()
if not project:
    print("No project is loaded")
    sys.exit()

# replacement strings for CDL
WINDOWS_LINE_ENDING = b'\r\n'
UNIX_LINE_ENDING = b'\n'
MAC_LINE_ENDING =b'\r'

###About dialog setup
aboutText1 = "LiveGrade2Resolve is a resolve script written by Brendon Rathbone to import a folder of CDL's and match them to a timeline of clips for DIT handoff on scripted Television shows."
aboutText2 = "Copyright Brendon Rathbone 2021."
aboutText3 = '<h1>About Dialog</h1>\n<p>Version 1.4 - Nov 2021</p>\n<p>CDL2Resolve is a resolve script written by Brendon Rathbone to import a folder of CDLs and match them to a timeline of clips for DIT handoff on scripted Television shows. <p>\n<p>Copyright &copy; 2021 Brendon Rathbone.</p><p>\n<p><img src=data:image/jpg;base64,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>'
URL = "https://paypal.me/ambustion"

###UI Variables
TimelineText = "Timeline Clips - " + timeline.GetName()
status_text = ""
Frames_toggle = True
Folder_Name = ""
MetadataList = []
object_List = []
ScriptEMetadataList = []
ClipListNames = []
clip_list = []
CDL_List = []
LookList = []

def str2reel(look_name):
	if ReelMatching == 'vfx':
		reel,type,client,version = look_name.split("_")
	if ReelMatching == 'arri':
		reel , type , client=look_name.split("_")
	return reel

#def str2reelarri(look_name):
#	reel,type,client = look_name.split("_")
#	return reel

def addLut(lutpath,reel):
	clip_list = []
	dir,base = os.path.split(lutpath)
	date = base.split("_")[0]
	newFolder = os.path.join(defLut,date)
	newLoc = os.path.join(defLut,date, base)
	print("moving " + lutpath + " to " + newLoc)
	try:
		os.mkdir(newFolder)
	except OSError:
		print("Creation of the directory %s failed" % newFolder)
	else:
		print("Successfully created the directory %s " % newFolder)
	shutil.copy2(lutpath, newLoc)
	project.RefreshLUTList(True)

	object_List = []
	trackCount = timeline.GetTrackCount(trackType)
	ClipListNames = []
	for index in range(1, int(trackCount) + 1):
		# print(trackType + " " + str(index))
		clips = timeline.GetItemListInTrack(trackType, index)
		for clip in clips:
			reelname = clip.GetName()[:9]
			print(reelname)
			if reelname == reel:
				clip.SetLUT(2, base)
				print("success")
###
def GetCDL(cdl):
	newfields = []
	newrows = []
	MetadataList = []

	tree = ET.parse(cdl)
	root = tree.getroot()
	for item in root:
		for elem in root.iter():
			if "Slope" in elem.tag:
				slope = elem.text
			if "Offset" in elem.tag:
				offset = elem.text
			if "Power" in elem.tag:
				power = elem.text
			if "Saturation" in elem.tag:
				sat = elem.text
	filename = os.path.basename(cdl)
	reel=str2reel(filename)
	CDLdataList = {"reel": reel, "slope": slope, "offset": offset, "power": power, "sat": sat}
	return CDLdataList

def Get_ClipList():
	global clip_list
	global object_List
	global ClipListNames
	clip_list = []
	object_List = []
	trackCount = timeline.GetTrackCount(trackType)
	ClipListNames = []
	for index in range(1, int(trackCount) + 1):
		#print(trackType + " " + str(index))
		clips = timeline.GetItemListInTrack(trackType, index)
		for clip in clips:
			ClipListNames.append(clip.GetName())
			clip_list.append(clip)

	itm['Status'].Text = ClipListNames
	return clip_list, ClipListNames

def Select_CDLFolder():
	global Folder_Name
	global Clips
	global MetadataList
	newfields = []
	newrows = []
	MetadataList = []
	CDLdataList = []
	for x in file_list:
		tree = ET.parse(x)
		#print(tree)
		#print(x)
		root = tree.getroot()
		slope=root[0][0][0][1].text
		offset=root[0][0][0][2].text
		power=root[0][0][0][3].text
		sat=root[0][0][1][0].text
		filename = os.path.basename(x)
		reel = str2reel(filename)
		CDLdataList.append({"reel":reel,"slope":slope,"offset":offset,"power":power,"sat":sat})

	return CDLdataList

def add_cdl():
	global cdlMatch
	global clip_list
	for x in cdlMatch:
		for y in clip_list:
			clipreel = str2reel(y.GetName())
			if x[6] == clipreel:
				y.SetCDL({"NodeIndex" : NodeNum, "Slope" : x[2], "Offset" : x[3], "Power" : x[4], "Saturation" : x[5]})

###Window Defs
def AboutWindow():
	width, height = 500, 250
	win = disp.AddWindow(
		{"ID": "AboutWin", "WindowTitle": 'About Dialog', "Geometry": "{200, 200, 200, 100}"},
		[
			ui.VGroup({"ID": 'root'},
					  ## Add your GUI elements here:
					  [
						  ui.TextEdit({"ID": 'AboutText', "ReadOnly": "true",
									   "Alignment": "{AlignHCenter = true,AlignTop = true}", "HTML": aboutText3}),
						  ui.VGroup({"Weight": "0"},
									[

									ui.Label({"ID": "EMAIL", "Text": aboutText2,
											  "Alignment": "{AlignHCenter = true, AlignTop = true}", "WordWrap": "true",
											  "OpenExternalLinks": "true"}),
										ui.Label({"ID" : "URL", "Text":f"Buy me a Coffee: <a href={URL}>{URL}</a>",
												  "Alignment": {"AlignHCenter":True, "AlignTop":True},"OpenExternalLinks" : True,}),
										]),
					  ]),
		])

	itm = win.GetItems()



	###close the about window
	def _func(ev):
		disp.ExitLoop()

	win.On.AboutWin.Close = _func

	win.Show()
	disp.RunLoop()
	win.Hide()



###initialize main window
dlg = disp.AddWindow({"WindowTitle": "CDL2Resolve", "ID": "MyWin", "Geometry": [100, 100, 1000, 250], },
					 [
						 ui.VGroup({"Spacing": 2, },
								   [
									   # Add your GUI elements here:
									   ui.Label({"ID": "Timeline", "Text": TimelineText, "Weight": 0.5}),
									   ui.Tree({"ID":"CDLTree"}),
									   ui.HGap(0, .5),
										ui.HGap(0, .5),
									   ui.HGroup({"Spacing": 10, },
												 [
													ui.Button(
														 {"ID": "CDLFolder", "Text": "Select CDL Folder", "Weight": 0.5}),
												 ]),
									   ui.HGap(0, .5),
										ui.Button({"Weight": "0.25", "ID": 'AddButton',
												  "Text": 'Add CDL to resolve clips'}),
										ui.Label({"ID": "Status", "Text": "Waiting for input", "Weight": 0.5, "Alignment" : { "AlignHCenter" : True }}),
										ui.HGap(0, 2),
									   ui.Button({"Weight": "0.25", "ID": 'AboutDialogButton',
												  "Text": 'Show the About Dialog'})
								   ]),
					 ])

itm = dlg.GetItems()

col = itm["CDLTree"].NewItem()
col.Text[0] = 'Clip'
col.Text[1] = 'CDL Filename'
col.Text[2] = 'Slope'
col.Text[3] = 'Offset'
col.Text[4] = 'Power'
col.Text[5] = 'Saturation'
itm["CDLTree"].SetHeaderItem(col)
itm["CDLTree"].ColumnCount=6
###Resize the Columns
itm["CDLTree"].ColumnWidth[0]=275
itm["CDLTree"].ColumnWidth[1]=150
itm["CDLTree"].ColumnWidth[2]=90
itm["CDLTree"].ColumnWidth[3]=90
itm["CDLTree"].ColumnWidth[4]=90
itm["CDLTree"].ColumnWidth[5]=90
Get_ClipList()
for x in ClipListNames:
	itRow=itm['CDLTree'].NewItem()
	itRow.Text[0]=str(x)
	itm['CDLTree'].AddTopLevelItem(itRow)

# Close Main Window
def _func(ev):
	disp.ExitLoop()
dlg.On.MyWin.Close = _func

# Add your GUI element based event functions here:

def _func(ev):
	global cdlMatch
	selectedFolder = fu.RequestDir(defPath)
	File_List = os.listdir(selectedFolder)
	for x in File_List:
		if x.endswith(".cdl"):
			x = os.path.join(selectedFolder,x)
			LookList.append(x)

	CDLList = []
	itm['CDLTree'].Clear()
	cdlMatch = []
	for look in LookList:
		for y in ClipListNames:
			ClipReel = str2reel(y)
			lookreel = os.path.split(look)[1]
			lookreel = str2reel(lookreel)
			if ClipReel == lookreel:
				#print(cdlData)
				cdlData=GetCDL(look)
				fold,baselook = os.path.split(look)
				cdlMatch.append([y , baselook , cdlData['slope'] , cdlData['offset'] , cdlData['power'] , cdlData['sat'],cdlData['reel']])

		#print(cdlMatch)
	for x in cdlMatch:
		itRow=itm['CDLTree'].NewItem()
		itRow.Text[0]=str(x[0])
		itRow.Text[1]=str(x[1])
		itRow.Text[2]=str(x[2])
		itRow.Text[3]=str(x[3])
		itRow.Text[4]=str(x[4])
		itRow.Text[5]=str(x[5])
		itm['CDLTree'].AddTopLevelItem(itRow)

dlg.On.CDLFolder.Clicked = _func

def _func(ev):
	global CDL_List
	CDL_List = Select_CDLFolder()
	itm['Status'].Text = "Getting Clip Metadata"
	itm['Status'].Text = "Finished"
dlg.On.CDLButton.Clicked = _func

def _func(ev):
	ClipInfo(clip_list, ClipListNames)
dlg.On.ClipInfo.Clicked = _func

def _func(ev):
	itm['Status'].Text = "adding cdl and luts..."
	add_cdl()
dlg.On.AddButton.Clicked = _func

def _func(ev):
	AboutWindow()
dlg.On.AboutDialogButton.Clicked = _func

dlg.Show()
disp.RunLoop()
dlg.Hide()