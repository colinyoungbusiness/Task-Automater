import pandas as pd
from google_functions import convert_to_RFC_datetime, Create_Service, construct_request_body

CLIENT_SECRET_FILE = "New_Tasks_automater/client_secret_file.json"
API_NAME = "tasks"
API_VERSION = "v1"
SCOPES = ["https://www.googleapis.com/auth/tasks"]

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

responseInitial = service.tasklists().list(maxResults=100).execute()
reclaimList = responseInitial.get('items')[1]
reclaimListId = reclaimList['id']

responseList = service.tasks().list(
    maxResults=100,
    tasklist=reclaimListId,
).execute()
listItems = responseList.get('items')
nextPageToken = responseList.get('nextPageToken')

# print(pd.DataFrame(listItems))

# pd.set_option('display.max_columns', 100)
# pd.set_option('display.max_rows', 500)
# pd.set_option('display.min_rows', 500)
# pd.set_option('display.max_colwidth', 150)
# pd.set_option('display.width', 120)
# pd.set_option('expand_frame_repr', True)

for item in listItems:
    service.tasks().delete(tasklist=reclaimListId,task=item.get('id')).execute()