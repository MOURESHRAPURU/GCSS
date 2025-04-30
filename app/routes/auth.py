# from flask import Blueprint, render_template, redirect, url_for, flash, request
# from flask_login import login_user, logout_user, login_required, current_user
# from app.models import User, db

# bp = Blueprint('auth', __name__)

# @bp.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user = User.query.filter_by(username=username).first()
        
#         if user and user.check_password(password):
#             login_user(user)
#             if user.role == 'admin':
#                 return redirect(url_for('admin.dashboard'))
#             else:
#                 return redirect(url_for('counselor.dashboard'))
#         flash('Invalid username or password')
#     return render_template('auth/login.html')

# @bp.route('/register', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
    
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']
#         role = request.form['role']
        
#         if User.query.filter_by(username=username).first():
#             flash('Username already exists')
#             return render_template('auth/register.html')
        
#         if User.query.filter_by(email=email).first():
#             flash('Email already registered')
#             return render_template('auth/register.html')
        
#         user = User(username=username, email=email, role=role)
#         user.set_password(password)
#         db.session.add(user)
#         db.session.commit()
        
#         flash('Registration successful! Please login.')
#         return redirect(url_for('auth.login'))
    
#     return render_template('auth/register.html')

# @bp.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('auth.login'))

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Patient, Counsellor, RiskAssessment, Report, GeneticData, FamilyHistory
from flask import jsonify
from app import db

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            print(f"Logged in user: {user.username}, role: {user.role}, access_level: {user.access_level}")
            return redirect(url_for('admin.dashboard') if user.role == 'admin' else url_for('counselor.dashboard'))
        
        flash('Invalid username or password')
    return render_template('auth/login.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        
        # Set access_level based on role, or default to a minimum level if none provided
        access_level = 1 if role == 'admin' else 2  # Adjust levels as needed for your project
        
        # Validate unique username and email
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('auth.register'))
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('auth.register'))
        
        user = User(username=username, email=email, role=role, access_level=access_level)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    print(f"Current user: {current_user.username}, is_authenticated: {current_user.is_authenticated}")
    
    if current_user.access_level == 1:
        # Fetch patients from the database
        patients = Patient.query.all()
        counsellors = Counsellor.query.all()
        risk_assessments = RiskAssessment.query.all()
        reports = Report.query.all()
        return render_template(
            'admin/dashboard.html',
            patients=patients,
            counsellors=counsellors,
            risk_assessments=risk_assessments,
            reports=reports
        )
    else:
        flash('You do not have permission to access the dashboard.')
        return redirect(url_for('index'))


@bp.route('/api/patients', methods=['POST'])
@login_required
def create_patient():
    try:
        data = request.get_json()
        
        # Create patient
        patient = Patient(
            name=data['name'],
            contact_details=data['contact_details'],
            medical_history=data['medical_history']
        )
        db.session.add(patient)
        db.session.flush()  # Get patient ID before committing
        
        # Create genetic data
        genetic_data = GeneticData(
            patient_id=patient.id,
            gene_sequence=data['genetic_data']['gene_sequence'],
            mutations=data['genetic_data']['mutations'],
            test_results=data['genetic_data']['test_results']
        )
        db.session.add(genetic_data)
        
        # Create family history
        family_history = FamilyHistory(
            patient_id=patient.id,
            relationships=data['family_history']['relationships'],
            genetic_conditions=data['family_history']['genetic_conditions']
        )
        db.session.add(family_history)
        
        db.session.commit()
        return jsonify({'message': 'Patient created successfully', 'id': patient.id}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    
@bp.route('/api/patients/<int:patient_id>', methods=['PUT'])
@login_required
def update_patient(patient_id):
    try:
        data = request.get_json()
        patient = Patient.query.get_or_404(patient_id)
        
        # Update patient
        patient.name = data['name']
        patient.contact_details = data['contact_details']
        patient.medical_history = data['medical_history']
        
        # Update genetic data
        if patient.genetic_data:
            genetic_data = patient.genetic_data[0]
        else:
            genetic_data = GeneticData(patient_id=patient_id)
            db.session.add(genetic_data)
        
        genetic_data.gene_sequence = data['genetic_data']['gene_sequence']
        genetic_data.mutations = data['genetic_data']['mutations']
        genetic_data.test_results = data['genetic_data']['test_results']
        
        # Update family history
        if patient.family_history:
            family_history = patient.family_history[0]
        else:
            family_history = FamilyHistory(patient_id=patient_id)
            db.session.add(family_history)
        
        family_history.relationships = data['family_history']['relationships']
        family_history.genetic_conditions = data['family_history']['genetic_conditions']
        
        db.session.commit()
        return jsonify({'message': 'Patient updated successfully'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@bp.route('/api/patients/<int:patient_id>', methods=['DELETE'])
@login_required
def delete_patient(patient_id):
    try:
        patient = Patient.query.get_or_404(patient_id)
        db.session.delete(patient)
        db.session.commit()
        return jsonify({'message': 'Patient deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/api/generate_report/<int:patient_id>')
@login_required
def generate_report(patient_id):
    # Generate report logic here; for example, create a PDF or summary
    report_url = f"/reports/{patient_id}_report.pdf"  # Path to the generated report

    # Example response (actual report generation logic would go here)
    return jsonify({"report_url": report_url})

@bp.route('/check_auth')
@login_required
def check_auth():
    return f"Authenticated: {current_user.is_authenticated}, Username: {current_user.username}, Role: {current_user.role}, Access Level: {current_user.access_level}"


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


