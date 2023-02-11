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

function PostImage({ imgUrl, owner, onDoubleClick }) {
    return (
        <img
            className="card-img-top"
            src={imgUrl}
            alt={owner}
            style={{ width: "100%" }}
            onDoubleClick={onDoubleClick}
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
            <h6 className="card-title">
                {props.numLikes}
                {' '}
                {props.numLikes == 1 ? 'like' : 'likes'}
            </h6>
        </>
    );
}

// .then((data) =>{
//         // const newComments = comments.filter((comment) => comment.id !== id)
//     })

function EachComment({ comment, comments, setComments }) {

    const handleDelete = (event) => {
        let id = comment.commentid
        const url = '/api/v1/comments/' + id+'/';
        fetch(url, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        }, { credentials: "same-origin" })
        .then((response) => {
            if (!response.ok) throw Error(response.statusText)
        })
        .then((data) => {
            const newComments = comments.filter((comment) => 
            comment.commentid !== id)
            setComments(newComments)
        })
        .catch((error) => console.log(error));
        event.preventDefault();
    }

    return (
        <p>
            <a href={comment.ownerShowUrl}>
                <b>{comment.owner}</b>
            </a>
            {' '}
            <span className="comment-text">{comment.text}</span>
            {'  '}
            {comment.lognameOwnsThis &&
                <button className="delete-comment-button" onClick={handleDelete}>
                    {'Delete button'}
                </button>
            }
        </p>
    );
}

function PostComments({ comments, setComments }) {
    const rows = []
    comments.map((comment) => {
        rows.push(<EachComment key={comment.commentid} 
            comment={comment} 
            comments={comments} 
            setComments = {setComments} />);
    }
    );
    return (
        <>
            {rows}
        </>
    );
    // return (
    //     comments.map((comment) => (
    //         <div className="card-text" key={comment.commentid}>
    //             <a href = {comment.ownerShowUrl}>
    //                 <b>{comment.owner}</b>
    //             </a>
    //             {' '}
    //             {comment.text}
    //             {'  '}
    //             {comment.lognameOwnsThis && 
    //                 <button className="delete-comment-button" onClick={onClick}>
    //                     {'Delete button'}
    //                 </button>
    //             }
    //         </div>
    //     ))
    // );
}

// function NewComment(props) {

//     return  (
//         <form className="comment-form" onSubmit = {props.handleSubmit}>
//             <label>
//                 <input type="text" value={textEntry} onChange={props.handleChange} />
//             </label>
//         </form>
//     );
// }

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

    // // for post's comments
    const [comments, setComments] = useState([]);
    const [comments_url, setCommentsUrl] = useState("");

    // // for POST comments
    const [textEntry, setTextEntry] = useState('');

    const handleLike = (e) => {
        // if logname likes a post
        if (!lognameLikesThis) {
            setLognameLikesThis(true);
            setNumLikes(numLikes + 1);

            const url = '/api/v1/likes/?postid=' + post.postid;
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            }, { credentials: "same-origin" })
                .then((response) => {
                    if (!response.ok) throw Error(response.statusText);
                    return response.json();
                })
                .then((data) => {
                    setLikeUrl(data.url);
                })
                .catch((error) => console.log(error));

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
                .then((response) => {
                    if (!response.ok) throw Error(response.statusText)
                })
                .catch((error) => console.log(error));
        }
        e.preventDefault();
    }

    //function called when user types in text field
    const handleChange = (event) => {
        setTextEntry(event.target.value);
        console.log(event.target.value);
    }

    //function called when user submits
    const handleSubmit = (event) => {
        fetch(comments_url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'text': textEntry })
        }, { credentials: "same-origin" })
            .then((response) => {
                if (!response.ok) throw Error(response.statusText);
                return response.json();
            })
            .then((data) => {
                setComments(comments.concat(data));
            })
            .catch((error) => console.log(error));

        //prevents website from refreshing (default action of form submission)
        event.preventDefault();
    }

    const handleDoubleClick = (e) => {
        if (!lognameLikesThis) {
            setLognameLikesThis(true);
            setNumLikes(numLikes + 1);

            const url = '/api/v1/likes/?postid=' + post.postid;
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            }, { credentials: "same-origin" })
                .then((response) => {
                    if (!response.ok) throw Error(response.statusText);
                    return response.json();
                })
                .then((data) => {
                    setLikeUrl(data.url);
                })
                .catch((error) => console.log(error));
        }

        e.preventDefault();
    }

    // const handleDelete = (event) => {
    //     const url = '/api/v1/comments/?' + comment.commentid;
    //     fetch(url, {
    //         method: 'DELETE',
    //         headers: {
    //             'Content-Type': 'application/json'
    //         }
    //     }, { credentials: "same-origin" })
    //     .then((response) => {
    //             if (!response.ok) throw Error(response.statusText)
    //         })
    //     .catch((error) => console.log(error));
    //     e.preventDefault();
    // }

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
                    setCommentsUrl(data.comments_url);
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
                    created={created}
                />
                <PostImage
                    imgUrl={imgUrl}
                    owner={owner}
                    onDoubleClick={handleDoubleClick}
                />
                <div className="card-body">
                    <PostLikes
                        lognameLikesThis={lognameLikesThis}
                        numLikes={numLikes}
                        onClick={handleLike}
                    />
                    <PostComments
                        comments={comments}
                        setComments = {setComments}
                    />
                    <form className="comment-form" onSubmit={handleSubmit}>
                        <input
                            className="ui input"
                            type="text"
                            value={textEntry}
                            onChange={handleChange}
                        />
                    </form>
                    {/* <form className="comment-form" onSubmit = {handleSubmit}>
                    <input className="ui input" type="text" value={textEntry} onChange={handleChange} />
                </form> */}
                </div>
            </div>
            <br />
        </>
    );
}