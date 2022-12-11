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

async def get_proficiency_values():
    results = ProficiencyValues.query.all()

    proficiency_values = []
    for r in results:
        proficiency_values.append({
        'proficiencyValueID': r.ProficiencyValueID,
        'proficiencyDesc': r.ProficiencyDesc,
    })

    return proficiency_values