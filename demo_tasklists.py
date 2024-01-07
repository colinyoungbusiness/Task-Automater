import pandas as pd
from google_functions import Create_Service, convert_to_RFC_datetime

CLIENT_SECRET_FILE = "New_Tasks_automater/client_secret_file.json"
API_NAME = "tasks"
API_VERSION = "v1"
SCOPES = ["https://www.googleapis.com/auth/tasks"]

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


### Insert method

tasklistBitches = service.tasklists().insert(
    body={'title':'Bitches im tryna hit up'}
).execute()


### Insert a bunch of lists

for i in range(5):
    service.tasklist().insert(body={'title':'Tasklist #{0}'.format(i+1)}).execute()


### List method

response = service.tasklists().list().execute()
listItems = response.get('items')
nextPageToken = response.get('nextPageToken')

while nextPageToken:
    response = service.tasklists().list(
        maxResults = 30,
        pageToken = nextPageToken
    ).execute()
    listItems.extend(response.get('items'))
    nextPageToken = response.get('nextPageToken')

print(pd.DataFrame(listItems))

'''
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 500)
pd.set_option('display.min_rows', 500)
pd.set_option('display.max_colwidth', 150)
pd.set_option('display.width', 120)
pd.set_option('expand_frame_repr', True)
'''

### Delete method

'''
All of this stuff below is how to delete a ton of 
test lists if you made those but i didn't so it's all good
'''

for item in listItems:
    try:
        if isinstance(int(item.get('title').replace('Tasklist #','')), int):
            if int(item.get('title').replace('Tasklist #','')) > 50:
                print(int(item.get('title').replace('Tasklist #','')))
                # service.tasklist().delete(tasklist=item.get('id')).execute()
    except:
        pass

response = service.tasklists().list(maxResults=100).execute()
print(pd.DataFrame(response.get('items')))

### Update Method

Bitcheslist = response.get('items')[2]
Bitcheslist['title'] = 'Bitches i DID hit'
service.tasklists().update(tasklist=Bitcheslist['id'], body=Bitcheslist).execute()

print(Bitcheslist['title'])

### Get Method

listGet = service.tasklists().get(tasklist='WmV0XzdIZlJwVEdXcHlWNg').execute()
print(listGet)