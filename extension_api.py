from app import app, db
from sqlalchemy import text
from sqlalchemy.orm import load_only
from datetime import datetime, timedelta
from flask import session

with app.app_context():
    from models import Subjects
    from models import OutcomeLinks
    from models import Proficiencies
    from models import LetterGrades
    from models import ProficiencyValues
    from models import LetterGradeValues

async def get_all_proficiencies(campus_id: str):
    results = Proficiencies.query.filter_by(
        SchoolID=int(campus_id)
    ).all()

    proficiencies = []
    for r in results:
        proficiencies.append({
        'proficiencyID': r.ProficiencyID,
        'graderID': r.GraderID,
        'outcomeLinkID': r.OutcomeLinkID,
        'proficiencyValueID': r.ProficiencyValueID,
        'schoolID': r.SchoolID,
        'userID': r.UserID,
    })

    return proficiencies

async def get_all_outcomes_links(campus_id: str):
    results = OutcomeLinks.query.filter_by(
        SchoolID=int(campus_id)
    ).all()

    outcomes_links = []
    for r in results:
        outcomes_links.append({
        'outcomeLinkID': r.OutcomeLinkID,
        'outcomeID': r.OutcomeID,
        'courseID': r.CourseID,
        'subjectID': r.SubjectID,
        'schoolID': r.SchoolID,
    })

    return outcomes_links

async def get_all_subjects(campus_id: str):
    results = Subjects.query.filter_by(
        SchoolID=int(campus_id)
    ).all()

    subjects = []
    for r in results:
        subjects.append({
        'subjectID': r.SubjectID,
        'subjectName': r.SubjectName,
        'gradeLevel': r.GradeLevel,
        'veracrossSubjectID': r.VeracrossSubjectID,
        'schoolID': r.SchoolID,
        'academicYear': r.AcademicYear
    })

    return subjects

# async def get_subjects_for_school(user, campus_id: str, academic_year: str):
#     if permission(user, False):  # control access to teachers and admins
#         results = Subjects.query.filter_by(
#             SchoolID=int(campus_id),
# 			AcademicYear=academic_year
#         ).all()

#         subjects = []
#         for r in results:
#             subjects.append({
#                 'subjectID': r.SubjectID,
#                 'subjectName': r.SubjectName,
#                 'gradeLevel': r.GradeLevel
#             })
#     else:
#         return False

#     return subjects

# async def get_subjects(user, campus_id: str, academic_year: str, grade_levels: str):
# 	if permission(user, False):
# 		results = db.session.query(Subjects).filter(
# 			Subjects.SchoolID==int(campus_id),
# 			Subjects.AcademicYear==academic_year,
# 			Subjects.GradeLevel.in_(grade_levels.split(','))
# 		)

# 		subjects = []

# 		for r in results:
# 			subjects.append({
# 				'subjectID': r.SubjectID,
# 				'subjectName': r.SubjectName,
# 				'gradeLevel': r.GradeLevel
# 			})
# 	else:
# 		return False

# 	return subjects

# async def get_subjects_covered_by_course(base_url: str, access_token: str, user, course_id: int):
# 	if permission(user, False):
# 		results = db.session.execute('''
# SELECT			DISTINCT
# 				s.SubjectID,
# 				s.SubjectName,
# 				s.GradeLevel,
# 				s.SchoolID,
# 				s.AcademicYear,
# 				STRING_AGG(ol.OutcomeID, ',') AS OutcomeIDs
# FROM			Grading.OutcomeLinks ol
# 				JOIN Grading.Subjects s ON s.SubjectID = ol.SubjectID
# 					AND s.SchoolID = ol.SchoolID
# WHERE			ol.CourseID = :courseID
# GROUP BY		s.SubjectID,
# 				s.SubjectName,
# 				s.GradeLevel,
# 				s.SchoolID,
# 				s.AcademicYear''', { 'courseID': course_id })

