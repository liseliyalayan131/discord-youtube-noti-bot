import discord
from discord.ext import commands
import config
import db
import datetime

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def get_settings():
    settings = await db.collection.find_one({'_id': 'settings'})
    return settings['discord_channel_id'], settings['role_id']

async def send_notification(bot, title, url):
    settings = await db.collection.find_one({'_id': 'settings'})
    channel_id, role_id = settings['discord_channel_id'], settings['role_id']
    video_published_at = settings['video_published_at']
    
    channel = bot.get_channel(channel_id)
    role = discord.utils.get(channel.guild.roles, id=role_id)

    embed = discord.Embed(
        title=f"📹 {title}",
        url=url,
        description=f"Yeni bir video yüklendi! [{title}]({url})",
        color=discord.Color.green()
    )
    embed.add_field(name="📅 Yayınlanma Tarihi", value=video_published_at, inline=True)
    embed.set_thumbnail(url=f"https://img.youtube.com/vi/{url.split('=')[-1]}/hqdefault.jpg")
    embed.set_footer(text="YouTube Video Bilgisi", icon_url="https://upload.wikimedia.org/wikipedia/commons/4/42/YouTube_icon_%282013-2017%29.png")

    await channel.send(f"{role.mention} 🎉 **Yeni bir video yüklendi!** 🎉")
    await channel.send(embed=embed)
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{current_time}] Bildirim gönderildi: {title}")

async def load_extensions():
    for extension in ['events.on_ready', 'events.setup', 'events.test']:
        try:
            await bot.load_extension(extension)
        except Exception as e:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{current_time}] Failed to load extension {extension}: {e}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(config.DISCORD_TOKEN)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())