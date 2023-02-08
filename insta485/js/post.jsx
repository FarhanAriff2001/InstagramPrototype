import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
//import OnePost from "./OnePost";

function OwnerTime({ ownerShowUrl, ownerImgUrl, owner, postShowUrl, created }) {
  return (
    <div class="card-body">
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

function OnePost({ post }) {
  
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

// The parameter of this function is an object with a string called url inside it.
// url is a prop for the Post component.
export default function Post({ url }) {
  /* Display image and post owner of a single post */

  const [posts, setPosts] = useState([]);

  // const [imgUrl, setImgUrl] = useState("");
  // const [owner, setOwner] = useState("");

  useEffect(() => {
    // Declare a boolean flag that we can use to cancel the API request.
    let ignoreStaleRequest = false;

    // Call REST API to get the post's information
    fetch(url, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // If ignoreStaleRequest was set to true, we want to ignore the results of the
        // the request. Otherwise, update the state to trigger a new render.
        if (!ignoreStaleRequest) {
          setPosts(...posts, ...data.results);
          // setImgUrl(data.imgUrl);
          // setOwner(data.owner);
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

  // For each post in posts
  const renderedPosts = posts.map((post) => {
    // Return HTML for one post
    return (
        <OnePost post={post} />
    );
  });

  // Render post image and post owner
  return (
    // <div className="post">
    //   <img src={imgUrl} alt="post_image" />
    //   <p>{owner}</p>
    // </div>
    {renderedPosts}
  );
}

Post.propTypes = {
  url: PropTypes.string.isRequired,
};
