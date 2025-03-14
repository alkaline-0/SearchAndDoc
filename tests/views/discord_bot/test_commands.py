from ctypes import util

import discord
import discord.ext.commands as commands
import discord.ext.test as dpytest
import pytest
import pytest_asyncio

import models.channel


@pytest.mark.asyncio
async def test_throw_error_channel_does_not_exist(bot):
  await dpytest.message(content="!document_with_LLM wrong_channel test_keyword", channel=dpytest.get_config().channels[0], member=dpytest.get_config().members[0])
  res = dpytest.get_message().content
  assert res == "Channel does not exist."


@pytest.mark.asyncio
async def test_messages_get_populated(bot):
  _channel = channel=dpytest.get_config().channels[1]
  await dpytest.message(content="hello", channel=_channel, member=dpytest.get_config().members[0])
  await dpytest.message(content="test", channel=_channel, member=dpytest.get_config().members[1])
  await dpytest.message("!document_with_LLM general test_keyword")
  
  channel = models.channel.Channel(_channel)
  msgs = await channel.get_channel_messages()
  assert len(msgs) == 2
  
