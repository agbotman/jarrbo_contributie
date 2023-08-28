from django.utils.translation import gettext as _
import csv, codecs
from .models import Configuration, Activity, Member, MemberImport, \
                    Memberstatus, Contribution, Inschrijving, \
                    Machtiging, Paymentmethod
from datetime import datetime, date
import pytz
from django.db.models import Max, Min
from .tools import valid_iban, clean_iban, valid_postcode, clean_postcode, \
                    clean_date
import string

config = Configuration.objects.get()

result = {
    "active": 0,
    "new": 0,
    "unsubscribed": 0,
    "changed": 0
        }
        
zaal = Activity.objects.get(description='Zaal')
veld = Activity.objects.get(description='Veld')
vr30 = Activity.objects.get(description='Vr7x7')
curyear = datetime.now().year

class MissingHeaderException(Exception):
    """
    Exception raised when a required header is missing
    """
    def __init__(self, headers, msg=None):
        if msg is None:
            # Set some default useful error message
            msg = _("The following headers are missing: %s") % headers
        super(MissingHeaderException, self).__init__(msg)
        self.headers = headers

class InvalidFileFormatException(Exception):
    """
    Exception raised when not a text file
    """
    def __init__(self, msg=None):
        if msg is None:
            # Set some default useful error message
            msg = _("Invalid file format")
        super(InvalidFileFormatException, self).__init__(msg)

def import_Memberfile(memberfile):
    Requiredfields = ['Relatiecode','Voorletter(s)',
               'Roepnaam', 'Tussenvoegsel(s)', 'Achternaam',
               'Geslacht', 'Geboortedatum', 'Straatnaam', 
               'Huisnummer', 'Toevoeging', 'Postcode',
               'Plaats', 'Telefoon', 'Mobiel', 'E-mail',
               'Status', 'Leeftijdscategorie',
               'Laatste wijziging', 'Bondssporten', 'Lid sinds',
               'Bankrekeningnummer']
    csvfile = codecs.iterdecode(memberfile, 'utf-8')
    reader = csv.DictReader(csvfile, delimiter=';')
    result["active"] = 0
    result["new"] = 0
    result["unsubscribed"] = 0
    result["changed"] = 0
    maximport = Member.objects.aggregate(m=Max('last_import'))
    last = maximport["m"]
    try:
        headerchecked = False
        imp = MemberImport()
        for row in reader:
            if not headerchecked:
                missingheaders = check_headers(row, Requiredfields)
                if missingheaders:
                    raise MissingHeaderException(str(missingheaders))
                else:
                    imp.save()
                    headerchecked = True
            import_member(row, imp)
    except UnicodeDecodeError:
        raise InvalidFileFormatException()
    config.last_memberimport = date.today()
    config.save()
    imp.active_members = result["active"]
    imp.new_members = result["new"]
    imp.unsubscribed_members = Member.objects.filter(last_import=last).count()
    imp.changed_members = result["changed"]
    imp.save()
    
    # All member not found in this import will get the status afgemeld
    afgemeld = Memberstatus.objects.get(status='Afgemeld')
    for mbr in Member.objects.exclude(last_import=imp):
        mbr.status = afgemeld
        mbr.save()

    # All member in this import with status afgemeld will get the status aangemeld 
    aangemeld = Memberstatus.objects.get(status='Afgemeld')        
    for mbr in Member.objects.filter(last_import=imp,status=afgemeld):
        mbr.status = aangemeld
        mbr.save()
        
    return imp.id
    
def check_headers(dict, fields):
    missingheaders =[]
    for field in fields:
        if field not in dict:
            missingheaders.append(field)
    return missingheaders
    
