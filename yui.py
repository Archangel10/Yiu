import discord
import asyncio
import random
import os
import config
from discord.ext import commands
from discord.utils import get
from discord import utils


#Global
client = commands.Bot(command_prefix = config.prefix)
client.remove_command( 'help' )

@client.event
async def on_ready():
    client.loop.create_task(rainbowrole(config.rainbowrolename))
    print( 'Yui запущена' )  
    await client.change_presence( status = discord.Status.online, activity = discord.Game('>help') )

@client.event
async def on_command_error( ctx , error ):
    pass

# Clear
@client.command()
@commands.has_permissions( administrator = True )
async def clear( ctx, amount : int ):
    await ctx.channel.purge( limit = amount )
    emb = discord.Embed( title = f'Удаляет {amount} собщений ', colour = discord.Color.purple() )
    emb.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url )
    
    await ctx.send( embed = emb )

# Kick
@client.command()
@commands.has_permissions( administrator = True )
async def kick( ctx,member: discord.Member, *, reason = None ):
    emb = discord.Embed( title = 'Изгнан администратором', colour = discord.Color.purple() )
    await ctx.channel.purge( limit = 1 )
    await member.kick( reason = reason )

    emb.set_author( name = member.name, icon_url = member.avatar_url )
    emb.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url )

    channel = client.get_channel(config.channelid)
    await channel.send(  embed = emb )

# Ban
@client.command()
@commands.has_permissions( administrator = True )

async def ban( ctx,member: discord.Member, *, reason = None ):
    emb = discord.Embed( title = 'Заблокирован администратором', colour = discord.Color.purple() )
    await ctx.channel.purge( limit = 1 )
    await member.ban( reason = reason )

    emb.set_author( name = member.name, icon_url = member.avatar_url )
    emb.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url )


    channel = client.get_channel(config.channelid)
    await channel.send( embed = emb )

# UnBan
@client.command()
@commands.has_permissions( administrator = True )

async def unban( ctx, *, member ):
    emb = discord.Embed( title = 'Розблоктрван администратором', colour = discord.Color.purple() )
    await ctx.channel.purge(limit = 1 )
    
    banned_users = await ctx.guild.bans()

    for ban_entry in banned_users:
        user = ban_entry.user

        await ctx.guild.unban( user )

        emb.set_author( name = user.name, icon_url = user.avatar_url )
        emb.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url )

        channel = client.get_channel(config.channelid)
        await channel.send( embed = emb )

# Mute
@client.command()
@commands.has_permissions( administrator = True )
async def mute( ctx, member: discord.Member ):
    emb = discord.Embed( title = 'Вам запрещено писать в чат администратором', colour = discord.Color.purple() )
    await ctx.channel.purge( limit = 1 )

    mute_role = discord.utils.get( ctx.message.guild.roles, id = config.muteroleid)

    await member.add_roles( mute_role )
    channel = client.get_channel(config.channelid)

    emb.set_author( name = member.name, icon_url = member.avatar_url )
    emb.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url )

    await channel.send( embed = emb )

# UnMute
@client.command()
@commands.has_permissions( administrator = True )
async def unmute( ctx, member: discord.Member ):
    emb = discord.Embed( title = 'Вам разрешено писать в чат администратором', colour = discord.Color.purple() )
    await ctx.channel.purge( limit = 1 )

    mute_role = discord.utils.get( ctx.message.guild.roles, id = config.muteroleid)

    await member.remove_roles( mute_role )
    channel = client.get_channel(config.channelid)

    emb.set_author( name = member.name, icon_url = member.avatar_url )
    emb.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url )

    await channel.send( embed = emb )

# VimeWorld
@client.command()
async def skin( ctx, arg ):
    await ctx.channel.purge( limit = 1 )
    skin = config.code1 + arg + config.code2
    
    emb = discord.Embed( title = 'Вот твой скин', colour = discord.Color.purple(), url = skin )
    emb.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url )
    emb.set_image( url = skin)

    await ctx.send( embed = emb )

@client.command()
async def cloak( ctx, arg ):
    await ctx.channel.purge( limit = 1 )
    cloak = config.code3 + arg + config.code2
    
    emb = discord.Embed( title = 'Вот твой плащ', colour = discord.Color.purple(), url = cloak  )
    emb.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url )
    emb.set_image( url = cloak)

    await ctx.send( embed = emb )

