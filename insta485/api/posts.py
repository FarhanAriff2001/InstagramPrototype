"""REST API for posts."""
import flask
import insta485

@insta485.app.route('/api/v1/')
def get_api():
  context={
    "comments":"/api/v1/comments/",
    "likes":"/api/v1/likes/",
    "posts":"/api/v1/posts/",
    "url":"/api/v1/",
  }
  return flask.jsonify(**context)

@insta485.app.route('/api/v1/posts/<int:postid_url_slug>/')
def get_post(postid_url_slug):
    """Return post on postid.


    Example:
    {
      "created": "2017-09-28 04:33:28",
      "imgUrl": "/uploads/122a7d27ca1d7420a1072f695d9290fad4501a41.jpg",
      "owner": "awdeorio",
      "ownerImgUrl": "/uploads/e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg",
      "ownerShowUrl": "/users/awdeorio/",
      "postShowUrl": "/posts/1/",
      "url": "/api/v1/posts/1/"
    }
    """
    context = {
        "created": "2017-09-28 04:33:28",
        "imgUrl": "/uploads/122a7d27ca1d7420a1072f695d9290fad4501a41.jpg",
        "owner": "awdeorio",
        "ownerImgUrl": "/uploads/e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg",
        "ownerShowUrl": "/users/awdeorio/",
        "postid": "/posts/{}/".format(postid_url_slug),
        "url": flask.request.path,
    }
    return flask.jsonify(**context)

# @insta485.app.route('/api/v1/likes/?postid=<postid>', methods=['POST'])
# def post_likes():
#   return false

# @insta485.app.route('/api/v1/likes/<int:likeid>/', methods=['DELETE'])
# def delete_likes():
#   return false

@insta485.app.route('/api/v1/comments/', methods=['POST'])
def post_comments():
  """Post comments."""
  authenticate_users()
  # Get the text
  text = flask.request.get_json()['text']
  # text = flask.request.data.get('key')
  postid = flask.request.args.get('postid')
  username = flask.request.authorization['username']
  context = create_comment(username, postid, text)
  return flask.jsonify(context), 201

def create_comment(username, postid, text):
  """Make helper function to create comments"""
  connection = insta485.model.get_db()
  # INSERT INTO comments table
  connection.execute(
    "INSERT INTO comments (owner, postid, text) "
    "VALUES(?, ?, ?)",
    (username, postid, text, )
  )
  connection.commit()
  
  # find owner of the post
  cur = connection.execute(
    "SELECT owner FROM posts WHERE postid = ?",
    (postid, )
  )
  owner = cur.fetchone()
  
  # find info for the return
  cur = connection.execute(
    "SELECT commentid, owner,text FROM comments WHERE rowid = last_insert_rowid()",
  )
  comment = cur.fetchone()
  
  
  # comment_list = dict()
  # for comment in comments:
    # if username == owner:
    #   boole = True
    # else:
    #   boole = False
    # comment_list.update({'commentid': comment.commentid, 'lognameOwnsThis' : boole,
    #                      'owner': comment.owner, 
    #                      'ownerShowUrl' : "/users/{}/".format(comment.owner),
    #                      'text': comment.text,
    #                      'url' : "/api/v1/comments/{}/".format(comment.postid)
    #   })
  if username == owner['owner']:
    boole = True
  else:
    boole = False
    
    context = {"commentid" : comment.commentid, "lognameOwnsThis" : boole,
               "owner" : comment.owner, "ownerShowUrl" : "/users/{}/".format(comment.owner),
               "text" : comment.text, "url" : "/api/v1/comments/{}/".format(comment.postid)}
    
    return context

@insta485.app.route('/api/v1/comments/<int:commentid>/', methods=['DELETE'])
def delete_comments(commentid):
  
  authenticate_users()
  connection = insta485.model.get_db()
  commentid = commentid
  connection.execute(
      "DELETE FROM comments WHERE commentid = ?",
      (commentid, )
  )
  connection.commit()
  return flask.redirect('/api/v1/posts/1'), 204

@insta485.app.route('/api/v1/posts/', methods=['GET'])
def get_posts():
  authenticate_users()
  connection = insta485.model.get_db()
  cur = connection.execute(
    "SELECT * FROM posts",
  )
  users = cur.fetchall()
  return flask.jsonify(users), 200

def authenticate_users():
  connection = insta485.model.get_db()
  if flask.request.authorization:
    username = flask.request.authorization['username']
    keyword = flask.request.authorization['password']
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
      n_password = insta485.views.index.salt_password(keyword, salt)

    cur = connection.execute(
      "SELECT username from users WHERE username= ? AND password = ?",
      (username, n_password, )
    )
    if not cur.fetchone():
      flask.abort(403)
    flask.session['username'] = username
    flask.session['password'] = keyword
  if 'username' not in flask.session:
    return flask.abort(403)
  