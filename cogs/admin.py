import discord
import json
from discord.ext import commands

class admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['Prefix'])
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, prefix):
        with open('prefixes.json', 'r') as f:
            prefixe = json.load(f)
        prefixe[str(ctx.guild.id)] = prefix
        with open('prefixes.json', 'w') as f:
            json.dump(prefixe, f, indent=4)
        await ctx.send(f"Prefix for this server changed to {prefix}")

    @commands.command(aliases=['Clear'])
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount=2):
        await ctx.channel.purge(limit=amount)

    @commands.command(aliases=['Kick'])
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.User, *, reason="No reason"):
        await ctx.guild.kick(member)
        await ctx.send(f'User {member.mention} has been kicked for {reason}')

    @commands.command(aliases=['Ban'])
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.User, *, reason="No reason"):
        await ctx.guild.ban(member)
        await member.send(f"you got banned from {ctx.message.guild.name} because {reason}")
        await ctx.send(f'User {member.mention} has been banned for {reason}')

    @commands.command(aliases=['Unban'])
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        if member == None:
            return await ctx.send("You must put user info that you want to unban!!")
        member_name, member_disc = member.split('#')
        for banned_entry in banned_users:
            user = banned_entry.user
            if (user.name, user.discriminator) == (member_name, member_disc):
                await ctx.guild.unban(user)
                await user.send(f"you got unbanned from {ctx.message.guild.name}")
                await ctx.send(member_name + " unbanned.")
                return

        await ctx.send("We can't find member you want")

async def setup(client):
    await client.add_cog(admin(client))