# 		expired_token = session["canvas_oauth2_token"]["expires"] - datetime.now() <= timedelta(minutes=3)
# 		if expired_token:
# 			print('Token is expired')

# 		subjects = []
# 		for r in results:
# 			subjects.append({
# 				'subjectID': r.SubjectID,
# 				'subjectName': r.SubjectName,
# 				'gradeLevel': r.GradeLevel,
# 				'schoolID': r.SchoolID,
# 				'academicYear': r.AcademicYear,
# 				'outcomes': await canvas_api.outcomes_data(base_url, access_token, r.OutcomeIDs)
# 			})

# 		return subjects
# 	else:
# 		return False

# async def get_subject_for_outcome(outcome_id: int, course_id: int):
# 	result = OutcomeLinks.query.filter_by(
# 		OutcomeID=outcome_id,
# 		CourseID=course_id
# 	).first()

# 	if result == None:
# 		return None

# 	return result.SubjectID

# async def outcomes_links(user, campus_id: str, course_id: str):

#     if permission(user, True, course_id):  # control access to course's teachers and admins
#         results = OutcomeLinks.query.filter_by(
#             SchoolID=int(campus_id),
#             CourseID=int(course_id)
#         ).all()

#         outcomes_links = []
#         for r in results:
#             outcomes_links.append({
#                 'outcomeLinkID': r.OutcomeLinkID,
#                 'outcomeID': r.OutcomeID,
#                 'subjectID': r.SubjectID
#             })
#     else:
#         return False

#     return outcomes_links

# async def save_outcome_links(user, outcome_links):

# 	new_outcome_links = [];

# 	for outcome_link in outcome_links:
# 		new_outcome_link = await link_outcome_to_subject(user, outcome_link['schoolID'], outcome_link['courseID'], outcome_link['outcomeID'], outcome_link['subjectID'])

# 		if new_outcome_link != 400:
# 			new_outcome_links.append(new_outcome_link);
# 		else:
# 			return 400

# 	return outcome_links;

# async def link_outcome_to_subject(user, campus_id: str, course_id: str, outcome_id: str, subject_id: str):

# 	if permission(user, True, course_id):
# 		existent_links = OutcomeLinks.query.filter_by(
# 			OutcomeID=int(outcome_id),
# 			CourseID=int(course_id),
# 			SchoolID=int(campus_id)
# 		).all()

# 		if len(existent_links) > 0:
# 			new_record_subject = Subjects.query.filter_by(
# 				SchoolID=int(campus_id),
# 				SubjectID=int(subject_id)
# 			).first()

# 			new_record_subject_grade_level = new_record_subject.GradeLevel

# 			for link in existent_links:
# 				if link.SubjectID is not int(subject_id):
# 					link_subject = Subjects.query.filter_by(SubjectID=link.SubjectID).first()

# 					if link_subject.GradeLevel == new_record_subject_grade_level:
# 						link.SubjectID = subject_id

# 						try:
# 							db.session.commit()
# 						except Exception as e:
# 							return 400

# 					else:
# 						# new record for different grade level
# 						link = OutcomeLinks(
# 							OutcomeID=outcome_id,
# 							CourseID=course_id,
# 							SubjectID=subject_id,
# 							SchoolID=campus_id
# 						)

# 						db.session.add(link)

# 						try:
# 							db.session.commit()
# 						except Exception as e:
# 							return 400

# 			return {'OutcomeLinkID': link.OutcomeLinkID}

# 		else:
# 			link = OutcomeLinks(
# 				OutcomeID=outcome_id,
# 				CourseID=course_id,
# 				SubjectID=subject_id,
# 				SchoolID=campus_id
# 			)

# 			db.session.add(link)

# 			try:
# 				db.session.commit()
# 			except Exception as e:
# 				return 400

# 			return {'OutcomeLinkID': link.OutcomeLinkID}
# 	else:
# 		return 400

