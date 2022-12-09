# get_results.py
import asyncio
from aiohttp import ClientSession
from canvas_api import canvas_get
from utiliy import grade_level
from copy import deepcopy


##################################################### 
# 
# Get CPA results
#
##################################################### 

async def get_results(base_url,assignments,outcomes,sections,graduation_years,subjects_codes,outcomes_exclusion_list):

    semaphore = asyncio.Semaphore(20)

    async with ClientSession() as client:
        url = base_url + '/api/v1/courses/{c_id}/assignments/{a_id}/submissions'
        params = [
            ('include[]', 'full_rubric_assessment'),
            ('include[]', 'user'),
            ('per_page', '100'),
        ]

        resp = await asyncio.gather(*[
            asyncio.create_task(canvas_get(semaphore, url.format(c_id = a['course']['id'], a_id = a['id']), client, resp_data=[], params=params))
            for a in assignments
        ])

        results = []
        for assignment in resp:
            for submission in assignment:
                if 'full_rubric_assessment' in submission:
                    for outcome in submission['full_rubric_assessment']['data']:
                        if 'points' in outcome:
                            result = {
                                'subject': '',
                                'course_id': '',
                                'course_name': '',
                                'assignment_id': submission['assignment_id'],
                                'assignment_date': '',
                                'student_id': submission['user']['id'],
                                'student_name': submission['user']['sortable_name'],
                                'student_section': '',
                                'student_grade': grade_level(submission['user'],graduation_years),
                                'outcome_id': str(outcome['learning_outcome_id']),
                                'outcome_title': '',
                                'result': str(outcome['points'])[:1],
                                'cpa': '',
                                'type': ''
                            }
                            if { str(result['assignment_id']): str(result['outcome_id']) } not in outcomes_exclusion_list:
                                results.append(result)

        for r in results:
            for a in assignments:
                if r['assignment_id'] == a['id']:
                    r['assignment_date'] = a['date']
                    r['course_id'] = a['course']['id']
                    r['course_name'] = a['course']['name']

            for o in outcomes:
                if r['outcome_id'] == o['id']:
                   r['outcome_title'] = o['title']

            for s in sections:
                if r['course_id'] == s['course']:
                    for student in s['students']:
                        if str(student) == str(r['student_id']):
                            if len(s['name']) <= len(r['student_section']) or r['student_section'] == '':
                                r['student_section'] = s['name']

            if len(r['outcome_title']) > 0: 
                code = r['outcome_title'][-3:].replace('.','').replace(')','')
                code = ''.join([i for i in code if not i.isdigit()])
                if code in subjects_codes:
                    r['subject'] = subjects_codes[code]
                else:
                    r['subject'] = r['course_name']

            # workaround for portuguese outcomes with equal names
            for o in outcomes:
                if r['outcome_id'] == o['id']:
                    if 'Por_' in r['outcome_title']:
                        r['outcome_title'] = o['title']+' ['+str(o['id'])+']'        
            
        # add final proficiency for outcomes that were assessed twice for the same student
        results = [dict(tupleized) for tupleized in set(tuple(item.items()) for item in results)] #remove duplicates
        results = sorted(results, key=lambda d: d['assignment_id'])
        results = sorted(results, key=lambda d: (d['assignment_date'] is None, d['assignment_date']))  

        student_subject_outcome = []
        for r in results:
            sso =  {
                'student': r['student_id'],
                'outcome': r['outcome_title'],
                'subject': r['subject']
            }
            if sso not in student_subject_outcome:
                student_subject_outcome.append(sso)
        
        extra_results = []
        for sso in student_subject_outcome:
            cpas = []

            for r in results:
                if r['student_id'] == sso['student'] and r['outcome_title'] == sso['outcome'] and r['subject'] == sso['subject']:
                    if r not in cpas:
                        cpas.append(r)

            if len(cpas) > 1:
                scores_sum = 0
                scores_num = 0

                for cpa in cpas:
                    scores_num += 1
                    scores_sum += int(cpa['result'])

                new_result = deepcopy(cpas[0])

                new_result['assignment_id'] = 999999
                new_result['course_id'] = 999999
                new_result['assignment_date'] = None
                new_result['result'] = str(round(scores_sum / scores_num))
                new_result['type'] = 'Final Proficiency'

                if new_result not in extra_results:    
                    extra_results.append(new_result)
        
        for r in extra_results:
            if r not in results:
                results.append(r)
        
        #define CPAs numbers and type
        results = sorted(results, key=lambda d: d['assignment_id'])
        results = sorted(results, key=lambda d: (d['assignment_date'] is None, d['assignment_date']))
        results = sorted(results, key=lambda d: d['subject'])
        results = sorted(results, key=lambda d: d['outcome_title'])     
        results = sorted(results, key=lambda d: d['student_id'])

        index = 0
        for r in results:
            if index == 0:
                r['cpa'] = 1
                r['type'] = 'Final Proficiency'
            elif index > 0:
                if results[index-1]['student_id'] == r['student_id'] and results[index-1]['outcome_title'] == r['outcome_title'] and results[index-1]['subject'] == r['subject']:
                    try:
                        results[index+1]

                        if results[index+1] and results[index+1]['student_id'] == r['student_id'] and results[index+1]['outcome_title'] == r['outcome_title'] and results[index+1]['subject'] == r['subject']:
                            r['cpa'] = int(results[index-1]['cpa']) + 1
                            r['type'] = "Cumul Prof. " + str(r['cpa'])
                        else:
                            r['cpa'] = int(results[index-1]['cpa']) + 1
                            r['type'] = 'Final Proficiency'
                    except IndexError:
                        r['cpa'] = int(results[index-1]['cpa']) + 1
                        r['type'] = 'Final Proficiency'                 
                else:
                    try:
                        results[index+1]

                        if results[index+1]['student_id'] == r['student_id'] and results[index+1]['outcome_title'] == r['outcome_title'] and results[index+1]['subject'] == r['subject']:
                            r['cpa'] = 1
                            r['type'] = 'Cumul Prof. 1'
                        else:
                            r['cpa'] = 1
                            r['type'] = 'Final Proficiency'
                    except IndexError:
                            r['cpa'] = 1
                            r['type'] = 'Final Proficiency'               
            index += 1

        return results