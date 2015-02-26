#!/usr/bin/python3

from subprocess import check_output,call,PIPE,DEVNULL;
from email.mime.text import MIMEText
from socket import gethostname
import re
import sys

mailto   = "user@hoge.com"
mailfrom = "root@%s" % gethostname()

def mail(content):
    msg = MIMEText(content, "plain", "utf-8")
    msg["Subject"] = "[APT] upgradables for %s" % gethostname()
    msg["From"]    = mailfrom
    msg["To"]      = mailto
    print("-"*20)
    print(msg.as_string())
    check_output(["/usr/sbin/sendmail", "-t"],
                 input = msg.as_string().encode("utf-8"))
    
def apt_upgradable_list():
    call(["apt","update"],stdout = DEVNULL,stderr=DEVNULL)
    out = check_output(
            ["apt","list","--upgradable"],
            universal_newlines=True,
            )
    return out[out.find("\n")+1:]

if __name__=="__main__":
    ret=apt_upgradable_list()
    if len(ret)>0:
        print("[APT] upgradables for %s"%gethostname())
        print("-"*20)
        print(ret)
        mail(ret)
    else:
        print("Nothing will be mailed.")
