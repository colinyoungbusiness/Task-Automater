import pandas as pd
from google_functions import Create_Service, convert_to_RFC_datetime

CLIENT_SECRET_FILE = "New_Tasks_automater/client_secret_file.json"
API_NAME = "tasks"
API_VERSION = "v1"
SCOPES = ["https://www.googleapis.com/auth/tasks"]

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

### Tasklist creation
### List method from the tasklists

response = service.tasklists().list().execute()
listItems = response.get('items')
nextPageToken = response.get('nextPageToken')

while nextPageToken:
    response = service.tasklists().list(
        maxResults = 50,
        pageToken = nextPageToken
    ).execute()
    listItems.extend(response.get('items'))
    nextPageToken = response.get('nextPageToken')


print(pd.DataFrame(listItems))

pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 500)
pd.set_option('display.min_rows', 500)
pd.set_option('display.max_colwidth', 150)
pd.set_option('display.width', 120)
pd.set_option('expand_frame_repr', True)

#bitchesListid = 'WmV0XzdIZlJwVEdXcHlWNg'
bitchesListid = 'ZTZWdnJvcE5HZXhmV0JRMg'

### Insert method

### Our first task

title = 'Hot Men to Fuck'
notes = 'mostly kyle peng'
due = ''
status = 'needsAction'
deleted = False

request_body = {
    'title': title,
    'notes': notes,
    'due': due,
    'deleted': deleted,
    'status': status
}

response = service.tasks().insert(
    tasklist=bitchesListid,
    body=request_body
).execute()

responseHotMen = response

### Our task creation function with default values

def construct_request_body(title, notes=None, due=None, status='needsAction, deleted=False'):
    try:
        request_body = {
        'title': title,
        'notes': notes,
        'due': due,
        'deleted': deleted,
        'status': status
        }
        return request_body
    except Exception:
        return None
    

### Our second task

responseMoreMen = service.tasks().insert(
    tasklist=bitchesListid,
    body=construct_request_body('Hotter Men'),
    previous=responseHotMen.get('id')
).execute()

### Our third task

responseEvenMoreMen = service.tasks().insert(
    tasklist=bitchesListid,
    body=construct_request_body('Hottest Men'),
    previous=responseMoreMen.get('id')
).execute()

responseMoreDylan = service.tasks().insert(
    tasklist=bitchesListid,
    parent=responseMoreMen.get('id'),
    body=construct_request_body(
        'Dylan W',
        notes = 'Fat and short',
        due = convert_to_RFC_datetime(2023, 9, 5, 22, 0)
    )
).execute()

### A bunch of dummy tasks

for i in range(5):
    service.tasks().insert(
        tasklist=bitchesListid,
        parent=responseHotMen.get('id'),
        body=construct_request_body(
            "Dummy Task #{0}", format(i+1),
            due = convert_to_RFC_datetime(2023,(i%12)+1,6,22,0)
        )
    ).execute()

### List method

# This is showing the list of everything due before the seventh of September

response = service.tasks().list(
    tasklist=bitchesListid,
    #dueMin=convert_to_RFC_datetime(2023,3,7),
    showCompleted=False
).execute()
listItems = response.get('items')
nextPageToken = response.get('nextPageToken')

while nextPageToken:
    response = service.tasks().list(
    tasklist=bitchesListid,
    #dueMax=convert_to_RFC_datetime(2024,3,7),
    showCompleted=False,
    pageToken=nextPageToken
    ).execute()
    listItems = response.get('items')
    nextPageToken = response.get('nextPageToken')
    
print(pd.DataFrame(listItems))

### Delete Method

# What's crazy is that this loop then iterates over that list of
# everything due before the seventh and then deletes all of it

for item in listItems:
    service.tasks().delete(tasklist=bitchesListid,task=item.get('id')).execute()

### Update Method

# The code below gets a list of all the tasks due between the fourth
# and the seventh of September then iterates over the list and updates
# them

response = service.tasks().list(
    tasklist=bitchesListid,
    dueMin=convert_to_RFC_datetime(2023,9,4),
    dueMax=convert_to_RFC_datetime(2023,9,7),
    showCompleted=False
).execute()
listItems = response.get('items')
nextPageToken = response.get('nextPageToken')

while nextPageToken:
    response = service.tasks().list(
    tasklist=bitchesListid,
    dueMin=convert_to_RFC_datetime(2023,9,4),
    dueMax=convert_to_RFC_datetime(2023,9,7),
    showCompleted=False,
    pageToken=nextPageToken
).execute()
    listItems = response.get('items')
    nextPageToken = response.get('nextPageToken')

for taskItem in listItems:
    taskItem["status"] = 'completed'
    service.tasks().update(
        tasklist=bitchesListid,
        task=taskItem.get('id'),
        body=taskItem
    ).execute()

### Clear Method

# This just gets rid of the tasks from the list. So if you want
# to clear up space after completing a bunch of tasks you can 
# use this to then remove them from the tasklist

response = service.tasks().list(
    tasklist=bitchesListid,
    dueMin=convert_to_RFC_datetime(2023,9,7),
    dueMax=convert_to_RFC_datetime(2023,9,10),
    showCompleted=True,
    showHidden=True
).execute()
listItems = response.get('items')
nextPageToken = response.get('nextPageToken')

while nextPageToken:
    response = service.tasks().list(
    tasklist=bitchesListid,
    dueMin=convert_to_RFC_datetime(2023,9,4),
    dueMax=convert_to_RFC_datetime(2023,9,7),
    showCompleted=True,
    showHidden=True,
    pageToken=nextPageToken
).execute()
    listItems = response.get('items')
    nextPageToken = response.get('nextPageToken')

service.tasks().clear(tasklist=bitchesListid).execute()

### Move method

response = service.tasks().list(
    tasklist=bitchesListid,
    maxResults = 100
).execute()
listItems = response.get('items')
nextPageToken = response.get('nextPageToken')

print(pd.DataFrame(listItems))

# This will attempt to move Dylan Wahl behind Dylan W
service.tasks().move(
    tasklist=bitchesListid,
    task='UV9VMFRZU3ktTHdLX1U1cA', # Dylan Wahl
    parent='VGtPM3JWNmRhTmlDVnVGWA', # Hotter Men
    previous='emJDWlZsWW5naXRZaFptcg' # Dylan W
).execute()

