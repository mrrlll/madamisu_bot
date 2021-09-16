# -*- coding: utf-8 -*-
from typing import overload
from discord import activity, channel, Embed
from main import MyBot
from discord.ext import commands
import discord

# コグとして用いるクラスを定義
class mycog2(commands.Cog):

    # mycogクラスのコンストラクタ
    def __init__(self, bot):
        self.bot = bot

    # コマンドの例
    @commands.command()
    async def ping(self, ctx):
        await ctx.reply('pong!')

# Bot本体側からコグを読み込む際に呼び出される関数
def setup(bot):
    return bot.add_cog(mycog2(bot))
