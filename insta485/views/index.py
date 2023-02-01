"""
Insta485 index (main) view.

URLs include:
/
"""
import pathlib
import uuid
import hashlib
import os
import flask
import insta485
from insta485.views.query import (
    query_index, query_post, query_explore,
    query_user, query_followers,
    query_following, query_edit, query_delete, query_password
    )


# return files from var/upload/
@insta485.app.route('/uploads/<path:filename>')
def return_files(filename):
    """To get static files."""
    if 'username' not in flask.session:
        flask.abort(403)
    return flask.send_from_directory(insta485.app.config["UPLOAD_FOLDER"],
                                     filename, as_attachment=True)


# index page
@insta485.app.route('/')
def show_index():
    """Display / route."""
    # flask.session.clear()
    if 'username' in flask.session:
        username = flask.session['username']
        context = query_index(username)
        return flask.render_template('index.html', **context)
    return flask.redirect(flask.url_for('login'))


# login page
@insta485.app.route('/accounts/login/', methods=['GET'])
def login():
    """Login page."""
    if 'username' in flask.session:
        return flask.redirect(flask.url_for('show_index'))
    return flask.render_template('login.html')


# logout page
@insta485.app.route('/accounts/logout/', methods=['POST'])
def logout():
    """Logout page."""
    flask.session.clear()
    return flask.redirect(flask.url_for('login'))


# likes
@insta485.app.route('/likes/', methods=['POST'])
def likes():
    """Routing to directory /likes/."""
    target = flask.request.args.get("target")
    operation = flask.request.form["operation"]
    if operation == 'like':
        post_ids = flask.request.form["postid"]
        like(post_ids)
        if target is None:
            return flask.redirect('/')
        return flask.redirect(target)
    if operation == 'unlike':
        post_ids = flask.request.form["postid"]
        unlike(post_ids)
        if target is None:
            return flask.redirect('/')
        return flask.redirect(target)
    return flask.redirect(target)


def like(post_ids):
    """Make Helper function for likes."""
    connection = insta485.model.get_db()
    logname = flask.session["username"]
    # authenticate if logname already like the post(postid)
    cur = connection.execute(
        "Select likeid "
        "FROM likes WHERE postid=? AND owner=?",
        (post_ids, logname, )
    )
    if cur.fetchone() is not None:
        flask.abort(409)
    connection.execute(
        "INSERT INTO likes (owner, postid) "
        "VALUES(?, ?)",
        (logname, post_ids, )
    )
    connection.commit()


def unlike(post_ids):
    """Make Helper function for likes."""
    connection = insta485.model.get_db()
    logname = flask.session["username"]
    # authenticate if logname already unlike (not like) the post(postid)
    cur = connection.execute(
        "SELECT owner "
        "FROM likes WHERE postid=? AND owner=?",
        (post_ids, logname, )
    )
    if cur.fetchone() is None:
        flask.abort(409)
    cur = connection.execute(
        "DELETE FROM likes WHERE postid=? AND owner=?",
        (post_ids, logname, )
    )
    connection.commit()


# comments
@insta485.app.route('/comments/', methods=['POST'])
def comments():
    """Route to directory /comments/."""
    target = flask.request.args.get("target")
    operation = flask.request.form["operation"]

    if operation == 'create':
        connection = insta485.model.get_db()
        postid = flask.request.form["postid"]
        text = flask.request.form["text"]
        logname = flask.session["username"]
        connection.execute(
            "INSERT INTO comments (owner, postid, text) "
            "VALUES(?, ?, ?)",
            (logname, postid, text, )
        )
        connection.commit()
        if target is None:
            return flask.redirect('/')
        return flask.redirect(target)
    if operation == 'delete':
        connection = insta485.model.get_db()
        commentid = flask.request.form["commentid"]
        logname = flask.session["username"]
        connection.execute(
            "DELETE FROM comments WHERE commentid = ?",
            (commentid, )
        )
        connection.commit()
        return flask.redirect(target)
    return flask.redirect(target)


# posts
@insta485.app.route('/posts/', methods=['POST'])
def posts():
    """Route to directory /posts/."""
    target = flask.request.args.get("target")
    operation = flask.request.form["operation"]
    if operation == 'create':
        files = flask.request.files['file']
        p_create(files)
        if target is None:
            logname = flask.session['username']
            return flask.redirect('/users/'+logname+'/')
        return flask.redirect(target)
    if operation == 'delete':
        post_ids = flask.request.form["postid"]
        p_delete(post_ids)
        if target is None:
            logname = flask.session['username']
            return flask.redirect('/users/'+logname+'/')
        return flask.redirect(target)
    return flask.redirect(target)


def p_create(files):
    """Make helper function for posts."""
    filename = files.filename
    uuid_basename = encryption_files(files, filename)

    logname = flask.session["username"]
    connection = insta485.model.get_db()

    connection.execute(
        "INSERT INTO posts (filename,owner) "
        "VALUES (?, ?)",
        (uuid_basename, logname, )
    )

    connection.commit()


