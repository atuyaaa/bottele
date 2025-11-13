from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import yt_dlp
import os

BOT_TOKEN = os.getenv("8375261004:AAFT7U-nP4n5tQLIiX-u79xBRr7m3JTvwho")
CHANNEL_ID = os.getenv("alewanabot")  # contoh: @namachannelkamu
DOWNLOAD_PATH = "downloads"
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

async def download_song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{DOWNLOAD_PATH}/%(title)s.%(ext)s',
            'noplaylist': True,
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}" if "youtube.com" not in query else query, download=True)
            if 'entries' in info:
                info = info['entries'][0]

        title = info.get('title', 'lagu')
        filename = f"{DOWNLOAD_PATH}/{title}.mp3"

        # Kirim langsung ke channel
        if CHANNEL_ID:
            await context.bot.send_audio(chat_id=CHANNEL_ID, audio=open(filename, 'rb'), title=title)
        else:
            await update.message.reply_audio(audio=open(filename, 'rb'), title=title)

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"❌ Terjadi kesalahan: {e}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_song))

if __name__ == "__main__":
    print("🚀 Bot aktif di Railway")
    app.run_polling()
