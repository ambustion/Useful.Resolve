# Useful.Resolve

A bunch of Scripts I find useful for Davinci Resolve

I kept adding new repos for scripts so thought I would just keep the smaller ones here. I am mostly a colorist so messy but drop me an email at ambustion@gmail.com and I can likely help answer any questions.

Most rely on having python(3.6) scripting set up in resolve. I've been making more of them external so just ask and I can probably convert. 

# Resolve External environment setup
This is just an example of how I've been able to call resolve from a script from outside of resolve. Helpful if you want to use your own python version or just to have threaded scripts run outside of the main resolve UI scripting.
```
###env initialization
import sys
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
```

# ExportCDL.py:
Let's you export a timeline to individual .cdl files. Comes with a mini resolve gui just for some double checking. Also can export a timeline edl alongside the cdl. 
Meant to work with dailies workflows where you have a timeline of nodes with a cdl adjustment node and a lut node only. Doesn't work well on a full edit.
make sure your luma adjustment is set to 0 as per the resolve manual. - please note export lut button not working yet but you can have fun clicking it if you want.

![](/Assets/ExportCDL.JPG)


# GetStillsAtGMarkers.py
-Grabs stills at all Green markers by default. Can change color by editing the script. Relies on my ResolveTransport Module(in progress but it works for me). Also requires pyautogui(Pip install pyautogui) for now but once I can update my resolve will integrate the new stills commands into it so that won't be needed.

# ResolveTransport
 A python module for controlling a resolve timeline

Must paste System.Remote.Control = 1 to the advanced panel of the Davinci Resolve Preferences. 

By default, connects to 127.0.0.1 and port 9060

Sample usage:

from ResolveTransport import ResolveTransport
rt = ResolveTransport()

##Establish Connection - Will print confirmation
rt.connect()

### Get current timeline timecode
rt.gettc()

### Go to timecode
rt.settc(01:00:00:00)

### Get current timeline fps
rt.getfps

# slate.setting
A fusion slate to read timecode and project name automatically from resolve timelines. 
