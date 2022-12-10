# main.py
from flask import Flask
import asyncio
from vx_api import get_vx_api_token
from vx_api import vx_api_get
from extension_api import get_all_proficiencies
from extension_api import get_all_outcomes_links
from extension_api import get_all_subjects
from app import app

# from tasks.get_courses_outcomes_list import get_courses_outcomes_list
# from tasks.get_terms import get_terms
# from tasks.get_courses import get_courses
# from tasks.get_assignments import get_assignments
# from tasks.get_results import get_results
# from tasks.get_outcomes import get_outcomes
# from tasks.get_sections import get_sections
# from tasks.update_sheet import update_sheet
# from tasks.get_outcomes_list import get_outcomes_list
# from tasks.update_outcomes_sheet import update_outcomes_sheet
import time


##################################################### 
# 
# Parameters
#
##################################################### 



##################################################### 
# 
# App Routes
#
##################################################### 

@app.route("/")
def main():
    return 'Choose a route.'

@app.route("/update_grades/<campus>")
def update_grades(campus):
    # define school id
    if campus == 'sp':
        school_id = 3

    # get all final proficiencies (Canvas Extension DB)
    proficiencies = asyncio.run(get_all_proficiencies(school_id))
    
    # get all outcomes links (Canvas Extension DB)
    outcomes_links = asyncio.run(get_all_outcomes_links(school_id))

    # get all subjects (Canvas Extension DB)
    subjects = asyncio.run(get_all_subjects(school_id))

    # add veracrossSubjectID to each proficiency
    for p in proficiencies:
        for l in outcomes_links:
            if p['outcomeLinkID'] == l['outcomeLinkID']:
                p['outcomeID'] = l['outcomeID']
                p['courseID'] = l['courseID']
                p['subjectID'] = l['subjectID']

    for p in proficiencies:
        for s in subjects:
            if p['subjectID'] == s['subjectID']:
                p['subjectName'] = s['subjectName']
                p['gradeLevel'] = s['gradeLevel']
                p['veracrossSubjectID'] = s['veracrossSubjectID']
                p['academicYear'] = s['academicYear']

    # get Veracross classes list
    semaphore = asyncio.Semaphore(20)

    classes = asyncio.run(vx_api_get(semaphore,'classes',campus))
    if classes:
        token = classes['token']

    # identify the assessed classes
    subjects_assessed =[]
    for p in proficiencies:
        if p['veracrossSubjectID'] not in subjects_assessed:
            subjects_assessed.append(p['veracrossSubjectID'])

    classes_assessed = []
    for s in subjects_assessed:
        for c in classes['data']:
            if s == c['course']['id']:
                if c['id'] not in classes_assessed:
                    print(c['course']['name'])
                    classes_assessed.append(c['id'])
    print(classes_assessed)

    # get Veracross Qualitative Grades for each class assessed
    grades = asyncio.run(vx_api_get(semaphore,'classes',campus))
    for c in classes_assessed:
        classes = asyncio.run(vx_api_get(semaphore,'classes',campus))
        if classes:
            token = classes['token']


    # print(grades['token'])

    return 'OK!'

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=9000, debug=True)