# main.py
from flask import Flask
from tasks.get_courses_outcomes_list import get_courses_outcomes_list
from tasks.get_terms import get_terms
from tasks.get_courses import get_courses
from tasks.get_assignments import get_assignments
from tasks.get_results import get_results
from tasks.get_outcomes import get_outcomes
from tasks.get_sections import get_sections
from tasks.update_sheet import update_sheet
from tasks.get_outcomes_list import get_outcomes_list
from tasks.update_outcomes_sheet import update_outcomes_sheet
import asyncio
import time

app = Flask(__name__)


##################################################### 
# 
# Parameters
#
##################################################### 

base_url = 'https://avenuessp.instructure.com'
#base_url = 'https://avenuessv.instructure.com'
#base_url = 'https://avenues.instructure.com'

sheets_urls = {
    '6th Grade': '[22-23] CP Gradebook - 6th Grade',
    '7th Grade': '[22-23] CP Gradebook - 7th Grade',
    '8th Grade': '[22-23] CP Gradebook - 8th Grade',
    '9th Grade': '[22-23] CP Gradebook - 9th Grade',
    '10th Grade': '[22-23] CP Gradebook - 10th Grade',
    '11th Grade': '[22-23] CP Gradebook - 11th Grade',
    '12th Grade': '[22-23] CP Gradebook - 12th Grade',
}
model_tab = '[MODEL]'

graduation_years = [
    {'year': '29', 'grade': '6th Grade'},
    {'year': '28', 'grade': '7th Grade'},
    {'year': '27', 'grade': '8th Grade'},
    {'year': '26', 'grade': '9th Grade'},
    {'year': '25', 'grade': '10th Grade'},
    {'year': '24', 'grade': '11th Grade'},
    {'year': '23', 'grade': '12th Grade'},
]
subjects_codes = {
    'a': 'Art & Design',
    'wc': 'World Course',
    'e': 'English',
    's': 'Science',
    'm': 'Music'
}
account_id = '1'
terms_SIS_ids = ['50.2022', '42.2022']
cpa_title = '[CPA] Cumulative Performance Assignment'

# outcomes list
#outcomes_sheet_url = '[21-22] Semester 2 Outcomes List - VX - V2'
#outcomes_sheet_url = '[22-23] Semester 1 Outcomes List - SV'
outcomes_sheet_url = '[22-23] Semester 1 Outcomes List - NY'
outcomes_period = { 
    'start': '2022-01-01T00:00:00Z',
    'end': '2022-12-31T00:00:00Z'
}

# courses exclusion list
courses_exclusion_list = [
    #2637, 2643, 3188, 2727, 2709, 2996, 2991, 3026, 3027, 2735, 3123,
    #2658, 3008, 3123, 2703, 2698, 2992, 3032, 3123, 2716, 3170, 3006,
]

# assignments exclusion list
assignments_exclusion_list = [
    #24529, 23675, 24529, 24408
]

# outcomes exclusion
outcomes_exclusion_list = [
    # { "26263": "6390" }, #assignment_id: outcome_id 
    # { "26846": "6973" }
]

##################################################### 
# 
# App Routes
#
##################################################### 

@app.route("/")
def main():
    
    # Get relevant terms IDs
    terms = asyncio.run(get_terms(base_url,account_id,terms_SIS_ids))
    #print(terms)

    # Get active courses
    courses = asyncio.run(get_courses(base_url,account_id,terms,courses_exclusion_list))
    #print(courses)

    # Get CPA assignments
    assignments = asyncio.run(get_assignments(base_url,courses,cpa_title,assignments_exclusion_list,outcomes_exclusion_list))
    #print(assignments)

    # Get outcomes list
    outcomes = asyncio.run(get_outcomes(base_url,courses))
    #print(outcomes)

    # Get sections and their students
    sections = asyncio.run(get_sections(base_url,courses))
    #print(sections)

    # Get CPA results
    results = asyncio.run(get_results(base_url,assignments,outcomes,sections,graduation_years,subjects_codes,outcomes_exclusion_list))
    #print(results)

    #Update each grade-level sheet
    for grade in sheets_urls.keys():
        update_sheet(sheets_urls[grade],results,model_tab,grade)
        print(grade + ' results successfully gotten.')
        time.sleep(30)

    return 'Results successfully gotten.'


@app.route('/cpa-outcomes-list')
def cpa_outcomes_list():
    # Get relevant terms IDs
    terms = asyncio.run(get_terms(base_url,account_id,terms_SIS_ids))
    #print(terms)

    # Get active courses
    courses = asyncio.run(get_courses(base_url,account_id,terms,courses_exclusion_list))
    #print(courses)

    # courses = [{'name': '10th_PBL', 'id': 3054}]

    # Get CPA assignments
    assignments = asyncio.run(get_assignments(base_url,courses,cpa_title,assignments_exclusion_list,outcomes_exclusion_list,True))
    #print(assignments)

    # Get outcomes list aligned on the CPAs
    outcomes = asyncio.run(get_outcomes_list(base_url,assignments,graduation_years,outcomes_period,subjects_codes))
    #print(outcomes)

    # Update the outcomes list sheet
    update_outcomes_sheet(outcomes_sheet_url,outcomes)

    return 'Outcomes list successfully updated.'

@app.route('/all-outcomes-list')
def all_outcomes_list():
    # Get relevant terms IDs
    terms = asyncio.run(get_terms(base_url,account_id,terms_SIS_ids))
    #print(terms)

    # Get active courses
    courses = asyncio.run(get_courses(base_url,account_id,terms,courses_exclusion_list))
    #print(courses)

    # Get outcomes list
    outcomes = asyncio.run(get_courses_outcomes_list(base_url,courses,graduation_years,subjects_codes))
    #print(outcomes)
    
    # Update the outcomes list sheet
    update_outcomes_sheet(outcomes_sheet_url,outcomes)

    return 'Outcomes list successfully updated.'

@app.route('/outcomes-results')
def outcomes_results():
    # Get relevant terms IDs
    terms = asyncio.run(get_terms(base_url,account_id,terms_SIS_ids))
    print(terms)

    # Get active courses
    courses = asyncio.run(get_courses(base_url,account_id,terms,courses_exclusion_list))
    print(courses)

    # Get assignments
    assignments = asyncio.run(get_assignments(base_url,courses,None,assignments_exclusion_list,outcomes_exclusion_list))
    print(assignments)

    # Get outcomes list
    outcomes = asyncio.run(get_outcomes(base_url,courses))
    print(outcomes)

    # Get sections and their students
    sections = asyncio.run(get_sections(base_url,courses))
    print(sections)

    # Get CPA results
    results = asyncio.run(get_results(base_url,assignments,outcomes,sections,graduation_years,subjects_codes,outcomes_exclusion_list))
    #print(results)

    # Update sheet
    update_sheet('Outcome Results Analysis',results,model_tab,'10th Grade')

    return 'Results successfully gotten.'