def import_member(r, imp):
    if r['Status'] == "definitief":
        result["active"] += 1
        try:
            m = Member.objects.get(relatiecode=r['Relatiecode'])
            if memberchanged(m,r):
                updatemember(m,r)
                result["changed"] += 1
        except Member.DoesNotExist:
            m = newmember(r)
            result["new"] += 1
        if "Veld" in r['Bondssporten']:
            if r['Leeftijdscategorie'] == 'Senioren Vrouwen' and \
                (curyear - m.geboortedatum.year) > 29:
                if not vr30 in m.activities.all():
                    m.activities.add(vr30)
                try:
                    c = Contribution.seizoen_objects.get(member=m, activity=vr30)
                except:
                    c = Contribution.seizoen_objects.create_contribution(member=m,
                                                                         seizoen=config.seizoen,
                                                                         activity=vr30)
            else:
                if not veld in m.activities.all():
                    m.activities.add(veld)
                try:
                    c = Contribution.seizoen_objects.get(member=m, activity=veld)
                except:
                    c = Contribution.seizoen_objects.create_contribution(member=m,
                                                                         seizoen=config.seizoen,
                                                                         activity=veld)
        if "Zaal" in r['Bondssporten']:
            if not zaal in m.activities.all():
                m.activities.add(zaal)
            try:
                c = Contribution.seizoen_objects.get(member=m, activity=zaal)
            except:
                c = Contribution.seizoen_objects.create_contribution(member=m,
                                                                     seizoen=config.seizoen,
                                                                     activity=zaal)
        m.last_import = imp
        m.save()
        
def memberchanged(m,r):
    if not (m.voorletters == r['Voorletter(s)']):
        return True
    if not (m.roepnaam == r['Roepnaam']):
        return True
    if not (m.tussenvoegsels == r['Tussenvoegsel(s)']):
        return True
    if not (m.achternaam == r['Achternaam']):
        return True
    if not (m.geslacht == r['Geslacht']):
        return True
    if not (m.geboortedatum == datetime.strptime(r['Geboortedatum'],"%d-%m-%Y").date()):
        return True
    if not (m.straatnaam == r['Straatnaam']):
        return True
    if not (m.huisnummer == int(r['Huisnummer'])):
        return True
    if not (m.toevoeging == r['Toevoeging']):
        return True
    if not (m.postcode == r['Postcode']):
        return True
    if not (m.plaats == r['Plaats']):
        return True
    if not (m.telefoon == r['Telefoon']):
        return True
    if not (m.mobiel == r['Mobiel'].replace(" ", "")):
        return True
    if not (m.email == r['E-mail']):
        return True
    if not (m.iban == r['Bankrekeningnummer']):
        return True
    return False

def updatemember(m,r):
    m.voorletters = r['Voorletter(s)']
    m.roepnaam = r['Roepnaam']
    m.tussenvoegsels = r['Tussenvoegsel(s)']
    m.achternaam = r['Achternaam']
    m.geslacht = r['Geslacht']
    m.geboortedatum = datetime.strptime(r['Geboortedatum'],"%d-%m-%Y").date()
    m.straatnaam = r['Straatnaam']
    m.huisnummer = int(r['Huisnummer'])
    m.toevoeging = r['Toevoeging']
    m.postcode = r['Postcode']
    m.plaats = r['Plaats']
    m.telefoon = r['Telefoon']
    m.mobiel = r['Mobiel'].replace(" ", "")
    m.email = r['E-mail']
    if valid_iban(r['Bankrekeningnummer']):
        m.iban = r['Bankrekeningnummer']
        m.machtiging = True
    m.save()
    return 
    
