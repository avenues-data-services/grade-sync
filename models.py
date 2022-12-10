# Data Models
from app import db

db.Model.metadata.reflect(bind=db.engine,schema='Grading')

class Subjects(db.Model):
    __table__ = db.Model.metadata.tables['Grading.Subjects']

    def __repr__(self):
        return f'<Subject {self.SubjectName}>'

class OutcomeLinks(db.Model):
    __table__ = db.Model.metadata.tables['Grading.OutcomeLinks']

    def __repr__(self):
        return f'<OutcomeLink {self.OutcomeLinkID}>'

class Proficiencies(db.Model):
    __table__ = db.Model.metadata.tables['Grading.Proficiencies']

    def __repr__(self):
        return f'<Proficiency {self.ProficiencyID}>'

class LetterGrades(db.Model):
    __table__ = db.Model.metadata.tables['Grading.LetterGrades']

    def __repr__(self):
        return f'<Proficiency {self.LetterGradeID}>'

class LetterGradeValues(db.Model):
    __table__ = db.Model.metadata.tables['Grading.LetterGradeValues']

    def __repr__(self):
        return f'<Proficiency {self.LetterGradeValueID}>'

class ProficiencyValues(db.Model):
    __table__ = db.Model.metadata.tables['Grading.ProficiencyValues']

    def __repr__(self):
        return f'<Proficiency {self.ProficiencyValueID}>'