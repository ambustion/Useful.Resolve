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

import DaVinciResolveScript as bmd

ScriptDir = os.path.dirname(os.path.realpath(sys.argv[0]))
fu = bmd.scriptapp('Fusion')
resolve = bmd.scriptapp('Resolve')
ui = fu.UIManager
disp = bmd.UIDispatcher(ui)


dlg = disp.AddWindow({"WindowTitle": "StillLabel", "ID": "MyWin", "Geometry": [100, 100, 1000, 100], },
                     [
                         ui.VGroup({"Spacing": 2, },
                                   [
                                       # Add your GUI elements here:
                                       ui.Label({"ID": "Timeline", "Text": "Enter Still Label", "Weight": 0.5}),
                                       ui.LineEdit({"ID":"label"}),
                                       ui.Button({"ID":"AddButton", "Text":"Add", "Weight":0})
                                       ]),
                         ])
itm = dlg.GetItems()
def _func(ev):
    disp.ExitLoop()
dlg.On.MyWin.Close = _func

def _func(ev):
    label=str(itm["label"].Text)
    projectManager=resolve.GetProjectManager()
    project=projectManager.GetCurrentProject()
    timeline = project.GetCurrentTimeline()
    gallery=project.GetGallery()
    current_album=gallery.GetCurrentStillAlbum()
    still=timeline.GrabStill()
    current_album.SetLabel(still , label)
    disp.ExitLoop()
dlg.On.AddButton.Clicked = _func

dlg.Show()
disp.RunLoop()
dlg.Hide()
