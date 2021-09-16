from typing import overload
from discord import activity, channel, Embed
from main import MyBot
from discord.ext import commands
import discord


class calender(commands.cog):

    # mycogクラスのコンストラクタ
    def __init__(self, bot):
        self.bot = bot

    


    # Bot本体側からコグを読み込む際に呼び出される関数
def setup(bot):
    return bot.add_cog(calender(bot))
