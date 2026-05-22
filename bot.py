import discord
from discord.ext import commands, tasks
from discord.ui import View, Button
import random
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="+", intents=intents)

CANAL_ID = 1503916757424017529
BIGVOUCH_CANAL_ID = 1503916783667515432

parar_vouch = False
parar_bigvouch = False

trocas = {}

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

class TrocaView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Enviar", style=discord.ButtonStyle.green)
    async def enviar(self, interaction: discord.Interaction, button: Button):

        canal = interaction.channel.id

        if canal not in trocas:
            trocas[canal] = {
                "enviador": interaction.user,
                "recebedor": None,
                "valor": None,
                "item": None,
                "confirm_enviador": False,
                "confirm_recebedor": False,
                "etapa": "valor"
            }

            await interaction.response.send_message(
                "💸 Você será quem ENVIA.\nDigite o valor da troca no chat.",
                ephemeral=True
            )

        else:
            await interaction.response.send_message(
                "❌ Já existe um enviador.",
                ephemeral=True
            )

    @discord.ui.button(label="Receber", style=discord.ButtonStyle.blurple)
    async def receber(self, interaction: discord.Interaction, button: Button):

        canal = interaction.channel.id

        if canal not in trocas:
            return await interaction.response.send_message(
                "❌ Primeiro alguém deve clicar em ENVIAR.",
                ephemeral=True
            )

        troca = trocas[canal]

        if troca["recebedor"] is not None:
            return await interaction.response.send_message(
                "❌ Já existe um recebedor.",
                ephemeral=True
            )

        if interaction.user.id == troca["enviador"].id:
            return await interaction.response.send_message(
                "❌ Você já é o enviador.",
                ephemeral=True
            )

        troca["recebedor"] = interaction.user
        troca["etapa"] = "item"

        await interaction.response.send_message(
            "🎁 Você será quem RECEBE.\nDigite o item da troca no chat.",
            ephemeral=True
        )

@bot.command()
async def ec(ctx):

    trocas.pop(ctx.channel.id, None)

    embed = discord.Embed(
        title="💸 • Eclipse MM",
        description=(
            "Clique nos botões abaixo.\n\n"
            "🟢 Quem vai PAGAR → Enviar\n"
            "🔵 Quem vai RECEBER → Receber"
        ),
        color=0x8A2BE2
    )

    await ctx.send(
        embed=embed,
        view=TrocaView()
    )

@bot.command()
async def confirmar(ctx):

    if ctx.channel.id not in trocas:
        return await ctx.send("❌ Nenhuma troca ativa.")

    troca = trocas[ctx.channel.id]

    if troca["recebedor"] is None:
        return await ctx.send("❌ Ainda falta alguém clicar em RECEBER.")

    if ctx.author.id == troca["enviador"].id:
        troca["confirm_enviador"] = True

    elif ctx.author.id == troca["recebedor"].id:
        troca["confirm_recebedor"] = True

    else:
        return

    await ctx.send(f"✅ {ctx.author.mention} confirmou.")

    if troca["confirm_enviador"] and troca["confirm_recebedor"]:

        valor = troca["valor"]
        item = troca["item"]

        mm = 1.00
        gateway = 0.20

        total = float(valor) + mm + gateway

        try:
            await ctx.channel.purge(limit=100)
        except:
            pass

        embed = discord.Embed(
            title="💸 • PAGAMENTO PIX",
            description=(
                f"📤 Enviador: {troca['enviador'].mention}\n"
                f"📥 Recebedor: {troca['recebedor'].mention}\n\n"
                f"💰 Valor da troca: R$ {valor:.2f}\n"
                f"👑 Taxa MM: R$ {mm:.2f}\n"
                f"⚡ Gateway: R$ {gateway:.2f}\n"
                f"🎁 Item: {item}\n\n"
                f"# Total: R$ {total:.2f}"
            ),
            color=0x8A2BE2
        )

        view = View()

        view.add_item(
            Button(
                label="Verificar Pagamento",
                style=discord.ButtonStyle.green
            )
        )

        view.add_item(
            Button(
                label="QR Code",
                style=discord.ButtonStyle.gray
            )
        )

        view.add_item(
            Button(
                label="Copia e Cola",
                style=discord.ButtonStyle.blurple
            )
        )

        await ctx.send(embed=embed, view=view)

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

@bot.event
async def on_message(message):

    await bot.process_commands(message)

    if message.author.bot:
        return

    if message.channel.id not in trocas:
        return

    troca = trocas[message.channel.id]

    if (
        troca["etapa"] == "valor"
        and message.author.id == troca["enviador"].id
        and troca["valor"] is None
    ):

        try:

            valor = float(message.content.replace(",", "."))

            troca["valor"] = valor

            await message.delete()

            await message.channel.send(
                f"✅ Valor definido: R$ {valor:.2f}"
            )

        except:

            await message.channel.send(
                "❌ Digite apenas números.\nExemplo: `50`"
            )

    elif (
        troca["etapa"] == "item"
        and troca["recebedor"] is not None
        and message.author.id == troca["recebedor"].id
        and troca["item"] is None
    ):

        troca["item"] = message.content

        await message.delete()

        await message.channel.send(
            f"🎁 Item definido: {message.content}\n\n"
            "Agora os dois usem `+confirmar`."
        )

bot.run(os.getenv("TOKEN"))
