import re
from googleapiclient.discovery import build


def get_video_id(URL):
    pattern = r'(?<=v=)[\w-]+'
    video_id = re.search(pattern, URL)
    return video_id[0]


def get_youtube_instance():
    DEVELOPER_KEY = 'AIzaSyB5N5FdV8vJFkxAbQsDuJro94lYRcPGIfY'
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'
    youtube = build(YOUTUBE_API_SERVICE_NAME,
                    YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)
    return youtube


def getAllTopLevelCommentReplies(topCommentId, replies, token):
    replies_response = youtube.comments().list(part='snippet',
                                               maxResults=100,
                                               parentId=topCommentId,
                                               pageToken=token).execute()

    for item in replies_response['items']:
        # Append the reply's text to the
        replies.append(item['snippet']['textDisplay'])

    if "nextPageToken" in replies_response:
        return getAllTopLevelCommentReplies(topCommentId, replies,
                                            replies_response['nextPageToken'])
    else:
        return replies


def get_comments(youtube, video_id, comments=[], token=''):

    # Stores the total reply count a top level commnet has.
    totalReplyCount = 0

    # Replies of the top-level comment might have.
    replies = []

    video_response = youtube.commentThreads().list(part='snippet',
                                                   videoId=video_id,
                                                   order='relevance',
                                                   pageToken=token).execute()
    for item in video_response['items']:
        comment = item['snippet']['topLevelComment']
        text = comment['snippet']['textDisplay']
        comments.append(text)

        # Get the total reply count:
        totalReplyCount = item['snippet']['totalReplyCount']

        if (totalReplyCount > 0):
            comments.extend(
                getAllTopLevelCommentReplies(comment['id'], replies, None))

        # Clear variable - just in case - not sure if need due "get_comments" function initializes the variable.
        replies = []

    if "nextPageToken" in video_response:
        return get_comments(youtube, video_id, comments,
                            video_response['nextPageToken'])
    else:
        storage_comments(comments, video_id)


def storage_comments(comments, video_id):
    file_name = 'comments_' + video_id + '.txt'
    with open(file_name, 'w') as f:
        for comment in comments:
            f.write(comment + '\n')


if __name__ == "__main__":
    URL = input('Enter YouTube link: ').split()
    video_id = get_video_id(URL)
    youtube = get_youtube_instance()
    get_comments(youtube, video_id)
