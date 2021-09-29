# -*- coding: utf-8 -*-
from typing import overload
from discord import activity, channel, Embed
from main import MyBot
from discord.ext import commands
import discord
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
import datetime
from dateutil.relativedelta import relativedelta


class calendar(commands.Cog):

    # mycogクラスのコンストラクタ
    def __init__(self, bot):
        self.bot = bot

    # コマンドの例
    @commands.command()
    async def calendar(self, ctx):
        
        # 時間のかかる処理なので入力中の表示
        async with ctx.typing():

            # カレンダー部分のスクリーンショット
            #path = "C:/bin/chromedriver"
            path = "/usr/bin/chromedriver"

            options = Options()
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            driver = webdriver.Chrome(options = options,executable_path = path)
            driver.set_window_size(1920, 1080)

            # ドライバが設定されるまでの待ち時間
            driver.implicitly_wait(5)

            driver.get('https://calendar.google.com/calendar/embed?src=epion1516%40gmail.com&ctz=Asia%2FTokyo')
            time.sleep(5)

            # 指定の要素をpngでキャプチャ
            png = driver.find_element_by_class_name('mv-container').screenshot_as_png

            # ファイルの保存
            with open('./img.png', 'wb') as f:
                f.write(png)

            # 次の月へ
            driver.find_element_by_id('navForward1').click()
            time.sleep(3)
            png2 = driver.find_element_by_class_name('mv-container').screenshot_as_png

            with open('./img2.png', 'wb') as f:
                f.write(png2)

            # 予定リスト
            driver.find_element_by_id('tab-controller-container-agenda').click()
            driver.set_window_size(480, 1440)
            driver.find_element_by_id('todayButton1').click()
            time.sleep(5)
            png3 = driver.find_element_by_id('eventContainer1').screenshot_as_png

            with open('./img3.png', 'wb') as f:
                f.write(png3)

            # カレンダーチャンネルのクリア
            channel = discord.utils.get(ctx.guild.text_channels, name = "カレンダー")
            await channel.purge()

            # カレンダーのキャプチャを送信
            imgpath = os.getcwd() + "/img.png"
            month = datetime.datetime.now().strftime('%-m月')
            await channel.send(month, file = discord.File(imgpath))
            imgpath = os.getcwd() + "/img2.png"
            next_month = datetime.datetime.now() + relativedelta(months = 1)
            await channel.send(next_month.strftime('%m-月'), file = discord.File(imgpath))
            imgpath = os.getcwd() + "/img3.png"
            await channel.send("リスト", file = discord.File(imgpath))


            driver.close()


# Bot本体側からコグを読み込む際に呼び出される関数
def setup(bot):
    return bot.add_cog(calendar(bot))
