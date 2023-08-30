import re, sqlite3, os

def isAdmin(compare, LIST_OF_ADMINS):
    for entry in LIST_OF_ADMINS:
        if entry == compare:
            return True
        else:
            pass
    return False

def isUser(userID):
    conn = sqlite3.connect(os.path.realpath('./lib/data/database.db'))
    c = conn.cursor()
    c.execute("SELECT * from users WHERE userID =(?)", (userID,))
    userInfo = c.fetchone()
    c.execute("SELECT * from users WHERE userID =(?)", (userID,))
    exists = c.fetchone() is not None
    return exists

def check_time(update, duration):
    type = ''.join([i for i in duration if not i.isdigit()])
    #await ctx.send(type)
    print(type)
    type = type.strip("\n")
    if type == "m":
        time = re.sub("[^0-9]", "", duration)
        return int(time) * 60
    elif type == "h":
        time = re.sub("[^0-9]", "", duration)
        return int(time) * 3600
    elif type == "d":
        time = re.sub("[^0-9]", "", duration)
        return int(time) * 86400
    elif type == "w":
        time = re.sub("[^0-9]", "", duration)
        return int(time) * 604800
    elif type == "m":
        time = re.sub("[^0-9]", "", duration)
        return int(time) * 2592000
    elif type == "y":
        time = re.sub("[^0-9]", "", duration)
        return int(time) * 31536000
    else:
        update.message.reply_text("**{}** is an invalid time-key! **m/h/d/w/m/y** are valid!".format(type))
        return "Invalid"
