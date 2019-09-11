from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

#
# Google Calendar event generator for class assignments
#
# To use:
#   1) Change <your_email@here.com> to your email
#   2) Modify settings below as necessary to set information for assignments' description, due time, etc.
#   3) Add a new entry to event_entries for each individual assignment due date
#      Each new entry is a list of 3 strings with format: [month, day, title of assignment]
#   4) Run this python file to add events to Google Calendar
#   *Note: You may have to generate a new credential file for adding events to your Google Calendar the
#    first time you run this script

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

# settings for all assignment entries
EMAIL = '<your-email@here.com>' # change this to your email
# events' year and time
YEAR = '2019'
HOUR = '23' # 24 hour format
MINUTE = '59'
# events' text information
SUMMARY_PREFIX = '' # prefix for assignment titles
SUMMARY_SUFFIX = '' # suffix for assignment titles
LOCATION = ''
DESCRIPTION = ''
# color of calendar entry, see https://developers.google.com/calendar/v3/reference/colors
# for more information
COLOR_ID = 9  # 11 = tomato
              # 9 = dark blue

# each entry is a list of [month, day, summary (title of assignment)]
event_entries = [
    ['1', '1', 'Assignment 1'],
    ['1', '2', 'Assignment 2']
]

"""
    Returns formatted datetime given month and day
"""
def create_time(month, day):
    return '{year}-{month}-{day}T{hour}:{minute}:00'.format(
        year=YEAR, month=month, day=day, hour=HOUR, minute=MINUTE
    )

"""
    Returns an event dictionary object generated from parameters that can be passed
    to the Google Calendar API call. 
"""
def create_event(startTime, endTime, colorId, summary, location, description):
    # '2015-05-28T17:00:00-07:00'
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'colorId': colorId,
        'start': {
            'dateTime': startTime,
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': endTime,
            'timeZone': 'America/New_York',
        },
        'attendees': [
            {'email': EMAIL, 'responseStatus': 'accepted'}
        ],
        'reminders': {
            'useDefault': True,
        },
    }

    return event

"""
    Returns list of event dictionary objects generated from event_entries and settings
    defined above.
"""
def get_events():
    events = []
    for entry in event_entries:
        month, day, summary = entry
        full_summary = SUMMARY_PREFIX + summary + SUMMARY_SUFFIX
        location = LOCATION
        description = DESCRIPTION
        colorId = COLOR_ID
        datetime = create_time(month, day)
        events.append(create_event(datetime, datetime, colorId, full_summary, location, description))
    return events


def main():
    """Shows basic usage of the Google Calendar API.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    for event in get_events():
        created_event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % (created_event.get('htmlLink')))

if __name__ == '__main__':
    main()
