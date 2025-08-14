from config import config, save_config, MODERATOR_IDS, ADMINISTRATOR_IDS
from utils import send_lackmessage, is_admin, is_owner

def handle_role_commands(bot, content, m, author_id, channel_id):
    if not bot:
        print("Error: bot object not provided to handle_role_commands.")
        return

    if content.startswith("!addmod "):
        if not is_admin(author_id): return send_lackmessage(bot, channel_id)
        if m["mentions"]:
            new_mod = m["mentions"][0]["id"]
            if new_mod not in config["moderator_ids"]:
                config["moderator_ids"].append(new_mod)
                save_config(config)
                bot.sendMessage(channel_id, "Moderator added.")
            else:
                bot.sendMessage(channel_id, "User is already a moderator.")
        else:
            bot.sendMessage(channel_id, "Mention a user to add as moderator.")

    elif content.startswith("!removemod "):
        if not is_admin(author_id): return send_lackmessage(bot, channel_id)
        if m["mentions"]:
            remove_id = m["mentions"][0]["id"]
            if remove_id in config["moderator_ids"]:
                config["moderator_ids"].remove(remove_id)
                save_config(config)
                bot.sendMessage(channel_id, "Moderator removed.")
            else:
                bot.sendMessage(channel_id, "User is not a moderator.")
        else:
            bot.sendMessage(channel_id, "Mention a user to remove as moderator.")

    elif content == "!modlist":
        if not is_admin(author_id): return send_lackmessage(bot, channel_id)
        mods = config.get("moderator_ids", [])
        if mods:
            mentions = "\n".join([f"<@{mid}>" for mid in mods])
            bot.sendMessage(channel_id, f"Moderators:\n{mentions}")
        else:
            bot.sendMessage(channel_id, "No moderators set.")

    elif content.startswith("!addadmin "):
        if not is_owner(author_id):
            bot.sendMessage(channel_id, config.get("not_owner_message", "Only the bot owner can perform this action."))
            return
        if m["mentions"]:
            new_admin = m["mentions"][0]["id"]
            if new_admin not in config["administrator_ids"]:
                config["administrator_ids"].append(new_admin)
                save_config(config)
                bot.sendMessage(channel_id, config.get("admin_add_message", "Administrator added."))
            else:
                bot.sendMessage(channel_id, config.get("user_already_admin_message", "User is already an administrator."))
        else:
            bot.sendMessage(channel_id, "Mention a user to add as administrator.")

    elif content.startswith("!removeadmin "):
        if not is_owner(author_id):
            bot.sendMessage(channel_id, config.get("not_owner_message", "Only the bot owner can perform this action."))
            return
        if m["mentions"]:
            remove_id = m["mentions"][0]["id"]
            if remove_id in config["administrator_ids"]:
                config["administrator_ids"].remove(remove_id)
                save_config(config)
                bot.sendMessage(channel_id, config.get("admin_remove_message", "Administrator removed."))
            else:
                bot.sendMessage(channel_id, config.get("user_not_admin_message", "User is not an administrator."))
        else:
            bot.sendMessage(channel_id, "Mention a user to remove as administrator.")

    elif content == "!adminlist":
        admins = config.get("administrator_ids", [])
        if admins:
            mentions = "\n".join([f"<@{aid}>" for aid in admins])
            bot.sendMessage(channel_id, f"{config.get('admin_list_message', 'Administrators:')}\n{mentions}")
        else:
            bot.sendMessage(channel_id, "No administrators set.")