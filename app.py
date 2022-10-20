from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_required, logout_user
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from flask import Flask , render_template

# import for blueprint

from Controller.onMe import onMe
from Controller.delete import Delete
from Controller.dolci import Dolci
from Controller.login import Login
from Controller.dashboard.posts import Posts
from Controller.dashboard.users import Users
from Controller.dashboard.create import Create
from Controller.dashboard.admin import Admin
from Controller.dashboard.update import Update
from Controller.dashboard.register import Register

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prova.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'

# blueprint

app.register_blueprint(onMe)
app.register_blueprint(Delete)
app.register_blueprint(Dolci)
app.register_blueprint(Login)
app.register_blueprint(Posts)
app.register_blueprint(Users)
app.register_blueprint(Create)
app.register_blueprint(Admin)
app.register_blueprint(Update)
# app.register_blueprint(Register)


CORS(app)


@app.route('/')
def index():

    return render_template('index.html')

# LOGIN 

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


# logout

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('/')

# back

@app.route('/back')
@login_required
def back():
    
    return redirect('/dashboard')

@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')

    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug = False)
