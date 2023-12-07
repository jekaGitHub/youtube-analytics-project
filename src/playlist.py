from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
import isodate
from datetime import timedelta

load_dotenv()

api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class PlayList:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id

        playlist_response = PlayList.get_playlist(playlist_id)
        self.title = playlist_response['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/playlist?list=' + self.playlist_id

    @classmethod
    def get_playlist(cls, playlist_id):
        playlist_response = youtube.playlists().list(
            part='snippet',
            id=playlist_id
        ).execute()
        return playlist_response

    @property
    def total_duration(self):
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        total = timedelta(seconds=0)
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total += duration
        return total

    def show_best_video(self):
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=','.join(video_ids)
                                               ).execute()

        popular_video = max(video_response, key=lambda x: x['items'][0]['statistics']['likeCount'])
        return popular_video.url_video
