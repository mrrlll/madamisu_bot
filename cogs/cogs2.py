# -*- coding: utf-8 -*-
from typing import overload
from discord import activity, channel, Embed
from main import MyBot
from discord.ext import commands
import discord
import datetime

# コグとして用いるクラスを定義
class mycog2(commands.Cog):

    # mycogクラスのコンストラクタ
    def __init__(self, bot):
        self.bot = bot
    
    # コマンド使用のログ
    def log(ctx):
        log = ['----------------------------', datetime.datetime.now().strftime('%Y/%m/%d  %H:%M:%S'), ctx.author.id, ctx.author.name, ctx.message.content]
        
        print(log[0])
        print(log[1])
        print(log[2])
        print(log[3])
        print(log[4])
        print(log[0])

        with open('./log.txt', 'a', encoding = 'utf-8') as f:
            for data in log:
                f.write("%s\n" % data)
            

    # コマンドの例
    @commands.command()
    async def ping(self, ctx):
        mycog2.log(ctx)
        await ctx.reply('pong!')

    

# Bot本体側からコグを読み込む際に呼び出される関数
def setup(bot):
    return bot.add_cog(mycog2(bot))
