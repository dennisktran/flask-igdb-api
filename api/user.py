import models

import os
import sys
import secrets
from PIL import Image

from flask import Blueprint, request, jsonify, url_for, send_file
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from playhouse.shortcuts import model_to_dict

user = Blueprint('user', 'user', url_prefix='/user')


@user.route('/register', methods=["POST"])
def register():
    pay_file = request.files
    payload = request.form.to_dict()
    dict_file = pay_file.to_dict()

    print(payload, "<==== this is the payload")
    print(dict_file)

    payload['email'].lower()
    try:
        models.User.get(models.User.email == payload['email'])
        return jsonify(status={"code": 401, "message": "a user with the same name or email exists"})
    except models.DoesNotExist:
        payload['password'] = generate_password_hash(payload['password'])
        user = models.User.create(**payload)
        print(type(user))
        login_user(user)
        user_dict = model_to_dict(user)
        print(user_dict)
        print(type(user_dict))
        del user_dict['password']

        return jsonify(status={"code": 201, "message": "Success"})


@user.route('/login', methods=["POST"])
def login():
    payload = request.get_json()
    print(payload, '<-- this is payload')

    try:
        user = models.User.get(models.User.email == payload['email'])
        user_dict = model_to_dict(user)
        if(check_password_hash(user_dict['password'], payload['password'])):
            del user_dict['password']
            login_user(user)
            print(user, '<--- this is user')

            return jsonify(data=user_dict, status={"code": 200, "message": "Success"})
        else:
            return jsonify(data={}, status={"code": 401,
            "message": "Username or Password is incorrect"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401,
        "message": "Username or Password is incorrect"})


@user.route('<id>/clients', methods=["GET"])
def get_user_clients(id):
    user = models.User.get_by_id(id)
    print(user.clients, ".clientsss")

    clients = [model_to_dict(client) for client in user.clients]

    return jsonify(data=clients, status={"code": 201, "message": "Success"})

# @user.route('/logout', methods=['GET'])
# @login_required
# def logout():
#     """Logout the current user."""
#     user = current_user
#     user.authenticated = False
#     db.session.add(user)
#     db.session.commit()
#     logout_user()
#     return render_template("logout.html")
