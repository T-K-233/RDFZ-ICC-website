from flask import session, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from . import app, babel, lazy_translations
from .TK import HWARecognizer
from config import LANGUAGES
import base64
from matplotlib import pyplot as plt
import os

PAGE_TREE = {
    'about': {
        'about ICC': [],
        'mission': [],
        'faculty': [],
        'matriculation': [],
        'admission': []
    },
    'academics': {
        'chinese curricula': [],
        'Cambridge A Level Program': [],
        'The Advanced Placement Program': [],
        'International Baccalaureate': [],
    },
    'student': {
        'campus life': [],
        'extra-curricular activity': [],
    },
    'resources': {
        'contacts': [],
        'school calendar': [],
        'campus map': [],
        'location': [],
        'for media': [],
    },
}

lazy_translations.init_all()
HWA_recognizer = HWARecognizer()

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
    return render_template('home.html', PAGE_TREE=PAGE_TREE)


@app.route('/<branch>/<page>.html')
def general_register(branch, page):
    if branch in PAGE_TREE:
        if page in PAGE_TREE[branch]:
            if page == 'matriculation':
                import csv
                data_list = []
                for i in range(2010, 2019):
                    with open('./matriculation/%s.csv' % i, newline='', encoding='utf-8') as csvfile:
                        data_list.append(list(csv.reader(csvfile, delimiter=',')))
                return render_template('%s.html' % branch, INDEX=[branch, page], DATA=data_list)
            return render_template('%s.html' % branch, INDEX=[branch, page])


@app.route('/student/extra-curricular-activity/<page>.html')
def extra_curricular_activity(page):
    return render_template('activities/%s.html' % page, INDEX=['extra-curricular activity', page])


@app.route('/author.html')
def author():
    return render_template('author.html', INDEX=[None, 'website authors'])


@app.route('/stem/ai_experiments', methods=['GET', 'POST'])
def ai_experiments():
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

