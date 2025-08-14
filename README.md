# Mananger

A versatile Python bot for managing and moderating Discord group DMs, built using the `discum` library. It provides a range of features from moderation and role management to group protection and customizable messages.

---

## Features

-   **Role-Based Permissions:** Three-tiered permission system (Moderator, Administrator, Owner).
-   **Moderation Suite:** Commands for kicking, banning, unbanning, and warning users.
-   **Group Protection:** Automatically reverts changes to the group DM's name and icon.
-   **Customization:** Almost all bot responses and settings can be configured via a JSON file.
-   **Auto-Moderation:** Automatically kicks banned users if they rejoin the group.
-   **Utility Commands:** Includes commands for "ringing" users to get their attention.

---

## Prerequisites

-   Python 3.6+
-   `discum` library
-   `requests` library

---

## Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/fqhy/manager.git
    cd manager
    ```

2.  **Install dependencies:**
    ```bash
    pip install discum requests
    ```

3.  **Configure the bot:**
    -   Open `thangs.json` and fill in the required values. See the [Configuration](#configuration) section below for details.

4.  **Run the bot:**
    ```bash
    python bot.py
    ```

---

## Configuration

All bot settings are managed in the `thangs.json` file.

-   `user_token`: **(Required)** Your Discord user token.
-   `group_dm_id`: **(Required)** The ID of the group DM you want the bot to operate in.
-   `admin_user_id`: **(Required)** The Discord user ID of the person who owns and controls the bot.
-   `moderator_ids`: A list of user IDs for moderators.
-   `administrator_ids`: A list of user IDs for administrators.
-   All other keys are for customizing bot messages and behavior. You can edit their values as needed.

**Example `thangs.json`:**
```json
{
  "user_token": "YOUR_DISCORD_USER_TOKEN",
  "group_dm_id": "YOUR_GROUP_DM_ID",
  "admin_user_id": "YOUR_OWN_USER_ID",
  "moderator_ids": [],
  "administrator_ids": [],
  "banned_users": {},
  "warnings": {},
  "warn_amount": 3,
  "warn_punishment": {
    "type": "kick",
    "duration": "1d"
  },
  "rules": "1. Be respectful.\\n2. No spamming.",
  "nameprotect": null,
  "pfpprotect": null,
  "current_icon_hash": null,
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
