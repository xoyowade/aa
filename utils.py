# -*- coding: utf-8 -*-

import sys, traceback
import smtplib
from datetime import date
import data
import conf

def log(event, recs):
    log = "[%s %s][%s]: |" % (date.today(), event.am, event.addr)
    for rec in recs:
        if rec.balance > 0:
            log += "%s %s|" % (rec.id, rec.balance)
        else:
            log += "%s|" % (rec.id)

    log += "\n"

    with open(conf.log_file, "a+") as logfile:
        logfile.write(log.encode('utf-8'))

    return log

def balance(recs, total):
    avg = total / len(recs)
    for rec in recs:
        rec.balance -= avg
        ori_rec = data.get(rec.recno)
        assert(ori_rec)
        rec.balance += ori_rec.balance
    return

def genmsg(recs, event):
    msg = u"最近活动记录：%s\r\n\r\n" % event
    for rec in recs:
        msg += u"%s (%s): %f 元\r\n" % (rec.name.decode('utf-8'), rec.id, rec.balance)
    return msg

def sendmail(toaddrs, msg):
    mail= u"""From: %s
To: %s
Subject: [AA]%s 最新榜单

%s
""" % (conf.admin_mail, ", ".join(toaddrs), date.today(), msg)
    if conf.send_mail_swtich:
        smtp_server = smtplib.SMTP(conf.smtp_server_addr)
        smtp_server.sendmail(conf.admin_mail, toaddrs, mail.encode('utf-8'))
        smtp_server.quit()

def inform_by_mail(recs, event):
    try:
        mailmsg = genmsg(recs, event)
        toaddrs = []
        for rec in recs:
            toaddrs.append(rec.id + conf.domain)

        sendmail(toaddrs, mailmsg)
    except BaseException as e:
        print >>sys.stderr, "Connect to ", conf.smtp_server_addr, " fail"
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stderr)

if __name__=="__main__":
    """
    Test for email inform
    """
    class Record(object): pass
    recs = []
    rec = Record()
    rec.id = "zwxiao"
    rec.name = "肖之慰"
    rec.balance = 1.0
    recs.append(rec)
    print conf.send_mail_swtich
    inform_by_mail(recs, "event")
