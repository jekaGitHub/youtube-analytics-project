import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    # api_key: str = os.getenv('YT_API_KEY')
    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.youtube: object = Channel.get_service()
        self.__channel_id = channel_id

        info_channel = self.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title = info_channel['items'][0]['snippet']['title']
        self.description = info_channel['items'][0]['snippet']['description']
        self.url = info_channel['items'][0]['snippet']['thumbnails']['default']['url']
        self.subscriber_count = info_channel['items'][0]['statistics']['subscriberCount']
        self.video_count = info_channel['items'][0]['statistics']['videoCount']
        self.view_count = info_channel['items'][0]['statistics']['viewCount']

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=os.getenv('YT_API_KEY'))

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()))

    def to_json(self, filename):
        data = {
            "id": self.__channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscriber_count": self.subscriber_count,
            "video_count": self.video_count,
            "view_count": self.view_count
        }
        
        json_data = json.dumps(data)

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(json_data, f)
