import discum
from config import USER_TOKEN, GROUP_DM_ID
from moderation import handle_moderation_commands, setup_auto_kick_on_join
from ring import handle_ring_command, handle_ringall_command
from messages import handle_message_settings_command
from protection import setup_protection_handlers
from roles import handle_role_commands

bot = discum.Client(token=USER_TOKEN, log=False)

@bot.gateway.command
def on_message(resp):
    if resp.event.ready_supplemental:
        print("Bot is ready.")

    if resp.event.message:
        m = resp.parsed.auto()
        author_id = m["author"]["id"]
        content = m["content"]
        channel_id = m["channel_id"]

        if channel_id == GROUP_DM_ID:
            if content.startswith(("!kick", "!ban", "!unban", "!warn", "!rules", "!editrules", "!banmessage", "!unbanmessage", "!warnamount", "!warnpunishment", "!warnmessage", "!warnpunishmentmessage")):
                handle_moderation_commands(bot, m, author_id, channel_id, content)

            elif content.startswith(("!ring ", "!call ", "!вызвать ")):
                handle_ring_command(bot, m, author_id, channel_id)

            elif content.startswith("!ringall"):
                handle_ringall_command(bot, channel_id)

            elif content == "!help" or content == "!config":
                handle_message_settings_command(bot, content, author_id, channel_id)

            elif content.startswith((
                "!kickmessage ", "!lackmessage ", "!ringmessage ",
                "!ringallmessage ", "!nameprotect ", "!pfpprotect ",
                "!protectmessage "
            )):
                handle_message_settings_command(bot, content, author_id, channel_id)

            elif content.startswith((
                "!addmod ", "!removemod ", "!modlist",
                "!addadmin ", "!removeadmin ", "!adminlist"
            )):
                handle_role_commands(bot, content, m, author_id, channel_id)

setup_protection_handlers(bot)
setup_auto_kick_on_join(bot)

bot.gateway.run(auto_reconnect=True)