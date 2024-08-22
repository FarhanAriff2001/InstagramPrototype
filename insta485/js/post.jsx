import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import InfiniteScroll from "react-infinite-scroll-component";
import OnePost from "./OnePost";

export default function Post({ url }) {
  const [posts, setPosts] = useState([]);
  const [nextUrl, setNextUrl] = useState("");
  const [hasMore, setHasMore] = useState(true);
  const [isMount, setMount] = useState(false);

  useEffect(() => {
    let ignoreStaleRequest = false;

    if (url.length !== 0) {
      fetch(url, { credentials: "same-origin" })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {
          if (!ignoreStaleRequest) {
            setPosts([...posts, ...data.results]);
            setNextUrl(data.next);
            if (data.next === "" || data.results.splice(-1).postid === 1) {
              setHasMore(false);
            }
          }
        })
        .catch((error) => console.log(error));
    }

    return () => {
      ignoreStaleRequest = true;
    };
  }, [url]);

  const fetchData = (stringUrl) => {
    if (stringUrl.length !== 0) {
      fetch(stringUrl, { credentials: "same-origin" })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {
          setPosts([...posts, ...data.results]);
          setNextUrl(data.next);
          if (data.next === "" || data.results.splice(-1).postid === 1) {
            setHasMore(false);
          }
          setMount(true);
        })
        .catch((error) => console.log(error));
    }
  };

  const rows = posts.map((post) => (
    <OnePost key={post.postid} postid={post.postid} url={post.url} />
  ));

  if ({ isMount }) {
    return (
      <InfiniteScroll
        dataLength={posts.length}
        next={fetchData(nextUrl)}
        hasMore={hasMore}
        loader={<h4>Loading...</h4>}
        scrollThreshold={1.0}
        height={document.documentElement.scrollHeight}
        endMessage={
          <p style={{ textAlign: "center" }}>
            <b>Yay! You have seen it all</b>
          </p>
        }
      >
        {rows}
      </InfiniteScroll>
    );
  }
  return null;
}

Post.propTypes = {
  url: PropTypes.string.isRequired,
};
