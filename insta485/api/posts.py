"""REST API for posts."""
import flask
import insta485


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
  """Return post on postid."""
  authenticate_users()
  # get contexts
  # 1. Query for comments untill imgUrl
  comments = get_comments(postid_url_slug)
  comments_url = "/api/v1/comments/?postid={}".format(postid_url_slug)
  created = ""
  connection = insta485.model.get_db()
  cur = connection.execute(
    "SELECT filename FROM posts WHERE postid = ?",
    (postid_url_slug, )
  )
  imgUrl = "/uploads/{}".format(cur.fetchone()['filename'])
  # 2. Query for likes
  likes = get_likes(postid_url_slug)
  # 3. Query for owner till ownerShowUrl
  cur = connection.execute(
      "SELECT P.owner, U.filename as file "
      "FROM posts P "
      "JOIN users U ON P.owner = U.username "
      "WHERE P.postid == ?",
      (postid_url_slug, )
  )
  post = cur.fetchone()
  owner = post['owner']
  ownerImgUrl = "/uploads/{}".format(post['file'])
  ownerShowUrl = "/users/{}/".format(post['owner'])
  postShowUrl = "/posts/{}/".format(postid_url_slug)
  postid = postid_url_slug
  url =  "/api/v1/posts/{}/".format(postid_url_slug)
  context = {"comments" : comments, "comments_url" : comments_url,
             "created" : created, "imgUrl" : imgUrl, "likes" : likes,
             "owner" : owner, "ownerImgUrl" : ownerImgUrl,
             "ownerShowUrl" : ownerShowUrl,
             "postShowUrl" : postShowUrl, "postid" : postid, "url" : url}
  return flask.jsonify(context), 200


def get_comments(postid):
  """Make helper function to find comments for posts."""
  connection = insta485.model.get_db()
  # find info for the return
  cur = connection.execute(
    "SELECT C.commentid, C.owner, C.text "
    "FROM comments C "
    "WHERE C.postid = ?",
    (postid, )
  )
  comments = cur.fetchall()
  # def myFunc(e):
  #   return e['commentid']
  
  # comments.sort(key=myFunc)
  # comments = sorted(comments.items(), key=lambda x:x[0])
  logname = flask.session['username']
  comment_list = []
  for comment in comments:
    if logname == comment['owner']:
      boole = True
    else:
      boole = False
    comment_list.append({'commentid': comment['commentid'], 'lognameOwnsThis' : boole,
                         'owner': comment['owner'], 
                         'ownerShowUrl' : "/users/{}/".format(comment['owner']),
                         'text': comment['text'],
                         'url' : "/api/v1/comments/{}/".format(comment['commentid'])
      })
  return comment_list


def get_likes(postid):
  """Make helper function to find likes for posts."""
  connection = insta485.model.get_db()
  # find likes count
  cur = connection.execute(
    "SELECT count(distinct L.likeid) as likes  "
    "FROM likes L "
    "WHERE L.postid = ?",
    (postid, )
  )
  likes = cur.fetchone()
  # find likes owner and likeid if there
  logname = flask.session['username']
  cur = connection.execute(
    "SELECT L.owner, L.likeid  "
    "FROM likes L "
    "WHERE L.owner = ? and L.postid = ?",
    (logname, postid, )
  )
  likeOwner = cur.fetchone()
  # check if likeOwner is empty
  if likeOwner is not None:
    lognameLikesThis = True
    url = "/api/v1/likes/{}/".format(likeOwner['likeid'])
  else : 
    lognameLikesThis = False
    url = None
  # make likes dict
  likes_dict = {"lognameLikesThis" : lognameLikesThis, "numLikes" : likes['likes'],
                "url" : url}
  return likes_dict


@insta485.app.route('/api/v1/likes/', methods=['POST'])
def post_likes():
  """Post comments."""
  authenticate_users()
  postid = flask.request.args.get('postid')
  username = flask.request.authorization['username']
  connection = insta485.model.get_db()
  cur = connection.execute(
    "SELECT likeid, owner FROM likes "
    "WHERE owner = ? AND postid = ?",
    (username, postid, )
  )
  like = cur.fetchone()
  if like is not None:
    context = {"likeid" : like['likeid'] , 
               "url" : "/api/v1/likes/{}/".format(like['likeid']) 
               }
    return flask.jsonify(context), 200
  context = create_like(username, postid)
  return flask.jsonify(context), 201


