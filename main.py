import os
import requests
import discord
import time
from discord.ext import commands
import asyncio
import json
import subprocess

global student
global PRESENT
global ABSENT
global TIMESLEEP
global picture

# OUBLIE PAS DE MODIFIER LE CHANNEL ID

API_UID = "UID" # UID SERVER
API_SECRET = "SECRET" # SECRET SERVER

PRESENT = True
ABSENT = False
NEW = "ADD"

API_URL = "https://api.intra.42.fr"

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = commands.Bot(command_prefix='/', intents=intents)

def get_api_token():
	response = requests.post(f"{API_URL}/oauth/token",
		data={
			"grant_type": "client_credentials",
			"client_id": API_UID,
			"client_secret": API_SECRET,
		}
	)
	if response.status_code == 200:
		return response.json()["access_token"]
	else:
		raise Exception("Impossible de récupérer le token d'accès à l'API")

def get_student_locations(user_id):
	headers = {"Authorization": f"Bearer {get_api_token()}"}
	response = requests.get(f"{API_URL}/v2/users/{user_id}/locations", headers=headers)
	if response.status_code == 200:
		return response.json()
	else:
		return None

def load_student_json():
	global student
	global picture

	with open('students.json', 'r') as file:
		data = json.load(file)
	student = data['student']
	for stud, presence in student.items():
		student[stud] = ABSENT
	picture = data['picture']

@client.command()
async def presence(ctx):
	count = 0
	for stud, presence in student.items():
		if presence == PRESENT:
			count += 1
	embed = discord.Embed(title="Presence :", description=f"**{count}** humain(s) connectés", color=0x00FF00)
	for stud, presence in student.items():
		if presence == PRESENT:
			embed.add_field(name="✅", value=stud, inline=True)
	await ctx.send(embed=embed)

@client.command()
async def addpresence(ctx, login = None):
	if login is None:
		embed = discord.Embed(title="Ajout de présence", description="❌ Merci de fournir un login", color=0xFF0000)
		return await ctx.send(embed=embed)
	login = login.lower().replace(" ", "").replace("\n", "")
	
	location = get_student_locations(login)
	if location:
		student[login] = NEW
		with open('students.json', 'w') as file:
			data = {stud: ABSENT for stud in student}
			json.dump({"student": data, "picture": picture}, file, indent=4)
		
		embed = discord.Embed(title="Ajout de présence", description=f"✅ **{login}** est maintenant ajouté à la liste des humain(s) à vérifier", color=0x00FF00)
		return await ctx.send(embed=embed)
	else:
		embed = discord.Embed(title="Ajout de présence", description=f"❌ **{login}** n'est pas un étudiant de 42", color=0xFF0000)
		return await ctx.send(embed=embed)

@client.command()
async def removepresence(ctx, login=None):
	global student
	global picture
	if login is None:
		embed = discord.Embed(title="Suppression de présence", description="❌ Merci de fournir un login", color=0xFF0000)
		return await ctx.send(embed=embed)
	login = login.lower().replace(" ", "").replace("\n", "")
	if login in student:
		del student[login]
		with open('students.json', 'w') as file:
			data = {stud: ABSENT for stud in student}
			json.dump({"student": data, "picture": picture}, file, indent=4)
		embed = discord.Embed(title="Suppression de présence", description=f"✅ **{login}** a été supprimé de la liste des humain(s) à vérifier", color=0x00FF00)
		await ctx.send(embed=embed)
	else:
		embed = discord.Embed(title="Suppression de présence", description=f"❌ **{login}** n'est pas dans la liste des humain(s) à vérifier", color=0xFF0000)
		await ctx.send(embed=embed)

