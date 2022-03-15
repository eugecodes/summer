from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import zipfile
from os.path import basename
import smtplib
import logging
import config
import os

logLevel = logging.ERROR
if config.DEBUG is True:
    logLevel = logging.DEBUG
logger = logging.getLogger(__name__)
logger.setLevel(logLevel)
ch = logging.FileHandler(config.LOG_DEBUG, 'w')
ch.setLevel(logLevel)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

def lockProcess(filename='worldbank.lock'):
    if not isLockedProcess(filename):
        open(filename, 'a').close()

def unlockProcess(filename='worldbank.lock'):
    if isLockedProcess(filename):
        os.remove(filename)

def isLockedProcess(filename='worldbank.lock'):
    return os.path.isfile(filename)

def _canSendEmail():
    return hasattr(config, 'EMAIL') and config.EMAIL.get('ALLOW') is True

def sendEmail(emlFrom, emlTo, emlSubj, emlBody, files=None):
    if _canSendEmail():
        server = config.EMAIL.get('SERVER_SMTP')
        port = config.EMAIL.get('SERVER_PORT')
        usr = config.EMAIL.get('SERVER_USER')
        pwd = config.EMAIL.get('SERVER_PASS')

        msg = MIMEMultipart()
        msg['Subject'] = emlSubj
        msg['From'] = emlFrom
        msg['To'] = emlTo

        msg.attach(MIMEText(emlBody, 'plain', 'utf-8'))

        for f in files or []:
            ctype, encoding = mimetypes.guess_type(f)
            if ctype is None or encoding is not None:
                ctype = "application/octet-stream"
            maintype, subtype = ctype.split("/", 1)
            with open(f, 'rb') as fp:
                if maintype == "text":
                    attachment = MIMEText(fp.read(), _subtype=subtype)
                elif maintype == "image":
                    attachment = MIMEImage(fp.read(), _subtype=subtype)
                elif maintype == "audio":
                    attachment = MIMEAudio(fp.read(), _subtype=subtype)
                else:
                    attachment = MIMEBase(maintype, subtype)
                    attachment.set_payload(fp.read())
                    encoders.encode_base64(attachment)
                attachment.add_header("Content-Disposition", "attachment", filename=basename(f))
                msg.attach(attachment)

        s = smtplib.SMTP(server, port)
        s.ehlo()
        s.starttls()
        s.ehlo()
        if usr and pwd:
            s.login(usr, pwd)
        s.sendmail(emlFrom, emlTo, msg.as_string())
        s.quit()

def sendDebugEmail():
    if _canSendEmail():
        emlFrom = config.EMAIL.get('FROM')
        emlTo = config.EMAIL.get('TO')
        emlSubj = config.EMAIL.get('SUBJ')
        debugFile = config.LOG_DEBUG
        attachments = None
        zipFileName = 'log/debug.zip'
        with zipfile.ZipFile(zipFileName, 'w', zipfile.ZIP_DEFLATED) as zipf:
            absname = os.path.abspath(debugFile)
            arcname = os.path.basename(debugFile)
            zipf.write(absname, arcname)
            attachments = [zipFileName]

        sendEmail(emlFrom, emlTo, emlSubj, 'Import successfully completed', attachments)
        if attachments is not None:
            for attachment in attachments:
                os.remove(attachment)

def sendErrorEmail(e):
    if _canSendEmail():
        emlFrom = config.EMAIL.get('FROM')
        emlTo = config.EMAIL.get('TO')
        emlSubj = config.EMAIL.get('SUBJ')
        body = "Error during data import\nError: %s" % e
        sendEmail(emlFrom, emlTo, emlSubj, body)
