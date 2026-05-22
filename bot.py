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
    def __init__(self, enviador, recebedor):
        super().__init__(timeout=None)

        self.enviador = enviador
        self.recebedor = recebedor

    @discord.ui.button(label="Enviar", style=discord.ButtonStyle.green)
    async def enviar(self, interaction: discord.Interaction, button: Button):

        if interaction.user.id != self.enviador.id:
            return await interaction.response.send_message(
                "❌ Apenas o enviador pode clicar aqui.",
                ephemeral=True
            )

        trocas[interaction.channel.id] = {
            "valor": None,
            "item": None,
            "confirm_enviador": False,
            "confirm_recebedor": False,
            "enviador": self.enviador,
            "recebedor": self.recebedor
        }

        await interaction.response.send_message(
            "💸 Digite o valor da troca no chat.",
            ephemeral=True
        )

    @discord.ui.button(label="Receber", style=discord.ButtonStyle.blurple)
    async def receber(self, interaction: discord.Interaction, button: Button):

        if interaction.user.id != self.recebedor.id:
            return await interaction.response.send_message(
                "❌ Apenas quem vai receber pode clicar aqui.",
                ephemeral=True
            )

        if interaction.channel.id not in trocas:
            return await interaction.response.send_message(
                "❌ O enviador ainda não informou o valor.",
                ephemeral=True
            )

        await interaction.response.send_message(
            "🎁 Digite o item da troca no chat.",
            ephemeral=True
        )

@bot.command()
async def ec(ctx, enviador: discord.Member, recebedor: discord.Member):

    embed = discord.Embed(
        title="🧪 SIMULAÇÃO • Eclipse MM",
        description=(
            f"📤 Enviador: {enviador.mention}\n"
            f"📥 Recebedor: {recebedor.mention}\n\n"
            "Clique no botão correspondente."
        ),
        color=0x8A2BE2
    )

    await ctx.send(
        embed=embed,
        view=TrocaView(enviador, recebedor)
    )

@bot.command()
async def confirmar(ctx):

    if ctx.channel.id not in trocas:
        return await ctx.send("❌ Nenhuma troca ativa.")

    troca = trocas[ctx.channel.id]

    if ctx.author.id == troca["enviador"].id:
        troca["confirm_enviador"] = True

    elif ctx.author.id == troca["recebedor"].id:
        troca["confirm_recebedor"] = True

    else:
        return

    await ctx.send(f"✅ {ctx.author.mention} confirmou.")

    if troca["confirm_enviador"] and troca["confirm_recebedor"]:

        valor = troca["valor"] or "0"
        item = troca["item"] or "Não informado"

        mm = 1.00
        gateway = 0.20

        total = float(valor) + mm + gateway

        embed = discord.Embed(
            title="🧪 SIMULAÇÃO • PAGAMENTO PIX",
            description=(
                "Sistema apenas para TESTE.\n\n"
                f"💰 Valor da troca: R$ {valor}\n"
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
        message.author.id == troca["enviador"].id
        and troca["valor"] is None
    ):

        try:
            valor = float(message.content.replace(",", "."))

            troca["valor"] = valor

            await message.channel.send(
                f"✅ Valor definido: R$ {valor}"
            )

        except:
            pass

    elif (
        message.author.id == troca["recebedor"].id
        and troca["item"] is None
    ):

        troca["item"] = message.content

        await message.channel.send(
            f"🎁 Item definido: {message.content}\n\n"
            "Agora os dois usem `+confirmar`."
        )

bot.run(os.getenv("TOKEN"))
