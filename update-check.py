#!/usr/bin/python3

from subprocess import Popen,call,PIPE;
from email.mime.text import MIMEText
from socket import gethostname
import re

mailto   = "user@hoge.com"
mailfrom = "root@%s" % gethostname()

def mail(content):
    msg = MIMEText(content)
    msg["Subject"] = "[APT] upgradables for %s" % gethostname()
    msg["From"]    = mailfrom
    msg["To"]      = mailto

    Popen(["/usr/sbin/sendmail","-t"],stdin=PIPE) \
            .communicate(msg.as_string().encode("utf-8"))

def apt_upgradable_list():
    call(["apt-get","update"])
    (outs, errs) = Popen(
            ["apt-get","-u","--assume-no","-V","upgrade"],
            stdout = PIPE,
            universal_newlines=True,
            ).communicate()
    m = re.search(r"^(\d+)\s*upgraded.*(\d)+\s*not upgraded\.$", outs,
            flags=re.MULTILINE)
    if m and sum(int(s) for s in m.groups()) > 0:
        return "\n".join(outs.split("\n")[4:-2])
    else:
        return None

if __name__=="__main__":
    ret=apt_upgradable_list()
    if ret:
        mail(ret)
