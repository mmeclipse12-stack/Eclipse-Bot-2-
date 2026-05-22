import discord
from discord.ext import commands, tasks
from discord.ui import View, Button, Modal, TextInput
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

    if not vouch_auto.is_running():
        vouch_auto.start()

    if not bigvouch_auto.is_running():
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

def criar_embed_ec(canal_id):

    troca = trocas[canal_id]

    valor_txt = "Não informado"
    if troca["valor"] is not None:
        valor_txt = f"R$ {troca['valor']:.2f}"

    embed = discord.Embed(
        title="💸 • Eclipse MM",
        description=(
            f"👤 Participante 1: {troca['membro1'].mention}\n"
            f"👤 Participante 2: {troca['membro2'].mention}\n\n"
            f"📤 Enviador: {troca['enviador'].mention if troca['enviador'] else 'Não escolhido'}\n"
            f"📥 Recebedor: {troca['recebedor'].mention if troca['recebedor'] else 'Não escolhido'}\n"
            f"💰 Valor: {valor_txt}\n"
            f"🎁 Item: {troca['item'] if troca['item'] else 'Não informado'}\n\n"
            f"✅ Enviador confirmou: {'Sim' if troca['confirm_enviador'] else 'Não'}\n"
            f"✅ Recebedor confirmou: {'Sim' if troca['confirm_recebedor'] else 'Não'}\n\n"
            "Use os botões abaixo para escolher função, preencher dados e confirmar."
        ),
        color=0x8A2BE2
    )

    return embed

async def atualizar_painel_ec(channel):

    troca = trocas.get(channel.id)

    if not troca:
        return

    try:
        msg = await channel.fetch_message(troca["mensagem_id"])
        await msg.edit(embed=criar_embed_ec(channel.id), view=ECView())
    except:
        await channel.send(embed=criar_embed_ec(channel.id), view=ECView())

class ValorModal(Modal, title="Informar valor da troca"):

    valor = TextInput(
        label="Valor",
        placeholder="Exemplo: 50 ou 50,90",
        required=True,
        max_length=12
    )

    async def on_submit(self, interaction: discord.Interaction):

        troca = trocas.get(interaction.channel.id)

        if not troca:
            return await interaction.response.send_message("❌ Nenhuma troca ativa.", ephemeral=True)

        if not troca["enviador"] or interaction.user.id != troca["enviador"].id:
            return await interaction.response.send_message("❌ Só quem clicou em ENVIAR pode informar o valor.", ephemeral=True)

        texto = str(self.valor).replace(",", ".").strip()

        try:
            valor = float(texto)
        except:
            return await interaction.response.send_message("❌ Digite apenas números. Exemplo: `50`", ephemeral=True)

        if valor <= 0:
            return await interaction.response.send_message("❌ O valor precisa ser maior que 0.", ephemeral=True)

        troca["valor"] = valor
        troca["confirm_enviador"] = False
        troca["confirm_recebedor"] = False

        await interaction.response.send_message(f"✅ Valor definido: R$ {valor:.2f}", ephemeral=True)
        await atualizar_painel_ec(interaction.channel)

class ItemModal(Modal, title="Informar item da troca"):

    item = TextInput(
        label="Item",
        placeholder="Exemplo: Brainrot secreto",
        required=True,
        max_length=80
    )

    async def on_submit(self, interaction: discord.Interaction):

        troca = trocas.get(interaction.channel.id)

        if not troca:
            return await interaction.response.send_message("❌ Nenhuma troca ativa.", ephemeral=True)

        if not troca["recebedor"] or interaction.user.id != troca["recebedor"].id:
            return await interaction.response.send_message("❌ Só quem clicou em RECEBER pode informar o item.", ephemeral=True)

        troca["item"] = str(self.item).strip()
        troca["confirm_enviador"] = False
        troca["confirm_recebedor"] = False

        await interaction.response.send_message("✅ Item definido.", ephemeral=True)
        await atualizar_painel_ec(interaction.channel)

