import unittest
import os
from rec_email import ReciveEmail
from send_email import send_mail
import time
from main import ProcessEmail
from app import app
import unittest


cwd = os.getcwd()
f1 = open(os.path.join(cwd,"emailID.txt"))
emailID = f1.read().rstrip('\n')
f1.close()

f2 = open(os.path.join(cwd,"password.txt"))
emailPassword = f2.read().rstrip('\n')
f2.close()

f3 = open(os.path.join(cwd,os.path.join("test","emailID.txt")))
emailID_test = f3.read().rstrip('\n')
f3.close()

f4 = open(os.path.join(cwd,os.path.join("test","password.txt")))
emailPassword_test = f4.read().rstrip('\n')
f4.close()



class TestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_send_rec_email(self):

        obj = ReciveEmail()

        send_mail(emailID,"Testing send_email Unittest","Mail Body to Test the send_email program with unittest")
        time.sleep(40)

        res = obj.check_email()

        assert "Testing send_email Unittest" in res[0]


    def test_main(self):
        send_mail(emailID,"Testing main Unittest","A solar panel is a series of interconnected silicon solar cells, link together to form a circuit. There is a glass layer on the front with an insulating layer and a protective back sheet on the rear of the panel. Solar panels absorb the sunlight and produce an electric current that travels across wires eventually working its way to your home or business. A single solar panel can generate only a limited amount of electricity. Therefore, most installations contain multiple solar panels.",emailID_test,emailPassword_test)
        time.sleep(40)
        ProcessEmail(test=True)
        time.sleep(40)
        obj = ReciveEmail(emailID_test,emailPassword_test)
        res = obj.check_email()
        assert "This is an Auto generated Response" in res[0]
    
    
    def test_mail_api(self):
        

        send_mail(emailID,"Testing main Unittest","A solar panel is a series of interconnected silicon solar cells, link together to form a circuit. There is a glass layer on the front with an insulating layer and a protective back sheet on the rear of the panel. Solar panels absorb the sunlight and produce an electric current that travels across wires eventually working its way to your home or business. A single solar panel can generate only a limited amount of electricity. Therefore, most installations contain multiple solar panels.",emailID_test,emailPassword_test)
        time.sleep(40)
        rv = self.app.post('/mail/', data = '{"id":"testworks1010@gmail.com","password":"T1e2s3t4","test":1}', follow_redirects=True)
        time.sleep(40)
        obj = ReciveEmail(emailID_test,emailPassword_test)
        res = obj.check_email()
        assert "This is an Auto generated Response" in res[0]

if __name__ == '__main__':
    unittest.main()

