import datetime
import pickle
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request


def Create_Service(client_secret_file, api_name, api_version, *scopes):
    print(client_secret_file, api_name, api_version, scopes, sep='-')
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    print(SCOPES)

    cred = None

    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
    # print(pickle_file)

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            try:
                cred.refresh(Request())
            except Exception as e:
                print(f"Error refreshing credentials: {e}")
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        # Save the new credentials only if they are valid
        if cred.valid:
            with open(pickle_file, 'wb') as token:
                pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print(e)
        print(f'Failed to create service instance for {API_SERVICE_NAME}')
        return None

def convert_to_RFC_datetime(year=2023, month=12, day=12, hour=23, minute=59):
    dt = datetime.datetime(year, month, day, hour, minute, 0, 000).isoformat() + 'Z'
    return dt

def construct_request_body(title, notes=None, due=None, status='needsAction', deleted=False):
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

def convert_from_mdy(input_date='mm/dd/yyyy'):
    raw_date = datetime.strptime(input_date, "%m/%d/%Y")
    dt = raw_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    return dt

def format_date_with_suffix(input_date_str):
    try:
        # Parse the input date string
        input_date = datetime.datetime.strptime(input_date_str, "%m/%d/%Y")

        # Format the parsed date as "Month Day" format
        formatted_date = input_date.strftime("%B %#d")

        # Add a variable that holds the year
        f_year = input_date.strftime('%Y')

        # Add the appropriate suffix (e.g., "st", "nd", "rd", or "th") to the day
        day = input_date.day
        if 10 <= day % 100 <= 20:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")

        # Combine the formatted month and day with the suffix
        formatted_date_with_suffix = f"{formatted_date}{suffix}{' '}{f_year}"

        return formatted_date_with_suffix

    except ValueError:
        return ''  # Invalid date format