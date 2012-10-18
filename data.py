# -*- coding: utf-8 -*-

import sys
from kirbybase import *
import conf

balance_table = conf.db_file
db = KirbyBase()

def init(db_file):
    global balance_table
    balance_table = db_file

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


if __name__=="__main__":
    #db = KirbyBase()
    try:
        db.drop(balance_table)
    except OSError:
        pass
    except KBError as e:
        print "WARNNING:", e
        sys.exit(1)

    try:
        db.create(balance_table, ['id:str', 'name:str', 'balance:float'])
    except KBError as e:
        print "WARNNING:", e
        sys.exit(2)

    if len(sys.argv) < 2:
        db.close()
        sys.exit(0)

    # initial database
    name_list = sys.argv[1]
    with open(name_list, "r") as namefile:
        for line in namefile.readlines():
            items = line.split('\t')
            id = items[0]
            name = items[1].strip()
            db.insert(balance_table, [id, name, 0.0])

    db.close()
