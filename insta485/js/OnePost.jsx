import React, { useState, useEffect } from "react";
import moment from 'moment';
  
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
        styles="width:100%" 
    />
);
}

function PostLikesComments({likes, comments}) {
    return (
        <div className = "card-body">
            <h6 className = "card-title">
                {likes.numLikes}
                {' '}
                {likes.numLikes == 1 ? 'like' : 'likes'}
            </h6>    
            {comments.map((comment) => (
                <div className="card-text" key={comment.commentid}>
                    <a href = {comment.ownerShowUrl}>
                        <b>{comment.owner}</b>
                    </a>
                    {' '}
                    {comment.text}
                </div>
            ))}
        </div>
    );
}

export default function OnePost({ post }) {
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
                const m = moment.utc(data.created, 'YYYY-MM-DD hh:mm:ss');
                setCreated(m.local().fromNow());
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
        <>
        <div className="card mx-auto" style={{ width: '600px' }}>
            <OwnerTime
                ownerShowUrl={ownerShowUrl}
                ownerImgUrl={ownerImgUrl}
                owner={owner}
                postShowUrl={postShowUrl}
                created={created} />
            <PostImage
                imgUrl={imgUrl}
                owner={owner} />
            <PostLikesComments
                likes={likes}
                comments={comments} />
        </div>
        <br />
        </>
    );
}