import os

from flask import (json, redirect, render_template, request,
                   url_for)
from werkzeug.utils import secure_filename

from app import app

# Allowed file types
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

start = "/images"

# To check for the type of image file uploaded


def allowed_file(filename):
    return'.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# To check for id
def count_id():
    with open("data.json") as json_file:
        data = json.load(json_file)
        temp = data["posts"]
        counter = -1
        for id in temp:
            counter += 1
        return counter


# FUNCTION: To write the new dictionary to the json file
def write_json(data, filename="data.json"):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent=2)


# FUNCTIONS: To read the json files
def read_admin_json():
    json_admin_file = open('admin.json', 'r')
    json_admin = json_admin_file.read()
    admin = json.loads(json_admin)
    return admin


def read_data_json():
    with open("data.json") as json_file:
        data = json.load(json_file)
    return data


# Homepage route
@app.route('/')
@app.route('/homepage')
def homepage():
    # Read data json file
    data = read_data_json()

    return render_template('homepage.html', title='Home', data=data)


# Homepage route; parses post requests from create
@app.route('/', methods=['POST'])
def uploads():
    file = request.files['image']

    if request.method == 'POST':
        # Save image files to static/images
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image = str('images/'+filename)

        # Appends the new data to the data json file
        data = read_data_json()
        id_count = (count_id() + 1)
        y = {"date": request.form.get('date'),
             "title": request.form.get('header'),
             "body": request.form.get('post'),
             "id": id_count,
             "image": image
             }
        data["posts"].append(y)
        write_json(data)

    return redirect(url_for('homepage'))


# Create page route
@ app.route('/create', methods=['GET', 'POST'])
def create():
    return render_template('post.html', title='create')


# About page route
@ app.route('/about')
def about():
    # Read admin json file
    admin = read_admin_json()
    return render_template('about.html', title='about me', admin=admin)


# Summary page route
@ app.route('/summary')
def summary():
    data = read_data_json()
    return render_template('summary.html', title='summary', data=data)


# Details route; receives query param from summary page
@ app.route('/details')
def details():
    data = read_data_json()

    # convert the query param to int
    id = int(request.args.get('postid'))
    temp = data["posts"]
    post_header = temp[id]['title']
    post_body = temp[id]['body']
    post_date = temp[id]['date']
    post_picture = temp[id]['image']

    return render_template('details.html', title='details', post_header=post_header, post_body=post_body, post_date=post_date, data=data, id=id, post_picture=post_picture)


# Edit route; receives query param from summary page
@ app.route('/edit_post')
def edit_post():
    data = read_data_json()
    id = int(request.args.get('postid'))
    temp = data["posts"]
    post_header = temp[id]['title']
    post_body = temp[id]['body']

    return render_template('edit.html', title='edit', id=id, post_body=post_body, post_header=post_header)


# Edit function; receives query params from details page,
@ app.route('/edit', methods=['GET', 'POST'])
def edit():
    data = read_data_json()
    id = int(request.args.get('postid'))

    file = request.files['image']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        img = (os.path.join(app.config['UPLOAD_FOLDER'], filename))
        if img != '/app/static/images/'+filename:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # convert image name to string
        image = str('images/'+filename)

    # Compares the new data and writes to the json file
    if data["posts"][id]['title'] != request.form.get('edit_header'):
        data["posts"][id]['title'] = request.form.get('edit_header')

    if data["posts"][id]['body'] != request.form.get('edit_post'):
        data["posts"][id]['body'] = request.form.get('edit_post')

    if file:
        data["posts"][id]['image'] = image
    write_json(data)

    return redirect(url_for('summary'))


# Delete funtion; receives query param from details page
@ app.route('/delete')
def delete():
    data = read_data_json()
    id = int(request.args.get('postid'))

    # delete and write to json file
    del data["posts"][id]
    counter = 0
    for post_id in data["posts"]:
        post_id['id'] = counter
        counter += 1
    write_json(data)
    return redirect(url_for('summary'))
