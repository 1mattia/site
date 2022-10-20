from flask import Blueprint , render_template, render_template , request , redirect
from flask import Flask 
from flask_login import login_required
import sqlite3
from werkzeug.utils import secure_filename

Update = Blueprint('update', __name__)

app = Flask(__name__)

@Update.route('/update/<int:id>/', methods=['GET', 'POST'])
@login_required
def update(id):
    connection = sqlite3.connect('prova.db')
    connection.row_factory = sqlite3.Row
    posts = connection.execute('SELECT * FROM posts' ).fetchall()

    connection.commit()

    if request.method == 'POST':
        titolo = request.form['titolo']
        info = request.form['info']
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(app.config['UPLOAD_FOLDER'] + filename)
        connection.execute('UPDATE posts SET titolo=(?) , info=(?) , filename=(?) WHERE id=(id)',[titolo,info,filename])
        connection.commit()
        connection.close()
        return redirect('/dashboard')

    return render_template('update.html' , posts = posts)