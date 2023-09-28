# Dependencies
import telebot as tb
import subprocess
import shutil
import threading
import random
import os

# Your API ID and API hash from the Telegram's API website
# get credentials data
bot_token = '6492106506:AAGC1AVB_hwjZijNNxWYsE6XZcvAcY_6h84'

# Create an object bot
bot = tb.TeleBot(bot_token, parse_mode='MarkdownV2')

# Lock to prevent multiple threads from interfering with each other
lock = threading.Lock()

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, """*Welcome to BotJadMusicRemover 👋🙋‍♂️
The place where you can remove the music from your favorite songs*

📍 *About*
BotJadMusicRemover takes your song video then it reply with the video without the music, only vocals

🛑🛑🛑PLZ, use /ready command if you ready🛑🛑🛑
""")

@bot.message_handler(commands=['ready'])
def send_message_if_ready(message):
    bot.send_message(message.chat.id, text='Oh, Happy thats you are ready😊')
    bot.send_message(message.chat.id, text='Now, give me your song video 😀')

@bot.message_handler(content_types=['video'])
def process_video(message):
    try:
        bot.send_message(message.chat.id, "I process your video, Wait me")
        # Create an output directory to save the user videos 
        if not os.path.exists("/content/outputs"):
          os.system("mkdir outputs")
          
        # Receive the video from the user
        video = message.video
        file_info = bot.get_file(video.file_id)

        # Define a specific video file path without periods
        video_path = file_info.file_path

        # Download the video and save it to the specified file path
        downloaded_file = bot.download_file(video_path)
        # Check if the file has been fully downloaded
        if len(downloaded_file) == file_info.file_size:
            # Save the video file
            # with open("output.mp4", 'wb') as new_file:
            #     new_file.write(downloaded_file)
                # bot.send_video(message.chat.id, open("output.mp4", 'rb'))
        
            # Generate a random name video
            chars = "abcdefghijklmnopqrstuvwxyz"
            CHARS = chars.upper()
            nums = "123456789"
            all_chars = chars + CHARS + nums
            random_name = "".join(random.sample(all_chars, 5))
            # print(random_name)
            with open(f"outputs/{random_name}.mp4", "wb") as video_file:
                video_file.write(downloaded_file)
        
        # Spare Plan
        # subprocess.run(['spleeter', 'separate', '-o', '.', '-c', 'mp3', "output.mp4"])
        # bot.send_audio(message.chat.id, audio=open("output/vocals.mp3", 'rb'))
        
        # Main Plan 
        command = ["demucs", "-s", "vocals", f"outputs/{random_name}.mp4", "vocals.mp4"]
        subprocess.run(command)
        bot.send_audio(message.chat.id, audio=open(f"/content/separated/htdemucs/{random_name}/vocals.wav", 'rb'))

        # Remove the generated folder by the model
        shutil.rmtree("./separated")

    except Exception as e:
        # Escape the period in the error message to avoid the Telegram entity parsing issue
        error_message = "An error occurred: " + str(e).replace('.', '\\.')
        bot.reply_to(message, error_message)

bot.infinity_polling()