class ECView(View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Enviar", style=discord.ButtonStyle.green)
    async def enviar(self, interaction: discord.Interaction, button: Button):

        troca = trocas.get(interaction.channel.id)

        if not troca:
            return await interaction.response.send_message("❌ Nenhuma troca ativa.", ephemeral=True)

        permitidos = [troca["membro1"].id, troca["membro2"].id]

        if interaction.user.id not in permitidos:
            return await interaction.response.send_message("❌ Você não participa dessa troca.", ephemeral=True)

        if troca["enviador"] is not None:
            return await interaction.response.send_message("❌ Já existe um enviador.", ephemeral=True)

        if troca["recebedor"] and interaction.user.id == troca["recebedor"].id:
            return await interaction.response.send_message("❌ Você já escolheu RECEBER.", ephemeral=True)

        troca["enviador"] = interaction.user

        await interaction.response.send_message("✅ Você escolheu ENVIAR.", ephemeral=True)
        await atualizar_painel_ec(interaction.channel)

    @discord.ui.button(label="Receber", style=discord.ButtonStyle.blurple)
    async def receber(self, interaction: discord.Interaction, button: Button):

        troca = trocas.get(interaction.channel.id)

        if not troca:
            return await interaction.response.send_message("❌ Nenhuma troca ativa.", ephemeral=True)

        permitidos = [troca["membro1"].id, troca["membro2"].id]

        if interaction.user.id not in permitidos:
            return await interaction.response.send_message("❌ Você não participa dessa troca.", ephemeral=True)

        if troca["recebedor"] is not None:
            return await interaction.response.send_message("❌ Já existe um recebedor.", ephemeral=True)

        if troca["enviador"] and interaction.user.id == troca["enviador"].id:
            return await interaction.response.send_message("❌ Você já escolheu ENVIAR.", ephemeral=True)

        troca["recebedor"] = interaction.user

        await interaction.response.send_message("✅ Você escolheu RECEBER.", ephemeral=True)
        await atualizar_painel_ec(interaction.channel)

    @discord.ui.button(label="Informar Valor", style=discord.ButtonStyle.green)
    async def informar_valor(self, interaction: discord.Interaction, button: Button):

        troca = trocas.get(interaction.channel.id)

        if not troca or not troca["enviador"]:
            return await interaction.response.send_message("❌ Primeiro escolha quem vai ENVIAR.", ephemeral=True)

        if interaction.user.id != troca["enviador"].id:
            return await interaction.response.send_message("❌ Só o enviador pode informar o valor.", ephemeral=True)

        await interaction.response.send_modal(ValorModal())

    @discord.ui.button(label="Informar Item", style=discord.ButtonStyle.blurple)
    async def informar_item(self, interaction: discord.Interaction, button: Button):

        troca = trocas.get(interaction.channel.id)

        if not troca or not troca["recebedor"]:
            return await interaction.response.send_message("❌ Primeiro escolha quem vai RECEBER.", ephemeral=True)

        if interaction.user.id != troca["recebedor"].id:
            return await interaction.response.send_message("❌ Só o recebedor pode informar o item.", ephemeral=True)

        await interaction.response.send_modal(ItemModal())

    @discord.ui.button(label="Confirmar", style=discord.ButtonStyle.gray)
    async def confirmar_btn(self, interaction: discord.Interaction, button: Button):

        troca = trocas.get(interaction.channel.id)

        if not troca:
            return await interaction.response.send_message("❌ Nenhuma troca ativa.", ephemeral=True)

        if not troca["enviador"] or not troca["recebedor"]:
            return await interaction.response.send_message("❌ Falta escolher Enviar/Receber.", ephemeral=True)

        if troca["valor"] is None:
            return await interaction.response.send_message("❌ Falta informar o valor.", ephemeral=True)

        if not troca["item"]:
            return await interaction.response.send_message("❌ Falta informar o item.", ephemeral=True)

        if interaction.user.id == troca["enviador"].id:
            troca["confirm_enviador"] = True
            await interaction.response.send_message("✅ Enviador confirmou.", ephemeral=True)

        elif interaction.user.id == troca["recebedor"].id:
            troca["confirm_recebedor"] = True
            await interaction.response.send_message("✅ Recebedor confirmou.", ephemeral=True)

        else:
            return await interaction.response.send_message("❌ Você não participa dessa troca.", ephemeral=True)

        if troca["confirm_enviador"] and troca["confirm_recebedor"]:
            await finalizar_ec(interaction.channel)
        else:
            await atualizar_painel_ec(interaction.channel)

async def finalizar_ec(channel):

    troca = trocas.get(channel.id)

    if not troca:
        return

    valor = troca["valor"]
    item = troca["item"]

    mm = 1.00
    gateway = 0.20

    total = valor + mm + gateway

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

    try:
        await channel.purge(limit=100)
    except:
        pass

    await channel.send(embed=embed, view=view)

    trocas.pop(channel.id, None)

@bot.command()
async def ec(ctx, membro1: discord.Member, membro2: discord.Member):

    trocas[ctx.channel.id] = {
        "membro1": membro1,
        "membro2": membro2,
        "enviador": None,
        "recebedor": None,
        "valor": None,
        "item": None,
        "confirm_enviador": False,
        "confirm_recebedor": False,
        "mensagem_id": None
    }

    embed = criar_embed_ec(ctx.channel.id)

    msg = await ctx.send(
        embed=embed,
        view=ECView()
    )

    trocas[ctx.channel.id]["mensagem_id"] = msg.id

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