# async def update_final_proficiency(
#     user,
#     campus_id: str,
#     student_id: str,
#     outcome_link_id: str,
#     proficiency_value_id: str,
#     grader_id: str
# ):

#     # control access to student's teachers and admins
#     if permission(user, True, student=student_id):
#         outcomeLink = OutcomeLinks.query.filter_by(OutcomeLinkID=int(outcome_link_id)).first()

#         # check if record already exists
#         existent_proficiency = Proficiencies.query.filter_by(
#             UserID=int(student_id),
#             OutcomeLinkID=int(outcome_link_id),
#             SchoolID=int(campus_id)
#         ).first()

#         # update record
#         if existent_proficiency:
#             existent_proficiency.GraderID = int(grader_id)
#             existent_proficiency.ProficiencyValueID = int(proficiency_value_id)
#             try:
#                 db.session.commit()
#                 await set_letter_grade(outcomeLink.SubjectID, student_id, campus_id, grader_id)
#             except Exception as e:
#                 return 400

#             return {
# 				'proficiencyID': existent_proficiency.ProficiencyID,
# 				'graderID': existent_proficiency.GraderID,
# 				'outcomeLinkID': existent_proficiency.OutcomeLinkID,
#                 'outcomeID': outcomeLink.OutcomeID,
# 				'proficiencyValueID': existent_proficiency.ProficiencyValueID,
# 				'schoolID': existent_proficiency.SchoolID,
# 				'userID': existent_proficiency.UserID,
#                 'subjectID': outcomeLink.SubjectID
# 			}

#         # add record
#         else:
#             proficiency = Proficiencies(
#                 UserID=int(student_id),
#                 OutcomeLinkID=int(outcome_link_id),
#                 ProficiencyValueID=int(proficiency_value_id),
#                 GraderID=int(grader_id),
#                 SchoolID=int(campus_id)
#             )
#             db.session.add(proficiency)
#             try:
#                 db.session.commit()
#                 await set_letter_grade(outcomeLink.SubjectID, student_id, campus_id, grader_id)
#             except Exception as e:
#                 return 400

#             return {
# 				'proficiencyID': proficiency.ProficiencyID,
# 				'graderID': proficiency.GraderID,
# 				'outcomeLinkID': proficiency.OutcomeLinkID,
#                 'outcomeID': outcomeLink.OutcomeID,
# 				'proficiencyValueID': proficiency.ProficiencyValueID,
# 				'schoolID': proficiency.SchoolID,
# 				'userID': proficiency.UserID,
#                 'subjectID': outcomeLink.SubjectID
# 			}
#     else:
#         return 400

# async def set_letter_grade(subject_id: int, user_id: int, school_id: int, grader_id: int):
# 	try:
# 		query = '{CALL Grading.SetLetterGrade (?, ?, ?, ?)}'

# 		connection = db.engine.raw_connection()
# 		cursor = connection.cursor()
# 		cursor.execute(query, (subject_id, int(user_id), int(school_id), grader_id))
# 		connection.commit()
# 	finally:
# 		connection.close()

# async def get_outcome_link(course_id: int, outcomes_ids, gradelevels_ids):
#     for i in range(len(gradelevels_ids)):
#         gradelevels_ids[i] = str(gradelevels_ids[i])
#     str_gradelevels_ids = ', '.join(gradelevels_ids)

#     for i in range(len(outcomes_ids)):
#         outcomes_ids[i] = str(outcomes_ids[i])
#     str_outcomes_ids = ', '.join(outcomes_ids)

