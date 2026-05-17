import discord
from discord.ext import commands, tasks
import random
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="+", intents=intents)

CANAL_ID = 1503916757424017529
BIGVOUCH_CANAL_ID = 1503916783667515432

parar_vouch = False
parar_bigvouch = False

nomes = [
    "Fraga", "visionario", "GOD_KAIOX", "ruan", "Brenox",
    "Alan", "Neco", "bah", "moc", "77",
    "Juliana", "cix", "ultimate", "quebe", "Estevao",
    "Lynyk", "Pedro", "Kauan", "Gui", "Mika",
    "Shadow", "Lotus", "Dragon", "Rafael", "Victor",
    "Lukinha", "Sasuke", "Narutin", "Gustavo", "Killer",
    "Frost", "Dark", "Ghost", "Ryann", "Pablo",
    "Tsunami", "Kauazin", "Skull", "Hazin", "Matheus",
    "Felp", "Tiozinn", "Riquinho", "Eclipse", "Joazin",
    "Brunin", "Carlos", "Lipe", "Gabe", "Davi",
    "Natan", "Mush", "Kyr", "Mikael", "Vortex",
    "Sniper", "Raze", "Venom", "Titan", "Rafa",
    "Leo", "Jota", "King", "Zero", "Pekka",
    "Luan", "Kadu", "Mendes", "Nicolas", "Ruanzin",
    "Dagger", "Docker", "Mestre", "Lorenzo", "Marlon",
    "Guilherme", "Morcego", "Pinguim", "Trem", "Foguete",
    "Biel", "Cauan", "Rick", "Loki", "Mago",
    "Akira", "Yuri", "Santi", "Mikazin", "Demon",
    "Maluco", "Ninja", "Bolt", "Kakashi", "Jhow",
    "Wesley", "Arthur", "Cris", "Playboy", "Fael"
]

@bot.event
async def on_ready():
    print(f"Bot ligado como {bot.user}")
    vouch_auto.start()
    bigvouch_auto.start()

@bot.command()
async def scam(ctx):

    file = discord.File("scam.png", filename="scam.png")

    embed = discord.Embed(color=0x8A2BE2)
    embed.set_image(url="attachment://scam.png")

    await ctx.send(embed=embed, file=file)

def criar_vouch():

    valor = round(random.uniform(10, 300), 2)

    p1 = random.choice(nomes)
    p2 = random.choice(nomes)

    while p1 == p2:
        p2 = random.choice(nomes)

    embed = discord.Embed(
        title="💸 ── Troca de PIX completa. (Automático)",
        description="Uma troca de pix automática aconteceu, informações abaixo:",
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

    return embed

def criar_bigvouch():

    valor = round(random.uniform(300, 3000), 2)

    p1 = random.choice(nomes)
    p2 = random.choice(nomes)

    while p1 == p2:
        p2 = random.choice(nomes)

    embed = discord.Embed(
        title="💰 ── BIG VOUCH",
        description="Uma troca de pix automática aconteceu, informações abaixo:",
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

    return embed

@bot.command()
async def vouch(ctx, quantidade: int = 1):

    global parar_vouch
    parar_vouch = False

    quantidade = max(1, quantidade)

    for _ in range(quantidade):

        if parar_vouch:
            await ctx.send("🛑 Vouch manual parado.")
            break

        await ctx.send(embed=criar_vouch())

@bot.command()
async def stopvouch(ctx):

    global parar_vouch
    parar_vouch = True

    await ctx.send("🛑 Parando os vouchs manuais...")

@bot.command()
async def bigvouch(ctx, quantidade: int = 1):

    global parar_bigvouch
    parar_bigvouch = False

    quantidade = max(1, quantidade)

    for _ in range(quantidade):

        if parar_bigvouch:
            await ctx.send("🛑 Big vouch manual parado.")
            break

        await ctx.send(embed=criar_bigvouch())

@bot.command()
async def stopbigvouch(ctx):

    global parar_bigvouch
    parar_bigvouch = True

    await ctx.send("🛑 Parando os big vouchs manuais...")

@tasks.loop(minutes=3)
async def vouch_auto():

    canal = bot.get_channel(CANAL_ID)

    if canal:
        await canal.send(embed=criar_vouch())

@tasks.loop(minutes=3)
async def bigvouch_auto():

    canal = bot.get_channel(BIGVOUCH_CANAL_ID)

    if canal:
        await canal.send(embed=criar_bigvouch())

bot.run(os.getenv("TOKEN"))
