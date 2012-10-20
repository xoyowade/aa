# -*- coding: utf-8 -*-

import sys
from kirbybase import *

balance_table = ""
db = KirbyBase()

def init(db_file):
    global balance_table
    balance_table = db_file
    print "load database %s" % db_file

def batch_update(recs):
    for rec in recs:
        update(rec)

def update(rec):
    try:
        db.update(balance_table, ['recno'], [rec.recno], 
                  [rec.balance], ['balance'])
        return True
    except KBError as e:
        print >>sys.stderr, "[WARNNING]", e
        return False

def show(sortDesc=['recno']):
    try:
        result = db.select(balance_table, ['recno'], ["*"], returnType='object', sortFields=sortDesc)
        return result
    except KBError as e:
        print >>sys.stderr, "[WARNNING]", e
        return []

def get(recno):
    try:
        result = db.select(balance_table, ['recno'], [recno], returnType='object')
        return result[0]
    except KBError as e:
        print >>sys.stderr, "[WARNNING]", e
        return None

def generate(name_list):
    try:
        db.drop(balance_table)
    except OSError:
        pass
    except KBError as e:
        print >>sys.stderr, "WARNNING:", e
        return

    try:
        db.create(balance_table, ['id:str', 'name:str', 'balance:float'])
    except KBError as e:
        print >>sys.stderr, "WARNNING:", e
        return

    if name_list and len(name_list) > 0:
        # initialize database
        with open(name_list, "r") as namefile:
            for line in namefile.readlines():
                items = line.split('\t')
                id = items[0]
                name = items[1].strip()
                db.insert(balance_table, [id, name, 0.0])
    