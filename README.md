# keylogger-v1

for educational purposes only!

### background: malware using python
- There has been a [rise of python malware](https://www.cyborgsecurity.com/cyborg_labs/python-malware-on-the-rise/) in the last few years. 
- Python's large library collection and ease of use make it ideal for malware developers.


### credit/inspiration: Grant Collins 

[Grant Collins](https://www.youtube.com/watch?v=25um032xgrw&t=1848s&ab_channel=GrantCollins) is a Cybersecurity focused Youtube channel and makes a number of videos regarding python keyloggers.<br> 
His video documents making a keylogger in python. I have used the elements he has implemented in his keylogger.

### project aims
- to create a basic (version-1) keylogger using python software: an introduction to writing python malware, of sorts
- gaining an understanding of the versatility of python malware. I have been heavily inspired by his video and have  used the elements he has implemented in his keylogger.

## core features

### basic keylogger
- the basic keylogger is simple and uses pynput to log the keys pressed. These are then written to a file.

### start requirements and timer
- The keylogger begins running when the program has detected that a search engine is running on the computer (either Chrome, Safari, or Firefox). Then, a timer with a predetermined amount of time begins to run. The keylogger will stop when this timer ends.

### other features
- Recording audio for a predetermined amount of time
- Taking a screenshot of the screen
- Recording the computer's system information
- Copying the clipboard contents

## encryption
- using Fernet cryptography, files can be encrypted and sent.
- encrypted files are kept seperate from the unencrypted files, for ease of use and error checking.
- there is a decryption function to decrypt the encrypted files with the encryption key generated.

## further obfuscation:
- PyArmor is a command line obfuscation tool for python scripts. I have not used it purely because it would obfuscate my code on git. Pretend I did.

## next time:
- implement more formatting of the keylogger file, so it is more readable
- add more obfuscation techniques, and implement them
- making the storage and sending of files more discreet
