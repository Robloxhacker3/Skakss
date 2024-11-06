import requests
import time
import json
import base64
import discord
import random
import os
from discord.ext import commands

f = open('premium.txt', 'r')
premiums = f.read().splitlines()
f.close()

def last_used(user_id):
    f = open('log.txt', 'r')
    text = f.read().splitlines()
    f.close()

    d = {}
    for line in text:
        if ':' in line:
            d[line[0:line.find(':')]] = line[line.find(':') + 1: len(line)]

    if str(user_id) in d:
        return d[str(user_id)]
    else:
        return 0

def update_dict(user_id):
    f = open('log.txt', 'r')
    text = f.read().splitlines()
    d = {}
    for line in text:
        if ':' in line:
            d[line[0:line.find(':')]] = line[line.find(':') + 1: len(line)]
    d[str(user_id)] = str(int(time.time()))

    new_text_file = ''
    keys = d.keys()
    for key in keys:
        new_text_file = new_text_file + str(key) + ':' + str(d[key]) + '\n'
    new_text_file = new_text_file[0:len(new_text_file) - 1]

    f.close()
    f = open('log.txt', 'w')
    f.write(new_text_file)
    f.close()

def bypass_link(url):
    first_link = 'https://publisher.linkvertise.com/api/v1/redirect/link/static/'

    second_link = 'https://publisher.linkvertise.com/api/v1/redirect/link/insert/linkvertise/path/here/target?serial=base64encodedjson'
    second_link_front = second_link[0:second_link.find('insert/linkvertise')]
    second_link_back = second_link[second_link.find('/target?serial'):second_link.find('base64encodedjson')]

    new_link = "None"

    try:
        input_link = url
        link = ''
        if '.com/' in input_link:
            if '?o=' in input_link:
                link = input_link[input_link.find('.com/') + 5:input_link.find('?o=')]
            else:
                link = input_link[input_link.find('.com/') + 5:len(input_link)]
        if '.net/' in input_link:
            if '?o=' in input_link:
                link = input_link[input_link.find('.net/') + 5:input_link.find('?o=')]
            else:
                link = input_link[input_link.find('.net/') + 5:len(input_link)]

        r = requests.get(first_link + link, timeout=2)
        text = r.text
        link_id = text[text.find('"id":') + 5:text.find(',"url":')]

        new_json = {"timestamp": int(time.time()), "random": "6548307", "link_id": int(link_id)}

        s = json.dumps(new_json)
        json_converted = base64.b64encode(s.encode('utf-8'))
        json_converted = str(json_converted)
        json_converted = json_converted[2:len(json_converted) - 1]

        r = requests.get(second_link_front + link + second_link_back + json_converted, timeout=4)
        converted_json = json.loads(r.text)
        new_link = converted_json['data']['target']
    except:
        filler_value = "filler_value"

    new_dict = {
        "new_link": new_link,
    }
    return new_dict

def get_data():
    f = open('data.json', 'r')
    data = json.load(f)
    f.close()

    return data

def add_message(message, bypass_time):
    data = get_data()
    message_ids = []
    for temp in data['messages']:
        message_ids.append(temp['message_id'])

    message_id = message.id
    time_created = message.created_at

    if message_id not in message_ids:
        new_json = {
            "message_id": message.id,
            "time_created": time_created,
            "bypass_time": bypass_time
        }
        data['messages'].append(new_json)

        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)

# Setup the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def bypass(ctx, url: str):
    """
    Command to handle bypassing the linkvertise.
    """
    result = bypass_link(url)
    await ctx.send(f"Bypass Result: {result['new_link']}")

# Run the bot with your token
bot.run('YOUR_TOKEN_HERE')
