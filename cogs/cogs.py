# -*- coding: utf-8 -*-
from typing import overload
from discord import activity, channel, Embed
from discord.enums import ActivityType
from discord.embeds import EmptyEmbed
from dispander.module import fetch_message_from_id
from main import MyBot
from discord.ext import commands
import discord
import os
from dispander import dispand
import json
import urllib.parse
import urllib.request
import re
import datetime


regex_discord_message_url = (
    '(?!<)https://(ptb.|canary.)?discord(app)?.com/channels/'
    '(?P<guild>[0-9]{18})/(?P<channel>[0-9]{18})/(?P<message>[0-9]{18})(?!>)'
)
regex_extra_url = (
    r'\?base_aid=(?P<base_author_id>[0-9]{18})'
    '&aid=(?P<author_id>[0-9]{18})'
    '&extra=(?P<extra_messages>(|[0-9,]+))'
)


# コグとして用いるクラスを定義
class mycog(commands.Cog):

    filepath = os.getcwd() + "/cogs/file/"

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

    @commands.command()
    async def c(self, ctx):
        
        mycog.log(ctx)

        guild = ctx.guild
        cmd = ctx.message.content.replace('!c ', '').replace('　', ' ').replace('、', ',').split(',')
        
        # 「キャラクター」カテゴリーを作成
        category = await guild.create_category("キャラクター", position = 1)
        
        # 観戦ロール作成
        watch_role = await guild.create_role(name = "観戦", colour = discord.Colour.from_rgb(153,45,34))
        
        for name in cmd:
            # 各ロールを作成
            char_role = await guild.create_role(name = name)

            # キャラクターテキストチャンネルの権限
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(send_messages = False, read_messages = False),
                char_role: discord.PermissionOverwrite(send_messages = True, read_messages = True),
                watch_role: discord.PermissionOverwrite(send_messages = True, read_messages = True)
                }

            # 各テキストチャンネルの作成
            await category.create_text_channel(name, overwrites = overwrites)



        # テキストチャンネルのテンプレート 
        category = discord.utils.get(guild.categories, name = "テキストチャンネル")
        await category.create_text_channel(name = "共通")
        await category.create_text_channel(name = "公開情報")
        await category.create_text_channel(name = "キャラクター")
        await category.create_text_channel(name = "ルール")
        await category.create_text_channel(name = "導入")

        # 観戦チャンネルの権限
        overwrites = {
                guild.default_role: discord.PermissionOverwrite(send_messages = False, read_messages = False),
                watch_role: discord.PermissionOverwrite(send_messages = True, read_messages = True)
                }

        # 観戦チャンネルの作成
        channel = await category.create_text_channel(name = "観戦", overwrites = overwrites)

        # ボイスチャンネルのテンプレート
        category = discord.utils.get(guild.categories, name = "ボイスチャンネル")
        await category.create_text_channel(name = "呼びかけ用")
        await category.create_voice_channel(name = "密談１")
        await category.create_voice_channel(name = "密談２")
        await category.create_voice_channel(name = "密談３")


    # テキストチャンネルのお掃除
    @commands.command()
    async def clean(self, ctx):
        mycog.log(ctx)
        if ctx.message.author.guild_permissions.administrator:
            await ctx.message.channel.purge()

    # !status ○○でステータスの変更
    @commands.command()
    async def status(self, ctx):
        mycog.log(ctx)
        if ctx.message.author.bot:
            return
        else:
            status = ctx.message.content.split(" ")
            await self.bot.change_presence(activity = discord.Game(name = status[1], type = 1))
    
    # DeepL APIを使った翻訳
    @commands.command()
    async def translate(self, ctx):
        mycog.log(ctx)
        messages = []
        translatetxt = ctx.message.content.split(' ', 1)
        if ctx.message.author.bot:
            return
        elif translatetxt[1].startswith('https://discord.com/channels/'):
            for ids in re.finditer(regex_discord_message_url, ctx.message.content):
                if ctx.message.guild.id != int(ids['guild']):
                    continue
                fetched_message = await fetch_message_from_id(
                    guild = ctx.message.guild,
                    channel_id = int(ids['channel']),
                    message_id = int(ids['message']),
                )
                messages.append(fetched_message)
                #await ctx.reply(messages[0].content)
                translatetxt = messages[0].content
        else:
            translatetxt = translatetxt[1]

        with open(mycog.filepath + 'config.json') as j:
            config = json.load(j)
        AUTH_KEY = config['auth_key']
        DEEPL_TRANSLATE_EP = 'https://api-free.deepl.com/v2/translate'
        T_LANG_CODES = ["DE", "EN", "FR", "IT", "JA", "ES",
                        "NL", "PL", "PT-PT", "PT-BR", "PT", "RU", "ZH"]
        S_LANG_CODES = ["DE", "EN", "FR", "IT",
                        "JA", "ES", "NL", "PL", "PT", "RU", "ZH"]
        #p = argparse.ArgumentParser()
        #p.add_argument('-m', '--message', help = 'text to translate. (Default: Hello World.)', default = 'Hello World.')
        #p.add_argument('-t', '--target', help = f'target language code (Default: JA). allowed lang code : {str(T_LANG_CODES)}', default = 'JA')
        #p.add_argument('-s', '--source', help = f'source language code (Default: auto). allowed lang code : {str(S_LANG_CODES)}', default = '')
        #args = p.parse_args()
        
        async def trans(translatetxt, s_lang = 'EN', t_lang = 'JA'):
            headers = { 'Content-Type': 'application/x-www-form-urlencoded; utf-8'}

            params = {
                'auth_key': AUTH_KEY,
                'text': translatetxt,
                'target_lang': t_lang
            }

            if s_lang != '':
                params['source_lang'] = s_lang

            req = urllib.request.Request(
                DEEPL_TRANSLATE_EP,
                method = 'POST',
                data = urllib.parse.urlencode(params).encode('utf-8'),
                headers = headers
            )

            try:
                with urllib.request.urlopen(req) as res:
                    res_json = json.loads(res.read().decode('utf-8'))
                    print(res_json["translations"])
                    await ctx.reply(res_json["translations"][0]["text"])
            except urllib.error.HTTPError as e:
                print(e)

        await trans(translatetxt, t_lang = 'JA', s_lang = 'EN')

    # メッセージリンクの展開
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        elif message.content.startswith('https://discord.com/channels/'):
            await dispand(message)

# Bot本体側からコグを読み込む際に呼び出される関数
def setup(bot):
    return bot.add_cog(mycog(bot))
