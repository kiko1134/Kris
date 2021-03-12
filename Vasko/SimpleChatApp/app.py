from flask import Flask
from flask import render_template, request, redirect, url_for
import logging

from flask_httpauth import HTTPBasicAuth

import hashlib
from message import Message
from user import  User
from friendship import Friendship


app: Flask = Flask(__name__)
auth = HTTPBasicAuth()

logFormatStr = '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
logging.basicConfig(format=logFormatStr, filename="global.log", level=logging.DEBUG)
formatter = logging.Formatter(logFormatStr, '%m-%d %H:%M:%S')
fileHandler = logging.FileHandler("flask-app.log")
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(formatter)
streamHandler = logging.StreamHandler()
streamHandler.setLevel(logging.DEBUG)
streamHandler.setFormatter(formatter)
app.logger.addHandler(fileHandler)
app.logger.addHandler(streamHandler)

app.logger.info("Logging is set up.")

my_id = None
my_name = "Admin"


@app.route('/')
def home():
    return render_template('home.html')


@auth.verify_password
def verify_password(username, password):
    user = User.find_by_username(username)
    if user:
        global my_name
        global my_id
        my_name = user.username
        my_id = user.id
        return user.verify_password(hashlib.sha256(password.encode('utf-8')).hexdigest())
    return False


@app.route('/register', methods=['GET', 'POST'])
def verify():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        values = (
            None,
            request.form['username'],
            User.hash_password(request.form['password'])
        )
        u = User(*values).create()

        return redirect(url_for('home'))


@app.route('/friends')
@auth.login_required
def show_friends():
    return render_template('friends.html', friendships=Friendship.all_for_u(my_name))


@app.route('/friends/new', methods=['POST'])
def new_friend():
    if request.method == 'POST':
        name = request.form['friend_name']
        user = User.find_by_username(my_name)
        users_list = User.get_usernames()
        if name:
            if name in users_list:
                new_friendship = Friendship(None, user.username, name, None, None).create()
                app.logger.debug('Friend with name: %s was just added by %s.', new_friendship.friend_name, new_friendship.sender_name)
            else:
                app.logger.error('User: %s is not registered.', name)

    return redirect(url_for('show_friends'))


@app.route('/friends/<int:friendship_id>/delete', methods=['POST'])
def delete_friend(friendship_id):
    friendship = Friendship.find(friendship_id)
    friendship.delete()

    app.logger.debug('Friend with name: %s was just deleted from %s\'s list of friends.', friendship.friend_name, my_name)
    return redirect(url_for('show_friends'))


@app.route('/friends/<int:friendship_id>')
def show_chat(friendship_id):
    friendship = Friendship.find(friendship_id)

    return render_template('friend.html', messages=Message.all_with(friendship.friendship_id), friendship=friendship, my_name=my_name)


@app.route('/friends/<int:friendship_id>/edit', methods=['GET', 'POST'])
def edit_nickname(friendship_id):
    friendship = Friendship.find(friendship_id)
    if request.method == 'GET':

        return render_template('edit_nickname.html', friendship=friendship)
    elif request.method == 'POST':
        friendship.nickname_2 = request.form['nickname_2']
        friendship.nickname_1 = request.form['nickname_1']
        friendship.save()

        app.logger.debug('The nickname for %s was edited.', friendship.friend_name)
        return redirect(url_for('show_chat', friendship_id=friendship.friendship_id, my_name=my_name))


@app.route('/message/new', methods=['POST'])
def new_message():
    if request.method == 'POST':
        friendship_id = request.form['friendship_id']
        content = request.form['message']
        if content:
            values = (None, friendship_id, my_name, content)
            Message(*values).create()
            app.logger.debug('%s just sent a new message.', my_name)
        return redirect(url_for('show_chat', friendship_id=friendship_id, my_name=my_name))