#     results = db.session.execute('''
#         SELECT          ol.OutcomeLinkID,
#                         ol.OutcomeID,
#                         ol.CourseID,
#                         s.SubjectID,
#                         s.SubjectName,
#                         s.GradeLevel
#         FROM            Grading.OutcomeLinks ol
#                         JOIN Grading.Subjects s ON s.SubjectID = ol.SubjectID
#                             AND ol.SchoolID = s.SchoolID
#         WHERE           ol.OutcomeID IN (SELECT convert(int, value) FROM string_split(:outcomesIDs, ','))
#                         AND s.GradeLevel IN (SELECT convert(int, value) FROM string_split(:gradeLevelsIDs, ','))
#                         AND ol.CourseID = :courseID''', { 'outcomesIDs': str_outcomes_ids, 'gradeLevelsIDs': str_gradelevels_ids, 'courseID': course_id })

#     rows = results.fetchall()

#     if rows == None:
#         return None

#     outcomeLinks = {}
#     for r in rows:
#         outcomeLinks[r.OutcomeID] = {
#             'outcomeLinkID': r.OutcomeLinkID,
#             'outcomeID': r.OutcomeID,
#             'courseID': r.CourseID,
#             'subjectID': r.SubjectID,
#             'subjectName': r.SubjectName,
#             'gradeLevel': r.GradeLevel
#         }

#     return outcomeLinks

# async def get_proficiency_for_student_outcome(course_id: int, student_ids, outcomes_ids):
#     for i in range(len(student_ids)):
#         student_ids[i] = str(student_ids[i])
#     str_students_ids = ', '.join(student_ids)

#     for i in range(len(outcomes_ids)):
#         outcomes_ids[i] = str(outcomes_ids[i])
#     str_outcomes_ids = ', '.join(outcomes_ids)

#     results = db.session.execute('''
#     SELECT          p.ProficiencyID,
#                 pv.ProficiencyValueID,
#                 pv.ProficiencyDesc,
#                 pv.ProficiencyValue,
#                 ol.OutcomeLinkID,
#                 ol.OutcomeID,
#                 s.SubjectID,
#                 s.SubjectName,
#                 s.GradeLevel,
#                 p.UserID,
#                 p.SchoolID,
#                 ol.CourseID,
#                 p.GraderID
#     FROM            Grading.Proficiencies p
#                 JOIN Grading.ProficiencyValues pv ON pv.ProficiencyValueID = p.ProficiencyValueID
#                 JOIN Grading.OutcomeLinks ol ON ol.OutcomeLinkID = p.OutcomeLinkID
#                     AND ol.SchoolID = p.SchoolID
#                 JOIN Grading.Subjects s ON s.SubjectID = ol.SubjectID
#                     AND s.SchoolID = ol.SchoolID
#     WHERE           ol.CourseID = :courseID
#                 AND ol.OutcomeID IN (SELECT convert(int, value) FROM string_split(:outcomesIDs, ','))
#                 AND p.UserID IN (SELECT convert(int, value) FROM string_split(:studentsIDs, ','))''', {'courseID': course_id, 'outcomesIDs': str_outcomes_ids, 'studentsIDs': str_students_ids})

#     rows = results.fetchall()

#     if rows == None:
#         return None

#     proficiencies = {}
#     for r in rows:
#         proficiencies[str(r.UserID)+'_'+str(r.OutcomeID)] = {
#             'proficiencyID': r.ProficiencyID,
#             'proficiencyValueID': r.ProficiencyValueID,
#             'proficiencyDesc': r.ProficiencyDesc,
#             'proficiencyValue': r.ProficiencyValue,
#             'outcomeLinkID': r.OutcomeLinkID,
#             'outcomeID': r.OutcomeID,
#             'subjectID': r.SubjectID,
#             'subjectName': r.SubjectName,
#             'gradeLevel': r.GradeLevel,
#             'userID': r.UserID,
#             'schoolID': r.SchoolID,
#             'courseID': r.CourseID,
#             'graderID': r.GraderID
#         }

#     return proficiencies

# # TODO: deprecate?
# async def course_proficiencies(user, campus_id: str, course_id: str):

