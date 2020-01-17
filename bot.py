from discord.ext import commands
import discord
import asyncio
import QCore as Q
import json
import configparser
import os

config = configparser.ConfigParser()
config.read('config.ini')
conf = config['QCore']


def enter(text):
    print(text)
    return input()


print(conf['Token'])
tOKEN = (conf['Token'] if conf['Token'] != "" else enter("Enter the Token: "))

print('OK...')


prefix = (conf['Prefix'] if conf['Prefix'] != "" else enter("Enter the Prefix: "))

print("The token is", tOKEN,"\nThe Prefix is {}".format(prefix))
bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix))


#####################################################################}
@bot.event
async def on_ready():
    await log('run QCore as [{0.user}] '.format(bot))
    gis = []
    for g in bot.guilds:
        gis.append(g.name)
    await log("I'm in {}".format(gis))


##################--VARS--#####################}
O = [475776964733566987, 438010452627292202, 520470342498779156]
log_ch = 652776939412652042
##################--EVARS--###{

player = {}
gulids = []
plmsgs = []
ng = {}
msg = {}
msgs = []
#############################--CONFIG--#############################
config = {}
try:
    with open(file="configs.json", mode="r", encoding='utf-8') as congs:
        config = json.load(congs)
except:
    pass


def congR():
    with open(file="configs.json", mode="w", encoding='utf-8') as congs:
        json.dump(config, congs)


######################################################################}


###########################/CLASS/###################################
class pager:
    def __init__(self, surah=None, page=None):
        try:
            if page is not None:
                self.Page = int(page)
            if surah is not None:
                NP = Q.QPage(surah).Surah
                self.FPage = NP.StartPage
                self.SName = NP.SurahName
                self.Page = int(self.FPage)
            self.url = Q.urlP(self.Page)
            Embed = discord.Embed(title='Page/' + str(self.Page), color=0xffffff)
            Embed.set_image(url=self.url)
            self.e = Embed
        except:
            self.Page = None


###########---VOICE---############
class reg:
    def __init__(self):
        pass

    def player(self, id, force=False):
        if (id not in player) or force:
            player[id] = {
                'url': None,
                'Sid': None,
                'shik': None,
                'author': None,
                'p': None,
                'pn': None
            }

    def guild(self, id, force=False):
        if (str(id) not in config) or force:
            config[str(id)] = {
                'mod': [475776964733566987],
                'shik': 'ajm',
                'r-room': 0,
                'r-sta': '8006'
            }


reg = reg()


async def log(text):
    print(text)
    ch = bot.get_channel(log_ch)
    E = discord.Embed(
        title='',
        description=text,
        color=0xffffff)
    await ch.send(embed=E)


def vcss():
    gulidsids = []
    for g in bot.voice_clients:
        gulidsids.append(g.guild.id)

    return gulidsids


def vc(guildid):
    for g in bot.voice_clients:
        vc = g
        if g.guild.id == guildid:
            return vc


async def connect(ctx):
    global player
    id = ctx.guild.id
    vc = ctx.author.voice.channel
    vcc = vcss()
    if id not in vcc:
        player[id]['p'] = await vc.connect()
    else:
        for vcc in bot.voice_clients:
            if id == vcc.guild.id:
                player[id]['p'] = vcc
                await player[id]['p'].move_to(vc)


# game
# bot.change_presence(status=discord.Status.idle, activity=game)

async def status(set: str):
    game = discord.Game(set)
    await bot.change_presence(status=discord.Status.online, activity=game)


async def tempmsg(ctx, msg, time=1.5):
    m = await ctx.send(msg)
    await asyncio.sleep(time)
    try:
        await m.delete()
    except:
        pass


art = asyncio.run_coroutine_threadsafe


class after:
    def __init__(self, ctx):
        self.ctx = ctx

    def ifdone(self, erorr):
        t1 = self.ctx.send('__**صـدق اللّٰه العظيمـ**__')
        id = self.ctx.author.voice.channel.guild.id
        try:
            m = art(t1, bot.loop).result()
            try:
                t2 = player[id]['pn'].delete()
                art(t2, bot.loop).result()
            except:
                pass
            art(asyncio.sleep(7), bot.loop).result()
            t3 = m.delete()
            art(t3, bot.loop).result()
            art(status('.play اسم السورة'), bot.loop).result()
        except:
            pass


#
# async def ifdone(ctx):
#     id = ctx.author.voice.channel.guild.id
#     while player[id]['p'].is_playing(): pass
#     try:
#         await player[id]['pn'].delete()
#     except:
#         pass
#
#     await tempmsg('__**صـدق اللّٰه العظيمـ**__', ctx, 3.5)
#     player[id]['pn'] = None


