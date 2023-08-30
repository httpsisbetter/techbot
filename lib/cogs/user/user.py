import telegram, emoji
from datetime import datetime, timedelta

from ...external import *
from ...data.keys import *

def subloop(context):
    conn = sqlite3.connect(os.path.realpath('./lib/data/database.db'))
    c = conn.cursor()
    c.execute("SELECT * from users")
    userlist = c.fetchall()
    
    for row in userlist:
        subEnd = row[5]
        channelID = row[2]
        userID = row[0]
        try:
            end = datetime.strptime(str(subEnd), "%Y-%m-%d %H:%M:%S.%f")
            currTime = datetime.now()
            #print(f"{end} | {currTime}")
            if end < currTime:
                                
                c.execute(f"DELETE from users WHERE userID ={userID}")
                conn.commit()

                updater = telegram.ext.Updater(TOKEN, use_context=True)
                updater.bot.sendMessage(chat_id=userID, text="Your Subscription has Ended :(")
                #webhook = DiscordWebhook(url=expired_users, content=f"A sub just expired for {userID}")
                #webhook.execute()
                print(f"A sub just expired for {userID}")
            else:
                pass
        except Exception as f:
            print(f)
    conn.close()    
    



def redeem(update, context):
    try:
        key = context.args[0]
    except Exception:
        update.message.reply_text(("\u274C Incorrect format, use /redeem <key>"))
        return

    user = update.message.from_user
    
    conn = sqlite3.connect(os.path.realpath('./lib/data/database.db'))
    c = conn.cursor()
    c.execute(f"SELECT * from licenses WHERE license = (?) AND used = 1", (key,))
    exists = c.fetchone() is not None
    c.execute(f"SELECT * from licenses WHERE license = (?)", (key,))
    row = c.fetchone()
    if exists == True:
        # Creation of room frontend
        c.execute(f"SELECT * FROM users WHERE userID={user['id']}",)
        user_exists = c.fetchone() is not None
        print(user_exists)
        if user_exists == False:
            username = user['username']
            bot_type = row[2]
            
            # Database backend
            c.execute(""" UPDATE licenses SET used = 0 WHERE license = (?)""", (key,))
            
            userID = user['id']
            channelID=user['id']
            subDuration = row[1]
            subStart = datetime.now()
            subEnd = subStart + timedelta(seconds=float(subDuration))
            c.execute(""" INSERT INTO users VALUES (?,?,?,?,?,?,?)""",(userID, username, channelID, bot_type, subStart, subEnd, subDuration) )
            update.message.reply_text(emoji.emojize(f"\u2705 Thank you for your purchase \n:hourglass_not_done: Expiration date: {subEnd}"))
            #webhook = DiscordWebhook(url=new_users, content=f"A new user just redeem a key! UserID: {userID} | Username: {username}")
            #webhook.execute()
            conn.commit()
            conn.close()
        #   Extend sub
        if user_exists == True:
            c.execute(""" UPDATE licenses SET used = 0 WHERE license = (?)""", (key,))
            
            c.execute(f"SELECT * FROM users WHERE userID={user['id']}",)
            user1 = c.fetchone()
            currEnd = user1[5]
            subDuration = row[1]
            
            currEnd1 = datetime.strptime((currEnd), "%Y-%m-%d %H:%M:%S.%f")
            end = currEnd1 + timedelta(seconds=float(subDuration))
            
            c.execute(' UPDATE users SET subscription_expiration = (?) WHERE userID = (?)', (end, user['id']))                    
            conn.commit()
            conn.close()
            
            update.message.reply_text(emoji.emojize(f"\u2705 Extended your subscription. \n:hourglass_not_done: Expiration date: {end}"))
            #webhook = DiscordWebhook(url=new_users, content=f"A new user just redeem a key! UserID: {userID} | Username: {username}")
            #webhook.execute()
            
    if exists == False:
        update.message.reply_text(("\u274C This key either does not exist or has been used before"))
        conn.close()

    conn.close()

    
        
def aboutme(update, context):
    conn = sqlite3.connect(os.path.realpath('./lib/data/database.db'))
    c = conn.cursor()
    user = update.message.from_user
    
    c.execute("SELECT * from users WHERE userID =(?)", (user['id'],))
    userInfo = c.fetchone()
    c.execute("SELECT * from users WHERE userID =(?)", (user['id'],))
    exists = c.fetchone() is not None
    
    if exists == True:
        update.message.reply_text(emoji.emojize(f"""
:bust_in_silhouette: User Found!
:hourglass_not_done: Expiration date: {userInfo[5]}
:right_arrow: Buy more -> /buy
                                  """))
        #await ctx.send("User found!")
    if exists == False:
        update.message.reply_text(emoji.emojize("\u274C You don't have a subscription -> /buy"))
