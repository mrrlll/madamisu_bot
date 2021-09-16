# -*- coding: utf-8 -*-
from typing import overload
from discord import activity, channel, Embed
from main import MyBot
from discord.ext import commands
import discord
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


class calendar(commands.Cog):

    # mycogクラスのコンストラクタ
    def __init__(self, bot):
        self.bot = bot

    # コマンドの例
    @commands.command()
    async def calendar(self, ctx):
        path = "C:/bin/chromedriver.exe"

        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options = options,executable_path = path)
        driver.maximize_window()

        # ドライバが設定されるまでの待ち時間
        driver.implicitly_wait(10)

        driver.get('https://calendar.google.com/calendar/embed?src=epion1516%40gmail.com&ctz=Asia%2FTokyo')
        time.sleep(5)

        png = driver.find_element_by_class_name('mv-container').screenshot_as_png

        with open ('./img.png', 'wb') as f:
            f.write(png)

        driver.close()




# Bot本体側からコグを読み込む際に呼び出される関数
def setup(bot):
    return bot.add_cog(calendar(bot))
