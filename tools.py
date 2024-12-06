import re
from datetime import datetime, date
from jarrbo_contributie.models import *
from django.core.mail import get_connection, send_mail
from django.core.mail.message import EmailMessage
import csv

def clean_iban(iban):
    return iban.upper().replace(' ','')

_country2length = dict(
    AL=28, AD=24, AT=20, AZ=28, BE=16, BH=22, BA=20, BR=29,
    BG=22, CR=21, HR=21, CY=28, CZ=24, DK=18, DO=28, EE=20,
    FO=18, FI=18, FR=27, GE=22, DE=22, GI=23, GR=27, GL=18,
    GT=28, HU=28, IS=26, IE=22, IL=23, IT=27, KZ=20, KW=30,
    LV=21, LB=28, LI=21, LT=20, LU=20, MK=19, MT=31, MR=27,
    MU=30, MC=27, MD=24, ME=22, NL=18, NO=15, PK=24, PS=29,
    PL=28, PT=25, RO=24, SM=27, SA=24, RS=22, SK=24, SI=19,
    ES=24, SE=24, CH=21, TN=24, TR=26, AE=23, GB=22, VG=24 )
 
def valid_iban(iban, country=None):
    # Ensure upper alphanumeric input.
    iban = iban.replace(' ','').replace('\t','').upper()
    if not re.match(r'^[\dA-Z]+$', iban): 
        return False
    # Check country code
    if country and iban[:2]!=country:
        return False
    # Check valid country code
    if iban[:2] not in _country2length:
        return False
    # Validate country code against expected length.
    if len(iban) != _country2length[iban[:2]]:
        return False
    # Shift and convert.
    iban = iban[4:] + iban[:4]
    digits = int(''.join(str(int(ch, 36)) for ch in iban)) #BASE 36: 0..9,A..Z -> 0..35
    return digits % 97 == 1
    
def clean_postcode(pc):
    # standard output in uppercase and space between number and characters
    return pc[:4] + ' ' + pc[-2:].upper()
    
def valid_postcode(pc):
    # Ensure upper alphanumeric input.
    pc = pc.replace(' ','').replace('\t','').upper()
    if not re.match(r'^[1-9](\d{3})[A-Z]{2}$', pc):
        return False
    return True
    
def clean_date(datum):
    d = datum.split('-')
    jr = int(d[2])
    if jr < 100:
        if jr > 25:
            jr = jr + 1900
        else:
            jr = jr + 2000
    return datetime(jr,int(d[1]),int(d[0])).date()

def send_contributiemail(subject, body, to):
    from jarrbo_contributie.models import Configuration
    config = Configuration.objects.get()
    host = config.mail_host
    port = config.mail_port
    username = config.mail_username
    password = config.mail_password
    use_tls = config.mail_use_tls
    from_email = config.mail_username
    bcc = config.mail_username
    with get_connection(
                host=host, 
                port=port, 
                username=username, 
                password=password, 
                use_tls=use_tls
        ) as connection:
        EmailMessage(subject, body, from_email, [to], [bcc],
                 connection=connection).send()

def backup_db(event="imp"):
    from pathlib import Path
    from django.core import management
    from django.conf import settings
    import datetime
    import subprocess
    dt = datetime.datetime.now()
    filename = f"{settings.LOCALS['DB_NAME']}-{event}-{dt:%Y%m%d%H%M}.json"
    backupfile = settings.DATA_FOLDER / filename
    rcloneconfig = settings.BASE_DIR / 'rclone.conf'
    remotebackup = settings.REMOTE_BACKUP / filename
    with open(backupfile, 'w') as f:
        management.call_command('dumpdata','--all', stdout=f)
    rclonecmd = f"rclone copyto --config={rcloneconfig} {backupfile} Onedrive:'{remotebackup}'"
    subprocess.run(rclonecmd, shell=True)
    subprocess.run(f"rm {backupfile}", shell=True)
