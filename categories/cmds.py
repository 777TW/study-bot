import discord
from discord.ext import commands
from discord import app_commands
import json
intents = discord.Intents.all()
intents.members = True
from classes import Cog_Extension
import datetime
from datetime import date
from functions import now_time, clear_over_time, alarm_set, find_todolist, get_timeint
import os
dirname = os.path.dirname(__file__).replace('\categories', '')


class cmds(Cog_Extension):

    @commands.command()
    async def sync(self, ctx) -> None:
        fmt = await ctx.bot.tree.sync()
        await ctx.send(f'Synced {len(fmt)} commands')

    #ping
    @app_commands.command(name = "ping", description = "查詢機器人ping")
    async def ping(self, interaction = discord.Interaction):
        await interaction.response.send_message(f'{round(self.bot.latency*1000)}ms')

    #countdown
    @app_commands.command(name = "countdown", description = "來看看分科剩幾天吧")
    async def countdown(self, interaction: discord.Interaction):
        time = datetime.datetime.now(   tz=datetime.timezone(datetime.timedelta(hours=8))).replace(tzinfo = None)
        date = "2024/07/12 00:00:00"
        datestr = datetime.datetime.strptime(date, "%Y/%m/%d %H:%M:%S")
        duration = datestr - time
        game = discord.Game(f'學測倒數{duration.days + 1}天')
        await interaction.response.send_message(f'分科倒數{duration.days + 1}天...')
        await self.bot.change_presence(status=discord.Status.online, activity=game)
        
    #todo
    @app_commands.command(name = "todo", description = "能幫助你記住事情的神奇指令")
    @app_commands.describe(日期 = "格式範例 2024/1/1", 時間 = "格式範例 12:30", 事情 = "你想要被提醒的文字", 次數 = "你想要他提醒你的次數")
    @app_commands.choices(頻率  = [
        app_commands.Choice(name = "一次就好", value = "once"),
        app_commands.Choice(name = "一個小時一次", value = "once per hour"),
        app_commands.Choice(name = "一天兩次", value = "twice a day"),
        app_commands.Choice(name = "一天一次", value = "once a day"),
        app_commands.Choice(name = "一個禮拜一次", value = "once a week"),
        app_commands.Choice(name = "一個月一次", value = "once a month"),
        app_commands.Choice(name = "一年一次", value = "once a year"),
    ])
    async def todo(self, interaction: discord.Interaction, 日期: str, 時間: str, *, 事情: str, 頻率: app_commands.Choice[str], 次數: int):
        channel_id = interaction.channel.id
        day_splited = 日期.split("/")
        time_splited = 時間.split(":")
        now_timeint = now_time()


        try:
            timeint = int(day_splited[0])*100000000 + int(day_splited[1])*1000000 + int(day_splited[2])*10000 + int(time_splited[0])*100 + int(time_splited[1])
        except:
            await interaction.response.send_message("輸入格式錯誤！\n正確格式應為 /todo 年/月/日 小時:分鐘 事情\n範例： /todo 2023/1/1 00:00 新年快樂")
            return
        try:
            date(int(day_splited[0]), int(day_splited[1]), int(day_splited[2]))
        except:
            await interaction.response.send_message("沒有此日期！\n正確格式應為 /todo 年/月/日 小時:分鐘 事情\n範例： /todo 2023/1/1 00:00 新年快樂")
            return
        if now_timeint >= timeint:
            await interaction.response.send_message("請輸入一個大於現在的時間！\n正確格式應為 /todo 年/月/日 小時:分鐘 事情\n範例： /todo 2023/1/1 00:00 新年快樂")
            return
        elif int(time_splited[0]) >= 24 or int(time_splited[0]) < 0 or int(time_splited[1]) >= 60 or int(time_splited[1]) < 0:
            await interaction.response.send_message("時間格式錯誤！\n正確格式應為 /todo 年/月/日 小時:分鐘 事情\n範例： /todo 2023/1/1 00:00 新年快樂")
            return



        with open(r"{}\json\settings.json".format(dirname), "r", encoding = "utf-8") as jsettings_id_read:
            jsettings_id_loaded = json.load(jsettings_id_read)
            todo_id = int(jsettings_id_loaded['todo_id'])
            jsettings_id_loaded['todo_id'] = str(todo_id + 1)
        with open(r"{}\json\settings.json".format(dirname), "w", encoding = "utf-8") as jsettings_id_write:
            json.dump(jsettings_id_loaded, jsettings_id_write)


        clear_over_time()


        with open(r"{}\json\todo.json".format(dirname), "r", encoding = "utf-8") as jtodo_input_read:
            jtodo_input_loaded = json.load(jtodo_input_read)
        with open(r"{}\json\todo.json".format(dirname), "w", encoding = "utf-8") as jtodo_input_write:
            jtodo_input_loaded.append({
                "date": {
                    "year": int(day_splited[0]), 
                    "month": int(day_splited[1]), 
                    "day": int(day_splited[2]), 
                    "hour": int(time_splited[0]), 
                    "minute": int(time_splited[1]) 
                },
                "thing": 事情, 
                "channel_id": channel_id, 
                "user": {
                    "user_name": str(interaction.user),
                    "user_id": interaction.user.id 
                },
                "timeint": timeint,
                "todo_id": todo_id,
                "frequency": 頻率.value,
                "frequency_n": 頻率.name,
                "times": 次數,
            })
            json.dump(jtodo_input_loaded, jtodo_input_write)



            with open(r"{}\json\time.json".format(dirname), "r", encoding = "utf-8") as jcheck_time_set_read:
                jcheck_time_set_loaded = json.load(jcheck_time_set_read)
            ct = 0
            if str(jcheck_time_set_loaded) != "[]":
                for time in jcheck_time_set_loaded:
                    if time != timeint:
                        ct += 1
                if ct == len(jcheck_time_set_loaded):
                    with open(r"{}\json\time.json".format(dirname), "w", encoding = "utf-8") as jcheck_time_set_write:
                        jcheck_time_set_loaded.append(timeint)
                        json.dump(jcheck_time_set_loaded, jcheck_time_set_write)

                    
                    alarm_set(int(day_splited[0]), int(day_splited[1]), int(day_splited[2]), int(time_splited[0]), int(time_splited[1]), timeint, self.bot)
            else:
                with open(r"{}\json\time.json".format(dirname), "w", encoding = "utf-8") as jcheck_time_set_write:
                    jcheck_time_set_loaded.append(timeint)
                    json.dump(jcheck_time_set_loaded, jcheck_time_set_write)
                    
                    
                alarm_set(int(day_splited[0]), int(day_splited[1]), int(day_splited[2]), int(time_splited[0]), int(time_splited[1]), timeint, self.bot)
            await interaction.response.send_message(f'已經設定完成！\n將會在{str(int(day_splited[0])).zfill(4)}/{str(int(day_splited[1])).zfill(2)}/{str(int(day_splited[2])).zfill(2)} {str(int(time_splited[0])).zfill(2)}:{str(int(time_splited[1])).zfill(2)}時提醒你{事情}')


    #todolist
    @app_commands.command(name = "todolist", description = "查看你設定了哪些todo")
    async def todolist(self, interaction: discord.Interaction):
        userid = interaction.user.id
        mytodolist = []
        find_todolist(mytodolist, userid)
        if str(mytodolist) == '[]':
            await interaction.response.send_message("你還沒有設定任何的todo喔!", ephemeral = True)
        else:
            mytodolist.sort(key = get_timeint)
            number = 1
            list = ""
            for data in mytodolist:
                year = data['date']['year']
                month = data['date']['month']
                day = data['date']['day']
                hour = data['date']['hour']
                minute = data['date']['minute']
                thing = data['thing']
                frequency = data['frequency_n']
                times = data['times']
                if len(thing) > 20:
                    thing = thing.replace(thing[20:],'...')

                list = list + (f'**{number}.** {str(year).zfill(4)}/{str(month).zfill(2)}/{str(day).zfill(2)} {str(hour).zfill(2)}:{str(minute).zfill(2)} {thing} 模式: {frequency} 剩餘次數: {times}\n')
                number += 1

            await interaction.response.send_message(list, ephemeral = True)

    #todoerase
    @app_commands.command(name = "todoerase", description = "刪除你不要的todo")
    @app_commands.describe(number = "要刪除的項目")
    async def todoerase(self, interaction: discord.Interaction, number: str):
        try:
            int(number)
        except:
            await interaction.response.send_message("請輸入一個數字! 正確格式為: /todoerase 數字", ephemeral = True)
        userid = interaction.user.id
        mytodolist = []
        find_todolist(mytodolist, userid)
        if str(mytodolist) == '[]':
            await interaction.response.send_message('你還沒有設定todo!', ephemeral = True)
        else:
            mytodolist.sort(key = get_timeint)
            for i, dictionary in enumerate(mytodolist):
                if int(i)+1 == int(number):
                    erasetodo = dictionary
                    break
                if int(i)+1 == len(mytodolist):
                    await interaction.response.send_message('你輸入的數字不正確!', ephemeral = True)
            with open(r"{}\json\todo.json".format(dirname), 'r') as eraset:
                jeraset = json.load(eraset)
                for idx, dictionary in enumerate(jeraset):
                    if erasetodo == dictionary:
                        jeraset.pop(idx)
                        with open(r"{}\json\todo.json".format(dirname), 'w') as jlist_w:
                            json.dump(jeraset, jlist_w)
            mytodolist.pop(int(number)-1)
            num = 1
            list = ""
            for data in mytodolist:
                year = data['date']['year']
                month = data['date']['month']
                day = data['date']['day']
                hour = data['date']['hour']
                minute = data['date']['minute']
                thing = data['thing']
                frequency = data['frequency_n']
                times = data['times']
                if len(thing) > 20:
                    thing = thing.replace(thing[20:],'...')

                list = list + (f'**{num}.** {str(year).zfill(4)}/{str(month).zfill(2)}/{str(day).zfill(2)} {str(hour).zfill(2)}:{str(minute).zfill(2)} {thing} 模式: {frequency} 剩餘次數: {times}\n')
                num += 1
            await interaction.response.send_message(f'已經成功幫你移除第{number}項啦!\n更新後的todolist:\n' + list, ephemeral = True)
    
async def setup(bot):
    await bot.add_cog(cmds(bot))