def p_delete(post_ids):
    """Make helper function for posts."""
    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT P.filename as file "
        "FROM posts P WHERE P.postid = ?",
        (post_ids, )
    )
    files = cur.fetchone()
    path = insta485.app.config["UPLOAD_FOLDER"]/files['file']
    os.remove(path)

    cur = connection.execute(
        "DELETE FROM posts WHERE postid=?",
        (post_ids, )
    )
    connection.commit()


# likes
@insta485.app.route('/following/', methods=['POST'])
def following():
    """Route to directory /following/."""
    target = flask.request.args.get("target")
    operation = flask.request.form["operation"]
    if operation == 'follow':
        username = flask.request.form["username"]
        follow(username)
        return flask.redirect(target)
    if operation == 'unfollow':
        username = flask.request.form["username"]
        unfollow(username)
        return flask.redirect(target)
    return flask.redirect(target)


def follow(username):
    """Make helper function for following."""
    connection = insta485.model.get_db()
    username2 = username
    logname = flask.session["username"]
    connection.execute(
        "INSERT INTO following (username1, username2) "
        "VALUES(?, ?)",
        (logname, username2, )
    )
    connection.commit()


def unfollow(username):
    """Make helper function for following."""
    connection = insta485.model.get_db()
    username2 = username
    logname = flask.session["username"]
    connection.execute(
        "DELETE FROM following WHERE username1=? AND username2=?",
        (logname, username2, )
    )
    connection.commit()


# /account/?target=URL
@insta485.app.route('/accounts/', methods=['POST'])
def accounts():
    """Route to directory accounts."""
    target = flask.request.args.get("target")
    operation = flask.request.form["operation"]

    # if login
    if operation == 'login':
        login2()
        if target is None:
            return flask.redirect('/')
    # if create
    if operation == 'create':
        create2()
        flask.session['username'] = flask.request.form['username']
        flask.session['password'] = flask.request.form['username']

    if operation == 'delete':
        delete2()

    if operation == 'update_password':
        password2()

    if operation == 'edit_account':
        edit2()

    return flask.redirect(target)


# helper function for /accounts/
def login2():
    """Make helper function for operation:login."""
    username = flask.request.form['username']
    keyword = flask.request.form['password']

    if (username is None) or (keyword is None):
        flask.abort(400)
    connection = insta485.model.get_db()
    # authenticate username
    cur = connection.execute(
        "SELECT username from users WHERE username= ?",
        (username, )
    )
    if not cur.fetchone():
        flask.abort(403)
    else:
        # authenticate password
        cur = connection.execute(
            "SELECT password from users WHERE username= ?",
            (username, )
        )
        password_s = cur.fetchone()
        if password_s is None:
            flask.abort(403)
        stri = password_s['password']
        lists = stri.split('$')
        salt = lists[1]
        n_password = salt_password(keyword, salt)

    cur = connection.execute(
        "SELECT username from users WHERE username= ? AND password = ?",
        (username, n_password, )
    )

    if not cur.fetchone():
        flask.abort(403)

    flask.session['username'] = username
    flask.session['password'] = keyword


def encryption_files(file_obj, filename):
    """Make helper function to encrypt files."""
    stem = uuid.uuid4().hex
    suffix = pathlib.Path(filename).suffix.lower()
    uuid_basename = f"{stem}{suffix}"
    # Save to disk
    path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
    file_obj.save(path)
    return uuid_basename


def hashing_password(keyword):
    """Make helper function to get the hashed password."""
    algorithm = 'sha512'
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + keyword
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    return password_db_string


def salt_password(keyword, salt):
    """Make helper function to get the password after salt."""
    algorithm = 'sha512'
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + keyword
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    return password_db_string


def create2():
    """Make helper function for operation : create."""
    username = flask.request.form['username']
    keyword = flask.request.form['password']
    fullname = flask.request.form['fullname']
    email = flask.request.form['email']
    files = flask.request.files['file']

    if (username is None) or (keyword is None) or (
        (fullname is None) or (email is None) or (
            ('file' not in flask.request.files))):
        flask.abort(400)

    filename = files.filename
    uuid_basename = encryption_files(files, filename)
    password_db_string = hashing_password(keyword)
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT DISTINCT username "
        "FROM users",
    )
    users = cur.fetchall()
    users_list = []
    for user in users:
        users_list.append(user["username"])

    if username in users_list:
        flask.abort(409)

    cur = connection.execute(
        "INSERT INTO users "
        "(username, fullname, email, filename, password) "
        "VALUES (?, ?, ?, ?, ?)",
        (username, fullname, email, uuid_basename, password_db_string)
    )
    connection.commit()


