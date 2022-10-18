from flask import Blueprint
from flask import Flask , render_template

onMe = Blueprint('onMe', __name__)

app = Flask(__name__)



@onMe.route('/on-me')
def home():

    return render_template('on-me.html')