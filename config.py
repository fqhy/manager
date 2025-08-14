import json

CONFIG_FILE = "thangs.json"

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        config = {
            "user_token": "YOUR_USER_TOKEN",
            "group_dm_id": "YOUR_GROUP_DM_ID",
            "moderator_ids": [],
            "administrator_ids": [],
            "admin_user_id": "YOUR_OWNER_USER_ID",
            "banned_users": {},
            "warnings": {},
            "warn_amount": 3,
            "warn_punishment": {"type": "kick", "duration": "1d"},
            "rules": "1. Be respectful.\n2. No spamming.\n3. Follow Discord's ToS.",
            "nameprotect": None,
            "pfpprotect": None,
            "current_icon_hash": None,
            "lackmessage": "You do not have permission to do that.",
            "kickmessage": "User kicked.",
            "ban_message": "User has been banned.",
            "unban_message": "User has been unbanned.",
            "warn_message": "User {target_id} has been warned. ({warn_count}/{max_warns})",
            "warn_punishment_message": "User {target_id} has reached {max_warns} warnings and has been {punishment}.",
            "ringmessage": "User has been rung.",
            "ringallmessage": "All users have been rung.",
            "protectmessage": "Settings restored.",
            "admin_add_message": "Administrator added.",
            "admin_remove_message": "Administrator removed.",
            "admin_list_message": "Administrators:",
            "not_admin_message": "You are not authorized to manage administrators.",
            "not_owner_message": "Only the bot owner can perform this action.",
            "user_already_admin_message": "User is already an administrator.",
            "user_not_admin_message": "User is not an administrator."
        }
        save_config(config)

    default_keys = {
        "banned_users": {}, "warnings": {}, "warn_amount": 3,
        "warn_punishment": {"type": "kick", "duration": "1d"},
        "rules": "1. Be respectful.\n2. No spamming.",
        "ban_message": "User has been banned.",
        "unban_message": "User has been unbanned.",
        "warn_message": "User {target_id} has been warned. ({warn_count}/{max_warns})",
        "warn_punishment_message": "User {target_id} has reached {max_warns} warnings and has been {punishment}."
    }
    for key, value in default_keys.items():
        if key not in config:
            config[key] = value
            
    save_config(config)
    return config

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

config = load_config()

USER_TOKEN = config.get("user_token")
GROUP_DM_ID = config.get("group_dm_id")
MODERATOR_IDS = config.get("moderator_ids", [])
ADMINISTRATOR_IDS = config.get("administrator_ids", [])
ADMIN_USER_ID = config.get("admin_user_id")