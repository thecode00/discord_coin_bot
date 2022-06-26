import discord
from discord.ext import commands
from pretty_help import PrettyHelp
from bs4 import BeautifulSoup
import urllib.request
import requests
import json
import os

bot_activity = discord.Game(name='#help | 떡락')
bot = commands.Bot(command_prefix='#', activity=bot_activity)
bot.help_command = PrettyHelp()
TOKEN = os.environ.get('TOKEN')  # heroku 외부 설정에서 가져옴


@bot.event
async def on_ready():
    print("봇이 시작되었습니다.")


class CCog(commands.Cog, name="Commands"):
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

            embed = discord.Embed(title=json_name)
            embed.add_field(name="가격", value=str(int(json_price)))
            await ctx.send(embed=embed)
        else:
            await ctx.send("코인이름 오류   ex:   비트코인 -> BTC, 이더리움 -> ETH")

    @commands.command()
    async def maple(self, ctx, nick):
        """maple.gg에서 플레이어 정보를 가져옴"""
        url = "http://maple.gg/u/" + nick
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            nickname = soup.select_one(
                "#user-profile > section > div.row.row-normal > div.col-lg-8 > h3 > b")
            level = soup.select_one(
                "#user-profile > section > div.row.row-normal > div.col-lg-8 > div.user-summary > ul > li:nth-child(1)")
            image_url = soup.select_one(
                "#user-profile > section > div.row.row-normal > div.col-lg-4.pt-1.pt-sm-0.pb-1.pb-sm-0.text-center.mt-2.mt-lg-0 > div > div.col-6.col-md-8.col-lg-6 > img").get("src")

            urllib.request.urlretrieve(image_url, "char.png")
            image = discord.File("char.png", filename="image.png")
            print(image_url)
            embed = discord.Embed(title=nickname.get_text(), color=0xffb30f)
            embed.set_thumbnail(url="attachment://image.png")
            embed.add_field(name="레벨", value=level.get_text(), inline=True)
            try:    # 무릉 최고기록이 존재할때
                print("try")
                mulung = soup.select_one(
                    "#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(1) > section > div > div.pt-4.pt-sm-3.pb-4 > div > h1")
                mulung = mulung.get_text().replace(" ", "").replace("\n", "")  # 공백 제거
                print(mulung)
                embed.add_field(name="무릉도장 최고기록", value=mulung, inline=True)
            except Exception as e:  # 무릉 기록이 존재하지 않을때
                print(e)
                mulung = soup.select_one(
                    "#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(1) > section > div > div.text-secondary")
                embed.add_field(name="무릉도장 최고기록",
                                value=mulung.get_text(), inline=True)
            embed.set_thumbnail(url=image_url)

            await ctx.send(embed=embed, file=image)
        else:
            await ctx.send("닉네임 오류")

    @commands.command()
    async def ping(self, ctx):
        """Pong!"""
        await ctx.send(f'pong! {round(round(bot.latency, 4)*1000)}ms')

    # @commands.command()
    # async def test(self, ctx):


bot.add_cog(CCog(bot))
# github에 올릴때 밑에걸로 올리기
bot.run(TOKEN)
