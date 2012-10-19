import sys
import yaml

db_file = ""
send_mail_swtich = ""
log_file = ""
domain = ""
admin_mail = ""
smtp_server_addr = ""

def load(conf_file):
	f = open(conf_file)
	conf = yaml.load(f)
	f.close()

	### Configurations ###
	m = sys.modules[__name__]

	m.db_file = conf["database_file"]
	m.send_mail_swtich = conf["send_mail_switch"]
	m.log_file = conf["log_file"]
	m.domain = conf["domain"]
	m.admin_mail = conf["admin_mail"]
	m.smtp_server_addr = conf["smtp_server"]