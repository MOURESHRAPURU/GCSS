# from flask import Blueprint, render_template
# from app.utils.decorators import admin_required
# from app.models import Patient, FamilyHistory, GeneticData

# bp = Blueprint('admin', __name__)

# @bp.route('/admin/dashboard')
# @admin_required
# def dashboard():
#     patients = Patient.query.all()
#     return render_template('admin/dashboard.html', patients=patients)

# @bp.route('/admin/patient/<int:id>')
# @admin_required
# def patient_detail(id):
#     patient = Patient.query.get_or_404(id)
#     family_history = FamilyHistory.query.filter_by(patient_id=id).first()
#     genetic_data = GeneticData.query.filter_by(patient_id=id).first()
#     return render_template('admin/patient_detail.html', 
#                          patient=patient, 
#                          family_history=family_history, 
#                          genetic_data=genetic_data)

from flask import Blueprint, render_template, redirect, url_for, flash
from app.utils.decorators import admin_required
from app.models import Patient, FamilyHistory, GeneticData

bp = Blueprint('admin', __name__)

@bp.route('/admin/dashboard')
@admin_required
def dashboard():
    try:
        patients = Patient.query.all()
    except Exception as e:
        flash('Error loading patient data')
        patients = []
    return render_template('admin/dashboard.html', patients=patients)

@bp.route('/admin/patient/<int:id>')
@admin_required
def patient_detail(id):
    try:
        patient = Patient.query.get_or_404(id)
        family_history = FamilyHistory.query.filter_by(patient_id=id).first()
        genetic_data = GeneticData.query.filter_by(patient_id=id).first()
    except Exception as e:
        flash('Error loading patient details')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/patient_detail.html', patient=patient, family_history=family_history, genetic_data=genetic_data)
