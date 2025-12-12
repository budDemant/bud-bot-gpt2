import os
import json
from datetime import datetime

# Ex: I only want messages from after May 30th, 2023
# Create a function that takes 2 dates to establish a range of accepted dates
# First, get all of the timestamps from messages.json keys and values!
def filter_date(year):
    pass


def main():
    with open('filter_date_test/messages.json', 'r') as f:
        messages = json.load(f)
    
    for msg in messages:
        timestamp = datetime.strptime(msg["Timestamp"], "%Y-%m-%d %H:%M:%S")
        print(timestamp)
        


if __name__ == "__main__":
    main()