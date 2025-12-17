import json
from datetime import datetime
import emoji
from pathlib import Path
import shutil
import re

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
#TODO: case sensitive and match whole word option (regex word boundaries on/off)
#TODO: concatenate phrases that aren't quite next to each other in a sentence (e.g. "I'm German")
def filter_words_phrases(messages, word_list):
    filtered = []
    for msg in messages:
        content_lower = msg["Contents"].lower()
        if not any(re.search(r'\b' + re.escape(word) + r'\b', content_lower) for word in word_list):
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


def filter_links(messages, exclude_links=False): # if True, excludes msg with links
    # Regex pattern to match URLs (http/https)
    url_pattern = re.compile(
        r'https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)',  # path
        re.IGNORECASE
    )
    
    filtered = []
    for msg in messages:
        content = msg["Contents"]
        has_link = bool(url_pattern.search(content))
        
        if has_link != exclude_links:
            filtered.append(msg)
    
    return filtered


'''Input a list of guild names and channel info dict, returns True if guild name matches'''
#TODO: What if a user only wants certain channels from a guild?
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
    
    #TODO: main entry point that combines every function.
    #TODO: I found a bot channel, how should I automatically filter these out??
    
    
    parent_folder = Path('Messages_guilds_dms_dates_emojis_links_words')
    
    for folder in parent_folder.iterdir():
        with open(f'{folder}/messages.json', 'r', encoding='utf-8') as f:
            messages = json.load(f)
    
        for msg in messages:
            # print(msg["Contents"])
            with open('final_output.txt', 'a', encoding='utf-8') as f:
                f.write(msg["Contents"] + '\n')
    
    
    # dm_list = [line.strip().lower() for line in open('filtered_dms.txt', 'r', encoding='utf-8')] 
    
    
    '''Links'''
    # parent_folder = Path('Messages')
    # all_filtered_messages = []
    
    # for folder in parent_folder.iterdir():
    #     if not folder.is_dir(): # skip index.json
    #         continue
        
    #     messages_path = folder / 'messages.json'
    #     if not messages_path.exists(): # skip folders that don't have messages.json
    #         continue
        
    #     with open(messages_path, 'r', encoding='utf-8') as f: 
    #         messages = json.load(f)
        
    #     # with links:
    #     # msg_with_links = filter_links(messages, exclude_links=False)
    #     # all_filtered_messages.extend(msg_with_links)
        
    #     # without links:
    #     msg_without_links = filter_links(messages, exclude_links=True)
    #     all_filtered_messages.extend(msg_without_links)
    
    # with open("new_messages.json", "w", encoding='utf-8') as f:
    #     json.dump(all_filtered_messages, f, indent=4, ensure_ascii=False) 
    '''Links'''
    # parent_folder = Path('Messages_guilds_dms_dates_emojis')
    # new_folder = Path('Messages_guilds_dms_dates_emojis_links')

    # for folder in parent_folder.iterdir():
    #     if not folder.is_dir():
    #         continue
    #     with open(f'{folder}/messages.json', 'r', encoding='utf-8') as f:
    #         messages = json.load(f)
    #     links_filtered = filter_links(messages, exclude_links=True)
    #     if links_filtered:  # only copy if there are messages left
    #         destination = new_folder / folder.name
    #         shutil.copytree(folder, destination)
    #         with open(f'{destination}/messages.json', "w", encoding='utf-8') as f:
    #             json.dump(links_filtered, f, indent=4, ensure_ascii=False)
        
    
    '''Searching for messages with key words'''
    # parent_folder = Path("Messages")
    
    # for folder in parent_folder.iterdir():
    #     if not folder.is_dir(): # skip index.json
    #         continue
        
    #     messages_path = folder / 'messages.json'
    #     if not messages_path.exists(): # not every folder in Messages has a messages.json
    #         continue
    #     with open(messages_path, 'r', encoding='utf-8') as f:
    #         msg_info = json.load(f)
    #     keyword = "home"
    #     for msg in msg_info:
    #         if keyword in msg["Contents"]:
    #             print(msg)
    
    '''Searching for deleted Group DMs'''
    #TODO: what about GROUP_DM name: null?
    # parent_folder = Path("Messages")
    
    # for folder in parent_folder.iterdir():
    #     if not folder.is_dir(): # skip index.json
    #         continue
        
    #     with open(f'{folder}/channel.json', 'r') as f:
    #         channel_info = json.load(f)
            
    #     type = channel_info.get("type")
    #     name = channel_info.get("name")
        
    #     if type == "GROUP_DM" and not name:
    #         print(folder)
    
    '''Searching for deleted DMs'''
    # parent_folder = Path("Messages")
    
    # for folder in parent_folder.iterdir():
    #     if not folder.is_dir(): # skip index.json
    #         continue
        
    #     with open(f'{folder}/channel.json', 'r') as f:
    #         channel_info = json.load(f)
        
    #     recipients = channel_info.get("recipients")
    #     if not recipients: # guilds don't have this key
    #         continue
        
    #     name = recipients[0]
    #     if "Deleted User" not in name:
    #         continue
        
    #     print(folder)
    
    '''Searching for particular folder'''
    # parent_folder = Path("Messages")
    
    # for folder in parent_folder.iterdir():
    #     if folder.is_dir():
    #         with open(f'{folder}/channel.json', 'r') as f:
    #             channel_info = json.load(f)
    #         name = channel_info.get("name")
    #         if name == "Book Club":
    #             print(folder)
    
    
    '''DMs'''
    #TODO: index_list has many repeats because of main entry point (doesn't affect functionality)
    # dm_list = [line.strip().lower() for line in open('filtered_dms.txt', 'r', encoding='utf-8')] 
    
    # parent_folder = Path("Messages")
    # new_folder = Path('Messages_guilds')
    
    # with open('index.json', 'r') as f:
    #     index_info = json.load(f)
    
    # for folder in parent_folder.iterdir():
    #     if folder.is_dir(): # for index.json
    #         with open(f'{folder}/channel.json', 'r') as f:
    #             channel_info = json.load(f)
            
    #         if filter_dms(channel_info, index_info, dm_list):
    #             destination = new_folder / folder
    #             shutil.copytree(folder, destination)
    
    
    '''Guilds/Servers''' 
    #TODO: server names shouldn't have to be exact (e.g. "movie type" vs "movie type server")
    # guild_list = [line.strip().lower() for line in open('filtered_guilds.txt', 'r', encoding='utf-8')] 
    
    # parent_folder = Path("Messages")
    # new_folder = Path('Messages_guilds')
    
    # for folder in parent_folder.iterdir():
    #     if not folder.is_dir():
    #         continue
    #     with open(f'{folder}/channel.json', 'r', encoding='utf-8') as f:
    #         channel_info = json.load(f)
        
    #     if filter_guilds(channel_info, guild_list):
    #         destination = new_folder / folder.name
    #         shutil.copytree(folder, destination)
    
    '''Emojis'''
    # parent_folder = Path('Messages_guilds_dms_dates')
    # new_folder = Path('Messages_guilds_dms_dates_emojis')
    
    
    # for folder in parent_folder.iterdir():
    #     if not folder.is_dir():
    #         continue
    #     with open(f'{folder}/messages.json', 'r', encoding='utf-8') as f:
    #        messages = json.load(f)
    #     emojis_filtered = filter_emojis(messages)
    #     if filter_emojis(messages):
    #         destination = new_folder / folder.name # .name because folder is the whole path, including Messages
    #         shutil.copytree(folder, destination)
    #         with open(f'{destination}/messages.json', "w", encoding='utf-8') as f:
    #             json.dump(emojis_filtered, f, indent=4, ensure_ascii=False) 
    
    '''Words/Phrases'''
    # word_list = [line.strip().lower() for line in open('filtered_words.txt', 'r', encoding='utf-8')] 
    # parent_folder = Path('Messages_dates_guilds')
    # all_filtered_messages = []
    
    # for folder in parent_folder.iterdir():
    #     if not folder.is_dir(): # skip index.json
    #         continue
        
    #     messages_path = folder / 'messages.json'
    #     if not messages_path.exists(): # skip folders that don't have messages.json
    #         continue
        
    #     with open(messages_path, 'r', encoding='utf-8') as f: 
    #         messages = json.load(f)
        
    #     msg_words_filtered = filter_words_phrases(messages, word_list)
    #     all_filtered_messages.extend(msg_words_filtered)
    
    # with open("new_messages.json", "w", encoding='utf-8') as f:
    #     json.dump(all_filtered_messages, f, indent=4, ensure_ascii=False)
    '''Word/Phrases'''
    # parent_folder = Path('Messages_guilds_dms_dates_emojis_links')
    # new_folder = Path('Messages_guilds_dms_dates_emojis_links_words')
    # word_list = [line.strip().lower() for line in open('filtered_words.txt', 'r', encoding='utf-8')] 
    # for folder in parent_folder.iterdir():
    #     if not folder.is_dir():
    #         continue
    #     with open(f'{folder}/messages.json', 'r', encoding='utf-8') as f:
    #         messages = json.load(f)
    #     words_filtered = filter_words_phrases(messages, word_list)
    #     if words_filtered:  # only copy if there are messages left
    #         destination = new_folder / folder.name
    #         shutil.copytree(folder, destination)
    #         with open(f'{destination}/messages.json', "w", encoding='utf-8') as f:
    #             json.dump(words_filtered, f, indent=4, ensure_ascii=False) 
    
    '''Datetime'''
    # parent_folder = Path('Messages_guilds_dms')
    # new_folder = Path('Messages_guilds_dms_dates')
    # start_date = datetime(2023, 5, 30) # Y/MM/DD
    # # end_date = datetime(2024, 1, 12)
    
    # for folder in parent_folder.iterdir():
    #     if not folder.is_dir():
    #         continue
    #     with open(f'{folder}/messages.json', 'r', encoding='utf-8') as f:
    #        messages = json.load(f)
    #     date_filtered = filter_date_time(messages, start_date)
    #     if filter_date_time(messages, start_date):
    #         destination = new_folder / folder.name # .name because folder is the whole path, including Messages
    #         shutil.copytree(folder, destination)
    #         with open(f'{destination}/messages.json', "w", encoding='utf-8') as f:
    #             json.dump(date_filtered, f, indent=4, ensure_ascii=False) 
            
          
        
    
    
    
if __name__ == "__main__":
    main()