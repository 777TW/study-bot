import discord
from discord.ext import commands
intents = discord.Intents.all()
intents.members = True
from classes import Cog_Extension


class reload(Cog_Extension):

    @commands.command()
    async def load(self, ctx, extension):
        await self.bot.load_extension("categories." + extension)
        await ctx.send(f'成功啟用{extension}。')
    
    @commands.command()
    async def unload(self, ctx, extension):
        await self.bot.unload_extension("categories." + extension)
        await ctx.send(f'成功停用{extension}。')

    @commands.command()
    async def reload(self, ctx, extension):
        await self.bot.reload_extension("categories." + extension)
        await ctx.send(f'成功重載{extension}。')

async def setup(bot):
    await bot.add_cog(reload(bot))