def delete2():
    """Make helper function for opretaion : delete."""
    if 'username' not in flask.session:
        flask.abort(403)

    username = flask.session['username']
    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT U.filename as file "
        "FROM users U WHERE U.username = ?",
        (username, )
    )
    files = cur.fetchone()
    path = insta485.app.config["UPLOAD_FOLDER"]/files['file']
    os.remove(path)
    cur = connection.execute(
        "SELECT P.filename as file "
        "FROM posts P WHERE owner = ?",
        (username, )
    )
    files = cur.fetchall()
    for file in files:
        path = insta485.app.config["UPLOAD_FOLDER"]/file['file']
        os.remove(path)
    cur = connection.execute(
        "DELETE FROM users WHERE username = ?",
        (username, )
    )
    flask.session.clear()


def password2():
    """Make helper function for operation : delete."""
    if 'username' not in flask.session:
        flask.abort(403)
    old_password = flask.request.form['password']
    new_password = flask.request.form['new_password1']
    new_password2 = flask.request.form['new_password2']
    username = flask.session['username']

    if (old_password is None) or (new_password is None) or (
        (new_password2 is None)
            ):
        flask.abort(400)

    # verify if old_password with the hash
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT password from users WHERE username=?",
        (username, )
    )
    password_s = cur.fetchone()
    stri = password_s['password']
    lists = stri.split('$')
    salt = lists[1]
    n_password = salt_password(old_password, salt)

    if n_password != stri:
        flask.abort(403)

    # verify new1 == new2
    if new_password != new_password2:
        flask.abort(401)
    n_password = hashing_password(new_password)

    # Updata hashed password
    cur = connection.execute(
        "UPDATE users "
        "SET password=? "
        "WHERE username=?",
        (n_password, username, )
    )

    connection.commit()


def edit2():
    """Make helper function for operation : edit."""
    if 'username' not in flask.session:
        flask.abort(403)
    files = flask.request.files['file']
    fullname = flask.request.form['fullname']
    email = flask.request.form['email']
    username = flask.session['username']
    # abort if fullname or email is none
    if (fullname is None) or (email is None):
        flask.abort(400)

    connection = insta485.model.get_db()

    # if no photo, only fullname and email updated
    if 'file' not in flask.request.files:
        connection.execute(
            "UPDATE users "
            "SET fullname=?, email=? "
            "WHERE username=?",
            (fullname, email, username, )
        )
        connection.commit()
    # if photo included, then update all, and delete the old photo
    else:
        filename = files.filename
        uuid_basename = encryption_files(files, filename)
        connection.execute(
            "UPDATE users "
            "SET fullname=?, email=?, filename=? "
            "WHERE username=?",
            (fullname, email, uuid_basename, username, )
        )
        connection.commit()


# END OF helper function for /accounts/

# create page
@insta485.app.route('/accounts/create/', methods=['GET'])
def create():
    """Create page."""
    if 'username' in flask.session:
        return flask.redirect(flask.url_for('edit'))
    return flask.render_template('create.html')


# edit page
@insta485.app.route('/accounts/edit/', methods=['GET'])
def edit():
    """Edit page."""
    username = flask.session['username']
    context = query_edit(username)
    return flask.render_template('edit.html', **context)


# delete page
@insta485.app.route('/accounts/delete/', methods=['GET'])
def delete():
    """Delete page."""
    username = flask.session['username']
    context = query_delete(username)
    return flask.render_template('delete.html', **context)


# update_password page
@insta485.app.route('/accounts/password/', methods=['GET'])
def show_password():
    """Password page."""
    username = flask.session['username']
    context = query_password(username)
    return flask.render_template('password.html', **context)


# post page
@insta485.app.route('/posts/<int:postid>/', methods=['GET'])
def show_posts(postid):
    """Post pages."""
    if 'username' not in flask.session:
        return flask.redirect('/accounts/login/')
    username = flask.session['username']
    context = query_post(postid, username)
    return flask.render_template('post.html', **context)


# explore page
@insta485.app.route('/explore/')
def show_explore():
    """Explore page."""
    username = flask.session['username']
    context = query_explore(username)
    return flask.render_template('explore.html', **context)


# user page
@insta485.app.route('/users/<username>/')
def show_user(username):
    """Users pages."""
    if 'username' not in flask.session:
        return flask.redirect('/accounts/login/')
    logname = flask.session['username']
    context = query_user(username, logname)
    return flask.render_template('user.html', **context)


# follower page
@insta485.app.route('/users/<username>/followers/')
def show_followers(username):
    """Followers pages."""
    if 'username' not in flask.session:
        return flask.redirect('/accounts/login/')
    logname = flask.session['username']
    context = query_followers(username, logname)
    return flask.render_template('followers.html', **context)


# following page
@insta485.app.route('/users/<username>/following/')
def show_following(username):
    """Following pages."""
    if 'username' not in flask.session:
        return flask.redirect('/accounts/login/')
    logname = flask.session['username']
    context = query_following(username, logname)
    return flask.render_template('following.html', **context)
