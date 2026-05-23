import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

TOKEN = os.getenv("TOKEN")
# =========================================
# 🧠 NỐI TỪ XỊN
# =========================================

current_word = ""
used_words = set()
game_running = False
noitu_channel = {}

WORDS = [
    "con mèo",
    "máy tính",
    "siêu xe",
    "đi học",
    "trái đất",
    "mặt trời",
    "quả táo",
    "học bài",
    "cá vàng",
    "dựng phim"
]

# =========================================
# ADD KÊNH
# =========================================

@bot.command()
@commands.has_permissions(administrator=True)
async def addnoitu(ctx):

    guild_id = str(ctx.guild.id)

    if guild_id in noitu_channel:

        return await ctx.send(
            "❌ Server đã add rồi!"
        )

    noitu_channel[guild_id] = ctx.channel.id

    await ctx.send(
        f"✅ Đã add kênh nối từ:\n"
        f"{ctx.channel.mention}"
    )

# =========================================
# START
# =========================================

@bot.command(name="start")
async def start(ctx):

    global current_word
    global used_words
    global game_running

    guild_id = str(ctx.guild.id)

    if guild_id not in noitu_channel:

        return await ctx.send(
            "❌ Chưa add kênh!"
        )

    if ctx.channel.id != noitu_channel[guild_id]:

        return await ctx.send(
            "❌ Không đúng kênh!"
        )

    used_words.clear()

    game_running = True

    current_word = random.choice(WORDS)

    await ctx.send(
        f"🧠 Bắt đầu với từ:\n"
        f"**{current_word}**"
    )

# =========================================
# STOP
# =========================================

@bot.command(name="stop")
async def stop(ctx):

    global game_running
    global current_word

    game_running = False
    current_word = ""

    await ctx.send(
        "🛑 Đã dừng nối từ!"
    )

# =========================================
# MESSAGE
# =========================================

@bot.event
async def on_message(message):

    global current_word
    global used_words
    global game_running

    if message.author.bot:
        return

    guild_id = str(message.guild.id)

    text = message.content.lower().strip()

    if (
        game_running and
        guild_id in noitu_channel and
        message.channel.id ==
        noitu_channel[guild_id]
    ):

        last_word = current_word.split()[-1]

        # =================================
        # ĐÚNG
        # =================================

        if text.startswith(last_word):

            # KHÔNG PHẢI TỪ THẬT

            if VALID_WORDS and text not in VALID_WORDS:

                return await message.add_reaction("❌")

            # TRÙNG

            if text in used_words:

                return await message.add_reaction("⚠️")

            used_words.add(text)

            current_word = text

            next_word = text.split()[-1]

            await message.add_reaction("☑️")

            # =================================
            # CHECK CÒN TỪ KHÔNG
            # =================================

            possible = False

            for w in VALID_WORDS:

                if (
                    w.startswith(next_word)
                    and w not in used_words
                ):

                    possible = True
                    break

            # =================================
            # KHÔNG CÒN TỪ => THẮNG
            # =================================

            if VALID_WORDS and not possible:

                uid = str(message.author.id)

                if uid not in coins:
                    coins[uid] = 0

                reward = 2000

                coins[uid] += reward

                used_words.clear()

                current_word = random.choice(WORDS)

                return await message.channel.send(
                    f"❌ Không còn từ để nối tiếp.\n\n"
                    f"🏆 {message.author.mention} "
                    f"thắng và nhận "
                    f"{reward:,} xu!\n\n"
                    f"🔄 Lượt mới bắt đầu với từ:\n"
                    f"**{current_word}**"
                )

        # =================================
        # SAI
        # =================================

        else:

            await message.add_reaction("❌")

    await bot.process_commands(message)

# =========================================
# TOKEN
# =========================================

bot.run(os.environ["DISCORD_TOKEN"])
bot.run(TOKEN)



