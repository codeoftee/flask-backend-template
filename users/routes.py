
from flask import jsonify, request, render_template
from werkzeug.security import check_password_hash, generate_password_hash

from server import db
from . import user_bp
from .auth import auth
from .models import User


# change user password
@user_bp.route('/update-password', methods=['POST', 'GET'])
@auth.login_required
def update_password():
    user_id = auth.current_user().id
    user_to_update = User.query.get_or_404(user_id)

    old_password = request.json.get('password')
    new_password = request.json.get('new_password')
    new_password2 = request.json.get('new_password2')
    if new_password != new_password2:
        return jsonify({'done': False, 'message': "Passwords doesn't match."})
    if check_password_hash(user_to_update.password_hash, old_password):
        # update password
        password_hash = generate_password_hash(new_password)
        user_to_update.password_hash = password_hash
        db.session.commit()
        return jsonify({'done': True, 'message': "Password updated successfully!"})

    return jsonify({'done': False, 'message': 'Current password is invalid'})


# edit user profile
@user_bp.route('/edit-profile', methods=['GET', 'POST'])
@auth.login_required
def edit_profile():
    user_id = auth.current_user().id
    user_to_update = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user_to_update.firstname = request.form['firstname']
        user_to_update.lastname = request.form['lastname']
        user_to_update.phone = request.form['phone']
        user_to_update.address = request.form['address']
        if user_to_update.firstname == '' or user_to_update.lastname == '' or user_to_update.phone == '':
            return jsonify({'done': False, 'message': 'Please fill all fields'}), 400
        try:
            db.session.commit()
        except Exception as e:
            return jsonify({'done': False, 'message': 'Unable to save profile. {}'.format(e)}), 500

    return jsonify({'done': True, 'message': 'Profile updated successfully.'})


# get user profile
@user_bp.route('/profile')
@auth.login_required
def get_user():
    user = auth.current_user()
    user_profile = User.query.filter_by(id=user.id).first()
    if user_profile is None:
        return jsonify({'message': 'User not found'}), 404
    # return user info
