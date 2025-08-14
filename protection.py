from config import GROUP_DM_ID, config
from utils import reset_group_name, reset_group_pfp

def setup_protection_handlers(bot):
    @bot.gateway.command
    def on_event(resp):
        if resp.raw.get('t') == 'CHANNEL_UPDATE':
            channel_data = resp.raw.get('d', {})
            channel_id = channel_data.get('id')
            
            if channel_id == GROUP_DM_ID:
                protected_name = config.get("nameprotect")
                protected_pfp = config.get("pfpprotect")
                
                if "name" in channel_data and protected_name:
                    current_name = channel_data["name"]
                    if current_name != protected_name:
                        reset_group_name(bot, protected_name)
                
                if "icon" in channel_data and protected_pfp:
                    current_icon = channel_data["icon"]
                    if current_icon != config.get("current_icon_hash"):
                        reset_group_pfp(bot, protected_pfp)