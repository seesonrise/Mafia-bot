import asyncio
import disnake
import random
from collections import Counter


async def game(bot, channel: disnake.TextChannel, player: list):
    global guild, civilian, mafia, detective, doctor, vote1
    global civilianwon, mafiawon, ended
    civilianwon = False
    mafiawon = False
    ended = False
    guild = bot.get_guild(1080929023842074684)
    tempcivilian = []
    civilian = player
    mafia = random.choice(player)
    civilian.remove(mafia)
    detective = random.choice(civilian)
    tempcivilian += civilian
    tempcivilian.remove(detective)
    doctor = random.choice(tempcivilian)
    print(f"Mafia: {mafia.name}")
    print(f"Doctor: {doctor.name}")
    print(f"Detective: {detective.name}")
    print(f'Civilians: {civilian}')
    for i in range(5):
        a = await channel.send('@here')
        await asyncio.sleep(2)
        await a.delete()
    await channel.send(embed=disnake.Embed(description=f'``Правила игры:``\n1. Детективу запрещено всяческими другимим способами доказывать что человек мафия, только текстом.\n2. Запрещено сливать роли в личных сообщениях.'))
    intermission = await channel.send(embed=disnake.Embed(description=f'**Начало через 30 секунд**'))
    await asyncio.sleep(30)
    await intermission.delete()
    role_choise = await channel.send(embed=disnake.Embed(description=f'Выбор ролей.'))
    await asyncio.sleep(3)
    await role_choise.edit(embed=disnake.Embed(description=f'Выбор ролей..'))
    await asyncio.sleep(3)
    await role_choise.edit(embed=disnake.Embed(description=f'Выбор ролей...'))
    await mafia.send(embed=disnake.Embed(
        description=f'**Ваша роль Мафия** \n**Ваша задача убить всех мирных жителей**\n'
                    f'**Что-бы победить вам надо сократить количество мирных жителей до двух**'))
    await doctor.send(embed=disnake.Embed(
        description=f'**Ваша роль Доктор** \n**Вы можете вылечить любого человека**\n'
                    f'**Либо себя, что-бы уберечь от смерти **'))
    for member in civilian:
        if member == doctor or member == detective:
            pass
        else:
            await member.send(embed=disnake.Embed(
                description=f'**Ваша роль Мирный житель** \n**Ваша задача выжить и не умереть**'
                            f' \n**Вы должны делать верные выборы на головании **'))
            await asyncio.sleep(0.5)    
    await asyncio.sleep(3)
    await role_choise.delete()
    await channel.send(embed=disnake.Embed(description=f'Наступает ночь \nГород засыпает \nПросыпаеться мафия'))
    await asyncio.sleep(2)
    while True:
        if ended:
            break
        await play_cylce(bot, channel)
    if civilianwon:
        if detective:
            victory = guild.get_member(int(detective.id))
            await channel.send(embed=disnake.Embed(
                description=f'Игра закончена, победа за мирными жителями и детективом ' + victory.mention))
        else:
            await channel.send(embed=disnake.Embed(description=f'Игра закончена, победа за мирными жителями'))
    if mafiawon:
        victory = guild.get_member(int(mafia.id))
        await channel.send(embed=disnake.Embed(description=f'Игра закончена, победа за мафией ' + victory.mention))
    await asyncio.sleep(15)
    await channel.delete()


