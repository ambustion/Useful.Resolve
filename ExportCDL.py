import os
import xml.etree.ElementTree as ET
import re
from shutil import copyfile

ScriptDir = os.path.dirname(os.path.realpath(sys.argv[0]))

ui = fu.UIManager
disp = bmd.UIDispatcher(ui)
ClipsBool = True

def create_table():
    global CDLMatch
    global timeline
    global projectManager
    global project
    global SMPTE
    global TimelineText
    global cdlfile
    try:
        itm['Tree'].Clear()
    except:
        '''continue'''
    projectManager=resolve.GetProjectManager()
    project=projectManager.GetCurrentProject()

    timeline=project.GetCurrentTimeline()
    TimelineText="Timeline Clips - " + timeline.GetName()
    trackList=timeline.GetTrackCount("video")

    clipList=[]
    for x in range(1 , int(trackList) + 1):
        tmpclipList=timeline.GetItemListInTrack("video" , x)
        if tmpclipList == None:
            print()
        else:
            for y in tmpclipList:
                clipList.append(y)
    ClipRanges=[]
    for x in clipList:
        name=x.GetName()
        dur=x.GetDuration()
        mpItem=x.GetMediaPoolItem()
        start=mpItem.GetClipProperty('Start TC')
        end=mpItem.GetClipProperty('End TC')
        reel=mpItem.GetMetadata('Reel Number')
        stc=mpItem.GetMetadata('Scene') + mpItem.GetMetadata('Take') + mpItem.GetMetadata('Camera #')
        stc = stc.replace(" ","")
        ClipRanges.append({ "name": name , "Reel": reel , "start": start , "dur": dur , "end": end , "stc": stc })
    for x in ClipRanges:
        print(x)
    cdlfile = os.path.join(ScriptDir,"tmpCDL.edl")
    timeline.Export(cdlfile,resolve.EXPORT_EDL, resolve.EXPORT_CDL)

    cdlVals = []
    try:
        with open(cdlfile) as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("TITLE") or line.startswith("FCM") or line == "\n":
                    continue
                else:
                    splitLine = list(filter(None,re.split("[)( \r\n*]", line)))
                    cdlVals.append(splitLine)
    except:
        print("could not access temporary cdl file")
    cdlList = []
    n = 3 #split cdl into groups of 3
    for i in range(0, len(cdlVals), n):
        chunk = cdlVals[i:i+n]
        cdlList.append(chunk)
    CDLMatch = []
    for x in cdlList:
        for y in ClipRanges:
            if x[0][1] == y['Reel'] and x[0][4] >= y['start'] and x[0][4]<=y['end']:
                name = y['name']
                Desc = y['stc']
                slope = (x[1][1],x[1][2],x[1][3])
                offset = (x[1][4],x[1][5],x[1][6])
                power = (x[1][7],x[1][8],x[1][9])
                sat = (x[2][1])
                CDLMatch.append([name,Desc,slope,offset,power,sat])
            else:
                print("no match")
    for x in CDLMatch:
        print("CDL Matches")
        print(x)
create_table()



aboutText2 = "Copyright Brendon Rathbone 2021."
aboutText3 = '<h1>About Dialog</h1>\n<p>Version 0.1 - Aug 25 2021</p>\n<p>Simple Export of .cdl files from a resolve timeline. Make sure you are grading with luminance mixer default to 0 and only two nodes, one for cdl and one for LUT <p>\n<p>Copyright &copy; 2021 Brendon Rathbone.</p>'
URL = "https://paypal.me/ambustion"

def indent(elem, level=0):
    i = "\n" + level*"\t"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "\t"
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
def createCDL(cdl,loc):
    name_space={ # namespace defined below
        "xmlns": "urn:ASC:CDL:v1.01"
        }

    name = os.path.join(loc,cdl[1]+"_"+cdl[0]+ ".cdl")
    Desc=cdl[1]
    Slp=cdl[2][0]+" "+cdl[2][1]+" "+cdl[2][2]
    Offst=cdl[3][0]+" "+cdl[3][1]+" "+cdl[3][2]
    Pwr=cdl[4][0]+" "+cdl[4][1]+" "+cdl[4][2]
    St=cdl[5]
    # create the file structure
    root = ET.Element('ColorDecisionList',name_space)
    data=ET.SubElement(root,'ColorDecision')
    items=ET.SubElement(data , 'ColorCorrection')
    item1=ET.SubElement(items , 'SOPNode')
    item2=ET.SubElement(items , 'SATNode')
    item4=ET.SubElement(item1 , 'Description')
    item5=ET.SubElement(item1 , 'Slope')
    item6=ET.SubElement(item1 , 'Offset')
    item7=ET.SubElement(item1 , 'Power')
    item8=ET.SubElement(item2 , 'Saturation')

    item4.text=Desc
    item5.text=str(Slp)
    item6.text=str(Offst)
    item7.text=str(Pwr)
    item8.text=St
    tree=ET.ElementTree("ColorDecisionList")
    ET.register_namespace('' , "urn:ASC:CDL:v1.01")
    #_pretty_print(root)
    indent(root)
    # create a new XML file with the results
    with open(name, "wb") as myfile:
        tree._setroot(root)
        tree.write(myfile,encoding='UTF-8', xml_declaration=True,method="xml")



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

