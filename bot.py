import os
import csv
import sys
import time
import switch
import random
import keep_alive
import pandas as pd
import datetime
import discord
from discord.ext import commands
from dotenv import load_dotenv

BASE_DIR = os.path.abspath('')
opfolder = BASE_DIR+'/Output_data'
output = opfolder + '/output.txt'
output.replace(' ','\ ')

date_today = datetime.datetime.today()
date_text = date_today.strftime('%Y_%m_%d')

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')
bot.remove_command('help')

def import_html_asset(html_filename):
    d = pd.read_html(html_filename)
    df = pd.DataFrame(d[0])
    i=0
    col_r_name = {}
    for col_name in df.columns:
        col_r_name[col_name] = 'data_'+str(i)
        i+=1
    df_new = df.rename(columns=col_r_name)
    df_new['data_1'] = df_new['data_1'].apply(lambda x: x.lower())
    df_new = df_new.fillna('0')
    df_new.to_csv(f'{date_text}.csv')

def import_csv_asset(csv_filename,search_query):
    with open(f'{csv_filename}.csv') as imported_data:
        data_reader = csv.reader(imported_data)
        next(data_reader)
        for line in data_reader:
            if search_query in line:
                return line

@bot.command(name='covid')
async def corona(ctx,*args):
    arg=' '.join(args).lower()
    try:
        result = import_csv_asset(date_text,arg)
        if result:
            embed=discord.Embed(title="100% geniune.", color=0x14ff30)
            embed.set_author(name=f"Corona reports of {result[2].title()}", icon_url="http://www.fleet250.org/upload/race/corona.png")
            embed.add_field(name="Rank", value=result[0], inline=True)
            embed.add_field(name="Country with population", value=result[14], inline=True)
            embed.add_field(name="Total Cases", value=result[3], inline=True)
            embed.add_field(name="New Cases", value=result[4], inline=True)
            embed.add_field(name="Total Death", value=result[5], inline=True)
            embed.add_field(name="New Death", value=result[6], inline=True)
            embed.add_field(name="Total Recovered", value=result[7], inline=True)
            embed.add_field(name="Active Cases", value=result[8], inline=True)
            embed.add_field(name="Serious", value=result[9], inline=True)
            embed.set_footer(text="Cosmix-6 | Python Dev | SuperMOD - BOT")
            await ctx.send(embed=embed)
        else:
            await ctx.send('> `Check the country name and try again.`')
    except Exception as error:
        import_html_asset('covid_dataset.html')
        await corona(ctx,arg)

@bot.command(name = 'purge')
async def clear(ctx, count):
  if count.isdigit():
    await ctx.channel.purge(limit=int(count)+1)
  else:
    await ctx.send('> @purge `count`')

@bot.command(name='spam')
async def spam(ctx,*count):
    if len(count)>1:
        if count[0].isdigit():
            spam_text = ' '.join(count[1:])
            for counter in range(int(count[0])):
                await ctx.send(spam_text)
                time.sleep(0.1)
        else:
            await ctx.send('> Syntax : @spam `count` message')
    else:
        await ctx.send('> Syntax : @spam `count` `message`')

@bot.command(name='choose')
async def choose(ctx,*args):
  choosen = random.choice(args*3)
  # print(help(ctx.author))
  if '<@!' in choosen: await ctx.send(f'> {ctx.author}, I choose {choosen}.')
  else: await ctx.send(f'> {ctx.author}, I choose `{choosen}`.')
    
@bot.command(name="help")
async def help(ctx,*args)
    help_embed = discord.Embed(title="Command Help",description="Here are all the commands and their usages.",color=0x14ff30)
    help_embed.add_field(name="$spam", value="usage: `!spam <count> <message>`\nspams a message for the given number of times",inline=False)
    help_embed.add_field(name="$covid", value="usage: `!covid <country>`\ngives covid info about a country",inline=False)
    help_embed.set_footer(text="developed by Co$MiX-( ɹǝɯɯɐɹƃoɹd uoɥʇʎd )")
    await ctx.send(embed=help_embed)
    
@bot.command(name='cal')
async def addition(ctx,*args):
    arg = ''.join(args)
    try:
        await ctx.send(f'```**Look\'s quite easy,**\n\n{arg} = {(eval(arg)):.2f}```')
    except:
        await ctx.send('`Please avoid using alphabets.`')

@bot.command(name='!exit!')
async def close(ctx):
    await ctx.send('I\'m going to sleep now!')
    time.sleep(30)

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise
keep_alive.keep_alive()
bot.run(TOKEN)
