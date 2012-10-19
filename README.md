# AA accounting system

AA is a Chinese term for "Going Dutch", which means persons participating a common activity pay for themselves.   
AA accounting system comes out to help a constant group of people to record their regular actives (f.g. having lunch with colleagues in work day) and split the bills automatically. After each activity, AA would record the bill, update account for every person involved, and send a mail to inform every one of the latest updates.

# Prerequisites

- Python 2.4 or later

- "[web.py](http://webpy.org/)", a web framework

- "[KirbyBase](http://www.netpromi.com/kirbybase_python.html)", a plain-text database

- "[PyYAML](http://pyyaml.org/)", used to process yaml configuration file

# Initialize Database

1. Create a name list file, which consists of each user's id and name ( Separated with TAB, one record one line, as in `sample_name_list` ).

2. Execute `data.py` to initialize database with the name list.  
```
python data.py $NAME_LIST_FILE
```

# Run Server

1. Create your own configuration based on `aa.yml`.

2. Run server. `PORT` and `CONFIG_FILE` are both optional, with default value `8080` and `aa.yml` separately. 
```
python index.py $PORT $CONFIG_FILE &>$AA_LOG &
```