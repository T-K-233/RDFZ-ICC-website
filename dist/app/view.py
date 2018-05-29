from flask import session, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_babel import gettext as _
from . import app, babel
from config import LANGUAGES
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


@babel.localeselector
def get_locale():
    print(session['lang'])
    try:
        print('set lang: '+session['lang'])
        return session['lang']
    except:
        print('default lang:', request.accept_languages.best_match(LANGUAGES.keys()))
        return request.accept_languages.best_match(LANGUAGES.keys())


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


@app.route('/pictures')
def pictures():
    return render_template('pictures.html', PICS=list(os.walk('./app/static/pics'))[0][-1])


@app.route('/pictures', methods=['POST'])
def picture_upload():
    f = request.files['file']
    path = './app/static/pics/'+secure_filename(f.filename)
    f.save(path)
    return redirect(url_for('pictures'))

