"""
Reddit Comment Extractor

This script extracts comments from a Reddit post and saves them as JSON.
It tries to use PRAW first (if configured) and falls back to direct HTTP requests.
"""

import json
from typing import List, Optional

from loguru import logger
from praw import Reddit
from praw.models import Submission
from pydantic import BaseModel
from tqdm.auto import tqdm

from schema import (
    Comments,
    RedditComment,
    RedditPostData,
)


class RedditCommentExtractor(object):
    def __init__(self, post_url: str, client: Reddit):
        self.post_url = post_url
        self.client = client

        self.post_id: Optional[str] = None
        self.submission: Optional[Submission] = None
        self.post_data: Optional[RedditPostData] = None
        self.comments: Optional[Comments] = None

    def __get_post_id(self) -> None:
        """Extract the post ID from a Reddit URL."""
        parts = self.post_url.split("/")
        for i, part in enumerate(parts):
            if part == "comments" and i + 1 < len(parts):
                logger.debug(f"Found post ID: {parts[i + 1]}")
                self.post_id = parts[i + 1]
                return
        raise ValueError("Could not extract post ID from URL")

    def __get_submission(self) -> None:
        """Get the submission from the post ID."""
        self.submission = self.client.submission(id=self.post_id)
        logger.debug(f"Submission: {self.submission}")

    def extract(self) -> None:
        self.__get_post_id()
        logger.info(f"Post ID: {self.post_id}")

        self.__get_submission()
        logger.info(f"Submission: {self.submission}")

        self.post_data = RedditPostData(
            id=self.submission.id,
            title=self.submission.title,
            created_utc=self.submission.created_utc,
            score=self.submission.score,
            num_comments=self.submission.num_comments,
            url=self.submission.url,
            selftext=self.submission.selftext,
            subreddit=str(self.submission.subreddit),
        )
        logger.info(f"Post data: {self.post_data}")

        logger.info("Extracting comments")
        self.submission.comments.replace_more(limit=None)
        logger.success("Extracted comments")

        logger.info("Converting comments to RedditComment objects")
        comments: List[RedditComment] = []
        for _, comment in tqdm(enumerate(self.submission.comments.list())):
            comment_data = RedditComment(
                id=comment.id,
                body=comment.body,
                created_utc=comment.created_utc,
                score=comment.score,
                depth=comment.depth,
                parent_id=comment.parent_id,
                permalink=comment.permalink,
            )
            comments.append(comment_data)

        self.comments = Comments(comments=comments)
        logger.success(f"Total comments: {len(comments)}")

    def __save_pydantic_to_json(self, model: BaseModel, filename: str) -> None:
        """Save the post data and comments to a JSON file."""
        with open(filename, "w") as f:
            json.dump(model.model_dump(), f, indent=4)

        logger.info(f"Saved to {filename}")

    def save(self) -> None:
        try:
            self.__save_pydantic_to_json(self.post_data, "post_data.json")
            self.__save_pydantic_to_json(self.comments, "comments.json")
        except Exception as e:
            logger.error(f"Error saving to JSON: {e}")
