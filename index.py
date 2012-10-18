# -*- coding: utf-8 -*-

""" AA accounting system """

import data
import web
import time
import utils
from time import strftime

### Url mappings

urls = (
    '/', 'New',
    '/show', 'Show',
    '/new', 'New',
    '/log', 'Log',
)

render = web.template.render('templates', base='base')

class Record(object): pass

class New: 

    class Info:
        def __init__(self):
            self.date = strftime("%Y-%m-%d", time.localtime())
            if time.localtime().tm_hour < 15:
                self.am = "AM"
            else:
                self.am = "PM"
            self.submit_ok = False
            self.written_log = ""
    
    def GET(self): 
        recs = data.show(['id'])
        info = self.Info()
        return render.new(recs, info)

    def POST(self): 
        input = web.input()

        # parse event
        event = Record()
        event.am = input['am']
        event.addr = input['addr']

        # parse balance records
        recs = {}
        total = 0.0
        for key in input:
            keys = key.split('_')
            if len(keys) == 3:
                put = False
                rec = Record()
                rec.recno = int(keys[0])
                rec.id = keys[1]
                rec.balance = 0.0

                if keys[2] == 'balance':
                    try:
                        balance = float(input[key])
                    except ValueError as e:
                        balance = 0.0

                    if balance > 0:
                        assert(total - 0.0 < 0.001)
                        total = rec.balance = balance
                        put = True
                elif keys[2] == 'in' and (rec.recno not in recs):
                    put = True
                
                if put:
                    recs[rec.recno] = rec
                    
        recs = recs.values()

        # log
        written_log = utils.log(event, recs)

        # calculate balances
        utils.balance(recs, total)

        # update balances
        data.batch_update(recs)

        # inform users by mail
        recs = data.show(['balance'])
        utils.inform_by_mail(recs, written_log)

        # render
        recs = data.show(['id'])
        info = self.Info()
        info.submit_ok = True
        info.written_log = written_log
        return render.new(recs, info)

class Show: 
    
    def GET(self): 
        recs = data.show(['balance'])
        info = Record()
        return render.show(recs, info)

class Log: 
    
    def GET(self): 
        web.header('Content-type','text/html; charset=utf-8')
        web.header('Transfer-Encoding','chunked')
        with open(utils.log_file, "r+") as logfile:
            for line in logfile.xreadlines():
                yield line + "</br>"

if __name__=="__main__":
    app = web.application(urls, globals())
    web.internalerror = web.debugerror
    app.run()
