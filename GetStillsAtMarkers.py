from SMPTE import SMPTE
import time
import os
import sys

###env initialization
import sys
import os
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
import DaVinciResolveScript as bmd

ScriptDir = os.path.dirname(os.path.realpath(sys.argv[0]))
fu = bmd.scriptapp('Fusion')
resolve = bmd.scriptapp('Resolve')
print(resolve)

s = SMPTE()

trackType = "Video"
ScriptDir = os.path.dirname(os.path.realpath(sys.argv[0]))
config_loc = os.path.join(ScriptDir, "MemphisNotes_Config.ini")
# replacement strings
WINDOWS_LINE_ENDING = b'\r\n'
UNIX_LINE_ENDING = b'\n'
MAC_LINE_ENDING =b'\r'

ui = fu.UIManager
disp = bmd.UIDispatcher(ui)

ui = fu.UIManager
disp = bmd.UIDispatcher(ui)

ClipsBool = True

projectManager = resolve.GetProjectManager()
project = projectManager.GetCurrentProject()
gallery=project.GetGallery()
timeline = project.GetCurrentTimeline()
tlname = timeline.GetName()
startFrame = timeline.GetStartFrame()
print(startFrame)
fps = timeline.GetSetting('timelineFrameRate')
s.fps = fps


print(timeline.GetName())
mediapool = project.GetMediaPool()
bin = mediapool.GetCurrentFolder()
Clips = timeline.GetItemListInTrack()
if not project:
    print("No project is loaded")
    sys.exit()

Markers = timeline.GetMarkers()
print(Markers)

for x in Markers:
    if Markers[x]["color"] == "Green":
        tc = s.gettc(x+startFrame)
        timeline.SetCurrentTimecode(tc)
        #gallery = project.GetGallery()
        #gallery.SetCurrentStillAlbum("Test")
        timeline.GrabStill()