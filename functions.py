import discord
intents = discord.Intents.all()
intents.members = True
import datetime
import json
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import calendar
import os
dirname = os.path.dirname(__file__)

def now_time():
    nowtime = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8)))
    nowtime_int = nowtime.year*100000000 + nowtime.month*1000000 + nowtime.day*10000 + nowtime.hour*100 + nowtime.minute
    return nowtime_int

def clear_over_time():
    with open(r"{}\json\todo.json".format(dirname), "r", encoding = "utf-8") as jcheck_over_time_read:
        jcheck_over_time_loaded = json.load(jcheck_over_time_read)
        nowtime_int = now_time()
        for i, dictionary in enumerate(jcheck_over_time_loaded):
            if dictionary['timeint'] <= nowtime_int:
                jcheck_over_time_loaded.pop(i)
    with open(r"{}\json\todo.json".format(dirname), "w", encoding = "utf-8") as jcheck_over_time_write:
        json.dump(jcheck_over_time_loaded, jcheck_over_time_write)

def find_mintime(file):
    mintime_int = 999999999999
    for i in file:
        year = int(i['date']['year'])
        month = int(i['date']['month'])
        day = int(i['date']['day'])
        hour = int(i['date']['hour'])
        minute = int(i['date']['minute'])
        timeint = i['timeint']
        todo_id = i['todo_id']
        if timeint <= mintime_int:
            mintimeint = timeint
            mintodo_id = todo_id
            minyear = year
            minmonth = month
            minday = day
            minhour = hour
            minminute = minute
            minthing = i['thing']
            mincid = i['channel_id']
            minuid = i['user']['user_id']
            minusername = i['user']['user_name']

    return minyear, minmonth, minday, minhour, minminute, minthing, mincid, minuid, minusername, mintimeint, mintodo_id

def get_timeint(list):
    return list.get('timeint')

def find_todolist(todolist, userid):
    with open(r"{}\json\todo.json".format(dirname), "r", encoding = "utf-8") as jfind_todolist_read:
        jfind_todolist_loaded = json.load(jfind_todolist_read)
        for dictionary in jfind_todolist_loaded:
            if int(dictionary['user']['user_id']) == int(userid):
                todolist.append(dictionary)

async def output_todo(timeint, bot):
    with open(r"{}\json\todo.json".format(dirname), "r", encoding = "utf-8") as joutput_todo_read:
        joutput_todo_loaded = json.load(joutput_todo_read)
        joutput_todo_loaded_clone = joutput_todo_loaded.copy()
        for dictionary in joutput_todo_loaded_clone:
            channel = bot.get_channel(dictionary['channel_id'])
            user = bot.get_user(dictionary['user']['user_id'])
            if dictionary['timeint'] == timeint:
                try:
                    await channel.send(f'<@{int(dictionary["user"]["user_id"])}> {dictionary["thing"]}')
                except:
                    await user.send(f'<@{int(dictionary["user"]["user_id"])}> {dictionary["thing"]}')
                dictionary["times"] -= 1
                for i, dict in enumerate(joutput_todo_loaded): 
                    if str(dict['todo_id']) == str(dictionary['todo_id']):
                        
                        if dict['frequency'] == "once per hour" and dict['times'] != 0:
                            dict['date']['hour'] += 1
                            dict['timeint'] = int(dict['date']['year'])*100000000 + int(dict['date']['month'])*1000000 + int(dict['date']['day'])*10000 + int(dict['date']['hour'])*100 + int(dict['date']['minute'])
                            
                        elif dict['frequency'] == "twice a day" and dict['times'] != 0:
                            dict['date']['hour'] += 12
                            if dict['date']['hour'] >= 24:
                                dict['date']['hour'] %= 24
                                dict['date']['day'] += 1
                            dict['timeint'] = int(dict['date']['year'])*100000000 + int(dict['date']['month'])*1000000 + int(dict['date']['day'])*10000 + int(dict['date']['hour'])*100 + int(dict['date']['minute'])
                            
                        elif dict['frequency'] == "once a day" and dict['times'] != 0:
                            dict['date']['day'] += 1
                            monthday = calendar.monthrange(dict['date']['year'], dict['date']['month'])[1]
                            if dict['date']['day'] > monthday:
                                dict['date']['day'] -= monthday
                                dict['date']['month'] += 1
                                if dict['date']['month'] > 12:
                                    dict['date']['month'] %= 12
                                    dict['date']['year'] += 1
                            dict['timeint'] = int(dict['date']['year'])*100000000 + int(dict['date']['month'])*1000000 + int(dict['date']['day'])*10000 + int(dict['date']['hour'])*100 + int(dict['date']['minute'])
                            
                        elif dict['frequency'] == "once a week" and dict['times'] != 0:
                            dict['date']['day'] += 7
                            monthday = calendar.monthrange(dict['date']['year'], dict['date']['month'])[1]
                            if dict['date']['day'] > monthday:
                                dict['date']['day'] -= monthday
                                dict['date']['month'] += 1
                                if dict['date']['month'] > 12:
                                    dict['date']['month'] %= 12
                                    dict['date']['year'] += 1
                            dict['timeint'] = int(dict['date']['year'])*100000000 + int(dict['date']['month'])*1000000 + int(dict['date']['day'])*10000 + int(dict['date']['hour'])*100 + int(dict['date']['minute'])
                                    
                        elif dict['frequency'] == "once a month" and dict['times'] != 0:
                            dict['date']['month'] += 1
                            if dict['date']['month'] > 12:
                                dict['date']['month'] %= 12
                                dict['date']['year'] += 1
                            dict['timeint'] = int(dict['date']['year'])*100000000 + int(dict['date']['month'])*1000000 + int(dict['date']['day'])*10000 + int(dict['date']['hour'])*100 + int(dict['date']['minute'])
                                
                        elif dict['frequency'] == "once a year" and dict['times'] != 0:
                            dict['date']['year'] += 1
                            dict['timeint'] = int(dict['date']['year'])*100000000 + int(dict['date']['month'])*1000000 + int(dict['date']['day'])*10000 + int(dict['date']['hour'])*100 + int(dict['date']['minute'])
                            
                        else:
                            joutput_todo_loaded.pop(i)
                            
        with open(r"{}\json\todo.json".format(dirname), "w", encoding = "utf-8") as joutput_todo_write:
            json.dump(joutput_todo_loaded, joutput_todo_write)
        with open(r"{}\json\todo.json".format(dirname), "r", encoding = "utf-8") as joutput_time_read:
            joutput_time_loaded = json.load(joutput_time_read)
            for i, dict in enumerate(joutput_time_loaded):
                if dict == timeint:
                    joutput_time_loaded.pop(i)
        with open(r"{}\json\time.json".format(dirname), "w", encoding = "utf-8") as joutput_time_write:
            json.dump(joutput_time_loaded, joutput_time_write)

def alarm_set(year, month, day, hour, minute, timeint, bot):
    alarm = AsyncIOScheduler(timezone = "Asia/Shanghai")
    alarm.add_job(output_todo, "cron", args = [timeint, bot], year = year, month = month, day = day, hour = hour, minute = minute)
    alarm.start()