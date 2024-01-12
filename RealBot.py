import asyncio
import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
import json
import yt_dlp as youtube_dl
import nacl
import praw
import random
import datetime
import time
import config

def is_connected(ctx):
    voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()

def get_prefix(client, msg):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(msg.guild.id)]

song_queue = {}

async def search_song(amount, song, get_url=False):
    info = await client.loop.run_in_executor(None, lambda: youtube_dl.YoutubeDL({
        "format": "bestaudio/best",
        "quiet": True,
        "no_warnings": True,
    }).extract_info(
        f"ytsearch{amount}:{song}",
        download=False,
        ie_key="YoutubeSearch"
    ))
    if len(info["entries"]) == 0: return None

    return [entry["webpage_url"] for entry in info["entries"]] if get_url else info

async def play_song(ctx, url):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    ffmpeg_opts = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    ydl_opts = {'format': 'bestaudio'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        song_info = ydl.extract_info(url, download=False)
    voice.play(discord.FFmpegPCMAudio(song_info["url"], **ffmpeg_opts))
    voice.source.volume = 0.5

async def check_queue(ctx):
    voice = get(ctx.bot.voice_clients, guild=ctx.guild)
    if not is_connected(ctx):
        return
    if len(song_queue[ctx.guild.id]) > 0:
        title = pafy.new(song_queue[ctx.guild.id][0]).title
        time = pafy.new(song_queue[ctx.guild.id][0]).duration
        await ctx.send(f"Now Playing: **{title} {time}**")
        await play_song(ctx, song_queue[ctx.guild.id][0])
        song_queue[ctx.guild.id].pop(0)
    if len(song_queue[ctx.guild.id]) == 0 and not voice.is_playing():
        await voice.disconnect()
        await ctx.send("numb disconnected from voice channel because queue were empty!!")

async def connect_voicechannel(ctx):
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await voice_channel.connect()

num = {
    1: ":one:",
    2: ":two:",
    3: ":three:",
    4: ":four:",
    5: ":five:"
}

Cog = ('cogs.help','cogs.admin','cogs.info')

client = commands.Bot(command_prefix=get_prefix, intents=discord.Intents.all())
client.remove_command("help")

def setp():
    for guild in client.guilds:
        song_queue[guild.id] = []

reddit = praw.Reddit(
    client_id="bJ1SDTx7muBhDhH6nJH85A",
    client_secret="9gHbOFDBj1Ym1fN-hXEMXaQMJwsPcA",
    username="Bot1234Uni",
    password="Uni.1234",
    user_agent="pypraw",
    check_for_async=False
)

filter_words = ["Uni", "uni"]

@client.event
async def on_ready():
    print('numb wakes up')
    await client.load_extension('cogs.help')
    await client.load_extension('cogs.info')
    await client.load_extension('cogs.admin')

@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixe = json.load(f)
    prefixe[str(guild.id)] = '#'
    with open('prefixes.json', 'w') as f:
        json.dump(prefixe, f, indent=4)

@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixe = json.load(f)
    prefixe.pop(str(guild.id))
    with open('prefixes.json', 'w') as f:
        json.dump(prefixe, f, indent=4)

@client.event
async def on_message(msg):
    if msg.mentions:
        if msg.mentions[0] == client.user:
            with open('prefixes.json', 'r') as f:
                prefixe = json.load(f)
            prefix = prefixe[str(msg.guild.id)]
            if prefix == "*":
                await msg.channel.send(f"Use {prefix}help to check commands \n")
                await msg.channel.send(f"Prefix for this server is {prefix}")
            else:
                await msg.channel.send(f"Use {prefix}help to check commands \nPrefix for this server is {prefix}")

    for word in filter_words:
        if word in msg.content:
            await msg.delete()

    await client.process_commands(msg)

@client.event
async def on_voice_state_update(member, before, after):
    voice_state = member.guild.voice_client
    if voice_state is None:
        return
    if voice_state.channel.members == member:
        return
    if len(voice_state.channel.members) == 1 and voice_state.is_connected():
        voice = get(client.voice_clients, guild=member.guild)
        await member.guild.system_channel.send("numb paused!!\nand numb gonna leave voice channel if let it be alone for one minute :(")
        voice.pause()
        playing = False
        timer = 60
        while not playing:
            await asyncio.sleep(1)
            timer -= 1
            if not len(voice_state.channel.members) == 1:
                playing = True
                return voice.resume()
            if timer < 0:
                await voice.disconnet()
                return await member.guild.system_channel.send("numb disconnected!!")

@client.event
async def on_command_error(ctx, error):
    Prefix = get_prefix(client, ctx.message)
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Invalid Command\nUse {Prefix}help to check commands ")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Use {Prefix}help to check commands and their syntax")
    else:
        raise error

