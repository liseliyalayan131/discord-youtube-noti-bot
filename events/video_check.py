from discord.ext import tasks
import youtube_check
from bot import send_notification

@tasks.loop(minutes=10)
async def video_check_task(bot):
    title, url = await youtube_check.check_new_video()
    if title and url:
        await send_notification(bot, title, url)