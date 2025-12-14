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

# Include only messages from the text file of guild/server names
# So this function is looking inside each folder's channel.json and checking for the "guild: {name:}" key

# Might need to change this to account for DMs later...
'''Input a list of guild names, returns a new Messages folder called Messages_new, which contains folders
    of channel.json and messages.json that contain the right guild names'''
#TODO: maybe switch from os to Path from pathlib
def filter_guilds(guild_list):
    parent_folder = os.listdir("Messages_test")
    
    new_folder = "Messages_new"
    for folder in parent_folder:
        with open(f'Messages_test/{folder}/channel.json', 'r') as f:
            channel_info = json.load(f)
        guild_name = channel_info["guild"].get("name").lower()
        if guild_name in guild_list:
            combined_path = os.path.join(new_folder,folder)

    return combined_path

            
def main():
      
    guild_list = [line.strip().lower() for line in open('filtered_guilds.txt', 'r', encoding='utf-8')] 
        
    # parent_folder = list(Path("Messages_test").iterdir())
    parent_folder = Path("Messages_test")
    new_folder = Path('Messages_filtered')
    
    for folder in parent_folder.iterdir():
        with open(f'{folder}/channel.json', 'r') as f:
            channel_info = json.load(f)
        
        guild_name = channel_info["guild"].get("name").lower()
        
        if guild_name in guild_list:
            print(f"{guild_name} found in list")
            destination = new_folder / folder
            shutil.copytree(folder, destination)
    
    

    # Set the path to the parent folder
    folder = Path('Messages_test')
    copy_folder = Path('Messages_new')
    
    # Iterate through the child folders inside the parent folder
    for child_folder in folder.iterdir():
        print(child_folder.name)  # This will print just the name of the folder
            # Now you can access the files within each child folder
        destination = copy_folder / child_folder
        shutil.copytree(child_folder, destination)
        # for file in child_folder.iterdir():
        #     print(f"  {file.name}")
            
  
        

    '''pathlib example'''
    # parent = Path('parent_folder')
    # child = Path('child_folder')

    # # Copy files using shutil.copy2 for preserving metadata
    # for file_path in child.iterdir():
    #     if file_path.is_file():
    #         destination = parent / file_path.name
    #         shutil.copy2(file_path, destination)
    
    # Output: puts all contents of child_folder in parent_folder
    
    
    
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