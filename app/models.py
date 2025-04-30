from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    role = db.Column(db.String(20), nullable=False)
    access_level = db.Column(db.Integer, nullable=False, default=1)  # Default access level
    is_admin = db.Column(db.Boolean, default=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def has_access(self, required_level):
        """Check if the user has the required access level."""
        return self.access_level <= required_level

    

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

db = SQLAlchemy()

class Counsellor(db.Model):
    __tablename__ = 'COUNSELLOR'

    COUNSELLOR_ID = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(100))
    ROLE = db.Column(db.String(50))
    ACCESSLEVEL = db.Column(db.String(20))
    
    # Relationship with Risk Assessment
    risk_assessments = db.relationship('RiskAssessment', backref='counsellor', lazy=True)

class Patient(db.Model):
    __tablename__ = 'PATIENT'

    PATIENT_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    NAME = db.Column(db.String(100))
    CONTACT_DETAILS = db.Column(db.String(200))
    MEDICAL_HISTORY = db.Column(db.Text)

    # Relationships
    family_history = db.relationship('FamilyHistory', backref='patient', lazy=True)
    genetic_data = db.relationship('GeneticData', backref='patient', lazy=True)
    risk_assessments = db.relationship('RiskAssessment', backref='patient', lazy=True)

class RiskAssessment(db.Model):
    __tablename__ = 'RISK_ASSESSMENT'

    ASSESSMENT_ID = db.Column(db.Integer, primary_key=True)
    RISKLEVEL = db.Column(db.String(20))
    ANALYSIS_RESULTS = db.Column(db.Text)
    COUNSELLER_ID = db.Column(db.Integer, db.ForeignKey('COUNSELLOR.COUNSELLOR_ID'))
    PATIENT_ID = db.Column(db.Integer, db.ForeignKey('PATIENT.PATIENT_ID'))
    assessment_date = db.Column(db.DateTime, default=datetime.utcnow)  # Added based on trigger

    # Relationship with Report
    reports = db.relationship('Report', backref='risk_assessment', lazy=True)

class Report(db.Model):
    __tablename__ = 'REPORT'

    REPORT_ID = db.Column(db.Integer, primary_key=True)
    GENERATION_DATE = db.Column(db.Date)
    RECOMMENDED_INTERVENTIONS = db.Column(db.Text)
    ASSESSMENT_ID = db.Column(db.Integer, db.ForeignKey('RISK_ASSESSMENT.ASSESSMENT_ID'))

class FamilyHistory(db.Model):
    __tablename__ = 'FAMILY_HISTORY'

    FAMILYHISTORY_ID = db.Column(db.Integer, primary_key=True)
    RELATIONSHIPS = db.Column(db.Text)
    GENETIC_CONDITIONS = db.Column(db.Text)
    PATIENT_ID = db.Column(db.Integer, db.ForeignKey('PATIENT.PATIENT_ID'))

class GeneticData(db.Model):
    __tablename__ = 'GENETIC_DATA'

    GENETICDATA_ID = db.Column(db.Integer, primary_key=True)
    GENE_SEQUENCE = db.Column(db.Text)
    MUTATIONS = db.Column(db.Text)
    TEST_RESULTS = db.Column(db.Text)
    PATIENT_ID = db.Column(db.Integer, db.ForeignKey('PATIENT.PATIENT_ID'))

class AuditLog(db.Model):
    __tablename__ = 'audit_log'

    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    table_name = db.Column(db.String(50))
    record_id = db.Column(db.Integer)
    action = db.Column(db.String(20))
    changed_by = db.Column(db.String(100))
    change_date = db.Column(db.DateTime)