from googleapiclient.discovery import build
import mimetypes
import os

def submitwork(creds, classname, assignment_name, file_path):
    service = build('classroom', 'v1', credentials=cred)
    class_id = None
    courses = service.courses().list().execute()
    for course in courses['courses']:
        if course['name'] == class_name:
            class_id = course['id']
            break

    if class_id is None:
        print("Class not found.")
        return

    assignment_id = None
    course_works = service.courses().courseWork().list(courseId=class_id).execute()
    for course_work in course_works['courseWork']:
        if course_work['title'] == assignment_name:
            assignment_id = course_work['id']
            break
    file_name = os.path.basename(file_path)
    mime_type, _ = mimetypes.guess_type(file_path)
    media = service.courses().courseWork().studentSubmissions().turnIn(
        courseId=class_id,
        courseWorkId=assignment_id,
        body={},
        media_body=file_path,
        media_mime_type=mime_type
    ).execute()
    return True
