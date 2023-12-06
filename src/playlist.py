from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
# from isodate import parse_duration

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
        pass

    def show_best_video(self):
        pass


# if __name__ == '__main__':
#     obj1 = PlayList('PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw')
#     print(obj1.get_playlist('PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw'))
