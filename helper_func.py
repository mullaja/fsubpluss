#CodeXBotz #mrismanaziz

import asyncio
import base64
import re

from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant

from config import(
    ADMINS,
    FORCE_SUB_1,
    FORCE_SUB_2,
    FORCE_SUB_3,
    FORCE_SUB_4
)


async def _sub1(filter, client, update):
    if not FORCE_SUB_1:
        return True
    user_id = update.from_user.id
    if user_id in ADMINS:
        return True
    try:
        member = await client.get_chat_member(
            chat_id=FORCE_SUB_1, user_id=user_id
        )
    except UserNotParticipant:
        return False

    return member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]


async def _sub2(filter, client, update):
    if not FORCE_SUB_2:
        return True
    user_id = update.from_user.id
    if user_id in ADMINS:
        return True
    try:
        member = await client.get_chat_member(chat_id=FORCE_SUB_2, user_id=user_id)
    except UserNotParticipant:
        return False

    return member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]
    
async def _sub3(filter, client, update):
    if not FORCE_SUB_3:
        return True
    user_id = update.from_user.id
    if user_id in ADMINS:
        return True
    try:
        member = await client.get_chat_member(chat_id=FORCE_SUB_3, user_id=user_id)
    except UserNotParticipant:
        return False

    return member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]
    
async def _sub4(filter, client, update):
    if not FORCE_SUB_4:
        return True
    user_id = update.from_user.id
    if user_id in ADMINS:
        return True
    try:
        member = await client.get_chat_member(chat_id=FORCE_SUB_4, user_id=user_id)
    except UserNotParticipant:
        return False

    return member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]


async def is_subscribed(filter, client, update):
    if not FORCE_SUB_1:
        return True
    if not FORCE_SUB_2:
        return True
    if not FORCE_SUB_3:
        return True
    if not FORCE_SUB_4:
        return True
    user_id = update.from_user.id
    if user_id in ADMINS:
        return True
    try:
        member = await client.get_chat_member(chat_id=FORCE_SUB_4, user_id=user_id)
    except UserNotParticipant:
        return False
    try:
        member = await client.get_chat_member(chat_id=FORCE_SUB_3, user_id=user_id)
    except UserNotParticipant:
        return False
    try:
        member = await client.get_chat_member(chat_id=FORCE_SUB_2, user_id=user_id)
    except UserNotParticipant:
        return False
    try:
        member = await client.get_chat_member(
            chat_id=FORCE_SUB_1, user_id=user_id
        )
    except UserNotParticipant:
        return False

    return member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]


async def encode(string):
    string_bytes = string.encode("ascii")
    base64_bytes = base64.urlsafe_b64encode(string_bytes)
    base64_string = (base64_bytes.decode("ascii")).strip("=")
    return base64_string

async def decode(base64_string):
    base64_string = base64_string.strip("=") # links generated before this commit will be having = sign, hence striping them to handle padding errors.
    base64_bytes = (base64_string + "=" * (-len(base64_string) % 4)).encode("ascii")
    string_bytes = base64.urlsafe_b64decode(base64_bytes) 
    string = string_bytes.decode("ascii")
    return string


async def get_messages(client, message_ids):
    messages = []
    total_messages = 0
    while total_messages != len(message_ids):
        temb_ids = message_ids[total_messages : total_messages + 200]
        try:
            msgs = await client.get_messages(
                chat_id=client.db_channel.id, message_ids=temb_ids
            )
        except FloodWait as e:
            await asyncio.sleep(e.value)
            msgs = await client.get_messages(
                chat_id=client.db_channel.id, message_ids=temb_ids
            )
        except BaseException:
            pass
        total_messages += len(temb_ids)
        messages.extend(msgs)
    return messages


async def get_message_id(client, message):
    if (
        message.forward_from_chat
        and message.forward_from_chat.id == client.db_channel.id
    ):
        return message.forward_from_message_id
    elif message.forward_from_chat or message.forward_sender_name or not message.text:
        return 0
    else:
        pattern = "https://t.me/(?:c/)?(.*)/(\\d+)"
        matches = re.match(pattern, message.text)
        if not matches:
            return 0
        CHANNEL_DB = matches.group(1)
        msg_id = int(matches.group(2))
        if CHANNEL_DB.isdigit():
            if f"-100{CHANNEL_DB}" == str(client.db_channel.id):
                return msg_id
        elif CHANNEL_DB == client.db_channel.username:
            return msg_id


sub1 = filters.create(_sub1)
sub2 = filters.create(_sub2)
sub3 = filters.create(_sub3)
sub4 = filters.create(_sub4)
subs = filters.create(is_subscribed)
