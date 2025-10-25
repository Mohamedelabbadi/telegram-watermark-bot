import os
import json
from telegram import Update, Bot
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackContext
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

TOKEN = "8040811918:AAEC0IvDy_AigmfC36ZHu617D9V38YFdajU"
MAIN_CHANNEL = "@smimosas"
bot = Bot(token=TOKEN)

CHANNELS_FILE = "channels.json"
VIDEOS_FILE = "videos.json"

# ========================
# Helpers
# ========================

def load_json(file):
    if not os.path.exists(file):
        return []
    with open(file, "r") as f:
        return json.load(f)

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

def add_watermark(input_file, output_file, text):
    video = VideoFileClip(input_file)
    watermark = TextClip(
        text,
        fontsize=60,
        color='white',
        font='Arial-Bold'
    ).set_duration(video.duration).set_position(("center", "bottom"))
    
    final = CompositeVideoClip([video, watermark])
    final.write_videofile(output_file, codec="libx264", audio_codec="aac", fps=video.fps)

# ========================
# Main video functions
# ========================

def send_video_to_channel(video_path, channel_name):
    output_name = f"temp_{channel_name.replace('@','')}.mp4"
    add_watermark(video_path, output_name, channel_name)
    bot.send_video(
        chat_id=channel_name,
        video=open(output_name, 'rb'),
        caption=f"🎥 Shared by {channel_name}"
    )
    os.remove(output_name)

def handle_new_video(update: Update, context: CallbackContext):
    message = update.channel_post
    if not message or not message.video:
        return

    if message.chat.username != MAIN_CHANNEL.replace("@", ""):
        return

    video_id = message.video.file_id
    videos = load_json(VIDEOS_FILE)

    if video_id in videos:
        return  # already processed

    print("📥 New video detected in main channel!")
    new_file = bot.get_file(video_id)
    new_file.download("video.mp4")

    # Add to video history
    videos.append(video_id)
    save_json(VIDEOS_FILE, videos)

    # Send to all channels
    channels = load_json(CHANNELS_FILE)
    for ch in channels:
        send_video_to_channel("video.mp4", ch)
    os.remove("video.mp4")
    print("✅ Sent to all channels!")

# ========================
# Channel management
# ========================

def add_channel(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text("Usage: /addchannel @channel_username")
        return
    
    new_channel = context.args[0]
    channels = load_json(CHANNELS_FILE)

    if new_channel in channels:
        update.message.reply_text(f"{new_channel} already exists — will only receive new videos ✅")
        return

    channels.append(new_channel)
    save_json(CHANNELS_FILE, channels)
    update.message.reply_text(f"✅ Added new channel: {new_channel}\nSending all previous videos...")

    # Send all old videos to the new channel
    videos = load_json(VIDEOS_FILE)
    for vid_id in videos:
        file = bot.get_file(vid_id)
        file.download("temp_video.mp4")
        send_video_to_channel("temp_video.mp4", new_channel)
        os.remove("temp_video.mp4")

# ========================
# Main function
# ========================

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.video & Filters.chat(username=MAIN_CHANNEL.replace("@", "")), handle_new_video))
    dp.add_handler(CommandHandler("addchannel", add_channel))

    print("🚀 Bot started — watching main channel for new videos...")
    updater.start_polling()
    updater.idle()

if name == "__main__":
    main()