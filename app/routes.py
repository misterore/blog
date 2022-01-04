import os

from flask import (json, redirect, render_template, request,
                   url_for)
from werkzeug.utils import secure_filename

from app import app

# Allowed file types
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# To check for the type of image file uploaded


def allowed_file(filename):
    return'.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# To check for id


def count_id():
    with open("data.json") as json_file:
        data = json. load(json_file)
        temp = data["posts"]
        counter = 0
        for id in temp:
            counter += 1
        return counter

# To write the new dictionary to the json file


def write_json(data, filename="data.json"):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent=4)


def open_admin_json():
    json_admin_file = open('admin.json', 'r')
    json_admin = json_admin_file.read()
    admin = json.loads(json_admin)
    return admin


def open_data_json():
    json_data_file = open('data.json', 'r')
    json_data = json_data_file. read()
    data = json.loads(json_data)
    return data


@app.route('/')
@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    # Read data json file
    data = open_data_json()
    return render_template('homepage.html', title='Home', data=data)


@app.route('/', methods=['POST'])
def uploads():
    file = request.files['image']

    if request.method == 'POST':
        with open("data.json") as json_file:
            data = json.load(json_file)

        temp = data["posts"]
        id_count = (count_id() + 1)

        y = {"date": request.form.get('date'),
             "title": request.form.get('header'),
             "body": request.form.get('post'),
             "id": id_count
             }
        temp.append(y)
        write_json(data)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('homepage', name=filename))

    return redirect(url_for('homepage'))


@app.route('/create', methods=['GET', 'POST'])
def create():
    return render_template('post.html', title='create')


@app.route('/about')
def about():
    # Read admin json file
    admin = open_admin_json()
    return render_template('about.html', title='about me', admin=admin)


@app.route('/summary')
def summary():
    data = open_data_json()
    return render_template('summary.html', title='summary', data=data)


@app.route('/details')
def details():
    data = open_data_json()
    return render_template('details.html', title='details', data=data)
