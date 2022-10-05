from flask import Flask, render_template, url_for, redirect , request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import sqlite3
from werkzeug.utils import secure_filename



app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/img/"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prova.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'



# @app.route('/')
def index():

    return render_template('index.html')

@app.route('/on-me')
def home():

    return render_template('on-me.html')

@app.route('/<int:idx>/delete', methods=('POST',))
@login_required
def delete(idx):
    connection = sqlite3.connect('prova.db')
    connection.row_factory = sqlite3.Row
    connection.execute('DELETE FROM user WHERE id = ?', (idx,))
    connection.execute('DELETE FROM posts WHERE id = ?', (idx,))
    connection.commit()
    connection.close()
    return redirect('/dashboard')

@app.route('/<int:idx>/update', methods=('POST', 'GET'))
@login_required
def update(idx):
    
    return render_template('/dashboard' , update = update)

@app.route('/dolci')
def dolci():
    connection = sqlite3.connect('prova.db')
    connection.row_factory = sqlite3.Row
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('dolci.html', posts=posts)

# login 

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

# dashboard admin

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    
    connection = sqlite3.connect('prova.db')
    connection.row_factory = sqlite3.Row
    user = connection.execute('SELECT * FROM user').fetchall()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.commit()
    
    
    if request.method == 'POST':
        titolo = request.form['titolo']
        info = request.form['info']
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(app.config['UPLOAD_FOLDER'] + filename)
        connection.execute('INSERT INTO posts (titolo, info, filename) VALUES (?, ?, ?)', (titolo, info, filename))
        connection.commit()
        connection.close()
        return redirect('/dashboard')
    return render_template('dashboard.html', posts = posts , user = user)



@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug = False)