class SurahPL:
    def __init__(self, Surah, Shik, id):
        s = Q.QuranMP3(Surah, Shik)
        url = s.SurahLink
        self.audio = discord.FFmpegPCMAudio(url)
        if not id in gulids:
            gulids.append(id)
            reg.player(id)
        player[id]['url'] = url
        player[id]['Sid'] = s.ID
        player[id]['shik'] = s.name


##########################################################


# ➕ ➖
##########################################################

class panelPL:
    def __init__(self, id, E=None):
        try:
            self.Sname = Q.QPage(player[id]['Sid']).Name
            diss = player[id]['shik']
        except:
            self.Sname = 'RADIO'
            sta = player[id]['Sid']
            diss = Q.search(Q.RadioList, sta).items['Name']
        self.author = bot.get_user(player[id]['author'])
        self.url = player[id]['url']
        if E is None:
            E = discord.Embed(
                title=self.Sname,
                description=diss,
                color=0xffffff)
        E.set_thumbnail(url='https://www.mp3quran.net/images/quraan-logo.png')
        self.E = E


#####################======Buttons=======############################


@bot.event
async def on_reaction_add(rea, user):
    if (user != bot.user) and (rea.message.author == bot.user):
        try:
            await rea.message.remove_reaction(rea, user)
        except:
            pass
        global msgs
        global ng
        #####################--PAGER--###################
        for ms in msgs:
            data = str(bot.get_user(ms))
            ctxa = data[:15] + ('...' if len(data) > 15 else '')
            if ms == user.id:
                if str(rea.emoji) == '▶':
                    if 1 < ng[ms]:
                        ng[ms] -= 1
                        url = str(Q.urlP(int(ng[ms])))
                        e = pager(page=str(ng[ms])).e
                        e.set_author(name=ctxa)
                        e.set_image(url=url)
                        await rea.message.edit(embed=e)
                if str(rea.emoji) == '◀':
                    if 604 > ng[ms]:
                        ng[ms] += 1
                        url = str(Q.urlP(int(ng[ms])))
                        e = pager(page=str(ng[ms])).e
                        e.set_author(name=ctxa)
                        e.set_image(url=url)
                        await rea.message.edit(embed=e)
                if str(rea.emoji) == '🔴':
                    try:
                        await rea.message.delete()
                    except:
                        pass
                    msgs.remove(ms)

        #####################--PLAYER--###################
        for id in gulids:
            if player[id]['author'] == user.id:
                if str(rea) == '⏯':
                    if player[id]['p'].is_playing():
                        player[id]['p'].pause()
                    else:
                        player[id]['p'].resume()
                if str(rea) == '⏹':
                    player[id]['p'].stop()
                    player[id]['Sid'] = ''
                    player[id]['url'] = ''
                    await rea.message.delete()

        await log("{} > {}".format(user, rea.emoji))


# ===================================================================#

@bot.command()
@commands.guild_only()
async def play(ctx, Surah, *, Shik=None):
    global player
    global config
    id = ctx.guild.id
    reg.player(id)
    reg.guild(id)
    if Shik is None:
        Shik = config[str(id)]['shik']
    if ctx.author.voice is not None:
        #############--VARS---#############
        try:
            async with ctx.channel.typing():
                m = await ctx.send('الرجاء الانتظار...')
                c = SurahPL(Surah, Shik, id)
                player[id]['author'] = ctx.author.id
                audio = c.audio
                ####################################
                await connect(ctx)
                if not player[id]['p'].is_playing():
                    done = after(ctx).ifdone
                    player[id]['p'].play(audio, after=done)
                    panel = panelPL(id)
                    player[id]['pn'] = await ctx.send(embed=panel.E)
                    emoji = ['⏹', '⏯']
                    for e in emoji:
                        await player[id]['pn'].add_reaction(e)
                    try:
                        await m.delete()
                    except:
                        pass
                    await log('{}play {} {}:@{}#{} by:"{}"'.format(
                        prefix, Surah, Shik,
                        str(ctx.channel.guild),
                        str(ctx.channel),
                        str(ctx.author)))
                #await status(Q.QPage(player[id]['Sid']).Name)
            ############################################
        except:
            await tempmsg(ctx, '...❌')
    else:
        await tempmsg(ctx, '...❌')
    await ctx.message.delete()


