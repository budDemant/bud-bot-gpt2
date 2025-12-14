import json
from datetime import datetime
import emoji
from pathlib import Path
import shutil

#TODO: use argparse with a custom type format for CLI to handle and convert date/time user input
def filter_date_time(messages, start_date=None, end_date=None):
    filtered = []
    for msg in messages:
        timestamp = datetime.strptime(msg["Timestamp"], "%Y-%m-%d %H:%M:%S")
    
        if start_date and timestamp < start_date:
            continue
        if end_date and timestamp > end_date:
            continue
        
        filtered.append(msg)
    return filtered

#TODO: includes words from list, should exclude (currently including for search purposes)
def filter_words_phrases(messages, word_list):
    filtered = []
    for msg in messages:
        if any(word in msg["Contents"].lower() for word in word_list):
            filtered.append(msg)
    
    return filtered


def filter_emojis(messages):
    filtered = []
    for msg in messages:
        clean_content = emoji.replace_emoji(msg["Contents"], replace='')
        if clean_content.strip():  # if there's text left
            msg_copy = msg.copy()
            msg_copy["Contents"] = clean_content.strip()
            filtered.append(msg_copy)
    return filtered


'''Input a list of guild names and channel info dict, returns True if guild name matches'''
def filter_guilds(channel_info, guild_list):
    guild = channel_info.get("guild")
    if not guild:
        return False  # No guild (DM or deleted server), so skip it
    
    guild_name = guild.get("name", "").lower()
    return guild_name in guild_list


            
def main():
    
    '''Guilds/Servers'''  
    guild_list = [line.strip().lower() for line in open('filtered_guilds.txt', 'r', encoding='utf-8')] 
    
    parent_folder = Path("Messages_test")
    new_folder = Path('Messages_filtered')
    
    for folder in parent_folder.iterdir():
        with open(f'{folder}/channel.json', 'r') as f:
            channel_info = json.load(f)
        
        if filter_guilds(channel_info, guild_list):
            destination = new_folder / folder
            shutil.copytree(folder, destination)
 
    
    '''Emojis'''
    # with open('filter_emoji_test/messages.json', 'r', encoding='utf-8') as f: # Windows uses default cp1252 encoding, which can't handle Unicode/special chars
    #     messages = json.load(f)
    
    # msg_emojis_filtered = filter_emojis(messages)
    
    # with open("new_messages.json", "w", encoding='utf-8') as f:
    #     json.dump(msg_emojis_filtered, f, indent=4, ensure_ascii=False)
    
    '''Words/Phrases'''
    # word_list = [line.strip().lower() for line in open('filtered_words.txt', 'r', encoding='utf-8')] 
    # msg_words_filtered = filter_words_phrases(messages, word_list)
    
    '''Datetime'''
    # start_date = datetime(2023, 5, 30)
    # end_date = datetime(2024, 1, 12)
    # msg_date_filtered = filter_date_time(messages, start_date, end_date)
    
    
    
    
    
if __name__ == "__main__":
    main()