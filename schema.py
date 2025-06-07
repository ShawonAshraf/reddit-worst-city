from typing import List

from pydantic import BaseModel


class RedditPostData(BaseModel):
    id: str
    title: str
    created_utc: float
    score: int
    num_comments: int
    url: str
    selftext: str
    subreddit: str


class RedditComment(BaseModel):
    id: str
    body: str
    created_utc: float
    score: int
    depth: int
    parent_id: str
    permalink: str


class Comments(BaseModel):
    comments: List[RedditComment]
