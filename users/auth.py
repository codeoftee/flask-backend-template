from flask import jsonify, make_response, request
from flask_httpauth import HTTPTokenAuth
from werkzeug.security import check_password_hash, generate_password_hash

from server import db
from tools import number_generator, get_ip
from . import user_bp
from users.models import User, VerificationCodes

auth = HTTPTokenAuth(scheme='Bearer')


@user_bp.route('/test')
def admin_test():
    return jsonify({'done': True, 'message': 'Working'})


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@auth.verify_token
def verify_token(token):
    user = User.verify_auth_token(token)
    return user


@auth.get_user_roles
def get_user_roles(user):
    return user.get_roles()


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@user_bp.route('/send-password-reset-link', methods=['POST'])
def send_password_link():
    email = request.json.get('email')
    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({'done': False, 'message': 'No user found with the email address submitted.'})
    otp = number_generator()
    token = VerificationCodes(user_id=user.id, code=otp, active=True)
    db.session.add(token)
    db.session.commit()
    # TODO:: SEND resend link https://domain.com/reset-password/otp
    return jsonify({'done': True, 'message': 'We have sent a password reset link to your email address, '
                                             'click on the link to reset your password.', 'otp': otp})


@user_bp.route('/reset-password', methods=['POST'])
def reset_user_password():
    otp = request.json.get('otp')
    password = request.json.get('password')
    token = VerificationCodes.query.filter_by(code=otp).first()
    if token is None or token.active is False:
        return jsonify({'done': False, 'message': 'Invalid password reset token.'})
    # get user
    user = User.query.filter_by(id=token.user_id).first()
    if user is not None:
        password_hash = generate_password_hash(password)
        user.password_hash = password_hash
        db.session.commit()
        return jsonify({'done': True, 'message': 'Password reset successfully, you can now login with your new '
                                                 'password'})

    return jsonify({'done': False, 'message': 'We are unable to reset your password at the moment,'
                                              ' please try again later.'})


@user_bp.route('/login', methods=['POST'])
def login_user():
    password = request.json.get('password')
    email = request.json.get('email')

    user = User.query.filter(User.email == email).first()
    if user is None:
        return jsonify({'done': False, 'message': 'Invalid email or password.', 'error': 'not_found'}), 401

    if check_password_hash(user.password_hash, password):
        token = user.generate_auth_token()
        user.ip = get_ip()
        db.session.commit()
        return jsonify({'token': token, 'done': True, 'message': 'logged in'}), 200
    else:
        return jsonify({'done': False, 'message': 'Invalid email or password!'}), 401


# register user
@user_bp.route('/register', methods=['POST'])
def register_user():
    firstname = request.json.get('firstname')
    lastname = request.json.get('lastname')
    email = request.json.get('email')
    phone = request.json.get('phone')
    password = request.json.get('password')
    gender = request.json.get('gender')

    if not firstname or not lastname:
        return 'First name and last name are required'
    if not email:
        return 'Email is required'

    # check email
    existing = User.query.filter(User.email == email).first()
    if existing is not None:
        return jsonify({'done': False, 'message': 'This email address exists in our record for another user.'}), 400
    existing = User.query.filter(User.phone == phone).first()
    # check phone
    if existing is not None:
        return jsonify({'done': False, 'message': 'This phone number exists in our record for another user.'}), 400

    password_hash = generate_password_hash(password)
    new_user = User(firstname=firstname, lastname=lastname,
                    email=email, phone=phone, gender=gender, password_hash=password_hash,
                    ip=get_ip())
    db.session.add(new_user)
    db.session.commit()
    # TODO:: SEND WELCOME EMAIL

    token = new_user.generate_auth_token()
    print('TOKEN ---> ' + token)
    return jsonify({'done': True, 'message': 'Registration successful', 'token': token}), 201
