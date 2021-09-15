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
import csv
from dispander import dispand
import json
import urllib.parse
import urllib.request
import re