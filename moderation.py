import time
from datetime import datetime
from config import config, save_config
from utils import send_lackmessage, is_mod, is_admin, is_owner, parse_duration, kick_user

def handle_kick_command(bot, m, author_id, channel_id):
    if not is_admin(author_id) and not is_mod(author_id):
        send_lackmessage(bot, channel_id)
        return

    if not m["mentions"]:
        bot.sendMessage(channel_id, "Usage: !kick @user")
        return

    target_id = m["mentions"][0]["id"]

    if is_admin(target_id) and not is_admin(author_id):
        bot.sendMessage(channel_id, "You cannot kick an administrator.")
        return

    kick_message = config.get("kickmessage", "User kicked.")
    kick_user(bot, target_id, channel_id, kick_message)

def handle_ban_command(bot, m, author_id, channel_id, content):
    if not is_admin(author_id): return send_lackmessage(bot, channel_id)

    parts = content.split()
    if not m["mentions"] or len(parts) < 3:
        bot.sendMessage(channel_id, "Usage: !ban @user <time> (e.g., !ban @user 1d)")
        return

    target_id = m["mentions"][0]["id"]
    if is_admin(target_id) or is_owner(target_id):
        bot.sendMessage(channel_id, "You cannot ban an administrator or the owner.")
        return

    duration_str = parts[2]
    duration = parse_duration(duration_str)
    if isinstance(duration, str):
        bot.sendMessage(channel_id, f"Error: {duration}")
        return

    expires_at = (datetime.utcnow() + duration) if duration else None

    config["banned_users"][target_id] = {
        "expires_at": expires_at.isoformat() if expires_at else "permanent",
        "banned_by": author_id
    }
    save_config(config)

    expiry_msg = f"until {expires_at.isoformat()}" if expires_at else "permanently"
        
    bot.sendMessage(channel_id, f"User {target_id} has been banned {expiry_msg}.")
    kick_user(bot, target_id, channel_id, config.get("ban_message", "You have been banned from this group."))

def handle_unban_command(bot, m, author_id, channel_id, content):
    if not is_admin(author_id): return send_lackmessage(bot, channel_id)

    parts = content.split()
    target_id = None

    if m["mentions"]:
        target_id = m["mentions"][0]["id"]
    elif len(parts) > 1 and parts[1].isdigit():
        target_id = parts[1]
    else:
        bot.sendMessage(channel_id, "Usage: !unban <@user|userID>")
        return

    if target_id in config["banned_users"]:
        del config["banned_users"][target_id]
        save_config(config)
        bot.sendMessage(channel_id, f"User {target_id} has been unbanned.")
    else:
        bot.sendMessage(channel_id, "This user is not currently banned.")

def handle_warn_command(bot, m, author_id, channel_id):
    if not is_mod(author_id): return send_lackmessage(bot, channel_id)
    if not m["mentions"]: return bot.sendMessage(channel_id, "Usage: !warn @user")

    target_id = m["mentions"][0]["id"]
    if is_admin(target_id) or is_owner(target_id):
        bot.sendMessage(channel_id, "You cannot warn an administrator or the owner.")
        return

    warnings = config["warnings"].setdefault(target_id, {"count": 0, "warned_by": []})
    warnings["count"] += 1
    if author_id not in warnings["warned_by"]:
        warnings["warned_by"].append(author_id)

    warn_limit = config.get("warn_amount", 3)
    
    warn_msg_template = config.get("warn_message", "User {target_id} has been warned. ({warn_count}/{max_warns})")
    bot.sendMessage(channel_id, warn_msg_template.format(target_id=target_id, warn_count=warnings['count'], max_warns=warn_limit))

    if warnings["count"] >= warn_limit:
        punishment = config.get("warn_punishment", {"type": "kick"})
        punishment_type = punishment.get("type", "kick")
        duration_str = punishment.get("duration", "N/A")
        
        punishment_action_str = "kicked"
        del config["warnings"][target_id]

        if punishment_type == "kick":
            kick_user(bot, target_id, channel_id)
        elif punishment_type == "ban":
            duration = parse_duration(duration_str)
            expiry_msg = f"for {duration_str}" if duration else "permanently"
            punishment_action_str = f"banned {expiry_msg}"
            
            if isinstance(duration, str):
                expires_at = None
            else:
                 expires_at = (datetime.utcnow() + duration) if duration else None

            config["banned_users"][target_id] = {
                "expires_at": expires_at.isoformat() if expires_at else "permanent",
                "banned_by": bot.gateway.session.user['id']
            }
            kick_user(bot, target_id, channel_id)
        
        punishment_msg_template = config.get("warn_punishment_message", "User {target_id} has reached {max_warns} warnings and has been {punishment}.")
        bot.sendMessage(channel_id, punishment_msg_template.format(target_id=target_id, max_warns=warn_limit, punishment=punishment_action_str))

    save_config(config)