def create_like(username, postid):
  """Make helper function to create like."""
  connection = insta485.model.get_db()
    # INSERT INTO likes table
  connection.execute(
    "INSERT INTO likes (owner, postid) "
    "VALUES(?, ?)",
    (username, postid, )
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
    "SELECT likeid, owner FROM likes WHERE rowid = last_insert_rowid()",
  )
  likes = cur.fetchone()
  context = {"likeid" : likes['likeid'], "url" : "/api/v1/likes/{}/".format(likes['likeid'])}
  return context


@insta485.app.route('/api/v1/likes/<int:likeid>/', methods=['DELETE'])
def delete_likes(likeid):
  """To delete like."""
  authenticate_users()
  connection = insta485.model.get_db()
  likeid = likeid
  logname = flask.session['username']
  cur = connection.execute(
      "SELECT likeid, owner "
      "FROM likes "
      "WHERE likeid = ?",
      (likeid, )
  )
  user = cur.fetchone()
  if user is None:
    flask.abort(404)
  else:
    if user['owner'] != logname:
      flask.abort(403)
  connection.execute(
      "DELETE FROM likes WHERE likeid = ?",
      (likeid, )
  )
  connection.commit()
  return flask.redirect('/api/v1/posts/1'), 204


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
  if username == owner['owner']:
    boole = True
  else:
    boole = False
    
  context = {"commentid" : comment['commentid'], "lognameOwnsThis" : boole,
               "owner" : comment['owner'], "ownerShowUrl" : "/users/{}/".format(comment['owner']),
               "text" : comment['text'], "url" : "/api/v1/comments/{}/".format(postid)}  
  return context


@insta485.app.route('/api/v1/comments/<int:commentid>/', methods=['DELETE'])
def delete_comments(commentid):
  """To delete comment."""
  authenticate_users()
  connection = insta485.model.get_db()
  commentid = commentid
  logname = flask.session['username']
  cur = connection.execute(
      "SELECT commentid, owner "
      "FROM comments "
      "WHERE commentid = ?",
      (commentid, )
  )
  user = cur.fetchone()
  if user is None:
    flask.abort(404)
  else:
    if user['owner'] != logname:
      flask.abort(403)
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
    "SELECT MAX(P.postid) as post FROM posts P",
  )
  lastrowid = cur.fetchone()['post']
  
  size = flask.request.args.get("size", default = 10, type = int)
  page = flask.request.args.get("page", default = 0, type = int)
  lte = flask.request.args.get("postid_lte", default = lastrowid, type = int)
  logname = flask.session['username']
  url1 = flask.request.environ['RAW_URI']
  # cur = connection.execute(
  #   "SELECT DISTINCT postid FROM posts P "
  #   "WHERE P.owner = ?",
  #   (logname, )
  # )  
  # cur = connection.execute(
  #   "SELECT DISTINCT postid FROM posts P JOIN following F "
  #   "ON P.owner = F.username2 WHERE F.username1 = ?",
  #   (logname, logname, )
  # )
  
  # find list of posts
  # cur = connection.execute(
  #   "SELECT P.postid FROM posts P "
  #   "ORDER BY postid DESC "
  #   "LIMIT ? OFFSET ?",
  #   (size, size*page, )
  # )
  # posts = cur.fetchall()
  cur = connection.execute(
    "SELECT postid "
    "FROM ( "
    "SELECT * FROM posts WHERE "
    "owner = ? or owner in "
    "(SELECT username2 FROM following where username1 = ?) "
    ") "
    "ORDER BY postid DESC "
    "LIMIT ? OFFSET ?",
    (logname, logname, size, size*page, )
  )
  posts = cur.fetchall()
  posts_lists = []
  counter = 0
  for i in posts:
    posts_lists.insert(counter, i["postid"])
    counter = counter + 1
  # posts_listsA = sorted(posts_lists, reverse =True)
  # fixed url
  url = "/api/v1/posts/"
  next = ""
  # next url
  if counter < size:
    next = ""
  else :
    size_s = "?size={}".format(size)
    page += 1
    page_s = "&page={}".format(page)
    lte_s = "&postid_lte={}".format(lte)
    next = url + size_s + page_s + lte_s
  # making list of results(post)
  results = []
  for post in posts_lists:
    results.append(
      {"postid" : post, 
       "url" : "/api/v1/posts/{}/".format(post)
       }
      )

  
  context = {"next" : next, "results" : results, "url" : url1}
  
  return flask.jsonify(context), 200

