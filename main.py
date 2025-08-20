import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import yt_dlp

BOT_TOKEN =BOT_TOKEN = "8085158426:AAFfOGbqgzi7U9knLKM3eP8kLDZGwq8FBjg"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to Snapzilla Bot!\nSend me a video link from YouTube, Instagram, or Facebook to download it.")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    ydl_opts = {
        'outtmpl': 'downloaded_video.%(ext)s',
        'format': 'best',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, 'rb') as f:
            await update.message.reply_video(f, caption="✅ Here is your downloaded video!")
        os.remove(filename)
    except Exception as e:
        await update.message.reply_text("❌ Failed to download video. Please try again with a valid link.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

app.run_polling()
