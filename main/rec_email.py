import imaplib
import email
from email.header import decode_header
import os



cwd = os.getcwd()
f1 = open(os.path.join(cwd,"emailID.txt"))
emailID = f1.read().rstrip('\n')
f1.close()



f2 = open(os.path.join(cwd,"password.txt"))
emailPassword = f2.read().rstrip('\n')
f2.close()



class ReciveEmail:
    def __init__(self,emailID = emailID,emailPassword=emailPassword):
        username = emailID
        password = emailPassword
        self.imap = imaplib.IMAP4_SSL("imap.gmail.com")
        self.imap.login(username, password)

        self.status, self.messages = self.imap.select("INBOX")
        self.N = 1
        self.messages = int(self.messages[0])

    def clean(self,text):
        return "".join(c if c.isalnum() else "_" for c in text)

    def check_email(self):
        for i in range(self.messages, self.messages-self.N, -1):
            res, msg = self.imap.fetch(str(i), "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding)
                    From, encoding = decode_header(msg.get("From"))[0]
                    if isinstance(From, bytes):
                        From = From.decode(encoding)
                    print("Subject:", subject)
                    print("From:", From)
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            try:
                                body = part.get_payload(decode=True).decode()
                            except:
                                pass
                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                print("Body of the Email: ",body)
                            elif "attachment" in content_disposition:
                                filename = part.get_filename()
                    else:
                        content_type = msg.get_content_type()
                        body = msg.get_payload(decode=True).decode()
                        if content_type == "text/plain":
                            print(body)
                    if content_type == "text/html":
                        folder_name = self.clean(subject)
                    print("="*100)
        self.imap.close()
        self.imap.logout()
        return subject,From,body