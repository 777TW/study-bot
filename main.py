import discord
from discord.ext import commands
intents = discord.Intents.all()
intents.members = True
import json
import os
import asyncio
import datetime
from functions import clear_over_time, alarm_set
dirname = os.path.dirname(__file__)

with open(r"{}\json\settings.json".format(dirname), 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

bot = commands.Bot(command_prefix='#$%^&',
                   help_command=None,
                   intents=intents,
                   application_id="1115903981164703765")


@bot.event
async def on_ready():
    print(">> Bot is online <<")
    time = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8))).replace(tzinfo = None)
    date = "2024/07/12 00:00:00"
    datestr = datetime.datetime.strptime(date, "%Y/%m/%d %H:%M:%S")
    duration = datestr - time
    game = discord.Game(f'分科倒數{duration.days + 1}天')
    await bot.change_presence(status=discord.Status.online, activity=game)

    clear_over_time()
    with open(r"{}\json\time.json".format(dirname), "w", encoding="utf-8") as jtime_clear_write:
        json.dump([], jtime_clear_write)

    with open(r"{}\json\todo.json".format(dirname), "r", encoding="utf-8") as j_on_ready_todo_read:
        j_on_ready_todo_loaded = json.load(j_on_ready_todo_read)
    for time in j_on_ready_todo_loaded:
        with open(r"{}\json\time.json".format(dirname), "r",
                  encoding="utf-8") as jtime_record_read:
            jtime_record_loaded = json.load(jtime_record_read)
            ct = 0
            if str(jtime_record_loaded) != "[]":
                for i in jtime_record_loaded:
                    if i != time['timeint']:
                        ct += 1
            if ct == len(jtime_record_loaded):
                with open(r"{}\json\time.json".format(dirname), "w",
                          encoding="utf-8") as jtime_record_write:
                    jtime_record_loaded.append(time['timeint'])
                    json.dump(jtime_record_loaded, jtime_record_write)
                    alarm_set(time['date']['year'], time['date']['month'],
                              time['date']['day'], time['date']['hour'],
                              time['date']['minute'], time['timeint'], bot)


async def loads():
    for filename in os.listdir('./categories'):
        if filename.endswith('.py'):
            await bot.load_extension(f'categories.{filename[:-3]}')


async def main():
    await loads()
    if __name__ == "__main__":
        await bot.start(jdata['token'])

asyncio.run(main())