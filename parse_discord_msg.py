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

#TODO: there's a deleted group dm that I want... what if someone wants a deleted guild?
def filter_dms(channel_info, index_info, dm_list):
    index_list = []
    for key, value in index_info.items():
        for line in dm_list:
           if line.strip().lower() in value.strip().lower(): # compare if usernames match
               index_list.append(key)
    id = channel_info.get("id")
    type = channel_info.get("type")
    if "DM" in type and id in index_list:
        return True
    
    

            
def main():
    
    '''DMs'''
    #TODO: index_list has many repeats because of main entry point (doesn't affect functionality)
    dm_list = [line.strip().lower() for line in open('filtered_dms.txt', 'r', encoding='utf-8')] 
    
    parent_folder = Path("dms_test")
    new_folder = Path('dms_filtered')
    
    with open('index.json', 'r') as f:
        index_info = json.load(f)
    
    for folder in parent_folder.iterdir():
        with open(f'{folder}/channel.json', 'r') as f:
            channel_info = json.load(f)
        
        if filter_dms(channel_info, index_info, dm_list):
            destination = new_folder / folder
            shutil.copytree(folder, destination)
    
    
    
    # with open('index.json', 'r') as f:
    #     index_info = json.load(f)
        
    # with open('dms_test/dm_1/channel.json', 'r') as f:
    #     channel_info = json.load(f)
        
    # channel_id = channel_info.get("id") # or channel_info["id"]
    
    # for id in index_info:
    #     if channel_id in id:
    #         print(id)
            
    
    # index_list = []
    # for key, value in index_info.items():
    #     for line in dm_list:
    #        if line.strip().lower() in value.strip().lower(): # compare if usernames match
    #            index_list.append(value)
    # print(index_list)
    
    
    # Now just copy every channel with those ids into a new messages folder
    
    '''Searching for particular folder'''
    # parent_folder = Path("Messages")
    
    # for folder in parent_folder.iterdir():
    #     if folder.is_dir():
    #         with open(f'{folder}/channel.json', 'r') as f:
    #             channel_info = json.load(f)
    #         name = channel_info.get("name")
    #         if name == "Book Club":
    #             print(folder)
    
    
    
    #TODO: handle index.json (it's a file, not folder)???
    '''Guilds/Servers'''  
    # guild_list = [line.strip().lower() for line in open('filtered_guilds.txt', 'r', encoding='utf-8')] 
    
    # parent_folder = Path("Messages_test")
    # new_folder = Path('Messages_filtered')
    
    # for folder in parent_folder.iterdir():
    #     with open(f'{folder}/channel.json', 'r') as f:
    #         channel_info = json.load(f)
        
    #     if filter_guilds(channel_info, guild_list):
    #         destination = new_folder / folder
    #         shutil.copytree(folder, destination)
    
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