@client.command()
async def addpicture(ctx, login=None, url=None):
	global picture
	global student
	if ctx.author.id != AUTHOR_ID_DISCORD:
		embed = discord.Embed(title="Ajout de photo", description="❌ Vous n'avez pas la permission", color=0xFF0000)
		return await ctx.send(embed=embed)
	
	if login is None or url is None:
		embed = discord.Embed(title="Ajout de photo", description="❌ Merci de fournir un login et une url", color=0xFF0000)
		return await ctx.send(embed=embed)
	
	login = login.lower().replace(" ", "").replace("\n", "")
	for stud, presence in student.items():
		if stud == login:
			picture[login] = url
			with open('students.json', 'w') as file:
				data = {stud: ABSENT for stud in student}
				json.dump({"student": data, "picture": picture}, file, indent=4)
	if login in student:
		embed = discord.Embed(title="Ajout de photo", description=f"✅ **{login}** a été ajouté à la liste des photos", color=0x00FF00)
		await ctx.send(embed=embed)
	else:
		embed = discord.Embed(title="Ajout de photo", description=f"❌ **{login}** n'est pas dans la liste des humain(s) à vérifier", color=0xFF0000)
		await ctx.send(embed=embed)

@client.command()
async def removepicture(ctx, login=None):
	global picture
	global student
	if ctx.author.id != AUTHOR_ID_DISCORD:
		embed = discord.Embed(title="Suppression de photo", description="❌ Vous n'avez pas la permission", color=0xFF0000)
		return await ctx.send(embed=embed)
	
	if login is None:
		embed = discord.Embed(title="Suppression de photo", description="❌ Merci de fournir un login", color=0xFF0000)
		return await ctx.send(embed=embed)
	
	login = login.lower().replace(" ", "").replace("\n", "")
	if login in picture:
		del picture[login]
		with open('students.json', 'w') as file:
			data = {stud: ABSENT for stud in student}
			json.dump({"student": data, "picture": picture}, file, indent=4)
		embed = discord.Embed(title="Suppression de photo", description=f"✅ **{login}** a été supprimé de la liste des photos", color=0x00FF00)
		await ctx.send(embed=embed)
	else:
		embed = discord.Embed(title="Suppression de photo", description=f"❌ **{login}** n'est pas dans la liste des photos", color=0xFF0000)
		await ctx.send(embed=embed)

@client.command()
async def liste(ctx):
	global student
	embed = discord.Embed(title="Liste des etudiants", description="Voici la liste des humain(s) à vérifier", color=0x00FF00)
	for stud, presence in student.items():
		embed.add_field(name="ℹ️", value=stud, inline=True)
	await ctx.send(embed=embed)

@client.command()
async def receivejsonpresence(ctx):
	await ctx.send(file=discord.File('students.json'))

@client.command()
async def setsleeptime(ctx, time = None):
	global TIMESLEEP
	if ctx.author.id != AUTHOR_ID_DISCORD:
		embed = discord.Embed(title="Nouveau wait time 🕐", description=f"❌ Vous n'avez pas la permission", color=0xFF0000)
		return await ctx.send(embed=embed)
	if time != None and time.isdigit() and int(time) > 0:
		TIMESLEEP = int(time)
		embed = discord.Embed(title="Nouveau wait time 🕐", description=f"✅ Nouveau wait time : {time}\n ℹ️ Wait time actuel : {TIMESLEEP}", color=0x00FF00)
		return await ctx.send(embed=embed)
	else:
		embed = discord.Embed(title="Nouveau wait time 🕐", description=f"❌ Merci de founir un time valide\n ℹ️ Wait time actuel : {TIMESLEEP}", color=0xFF0000)
		return await ctx.send(embed=embed)

@client.command()
async def restartpresence(ctx):
	if ctx.author.id != AUTHOR_ID_DISCORD:
		embed = discord.Embed(title="Restart 🔄", description="❌ Vous n'avez pas la permission", color=0xFF0000)
		return await ctx.send(embed=embed)

	embed = discord.Embed(title="Restart 🔄", description="✅ Restart du bot", color=0x00FF00)
	await ctx.send(embed=embed)
	subprocess.Popen(["python3", "main.py"])
	await client.close()