def newmember(r):
    m = Member(relatiecode=r['Relatiecode'],
               voorletters=r['Voorletter(s)'],
               roepnaam=r['Roepnaam'],
               tussenvoegsels=r['Tussenvoegsel(s)'],
               achternaam=r['Achternaam'],
               geslacht=r['Geslacht'],
               geboortedatum=datetime.strptime(r['Geboortedatum'],"%d-%m-%Y").date(),
               straatnaam=r['Straatnaam'],
               huisnummer=r['Huisnummer'],
               toevoeging=r['Toevoeging'],
               postcode=r['Postcode'],
               plaats=r['Plaats'],
               telefoon=r['Telefoon'],
               mobiel=r['Mobiel'].replace(" ", ""),
               email=r['E-mail'],
               iban=r['Bankrekeningnummer'],
               aanmeldingsdatum=datetime.strptime(r['Lid sinds'],"%d-%m-%Y").date(),
              )
    if valid_iban(m.iban):
        m.machtiging = True
    a = Memberstatus.objects.get(status='Aangemeld')
    m.status = a
    m.save()
    # 2023-08-02 001 Inschrijvingen bestand wordt niet meer gebruikt bij ledenverwerking
    # i = getInschrijving(m.roepnaam, m.achternaam, m.postcode, m.geboortedatum)
    # if i:
    #     m.matchInschrijving(i)
    # return m

def import_Inschrijvingenfile(inschrijvingenfile):
    # utf-8-sig removes the BYTE ORDER MARK in the first row
    csvfile = codecs.iterdecode(inschrijvingenfile, 'utf-8-sig')
    reader = csv.DictReader(csvfile, delimiter=';')
    startdate = pytz.UTC.localize(datetime(2000,1,1))
    last = Inschrijving.objects.aggregate(maxdt=Max('datumtijd'))['maxdt'] or startdate
    for row in reader:
        dt = datetime.strptime(row['Datum ingevuld'],"%d-%m-%Y %H:%M")
        dt = pytz.UTC.localize(dt)
        if dt > last:
            i = Inschrijving()
            i.datumtijd = dt
            i.roepnaam = row['Roepnaam (lid)'].strip()
            i.achternaam = row['Achternaam (lid)'].strip()
            i.adres = row['Adres (lid)']
            i.woonplaats = row['Woonplaats (lid)'].strip()
            cl_postcode = clean_postcode(row['Postcode (lid)'])
            if valid_postcode(cl_postcode):
                i.postcode = cl_postcode
            else:
                i.postcode = '9999 XX'
            i.geboortedatum=clean_date(row['Geboren op (lid)'])
            i.machtiging = 'akkoord' in row['Eenmalige machtiging']
            i.naam_machtiging = row['Naam']
            i.adres_machtiging = row['Adres']
            cl_postcode = clean_postcode(row['Postcode'])
            if valid_postcode(cl_postcode):
                i.postcode_machtiging = cl_postcode
            else:
                i.postcode_machtiging = '9999 XX'
            i.plaats_machtiging = row['Woonplaats']
            cl_iban = clean_iban(row['IBAN nummer bankrekening'])
            if valid_iban(cl_iban):
                i.iban = cl_iban
            else:
                i.iban = 'INVALID IBAN'
            i.privacy_policy = 'kennis' in row['Privacy policy']
            i.webform = True
            i.save()
            m = getMember(i.roepnaam, i.achternaam, i.postcode, i.geboortedatum)
            if m:
                m.matchInschrijving(i)
    return

