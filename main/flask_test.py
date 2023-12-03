from app import app
import unittest

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    
    def test_mail(self):
        rv = self.app.post('/mail/', data = '{"id":"testworks1010@gmail.com","password":"T1e2s3t4"}', follow_redirects=True)

        send_mail(emailID,"Testing main Unittest","A solar panel is a series of interconnected silicon solar cells, link together to form a circuit. There is a glass layer on the front with an insulating layer and a protective back sheet on the rear of the panel. Solar panels absorb the sunlight and produce an electric current that travels across wires eventually working its way to your home or business. A single solar panel can generate only a limited amount of electricity. Therefore, most installations contain multiple solar panels.",emailID_test,emailPassword_test)
        time.sleep(40)
        ProcessEmail(test=True)
        time.sleep(40)
        obj = ReciveEmail(emailID_test,emailPassword_test)
        res = obj.check_email()
        assert "This is an Auto generated Response" in res[0]
        
        assert b'verification' in rv.data