@client.command()
async def helppresence(ctx):
	embed = discord.Embed(title="Liste de commande :", description="Voici la liste des commandes", color=0x00FF00)
	embed.add_field(name="/presence", value="Affiche la liste des humain(s) présentes", inline=False)
	embed.add_field(name="/addpresence", value="Ajoute une personne à la liste des humain(s) à vérifier", inline=False)
	embed.add_field(name="/removepresence", value="Supprime une personne de la liste des humain(s) à vérifier", inline=False)
	embed.add_field(name="/liste", value="Affiche la liste des humain(s) à vérifier", inline=False)
	embed.add_field(name="/setsleeptime", value="Change le temps d'attente entre chaque vérification **| Admin |**", inline=False)
	embed.add_field(name="/restartpresence", value="Redémarre le bot **| Admin |**", inline=False)
	embed.add_field(name="/helppresence", value="Affiche la liste des commandes", inline=False)
	embed.add_field(name="/addpicture", value="Ajoute une photo à un étudiant **| Admin |**", inline=False)
	embed.add_field(name="/removepicture", value="Supprime une photo d'un étudiant **| Admin |**", inline=False)
	embed.add_field(name="/receivejsonpresence", value="Reçoit le fichier json", inline=False)
	embed.add_field(name="/announce", value="Envoie un message dans le channel **| Admin |**", inline=False)
	await ctx.reply(embed=embed)

@client.command()
async def announce(ctx, str):
	if ctx.author.id != AUTHOR_ID_DISCORD:
		embed = discord.Embed(title="Annonce", description="❌ Vous n'avez pas la permission", color=0xFF0000)
		return await ctx.send(embed=embed)
	channel = client.get_channel(TON_CHANNEL_ID)
	embed = discord.Embed(title="Annonce", description=f"📢 **{str}**", color=0x00FF00)
	return await channel.send(embed=embed)
	
@client.event
async def on_ready():
    print(f"Bot connecté en tant que {client.user}")
    embed = discord.Embed(
        title="Bot 42Presence",
        description="✅ Bot connecté",
        color=0x00FF00
    )
    channel = client.get_channel(TON_CHANNEL_ID)
    await channel.send(embed=embed)

    global student
    global picture
    global TIMESLEEP
    TIMESLEEP = 90
    load_student_json()
    first_fill = True
    first_time = True
    mounir_check = False

    for stud, presence in student.items():
        location = get_student_locations(stud)
        if location:
            location = location[0]
            location_host = location["host"]
            location_end_at = location["end_at"]
            if location_end_at is None:
                student[stud] = PRESENT
            else:
                student[stud] = ABSENT
        await asyncio.sleep(0.6)

    embed = discord.Embed(
        title="Bot 42Presence",
        description="✅ Aucune erreur le bot a bien demmaré",
        color=0x00FF00
    )
    channel = client.get_channel(TON_CHANNEL_ID)
    await channel.send(embed=embed)

    while True:
        for login in student:
            locations = get_student_locations(login)
            if locations:
                location = locations[0]
                location_host = location["host"]
                location_end_at = location["end_at"]

                for stud, presence in student.items():
                    if presence == PRESENT and stud == login and location_end_at is not None:
                        student[login] = ABSENT
                        if not first_fill:
                            channel = client.get_channel(TON_CHANNEL_ID)
                            embed = discord.Embed(
                                title="Il/Elle est enfin parti ...",
                                description=f"❌ **{login}** est parti, Son poste était à **{location_host}**",
                                color=0xFF0000
                            )
                            if stud in picture:
                                embed.set_thumbnail(url=picture[stud])
                            await channel.send(embed=embed)

                for stud, presence in student.items():
                    if presence == ABSENT and stud == login and location_end_at is None:
                        student[login] = PRESENT
                        channel = client.get_channel(TON_CHANNEL_ID)
                        embed = discord.Embed(
                            title="Il/Elle est enfin venu ...",
                            description=f"✅ **{login}** est arrivé, Son poste est à **{location_host}**",
                            color=0x00FF00
                        )
                        for stud, presence in picture.items():
                            if stud == login:
                                embed.set_thumbnail(url=picture[stud])
                        await channel.send(embed=embed)
        first_fill = False
        await asyncio.sleep(TIMESLEEP)

client.run("BOT_ID") # FOR SERVER
