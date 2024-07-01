from discord.ext import commands
import db
import discord
import datetime

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='test')
    async def test(self, ctx):
        settings = await db.collection.find_one({'_id': 'settings'})
        if not settings or 'last_video_id' not in settings:
            await ctx.send("❌ Son yüklenen video bulunamadı.")
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{current_time}] Son yüklenen video bulunamadı.")
            return

        video_id = settings['last_video_id']
        video_title = settings.get('video_title', 'Video Başlığı Bulunamadı')
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        video_description = settings.get('video_description', 'Açıklama bulunamadı.')
        video_published_at = settings.get('video_published_at', 'Yayınlanma tarihi bulunamadı.')

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n{'='*60}")
        print(f"[{current_time}] Video Bilgileri:")
        print(f"Video ID: {video_id}")
        print(f"Video Başlığı: {video_title}")
        print(f"Video URL: {video_url}")
        print(f"Video Açıklaması: {video_description}")
        print(f"Yayınlanma Tarihi: {video_published_at}")
        print(f"{'='*60}\n")

        embed = discord.Embed(
            title=f"📹 {video_title}",
            url=video_url,
            description=video_description,
            color=discord.Color.blue()
        )
        embed.add_field(name="📅 Yayınlanma Tarihi", value=video_published_at, inline=True)
        embed.set_thumbnail(url=f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg")
        embed.set_footer(text="YouTube Video Bilgisi", icon_url="https://upload.wikimedia.org/wikipedia/commons/4/42/YouTube_icon_%282013-2017%29.png")

        await ctx.send("🎉 **Yeni bir video yüklendi!** 🎉")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Test(bot))