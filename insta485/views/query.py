"""TO store query function."""

import arrow
import insta485


def query_logname(logname):
    """Query logname."""
    # Connect to database
    connection = insta485.model.get_db()
    # Query database
    cur = connection.execute(
        "SELECT username, fullname "
        "FROM users "
        "WHERE username == ?",
        (logname, )
    )
    users = cur.fetchone()
    return users


def query_index(logname):
    """Query Index."""
    connection = insta485.model.get_db()

    # Query database
    users = query_logname(logname)

    # Query database
    cur = connection.execute(
        "SELECT P.postid, P.filename, P.owner, P.created, "
        "U.filename as file, count(distinct L.likeid) as likes "
        "FROM posts P "
        "JOIN users U ON P.owner = U.username "
        "JOIN likes L on P.postid = L.postid "
        "GROUP BY P.postid "
        "ORDER BY P.postid DESC"
    )
    posts = cur.fetchall()

    for post in posts:
        timestamp = arrow.get(post["created"])
        post["created"] = timestamp.humanize()

    # Query database
    cur = connection.execute(
        "SELECT C.owner, C.text, C.postid "
        "FROM comments C "
        "JOIN posts P ON C.postid = P.postid",
    )
    comments = cur.fetchall()

    # Query database
    cur = connection.execute(
        "SELECT username2 "
        "FROM following "
        "WHERE username1 == ?",
        (logname, )
    )
    following = cur.fetchall()

    cur = connection.execute(
        "SELECT DISTINCT postid "
        "FROM likes "
        "WHERE owner == ?",
        (logname, )
    )
    likes = cur.fetchall()

    like_list = []
    for like in likes:
        like_list.append(like["postid"])

    context = {"users": users, "posts": posts, "comments": comments,
               "following": following, "likes": like_list}
    return context


def query_post(postid, logname):
    """Query Post."""
    # Connect to database
    connection = insta485.model.get_db()

    # Query database
    users = query_logname(logname)

    # Query database
    cur = connection.execute(
        "SELECT P.postid, P.filename, P.owner, P.created, "
        "U.filename as file, count(distinct L.likeid) as likes "
        "FROM posts P "
        "JOIN users U ON P.owner = U.username "
        "LEFT JOIN likes L on P.postid = L.postid "
        "WHERE P.postid == ?",
        (postid, )
    )
    post = cur.fetchone()

    timestamp = arrow.get(post["created"])
    post["created"] = timestamp.humanize()

    # Query database
    cur = connection.execute(
        "SELECT C.owner, C.text, C.postid, C.commentid "
        "FROM comments C "
        "WHERE C.postid == ?",
        (postid,)
    )
    comments = cur.fetchall()

    cur = connection.execute(
        "SELECT DISTINCT postid "
        "FROM likes "
        "WHERE owner == ?",
        (logname, )
    )
    likes = cur.fetchall()

    like_list = []
    for like in likes:
        like_list.append(like["postid"])

    context = {"users": users, "post": post,
               "comments": comments, "likes": like_list}
    return context


def query_explore(username):
    """Query Explore."""
    # Connect to database
    connection = insta485.model.get_db()

    # Query database
    users = query_logname(username)

    # Query database
    cur = connection.execute(
        "SELECT DISTINCT U.username, U.filename "
        "FROM users U "
        "WHERE U.username != ? "
        "EXCEPT "
        "SELECT DISTINCT U2.username, U2.filename "
        "FROM users U2 "
        "JOIN following F2 ON U2.username = F2.username2 "
        "WHERE F2.username1 = ?",
        (username, username, )
    )
    not_following = cur.fetchall()

    context = {"users": users, "n_following": not_following}
    return context


def query_user(username, logname):
    """Query User."""
    # Connect to database
    connection = insta485.model.get_db()

    users = query_logname(logname)

    cur = connection.execute(
        "SELECT username2 "
        "FROM following "
        "WHERE username1 == ? ",
        (logname, )
    )
    follow = cur.fetchall()

    follow_list = []
    for fol in follow:
        follow_list.append(fol["username2"])

    # Query database user
    cur = connection.execute(
        "SELECT username, fullname "
        "FROM users "
        "WHERE username == ?",
        (username, )
    )
    user = cur.fetchone()

    # Query database followers
    cur = connection.execute(
        "SELECT count(distinct username1) AS num "
        "FROM following "
        "WHERE username2 == ?",
        (username, )
    )
    followers = cur.fetchone()

    # Query database following
    cur = connection.execute(
        "SELECT count(distinct username2) AS num "
        "FROM following "
        "WHERE username1 == ?",
        (username, )
    )
    following = cur.fetchone()

    # Query database posts
    cur = connection.execute(
        "SELECT P.postid, P.filename "
        "FROM posts P "
        "WHERE P.owner == ?",
        (username, )
    )
    posts = cur.fetchall()

    # Query database posts
    cur = connection.execute(
        "SELECT count(distinct P.postid) AS num "
        "FROM posts P "
        "WHERE P.owner == ?",
        (username, )
    )
    count = cur.fetchone()
    context = {"users": users, "user": user, "follow": follow_list,
               "followers": followers, "following": following,
               "posts": posts, "count": count}
    return context


def query_followers(username, logname):
    """Query Followers."""
    # Connect to database
    connection = insta485.model.get_db()

    # Query database
    users = query_logname(logname)
    # List of user's followers and profile picture
    cur = connection.execute(
        "SELECT F.username1, U.filename as file "
        "FROM following F "
        "JOIN users U ON F.username1 = U.username "
        "WHERE F.username2 == ?",
        (username, )
    )
    followers = cur.fetchall()

    # List of logname's following
    cur = connection.execute(
        "SELECT username2 "
        "FROM following "
        "WHERE username1 == ?",
        (users["username"], )
    )
    follow = cur.fetchall()

    follow_list = []
    for fol in follow:
        follow_list.append(fol["username2"])

    context = {"users": users, "followers": followers, "follow": follow_list}
    return context


def query_following(username, logname):
    """Query Following."""
    # Connect to database
    connection = insta485.model.get_db()

    # Query database
    users = query_logname(logname)
    # List of user's followers and profile picture
    cur = connection.execute(
        "SELECT F.username2, U.filename as file "
        "FROM following F "
        "JOIN users U ON F.username2 = U.username "
        "WHERE F.username1 == ?",
        (username, )
    )
    following = cur.fetchall()

    # List of logname's following
    cur = connection.execute(
        "SELECT username2 "
        "FROM following "
        "WHERE username1 == ?",
        (users["username"], )
    )
    follow = cur.fetchall()

    follow_list = []
    for fol in follow:
        follow_list.append(fol["username2"])

    context = {"users": users, "following": following, "follow": follow_list}
    return context


def query_edit(logname):
    """Query Edit."""
    # Connect to database
    connection = insta485.model.get_db()

    # Query database
    users = query_logname(logname)
    # List of user's followers and profile picture
    cur = connection.execute(
        "SELECT filename, email "
        "FROM users "
        "WHERE username == ?",
        (users["username"], )
    )
    profile = cur.fetchone()

    context = {"users": users, "profile": profile}
    return context


def query_delete(logname):
    """Query Delete."""
    # Query database
    users = query_logname(logname)
    context = {"users": users}
    return context


def query_password(logname):
    """Query Password."""
    # Query database
    users = query_logname(logname)
    context = {"users": users}
    return context
