import os
import json
from datetime import datetime

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


def main():
    with open('filter_date_test/messages.json', 'r') as f:
        messages = json.load(f)
    
    start_date = datetime(2023, 5, 30)
    end_date = datetime(2024, 1, 12)
   
    msg_date_filtered = filter_date_time(messages, start_date, end_date)
    
    with open("new_messages.json", "w") as f:
        json.dump(msg_date_filtered, f, indent=4)
    
    
    
        


if __name__ == "__main__":
    main()