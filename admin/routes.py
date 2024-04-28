import json
import os
from datetime import datetime

from flask import jsonify, request, g
from sqlalchemy import desc
from werkzeug.utils import secure_filename

from models import UploadedMedia
from server import db
from users.auth import auth
from users.models import User
from . import admin_
from .adminFunctions import delete_media


@admin_.route('/files', methods=['GET'])
@auth.login_required(role='admin')
def get_all_files():
    all_files = []
    files = UploadedMedia.query.order_by(desc('uploaded')).all()
    for ff in files:
        fd = ff.as_dict()
        fd['downloadUrl'] = 'https://server.ohmobility.com' + ff.downloadUrl
        all_files.append(fd)

    return jsonify(all_files)


@admin_.route('/delete-file/<file_id>')
@auth.login_required(role='admin')
def delete_uploaded_file(file_id):
    res = delete_media(file_id)
    if res == 1:
        return jsonify({'done': True, 'message': 'File deleted successfully.'})

    return jsonify({'done': False, 'message': 'File meta data not found. {}'.format(res)})


@admin_.route('/upload', methods=['POST'])
@auth.login_required(role='admin')
def upload_image():
    if request.method != "POST":
        return jsonify({'done': True})

    picture = request.files.get('image')
    folder = request.args.get('path')
    if folder is None:
        print('No path found')
        return jsonify({'done': False, 'message': 'No folder selected'}), 400

    if picture is None or picture.filename is None:
        return jsonify({'done': False, 'message': 'No file selected!'})

    # make folders if not exist
    path = 'static/uploads/' + folder

    if not os.path.exists(path):
        os.makedirs(path)
    # get the name of the picture
    filename = secure_filename(picture.filename)
    # save picture
    picture.save(os.path.join(path, filename))

    img_data = {
        "filename": filename,
        "downloadUrl": "/{}/{}".format(path, filename),
        "mimetype": picture.content_type,
        "path": '/' + path
    }

    img = UploadedMedia(
        filename=filename,
        downloadUrl=img_data['downloadUrl'],
        mimetype=img_data['mimetype'],
        path=img_data['path'])

    db.session.add(img)
    db.session.commit()

    img_data['id'] = img.id
    img_data['uploaded'] = img.uploaded

    return jsonify(img_data), 201


# get users
@admin_.route('/users', methods=['POST', 'GET'])
@auth.login_required(role='admin')
def load_users():
    users = User.query.order_by(User.created).all()
    all_users = []
    for item in users:
        all_users.append(item.as_dict())

    return jsonify({'done': True, 'data': all_users})


# get a user by id
@admin_.route('/users/<iid>')
@auth.login_required(role='admin')
def get_user_info(iid):
    u = User.query.filter_by(id=iid).first()
    if u is None:
        return jsonify({'done': False, 'message': 'Not found!'})

    # TODO return user info


@admin_.route('/profile')
@auth.login_required(role='admin')
def get_admin():
    if 'user' not in g:
        return jsonify({'done': False, 'message': 'Not found!'})

    return jsonify({'done': True, 'data': g.user.as_dict()})


# get dashboard stats
@admin_.route('/stats')
@auth.login_required(role='admin')
def stats():
    today_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
    # TODO: dashboard stats
    pass
