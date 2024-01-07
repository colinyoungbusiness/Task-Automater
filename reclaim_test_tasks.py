import pandas as pd
import csv
from google_functions import Create_Service, construct_request_body, format_date_with_suffix

CLIENT_SECRET_FILE = "New_Tasks_automater/client_secret_file.json"
API_NAME = "tasks"
API_VERSION = "v1"
SCOPES = ["https://www.googleapis.com/auth/tasks"]

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

response = service.tasklists().list(maxResults=100).execute()
reclaimList = response.get('items')[1]
reclaimListId = reclaimList['id']

### Actually creating tasks

# Replace 'your_file.csv' with the path to your CSV file
csv_file_path = 'New_Tasks_automater/conappssched2.csv'

with open(csv_file_path, mode='r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header row if it exists

    prev_row = ['','']  # To store the previous row

    for row in csv_reader:
        if prev_row:

            responseNewTask = service.tasks().insert(
                tasklist=reclaimListId,
                body=construct_request_body('CA' + row[1] + ' (for 2hr due ' + format_date_with_suffix(row[0]) + ' not before ' + format_date_with_suffix(prev_row[0]) + ')')
            ).execute()

        prev_row = row  # Update the previous row for the next iteration



'''
The Google Task integration supports natural language to create Tasks. In addition to being a fast way to add Tasks to Reclaim, one benefit of using natural language is that you can express options for the Task that are not natively supported by Google Tasks.
The general syntax for Google Tasks is as follows, and should be entered into the Title field of Google Tasks: TITLE ([DURATION] [DUE_DATE] [NOT_BEFORE] [TYPE])
The TITLE is required, and the additional text in the parenthesis is optional fine-tuning of the Task. Refer to Tasks overview for a description of each field.
Once synced, Reclaim will automatically strip out other parameters besides the title, so your calendar events and Google Tasks won't have a lot of extra words on them when they're placed on your calendar.
Examples
To create a work task for "Build slide deck" for four hours by next Friday, you would enter Build slide deck (for 4h due next Friday)
To create a personal task for "Mow the lawn" for one hour (default) by this Sunday, you would type Mow the lawn (type personal due sunday)
To create a work task for "Get back to CEO" for 30m by September 21st, not to be started before September 15th, you would type Get back to CEO (for 30m due sept 21 not before sept 15)
'''

# assignment_name = 'HW1'
# previous_date = '9/3/2023'
# input_date = '9/5/2023'
# output_date = format_date_with_suffix(input_date)
# output_previous_date = format_date_with_suffix(previous_date)
# print(assignment_name + ' (due ' + output_date + ' not before ' + output_previous_date + ')')

# responseNewTask = service.tasks().insert(
#     tasklist=reclaimListId,
#     body=construct_request_body('Do HW1 (due ' + output_date + ' )')
# ).execute()

# csv_file_path = 'New_Tasks_automater/conappssched2.csv'

# with open(csv_file_path, mode='r') as file:
#     csv_reader = csv.reader(file)
#     next(csv_reader)  # Skip the header row if it exists

#     prev_row = ['','']  # To store the previous row

#     for row in csv_reader:
#         if prev_row:

#             print(row[1] + ' (due ' + format_date_with_suffix(row[0]) + ' not before ' + format_date_with_suffix(prev_row[0]) + ')')

#         prev_row = row  # Update the previous row for the next iteration