# Help
@client.command()
async def help( ctx ):
    emb = discord.Embed( title = 'Навигацыя по командам', colour = discord.Color.purple() )
    await ctx.channel.purge(limit = 1 )
    
    emb.add_field( name = '{}clear'.format( config.prefix ), value = 'Очистка чата' )
    emb.add_field( name = '{}kick'.format( config.prefix ), value = 'Удалить игрока' )
    emb.add_field( name = '{}ban'.format( config.prefix ), value = 'Заблокировать игрока' )
    emb.add_field( name = '{}unban'.format( config.prefix ), value = 'Розблокировать игрока' )
    emb.add_field( name = '{}mute'.format( config.prefix ), value = 'Запретить писать в чат игроку' )
    emb.add_field( name = '{}unmute'.format( config.prefix ), value = 'Розрешыть писать в чат игроку' )
    emb.add_field( name = '{}skin'.format( config.prefix ), value = 'Узнать скин по нику' )
    emb.add_field( name = '{}cloak'.format( config.prefix ), value = 'Узнать плащ по нику' )

    await ctx.send( embed = emb )

# Error command
@clear.error 
async def clear_error( ctx, error ):
    if isinstance( error, commands.MissingRequiredArgument ):
        await ctx.channel.purge( limit = 1 )
        emb = discord.Embed(title = 'Обязательно укажыте количество удаляемых сообщений!  ' , colour = discord.Color.purple() )
        emb.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url )
        await ctx.send( embed = emb )
        
    if isinstance( error, commands.MissingPermissions ):
        await ctx.channel.purge( limit = 1 )
        emb = discord.Embed(title = ' У вас недостаточно прав \nна использование команды clear! ' , colour = discord.Color.purple() )
        emb.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url )
        await ctx.send( embed = emb )

@kick.error
async def kick_error( ctx, error ):
    if isinstance( error, commands.MissingRequiredArgument ):
        await ctx.channel.purge( limit = 1 )
        emb = discord.Embed(title = ' Обязательно укажыте кого хотите изгнать!  ' , colour = discord.Color.purple() )
        emb.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url )
        await ctx.send( embed = emb )
        
    if isinstance( error, commands.MissingPermissions ):
        await ctx.channel.purge( limit = 1 )
        emb = discord.Embed(title = ' У вас недостаточно прав \nна использование команды kick! ' , colour = discord.Color.purple() )
        emb.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url )
        await ctx.send( embed = emb )

@ban.error
async def ban_error( ctx, error ):
    if isinstance( error, commands.MissingRequiredArgument ):
        await ctx.channel.purge( limit = 1 )
        emb = discord.Embed(title = ' Обязательно укажыте кого хотите заблокировать!  ' , colour = discord.Color.purple() )
        emb.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url )
        await ctx.send( embed = emb )
        
    if isinstance( error, commands.MissingPermissions ):
        await ctx.channel.purge( limit = 1 )
        emb = discord.Embed(title = ' У вас недостаточно прав \nна использование команды ban! ' , colour = discord.Color.purple() )
        emb.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url )
        await ctx.send( embed = emb )

@unban.error
async def unban_error( ctx, error ):
    if isinstance( error, commands.MissingRequiredArgument ):
        await ctx.channel.purge( limit = 1 )
        emb = discord.Embed(title = ' Обязательно укажыте кого хотите розблокировать!  ' , colour = discord.Color.purple() )
        emb.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url )
        await ctx.send( embed = emb )
        
    if isinstance( error, commands.MissingPermissions ):
        await ctx.channel.purge( limit = 1 )
        emb = discord.Embed(title = ' У вас недостаточно прав \nна использование команды unban! ' , colour = discord.Color.purple() )
        emb.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url )
        await ctx.send( embed = emb )

@mute.error
async def mute_error( ctx, error ):
    if isinstance( error, commands.MissingRequiredArgument ):
        await ctx.channel.purge( limit = 1 )
        emb = discord.Embed(title = ' Обязательно укажыте кому хотите запретить писать!  ' , colour = discord.Color.purple() )
        emb.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url )
        await ctx.send( embed = emb )
        
    if isinstance( error, commands.MissingPermissions ):
        await ctx.channel.purge( limit = 1 )
        emb = discord.Embed(title = ' У вас недостаточно прав \nна использование команды mute! ' , colour = discord.Color.purple() )
        emb.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url )
        await ctx.send( embed = emb )

@unmute.error
async def unmute_error( ctx, error ):
    if isinstance( error, commands.MissingRequiredArgument ):
        await ctx.channel.purge( limit = 1 )
        emb = discord.Embed(title = ' Обязательно укажыте кому хотите разрешыть писать!  ' , colour = discord.Color.purple() )
        emb.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url )
        await ctx.send( embed = emb )
        
    if isinstance( error, commands.MissingPermissions ):
        await ctx.channel.purge( limit = 1 )
        emb = discord.Embed(title = ' У вас недостаточно прав \nна использование команды unmute! ' , colour = discord.Color.purple() )
        emb.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url )
        await ctx.send( embed = emb )

