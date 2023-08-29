import asyncio
import json
import datetime
import game
import logging

import disnake
from disnake.ext import commands
intents = disnake.Intents.all()
bot = commands.InteractionBot(
    test_guilds=[1137073750479732837],
    command_sync_flags=commands.CommandSyncFlags.default(),
    intents = intents
)

session = False
player = []
min_player = 4


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.slash_command(description="Начать сессию в мафию")
async def mafia(inter: disnake.ApplicationCommandInteraction, time_start: int):
    """
    Give several cookies to a user

    Parameters
    ----------
    time_start: :class:`int`
        Время до начала игры
    """
    global session
    guild = inter.guild
    if session:
        await inter.send(embed=disnake.Embed(description=f'**Игра уже началась**'))
        return
    player.append(inter.user)
    session = True
    channel = bot.get_channel(inter.channel.id)
    current_time = datetime.datetime.now().timestamp()
    new_time = int(current_time) + int(time_start)
    await inter.send('@here', embed=disnake.Embed(description=f'**Начало игры через <t:{new_time}:R>**\n``(Присоеденится /join)``\n`Количество участников: {len(player)}`'))
    for i in range(time_start):
        times = time_start - i
        await inter.edit_original_message(embed=disnake.Embed(description=f'**Начало игры через <t:{new_time}:R>**\n``(Присоеденится /join)``\n`Количество участников: {len(player)}`' if len(player) >= 4 else
                                              f'**Начало игры через <t:{new_time}:R>**\n``(Присоеденится /join)``\n`Количество участников: {len(player)}`\n``Для начала игры надо ещё {min_player - len(player)}``'))
        await asyncio.sleep(1)
    if len(player) < min_player:
        await inter.edit_original_message(embed=disnake.Embed(description=f'**Недостаточно игроков**'))
        logging.log(20, "Game don't start. Not enough player")
        session = False
        player.clear()
        return
    overwrite = {
        guild.default_role: disnake.PermissionOverwrite(view_channel=False)
    }
    current_time = datetime.datetime.now()
    time_stamp = current_time.timestamp()
    data_time = datetime.datetime.fromtimestamp(time_stamp)
    str_time = data_time.strftime("%HH-%MM-%SS")
    play_channel = await guild.create_text_channel(f"Игра {str_time}", overwrites=overwrite)
    for perm in player:
        await play_channel.set_permissions(perm, read_messages=True, view_channel=True, send_messages=False)
    await game.game(bot, play_channel, player=player)


@bot.slash_command(description="Присоедениться к игре")
@commands.cooldown(1, 3, commands.BucketType.user)
async def join(ctx: disnake.ApplicationCommandInteraction):
    global player, session
    if not session:
        await ctx.send(embed=disnake.Embed(description=f'``Игра не начата, для старта /mafia``'))
        return
    if ctx.user in player:
        await ctx.send(embed=disnake.Embed(description=f'``Вы уже присоеденились к игре``'))
        return
    player.append(ctx.user)
    await ctx.send(embed=disnake.Embed(description=f'``Вы успешно присоеденились``'))


@join.error
async def join_error(inter, exception):
    if exception == commands.CommandOnCooldown:
        await inter.send(f"Подождите ещё {exception.retry_after:.2f} секунд(ы) перед использованием команды")
    print(exception)


bot.run('')
