from cryptography.fernet import Fernet

key = " " #key from the generator key

#get the three files you want to unencrypt ( the e version)

encrypted_files = [fff,fff,fff]
count = 0

for decrypting_file in encrypted_files:

        with open(encrypted_files[count], 'rb') as f:  # open up each file
            data = f.read()

        fernet = Fernet(key)
        decrypted = fernet.decrypt(data)

        with open(encrypted_files[count], 'wb') as f:
            f.write(decrypted)


        count += 1

        time.sleep(120)  # each iteration to slepe for 2 emails for emails to be sent

