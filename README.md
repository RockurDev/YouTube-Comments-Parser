# YouTube Comments Extractor

This script extracts comments from a YouTube video and saves them to a text file.

## Prerequisites

- Python 3.x
- `google-api-python-client` library
- A Google Developer API Key with YouTube Data API v3 enabled

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/RockurDev/Analysis-Of-YouTube-Comments.git
    ```
2. Navigate to the project directory:
    ```bash
    cd your-repo-name
    ```
3. Install the required libraries:
    ```bash
    pip install google-api-python-client
    ```

## Usage

1. Open the script `main.py` and replace the `DEVELOPER_KEY` in the `get_youtube_instance` function with your own YouTube Data API v3 key.
2. Run the script:
    ```bash
    python main.py
    ```
3. Enter the YouTube video URL when prompted.

## Functions

### get_video_id(URL)
Extracts the video ID from a YouTube URL.

**Parameters:**
- `URL` (str): The YouTube video URL.

**Returns:**
- `video_id` (str): The extracted video ID.

### get_youtube_instance()
Creates an instance of the YouTube API client.

**Returns:**
- `youtube` (object): The YouTube API client instance.

### getAllTopLevelCommentReplies(topCommentId, replies, token)
Recursively retrieves all replies to a top-level comment.

**Parameters:**
- `topCommentId` (str): The ID of the top-level comment.
- `replies` (list): A list to store the replies.
- `token` (str): The page token for pagination.

**Returns:**
- `replies` (list): A list of replies.

### get_comments(youtube, video_id, comments=[], token='')
Retrieves all comments from a YouTube video.

**Parameters:**
- `youtube` (object): The YouTube API client instance.
- `video_id` (str): The ID of the YouTube video.
- `comments` (list): A list to store the comments.
- `token` (str): The page token for pagination.

**Returns:**
- None

### storage_comments(comments, video_id)
Stores the comments in a text file.

**Parameters:**
- `comments` (list): A list of comments.
- `video_id` (str): The ID of the YouTube video.

**Returns:**
- None

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