def handle_rules_command(bot, channel_id):
    rules = config.get("rules", "No rules have been set. Use !editrules to set them.").replace("\\n", "\n")
    bot.sendMessage(channel_id, f"{rules}")

def handle_editrules_command(bot, author_id, channel_id, content):
    if not is_admin(author_id): return send_lackmessage(bot, channel_id)
    new_rules = content[len("!editrules "):].strip()
    if not new_rules:
        bot.sendMessage(channel_id, "Usage: !editrules <your rules here...> (use \\n for new lines)")
        return

    config["rules"] = new_rules
    save_config(config)
    bot.sendMessage(channel_id, "Rules have been updated.")
    handle_rules_command(bot, channel_id)

def handle_moderation_settings(bot, author_id, channel_id, content):
    if not is_admin(author_id): return send_lackmessage(bot, channel_id)
    command, _, value = content.partition(' ')
    value = value.strip()

    if command == "!banmessage":
        if not value: return bot.sendMessage(channel_id, f"Current ban message: {config.get('ban_message')}")
        config["ban_message"] = value
        bot.sendMessage(channel_id, "Ban message updated.")
    elif command == "!unbanmessage":
        if not value: return bot.sendMessage(channel_id, f"Current unban message: {config.get('unban_message')}")
        config["unban_message"] = value
        bot.sendMessage(channel_id, "Unban message updated.")
    elif command == "!warnmessage":
        if not value: return bot.sendMessage(channel_id, f"Current warn message: {config.get('warn_message')}")
        config["warn_message"] = value
        bot.sendMessage(channel_id, "Warn message updated.")
    elif command == "!warnpunishmentmessage":
        if not value: return bot.sendMessage(channel_id, f"Current warn punishment message: {config.get('warn_punishment_message')}")
        config["warn_punishment_message"] = value
        bot.sendMessage(channel_id, "Warn punishment message updated.")
    elif command == "!warnamount":
        try:
            amount = int(value)
            if amount < 1: return bot.sendMessage(channel_id, "Amount must be at least 1.")
            config["warn_amount"] = amount
            bot.sendMessage(channel_id, f"Warning amount set to {amount}.")
        except ValueError:
            return bot.sendMessage(channel_id, "Usage: !warnamount <number>")
    elif command == "!warnpunishment":
        parts = value.split()
        punishment_type = parts[0].lower() if parts else ""
        if punishment_type not in ["kick", "ban"]:
            return bot.sendMessage(channel_id, "Usage: !warnpunishment <kick|ban> [duration]")
        if punishment_type == "ban":
            duration = parts[1] if len(parts) > 1 else "f"
            config["warn_punishment"] = {"type": "ban", "duration": duration}
            bot.sendMessage(channel_id, f"Warning punishment set to a {duration} ban.")
        else:
            config["warn_punishment"] = {"type": "kick"}
            bot.sendMessage(channel_id, "Warning punishment set to kick.")
    else:
        return bot.sendMessage(channel_id, "Unknown moderation setting.")

    save_config(config)

def handle_moderation_commands(bot, m, author_id, channel_id, content):
    if content.startswith("!kick "):
        handle_kick_command(bot, m, author_id, channel_id)
    elif content.startswith("!ban "):
        handle_ban_command(bot, m, author_id, channel_id, content)
    elif content.startswith("!unban "):
        handle_unban_command(bot, m, author_id, channel_id, content)
    elif content.startswith("!warn "):
        handle_warn_command(bot, m, author_id, channel_id)
    elif content == "!rules":
        handle_rules_command(bot, channel_id)
    elif content.startswith("!editrules "):
        handle_editrules_command(bot, author_id, channel_id, content)
    elif content.startswith(("!banmessage", "!unbanmessage", "!warnamount", "!warnpunishment", "!warnmessage", "!warnpunishmentmessage")):
        handle_moderation_settings(bot, author_id, channel_id, content)

def setup_auto_kick_on_join(bot):
    @bot.gateway.command
    def on_event(resp):
        if resp.raw.get('t') == 'CHANNEL_RECIPIENT_ADD':
            data = resp.raw.get('d', {})
            channel_id = data.get('channel_id')
            user = data.get('user', {})
            user_id = user.get('id')

            if str(user_id) in config.get("banned_users", {}):
                ban_info = config["banned_users"][str(user_id)]
                expires_at_str = ban_info.get("expires_at")

                is_expired = False
                if expires_at_str and expires_at_str != "permanent":
                    if datetime.utcnow() > datetime.fromisoformat(expires_at_str):
                        is_expired = True

                if is_expired:
                    del config["banned_users"][str(user_id)]
                    save_config(config)
                else:
                    time.sleep(1)
                    reason = config.get("ban_message", "You are banned from this group.")
                    kick_user(bot, user_id, channel_id, reason)