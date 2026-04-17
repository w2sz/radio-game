import json


# Clears data from logs.json

with open('logs.json', 'w') as f:
    json.dump([], f)