@client.command(aliases=['Poll', 'pll'])
@commands.has_permissions()
async def poll(ctx, *, msg):
    try:
        op1, op2 = msg.split("or")
        txt = f"React with :one: for {op1} or :two: for {op2}"
    except:
        await ctx.send("Correct: [First option] or [Second option]")
        return
    embed = discord.Embed(title="Poll", description=txt, color=discord.Colour.blue())
    messag = await ctx.send(embed=embed)
    await messag.add_reaction("1️⃣")
    await messag.add_reaction("2️⃣")

@client.command(aliases=['Meme'])
async def meme(ctx):
    subreddit = reddit.subreddit("meme")
    all_subs = []
    hot = subreddit.hot(limit=50)
    for submission in hot:
        all_subs.append(submission)
    random_sub = random.choice(all_subs)
    title = random_sub.title
    description = random_sub.selftext
    url = random_sub.url
    embed = discord.Embed(title=title, description=description)
    embed.set_image(url=url)
    await ctx.send(embed=embed)

@client.command(aliases=['Play', 'P', 'p'])
async def play(ctx, *, song=None):
    if ctx.author.voice is None or ctx.author.voice.channel is None:
        return await ctx.send("You must join to a voice channel first!!")
    if song is None:
        return await ctx.send("numb dosen't get any songs to play")
    if not is_connected(ctx):
        await connect_voicechannel(ctx)
    message = await ctx.send("numb is searching for song, this may take a few seconds!")
    if not ("youtube.com?watch?") in song or not "https://youtube" in song:
        reslt = await search_song(1, song, get_url=True)
        result = await search_song(1, song)
        if result is None:
            return await message.edit(content="numb can't find song you want try something else")
        song = reslt[0]
        for entry in result["entries"]:
            duration = entry['duration']
            time = str(datetime.timedelta(seconds=duration))
            title = f"{entry['title']} {time}"
    if ctx.voice_client.source is not None:
        song_queue[ctx.guild.id].append(song)
        return await message.edit(content=f"**{title}**\nadded to queue!")
    await message.edit(content=f"Now playing: **{title}**")
    await play_song(ctx, song)

@play.error
async def play_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        return await ctx.send("You should use this command slower, numb can't recognize it!!")
    else:
        raise error

