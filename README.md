# Useful.Resolve

A bunch of Scripts I find useful for Davinci Resolve

I kept adding new repos for scripts so thought I would just keep the smaller ones here. I am mostly a colorist so messy but drop me an email at ambustion@gmail.com and I can likely help answer any questions.

Most rely on having python(3.6) scripting set up in resolve. I've been making more of them external so just ask and I can probably convert. 


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

#slate.setting
A fusion slate to read timecode and project name automatically from resolve timelines. 
