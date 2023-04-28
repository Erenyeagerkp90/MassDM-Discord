import os
import random
import signal
import sys
import threading
import time
import discord
import discum
from termcolor import colored
import config


bot = discum.Client(token=sys.argv[1], log={"console": False, "file": False})
users = {}
total_users = []
total_dmed = 0


@bot.gateway.command
def on_event(resp):
    global users
    try:
        if resp.event.ready_supplemental:
            try:
                user = bot.gateway.session.user
                print(colored(f"Bot {sys.argv[2]}: Logged in as {user['username']}#{user['discriminator']}", "magenta"))
                thread = threading.Thread(target=send_dms, args=())
                thread.start()
                guilds = bot.gateway.session.guilds
                for guild_id, guild in guilds.items():
                    bot.gateway.request.lazyGuild(guild_id, {1: [[0, 99]]}, typing=True, threads=False, activities=True, members=[])
            except discord.LoginFailure:
                print(colored(f"Bot {sys.argv[2]}: Critical error! Token is probably dead", "magenta"))
                os.kill(os.getppid(), signal.SIGINT)
            except Exception as e:
                print(colored(f"Bot {sys.argv[2]}: Critical error! Failed to start", "magenta"))
                os.kill(os.getppid(), signal.SIGINT)
        if resp.event.message:
            m = resp.parsed.auto()
            if "guild_id" in list(m.keys()) and m['author']['id'] not in total_users:
                users[m['author']['id']] = {"username": m['author']['username'], "discriminator": m['author']['discriminator']}
                total_users.append(m['author']['id'])
                print(colored(f"Bot {sys.argv[2]}: {len(users)} IDs saved - Added {m['author']['username']}#{m['author']['discriminator']}", "cyan"))
        if resp.event.reaction_added:
            m = resp.parsed.auto()
            if "guild_id" in list(m.keys()) and m['member']['user']['id'] not in total_users:
                users[m['member']['user']['id']] = {"username": m['member']['user']['username'], "discriminator": m['member']['user']['discriminator']}
                total_users.append(m['member']['user']['id'])
                print(colored(f"Bot {sys.argv[2]}: {len(users)} IDs saved - Added {m['member']['user']['username']}#{m['member']['user']['discriminator']}", "cyan"))
    except discord.LoginFailure:
        print(colored(f"Bot {sys.argv[2]}: Critical error! Token is probably dead", "magenta"))
        os.kill(os.getppid(), signal.SIGINT)
    except Exception as e:
        pass


def send_dms():
    global users, total_dmed

    time.sleep(config.start_delay)

    while True:
        try:
            ids_saved = list(users.keys())
            if len(ids_saved) <= 0:
                print(colored(f"Bot {sys.argv[2]}: Waiting for active users...", "yellow"))
                time.sleep(10)
            else:
                user_id = random.choice(ids_saved)
                user = users[user_id]
                try:
                    if config.live:
                        dm = bot.createDM(user_id).json()['id']
                        bot.sendMessage(str(dm), message=config.dm_message)
                    total_dmed += 1
                    print(colored(f"Bot {sys.argv[2]}: {total_dmed} DMs sent - DMed {user['username']}#{user['discriminator']}", "green"))
                except discord.LoginFailure:
                    print(colored(f"Bot {sys.argv[2]}: Critical error! Token is probably dead", "magenta"))
                    os.kill(os.getppid(), signal.SIGINT)
                except Exception as e:
                    print(colored(f"Bot {sys.argv[2]}: DM failed - Target user might have their DMs enabled only for their friends or discord is asking for phone verification", "red"))
                del users[user_id]
                time.sleep(config.dm_delay)
        except discord.LoginFailure:
            print(colored(f"Bot {sys.argv[2]}: Critical error! Token is probably dead", "magenta"))
            os.kill(os.getppid(), signal.SIGINT)
        except Exception as e:
            pass


# Join up to 2 servers in case they were specified in the config file
if len(config.target_servers_invites) > 0:
    if len(config.target_servers_invites) <= 2:
        target_servers = config.target_servers_invites
    else:
        target_servers = config.target_servers_invites[:2]

    for server in target_servers:
        try:
            bot.joinGuild(server.split('/')[-1])
            print(colored(f"Bot {sys.argv[2]}: Joined {server}", "magenta"))
        except discord.LoginFailure:
            print(colored(f"Bot {sys.argv[2]}: Critical error! Token is probably dead", "magenta"))
            os.kill(os.getppid(), signal.SIGINT)
        except Exception as e:
            print(colored(f"Bot {sys.argv[2]}: Join {server} failed - Discord is probably asking for phone verification", "red"))


# Start DM bot
try:
    random.seed(int(sys.argv[2]))
    bot.gateway.run()
except discord.LoginFailure:
    print(colored(f"Bot {sys.argv[2]}: Critical error! Token is probably dead", "magenta"))
    os.kill(os.getppid(), signal.SIGINT)
except Exception as e:
    print(colored(f"Bot {sys.argv[2]}: Critical error! Token is probably dead", "magenta"))
    os.kill(os.getppid(), signal.SIGINT)