@client.group(aliases=['Youtube','Yt','yt'])
async def youtube(ctx, *, song=None):
    if ctx.author.voice is None or ctx.author.voice.channel is None:
        return await ctx.send("You must join to a voice channel first!!")
    if song is None:
        return await ctx.send("numb dosen't get any songs to play")
    message = await ctx.send("numb is searching for song, this may take a few seconds!")
    if not ("youtube.com?watch?") in song or "https://youtu.be/" in song:
        info = await search_song(5, song)
        result = await search_song(5, song, get_url=True)
        if info is None:
            return await message.edit(content="numb can't find song you want try something else")
        await message.delete()
        embd = discord.Embed(title=f"Results for {song}:",
                             description=f"**you can select one of link to play with one of emojis between 1 to 5\n or if It's not the song you want you can select ❌ reaction\n or even you can copy links and use it:**\n")
        amount = 1
        titles = []
        for entry in info["entries"]:
            duration = entry['duration']
            time = str(datetime.timedelta(seconds=duration))
            embd.description += f"{num[amount]}:  [{entry['title']}]({entry['webpage_url']}) {time}\n"
            title = f"{entry['title']} {time}"
            titles.append(title)
            amount += 1
    else:
        if ctx.voice_client.source is not None:
            song_queue[ctx.guild.id].append(song)
            return await message.edit(content=f"**{song}**\nadded to queue!")
        await message.edit(content=f"Now playing: **{song}**")
        return await play_song(ctx, song)

    search_msg = await ctx.send(embed=embd)
    msg_id = search_msg.id
    await search_msg.add_reaction("1️⃣")
    await search_msg.add_reaction("2️⃣")
    await search_msg.add_reaction("3️⃣")
    await search_msg.add_reaction("4️⃣")
    await search_msg.add_reaction("5️⃣")
    await search_msg.add_reaction("❌")
    search_msg = await ctx.channel.fetch_message(msg_id)
    votes = {"1️⃣": 0,"2️⃣": 0,"3️⃣": 0,"4️⃣": 0,"5️⃣": 0,"❌":0}
    reacted = []
    select_song = False
    await connect_voicechannel(ctx)
    timer = 60
    while not select_song:
        for reaction in search_msg.reactions:
            if reaction.emoji in ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","❌"]:
                async for user in reaction.users():
                    if user.voice.channel.id == ctx.voice_client.channel.id and user.id not in reacted and not user.bot:
                        votes[reaction.emoji] += 1
                        reacted.append(user.id)
        if votes["1️⃣"] > 0:
            song = result[0]
            title = titles[0]
            select_song = True
        elif votes["2️⃣"] > 0:
            song = result[1]
            title = titles[1]
            select_song = True
        elif votes["3️⃣"] > 0:
            song = result[2]
            title = titles[2]
            select_song = True
        elif votes["4️⃣"] > 0:
            song = result[3]
            title = titles[3]
            select_song = True
        elif votes["5️⃣"] > 0:
            song = result[4]
            title = titles[4]
            select_song = True
        elif votes["❌"] > 0:
            decliend = discord.Embed(title="You didn't choose any song from list",description="**Try and search another song**")
            voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
            if not voice_client.is_playing():
                await voice_client.disconnect()
            await search_msg.clear_reactions()
            return await search_msg.edit(embed=decliend)
        elif timer < 0:
            notselcted = discord.Embed(title="You just didn't select from options",description="**Try and search another song**")
            await search_msg.clear_reactions()
            return await search_msg.edit(embed=notselcted)
        await asyncio.sleep(1)
        timer -= 1
    if ctx.voice_client.source is not None:
        song_queue[ctx.guild.id].append(song)
        queue_song = discord.Embed(title="Your selected song added to queue!",description=f"**{title} added to queue!**")
        await search_msg.clear_reactions()
        return await search_msg.edit(embed=queue_song)
    playing_song = discord.Embed(title="Playing song",description=f"**numb plays {title} for you!**")
    await search_msg.clear_reactions()
    await search_msg.edit(embed=playing_song)
    await play_song(ctx, song)

@youtube.error
async def youtube_error(ctx,error):
    if isinstance(error, commands.CommandInvokeError):
        return
    else:
         raise error

@client.command(aliases=['Join'])
async def join(ctx):
    if ctx.author.voice is None or ctx.author.voice.channel is None:
        return await ctx.send("You must join to a voice channel first!!")
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        ch = ctx.author.voice.channel
        await voice_channel.connect()
        await ctx.send(f"numb joined to {ch}")
    else:
        ch = ctx.author.voice.channel
        await ctx.voice_client.move_to(voice_channel)
        await ctx.send(f"numb joined to {ch}")

@client.command(aliases=['Leave'])
async def leave(ctx):
    if (ctx.voice_client):
        ch = ctx.author.voice.channel
        await ctx.guild.voice_client.disconnect()
        await ctx.send(f"numb just left from {ch}")
    else:
        await ctx.send("numb is not in a voice channel!!")

@client.command(aliases=['Pause'])
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if not is_connected(ctx):
        return await ctx.send("numb is not playing anything!!")
    if voice.is_playing():
        voice.pause()
        await ctx.send("numb has paused the playing audio!")
    else:
        await ctx.send("numb is not playing anything!!")

