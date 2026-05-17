import discord
from discord.ext import commands, tasks
import random

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="+", intents=intents)

CANAL_ID = 1503916757424017529
BIGVOUCH_CANAL_ID = 1503916783667515432

nomes = [
    "Fraga", "visionario", "GOD_KAIOX", "77", "moc",
    "ruan", "Brenox", "cike", "Alan", "Estevao",
    "Lynyk", "quebe", "Safira", "Rubi", "Nexus",
    "Dragon", "Shadow", "Venom", "Blaze", "Ghost",
    "Vortex", "Hunter", "Sniper", "Kratos", "Zeus",
    "Apollo", "Hades", "Titan", "Flash", "Storm",
    "Drako", "Killer", "Wolf", "Ice", "Inferno",
    "Pixel", "Matrix", "Nova", "Turbo", "Fury",
    "Magma", "Toxic", "Cobra", "Falcon", "Raptor",
    "Blox", "Rex", "Joker", "Knight", "Sonic",
    "Bolt", "Chaos", "Rider", "Skull", "GamerX",
    "Darkzin", "Leozin", "Pedrin", "Guizin", "Kauazin",
    "Teteu", "Vitin", "Davi", "Luquinhas", "JPzin",
    "MlkDoido", "Capudo", "Lendario", "Slaa", "Ninja",
    "Pirata", "Mestre", "Patrao", "Luketa", "Kzin",
    "Brabao", "Misterioso", "Fantasma", "Monstro", "Zika",
    "TremBala", "Velocidade", "Roubador", "Pika", "Doidao",
    "Loucura", "Safado", "Ratinho", "Cabuloso", "Mitico",
    "Vision", "Dream", "Rusher", "Maluco", "KillerX",
    "Noobzera", "Prozin", "Hackzin", "Mago", "Lobo"
]

@bot.event
async def on_ready():
    print(f"Bot ligado como {bot.user}")
    vouch_fake.start()
    bigvouch_fake.start()

@bot.command()
async def scam(ctx):
    file = discord.File("scam.png", filename="scam.png")

    embed = discord.Embed(color=0x8A2BE2)
    embed.set_image(url="attachment://scam.png")

    await ctx.send(embed=embed, file=file)

@bot.command()
async def vouch(ctx, quantidade: int = 1):

    if quantidade < 1:
        quantidade = 1

    for _ in range(quantidade):

        valor = round(random.uniform(10, 300), 2)

        p1 = random.choice(nomes)
        p2 = random.choice(nomes)

        while p1 == p2:
            p2 = random.choice(nomes)

        embed = discord.Embed(
            title="🧪 • VOUCH",
            description="Mensagem automática de vouch.",
            color=0x8A2BE2
        )

        embed.add_field(
            name="💲 Valor:",
            value=f"`R$ {valor}`",
            inline=False
        )

        embed.add_field(
            name="👥 Participantes:",
            value=f"@{p1} e @{p2}",
            inline=False
        )

        embed.add_field(
            name="🕒 Horário:",
            value=f"<t:{int(discord.utils.utcnow().timestamp())}:f>",
            inline=False
        )

        await ctx.send(embed=embed)

@bot.command()
async def bigvouch(ctx, quantidade: int = 1):

    if quantidade < 1:
        quantidade = 1

    for _ in range(quantidade):

        valor = round(random.uniform(300, 3000), 2)

        p1 = random.choice(nomes)
        p2 = random.choice(nomes)

        while p1 == p2:
            p2 = random.choice(nomes)

        embed = discord.Embed(
            title="🧪 • BIG VOUCH",
            description="Mensagem automática de vouch.",
            color=0xffd700
        )

        embed.add_field(
            name="💸 Valor:",
            value=f"`R$ {valor}`",
            inline=False
        )

        embed.add_field(
            name="👥 Participantes:",
            value=f"@{p1} e @{p2}",
            inline=False
        )

        embed.add_field(
            name="🕒 Horário:",
            value=f"<t:{int(discord.utils.utcnow().timestamp())}:f>",
            inline=False
        )

        await ctx.send(embed=embed)

@tasks.loop(minutes=3)
async def vouch_fake():

    canal = bot.get_channel(CANAL_ID)

    if canal is None:
        return

    valor = round(random.uniform(10, 300), 2)

    p1 = random.choice(nomes)
    p2 = random.choice(nomes)

    while p1 == p2:
        p2 = random.choice(nomes)

    embed = discord.Embed(
        title="🧪 • VOUCH",
        description="Mensagem automática de vouch.",
        color=0x8A2BE2
    )

    embed.add_field(
        name="💲 Valor:",
        value=f"`R$ {valor}`",
        inline=False
    )

    embed.add_field(
        name="👥 Participantes:",
        value=f"@{p1} e @{p2}",
        inline=False
    )

    embed.add_field(
        name="🕒 Horário:",
        value=f"<t:{int(discord.utils.utcnow().timestamp())}:f>",
        inline=False
    )

    await canal.send(embed=embed)

@tasks.loop(minutes=3)
async def bigvouch_fake():

    canal = bot.get_channel(BIGVOUCH_CANAL_ID)

    if canal is None:
        return

    valor = round(random.uniform(300, 3000), 2)

    p1 = random.choice(nomes)
    p2 = random.choice(nomes)

    while p1 == p2:
        p2 = random.choice(nomes)

    embed = discord.Embed(
        title="🧪 • BIG VOUCH ECLIPSE",
        description="Mensagem automática de vouch.",
        color=0xffd700
    )

    embed.add_field(
        name="💸 Valor:",
        value=f"`R$ {valor}`",
        inline=False
    )

    embed.add_field(
        name="👥 Participantes:",
        value=f"@{p1} e @{p2}",
        inline=False
    )

    embed.add_field(
        name="🕒 Horário:",
        value=f"<t:{int(discord.utils.utcnow().timestamp())}:f>",
        inline=False
    )

    await canal.send(embed=embed)

import os

bot.run(os.getenv("TOKEN"))
