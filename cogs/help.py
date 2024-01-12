import discord
import json
from discord.ext import commands

class help(commands.Cog):
    def __init__(self, client):
        self.client = client

    def get_prefix(self, msg):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        return prefixes[str(msg.guild.id)]

    @commands.group(aliases=['Help'], invoke_without_command=True)
    async def help(self,ctx):
        prefix = self.get_prefix(ctx.message)
        emb = discord.Embed(title="Help",
                            description=f"Use {prefix}help <command> for extended information about that command",
                            color=discord.Colour.blue())
        emb.add_field(name="**Information**",
                      value=f"{prefix}serverinfo\n{prefix}getid\n{prefix}invite\n{prefix}userinfo\n{prefix}ping",
                      inline=True)
        emb.add_field(name="**Configuration**",
                      value=f"{prefix}prefix\n{prefix}clear\n{prefix}ban\n{prefix}unban\n{prefix}kick\n{prefix}poll",
                      inline=True)
        emb.add_field(
            name="**Music**",
            value=f"{prefix}join\n{prefix}leave\n{prefix}play\n{prefix}skip\n{prefix}voteskip\n{prefix}stop\n{prefix}pause\n{prefix}resume\n{prefix}restart\n{prefix}youtube",
            inline=True
        )
        emb.add_field(name="**Fun**", value=f"{prefix}meme", inline=True)
        await ctx.send(embed=emb)

    @help.command(aliases=['Meme'])
    async def meme(self,ctx):
        prefix = self.get_prefix(ctx.message)
        emb = discord.Embed(title="Meme", description="Post a meme from reddit", color=discord.Colour.blue())
        emb.add_field(name="**Syntax**", value=f"{prefix}meme")
        await ctx.send(embed=emb)

    @help.command(aliases=['Kick'])
    async def kick(self,ctx):
        prefix = self.get_prefix(ctx.message)
        emb = discord.Embed(title="Kick", description="Kick a member from server", color=discord.Colour.blue())
        emb.add_field(name="**Syntax**", value=f"{prefix}kick <member> [reason]")
        await ctx.send(embed=emb)

    @help.command(aliases=['Ban'])
    async def ban(self,ctx):
        prefix = self.get_prefix(ctx.message)
        emb = discord.Embed(title="Ban", description="Ban a member from server", color=discord.Colour.blue())
        emb.add_field(name="**Syntax**", value=f"{prefix}ban <member> [reason]")
        await ctx.send(embed=emb)

    @help.command(aliases=['Unban'])
    async def unban(self,ctx):
        prefix = self.get_prefix(ctx.message)
        emb = discord.Embed(title="Unban", description="Unban a member from server", color=discord.Colour.blue())
        emb.add_field(name="**Syntax**", value=f"{prefix}unban <member>")
        await ctx.send(embed=emb)

    @help.command(aliases=['Clear'])
    async def clear(self,ctx):
        prefix = self.get_prefix(ctx.message)
        emb = discord.Embed(title="Clear", description="Clear messages from Channel", color=discord.Colour.blue())
        emb.add_field(name="**Syntax**",
                      value=f"{prefix}clear <number of messages u want to clear> default number is 2")
        await ctx.send(embed=emb)

    @help.command(aliases=['Userinfo'])
    async def userinfo(self,ctx):
        prefix = self.get_prefix(ctx.message)
        emb = discord.Embed(title="Userinfo", description="Display information about user", color=discord.Colour.blue())
        emb.add_field(name="**Syntax**", value=f"{prefix}userinfo @<username>")
        await ctx.send(embed=emb)

    @help.command(aliases=['Invite'])
    async def invite(self,ctx):
        prefix = self.get_prefix(ctx.message)
        emb = discord.Embed(title="Invite", description='Gives invite link for "numb"', color=discord.Colour.blue())
        emb.add_field(name="**Syntax**", value=f"{prefix}invite")
        await ctx.send(embed=emb)

    @help.command(aliases=['Ping'])
    async def ping(self,ctx):
        prefix = self.get_prefix(ctx.message)
        emb = discord.Embed(title="Ping", description="Returns latency of bot to respond", color=discord.Colour.blue())
        emb.add_field(name="**Syntax**", value=f"{prefix}ping")
        await ctx.send(embed=emb)

    @help.command(aliases=['Join'])
    async def join(self,ctx):
        prefix = self.get_prefix(ctx.message)
        emb = discord.Embed(title="Join", description="Join bot to channel (You have to connected to channel first!)",
                            color=discord.Colour.blue())
        emb.add_field(name="**Syntax**", value=f"{prefix}join")
        await ctx.send(embed=emb)

    @help.command(aliases=['Leave'])
    async def leave(self,ctx):
        prefix = self.get_prefix(ctx.message)
        emb = discord.Embed(title="Leave", description="Bot leaves from channel that joined",
                            color=discord.Colour.blue())
        emb.add_field(name="**Syntax**", value=f"{prefix}leave")
        await ctx.send(embed=emb)

    @help.command(aliases=['Queue'])
    async def queue(self,ctx):
        prefix = self.get_prefix(ctx.message)
        emb = discord.Embed(title="Queue", description="Shows list of songs in queue", color=discord.Colour.blue())
        emb.add_field(name="**Syntax**", value=f"{prefix}queue")
        await ctx.send(embed=emb)

    @help.command(aliases=['Pause'])
    async def pause(self,ctx):
        prefix = self.get_prefix(ctx.message)
        emb = discord.Embed(title="Pause", description="Pause any audio that plays from bot",
                            color=discord.Colour.blue())
        emb.add_field(name="**Syntax**", value=f"{prefix}pause")
        await ctx.send(embed=emb)

    @help.command(aliases=['Resume'])
    async def resume(self,ctx):
        prefix = self.get_prefix(ctx.message)
        emb = discord.Embed(title="Resume", description="Resumes paused audio", color=discord.Colour.blue())
        emb.add_field(name="**Syntax**", value=f"{prefix}resume")
        await ctx.send(embed=emb)

    @help.command(aliases=['Stop'])
    async def stop(self,ctx):
        prefix = self.get_prefix(ctx.message)
        emb = discord.Embed(title="Stop", description="Stops bot from playing any songs", color=discord.Colour.blue())
        emb.add_field(name="**Syntax**", value=f"{prefix}stop")
        await ctx.send(embed=emb)

    @help.command(aliases=['Getid'])
    async def getid(self,ctx):
        prefix = self.get_prefix(ctx.message)
        emb = discord.Embed(title="Getid", description="Show you the ID of this server", color=discord.Colour.blue())
        emb.add_field(name="**Syntax**", value=f"{prefix}getid")
        await ctx.send(embed=emb)

    @help.command(aliases=['Serverinfo'])
    async def serverinfo(self,ctx):
        prefix = self.get_prefix(ctx.message)
        emb = discord.Embed(title="Serverinfo", description="Show you some info about server",
                            color=discord.Colour.blue())
        emb.add_field(name="**Syntax**", value=f"{prefix}serverinfo")
        await ctx.send(embed=emb)

    @help.command(aliases=['Voteskip'])
    async def voteskip(self,ctx):
        prefix = self.get_prefix(ctx.message)
        emb = discord.Embed(title="Voteskip", description="Setup vote for skipping audio that plays from numb",
                            color=discord.Colour.blue())
        emb.add_field(name="**Syntax**", value=f"{prefix}voteskip")
        await ctx.send(embed=emb)

async def setup(client):
    await client.add_cog(help(client))