@client.command(aliases=['Resumme'])
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if not is_connected(ctx):
        return await ctx.send("numb is not playing anything!!")
    if voice.is_paused():
        voice.resume()
        await ctx.send("numb is now playing!")
    else:
        await ctx.send("numb is not paused!!")

@client.command(aliases=['Stop'])
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if not is_connected(ctx):
        return await ctx.send("numb is not playing anything!!")
    if voice.is_paused() or voice.is_playing():
        ctx.voice_client.stop()
        song_queue[ctx.guild.id] = []
        await ctx.send("numb stops playing audio!!")
    else:
        await ctx.send("numb currently playing nothing!!")

@client.command(aliases=['Queue'])
async def queue(ctx):
    if len(song_queue[ctx.guild.id]) == 0 :
        return await ctx.send("numb currently playing nothing!!")
    embd = discord.Embed(tile="Song Queue", description="", color=discord.Colour.blue())
    i = 1
    for url in song_queue[ctx.guild.id]:
        title = pafy.new(url).title
        time = pafy.new(url).duration
        embd.description += f"**{i}: {title} {time}**\n"
        i += 1
    await  ctx.send(embed=embd)

@client.command(aliases=['Skip'])
async def skip(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if not is_connected(ctx):
        return await ctx.send("numb is not playing anything!!")
    if voice.is_playing() or voice.is_paused():
        ctx.voice_client.stop()
        await ctx.send("numb skips song!")
    else:
        await ctx.send("numb currently playing nothing!!")

@client.command(aliases=['Volume'])
async def volume(ctx, volume: int):
    if ctx.voice_client is None:
        return await ctx.send("numb not connected to voice channel!")
    ctx.voice_client.source.volume = volume / 100
    await ctx.send(f"Changed volume to {volume}%")

@client.command(aliases=['Voteskip'])
async def voteskip(ctx):
    if ctx.voice_client is None:
        return await ctx.send("numb not playing anything!")
    if ctx.author.voice is None:
        return await ctx.send("You are not connected to any voice channels!")
    if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
        return await ctx.send("numb not playing anything!")

    poll = discord.Embed(
        title=f"Vote to Skip audio",
        description="**80% of the members that connected to voice channel must vote to skip!**",
        color=discord.Colour.blue()
    )
    poll.add_field(name="Skip", value=":white_check_mark:")
    poll.add_field(name="Stay", value=":no_entry_sign:")
    poll.set_footer(text="Voting ends in 15 Seconds.")
    poll_mssg = await ctx.send(embed=poll)
    poll_id = poll_mssg.id

    await poll_mssg.add_reaction(u"\u2705")
    await poll_mssg.add_reaction(u"\U0001F6AB")
    await asyncio.sleep(15)
    poll_mssg = await ctx.channel.fetch_message(poll_id)

    votes = {u"\u2705": 0, u"\U0001F6AB": 0}
    reacted = []
    for reaction in poll_mssg.reactions:
        if reaction.emoji in [u"\u2705", u"\U0001F6AB"]:
            async for user in reaction.users():
                if user.voice.channel.id == ctx.voice_client.channel.id and user.id not in reacted and not user.bot:
                    votes[reaction.emoji] += 1
                    reacted.append(user.id)
    skip = False
    if votes[u"\u2705"] > 0:
        if votes[u"\U0001F6AB"] == 0 or votes[u"\u2705"] / (votes[u"\u2705"] + votes[u"\U0001F6AB"]) > 0.79:
            skip = True
            embd = discord.Embed(title="Skiped!", description="**Audio will get skip soon**")
    if not skip:
        embd = discord.Embed(title="Skip Failed!", description="**Voting to skip audio failed**")
    embd.set_footer(text="Voting has ended!!")
    if skip:
        ctx.voice_client.stop()
    await poll_mssg.clear_reactions()
    await poll_mssg.edit(embed=embd)



async def setup():
    await client.wait_until_ready()
    setp()

async def main():
    async with client:
        client.loop.create_task(setup())
        await client.start(config.token)

asyncio.run(main())