async def play_cylce(client, channel):
    global guild, civilian, mafia, detective, tempmember, doctor, detective_message, doctor_message, lived, cured_player, tempmember2, vote1, doctorplayers
    global civilianwon, mafiawon, ended
    cured_player = ''
    doctorplayers = []
    detective_message = True
    doctor_message = True
    lived = False
    await channel.send(embed=disnake.Embed(description=f'Мафия делает свой выбор'))
    number_to_id = {}
    templist = []
    templist += civilian
    templist.append(mafia)
    players = ''
    random.shuffle(civilian)
    for index, member in enumerate(civilian):
        number = index + 1
        number_to_id[number] = member.id
    print(number_to_id)
    for number, member in number_to_id.items():
        tempmember2 = guild.get_member(member)
        players += f'`Номер: {number}, Имя: {tempmember2.display_name}`\n'
    await mafia.send(embed=disnake.Embed(description=f'**Сделай выбор (отправь номер)**\n' + players))

    def check(m):
        return mafia == m.author
    try:
        mafia_choise1 = await client.wait_for('message', check=check, timeout=30)
    except asyncio.TimeoutError:
        pass
    try:
        mafia_choise = int(mafia_choise1.content)
        tempmember = guild.get_member(number_to_id[mafia_choise])
    except:
        mafia_choise = None
    try:
        if number_to_id[mafia_choise] == mafia.id:
            await mafia.send(embed=disnake.Embed(description=f'**Вы неможете убить сами себя**\n'
                                                             f'**Из-за ваших жалких потугов вы пропускаете ход**'))
    except:
        pass
    await asyncio.sleep(4)
    await channel.send(
        embed=disnake.Embed(description=f'Мафия сделала свой выбор \nМафия засыпает \nПросыпается Доктор'))
    if doctor:
        number_to_id = {}
        players = ''
        random.shuffle(civilian)
        for index, member in enumerate(civilian):
            number = index + 1
            number_to_id[number] = member.id
        for number, member in number_to_id.items():
            tempmember2 = guild.get_member(member)
            players += f'`Номер: {number}, Имя: {tempmember2.display_name}`\n'
        await doctor.send(embed=disnake.Embed(description=f'**Сделай выбор (учитите вы можете лечить только разных игроков, одного лечить не получится) (отправь номер)**\n' + players))

        def check(m):
            return doctor == m.author
        try:
            doctor_choise1 = await client.wait_for('message', check=check, timeout=30)
        except asyncio.TimeoutError:
            pass
        try:
            doctor_choise = int(doctor_choise1.content)
            if str(number_to_id[doctor_choise]) not in doctorplayers:
                cured_player = number_to_id[doctor_choise]
                doctorplayers.append(str(cured_player))
                await doctor.send(embed=disnake.Embed(description="**Вы вылечили данного игрока**"))
            else:
                await doctor.send(embed=disnake.Embed(description="**Вы уже лечили данного игрока, лечение недоступно**"))
                try:
                    await doctor.send(embed=disnake.Embed(description=f'**Даем второй шанс (отправь номер)**\n' + players))
                    doctor_choise1 = await client.wait_for('message', check=check, timeout=30)
                except asyncio.TimeoutError:
                    pass
                doctor_choise = int(doctor_choise1.content)
                if str(number_to_id[doctor_choise]) not in doctorplayers:
                    cured_player = number_to_id[doctor_choise]
                    doctorplayers.append(str(cured_player))
                    await doctor.send(embed=disnake.Embed(description="**Вы вылечили данного игрока**"))
        except:
            doctor_choise = None

        if tempmember.id == cured_player:
            lived = True
        elif tempmember.id == doctor.id:
            doctor = None
            print('killed doctor')
            civilian.remove(tempmember)
        elif tempmember.id == detective.id:
            detective = None
            print('killed detective')
            civilian.remove(tempmember)
        else:
            print('killed')
            civilian.remove(tempmember)

    await asyncio.sleep(random.randint(0, 10))
    await channel.send(
        embed=disnake.Embed(description=f'Доктор сделал свой выбор \nДоктор засыпает \nПросыпается Детектив'))
    if detective:
        templist = []
        players = ''
        number_to_id = {}
        templist += civilian
        templist.append(mafia)
        random.shuffle(templist)
        for index, member in enumerate(templist):
            number = index + 1
            number_to_id[number] = member.id
        for number, member in number_to_id.items():
            tempmember2 = guild.get_member(member)
            players += f'`Номер: {number}, Имя: {tempmember2.display_name}`\n'
        templist.clear()
        await detective.send(
            embed=disnake.Embed(description=f'**Выберите кого вы хотите проверить (отправь номер)**\n' + players))

        def check(m):
            return detective == m.author
        try:
            detective_choise1 = await client.wait_for('message', check=check, timeout=30)
        except asyncio.TimeoutError:
            pass
        try:
            detective_choise = int(detective_choise1.content)
            detective_choise = number_to_id[detective_choise]
        except:
            detective_choise = None
        try:
            if int(detective_choise) == mafia.id:
                await detective.send(embed=disnake.Embed(
                    description=f"Данный игрок является мафией \nВаша задача убедить в этом других"))
            elif int(detective_choise) == doctor.id:
                await detective.send(embed=disnake.Embed(
                    description=f"Данный игрок является доктором"))
            else:
                await detective.send(embed=disnake.Embed(description="Данный игрок является мирным жителем"))
        except Exception as e:
            detective_choise = None
    await asyncio.sleep(random.randint(0,10))
    await channel.send(
        embed=disnake.Embed(description=f'Детектив сделал свой выбор \nДетектив засыпает'))
    await asyncio.sleep(2)
    await channel.send(embed=disnake.Embed(description="Наступает день"))
    for i in civilian:
        print(i.name)
    await asyncio.sleep(2)
    if tempmember:
        if not detective and detective_message:
            await channel.send(
                embed=disnake.Embed(description=f"Этой ночью был убит Детектив {tempmember.mention}"))
            detective_message = False
        elif not doctor and doctor_message:
            await channel.send(
                embed=disnake.Embed(description=f"Этой ночью был убит Доктор {tempmember.mention}"))
            doctor_message = False
        else:
            if lived:
                await channel.send(
                    embed=disnake.Embed(description=f"Этой ночью на {tempmember.mention} было совершенно покушение"
                                                    f"\nНо Доктор успел спасти его"))
                lived = False
                cured_player = None
            else:
                await channel.send(
                    embed=disnake.Embed(description=f"Этой ночью был убит мирный житель {tempmember.mention}"))
    cured_player = None
    print(civilian)
    if len(civilian) <= 1:
        await channel.send(embed=disnake.Embed(description="Остался последний мирный житель"))
        ended = True
        mafiawon = True
        return
    await channel.send(embed=disnake.Embed(description="Город просыпается и начинается время обсуждения"))
    await asyncio.sleep(2)
    await channel.send(embed=disnake.Embed(description="Время обсуждаения пошло, у вас 60 секунд"))
    templist1 = []
    templist1 += civilian
    templist1.append(mafia)
    for perm in templist1:
        await channel.set_permissions(perm, view_channel=True, send_messages=True)
    await asyncio.sleep(60)
    players = ''
    templist.clear()
    templist = []
    templist += civilian
    templist.append(mafia)
    number_to_id = {}
    random.shuffle(templist)
    for index, member in enumerate(templist):
        number = index + 1
        number_to_id[number] = member.id
    for number, member in number_to_id.items():
        tempmember2 = guild.get_member(member)
        players += f'`Номер: {number}, Имя: {tempmember2.display_name}`\n'
    await channel.send(embed=disnake.Embed(description="**Спиcок живых игроков: **\n" + players))
    print(templist, players)
    vote1 = []
    for j in templist:
        await channel.send(embed=disnake.Embed(description=f"{j.mention} делай свой выбор (отправь номер)"))
        def check(m):
            return j == m.author
        try:
            choice_vote = await client.wait_for('message', check=check, timeout=30)
            choice_vote = choice_vote.content
        except asyncio.TimeoutError:
            pass
        try:
            choice = int(choice_vote)
            vote1.append(str(number_to_id[choice]))
        except Exception as e:
            print(e)
            pass
    for perm in templist:
        await channel.set_permissions(perm, view_channel=True, send_messages=False)
    templist.clear()
    print(vote1)
    votelist = Counter(vote1)
    most_common_id = 0
    try:
        if votelist.most_common(2)[0][1] == votelist.most_common(2)[1][1]:
            await channel.send(embed=disnake.Embed(description=f"Игроки не сошлись во мнениях"))
            await asyncio.sleep(3)
            await channel.send(embed=disnake.Embed(description=f'Наступает ночь, \nГород засыпает, \nПросыпаеться мафия'))
            return
        else:
            most_common_id = votelist.most_common(1)[0][0]
    except:
        most_common_id = votelist.most_common(1)[0][0]
    print(most_common_id)
    mostcommonmember = guild.get_member(int(most_common_id))
    if mostcommonmember:
        await channel.send(embed=disnake.Embed(description=f'По итогам голосования выбывает: {mostcommonmember.mention}'))
    if mostcommonmember == mafia:
        await channel.send(embed=disnake.Embed(description=f"Данный игрок являлся мафией"))
        civilianwon = True
        ended = True
        return
    elif mostcommonmember == detective:
        await channel.send(embed=disnake.Embed(description=f"Данный игрок являлся детективом"))
        detective = None
        civilian.remove(mostcommonmember)
        return
    else:
        if mostcommonmember:
            await channel.send(embed=disnake.Embed(description=f"Данный игрок являлся мирным жителем"))
            civilian.remove(mostcommonmember)
            await channel.send(embed=disnake.Embed(description=f'Наступает ночь \nГород засыпает \nПросыпаеться мафия'))
            await asyncio.sleep(3)
            return
