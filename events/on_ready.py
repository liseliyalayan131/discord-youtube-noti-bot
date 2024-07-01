from discord.ext import commands
import datetime

class OnReady(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n{'='*60}")
        print(f"[{current_time}] Bot {self.bot.user.name} başarıyla giriş yaptı!")
        print(f"[{current_time}] Code By Harmoni")
        print(f"{'='*60}\n")

async def setup(bot):
    await bot.add_cog(OnReady(bot))