dlg = disp.AddWindow({"WindowTitle": "Resolve Export CDL", "ID": "MyWin", "Geometry": [100, 100, 1000, 500], },
                     [
                         ui.VGroup({"Spacing": 2, },
                                   [
                                       # Add your GUI elements here:
                                       ui.Label({"ID": "Timeline", "Text": TimelineText, "Weight": 0}),
                                       ui.Tree({"ID": "Tree", "SortingEnabled": True,
                                                "Events": {"ItemDoubleClicked": True, "ItemClicked": True}}),
                                       ui.VGap(0, .2),
                                       ui.HGroup({"Spacing": 2,"Weight": 0 },
                                       [
                                       ui.CheckBox({"ID":"edlCheck", "Text":"Export EDL file?","Checked":True}),
                                        ui.CheckBox({"ID":"lutCheck", "Text":"Export LUT?","Checked":True}),
                                       ui.Label({"ID":"FolderTxt","Text":"folder location","Weight": 2}),
                                       ui.Button({"ID": "SaveLocButton", "Text": "Export CDL Files", "Weight": 0}),
                                           ]),
                                        ui.Button({"Weight": 0, "ID": 'ReloadButton',
                                                  "Text": 'Reload Clips'}),
                                       ui.Button({"Weight": 0, "ID": 'AboutDialogButton',
                                                  "Text": 'Show the About Dialog'})


                                   ]),
                     ])

itm = dlg.GetItems()
col=itm["Tree"].NewItem()
col.Text[0]='name'
col.Text[1]='scene'
col.Text[2]='Slope'
col.Text[3]='Offset'
col.Text[4]='Power'
col.Text[5]='Saturation'

itm["Tree"].SetHeaderItem(col)

itm["Tree"].ColumnCount=6
###Resize the Columns
itm["Tree"].ColumnWidth[0]=90
itm["Tree"].ColumnWidth[1]=90
itm["Tree"].ColumnWidth[2]=200
itm["Tree"].ColumnWidth[3]=200
itm["Tree"].ColumnWidth[4]=200
itm["Tree"].ColumnWidth[5]=90
for x in CDLMatch:
    itRow=itm['Tree'].NewItem()
    itRow.Text[0]=str(x[0])
    itRow.Text[1]=str(x[1])
    itRow.Text[2]=str(x[2])
    itRow.Text[3]=str(x[3])
    itRow.Text[4]=str(x[4])
    itRow.Text[5]=str(x[5])
    itm['Tree'].AddTopLevelItem(itRow)



# Close Main Window
def _func(ev):
    disp.ExitLoop()
dlg.On.MyWin.Close = _func

def _func(ev):
    selectedPath=str(fu.RequestDir('Y://TLOU//DISTRIBUTION'))

    print('[Folder] ' , selectedPath)
    itm['FolderTxt'].Text=selectedPath
    filecount = 0
    for x in CDLMatch:
        createCDL(x,selectedPath)
        filecount +=1
    save_string = str(filecount) + " cdl files "
    if itm['edlCheck'].Checked == True:
        filesave = os.path.join(selectedPath,timeline.GetName()+".edl")
        copyfile(cdlfile,filesave)
        save_string = save_string + "and 1 edl "
    save_string = save_string + "were saved to " + selectedPath
    itm['FolderTxt'].Text=save_string



dlg.On.SaveLocButton.Clicked = _func


def _func(ev):
    create_table()
    for x in CDLMatch:
        itRow=itm['Tree'].NewItem()
        itRow.Text[0]=str(x[0])
        itRow.Text[1]=str(x[1])
        itRow.Text[2]=str(x[2])
        itRow.Text[3]=str(x[3])
        itRow.Text[4]=str(x[4])
        itRow.Text[5]=str(x[5])
        itm['Tree'].AddTopLevelItem(itRow)
dlg.On.ReloadButton.Clicked = _func

def _func(ev):
    AboutWindow()
dlg.On.AboutDialogButton.Clicked = _func

dlg.Show()
disp.RunLoop()
dlg.Hide()