import discord
intents = discord.Intents.all()
intents.members = True
from datetime import datetime, timedelta, timezone
from classes import Cog_Extension
from discord import app_commands


class help(Cog_Extension):

    @app_commands.command(name = "help", description = "讓你了解每個指令個功能")
    async def help(self, interaction: discord.Interaction):
        embed=discord.Embed(color=0xd5b515, timestamp=datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=8))))
        embed.set_author(name="學測人2.0", icon_url="https://cdn.discordapp.com/attachments/956530927129997374/1116671823602516018/-removebg-preview.png")
        embed.add_field(name="todo", value="能在指定的時間提醒你事情\n如果不想要被別人看到你要機器人提醒你甚麼的話直接私訊機器人打指令就好了", inline=False)
        embed.add_field(name="todolist", value="能看到你已經設定了多少個todo\n而且只有你自己能看到", inline=False)
        embed.add_field(name="todoerase", value="設定todo的時候打錯? 已經完成了?\n使用這個指令就可以把設定好的todo刪掉\n可以使用 /todolist 可以查詢你的todo編號", inline=False)
        embed.add_field(name="ping", value="查詢機器人現在的ping", inline=False)
        embed.add_field(name="countdown", value="看看學測剩幾天...", inline=False)
        await interaction.response.send_message(embed=embed)

    
async def setup(bot):
    await bot.add_cog(help(bot))
