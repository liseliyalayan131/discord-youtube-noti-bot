from googleapiclient.discovery import build
import config
import db

youtube = build('youtube', 'v3', developerKey=config.YOUTUBE_API_KEY)

async def get_last_video_id():
    settings = await db.collection.find_one({'_id': 'settings'})
    return settings.get('last_video_id', None)

async def get_youtube_channel_id():
    settings = await db.collection.find_one({'_id': 'settings'})
    return settings.get('youtube_channel_id', None)

async def update_last_video_info(video_id, video_title, video_description, video_published_at):
    await db.collection.update_one(
        {'_id': 'settings'},
        {'$set': {
            'last_video_id': video_id,
            'video_title': video_title,
            'video_description': video_description,
            'video_published_at': video_published_at
        }},
        upsert=True
    )

async def check_new_video():
    youtube_channel_id = await get_youtube_channel_id()
    if not youtube_channel_id:
        print("YouTube kanal kimliği bulunamadı.")
        return None, None

    request = youtube.search().list(
        part='snippet',
        channelId=youtube_channel_id,
        order='date',
        maxResults=1
    )
    response = request.execute()
    print("YouTube Search Response:", response)
    if response['items']:
        video_id = response['items'][0]['id']['videoId']
        video_title = response['items'][0]['snippet']['title']
        video_description = response['items'][0]['snippet']['description']
        video_published_at = response['items'][0]['snippet']['publishedAt']

        print(f"Video ID: {video_id}")
        print(f"Video Başlığı: {video_title}")
        print(f"Video Açıklaması: {video_description}")
        print(f"Yayınlanma Tarihi: {video_published_at}")

        last_video_id = await get_last_video_id()
        if video_id != last_video_id:
            await update_last_video_info(video_id, video_title, video_description, video_published_at)
            return video_title, f"https://www.youtube.com/watch?v={video_id}"
    return None, None