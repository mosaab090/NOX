import discord
from discord.ext import commands
import os
import aiohttp
from datetime import timedelta
from dotenv import load_dotenv

# Load secret token from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'✅ NOX CORE ACTIVE ON CLOUD: {bot.user}')

# --- INFORMATIONAL ---

@bot.command()
async def socials(ctx):
    embed = discord.Embed(title="🌐 NOX OFFICIAL SOCIALS", color=discord.Color.blue())
    embed.add_field(name="YouTube", value="[@NOX_LEADER](https://youtube.com/@NOX_LEADER)", inline=False)
    embed.add_field(name="Instagram", value="[@redasimoreda](https://instagram.com/redasimoreda)", inline=False)
    embed.add_field(name="Discord", value="`theonlyshadowbyte`", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def codes(ctx):
    await ctx.send("🔥 **ACTIVE CODES:**\n• `COMMUNITY24` (Wrap)\n• `FREE183` (3 Keys)\n• `ROBLOX_RTC` (5 Keys)")

@bot.command()
async def req(ctx):
    await ctx.send("⚔️ **NOX REQUIREMENTS:**\n1. Rank 50+\n2. Must have Discord\n3. Active in VC\n4. Pass 1v1 Tryout")

@bot.command()
async def status(ctx):
    await ctx.send("🚀 **NOX TITAN CORE** is fully operational.")

@bot.command()
async def help(ctx):
    await ctx.send("⚙️ **COMMANDS:**\n`!socials`, `!codes`, `!req`, `!status`, `!ban`, `!kick`, `!ms`, `!unmute`, `!rm`, `!cr`, `!un`, `!name`, `!img`")

# --- MODERATION ---

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member.name} has been banned.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: int):
    user = await bot.fetch_user(user_id)
    await ctx.guild.unban(user)
    await ctx.send(f"🔓 {user.name} has been unbanned.")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"🥾 {member.name} has been kicked.")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def ms(ctx, member: discord.Member, minutes: int):
    await member.timeout(timedelta(minutes=minutes))
    await ctx.send(f"🔇 {member.mention} muted for {minutes}m.")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def unmute(ctx, member: discord.Member):
    await member.timeout(None)
    await ctx.send(f"🔊 {member.mention} unmuted.")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def rm(ctx, amount: int):
    deleted = await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🧹 Removed {len(deleted)-1} messages.", delete_after=5)

@bot.command()
@commands.has_permissions(manage_roles=True)
async def cr(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f"✅ Added {role.name} to {member.name}.")

@bot.command()
@commands.has_permissions(manage_nicknames=True)
async def un(ctx, member: discord.Member, *, new_name: str):
    await member.edit(nick=new_name)
    await ctx.send(f"👤 Nickname changed to {new_name}.")

@bot.command()
@commands.has_permissions(administrator=True)
async def name(ctx, *, new_name: str):
    await ctx.guild.edit(name=new_name)
    await ctx.send(f"🏢 Server name changed to {new_name}.")

@bot.command()
@commands.has_permissions(administrator=True)
async def img(ctx, url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                image_data = await resp.read()
                await ctx.guild.edit(icon=image_data)
                await ctx.send("🖼️ Server icon updated.")
            else:
                await ctx.send("❌ Failed to download image.")

bot.run(TOKEN)