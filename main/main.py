import email
import imaplib
import time
import pandas as pd
from similarity import Similarity
from rec_email import ReciveEmail
from send_email import send_mail
import os



cwd = os.getcwd()
f1 = open(os.path.join(cwd,"emailID.txt"))
emailID = f1.read().rstrip('\n')
f1.close()



f2 = open(os.path.join(cwd,"password.txt"))
emailPassword = f2.read().rstrip('\n')
f2.close()



class ProcessEmail:
    def __init__(self, corpusName=None,test=False):
        emails = pd.read_csv(os.path.join(cwd,"myEmails.csv"))
        sim_obj = Similarity(emails)
        self.login()
        self.corpusName = corpusName
        run = True
        last_email_id = 0
        self.models = None
        last_email = ""
        while run:
            replied = False
            rec_email_obj = ReciveEmail()
            msgSubject,msgFrom,msgBody=rec_email_obj.check_email()
            if ((self.user not in msgFrom) and
                    ("Auto generated Response:" not in msgSubject) and
                    (last_email != msgBody)):
                last_email = msgBody
                fout = open('lastEmail.txt', 'w')
                fout.write("Subject: "+msgSubject+"\n From: "+msgFrom+"\n Body: "+msgBody)
                fout.close()
                email_reply_body,similarity_value = sim_obj.rec_email_process(msgFrom,msgSubject,msgBody)
                if (similarity_value >= 0.30):
                    reply = ("This is an Auto generated Response" + "\n" +
                     "Subject: " +'Reply ' +msgSubject + '\n' +
                     "To: " + msgFrom + '\n' +
                     "From: " + "Auto reply: "+emailID + '\n\n' + email_reply_body)
                    send_mail(to=msgFrom,sub="This is an Auto generated Response", body=reply)
                    replied = True
                else:
                    print("No similar email is found hence no reply sent")
                if replied:
                    print ("The time is " + str(time.strftime("%I:%M:%S"))+" Email reply sent")
            else:
                print ("The time is " + str(time.strftime("%I:%M:%S")) +
                       ". No new mail. Will check again in 30 seconds.")
            if test:
                run = False
                break
            time.sleep(30)



    def login(self):
        ''' Get login info from user '''
        self.user = emailID
        self.pswd = emailPassword#getpass.getpass("Please enter your password: ")
        print(self.user,self.pswd)
        self.mail = imaplib.IMAP4_SSL('imap.gmail.com',993)
        self.mail.login(self.user, self.pswd)



if __name__ == '__main__':
    corpus ="myemail"
    proc = ProcessEmail(corpus)


