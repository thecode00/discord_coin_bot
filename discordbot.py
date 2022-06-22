import discord
from discord.ext import commands
from pretty_help import PrettyHelp
import requests
import json
import os

bot_activity = discord.Game(name='@help | 떡락')
bot = commands.Bot(command_prefix='@', activity=bot_activity)
bot.help_command=PrettyHelp()
TOKEN = os.environ.get('BOT_TOKEN') # heroku 외부 설정에서 가져옴

@bot.event
async def on_ready():
    print("봇이 시작되었습니다.")

class CCog(commands.Cog, name = "Commands"):
    """명령 리스트"""
    @commands.command(description='This is the full description')
    async def coin(self, ctx, id):
        """코인 가격 ex: @coin btc """
        url = "https://api.upbit.com/v1/ticker?markets=KRW-" + id
        headers = {"Accept": "application/json"}
        response = requests.get(url, headers=headers)
        print(response.status_code)
        print(type(response.text))
        
        if response.status_code == 200:
            json_original = json.loads(response.text)
            json_name = json_original[0]["market"]
            json_price = json_original[0]["trade_price"]
            print(json_price, json_name)
            await ctx.send("마켓: {0}   가격: {1}".format(json_name, int(json_price)))
        else:
            await ctx.send("코인이름 오류   ex:   비트코인 -> BTC, 이더리움 -> ETH")


    @commands.command()
    async def ping(self, ctx):
        """Pong!"""
        await ctx.send(f'pong! {round(round(bot.latency, 4)*1000)}ms')

bot.add_cog(CCog(bot))
bot.run(TOKEN)
