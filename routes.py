from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, current_app
from extensions import db, mail
from models import Portfolio, Testimonial, Submission, Admin
from flask_mail import Message
from forms import SubmissionForm, LoginForm
from functools import wraps

main = Blueprint('main', __name__)
admin = Blueprint('admin', __name__)

# ================= DECORATORS =================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('admin.admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# ================= MAIN ROUTES =================
@main.route('/')
def home():
    recent_projects = Portfolio.query.order_by(Portfolio.created_at.desc()).limit(6).all()
    testimonials = Testimonial.query.filter_by(is_approved=True).order_by(Testimonial.created_at.desc()).limit(3).all()
    form = SubmissionForm()
    return render_template('index.html', projects=recent_projects, testimonials=testimonials, form=form)

@main.route('/submit', methods=['POST'])
def submit():
    form = SubmissionForm()
    if form.validate_on_submit():
        try:
            submission = Submission(
                name=form.name.data,
                email=form.email.data,
                phone=form.phone.data,
                project_type=form.project_type.data,
                message=form.message.data,
                budget=form.budget.data,
                deadline=form.deadline.data
            )
            
            db.session.add(submission)
            db.session.commit()
            
            # Send confirmation email to client
            try:
                client_msg = Message(
                    subject="Project Requirement Received - ByCodeHub",
                    sender=current_app.config['MAIL_USERNAME'],
                    recipients=[submission.email]
                )
                client_msg.html = render_template('email_client_confirmation.html', submission=submission)
                mail.send(client_msg)
            except Exception as e:
                print(f"Error sending client email: {e}")
            
            # Send notification to admin
            try:
                admin_msg = Message(
                    subject=f"New Project Requirement - {submission.project_type}",
                    sender=current_app.config['MAIL_USERNAME'],
                    recipients=[current_app.config['MAIL_USERNAME']]
                )
                admin_msg.html = render_template('email_admin_notification.html', submission=submission)
                mail.send(admin_msg)
            except Exception as e:
                print(f"Error sending admin email: {e}")
            
            flash('Your requirement has been submitted successfully! We will contact you soon.', 'success')
            return redirect(url_for('main.home'))
        
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'error')
            print(f"Submission error: {e}")
            return redirect(url_for('main.home'))
    
    # If validation fails
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{getattr(form, field).label.text}: {error}", 'error')
    return redirect(url_for('main.home'))

@main.route('/portfolio')
def portfolio():
    category = request.args.get('category', 'all')
    if category == 'all':
        projects = Portfolio.query.order_by(Portfolio.created_at.desc()).all()
    else:
        projects = Portfolio.query.filter_by(category=category).order_by(Portfolio.created_at.desc()).all()
    return render_template('portfolio.html', projects=projects, current_category=category)

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/services')
def services():
    return render_template('services.html')

@main.route('/api/stats')
def api_stats():
    stats = {
        'total_projects': Portfolio.query.count(),
        'total_clients': Submission.query.count(),
        'completed_projects': Submission.query.filter_by(status='completed').count()
    }
    return jsonify(stats)

# ================= ADMIN ROUTES =================
@admin.route('/login', methods=['GET', 'POST'])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Admin.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            session['admin_logged_in'] = True
            session['admin_username'] = user.username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('admin.admin_dashboard'))
        else:
            flash('Invalid credentials', 'error')
    
    return render_template('admin_login.html', form=form)

@admin.route('/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('main.home'))

@admin.route('/dashboard')
@login_required
def admin_dashboard():
    total_submissions = Submission.query.count()
    pending = Submission.query.filter_by(status='pending').count()
    in_progress = Submission.query.filter_by(status='in_progress').count()
    completed = Submission.query.filter_by(status='completed').count()
    
    recent_submissions = Submission.query.order_by(Submission.created_at.desc()).limit(10).all()
    
    stats = {
        'total': total_submissions,
        'pending': pending,
        'in_progress': in_progress,
        'completed': completed
    }
    
    return render_template('admin_dashboard.html', stats=stats, submissions=recent_submissions)

@admin.route('/submissions')
@login_required
def admin_submissions():
    status_filter = request.args.get('status', 'all')
    
    if status_filter == 'all':
        submissions = Submission.query.order_by(Submission.created_at.desc()).all()
    else:
        submissions = Submission.query.filter_by(status=status_filter).order_by(Submission.created_at.desc()).all()
    
    return render_template('admin_submissions.html', submissions=submissions, current_status=status_filter)

@admin.route('/submission/<int:id>/update', methods=['POST'])
@login_required
def update_submission_status(id):
    submission = Submission.query.get_or_404(id)
    new_status = request.form.get('status')
    
    if new_status in ['pending', 'in_progress', 'completed']:
        submission.status = new_status
        db.session.commit()
        flash('Status updated successfully', 'success')
    
    return redirect(url_for('admin.admin_submissions'))

@admin.route('/submission/<int:id>/delete', methods=['POST'])
@login_required
def delete_submission(id):
    submission = Submission.query.get_or_404(id)
    db.session.delete(submission)
    db.session.commit()
    flash('Submission deleted successfully', 'success')
    return redirect(url_for('admin.admin_submissions'))
