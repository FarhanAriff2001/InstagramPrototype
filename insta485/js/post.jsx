import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import OnePost from './OnePost'

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
    <>
      {rows}
    </>
  );
}

Post.propTypes = {
  url: PropTypes.string.isRequired,
};

