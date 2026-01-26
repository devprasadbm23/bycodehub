from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class SubmissionForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    phone = StringField('Phone', validators=[DataRequired(), Length(max=20)])
    project_type = SelectField('Project Type', choices=[
        ('web_development', 'Web Development'),
        ('app_development', 'App Development'),
        ('ui_ux_design', 'UI/UX Design'),
        ('digital_marketing', 'Digital Marketing'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    budget = StringField('Budget')
    deadline = StringField('Deadline')
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit Requirement')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
