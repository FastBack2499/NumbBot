import discord
import json
from discord.ext import commands

class info(commands.Cog):
    def __init__(self, client):
        self.client = client

    def get_prefix(self, msg):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        return prefixes[str(msg.guild.id)]

    @commands.command(aliases=['UserInfo', 'Userinfo'])
    @commands.has_permissions()
    async def userinfo(self,ctx, member: discord.User):
        user = self.client.get_user(member.id)
        embed = discord.Embed(title=member.name, description=member.mention, color=discord.Colour.blue())
        embed.add_field(name="Username:", value=member.name + "#" + member.discriminator, inline=True)
        embed.add_field(name="ID:", value=member.id, inline=True)
        embed.add_field(name="Acc Creation Date:", value=user.created_at.strftime("%B %d %Y"), inline=True)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command(aliases=['ServerInfo', 'Serverinfo'])
    @commands.has_permissions()
    async def serverinfo(self,ctx):
        prefix = self.get_prefix( ctx.message)
        total_voice = len(ctx.guild.voice_channels)
        total_text = len(ctx.guild.text_channels)
        total_membr = ctx.guild.member_count
        guild_id = ctx.guild.id
        owner = ctx.guild.owner.id
        server = self.client.get_guild(guild_id)
        creation_date = server.created_at.strftime("%B %d %Y")
        embd = discord.Embed(title=f"About {ctx.message.guild.name}:", color=discord.Colour.blue())
        embd.add_field(name="**Total Users:**", value=f"{total_membr}", inline=True)
        embd.add_field(name="**Text Channels:**", value=f"{total_text}", inline=True)
        embd.add_field(name="**Voice Channels:**", value=f"{total_voice}", inline=True)
        embd.add_field(name="**Creation Date:**", value=f"{creation_date}", inline=True)
        embd.add_field(name="**Server ID:**", value=f"{guild_id}", inline=True)
        embd.add_field(name="**Owner:**", value=f"<@{owner}>", inline=True)
        embd.add_field(name="**Prefix:**", value=f"{prefix}", inline=True)
        embd.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embd)

    @commands.command(aliases=['Getid'])
    async def getid(self,ctx):
        server = ctx.guild.id
        await ctx.send(f"This Server's ID is {server}")

    @commands.command(aliases=['Ping'])
    async def ping(self,ctx):
        await ctx.send(f"Latency: {round(self.client.latency * 1000)}ms")

    @commands.command(aliases=['Invite'])
    async def invite(self,ctx):
        link = "https://discord.com/api/oauth2/authorize?client_id=960899886360981515&permissions=8&scope=bot"
        await ctx.send(f"Use this link to Invite numb to your server:\n{link}")

async def setup(client):
    await client.add_cog(info(client))