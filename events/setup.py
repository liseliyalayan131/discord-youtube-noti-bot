from discord.ext import commands
import db
import discord
import datetime

class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='setup')
    async def setup(self, ctx, discord_channel_id: int, role_id: int, youtube_channel_id: str):
        await db.collection.update_one(
            {'_id': 'settings'},
            {'$set': {
                'discord_channel_id': discord_channel_id,
                'role_id': role_id,
                'youtube_channel_id': youtube_channel_id
            }},
            upsert=True
        )
        await ctx.send(f"✅ Ayarlar başarıyla kaydedildi:\n"
                       f"Discord Kanal ID: {discord_channel_id}\n"
                       f"Rol ID: {role_id}\n"
                       f"YouTube Kanal ID: {youtube_channel_id}")
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n{'='*60}")
        print(f"[{current_time}] Ayarlar başarıyla kaydedildi:")
        print(f"Discord Kanal ID: {discord_channel_id}")
        print(f"Rol ID: {role_id}")
        print(f"YouTube Kanal ID: {youtube_channel_id}")
        print(f"{'='*60}\n")

    @commands.command(name='view_settings')
    async def view_settings(self, ctx):
        settings = await db.collection.find_one({'_id': 'settings'})
        if settings:
            embed = discord.Embed(
                title="📋 Mevcut Ayarlar",
                color=discord.Color.green()
            )
            embed.add_field(name="Discord Kanal ID", value=settings.get('discord_channel_id', 'Bulunamadı'), inline=False)
            embed.add_field(name="Rol ID", value=settings.get('role_id', 'Bulunamadı'), inline=False)
            embed.add_field(name="YouTube Kanal ID", value=settings.get('youtube_channel_id', 'Bulunamadı'), inline=False)
            await ctx.send(embed=embed)
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n{'='*60}")
            print(f"[{current_time}] Mevcut Ayarlar:")
            print(f"Discord Kanal ID: {settings.get('discord_channel_id', 'Bulunamadı')}")
            print(f"Rol ID: {settings.get('role_id', 'Bulunamadı')}")
            print(f"YouTube Kanal ID: {settings.get('youtube_channel_id', 'Bulunamadı')}")
            print(f"{'='*60}\n")
        else:
            await ctx.send("❌ Mevcut ayarlar bulunamadı.")
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{current_time}] Mevcut ayarlar bulunamadı.")

    @commands.command(name='clear_settings')
    async def clear_settings(self, ctx):
        await db.collection.delete_one({'_id': 'settings'})
        await ctx.send("🗑️ Ayarlar başarıyla silindi.")
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n{'='*60}")
        print(f"[{current_time}] Ayarlar başarıyla silindi.")
        print(f"{'='*60}\n")

async def setup(bot):
    await bot.add_cog(Setup(bot))