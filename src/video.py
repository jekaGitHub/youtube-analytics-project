from googleapiclient.discovery import build
import os
from dotenv import load_dotenv


load_dotenv()

api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:
    def __init__(self, video_id):
        self.video_id = video_id
        try:
            self.video_response = Video.get_video(video_id)
        except IndexError:
            self.title = None
            self.video_url = None
            self.view_count = None
            self.like_count = None
        else:
            self.title = self.video_response['items'][0]['snippet']['title']
            self.video_url = "https://youtu.be/" + self.video_id
            self.view_count = self.video_response['items'][0]['statistics']['viewCount']
            self.like_count = self.video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return f'{self.title}'

    @classmethod
    def get_video(cls, video_id):
        video_response = youtube.videos().list(part="snippet,statistics", id=video_id).execute()
        return video_response


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
