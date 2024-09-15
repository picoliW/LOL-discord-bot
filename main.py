import discord
import os
from dotenv import load_dotenv
import asyncio
import random 
from utils.habilidades import habilidades
from utils.falas import falas
from utils.personagens import personagens

load_dotenv()

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in como {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('l!help'):
        await message.channel.send("Comandos disponíveis: l!fala, l!skill")


    if message.content.startswith('l!personagem'):
        personagem_aleatorio, info_aleatoria = random.choice(list(personagens.items()))

        await message.channel.send("Tente adivinhar o nome de um personagem!")

        tentativas = 7

        try:
            for attempt in range(tentativas):
                def check(m):
                    return m.author == message.author and m.channel == message.channel

                user_guess = await client.wait_for('message', check=check, timeout=120)

                personagem_usuario = user_guess.content.lower()

                if personagem_usuario == personagem_aleatorio:
                    await message.channel.send(f"Parabéns! Você acertou o personagem: **{personagem_aleatorio}**!")
                    return 

                elif personagem_usuario in personagens:
                    info_usuario = personagens[personagem_usuario]
                    
                    resposta = f"Sua tentativa: **{personagem_usuario}**\n"

                    todos_corretos = True
                    algum_correto = False
                    
                    for key in info_usuario:
                        usuario_value = info_usuario[key]
                        aleatorio_value = info_aleatoria[key]

                        if isinstance(usuario_value, list):
                            if any(v in aleatorio_value for v in usuario_value):
                                resposta += f"{key}: {', '.join(usuario_value)} 🟨\n"
                                algum_correto = True
                            else:
                                resposta += f"{key}: {', '.join(usuario_value)} ❌\n"
                                todos_corretos = False
                        else:
                            if usuario_value == aleatorio_value:
                                resposta += f"{key}: {usuario_value} ✅\n"
                            else:
                                resposta += f"{key}: {usuario_value} ❌\n"
                                todos_corretos = False
                            if usuario_value in aleatorio_value:
                                algum_correto = True

                    if todos_corretos:
                        await message.channel.send(f"Você acertou! Personagem: {resposta}")
                        return
                    elif algum_correto:
                        await message.channel.send(resposta)
                    else:
                        await message.channel.send(f"Você errou todas as informações! {resposta}")

                    remaining_attempts = tentativas - (attempt + 1)
                    if remaining_attempts > 0:
                        await message.channel.send(f"Tentativas restantes: {remaining_attempts}")
                    else:
                        await message.channel.send(f"Você usou todas as tentativas! O personagem correto era: **{personagem_aleatorio}**")
                        return

                else:
                    remaining_attempts = tentativas - (attempt + 1)
                    if remaining_attempts > 0:
                        await message.channel.send(f"Personagem não encontrado! Você tem mais {remaining_attempts} tentativa(s).")
                    else:
                        await message.channel.send(f"Você usou todas as tentativas! O personagem correto era: **{personagem_aleatorio}**")
                        return

        except asyncio.TimeoutError:
            await message.channel.send("Você demorou muito para responder!")
    
    if message.content.startswith('l!fala'):
        fala, autor = random.choice(list(falas.items()))

        await message.channel.send(f'De quem é essa fala? "{fala}"')

        attempts = 3

        try:
            for attempt in range(attempts):
                def check(m):
                    return m.author == message.author and m.channel == message.channel

                user_guess = await client.wait_for('message', check=check, timeout=30)

                if user_guess.content.lower() == autor.lower():
                    await message.channel.send("Parabéns! Você acertou!")
                    return  

                else:
                    remaining_attempts = attempts - (attempt + 1)
                    if remaining_attempts > 0:
                        await message.channel.send(f"Resposta errada! Você tem mais {remaining_attempts} tentativa(s).")
                    else:
                        await message.channel.send(f"Resposta errada! A resposta correta era: {autor}")

        except asyncio.TimeoutError:
            await message.channel.send("Você demorou muito para responder!")      

    if message.content.startswith('l!skill'):
        habilidade, info = random.choice(list(habilidades.items()))
        nome_habilidade = habilidade
        imagem_url = info["imagem"]
        personagem = info["personagem"]

        embed = discord.Embed(
            title="De qual campeão é esta habilidade? e qual é a tecla? EX - (ezreal q, swain e, jhin p)",
            description="Adivinhe o campeão e a habilidade!",
            color=discord.Color.blue()
        )
        embed.set_image(url=imagem_url)

        await message.channel.send(embed=embed)

        attempts = 3

        try:
            for attempt in range(attempts):
                def check(m):
                    return m.author == message.author and m.channel == message.channel

                user_guess = await client.wait_for('message', check=check, timeout=30)

                if user_guess.content.lower() == personagem.lower():
                    await message.channel.send("Parabéns! Você acertou!")
                    return
                else:
                    remaining_attempts = attempts - (attempt + 1)
                    if remaining_attempts == 2:
                        await message.channel.send(f"Resposta errada! Você tem mais {remaining_attempts} tentativa(s).")
                    elif remaining_attempts == 1:
                        await message.channel.send(f"Resposta errada! Você tem mais {remaining_attempts} tentativa,\n Nome da habilidade: {nome_habilidade}.")
                    else:
                        await message.channel.send(f"Resposta errada! A resposta correta era: {personagem}")
        
        except asyncio.TimeoutError:
            await message.channel.send("Você demorou muito para responder!")

client.run(os.getenv('TOKEN'))