@bot.command()
@commands.guild_only()
async def radio(ctx, *, sta=None):
    global player
    global config
    id = ctx.guild.id
    reg.player(id)
    reg.guild(id)
    if sta is None:
        sta = config[str(id)]['r-sta']
    if (ctx.author.voice is not None):
        async with ctx.channel.typing():
            try:
                url = Q.search(Q.RadioList, sta).items['URL']
                player[id]['author'] = ctx.author.id
                player[id]['Sid'] = sta
                await connect(ctx)
                m = await ctx.send('الرجاء الانتظار...')
                audio = discord.FFmpegPCMAudio(url)
                await asyncio.sleep(3)
                if not player[id]['p'].is_playing():
                    done = after(ctx).ifdone
                    player[id]['p'].play(audio, after=done)
                    panel = panelPL(id)
                    player[id]['pn'] = await ctx.send(embed=panel.E)
                    try:
                        await m.delete()
                    except:
                        pass
                    await log('{}radio {}:@{}#{} by:"{}"'.format(
                        prefix, sta,
                        str(ctx.channel.guild),
                        str(ctx.channel),
                        str(ctx.author)))
                else:
                    await tempmsg(ctx, '...❌')
            except:
                await tempmsg(ctx, '...❌')
    else: await tempmsg(ctx, '...❌')
    # await status(Q.QPage(player[id]['Sid']).Name)
    await ctx.message.delete()


# ------------------------------------------#
# @bot.command()
# async def vol(ctx, vol):
#     volume = float(vol)
#     player.volume = volume / 100


@bot.command()
@commands.guild_only()
async def pl(ctx):
    id = ctx.author.voice.channel.guild.id
    try:
        await player[id]['pn'].delete()
    except:
        pass
    if (ctx.author.id == player[id]['author']) or (ctx.author.id in config[str(ctx.guild.id)]['mod']):
        player[id]['pn'] = await ctx.send(embed=panelPL(id).E)
        ee = ['⏹', '⏯']
        for e in ee:
            await player[id]['pn'].add_reaction(e)
    await asyncio.sleep(2)
    await ctx.message.delete()


@bot.command()
@commands.guild_only()
async def move(ctx):
    id = ctx.author.voice.channel.guild.id
    if (player[id]['author'] == ctx.author.id) or (ctx.author.id in config[str(ctx.guild.id)]['mod']):
        await player[id]['p'].move_to(ctx.author.voice.channel)
    else:
        await tempmsg(ctx, '...❌')
    await asyncio.sleep(7)
    await ctx.message.delete()


@bot.command()
@commands.guild_only()
async def stop(ctx):
    global player
    id = ctx.author.voice.channel.guild.id
    if (player[id]['author'] == ctx.author.id) or (ctx.author.id in config[str(ctx.guild.id)]['mod']):
        player[id]['p'].stop()
        player[id]['Sid'] = None
        player[id]['url'] = None
        await player[id]['pn'].delete()
        player[id]['pn'] = None
        await tempmsg(ctx, 'OK.⏹')
        await ctx.message.delete()


@bot.command()
@commands.guild_only()
async def leave(ctx):
    id = ctx.author.voice.channel.guild.id
    if (player[id]['author'] == ctx.author.id) or (ctx.author.id in config[str(ctx.guild.id)]['mod']):
        await player[id]['p'].disconnect()
        player[id]['p'] = None
        player[id]['Sid'] = None
        player[id]['url'] = None
        await player[id]['pn'].delete()
        player[id]['pn'] = None
    else:
        await tempmsg('...❌')
        await ctx.message.delete()


##############----PAGE----################
@bot.command()
async def p(ctx, page):
    try:
        global msgs
        user = ctx.author.id
        if user in msgs:
            try:
                await msg[ctx.author.id].delete()
            except:
                pass
            msgs.remove(ctx.author.id)
        P = pager(page=page)
        E = P.e
        msgs.append(ctx.author.id)
        data = str(bot.get_user(ctx.author.id))
        ctxa = data[:15] + ('...' if len(data) > 15 else '')
        E.set_author(name=ctxa)
        m = await ctx.send(embed=E)
        msg[ctx.author.id] = m
        reactions = ['◀', '🔴', '▶']
        for i in reactions:
            await m.add_reaction(i)
        ng[ctx.author.id] = int(page)

        @bot.event
        async def on_command_completion(ctx):
            await log('{}p {}  :@{}#{} by:"{}"'.format(
                prefix, page,
                str(ctx.channel.guild),
                str(ctx.channel),
                str(ctx.author)))
            await ctx.message.delete()
    except:
        await tempmsg(ctx, '...❌')
        try:
            await ctx.message.delete()
        except:
            pass


