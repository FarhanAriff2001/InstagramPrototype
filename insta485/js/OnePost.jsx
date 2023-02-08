import React, { useState, useEffect } from "react";

function OwnerTime({ ownerShowUrl, ownerImgUrl, owner, postShowUrl, created }) {
    return (
        <div class="card-body">
            <a href={ownerShowUrl}>
                <img
                    src={ownerImgUrl}
                    alt={{owner} + "'s pic"}
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

export default function OnePost({ post }) {

    const [comments, setComments] = useState([]);
    const [comments_url, setCommentsUrl] = useState("");
    const [created, setCreated] = useState("");
    const [imgUrl, setImgUrl] = useState("");
    const [likes, setLikes] = ({});
    const [owner, setOwner] = useState("");
    const [ownerImgUrl, setOwnerImgUrl] = useState("");
    const [ownerShowUrl, setOwnerShowUrl] = useState("");
    const [postShowUrl, setPostShowUrl] = useState("");

    useEffect(() => {
        // Declare a boolean flag that we can use to cancel the API request.
        let ignoreStaleRequest = false;

        // Call REST API to get the post's information
        fetch(post.url, { credentials: "same-origin" })
        .then((response) => {
            if (!response.ok) throw Error(response.statusText);
            return response.json();
        })
        .then((data) => {
            // If ignoreStaleRequest was set to true, we want to ignore the results of the
            // the request. Otherwise, update the state to trigger a new render.
            if (!ignoreStaleRequest) {
            setComments(data.comments);
            setCommentsUrl(data.comments_url);
            setCreated(data.created);
            setImgUrl(data.imgUrl);
            setLikes(data.likes);
            setOwner(data.owner);
            setOwnerImgUrl(data.ownerImgUrl);
            setOwnerShowUrl(data.ownerShowUrl);
            setPostShowUrl(data.postShowUrl);
            }
        })
        .catch((error) => console.log(error));

        return () => {
        // This is a cleanup function that runs whenever the Post component
        // unmounts or re-renders. If a Post is about to unmount or re-render, we
        // should avoid updating state.
        ignoreStaleRequest = true;
        };
    
    }, [url]);
  
    return (
        <div class="card mx-auto" style="width:600px">
            
            <OwnerTime
                ownerShowUrl={ownerShowUrl}
                ownerImgUrl={ownerImgUrl}
                owner={owner}
                postShowUrl={postShowUrl}
                created={created}
            />

        </div>
    );
}
