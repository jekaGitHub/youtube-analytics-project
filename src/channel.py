import json
import os

from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

api_key: str = os.getenv('YT_API_KEY')

class Channel:
    """Класс для ютуб-канала"""
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
    
    def __str__(self):
        return f'{self.title} ({self.url})'
    
    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        return int(self.subscriber_count) - int(other.subscriber_count)
    
    def __gt__(self, other):
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        return self.subscriber_count >= other.subscriber_count

    def __lt__(self, other):
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        return self.subscriber_count <= other.subscriber_count

    def __eq__(self, other):
        return self.subscriber_count == other.subscriber_count


    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=api_key)

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

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
