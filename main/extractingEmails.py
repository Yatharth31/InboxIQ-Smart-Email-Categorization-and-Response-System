import pandas as pd
import mailbox



def getcharsets(msg):
    charsets = set({})
    for c in msg.get_charsets():
        if c is not None:
            charsets.update([c])
    return charsets

def handleerror(errmsg, emailmsg,cs):
    print()
    print(errmsg)
    print("This error occurred while decoding with ",cs," charset.")
    print("These charsets were found in the one email.",getcharsets(emailmsg))
    print("This is the subject:",emailmsg['subject'])
    print("This is the sender:",emailmsg['From'])

def getbodyfromemail(msg):
    body = None
    if msg.is_multipart():    
        for part in msg.walk():
            if part.is_multipart(): 
                for subpart in part.walk():
                    if subpart.get_content_type() == 'text/plain':
                        body = subpart.get_payload(decode=True) 
            elif part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True)
    elif msg.get_content_type() == 'text/plain':
        body = msg.get_payload(decode=True) 
    for charset in getcharsets(msg):
        try:
            body = body.decode(charset)
        except UnicodeDecodeError:
            handleerror("UnicodeDecodeError: encountered.",msg,charset)
        except AttributeError:
             handleerror("AttributeError: encountered" ,msg,charset)
    return body    



if __name__ == '__main__':

    df_list = list()
    df = pd.DataFrame()

    loc = input("Enter the location of the .mbox file")
    # ex: "D:\test\Programs\takeout-20220328T102034Z-001\Takeout\Mail\emails.mbox"
    for thisemail in mailbox.mbox(loc):
        subject = thisemail["subject"]
        From = thisemail["from"]
        To = thisemail["to"]
        try:
            body = getbodyfromemail(thisemail)
        except:
            continue
        df_list.append({"To":To,"From":From,"Subject":subject,"Body":body})

    for i in df_list:
        try:
            df = df.append(i,ignore_index=True)
        except Exception as e:
            print(e)

    df.to_csv("myEmails.csv")