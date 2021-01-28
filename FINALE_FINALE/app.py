from flask import Flask, redirect, render_template, request, url_for, send_from_directory
from datetime import datetime
from contact import Contact
from user import User
from database import database
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET'])
def register_get():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register_post():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    values = (
        None,
        request.form['username'],
        request.form['number'],
        User.hash_password(request.form['password']),
        timestamp
    )
    # i = User(*values).create()
    i = database.create_user(User(*values))
    # if i == 0:
    #     return redirect('/register')
    return redirect('/')


@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
#    login_post.logged_user = 0
    username = request.form['username']
    password = request.form['password']
    user = database.get_user_by_name(username)
    number = database.find_by_number(username)
    if user is not None:
        if user.verify_password(password) is True:
#            login_post.logged_user = user.get_id()
            return redirect(url_for('display_contacts', user_id=user.get_id()))
        else:
            return redirect('/login')
    elif number is not None:
        if number.verify_password(password) is True:
#            login_post.logged_user = number.get_id()
            return redirect(url_for('display_contacts', user_id=number.get_id()))
        else:
            return redirect('/login')
    return 'No such user found. Have you registered?'


@app.route('/contacts/<int:user_id>', methods=['GET'])
def display_contacts(user_id):
#    if login_post.logged_user == user_id:
        user = database.get_user_by_id(user_id)
        ping(user)
        contacts = database.get_contacts_by_user_id(user)

        if contacts is None:
            app.logger.info('No contacts with this user id')
            return render_template('contacts.html', user_id=user.get_id())
        elif contacts is False:
            app.logger.error('Error getting contact by user id')
            return 'Error getting contact by user id'
        app.logger.info('At least 1 contact with this user id exists')
        return render_template('contacts.html', contacts=contacts, user_id=user.get_id())
#    else:
        return redirect('/')


@app.route('/contacts/<int:user_id>/create', methods=['GET'])
def create_contact_get(user_id):
    user = database.get_user_by_id(user_id)
    ping(user)
    return render_template('create_contact.html', user_id=user.get_id())


@app.route('/contacts/<int:user_id>/create', methods=['POST'])
def create_contact_post(user_id):
    user = database.get_user_by_id(user_id)
    ping(user)
    values = (None, request.form['Name'], request.form['Number'], request.form['Note'], user.get_id())
    if database.create_contact(Contact(*values)) is True:
        return redirect(url_for('display_contacts', user_id=user.get_id()))
    else:
        return 'Could not create contact. Does this contact exist already?'


@app.route('/contacts/<int:user_id>/<int:contact_id>', methods=['GET'])
def display_contact(user_id, contact_id):
    user = database.get_user_by_id(user_id)
    ping(user)
    contact = database.get_contact_by_id(contact_id)
    if contact is None:
        app.logger.error('No contact with this id.')
    return render_template('contact.html', user_id=user.get_id(), contact=contact)


@app.route('/contacts/<int:user_id>/<int:contact_id>', methods=['POST'])
def update_contact(user_id, contact_id):
    user = database.get_user_by_id(user_id)
    ping(user)
    contact = database.get_contact_by_id(contact_id)
    try:
        if request.form['Update_button'] is not None:
            values = (contact_id, request.form['Name'], request.form['Number'], request.form['Note'], user.get_id())
            database.update_contact(Contact(*values))
    except KeyError:
        app.logger.info('KeyError exception encountered when updating contact.')
        try:
            if request.form['Delete_button'] is not None:
                database.delete_contact(database.get_contact_by_id(contact_id))
        except KeyError:
            app.logger.error('KeyError exception encountered when deleting contact.')
        except:
            app.logger.error('Unidentified exception encountered when deleting contact.')
    except:
        app.logger.info('Unidentified exception encountered when updating contact.')
    return redirect(url_for('display_contacts', user_id=user.get_id()))


@app.route('/contacts/<int:user_id>/myinfo')
def display_user_profile(user_id):
    user = database.get_user_by_id(user_id)
    if user is None or False:
        return 'Error displaying user profile'
    username = user.get_name()
    number = user.get_number()
    return render_template('user_info.html', user=user, username=username, number=number)


def ping(user):
    database.ping(user)


if __name__ == "__main__":
    app.run()
