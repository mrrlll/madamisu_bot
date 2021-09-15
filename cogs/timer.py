# -*- coding: utf-8 -*-
from typing import overload
from discord import activity, channel, Embed
from main import MyBot
from discord.ext import commands
import discord
import time



class timer(commands.Cog):

    # mycogクラスのコンストラクタ
    def __init__(self, bot):
        self.bot = bot

    # コマンドの例
    @commands.command()
    async def timer(self, ctx):
        # ShimpleTimerを丸パクリしたい
        pass



# Bot本体側からコグを読み込む際に呼び出される関数
def setup(bot):
    return bot.add_cog(timer(bot))
