import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";

// function LikeUnlikeButton() {
//   return (
//     <button className="like-unlike-button">
//       FIXME button text here
//     </button>
//   );
// }

// The parameter of this function is an object with a string called url inside it.
// url is a prop for the Post component.
export default function Post({ url }) {
  /* Display image and post owner of a single post */

  const [imgUrl, setImgUrl] = useState("");
  const [owner, setOwner] = useState("");

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
          setImgUrl(data.imgUrl);
          setOwner(data.owner);
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

  // Render post image and post owner
  return (
    /*<div className="post">
      <img src={imgUrl} alt="post_image" />
      <p>{owner}</p>
    </div>*/

  
    <div className="card mx-auto" style={{ width: 600 }}>
      <div className="card-body">
        <a href="{{url_for('show_user', username = post.owner)}}">
          <img
            src="{{url_for('return_files', filename = post.file)}}"
            alt="{{post.owner}}'s pic"
            width={50}
            height={50}
          />
        </a>
        <a href="{{url_for('show_user', username = post.owner)}}">
          <b>
            {post.owner}
          </b>
        </a>
        <span
          style={{ position: "absolute", top: 35, right: 15, textAlign: "right" }}
        >
          <a href="{{url_for('show_posts', postid = post.postid)}}">
            {post.created}
          </a>
        </span>
      </div>
    </div>

  );
}

Post.propTypes = {
  url: PropTypes.string.isRequired,
};
