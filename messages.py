import time
import requests
import base64
import mimetypes
from config import config, save_config
from utils import send_lackmessage, is_mod, is_admin, reset_group_pfp, reset_group_name

def handle_message_settings_command(bot, content, author_id, channel_id):
    if not bot:
        print("Error: bot object not provided to handle_message_settings_command.")
        return

    if content == "!config":
        if not is_mod(author_id): return send_lackmessage(bot, channel_id)

        warn_punishment = config.get("warn_punishment", {})
        punishment_type = warn_punishment.get("type", "kick")
        punishment_duration = f" ({warn_punishment.get('duration', 'N/A')})" if punishment_type == "ban" else ""

        config_msg_lines = [
            "Current Bot Configuration:",
            f"Name Protection: {config.get('nameprotect', 'None')}",
            f"Kick Message: {config.get('kickmessage', 'User kicked.')}",
            f"Ban Message: {config.get('ban_message', 'User has been banned.')}",
            f"Unban Message: {config.get('unban_message', 'User has been unbanned.')}",
            f"Permission Denied: {config.get('lackmessage', 'No permission.')}",
            f"Settings Restored: {config.get('protectmessage', 'Settings restored.')}",
            f"Ring Message: {config.get('ringmessage', 'User rung.')}",
            f"Ring-All Message: {config.get('ringallmessage', 'All rung.')}",
            f"Warn Amount: {config.get('warn_amount', 3)}",
            f"Warn Punishment: {punishment_type.title()}{punishment_duration}",
            f"Warn Message: {config.get('warn_message', 'No warn message set.')}",
            f"Warn Punishment Message: {config.get('warn_punishment_message', 'No warn punishment messsage set.')}",
            f"Rules (raw): {config.get('rules', 'No rules have been set.')}"
        ]
        bot.sendMessage(channel_id, "\n".join(config_msg_lines))
        return

    elif content.startswith("!kickmessage "):
        if not is_mod(author_id): return send_lackmessage(bot, channel_id)
        config["kickmessage"] = content[len("!kickmessage "):].strip()
        save_config(config)
        bot.sendMessage(channel_id, "Kick message updated.")

    elif content.startswith("!lackmessage "):
        if not is_mod(author_id): return send_lackmessage(bot, channel_id)
        config["lackmessage"] = content[len("!lackmessage "):].strip()
        save_config(config)
        bot.sendMessage(channel_id, "Permission error message updated.")

    elif content.startswith("!ringmessage "):
        if not is_admin(author_id): return send_lackmessage(bot, channel_id)
        config["ringmessage"] = content[len("!ringmessage "):].strip()
        save_config(config)
        bot.sendMessage(channel_id, "Ring message updated.")

    elif content.startswith("!ringallmessage "):
        if not is_admin(author_id): return send_lackmessage(bot, channel_id)
        config["ringallmessage"] = content[len("!ringallmessage "):].strip()
        save_config(config)
        bot.sendMessage(channel_id, "Ring-all message updated.")

    elif content.startswith("!protectmessage "):
        if not is_mod(author_id): return send_lackmessage(bot, channel_id)
        config["protectmessage"] = content[len("!protectmessage "):].strip()
        save_config(config)
        bot.sendMessage(channel_id, "Protection message updated.")

    elif content.startswith("!nameprotect "):
        if not is_mod(author_id): return send_lackmessage(bot, channel_id)
        name = content[len("!nameprotect "):].strip()
        config["nameprotect"] = name
        save_config(config)
        reset_group_name(bot, name)

    elif content.startswith("!pfpprotect "):
        if not is_mod(author_id): return send_lackmessage(bot, channel_id)
        url = content[len("!pfpprotect "):].strip()

        mime_type, _ = mimetypes.guess_type(url)
        if not mime_type or not mime_type.startswith("image/"):
            return bot.sendMessage(channel_id, "That does not look like a valid image link.")

        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code != 200:
                return bot.sendMessage(channel_id, f"Could not fetch image. HTTP {resp.status_code}")

            encoded = base64.b64encode(resp.content).decode("utf-8")
            data_uri = f"data:{mime_type};base64,{encoded}"

            config["pfpprotect"] = data_uri
            config["current_icon_hash"] = None
            save_config(config)
            
            reset_group_pfp(bot, data_uri)
            bot.sendMessage(channel_id, "Group icon protection updated and applied.")

        except Exception as e:
            return bot.sendMessage(channel_id, f"Failed to apply icon: {e}")
        
    elif content == "!help":
        help_text = """
General Commands
!help - Shows this help message.
!rules - View the group rules.
!ring @user - Ring a user (Aliases: !call, !вызвать).
!ringall - Ring all non-admin users.

Moderator Commands
!warn @user - Warn a user.
!config - View the bot's current configuration.
!kick @user - Kick a user.
!nameprotect <name> - Set protected group name.
!pfpprotect <image_url> - Set protected group icon.
!protectmessage <msg> - Set protection restoration message.
!kickmessage <msg> - Set legacy kick message.
!lackmessage <msg> - Set permission error message.
!ringmessage <msg> - Set single-user ring message.
!ringallmessage <msg> - Set ring-all message.

Administrator Commands
!ban @user <time> - Ban a user (time: 1m, 1h, 1d, 1w, f).
!unban @user - Unban a user.
!addmod @user - Add a moderator.
!removemod @user - Remove a moderator.
!modlist - List all moderators.
!editrules <rules> - Set group rules (use \\n for new lines).
!warnamount <num> - Set warnings before punishment.
!warnpunishment <kick|ban> [time] - Set punishment for warnings.
!banmessage <msg> - Set the message for when a user is banned/kicked.
!unbanmessage <msg> - Set the unban confirmation message.
!warnmessage <msg> -  Set the warn message.
!warnpunishmentmessage <msg> - Set the warn punishment message.

Owner Commands
!addadmin @user - Add an Administrator.
!removeadmin @user - Remove an Administrator.
!adminlist - List all Administrators.
"""
        bot.sendMessage(channel_id, help_text)