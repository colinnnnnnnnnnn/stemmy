from telegram import Update
from telegram.ext import ContextTypes

from bot.workflow import process_youtube_url
from shared.exceptions import DownloadError, JobFailedError


async def split_and_send(update: Update, context: ContextTypes):
    msg = update.message
    await msg.chat.send_message("Downloading...")
    try:
        output_dir = await process_youtube_url(msg.chat_id, msg.text)
    except DownloadError as e:
        await msg.chat.send_message(f"Download failed: {e}")
        return
    except JobFailedError as e:
        await msg.chat.send_message(f"Processing failed: {e}")
        return
    await msg.chat.send_message("Sending stems...")
    for stem_path in sorted(output_dir.iterdir()):
        if not stem_path.is_file():
            continue
        with open(stem_path, "rb") as audio_file:
            await msg.chat.send_audio(
                audio_file,
                filename=stem_path.name,
                caption=stem_path.stem,
            )
