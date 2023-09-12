from flask import Flask, render_template, request, redirect, url_for, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

import os



app = Flask(__name__, template_folder='templates')
app.secret_key = os.urandom(24)
csrf = CSRFProtect(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/flaskapp_db'
db = SQLAlchemy(app)

Session = db.session
login_manager = LoginManager(app)
login_manager.login_view = 'admin_login'

# login_manager = LoginManager(app)
# login_manager.login_view = 'admin_login'

admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class UserAdmin(ModelView):
    can_create = True
    can_edit = True
    can_delete = True
    column_exclude_list = ['password']

admin.add_view(UserAdmin(User, db.session))

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route('/')
def login():
    return render_template('login.html', form=LoginForm())

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        hashed_password = generate_password_hash(password, method='sha256')

        session_db = Session()

        new_user = User(first_name=first_name, last_name=last_name, email=email, password=hashed_password)
        session_db.add(new_user)
        session_db.commit()
        session_db.close()

        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/home')
def home():
    if 'id' in session:
        return render_template('home.html')
    else:
        return redirect('/')

@app.route('/login_validation', methods=['POST'])
def login_validation():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        session_db = Session()
        user = session_db.query(User).filter_by(email=email).first()
        session_db.close()

        if user and check_password_hash(user.password, password):
            session['id'] = user.id
            return render_template('home.html')
        else:
            error_message = "Invalid login credentials. Please try again."
            return render_template('login.html', error_message=error_message, form=form)

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('id', None)
    return redirect('/')


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data  # Assuming admin login uses email as the username
        password = form.password.data
        # Replace with your admin username and password validation logic
        if email == 'form.email.data' and password == 'form.password.data':
            # Replace with your admin user retrieval logic if necessary
            user = User.query.filter_by(email=email).first()
            if user:
                login_user(user)
                return redirect(url_for('admin.index'))

    return render_template('admin_login.html', form=form)

@app.route('/admin')
@login_required
def admin_panel():
    return redirect('/admin/')



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