@bot.command()
async def s(ctx, surah=None):
    global msgs
    user = ctx.author.id
    try:
        try:
            if surah is None:
                surah = player[ctx.guild.id]['Sid']
        except:
            pass
        if user in msgs:
            try:
                await msg[ctx.author.id].delete()
            except:
                pass
            msgs.remove(ctx.author.id)
        p = pager(surah=surah)
        page = p.Page
        E = p.e
        data = str(bot.get_user(ctx.author.id))
        ctxa = ((data[:15] + '...') if len(data) > 15 else data)
        E.set_author(name=ctxa)
        msgs.append(ctx.author.id)
        m = await ctx.send(embed=E)
        reactions = ['◀', '🔴', '▶']
        for e in reactions:
            await m.add_reaction(e)
        ng[ctx.author.id] = int(page)

        @bot.event
        async def on_command_completion(ctx):
            await log('{}s {}  :#{} by:"{}"'.format(
                prefix, surah,
                str(ctx.channel),
                str(ctx.author)))
            try:
                await ctx.message.delete()
            except:
                pass
    except:
        await tempmsg(ctx, '...❌')
        try:
            await ctx.message.delete()
        except:
            pass


###############----SETTING----##############

# @commands.has_permissions(manage_channels=True,manage_messages=True) you can use this only, but I want to Acsess To every server(JUST REMOVE Every line has #MAIN)
@bot.command()
@commands.guild_only()
async def set(ctx, set, *, value=None):
    global config
    id = str(ctx.guild.id)
    erorr = False
    is_manege = False  # MAIN
    if ctx.author.id in O:
        is_manege = True
    for role in ctx.author.roles:  # MAIN
        if 'manage_roles' in role.permissions:  # MAIN
            is_manege = True  # MAIN
    if is_manege:  # MAIN
        reg.guild(id)
        if set == 'info':
            await tempmsg(ctx, config[id], 180)
        vals = ['shik', 'mod', 'r-room', 'r-sta', 'unmod']
        if set in vals:
            if set == 'shik':
                value = Q.search(Q.Shiks, value).items['name']
            if set == 'mod':
                value = Q.replacer(value, '<!@>', '')
                try:
                    value = int(value)
                except:
                    erorr = True
            if not erorr:
                if set == 'unmod':
                    if value not in O:
                        try:
                            config[id]['mod'].remove(value)
                        except:
                            await tempmsg(ctx, "Actually {} it dosen't exist in Mod".format(bot.get_user(value)), 4)
                    else:
                        await tempmsg(ctx, "__You can't remove ***THE OWNER***__")
                if type(config[id][set]) == list:
                    config[id][set].append(value)
                if type(config[id][set]) == str:
                    config[id][set] = str(value)
                if type(config[id][set]) == int:
                    config[id][set] = int(value)
                log = 'Setting {} for {} BY:{}'.format(value, set, ctx.author.mention)
                await tempmsg(ctx, log, 10)
                congR()
            else:
                await tempmsg(ctx, '***`Erorr`***')
        await asyncio.sleep(2)
        await ctx.message.delete()


@bot.command()
async def clear(ctx, usr=None):
    if ctx.author.id in O:
        m = await ctx.send('➖➖OK➖➖')
        await asyncio.sleep(5)
        msgs.clear()
        channel = ctx.channel
        if usr is None:
            async for message in channel.history(limit=300):
                if message.author == bot.user:
                    try:
                        await message.delete()
                    except:
                        pass
        else:
            usr = Q.replacer(usr, '<!@>', '')
            usr = bot.get_user(int(usr))
            async for msg in channel.history(limit=300):
                if msg.author == usr:
                    for c in cmds:
                        if (prefix + c) in msg.content:
                            try:
                                await msg.delete()
                            except:
                                pass
        await log('.clear {}'.format(usr if usr else ""))
        try:
            await m.delete()
        except:
            pass
        await tempmsg(ctx, 'Done! ✔️', 3)
    else:
        await tempmsg(ctx, ' ...❌')
    try:
        await ctx.message.delete()
    except:
        pass


@bot.command()
@commands.is_owner()
async def say(ctx, *, text):
    if ctx.author == bot.get_user(475776964733566987):
        await tempmsg(ctx, '➖➖OK➖➖')
        await asyncio.sleep(2)
        await ctx.send(text)
        await ctx.message.delete()
        await tempmsg(ctx, 'Done! ✔️', 3)

    else:
        await tempmsg(ctx, '...❌', 0.5)


cmds = []
for ii in bot.all_commands.items():
    cmds.append(ii[0])
#####################################################################}}

bot.run(tOKEN)

