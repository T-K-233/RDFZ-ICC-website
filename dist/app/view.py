from flask import session, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from . import app, babel
# from .plugins import HWARecognizer
from config import LANGUAGES
import base64
from matplotlib import pyplot as plt
import os

square_path = "img/square/"


'''

    'academics': {
        'chinese curricula': {'img': 'img/square/6.jpg'},
        'Cambridge A Level Program': {'img': 'img/square/7.jpg'},
        'The Advanced Placement Program': {'img': 'img/square/8.jpg'},
        'International Baccalaureate': {'img': 'img/square/9.jpg'},
    },
    'student': {
        'campus life': {'img': 'img/square/10.jpg'},
        'extra-curricular activity': {'img': 'img/square/11.jpg'},
    },
    'resources': {
        'contacts': {'img': 'img/square/12.jpg'},
        'school calendar': {'img': 'img/square/13.jpg'},
        'campus map': {'img': 'img/square/5.jpg'},
        'location': {'img': 'img/square/8.jpg'},
        'for media': {'img': 'img/square/2.jpg'},
    },
    '''

# load plugins
# HWA_recognizer = HWARecognizer()


@babel.localeselector
def get_locale():
    return session['lang'] if 'lang' in session else request.accept_languages.best_match(LANGUAGES.keys())


@app.route('/api/change_lang')
def language():
    if request.args.get('lang') in LANGUAGES:
        session['lang'] = request.args.get('lang')
    if request.args.get('redirect'):
        return redirect(request.args.get('redirect'))
    return redirect(url_for('home'))


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/<page>.html')
def general_register(page):
    if page == 'matriculation':
        import csv
        data_list = []
        for i in range(2010, 2019):
            with open('./matriculation/%s.csv' % i, newline='', encoding='utf-8') as csvfile:
                data_list.append(list(csv.reader(csvfile, delimiter=',')))
        return render_template('first_level/%s.html' % page, INDEX=page, DATA=data_list)
    return render_template('first_level/%s.html' % page, INDEX=page)


@app.route('/<branch>/<page>.html')
def secondary_register(branch, page):
    return render_template('second_level/%s.html' % page, PAGE=page, BRANCH=branch)


@app.route('/author.html')
def author():
    return render_template('author.html')


@app.route('/stem/nai', methods=['GET', 'POST'])
def plugins_ai():
    if request.method == 'POST':
        img = base64.b64decode(request.form.get('img')[22:])
        with open('temp.jpg', 'wb') as f:
            f.write(img)
        img = plt.imread('temp.jpg')
        res_arr = HWA_recognizer.recognize(img)
        return jsonify({'pred': res_arr})
    return render_template('draw.html')


@app.route('/pictures')
def pictures():
    return render_template('pictures.html', PICS=list(os.walk('./app/static/pics'))[0][-1])


@app.route('/pictures', methods=['POST'])
def picture_upload():
    f = request.files['file']
    path = './app/static/pics/'+secure_filename(f.filename)
    f.save(path)
    return redirect(url_for('pictures'))

