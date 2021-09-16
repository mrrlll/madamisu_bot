# -*- coding: utf-8 -*-
from discord import activity
from discord.ext import commands
from discord.ext import tasks
import traceback
import discord
import os

# 読み込むコグ
INITIAL_EXTENSIONS = [
    'cogs.cogs',
    'cogs.cogs2',
    'cogs.timer',
    'cogs.calender',
]

# botを動かすためのトークン
token = os.getcwd() + "/cogs/file/token.txt"
with open(token, 'r', encoding = 'UTF-8') as f:
    TOKEN = f.read()

# クラスの定義。 ClientのサブクラスであるBotクラスを継承
class MyBot(commands.Bot):

    # MyBotのコンストラクタ
    def __init__(self, command_prefix):
        # スーパークラスのコンストラクタに値を渡して実行
        super().__init__(command_prefix)

        # INITIAL_COGSに格納されている名前からコグを読み込む
        for cog in INITIAL_EXTENSIONS:
            try:
                self.load_extension(cog)
            except Exception:
                traceback.print_exc()

    # bot準備完了時のイベント
    async def on_ready(self):
        print('-----')
        print(self.user.name)
        print(self.user.id)
        print('-----')
        await self.change_presence(activity = discord.Game(name = "マーダーミステリー", type = 1))


if __name__ == '__main__':
    bot = MyBot(command_prefix = '!')
    bot.run(TOKEN)
