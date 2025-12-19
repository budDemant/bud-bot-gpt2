import json

json_file = 'guild_settings.json'

# Read file
def load_guild_settings():
    try:
        with open(json_file, 'r') as f:
            content = f.read()
            if not content.strip():  # if file is empty, needs to be in JSON format
                return {}
            return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}  # for missing/invalid file

# Write to file
def save_guild_settings(settings):
    with open(json_file, 'w') as f:
        json.dump(settings, f, indent=2)

# Update a specific guild's settings
def update_guild_channel(guild_id, channel_id):
    settings = load_guild_settings()
    
    guild_id_str = str(guild_id) # JSON keys must be strings
    
    settings[guild_id_str] = { # overwrite or add new entry
        "channel_id": channel_id,
        "enabled": True
    }
    
    save_guild_settings(settings)

# Check if ask command is allowed in channel
def is_channel_allowed(guild_id, channel_id):
    settings = load_guild_settings()
    guild_id_str = str(guild_id)
    
    if guild_id_str not in settings: # if no restriction in this guild, allow everywhere
        return True
    
    guild_settings = settings[guild_id_str]
    
    # if disabled or no channel set, allow everywhere
    if not guild_settings.get("enabled") or guild_settings.get("channel_id") is None:
        return True
    
    return guild_settings["channel_id"] == channel_id # check if current channel matches

#TODO: disable channel (unsetchannel)