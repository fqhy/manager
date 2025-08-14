import requests
from config import USER_TOKEN, GROUP_DM_ID, config
from utils import is_admin

def handle_ring_command(bot, m, author_id, channel_id):
    if not bot:
        print("Error: bot object not provided to handle_ring_command.")
        return

    if not m["mentions"]:
        bot.sendMessage(channel_id, "No user mentioned.")
        return
    target_id = m["mentions"][0]["id"]

    if is_admin(target_id):
        bot.sendMessage(channel_id, "You cannot ring an administrator.")
        return

    headers = {
        "Authorization": USER_TOKEN,
        "Content-Type": "application/json"
    }
    try:
        r = requests.post(
            f"https://discord.com/api/v9/channels/{GROUP_DM_ID}/call/ring",
            headers=headers,
            json={"recipients": [target_id]},
            timeout=5
        )
        if r.status_code == 204:
            msg = config.get("ringmessage", "User has been rung.")
            if msg:
                bot.sendMessage(channel_id, msg)
        else:
            bot.sendMessage(channel_id, f"Failed to ring (Error {r.status_code})")
    except Exception as e:
        bot.sendMessage(channel_id, f"Error ringing user: {str(e)}")

def handle_ringall_command(bot, channel_id):
    if not bot:
        print("Error: bot object not provided to handle_ringall_command.")
        return

    headers = {
        "Authorization": USER_TOKEN
    }
    try:
        group_info = requests.get(
            f"https://discord.com/api/v9/channels/{GROUP_DM_ID}",
            headers=headers,
            timeout=5
        )
        if group_info.status_code == 200:
            group_json = group_info.json()
            recipient_ids = [user["id"] for user in group_json.get("recipients", []) if not is_admin(user["id"])]
            if not recipient_ids:
                bot.sendMessage(channel_id, "No non-administrator users to ring.")
                return

            ring_headers = {
                "Authorization": USER_TOKEN,
                "Content-Type": "application/json"
            }
            r = requests.post(
                f"https://discord.com/api/v9/channels/{GROUP_DM_ID}/call/ring",
                headers=ring_headers,
                json={"recipients": recipient_ids},
                timeout=10
            )
            if r.status_code == 204:
                msg = config.get("ringallmessage", "All users have been rung.")
                if msg:
                    bot.sendMessage(channel_id, msg)
            else:
                bot.sendMessage(channel_id, f"Failed to ring all (Error {r.status_code})")
        else:
            bot.sendMessage(channel_id, f"Couldn't fetch group members (Error {group_info.status_code})")
    except Exception as e:
        bot.sendMessage(channel_id, f"Error ringing all: {str(e)}")