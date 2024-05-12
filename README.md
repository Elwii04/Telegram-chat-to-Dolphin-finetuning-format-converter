# Telegram-chat-to-Dolphin-finetuning-format-converter
A python script that takes exported telegram chats in .json format, merges them and converts them into the cognitivecomputation dolphin training format for llm finetuning.

How to use:

1. Export all your Telegram Chats you want to use in json format
2. Make sure you have a Main folder with subfolders with the information of your chats containing the result.json file
3. Run the code and choose the main folder location
4. Enter your Telegram name, so the script knows what name to replace with gpt (The script will assume you are the gpt and your chatting partner is the human)
5. Enter a system prompt to use e.g. "You are a helpful robot"