def import_Machtigingenfile(inschrijvingenfile):
    # utf-8-sig removes the BYTE ORDER MARK in the first row
    csvfile = codecs.iterdecode(inschrijvingenfile, 'utf-8-sig')
    reader = csv.DictReader(csvfile, delimiter=';')
    startdate = pytz.UTC.localize(datetime(2000,1,1))
    last = Machtiging.objects.aggregate(maxdt=Max('datumtijd'))['maxdt'] or startdate
    dateprocess = pytz.UTC.localize(datetime(2021,1,1))
    for row in reader:
        dt = datetime.strptime(row['Datum ingevuld'],"%d-%m-%Y %H:%M")
        dt = pytz.UTC.localize(dt)
        if dt > last:
            m = Machtiging()
            m.datumtijd = dt
            m.voornaam = row['Voornaam'].strip()
            m.achternaam = row['Achternaam'].strip()
            m.adres = row['Adres']
            m.woonplaats = row['Woonplaats']
            cl_postcode = clean_postcode(row['Postcode'])
            if valid_postcode(cl_postcode):
                m.postcode = cl_postcode
            else:
                m.postcode = '9999 XX'
            m.geboortedatum = clean_date(row['Geboortedatum'])
            m.naam_machtiging = row['ten name van']
            m.plaats_machtiging = row['Plaats']
            m.email_machtiging = row['email adres']
            cl_iban = clean_iban(row['IBAN Nummer'])
            if valid_iban(cl_iban):
                m.iban = cl_iban
            else:
                m.iban = 'INVALID IBAN'
            m.save()
            if dt > dateprocess:
                mbr = getMember(m.voornaam, m.achternaam, m.postcode, m.geboortedatum)
                if mbr:
                    mbr.machtiging = True
                    mbr.naam_machtiging = m.naam_machtiging
                    mbr.adres_machtiging = m.adres
                    mbr.postcode_machtiging = m.postcode
                    mbr.plaats_machtiging = m.plaats_machtiging
                    mbr.email_machtiging = m.email_machtiging
                    mbr.iban = m.iban
                    mbr.payment_method = Paymentmethod.objects.get(description='Incasso')
                    mbr.save()
                for c in mbr.contributions.all():
                    c.factuur_naam = m.naam_machtiging
                    c.factuur_adres = m.adres
                    c.factuur_postcode = m.postcode
                    c.factuur_plaats = m.plaats_machtiging
                    c.factuur_email = m.email_machtiging
                    c.payment_method = mbr.payment_method
                    c.save()
                    c.recreate_payments()
    return
    
def getMember(roepnaam, achternaam, postcode, geboortedatum):
    mbrlist = Member.objects.filter(geboortedatum=geboortedatum,
                                    postcode=postcode,
                                    roepnaam=roepnaam.title(),
                                    achternaam=achternaam.title())
    if mbrlist:
        return mbrlist[0]
    mbrlist = Member.objects.filter(geboortedatum=geboortedatum,
                                    postcode=postcode,
                                    roepnaam__startswith=roepnaam[0].upper())
    if mbrlist:
        return mbrlist[0]
    mbrlist = Member.objects.filter(geboortedatum=geboortedatum,
                                    achternaam=achternaam.title(),
                                    roepnaam__startswith=roepnaam[0].upper())
    if mbrlist:
        return mbrlist[0]
    mbrlist = Member.objects.filter(geboortedatum=geboortedatum,
                                    achternaam=achternaam.title(),
                                    postcode=postcode)
    if mbrlist:
        return mbrlist[0]
    mbrlist = Member.objects.filter(roepnaam=roepnaam,
                                    achternaam=achternaam.title(),
                                    postcode=postcode)
    if mbrlist:
        return mbrlist[0]
    return None

def getInschrijving(roepnaam, achternaam, postcode, geboortedatum):
    ilist = Inschrijving.objects.filter(geboortedatum=geboortedatum,
                                        postcode=postcode,
                                        roepnaam=roepnaam,
                                        achternaam=achternaam,
                                        member__isnull=True)
    if ilist:
        return ilist[0]
    ilist = Inschrijving.objects.filter(geboortedatum=geboortedatum,
                                        postcode=postcode,
                                        roepnaam__startswith=roepnaam[0],
                                        member__isnull=True)
    if ilist:
        return ilist[0]
    ilist = Inschrijving.objects.filter(geboortedatum=geboortedatum,
                                        achternaam=achternaam,
                                        roepnaam__startswith=roepnaam[0],
                                        member__isnull=True)
    if ilist:
        return ilist[0]
    ilist = Inschrijving.objects.filter(geboortedatum=geboortedatum,
                                        achternaam=achternaam,
                                        postcode=postcode,
                                        member__isnull=True)
    if ilist:
        return ilist[0]
    ilist = Inschrijving.objects.filter(roepnaam=roepnaam,
                                    achternaam=achternaam,
                                    postcode=postcode,
                                    member__isnull=True)
    if ilist:
        return ilist[0]
    return None

