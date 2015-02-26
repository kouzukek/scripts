#!/usr/bin/python3

from subprocess import check_output,call,PIPE,DEVNULL;
from email.mime.text import MIMEText
from socket import gethostname
import datetime
import urllib.request
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

def get_change_log(pkgname):
    uris = check_output(['apt-get','changelog','--print-uris',pkgname],universal_newlines=True)
    uri = uris.split('\n')[0].strip("'\"\n")
    data = urllib.request.urlopen(uri).read().decode()
    return data

def extract_changelog_lastupdated(changelog):
    months = dict(zip("Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec".split("|"),map(lambda x:x+1,range(12))))
    pattern = r"""
    \s*--.*
    (
    (Mon|Tue|Wed|Thu|Fri|Sat|Sun),\s 
    (?P<date>\d{1,2})\s(?P<month>Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s(?P<year>\d{4})\s
    (?P<hour>\d{2}):(?P<minute>\d{2}):(?P<second>\d{2})\s
    (?P<tz>[\+\-](\d{4}))
    )\s*$
    """[1:]
    m = re.search(pattern,changelog,re.VERBOSE|re.MULTILINE).groupdict()
    tz = datetime.timedelta(hours=int(m['tz'][:3]),minutes=int(m['tz'][3:]))
    return datetime.datetime(int(m['year']),months[m['month']],int(m['date']),
            int(m['hour']),int(m['minute']),int(m['second']),
            tzinfo = datetime.timezone(tz)).astimezone()

if __name__=="__main__":
    data = get_change_log('unzip')
    m = extract_changelog_lastupdated(data)
    print(m)
    sys.exit(0)
    ret=apt_list_upgradable()
    if len(ret)>0:
        print("[APT] upgradables for %s"%gethostname())
        print("-"*20)
        print(ret)
        if mailto:
            mail(ret)
    else:
        print("Nothing will be mailed.")
