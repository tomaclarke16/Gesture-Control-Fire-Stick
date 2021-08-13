from adb_shell.adb_device import AdbDeviceTcp
from adb_shell.auth.sign_pythonrsa import PythonRSASigner
from adb_shell.auth.keygen import keygen
import os

class FireStickController():

    def __init__(self):
        if not os.path.isfile('adbkey'):
            print('Generating ADB Keys')
            keygen('adbkey')
        else:
            print('ADB Keys Found')

        with open('adbkey') as f:
            priv = f.read()
        with open('adbkey'+'.pub') as f:
            pub = f.read()
        self.creds = PythonRSASigner(pub,priv)

    def addDevice(self,deviceIP):
        self.device = AdbDeviceTcp(deviceIP,5555,default_transport_timeout_s=9.)
        try:
            self.device.close()
        except:
            print('No Device Connected')
        else:
            self.device.connect(rsa_keys=[self.creds],auth_timeout_s=10.)
            print('Device Connected')

        return self.device
    
    def back(self):
        self.device._service(b'shell',b'input keyevent 4')
        print('Back Command Sent')

    def home(self):
        self.device._service(b'shell',b'input keyevent 3')
        print('Menu Command Sent')

    def select(self):
        self.device._service(b'shell',b'input keyevent 23')
        print('Select Command Sent')

    def up(self):
        self.device._service(b'shell',b'input keyevent 19')
        print('Up Command Sent')

    def down(self):
        self.device._service(b'shell',b'input keyevent 20')
        print('Down Command Sent')

    def left(self):
        self.device._service(b'shell',b'input keyevent 21')
        print('Left Command Sent')

    def right(self):
        self.device._service(b'shell',b'input keyevent 22')
        print('Right Command Sent')

    def playPause(self):
        self.device._service(b'shell',b'input keyevent 85')
        print('Play/Pause Command Sent')

    def rewind(self):
        self.device._service(b'shell',b'input keyevent 89')
        print('Rewind Command Sent')

    def forward(self):
        self.device._service(b'shell',b'input keyevent 90')
        print('FastForward Command Sent')