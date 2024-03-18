from pyrogram import Client
from pyrogram.types import Message
from bot import mergeApp, LOGGER
from config import Config

async def metaEditor(c: Client, m: Message):
    try:
        if m.reply_to_message and m.reply_to_message.video:
            video_message = m.reply_to_message
            video_file_id = video_message.video.file_id
            caption = f"Custom Caption Here"
            
            # Update the metadata of the video file
            await c.edit_message_caption(
                chat_id=m.chat.id,
                message_id=video_message.message_id,
                caption=caption
            )
            
            LOGGER.info(f"Updated metadata for video: {video_file_id}")
        else:
            await m.reply_text("Please reply to a video file to update its metadata.")
    except Exception as e:
        LOGGER.error(f"Error in metaEditor: {str(e)}")

