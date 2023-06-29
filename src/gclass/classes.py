import datetime
from googleapiclient.discovery import build

#SCOPES = ['https://www,googleapis.com/auth/classroom.courses.readonly']

def classnametoid(creds, classname):
    service = build('classroom', 'v1', credentials=creds)
    courses = service.courses().list().execute()
    return next((course['id'] for course in courses.get('courses', []) if course['name'] == classname), None)

def getclasses(creds):
    service = build('classroom', 'v1', credentials=creds)
    courses = service.courses().list().execute()
    if 'courses' in courses:
        return courses['courses']
    return None

def getassignments(creds, classname, status='done', due_date=datetime.datetime.now()):
    class_id = classnametoid(creds, classname)
    service =build('classroom', 'v1', credentials=creds)
    due_date = due_date.isoformat()
    assignments = service.courses().coursework().list(courseId=class_id).execute()
    return [assignment for assignment in assignments.get('courseWork', [])
    if assignment['state'] == 'PUBLISHED'
    and assignment.get('dueDate')
    and (
        (status == 'done' and assignment['dueDate']['dueDate'] < due_date)
        or (status == 'missing' and assignment['dueDate']['dueDate'] < due_date and 'submissionHistory' not in assignment)
        or (status == 'not_done' and assignment['dueDate']['dueDate'] >= due_date)
    )
]

def getclasscomments(creds, classname):
    class_id = classnametoid(creds, classname)
    service = build('classroom', 'v1', credentials=creds)
    comments = service.courses().announcements().list(courseId=class_id).execute()
    return [
    comment.get('text', '').strip()
    for comment in comments.get('announcements', [])
    if comment.get('text', '').strip()
]
