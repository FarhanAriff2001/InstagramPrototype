import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";

function OwnerTime({ ownerShowUrl, ownerImgUrl, owner, postShowUrl, created }) {
  return (
    <div className="card-body">
      <a href={ownerShowUrl}>
        <img
            src={ownerImgUrl}
            alt={owner}
            width={50}
            height={50} />
      </a>
      {'  '}
      <a href={ownerShowUrl}>
        <b>
            {owner}
        </b>
      </a>
      <span style={{ position: "absolute", top: 35, right: 15, textAlign: "right" }}>
        <a href={postShowUrl}>
            {created}
        </a>
      </span>
    </div>
  );
}

function PostImage({imgUrl, owner}) {
  return (
    <img 
    className="card-img-top" 
    src= {imgUrl} 
    alt= {owner} 
    styles="width:100%" />
  );
}

function PostLikesComments({likes, comments}) {
  return (
    <div className = "card-body">
      <h6 className = "cardtitle">
        {likes.numLikes}
        {' '}
        {likes.numLikes == 1 ? 'like' : 'likes'}
        </h6>    
      {comments.map((comment) => (
        <p className="card-text">
        <a href = {comment.ownerShowUrl}>
          <b>{comment.owner}</b>
        </a>{' '}
        {comment.text}
        </p>
      ))}
    </div>
  );
}

function OnePost({ post }) {
  // for postTime
  const [created, setCreated] = useState("");
  const [owner, setOwner] = useState("");
  const [ownerImgUrl, setOwnerImgUrl] = useState("");
  const [ownerShowUrl, setOwnerShowUrl] = useState("");
  const [postShowUrl, setPostShowUrl] = useState("");
  // for post picture
  const [imgUrl, setImgUrl] = useState("");
  // // for post likes
  const [likes, setLikes] = useState({});
  // // for post comments
  const [comments, setComments] = useState([]);
  // const [comments_url, setCommentsUrl] = useState("");

  useEffect(() => {
      let ignoreStaleRequest = false;
      fetch(post.url, { credentials: "same-origin" })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {
          if (!ignoreStaleRequest) {
            // for postTime
            setCreated(data.created);
            setOwner(data.owner);
            setOwnerImgUrl(data.ownerImgUrl);
            setOwnerShowUrl(data.ownerShowUrl);
            setPostShowUrl(data.postShowUrl);
            // // for post picture
            setImgUrl(data.imgUrl);
            // // for post likes
            setLikes(data.likes);
            // // for post comments
            setComments(data.comments);
            // setCommentsUrl(data.comments_url);
          }
        })
        .catch((error) => console.log(error));

      return () => {
        ignoreStaleRequest = true;
      };
  
  }, [post.url]);

  return (
      <div className="card mx-auto" styles="width:600px">
        <OwnerTime
          ownerShowUrl={ownerShowUrl}
          ownerImgUrl={ownerImgUrl}
          owner={owner}
          postShowUrl={postShowUrl}
          created={created} />
        <PostImage 
          imgUrl={imgUrl}
          owner={owner} />
        <PostLikesComments likes = {likes}
        comments = {comments} />
      </div>
  );
}

export default function Post({ url }) {
  const [posts, setPosts] = useState([]);
  useEffect(() => {
    let ignoreStaleRequest = false;
    fetch(url, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        if (!ignoreStaleRequest) {
          setPosts(data.results);
        }
      })
      .catch((error) => console.log(error));

    return () => {
      ignoreStaleRequest = true;
    };
  }, [url]);

  const rows = []
  posts.map((post) => {
    rows.push(<OnePost key = {post.postid} post= {post}/>);
  }
  );

  return (
    <div>{rows}</div>
  );
}

Post.propTypes = {
  url: PropTypes.string.isRequired,
};

