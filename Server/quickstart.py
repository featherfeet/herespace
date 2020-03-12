"""
https://developers.google.com/classroom/guides/manage-coursework
https://developers.google.com/classroom/guides/auth
https://developers.google.com/classroom/reference/rest/v1/courses.courseWork.studentSubmissions
"""

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly', 'https://www.googleapis.com/auth/classroom.coursework.students']

"""Shows basic usage of the Classroom API.
Prints the names of the first 10 courses the user has access to.
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

service = build('classroom', 'v1', credentials=creds)

# Call the Classroom API
results = service.courses().list(pageSize=10).execute()
courses = results.get('courses', [])

if not courses:
    print('No courses found.')
else:
    print('Courses:')
    for course in courses:
        print(course['name'])

courseWork = {
  'title': 'Test Assignment',
  'description': 'Ignore this assignment. I\'m testing a program I made that interacts with Google Classroom. See y\'all tomorrow at Hart!',
  'materials': [
     {'link': { 'url': 'http://olivertrevor.tech' }}
],
  'workType': 'ASSIGNMENT',
  'state': 'PUBLISHED',
}
courseWork = service.courses().courseWork().create(
    courseId='47229055142', body=courseWork).execute()
print('Assignment created with ID {0}'.format(courseWork.get('id')))
