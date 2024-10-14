from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# MySQL Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Dospordos1903@localhost/wave'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ey'

db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(100), nullable=False)
    m_name = db.Column(db.String(100), nullable=True)
    l_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"User('{self.f_name}', '{self.email}')"

# Route to render the create account form (READ)
@app.route('/Registration.html', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        first_name = request.form['inputFirstName']
        middle_name = request.form['inputMiddlename']
        last_name = request.form['inputLastName']
        email = request.form['inputEmail']
        password = request.form['inputPassword']

        # Hash the password before saving it to the database
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')  # Recommended hash method

        # Create a new user object
        new_user = User(f_name=first_name, m_name=middle_name, l_name=last_name, email=email, password=hashed_password)

        try:
            # Add the new user to the database
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully!', 'success')
            return redirect(url_for('login'))  # Redirect to the login page after registration
        except Exception as e:
            db.session.rollback()  # Rollback the session in case of error
            flash(f'An error occurred: {str(e)}', 'danger')  # Include error details for debugging
            return redirect(url_for('create_account'))

    return render_template('Registration.html')

# Route to render the login form
@app.route('/index', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['inputEmail']
        password = request.form['inputPassword']
        
        # Check if the user exists
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            # User is authenticated, store user info in session
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))  # Redirect to the dashboard after login
        else:
            flash('Login failed. Check your email and password.', 'danger')

    return render_template('index.html')

# Route to render a simple dashboard after login
@app.route('/wave')
def dashboard():
    return render_template('wave.html')  # Render the wave.html page

if __name__ == '__main__':
    app.run(debug=True)
