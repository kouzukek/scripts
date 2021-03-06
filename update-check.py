#!/usr/bin/python3

from subprocess import check_output,call,PIPE,DEVNULL;
from email.mime.text import MIMEText
from socket import gethostname
import re
import sys

mailto   = sys.argv[1] if len(sys.argv) == 2 else None
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
    
def apt_list_upgradable():
    call(["apt","update"],stdout = DEVNULL,stderr=DEVNULL)
    out = check_output(
            ["apt","list","--upgradable"],
            universal_newlines=True,
            )
    return out[out.find("\n")+1:]

if __name__=="__main__":
    ret=apt_list_upgradable()
    if len(ret)>0:
        print("[APT] upgradables for %s"%gethostname())
        print("-"*20)
        print(ret)
        if mailto:
            mail(ret)
    else:
        print("Nothing will be mailed.")
