
"""Send email via standard module smtplib

https://docs.python.org/3.5/library/smtplib.html

usage:

from common import mailer

f = 'email.ini'
mailer.init_config(f)

mailer.send_simple("This is a test.",  address='test@example.com' )


mailer.send_simple("This is a test.", subject="Test - ignore"  address='test@example.com' )

"""
from configparser import ConfigParser
#from email.message import EmailMessage

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from common import logger
log = logger.get_mod_logger(__name__)

config = None

smtp_port = 0

def init_config(config_file = 'email.ini'):
    global config, smtp_port

    config = ConfigParser()
    config.read(config_file)
    if 'port' in config['email']:
        smtp_port = config['email']['port']



def send_simple(text, subject="Testing", address=None, cc=None):
    msg = get_message( text, subject, address, cc_email=cc)

    with smtplib.SMTP(  config['email']['smtp_host'], smtp_port ) as s:
        try:
            s.set_debuglevel(0)

            if 'username' in config['email']:
                # probably won't work, requires TLS?
                print("login {}".format( config['email']['username']) )
                s.login(user=config['email']['username'], password=config['email']['password'])

            s.send_message(msg)
        except smtplib.SMTPRecipientsRefused as err:
            print("ERROR: send failed {}".format(err))
            return False

    return True


def send_multi(text, subject="Testing", address=[], cc=None):

    elist = ",".join(address)
    msg = get_message( text, subject=subject, address=elist, cc_email=cc)

    #return 
    with smtplib.SMTP(  config['email']['smtp_host'], smtp_port ) as s:
        try:
#            s.set_debuglevel(2)
#            s.set_debuglevel(1)
#            s.set_debuglevel(0)

            if 'username' in config['email']:
                # probably won't work, requires TLS?
                print("login {}".format( config['email']['username']) )
                s.login(user=config['email']['username'], password=config['email']['password'])

            s.send_message(msg)
        except smtplib.SMTPRecipientsRefused as err:
            log.error(f"send failed {err}" )
            return False

    return True
def get_message(text, subject="Testing", address=None, cc_email=None, cc_list=[]):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] =  config['email']['return_email']
    #msg['To'] = config['email']['admin_email']
    if address:
        msg['To'] = address

    elif 'test_email' in config['email']:
        msg['To'] = config['email']['test_email']
    elif 'admin_email' in config['email']:
        msg['To'] = config['email']['admin_email']
    else:
        log.error("No email specified")
        return

    cc = []
    if 'cc_email' in config['email']:
        cc.append(config['email']['cc_email'])

    if cc_email:
        cc.append( cc_email )
    if len(cc_list) > 0:
        cc += cc_list 
    if cc:
        log.info(f"cc = {cc} ")
        msg['Cc'] = ", ".join(cc)


    bcc = []
    if 'bcc_email' in config['email']:
        bcc.append(config['email']['bcc_email'])
        log.info("got here")

    if bcc:
        msg['Bcc'] = ", ".join(bcc)
    log.debug(f"cc={msg['Cc']}  bcc={msg['Bcc']}");

    if 'reply-to' in config['email']:
        msg['reply-to'] = config['email']['reply-to']

    if 'signature' in config['email']:
        text += "\n" + config['email']['signature']

    part = MIMEText(text, 'plain')

    msg.attach(part)
    #print("len={} send from {} to {} via {}".format(len(text), msg['From'], msg['To'],  config['email']['smtp_host'] ))
    return msg
