import discord
from discord.ext import commands
import random
import os
import requests

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

TOKEN = os.getenv("TOKEN")

# =========================
# LOAD TỪ ĐIỂN
# =========================

WORDS = []

url = "https://raw.githubusercontent.com/PhamHuynhAnh16/Bot_Noi_Tu_Viet_Nam_Discord/main/TuVung.txt"

try:
    data = requests.get(url).text
    WORDS = [w.strip().lower() for w in data.splitlines() if w.strip()]
    print(f"📚 Đã load {len(WORDS)} từ")
except:
    print("❌ Không load được từ điển")

# =========================
# NỐI TỪ
# =========================

current_word = ""
used_words = set()
game_running = False

@bot.event
async def on_ready():
    print(f"✅ {bot.user} online!")

@bot.command()
async def noitu(ctx):
    global current_word, used_words, game_running

    current_word = random.choice(WORDS)
    used_words = {current_word}
    game_running = True

    await ctx.send(
        f"🎮 Bắt đầu nối từ!\n"
        f"👉 Từ hiện tại: **{current_word}**"
    )

@bot.command()
async def stop(ctx):
    global game_running

    game_running = False

    await ctx.send("🛑 Đã dừng nối từ!")

@bot.event
async def on_message(message):
    global current_word, used_words, game_running

    if message.author.bot:
        return

    await bot.process_commands(message)

    if not game_running:
        return

    text = message.content.lower().strip()

    if text.startswith("!"):
        return

    # =========================
    # KHÔNG PHẢI TỪ THẬT
    # =========================

    if text not in WORDS:

        await message.reply(
            "<a:sai:1507364168326709329>"
        )

        return

    # =========================
    # TRÙNG TỪ
    # =========================

    if text in used_words:

        await message.reply(
            "⚠️ Từ này dùng rồi!"
        )

        return

    last_word = current_word.split()[-1]
    first_word = text.split()[0]

    # =========================
    # NỐI SAI
    # =========================

    if first_word != last_word:

        await message.reply(
            "<a:sai:1507364168326709329>"
        )

        return

    # =========================
    # ĐÚNG
    # =========================

    used_words.add(text)

    current_word = text

    await message.reply(
        "<a:ng:1507364188547190965>"
    )

    # =========================
    # CHECK HẾT TỪ
    # =========================

    possible = []

    end_word = text.split()[-1]

    for w in WORDS:

        if w not in used_words:

            if w.split()[0] == end_word:

                possible.append(w)

    if len(possible) <= 2:

        game_running = False

        await message.channel.send(
            f"🏆 {message.author.mention} thắng!\n"
            f"❌ Không còn nhiều từ để nối tiếp!"
        )

bot.run(TOKEN)
