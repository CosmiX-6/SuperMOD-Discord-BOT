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
from super_mod import lang_translator
import super_mod.assets.tr_asset_store as tas
from dotenv import load_dotenv

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

@bot.command(name='tr')
async def sm_translate(ctx,alias,*args):
    if alias == '-setup' or alias == '-set':
        arg = ' '.join(list(args))
        if len(arg) == 0:
            await ctx.send(f'> Please provide an alias || Refer the `!help tr` to know more.')
        elif lang_translator.tr_setup(arg.lower()):
            await ctx.send(f'> Default translation is now set to `{arg}`')
        else:
            await ctx.send(f'> Invalid alias `{arg}` || Please refer the `!help tr` to know more.')

    elif alias == '-t' or alias == '-to':
        if len(args) == 0:
            await ctx.send(f'> Please provide an alias || Refer the `!help tr` to know more.')
        elif len(args) == 1:
            await ctx.send(f'> Please provide an statement with alias || Refer the `!help tr` to know more.')
        else:
            arg = ' '.join(list(args[1:]))
            translated = lang_translator.tr_translate_to(args[0].lower(),arg)
            await ctx.reply(f'> {translated}' if translated is not False else f'Invalid alias `{args[0]}`.')

    elif alias == '-ds' or alias == '-status':
        status = lang_translator.detectors_status()
        embed=discord.Embed(title="Account status", color=0x14ff30, description="Note : Please use this detector only when required.")
        embed.set_author(name="Language detection Status", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/d/db/Green_circle.svg/200px-Green_circle.svg.png")
        for key, value in status.items():
            embed.add_field(name=key.title(), value=value, inline=True)
        embed.set_footer(text="Cosmix-6 | Python Dev | SuperMOD - BOT")
        await ctx.send(embed=embed)

    elif alias == '-d' or alias == '-detect':
        if len(args)!=0:
            arg = ' '.join(list(args))
            matches = lang_translator.tr_detector(arg)
            embed=discord.Embed(title=f"Result Found : {len(matches)}" if matches is not None else "No result found.", color=0x14ff30, description="Note : This language detection does not invlove Google.")
            embed.set_author(name="Language detection", icon_url="https://upload.wikimedia.org/wikipedia/commons/d/db/Google_Translate_Icon.png")
            if matches is not None:
                for i in matches:
                    language = i['language']
                    language = tas.LANGUAGES[language].title()+' - '+language
                    embed.add_field(name="Language", value=language, inline=True)
                    embed.add_field(name="Reliable", value='Yes' if i['isReliable']==True else 'No', inline=True)
                    embed.add_field(name="Confidence", value=i['confidence'], inline=True)
            else:
                embed=discord.Embed(title="No Match Found", description="Note : This language detection does not invlove Google.")
                
            embed.set_footer(text="Cosmix-6 | Python Dev | SuperMOD - BOT")
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'> Please provide an alias || Refer the `!help tr` to know more.')

    elif not alias.startswith('-') and alias.strip() != '':
        arg = ' '.join(list(args))
        arg = alias+' '+arg
        await ctx.reply(f'> {lang_translator.tr_translate(arg)}')

    else:
        await ctx.send('Invalid Input')

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
async def clear(ctx, count='1'):
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
  if '<@!' in choosen: await ctx.send(f'> {ctx.author.mention}, I choose {choosen}.')
  else: await ctx.send(f'> {ctx.author.mention}, I choose `{choosen}`.')
    
@bot.command(name="help")
async def help(ctx,*args):
    help_embed = discord.Embed(title="Command Help",description="Here are all the commands and their usages.",color=0x14ff30)
    help_embed.add_field(name="!tr", value="usage: `!tr -t <language> <message>`\nTranslate a message into requested language",inline=False)
    help_embed.add_field(name="!covid", value="usage: `!covid <country>`\nGives covid status about a country",inline=False)
    help_embed.add_field(name="!purge", value="usage: `!purge <count>`\nDeletes specified amount of message.",inline=False)
    help_embed.add_field(name="!spam", value="usage: `!spam <count> <message>`\nSpams a message for the given number of times",inline=False)
    help_embed.add_field(name="!choose", value="usage: `!choose <option1> <option2> <option...>`\nToss/Lottery system",inline=False)
    help_embed.add_field(name="!cal", value="usage: `!cal <arithematic_query>`\nCalculator (python3 based)",inline=False)
    help_embed.set_footer(text="developed by Co$MiX-( ɹǝɯɯɐɹƃoɹd uoɥʇʎd )")
    await ctx.send(embed=help_embed)
    
@bot.command(name='cal')
async def addition(ctx,*args):
    arg = ''.join(args)
    try:
        await ctx.send(f'```**Look\'s quite easy,**\n\n{arg} = {(eval(arg)):.2f}```')
    except:
        await ctx.send('`Please avoid using alphabets.`')

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise
keep_alive.keep_alive()
bot.run(TOKEN)
