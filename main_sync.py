import os
import re
import shutil
import time
from typing import Any

import httpx


def fetch_page_of_replies(
    client: httpx.Client, comment_id: str, page_token: str | None
):
    response = client.get(
        "/comments",
        params={
            "part": "snippet",
            "maxResults": 100,
            "parentId": comment_id,
            "pageToken": page_token,
        },
    )
    r_json: dict[str, Any] = response.json()

    replies: list[str] = [item["snippet"]["textDisplay"] for item in r_json["items"]]
    return replies, r_json.get("nextPageToken")


def fetch_replies(client: httpx.Client, comment_id: str):
    replies, next_page_token = fetch_page_of_replies(
        client, comment_id, page_token=None
    )

    while next_page_token:
        current_replies, next_page_token = fetch_page_of_replies(
            client, comment_id, next_page_token
        )
        replies += current_replies

    return replies


def fetch_page_of_comments(client: httpx.Client, video_id: str, page_token: str | None):
    response = client.get(
        "/commentThreads",
        params={
            "part": "snippet",
            "videoId": video_id,
            "order": "relevance",
            "pageToken": page_token,
        },
    )
    r_json: dict[str, Any] = response.json()

    comments: list[str] = []
    comment_ids_with_replies: list[str] = []

    for item in r_json["items"]:
        comment = item["snippet"]["topLevelComment"]
        comments.append(comment["snippet"]["textDisplay"])

        if item["snippet"]["totalReplyCount"] > 0:
            comment_ids_with_replies.append(comment["id"])

    return comments, comment_ids_with_replies, r_json.get("nextPageToken")


def fetch_comments(client: httpx.Client, video_id: str):
    (
        comments,
        comment_ids_with_replies,
        next_page_token,
    ) = fetch_page_of_comments(client=client, video_id=video_id, page_token=None)

    while next_page_token:
        (
            current_comments,
            current_comment_ids_with_replies,
            next_page_token,
        ) = fetch_page_of_comments(
            client=client, video_id=video_id, page_token=next_page_token
        )
        comments += current_comments
        comment_ids_with_replies += current_comment_ids_with_replies

    replies = []

    def task(comment_id: str):
        replies.extend(fetch_replies(client=client, comment_id=comment_id))

    for comment_id in comment_ids_with_replies:
        task(comment_id)
    return comments + replies


def clean_comment(comment: str):
    comment = re.sub(r"[^a-zA-Zа-яА-Я\s]", "", comment)
    comment = re.sub(r"\s+", " ", comment)
    return comment


def store_comments(comments: list[str], video_id: str):
    data = "\n".join(map(clean_comment, comments))

    with open(f"data_sync/comments_{video_id}.txt", "w+") as f:
        f.write(data)


def parse_video_id(video_url: str):
    pattern = r"(?<=/shorts/)[\w-]+" if "/shorts/" in video_url else r"(?<=v=)[\w-]+"
    match = re.search(pattern, video_url)
    assert match
    return match[0]


def fetch_and_store_comments_for_video(client: httpx.Client, video_url: str):
    video_id = parse_video_id(video_url)
    comments = fetch_comments(client=client, video_id=video_id)
    store_comments(comments=comments, video_id=video_id)


def main() -> None:
    if not os.path.exists("links.txt"):
        raise ValueError("File not found")

    if os.path.exists("data_sync"):
        shutil.rmtree("data_sync")
    os.mkdir("data_sync")

    video_urls = []
    with open("links.txt", "r") as f:
        video_urls += f.readlines()

    developer_key = "PUT DEVELOPER KEY HERE"
    client = httpx.Client(
        base_url="https://youtube.googleapis.com/youtube/v3",
        params={"key": developer_key},
    )

    for video_url in video_urls:
        fetch_and_store_comments_for_video(client=client, video_url=video_url)


if __name__ == "__main__":
    start_time = time.time()
    main()
    # time.sleep(5)
    end_time = time.time()

    video_urls = 0
    with open("links.txt", "r") as f:
        video_urls += len(f.readlines())

    print(video_urls, round(end_time - start_time, 3))
