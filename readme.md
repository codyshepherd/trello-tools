# trello-tools

One or more command-line tools for doing stuff with your Trello boards.

### history.py

Generate a scatterplot from the cards and datetime comments therein from a
given trello board and list.

e.g.

```
python history.py 'My Board' 'Automated Notifications List' \
  -c path/to/my/trello/creds.yaml \
  -t 'Title of My Scatterplot'
```

### Install

`pip install -r requirements.txt` in your favorite python >= 3.7 environment
