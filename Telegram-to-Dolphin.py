import os
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import filedialog, Tk
import json

def move_and_rename_json_files(folder_path):
    # Create a new folder for renamed files
    new_folder_path = os.path.join(folder_path, 'renamed_json_files')
    os.makedirs(new_folder_path, exist_ok=True)

    # Iterate through each subfolder in the main folder
    for subdir, _, files in os.walk(folder_path):
        # Check if result.json exists in the current subfolder
        if 'result.json' in files:
            # Extract the name of the subfolder
            folder_name = os.path.basename(subdir)
            # Construct the new filename
            new_filename = os.path.join(new_folder_path, folder_name + '_result.json')
            # Copy and rename the result.json file
            shutil.copy2(os.path.join(subdir, 'result.json'), new_filename)
            print(f"Renamed and copied {os.path.join(subdir, 'result.json')} to {new_filename}")

def choose_folder():
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Choose the main folder")
    return folder_path

if __name__ == "__main__":
    print("Please select the main folder containing the subfolders.")
    folder_path = choose_folder()
    if folder_path:
        move_and_rename_json_files(folder_path)
        print("All JSON files have been renamed and copied to the renamed_json_files folder in the main folder.")














def process_telegram_chat(chat_data):
    """Processes a single Telegram chat JSON file.

    Args:
        chat_data (dict): The data of a Telegram chat in JSON format.

    Returns:
        dict: The modified chat data with "from": replaced and the specified name anonymized.
    """
    name_to_replace = input("Enter your telegram username to replace: ")
    
    for message in chat_data.get("messages", []):
        if "from" in message and message["from"] == name_to_replace:
            message["from"] = "gpt"
        else:
            message["from"] = "human"
    return chat_data




def merge_telegram_chats(folder_path, output_filename):
    """Merges all Telegram chat JSON files in a folder into a single file.

    Args:
        folder_path (str): The path to the folder containing the chat files.
        output_filename (str): The name of the output file to save the merged data.
    """
    all_chat_data = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                chat_data = json.load(f)
                processed_data = process_telegram_chat(chat_data)
                all_chat_data.append(processed_data)

    output_file_path = os.path.join(folder_path, output_filename)
    with open(output_file_path, "w", encoding="utf-8") as f:
        json.dump(all_chat_data, f, indent=4, ensure_ascii=False)
        print(f"Merged chat data saved to: {output_file_path}")

folder_path = folder_path + "/renamed_json_files"

if __name__ == "__main__":
    #print("Please select the folder containing the Telegram chat JSON files.")
    if folder_path:
        print("Merging chat data...")
        output_filename = "merged_chats.json"  # Default output filename
        merge_telegram_chats(folder_path, output_filename)
    else:
        print("No folder selected. Exiting.")










def convert_to_dolphin(json_path, output_path):
    """
    Converts a JSON file containing chat data to the dolphin format.

    Args:
      json_path: Path to the input JSON file.
      output_path: Path to write the converted JSON file.
    """
    # Ask user for system message
    system_message_value = input("Enter the system message to use as system prompt: ")
    system_message = {"from": "system", "value": system_message_value}

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    dolphin_data = []

    for chat in data:
        dolphin_chat = []
        # Add system message at the beginning of each chat
        dolphin_chat.append(system_message)

        current_speaker = None
        current_message = ""

        for message in chat["messages"]:
            # Skip the first message if GPT starts the conversation
            if message["from"] == "gpt" and current_speaker is None:
                continue

            # Check for speaker change
            if message["from"] != current_speaker:
                # Add previous conversation if messages exist
                if current_message:
                    dolphin_chat.append({
                        "from": current_speaker,
                        "value": current_message.strip()  # Strip leading/trailing spaces
                    })
                current_speaker = message["from"]
                current_message = ""

            # Add line break if consecutive messages from the same speaker
            if current_speaker == message["from"] and current_message:
                current_message += "\n"

            # Combine consecutive messages from the same speaker
            current_message += ''.join(str(item) for item in message["text"])

        # Add the last conversation if messages exist
        if current_message:
            dolphin_chat.append({
                "from": current_speaker,
                "value": current_message.strip()  # Strip leading/trailing spaces
            })

        # Add chat to dolphin data
        dolphin_data.append({"conversations": dolphin_chat})

    # Write the converted data to a new JSON file
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, chat in enumerate(dolphin_data):
            json.dump(chat, f, indent=4, ensure_ascii=False)
            if i < len(dolphin_data) - 1:  # Check if it's not the last chat
                f.write("\n")  # Add a newline between chats

# Example usage
json_path = folder_path + "/merged_chats.json"
output_path = folder_path + "/converted_dataset.json"
convert_to_dolphin(json_path, output_path)

print(f"Converted data written to: {output_path}")