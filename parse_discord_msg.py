import os
import json
from datetime import datetime
import emoji

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


def filter_words_phrases(messages, word_list):
    word_list = [line.strip().lower() for line in open('filtered_words.txt', 'r', encoding='utf-8')] 
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
            
            
def main():
    with open('filter_emoji_test/messages.json', 'r', encoding='utf-8') as f: # Windows uses default cp1252 encoding, which can't handle Unicode/special chars
        messages = json.load(f)
    
    
    msg_emojis_filtered = filter_emojis(messages)
    
    # word_list = open(f'filtered_words.txt', 'r')
    # msg_words_filtered = filter_words_phrases(messages, word_list)
    
    # start_date = datetime(2023, 5, 30)
    # end_date = datetime(2024, 1, 12)
    # msg_date_filtered = filter_date_time(messages, start_date, end_date)
    
    with open("new_messages.json", "w", encoding='utf-8') as f:
        json.dump(msg_emojis_filtered, f, indent=4, ensure_ascii=False)
    
    
    
if __name__ == "__main__":
    main()