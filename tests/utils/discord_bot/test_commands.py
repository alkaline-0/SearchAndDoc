import asyncio
from ctypes import util
import os
import discord
import discord.ext.commands as commands
import pytest
import pytest_asyncio
import discord.ext.test as dpytest

@pytest.mark.asyncio
async def test_throw_error_channel_does_not_exist(bot):
  msg  = await dpytest.message(content="!document_with_LLM wrong_channel test_keyword", channel=dpytest.get_config().channels[0])
  res = dpytest.get_message().content
  assert res == "Channel does not exist."


@pytest.mark.asyncio
async def test_get_messages_for_existing_channel(bot):
  await dpytest.message(content="hello", channel=dpytest.get_config().channels[1])
  await dpytest.message(content="test", channel=dpytest.get_config().channels[1])
  await dpytest.message("!document_with_LLM general test_keyword")
  
