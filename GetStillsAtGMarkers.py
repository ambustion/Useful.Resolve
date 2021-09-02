from ResolveTransport import ResolveTransport
from pyautogui import hotkey
from timecode import Timecode
import DaVinciResolveScript as dvr_script

###Settings
MarkerColor = 'Green'
###

rt = ResolveTransport()
from python_get_resolve import GetResolve
resolve=dvr_script.scriptapp("Resolve")
fusion=resolve.Fusion()
ui = fusion.UIManager
disp = dvr_script.UIDispatcher(ui)

project = resolve.GetProjectManager().GetCurrentProject()
mediapool = project.GetMediaPool()
bin = mediapool.GetCurrentFolder()
Clips = bin.GetClipList()
timeline = project.GetCurrentTimeline()
TC_Start = timeline.GetStartFrame()
marks = timeline.GetMarkers()
print(marks)
if not project:
    print("No project is loaded")
    sys.exit()

resolve.OpenPage("color")
hotkey('ctrl', 'f')
for x in marks:
    if marks[x]['color'] == MarkerColor:
        print("This is a "+MarkerColor+" marker")
        print(x)
        TC = Timecode(23.976,frames=(x + TC_Start))
        rt.connect()
        rt.settc(str(TC))
        strippedtc = str(TC)
        stc = strippedtc.replace(":","")
        hotkey('ctrl', 'alt', 'shift', 's')
hotkey('ctrl' , 'f')