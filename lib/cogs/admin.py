import re, sqlite3, uuid, os, telegram, emoji
from discord_webhook import DiscordWebhook

from ..external import *
from ..data.keys import OWNERS, TOKEN


def createkey(update, context):
    if isAdmin(update.message.chat.id, OWNERS) == False: 
        update.message.reply_text("You are not allowed to use this command")
        user = update.message.from_user
        #webhook = DiscordWebhook(url=failed_admin, content=f"Someone's just tried accessing admin commands! username: {user['username']} | ID: {user['id']}").execute()
        return
    try:
        type = context.args[0]
        duration = context.args[1]
    except Exception:
        update.message.reply_text("Invalid format... /createkey <type> <duration>")
        return
    seconds = check_time(update, duration)
    if seconds == "Invalid": return
    
    conn = sqlite3.connect(os.path.realpath('./lib/data/database.db'))
    c = conn.cursor()
    key = str(uuid.uuid4())
    key=key[:14]

    c.execute("SELECT * FROM licenses")
    existing = c.fetchall()
    numbers = 0
    for license in existing:
        numbers += 1
    key = key + str(numbers)
    
    c.execute("INSERT INTO licenses VALUES (?,?,?,?)", (key, seconds, type, 1))

    update.message.reply_text(f"{key}, {seconds}, {type}, {1}")
    conn.commit()
    # Close conn
    conn.close()
    
def suspend(update, context):
    if isAdmin(update.message.chat.id, OWNERS) == False: 
        update.message.reply_text("You are not allowed to use this command")
        user = update.message.from_user
        #webhook = DiscordWebhook(url=failed_admin, content=f"Someone's just tried accessing admin commands! username: {user['username']} | ID: {user['id']}").execute()

    if isAdmin(update.message.chat.id, OWNERS) == True:
        try:
            username = context.args[0]
        except Exception:
            update.message.reply_text("Wrong Usage: /suspend <username>")
            return
        conn = sqlite3.connect(os.path.realpath('./lib/data/database.db'))
        c = conn.cursor()

        c.execute(f"SELECT * FROM users WHERE username =(?)", (username,))
        userinfo = c.fetchall()
        print(userinfo)
        
        c.execute(f"DELETE from users WHERE username =(?)", (username,))
        conn.commit()
        conn.close()
        try:
            updater = telegram.ext.Updater(TOKEN, use_context=True)
            updater.bot.sendMessage(chat_id=userinfo[0][2], text="Your subscription's been terminated by an administrator")
        except Exception as f:
            print(f)
            update.message.reply_text("There was an error notifying the user")
        update.message.reply_text("Successfully deleted their channel and sub!")
        
def unused(update, context):
    if isAdmin(update.message.chat.id, OWNERS) == False: 
        update.message.reply_text("You are not allowed to use this command")
        user = update.message.from_user
        #webhook = DiscordWebhook(url=failed_admin, content=f"Someone's just tried accessing admin commands! username: {user['username']} | ID: {user['id']}").execute()
    if isAdmin(update.message.chat.id, OWNERS) == True: 
        update.message.reply_text("Retrieving data...")

        conn = sqlite3.connect(os.path.realpath('./lib/data/database.db'))
        c = conn.cursor()
        c.execute("SELECT * FROM licenses")
        unformatted = c.fetchall()

        codes = ''
        #print(unformatted)
        for line in unformatted:
            if line[3] == 1:
                codes += line[0] + " | " +  str(int(line[1]) / 86400) + "d | " + line[2] + "\n"
            else:
                pass
        update.message.reply_text(codes)
        
def users(update, context):
    if isAdmin(update.message.chat.id, OWNERS) == False: 
        update.message.reply_text("You are not allowed to use this command")
        user = update.message.from_user
        #webhook = DiscordWebhook(url=failed_admin, content=f"Someone's just tried accessing admin commands! username: {user['username']} | ID: {user['id']}").execute()
    if isAdmin(update.message.chat.id, OWNERS) == True: 
        update.message.reply_text("Retrieving data...")
        
        conn = sqlite3.connect(os.path.realpath('./lib/data/database.db'))
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        unformatted = c.fetchall()

        users = ''
        c.execute("SELECT COUNT(*) FROM users")
        result = c.fetchone()[0]
        users += f"Number of users: {result}\n \n"
        
        for line in unformatted:
            users += str(line[1]) + " " +  str(line[0]) + " |" + line[3] + " / " + str(int(line[6])/86400) + " days" + "\n"
        update.message.reply_text(users)
        
def check(update, context):
    if isAdmin(update.message.chat.id, OWNERS) == False: 
        update.message.reply_text("You are not allowed to use this command")
        user = update.message.from_user
        #webhook = DiscordWebhook(url=failed_admin, content=f"Someone's just tried accessing admin commands! username: {user['username']} | ID: {user['id']}").execute()
        return
    
    conn = sqlite3.connect(os.path.realpath('./lib/data/database.db'))
    c = conn.cursor()
    try:
        username = context.args[0]
    except Exception:
        update.message.reply_text(emoji.emojize(f"""\u274C Invalid agrument... /check <username>"""))
        return
    
    c.execute("SELECT * from users WHERE username =(?)", (username,))
    userInfo = c.fetchone()
    c.execute("SELECT * from users WHERE username =(?)", (username,))
    exists = c.fetchone() is not None
    if exists == True:
        update.message.reply_text(emoji.emojize(f"""
:bust_in_silhouette: User Found | Chat ID: {userInfo[0]}
:hourglass_not_done: Start Date: {userInfo[4]}
:hourglass_not_done: Expiration date: {userInfo[5]}

:right_arrow: More Actions: /message /suspend
                                    """))
    else:
        update.message.reply_text(emoji.emojize(f"""\u274C User doesn't exist"""))
