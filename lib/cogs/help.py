from ..external import *
from ..data.keys import *

def help(update, context):
    string = (f"""
Avaliable command prompts
    
▫️ /start \- Welcome message
▫️ /help \- shows this message
▫️ /contact \- contact information
▫️ /methods \- List all available methods
▫️ /buy \- Buy a subscription
▫️ /redeem \- Redeem a license key
▫️ /aboutme \- Check your subscription details

**Network**
▫️ /attack \- Attack a server
▫️ /ping \- Ping an IP address
▫️ /whois \- Lookup a website
▫️ /portscan \- Scan IP for open ports

    """)
    context.bot.send_message(chat_id=update.message.chat_id, text=string, parse_mode='MarkdownV2')


def methods(update, context):
    string =(f"""
```
APIs [ API1, API2,]
Status
API1:  🟢
API2:  🔴

API1 [Layer7]
   HTTPv1 | HTTP-RAW
   HTTPV2 | TLS-PRO
BROWSERV2 | HTTP-BYPASS

API2 [BOTNET] 
STD | SYN | ONEPACKET
TCP | ACK | BRAINFUCK
TCP | UDP |
```
    """)
    context.bot.send_message(chat_id=update.message.chat_id, text=string, parse_mode='MarkdownV2')

def help_admin(update, context):
    if isAdmin(update.message.chat.id, OWNERS) == False: 
        update.message.reply_text("You are not allowed to use this command")
        user = update.message.from_user
        #webhook = DiscordWebhook(url=failed_admin, content=f"Someone's just tried accessing admin commands! username: {user['username']} | ID: {user['id']}").execute()
    if isAdmin(update.message.chat.id, OWNERS) == True: 
        update.message.reply_text("""
! Admin Commands !                                  

▫️ /createkey - Create key <type> <duration>
▫️ /users - Shows all users
▫️ /suspend - Remove user license
▫️ /unused - List all unused license keys
▫️ /users - List all users 
▫️ /check - Lookup and moderate a user
""")

def buy(update, context):
    update.message.reply_text("https://t.me/INPUTNAMEHERE")


def contact(update, context):
    update.message.reply_text("https://t.me/INPUTNAMEHERE")