#     if permission(user, True, course_id):  # control access to course's teachers and admins
#         fields = ['OutcomeLinkID']
#         outcomes_links_results = OutcomeLinks.query.filter_by(
#             CourseID=int(course_id),
#             SchoolID=int(campus_id)
#         ).options(load_only(*fields)).all()

#         outcomes_links = []
#         for l in outcomes_links_results:
#             outcomes_links.append(l.OutcomeLinkID)

#         results = Proficiencies.query.filter(
#             Proficiencies.OutcomeLinkID.in_(outcomes_links)
#         ).all()

#         proficiencies = []
#         for r in results:
#             proficiencies.append({
#                 'proficiencyID': r.ProficiencyID,
#                 'userID': r.UserID,
#                 'outcomeLinkID': r.OutcomeLinkID,
#                 'proficiencyValueID': r.ProficiencyValueID,
#                 'graderID': r.GraderID,
#                 'schoolID': r.SchoolID
#             })
#     else:
#         return False

#     return proficiencies

# async def subject_proficiencies(user, campus_id: str, subject_id: str):

#     if permission(user, False):  # control access to teachers and admins
#         fields = ['OutcomeLinkID']
#         outcomes_links_results = OutcomeLinks.query.filter_by(
#             SubjectID=int(subject_id),
#             SchoolID=int(campus_id)
#         ).options(load_only(*fields)).all()

#         outcomes_links = []
#         for l in outcomes_links_results:
#             outcomes_links.append(l.OutcomeLinkID)

#         if user['mode'] == 'admin':
#             results = Proficiencies.query.filter(
#                 Proficiencies.OutcomeLinkID.in_(outcomes_links)
#             ).all()
#         else:
#             students = []

#             for enrollment in user['teacher']:
#                 for s in enrollment['sections']['all']['students']:
#                     students.append(int(s['id']))

#             results = Proficiencies.query.filter(
#                 Proficiencies.OutcomeLinkID.in_(outcomes_links),
#                 Proficiencies.UserID.in_(students),
#             ).all()

#         proficiencies = []
#         for r in results:
#             proficiencies.append({
#                 'proficiencyID': r.ProficiencyID,
#                 'userID': r.UserID,
#                 'outcomeLinkID': r.OutcomeLinkID,
#                 'proficiencyValueID': r.ProficiencyValueID,
#                 'graderID': r.GraderID,
#                 'schoolID': r.SchoolID
#             })
#     else:
#         return False

#     return proficiencies

# async def students_lettergrades_results(base_url: str, access_token: str, user, campus_id: int, subject_id: str, students_ids):
#     if permission(user, False):  # control access to teachers and admins
#         if students_ids:
#             students_ids_arr = [int(s) for s in students_ids.split(',')]
#         else:
#             students_ids_arr=[]

#         # Subject Outcomes Links
#         results_links = OutcomeLinks.query.filter(
#             OutcomeLinks.SubjectID==int(subject_id),
#             OutcomeLinks.SchoolID==campus_id
#         ).all()

#         outcomesLinks = []
#         outcomesIDs = []
#         for r in results_links:
#             if r.OutcomeLinkID not in outcomesLinks:
#                 outcomesLinks.append(r.OutcomeLinkID)
#             if r.OutcomeID not in outcomesIDs:
#                 outcomesIDs.append(r.OutcomeID)

#         # Subject Outcomes Title/Description
#         outcomes_data_results = await canvas_api.outcomes_data(base_url, access_token, ','.join(str(o) for o in outcomesIDs))

#         # Letter Grade Results
#         letter_grades_values = []
#         letter_grades_values_results = LetterGradeValues.query.all()
#         for r in letter_grades_values_results:
#             letter_grades_values.append({
#                'letterGradeValueID': r.LetterGradeValueID,
#                'letterGradeDesc': r.LetterGradeDesc,
#                'letterGradeValue': r.LetterGradeValue
#             })

