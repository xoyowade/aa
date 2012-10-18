import yaml

f = open('aa.yml')
conf = yaml.load(f)
f.close()

### Configurations ###

db_file = conf["database_file"]
send_mail_swtich = conf["send_mail_switch"]
log_file = conf["log_file"]
domain = conf["domain"]
admin_mail = conf["admin_mail"]
smtp_server_addr = conf["smtp_server"]
