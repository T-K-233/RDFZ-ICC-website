from flask import session, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from app import app, babel
from config import LANGUAGES
import os


@babel.localeselector
def get_locale():
    try:
        print('setted lang: '+session['lang'])
        return session['lang']
    except:
        print('default lang')
        return request.accept_languages.best_match(LANGUAGES.keys())


@app.route('/api/lang', methods=['POST'])
def language():
    if request.form.get('lang') in LANGUAGES:
        session['lang'] = request.form.get('lang')
        return 'success'
    else:
        return 'error'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about/<page>.html')
def about(page):
    return render_template('about.html', PAGE=page)


@app.route('/academics/<page>.html')
def academics(page):
    return render_template('academics.html', PAGE=page)


@app.route('/student/<page>.html')
def student(page):
    return render_template('student.html', PAGE=page)


@app.route('/student/activity/<page>.html')
def student_activity(page):
    return render_template('student_activity.html', PAGE=page)


@app.route('/resources/<page>.html')
def resources(page):
    return render_template('resources.html', PAGE=page)


@app.route('/author.html')
def author():
    return render_template('author.html')


@app.route('/pictures')
def pictures():
    return render_template('pictures.html', PICS=list(os.walk('./app/static/pics'))[0][-1])


@app.route('/pictures', methods=['POST'])
def picture_upload():
    f = request.files['file']
    path = './app/static/pics/'+secure_filename(f.filename)
    f.save(path)
    return redirect(url_for('pictures'))


@app.route('/app_test')
def test():
    return render_template('TEMP.html')


@app.route('/open_day')
def open_day():
    return render_template('open_day.html')


