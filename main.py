# -*- coding: utf-8 -*-

""" AA accounting system """

from optparse import OptionParser
import sys
from time import strftime, localtime

import web

import conf
import data
import utils

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
            self.date = strftime("%Y-%m-%d", localtime())
            if localtime().tm_hour < 15:
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
        with open(conf.log_file, "r+") as logfile:
            for line in logfile.xreadlines():
                yield line + "</br>"

if __name__=="__main__":
    # load parameters
    parser = OptionParser()
    parser.add_option("-b", "--bind", type="string", dest="bind",
      default="0.0.0.0:8080", help="set ip and port to bind [default: %default]")
    parser.add_option("-c", "--config", type="string", dest="conf_file",
      default="aa.yml", help="set path to the configuration file [default: %default]")
    parser.add_option("-g", "--generate_database", action="store_true", dest="generate_database",
      default=False, help="generate an empty database, with the name_list given in \"-l\" [default: %default]")
    parser.add_option("-l", "--name_list", type="string", dest="name_list",
      default="sample_name_list", help="set the name_list file used to generate database [default: %default]")
    (options, args) = parser.parse_args()

    # load configuration file
    conf.load(options.conf_file)
    print "load config %s" % options.conf_file

    # init database
    data.init(conf.db_file)

    # generate an empty database
    if options.generate_database:
        data.generate(options.name_list)
        # clear the activity log
        with open(conf.log_file, "w") as logfile:
            pass
        print "generate database with %s" % options.name_list
        print "clear activity log %s" % conf.log_file
        sys.exit(0)

    # run webpy server
    # webpy assumes the 1st param to be port
    sys.argv = [sys.argv[0], options.bind]
    app = web.application(urls, globals())
    web.internalerror = web.debugerror
    app.run()
