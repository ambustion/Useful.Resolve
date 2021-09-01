# Useful.Resolve
A bunch of Scripts I find useful for Davinci Resolve

I kept adding new repos for scripts so thought I would just keep the smaller ones here. I am mostly a colorist so messy but drop me an email at ambustion@gmail.com and I can likely help answer any questions.

Most rely on having python(3.6) scripting set up in resolve. I've been making more of them external so just ask and I can probably convert. 
###ExportCDL.py
Let's you export a timeline to individual .cdl files. Comes with a mini resolve gui just for some double checking. Also can export a timeline edl alongside the cdl. 
Meant to work with dailies workflows where you have a timeline of nodes with a cdl adjustment node and a lut node only. Doesn't work well on a full edit.
make sure your luma adjustment is set to 0 as per the resolve manual. - please note export lut button not working yet but you can have fun clicking it if you want.

![Alt text](Assets/ExportCDL.jpg?raw=true "ExportCDL")
