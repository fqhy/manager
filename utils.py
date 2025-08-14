import requests
from datetime import datetime, timedelta
from config import config, save_config, USER_TOKEN, GROUP_DM_ID, MODERATOR_IDS, ADMINISTRATOR_IDS, ADMIN_USER_ID

def send_lackmessage(bot, channel_id):
    msg = config.get("lackmessage", "You do not have permission to do that.")
    if bot:
        bot.sendMessage(channel_id, msg)
    else:
        print(f"Error: bot object not provided to send_lackmessage. Message: {msg}")

def is_mod(author_id):
    return str(author_id) in MODERATOR_IDS

def is_admin(author_id):
    return str(author_id) in ADMINISTRATOR_IDS

def is_owner(author_id):
    return str(author_id) == ADMIN_USER_ID

def parse_duration(time_str):
    if not time_str or time_str.lower() == 'f':
        return None

    unit = time_str[-1].lower()
    try:
        value = int(time_str[:-1])
    except ValueError:
        return "Invalid time value."

    if unit == 's':
        return timedelta(seconds=value)
    elif unit == 'm':
        return timedelta(minutes=value)
    elif unit == 'h':
        return timedelta(hours=value)
    elif unit == 'd':
        return timedelta(days=value)
    elif unit == 'w':
        return timedelta(weeks=value)
    elif unit == 'y':
        return timedelta(days=value * 365)
    
    return "Invalid time unit. Use s, m, h, d, w, y."

def kick_user(bot, user_id, channel_id, reason=""):
    headers = {"Authorization": USER_TOKEN}
    r = requests.delete(f"https://discord.com/api/v9/channels/{channel_id}/recipients/{user_id}", headers=headers, timeout=5)
    if r.status_code == 204:
        if reason:
            bot.sendMessage(channel_id, reason)
        return True
    else:
        bot.sendMessage(channel_id, f"Failed to kick user {user_id}. Status: {r.status_code}")
        return False

def reset_group_name(bot, target_name):
    headers = {
        "Authorization": USER_TOKEN,
        "Content-Type": "application/json"
    }
    try:
        response = requests.patch(
            f"https://discord.com/api/v9/channels/{GROUP_DM_ID}",
            headers=headers,
            json={"name": target_name},
            timeout=5
        )
        if response.status_code == 200:
            protect_msg = config.get("protectmessage", "Group name restored.")
            bot.sendMessage(GROUP_DM_ID, protect_msg)
        else:
            print(f"Failed to reset name: {response.status_code}")
    except Exception as e:
        print(f"Name reset error: {e}")

def reset_group_pfp(bot, target_pfp):
    headers = {
        "Authorization": USER_TOKEN,
        "Content-Type": "application/json"
    }
    try:
        response = requests.patch(
            f"https://discord.com/api/v9/channels/{GROUP_DM_ID}",
            headers=headers,
            json={"icon": target_pfp},
            timeout=5
        )
        if response.status_code == 200:
            new_icon_hash = response.json().get("icon")
            config["current_icon_hash"] = new_icon_hash
            save_config(config)
            
            protect_msg = config.get("protectmessage", "Group icon restored.")
            bot.sendMessage(GROUP_DM_ID, protect_msg)
        else:
            print(f"Failed to reset PFP: {response.status_code}")
    except Exception as e:
        print(f"PFP reset error: {e}")