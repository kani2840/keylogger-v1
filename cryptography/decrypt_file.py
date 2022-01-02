from cryptography.fernet import Fernet

key = "UEEnOeF61l4St2C_-0LRcCXxmPiaQq49REBPzJpEovo="  # key from the generator key

keys_information_e = "log_e.txt"  # getting the files we want to decrypt
system_info_e = "sysinfo_e.txt"
clipboard_info_e = "clipboard_e.txt"

encrypted_files = [keys_information_e, system_info_e, clipboard_info_e]
count = 0

for decrypting_file in encrypted_files:
    with open(encrypted_files[count], 'rb') as f:  # open up each file
        data = f.read()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    with open(encrypted_files[count], 'wb') as f:
        f.write(decrypted)

    count += 1

