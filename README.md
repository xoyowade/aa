# Prerequisites

- Python 2.4 or later

- "[web.py](http://webpy.org/)", a web framework

- "[KirbyBase](http://www.netpromi.com/kirbybase_python.html)", a plain-text database

- "[PyYAML](http://pyyaml.org/)", used to process yaml configuration file

# Initialize Database

1. Create a name list file, which consists of each user's id and name ( Seperated with TAB, one record one line, as in `sample_name_list` ).

2. Execute `data.py` to initialize database with the name list.  
```
python data.py $NAME_LIST_FILE
```

# Run Server

1. Edit `aa.yml` to configue your own AA system.

2. Run server. Port is optional, default 8080. 
```
python index.py $PORT &>$AA_LOG &
```