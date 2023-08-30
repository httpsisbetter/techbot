import telegram.ext
from functools import wraps
import os, json, requests, time

from lib.data.keys import TOKEN
from lib.cogs.help import *
from lib.cogs.admin import *
from lib.cogs.user.user import *
from lib.cogs.user.utilites import *


def start(update, context):
    update.message.reply_text("Welcome to QueerTech, use /help to start")


def main():
    
    updater = telegram.ext.Updater(TOKEN, use_context=True)
    disp = updater.dispatcher

    disp.add_handler(telegram.ext.CommandHandler("start", start))
    disp.add_handler(telegram.ext.CommandHandler("help", help))
    disp.add_handler(telegram.ext.CommandHandler("contact", contact))
    disp.add_handler(telegram.ext.CommandHandler("attack", attack, pass_args=True))
    disp.add_handler(telegram.ext.CommandHandler("methods", methods))
    disp.add_handler(telegram.ext.CommandHandler("ping", ping, pass_args=True))
    disp.add_handler(telegram.ext.CommandHandler("whois", lookup, pass_args=True))
    disp.add_handler(telegram.ext.CommandHandler("portscan", portscan, pass_args=True))
    disp.add_handler(telegram.ext.CommandHandler("buy", buy))
    disp.add_handler(telegram.ext.CommandHandler("redeem", redeem, pass_args=True))
    disp.add_handler(telegram.ext.CommandHandler("aboutme", aboutme))
    

    disp.add_handler(telegram.ext.CommandHandler("help_admin", help_admin))
    disp.add_handler(telegram.ext.CommandHandler("createkey", createkey, pass_args=True))
    disp.add_handler(telegram.ext.CommandHandler("suspend", suspend, pass_args=True))
    disp.add_handler(telegram.ext.CommandHandler("unused", unused))
    disp.add_handler(telegram.ext.CommandHandler("users", users))
    disp.add_handler(telegram.ext.CommandHandler("check", check, pass_args=True))

    job_queue = updater.job_queue

    job_queue.run_repeating(subloop, interval=9, first=5)

    updater.start_polling()
    updater.idle()
    
if __name__ == '__main__':
    main()
