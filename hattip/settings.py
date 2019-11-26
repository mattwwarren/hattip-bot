import json
import os

CONFIG_FILE = 'config.json'
SETTINGS_KEYS = {'SLACK_BOT_OAUTH_TOKEN'}
SETTINGS = None

if os.path.isfile(CONFIG_FILE):
    with open('config.json') as fp:
        SETTINGS = json.load(fp)
else:
    for k in SETTINGS_KEYS:
        SETTINGS[k] = os.environ.get(k)

for k in SETTINGS_KEYS:
    if k not in SETTINGS:
        print('You are missing %s' % (k))
