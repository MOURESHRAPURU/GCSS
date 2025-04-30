from flask import Blueprint, jsonify, request
from app.utils.risk_assessment import GeneticRiskAssessment
from app.models import Patient, GeneticData, FamilyHistory, Report
from app import db
from app.utils.decorators import access_level_required
from datetime import datetime

bp = Blueprint('risk_assessment', __name__)

@bp.route('/api/generate_report/<int:patient_id>', methods=['POST'])
@access_level_required(2)  # Requires appropriate access level
def generate_patient_report(patient_id):
    # Fetch patient data
    patient = Patient.query.get_or_404(patient_id)
    genetic_data = GeneticData.query.filter_by(patient_id=patient_id).first()
    family_history = FamilyHistory.query.filter_by(patient_id=patient_id).first()
    
    # Prepare data for risk assessment
    patient_data = {
        'name': patient.name,
        'id': patient.id,
        'medical_history': patient.medical_history
    }
    
    genetic_data_dict = {
        'gene_sequence': genetic_data.gene_sequence,
        'mutations': genetic_data.mutations,
        'test_results': genetic_data.test_results
    }
    
    family_history_dict = {
        'relationships': family_history.relationships,
        'genetic_conditions': family_history.genetic_conditions
    }
    
    # Generate risk assessment report
    risk_assessor = GeneticRiskAssessment()
    report = risk_assessor.generate_report(
        patient_data,
        genetic_data_dict,
        family_history_dict
    )
    
    # Save report to database (you'll need to create a Report model)
    new_report = Report(
        patient_id=patient_id,
        risk_level=report['risk_assessment']['risk_level'],
        recommendations=str(report['risk_assessment']['recommendations']),
        report_data=str(report),
        generation_date=datetime.now()
    )
    db.session.add(new_report)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'report': report,
        'report_id': new_report.id
    })