# Words # Filter
@client.event

async def on_message( message ):
    await client.process_commands( message )
    msg = message.content.lower()  

    if msg in config.hello_words:
        await message.channel.send(config.hello_words_msg)
    
    if msg in config.answer_words:
        await message.channel.send(config.answer_words_msg)

    if msg in config.goodbye_words:
        await message.channel.send(config.goodbye_words_msg)

    if msg in config.bad_words:
        await message.delete()
        await message.author.send(f' { message.author.name } ' + config.bad_words_msg)

# Rainbow role
colourse = [discord.Color.dark_orange(),discord.Color.orange(),discord.Color.dark_gold(),discord.Color.gold(),discord.Color.dark_magenta(),discord.Color.magenta(),discord.Color.red(),discord.Color.dark_red(),discord.Color.blue(),discord.Color.dark_blue(),discord.Color.teal(),discord.Color.dark_teal(),discord.Color.green(),discord.Color.dark_green(),discord.Color.purple(),discord.Color.dark_purple()]
@client.event
async def rainbowrole(role):
    for role in client.get_guild(config.serverid).roles:
        if str(role) == str(config.rainbowrolename):
            print("detected role")
            while not client.is_closed():
                try:
                    await role.edit(color=random.choice(colourse))
                except Exception:
                    print("can't edit role, make sure the bot role is above the rainbow role and that is have the perms to edit roles")
                    pass
                await asyncio.sleep(config.delay)
    print('role with the name "' + config.rainbowrolename +'" not found')
    print("creating the role...")
    try:
        await client.get_guild(config.serverid).create_role(reason="Created rainbow role", name=config.rainbowrolename)
        print("role created!")
        await asyncio.sleep(2)
        client.loop.create_task(rainbowrole(config.rainbowrolename))
    except Exception as e:
        print("couldn't create the role. Make sure the bot have the perms to edit roles")
        print(e)
        pass
        await asyncio.sleep(10)
        client.loop.create_task(rainbowrole(config.rainbowrolename))

# Auto role
@client.event
async def on_member_join( member ):
    emb = discord.Embed( title = 'Добро пожаловать на наш сервер', colour = discord.Color.purple() )
    
    channel = client.get_channel(config.channelid)
    
    role = discord.utils.get( member.guild.roles, id = config.newplayerroleid )

    await member.add_roles( role )

    emb.set_author( name = member.name, icon_url = member.avatar_url )

    await channel.send( embed = emb )

# Color role
@client.event
async def on_raw_reaction_add(self, payload):
	if payload.message_id == config.POST_ID:
		channel = self.get_channel(payload.channel_id) # получаем объект канала
		message = await channel.fetch_message(payload.message_id) # получаем объект сообщения
		member = utils.get(message.guild.members, id=payload.user_id) # получаем объект пользователя который поставил реакцию

		try:
			emoji = str(payload.emoji) # эмоджик который выбрал юзер
			role = utils.get(message.guild.roles, id=config.ROLES[emoji]) # объект выбранной роли (если есть)
			
			if(len([i for i in member.roles if i.id not in config.EXCROLES]) <= config.MAX_ROLES_PER_USER):
				await member.add_roles(role)
				print('[SUCCESS] User {0.display_name} has been granted with role {1.name}'.format(member, role))
			else:
				await message.remove_reaction(payload.emoji, member)
				print('[ERROR] Too many roles for user {0.display_name}'.format(member))
			
		except KeyError as e:
				print('[ERROR] KeyError, no role found for ' + emoji)
		except Exception as e:
				print(repr(e))

async def on_raw_reaction_remove(self, payload):
	channel = self.get_channel(payload.channel_id) # получаем объект канала
	message = await channel.fetch_message(payload.message_id) # получаем объект сообщения
	member = utils.get(message.guild.members, id=payload.user_id) # получаем объект пользователя который поставил реакцию

	try:
		emoji = str(payload.emoji) # эмоджик который выбрал юзер
		role = utils.get(message.guild.roles, id=config.ROLES[emoji]) # объект выбранной роли (если есть)

		await member.remove_roles(role)
		print('[SUCCESS] Role {1.name} has been remove for user {0.display_name}'.format(member, role))

	except KeyError as e:
		print('[ERROR] KeyError, no role found for ' + emoji)
	except Exception as e:
		print(repr(e))


























#Connect
client.run(config.token)
