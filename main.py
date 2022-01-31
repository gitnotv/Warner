import discord
from discord.ext import commands
import json
import os 
import random
import time
import datetime
import asyncio

os.chdir('C:\\Users\\wongh85\\Desktop\\Warns Bot')

client = commands.Bot(command_prefix= '?')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title="**Command on cooldown**", description='**Command still on cooldown**, please try again in {:.2f}s'.format(error.retry_after), colour = discord.Colour.red())
        await ctx.send(embed=embed)



@client.event
async def on_ready():
    print("Bot is ready")



async def get_data():
    with open ("data.json",'r') as f:
        users = json.load(f)
    return users




async def open_profile(user):
    users = await get_data()
    
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]['warncount'] = 0


    with open ("data.json",'w') as f:
        json.dump(users,f)
        return True

@client.listen("on_message")
async def on_message(ctx):
    await open_profile(ctx.author)




@client.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *,reason='No reason Provided'):
    users = await get_data()
    user = member
    await open_profile(member)
    users[str(user.id)]['warncount'] += 1
    await ctx.send(f"{member.mention} was warned for the reason: {reason}")
    with open ('data.json', 'w') as f:
        json.dump(users,f)


@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def warncount(ctx, member: discord.Member):
    if member == None:
        member = ctx.author
    await open_profile(member)
    users = await get_data()
    user = member
    warncount = users[str(user.id)]['warncount']
    await ctx.send(f"{member.mention} has {warncount} warn(s).")


@client.command()
@commands.has_permissions(kick_members=True)
async def reset(ctx, member: discord.Member):
    await open_profile(member)
    users = await get_data()
    user = member
    users[str(user.id)]['warncount'] = 0
    await ctx.send(f"{member.mention}'s warns have been resetted to 0.")
    with open ('data.json', 'w') as f:
        json.dump(users,f)

client.remove_command('help')

@client.command()
@commands.has_permissions(kick_members=True)
async def help(ctx):
    embed = discord.Embed(title=" Help center", description=' **?help** - shows this command \n **?warn** <member> <reason(optional)> - warns specified user \n **?reset** <user> - resets warn count for specified user \n **?warncount** <user> - shows how much warns a specified user has \n\n **IMPORTANT** Instead of doing ?warncount <user> in general you could alternativley right click the user and press copy id and type ?warncount <the id you copied> \n\n', colour = discord.Colour.blue())
    await ctx.send(embed=embed)




client.run('OTM2ODc3NDU1MDkwNzk4NjUz.YfTlHw.D5mnf03JBMmZbfl-M8HyP9buxv8')