#         overall_results = []
#         if user['mode'] == 'admin':
#             results_letter_grades = LetterGrades.query.filter(
#                 LetterGrades.SubjectID==int(subject_id),
#                 LetterGrades.SchoolID==campus_id,
#             ).all()
#         else:
#             results_letter_grades = LetterGrades.query.filter(
#                 LetterGrades.SubjectID==int(subject_id),
#                 LetterGrades.SchoolID==campus_id,
#                 LetterGrades.UserID.in_(students_ids_arr)
#             ).all()

#         for r in results_letter_grades:
#             new_record = {
#                 'userID': r.UserID,
# 				'userName': '',
#                 'subjectID': r.SubjectID,
#                 'schoolID': r.SchoolID,
#                 'letterGradeID': r.LetterGradeID,
#                 'letterGradeValueID': r.LetterGradeValueID,
#                 'letterGradeDesc': None,
#                 'letterGradeValue': None,
#                 'overwritten': True if r.Overwritten != None else False,
#                 'graderID': r.GraderID,
#                 'proficiencies': {}
#             }
#             for value in letter_grades_values:
#                 if value['letterGradeValueID'] == new_record['letterGradeValueID']:
#                     new_record['letterGradeDesc'] = value['letterGradeDesc']
#                     new_record['letterGradeValue'] = value['letterGradeValue']
#             overall_results.append(new_record)

#         # Proficiencies Results
#         if user['mode'] == 'admin':
#             results_proficiencies = Proficiencies.query.filter(
#                 Proficiencies.OutcomeLinkID.in_(outcomesLinks),
#                 Proficiencies.SchoolID==campus_id,
#             ).all()
#         else:
#             results_proficiencies = Proficiencies.query.filter(
#                 Proficiencies.OutcomeLinkID.in_(outcomesLinks),
#                 Proficiencies.UserID.in_(students_ids_arr),
#                 Proficiencies.SchoolID==campus_id,
#             ).all()

#         proficiencies = []
#         for rp in results_proficiencies:
#             proficiency = {
#                 'proficiencyID': rp.ProficiencyID,
#                 'userID': rp.UserID,
#                 'outcomeLinkID': rp.OutcomeLinkID,
#                 'outcomeID': '',
#                 'outcomeTitle':'',
#                 'outcomeDesc':'',
#                 'proficiencyValueID': rp.ProficiencyValueID,
#                 'graderID': rp.GraderID,
#                 'schoolID': rp.SchoolID
#             }
#             for rl in results_links:
#                 if rl.OutcomeLinkID == rp.OutcomeLinkID:
#                     proficiency['outcomeID'] = rl.OutcomeID
#             for o_id in outcomes_data_results:
#                 if o_id == proficiency['outcomeID']:
#                     proficiency['outcomeTitle'] = outcomes_data_results[o_id]['title']
#                     proficiency['outcomeDesc'] = outcomes_data_results[o_id]['description']
#             proficiencies.append(proficiency)
#     else:
#         return False

#     # Overall Results
#     for r in overall_results:
#         for p in proficiencies:
#             if r['userID'] == p['userID']:
#                 r['proficiencies'][p['outcomeID']] = p

#     return overall_results

# async def subject_letter_grades(user, campus_id: str, subject_id: str):

#     if permission(user, False):  # control access to teachers and admins

#         if user['mode'] == 'admin':
#             results = LetterGrades.query.filter_by(
#                 SubjectID=int(subject_id),
#                 SchoolID=int(campus_id)
#             ).all()
#         else:
#             students = []

#             for enrollment in user['teacher']:
#                 for s in enrollment['sections']['all']['students']:
#                     students.append(int(s['id']))

#             results = LetterGrades.query.filter(
#                 LetterGrades.SubjectID == int(subject_id),
#                 LetterGrades.SchoolID == int(campus_id),
#                 LetterGrades.UserID.in_(students),
#             ).all()

