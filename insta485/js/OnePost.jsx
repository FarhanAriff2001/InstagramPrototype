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

function PostLikes(props) {
    return (
        // Like-unlike button and display numLikes
        <>
        <button className="like-unlike-button" 
            onClick={props.onClick}>
            {props.lognameLikesThis ? 'unlike' : 'like'}
        </button>
        <h6 className = "card-title">
            {props.numLikes}
            {' '}
            {props.numLikes == 1 ? 'like' : 'likes'}
        </h6>    
        </>
    );
}

function PostComments( {comments} ) {
    return (
        comments.map((comment) => (
            <div className="card-text" key={comment.commentid}>
                <a href = {comment.ownerShowUrl}>
                    <b>{comment.owner}</b>
                </a>
                {' '}
                {comment.text}
            </div>
        ))
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
    const [lognameLikesThis, setLognameLikesThis] = useState(false);
    const [numLikes, setNumLikes] = useState(0);
    const [likeUrl, setLikeUrl] = useState("");

    // // for post comments
    const [comments, setComments] = useState([]);
    // const [comments_url, setCommentsUrl] = useState("");

    const handleLike = (e) => {
        // if logname likes a post
        if(!lognameLikesThis) {
            setLognameLikesThis(true);
            setNumLikes(numLikes + 1);

            const url = '/api/v1/likes/?postid=' + post.postid;
            fetch(url, { 
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                } 
            }, { credentials: "same-origin" })
            .then(() => {
                console.log('Like created');
            })
        }
        // if logname unlikes a post
        else {
            setLognameLikesThis(false);
            setNumLikes(numLikes - 1);

            fetch(likeUrl, { 
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                } 
             }, { credentials: "same-origin" })
            .then(() => {
                console.log('Like deleted');
            })
        }

        e.preventDefault();
    }


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
                setLognameLikesThis(data.likes.lognameLikesThis);
                setNumLikes(data.likes.numLikes);
                setLikeUrl(data.likes.url);
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

            <div className = "card-body">
                <PostLikes
                    lognameLikesThis={lognameLikesThis}
                    numLikes={numLikes}
                    onClick={handleLike}
                />
                <PostComments
                    comments={comments} 
                />
            </div>
        </div>
        <br />
        </>
    );
}