#         letter_grades = []
#         for r in results:
#             letter_grades.append({
#                 'letterGradeID': r.LetterGradeID,
#                 'userID': r.UserID,
#                 'subjectID': r.SubjectID,
#                 'letterGradeValueID': r.LetterGradeValueID,
#                 'graderID': r.GraderID,
#                 'overwritten': r.Overwritten,
#                 'schoolID': r.SchoolID
#             })
#     else:
#         return False

#     return letter_grades

# async def update_letter_grade(
#     user,
#     campus_id: str,
#     student_id: str,
#     subject_id: str,
#     letter_grade_value_id: str,
#     grader_id: str,
#     overwritten: bool,
# ):

#     # control access to student's teachers and admins
#     if permission(user, True, student=student_id):
#         letter_grade_value = LetterGradeValues.query.filter(
# 			LetterGradeValues.LetterGradeValueID == int(letter_grade_value_id)
# 		).one();

#         # check if record already exists
#         existent_grade = LetterGrades.query.filter_by(
#             UserID=int(student_id),
#             SubjectID=int(subject_id),
#             SchoolID=int(campus_id)
#         ).first()

#         # update record
#         if existent_grade:
#             existent_grade.GraderID = int(grader_id)
#             existent_grade.LetterGradeValueID = int(letter_grade_value_id)
#             if overwritten:
#                 existent_grade.Overwritten = datetime.now()
#             else:
#                 existent_grade.Overwritten = None
#             try:
#                 db.session.commit()
#             except Exception as e:
#                 return 400
#             return {
# 				'letterGradeID': existent_grade.LetterGradeID,
# 				'letterGradeValueID': int(letter_grade_value_id),
# 				'letterGradeValue': letter_grade_value.LetterGradeValue,
# 				'letterGradeDesc': letter_grade_value.LetterGradeDesc,
# 				'overwritten': True if existent_grade.Overwritten != None else False,
# 				'subjectID': existent_grade.SubjectID
# 			}

#         # add record
#         else:
#             letter_grade = LetterGrades(
#                 UserID=int(student_id),
#                 SubjectID=int(subject_id),
#                 LetterGradeValueID=int(letter_grade_value_id),
#                 GraderID=int(grader_id),
#                 SchoolID=int(campus_id)
#             )
#             if overwritten:
#                 letter_grade.Overwritten = datetime.now()
#             db.session.add(letter_grade)
#             try:
#                 db.session.commit()
#             except Exception as e:
#                 return 400

#             return {'LetterGradeID': letter_grade.LetterGradeID}
#     else:
#         return 400

# async def letter_grades_values():

#     results = LetterGradeValues.query.all()

#     letter_grades_values = []
#     for r in results:
#         letter_grades_values.append({
#             'letterGradeValueID': r.LetterGradeValueID,
#             'letterGradeDesc': r.LetterGradeDesc,
#             'letterGradeValue': r.LetterGradeValue,
#         })

#     return letter_grades_values

# async def proficiencies_values():

#     results = ProficiencyValues.query.all()

#     proficiencies_values = []
#     for r in results:
#         proficiencies_values.append({
#             'proficiencyValueID': r.ProficiencyValueID,
#             'proficiencyDesc': r.ProficiencyDesc,
#             'proficiencyValue': r.ProficiencyValue,
#         })

#     return proficiencies_values

# def permission(user, enrollment_check, course=None, student=None):
# 	permission = False
# 	if user['admin']:
# 		permission = True
# 	elif 'teacher' in user:
# 		permission = True
# 		# if not enrollment_check:
# 		# 	permission = True
# 		# else:
# 		# 	if student:
# 		# 		for enrollment in user['teacher']:
# 		# 			for s in enrollment['sections']['all']['students']:
# 		# 				if int(s['id']) == int(student):
# 		# 					permission = True
# 		# 				else:
# 		# 					for enrollment in user['teacher']:
# 		# 						if int(enrollment['course_id']) == course:
# 		# 							permission = True

# 	return permission