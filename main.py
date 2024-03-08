import discord
import discord.ui
from discord.ui import InputText, Modal
import asyncio
from discord import NotFound, InvalidArgument, HTTPException
from discord.utils import get
from discord.ext.commands.errors import CommandNotFound
import pytz
from datetime import datetime, timedelta
#Subimports.
from discord.ext import commands
from discord.ext import tasks
import time
import io
from io import *
import requests
import mysql.connector
from datetime import timedelta
from discord.ext import pages
import ast
from PIL import Image, ImageFont, ImageDraw
from itertools import islice
import arrow, traceback, threading, bs4
from aioconsole import aexec
from bit import Key, PrivateKey, PrivateKeyTestnet
from bit.network import currency_to_satoshi, satoshi_to_currency
from chat_exporter import chat_exporter
import warnings
from urllib3.exceptions import InsecureRequestWarning
warnings.filterwarnings("ignore", category=InsecureRequestWarning)

TOKEN = "Discord_Bot_Token"
PREFIX = "$"
ROBLOSECURITY = "Roblox_Cookie"
VIPSERVER_CODE = "34317217392719922689099966055994"
AUTOAMP_CATEGORY_ID = 1135516215671005245
AUTOAMP_LOGS_ID = 1081233927483686933
AUTOAMP_TRANSCRIPTS_ID = 1081233969284128809
###
MMPASS_CATEGORY_ID = 1081201921945251890
MMPASS_LOGS_ID = 1081230772637270116
MMPASS_TRANSCRIPTS_ID = 1037418335295512586
CRYPTO_LOGS = 1038216652447305808
SUBS_ID = 1038522125167886380
###
CLOSED_CATEGORY_ID = 1135516890379325490
TRADETAB_STATUS_ID = 1081234786443603979
BLACKLIST_ROLE_ID = 1104590683144208390
MM_ROLE_ID = 1104590683395858455
STAFF_ROLE_ID = 1104590683395858455
GUILD_ID = 1104590683144208384
SHUTDOWN_ID = 1035829141716619284
REQUEST_CHANNEL_ID = 1135516341319761960
TICKET_RENAMER_ROLE = 1104590683144208386
SUBSCRIBER_ROLE = 1104590683207114823
CLIENT_ROLE_ID = 1135518672052572171
###
DB_SERVERID = 1000834812795420742
MAIN_INFOID = 1001570937973510255
IMAGECHANNEL_ID = 1010616139392503868
IGNORE_THESE = [1000834813953056839, 1041389275004026932, 1002209255052546170,
                1001570937973510255, 1038216652447305808, 1006524375106863107,
                1010616139392503868, 1035829141716619284, 1002208502921580596,
                1002208531434450974, 1002208618541748234, 1002208657288732722,
                1002208677681434654, 1002208727719497758, 1002208762616090726,
                1007626258223476856, 1037418335295512586, 1081230772637270116,
                1081233969284128809, 1081233927483686933, 1038522125167886380,
                1026057875635839017, 1082975637091921971]
###
IsThBeingUpdated_CHANNEL = 1007626258223476856
IsThBeingUpdated_MESSAGE = 1007626992222490685
###
SUCCCOLOR = 0x57f287
MAINCOLOR = 0xa340ff
grey = 0x99AAB5
redcolor = 0xed4245
MMACC_ID = 4447189943
MMACC_USER = "p_ap3"
GAMEPASS_ACCID = 4010518799
FEE_MODE = True
AM_VIP_SERVER = 633228503
GAME_PASS = 4058102693

TicketAccess = [358594990982561792, 700902892495699968]

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents, case_insensitive=True, help_command=None)

AreThoseYourItems_List = []

sessionCheck = requests.Session()
sessionCheck.verify = False

Create_rbxSession = requests.Session()
#proxies = {'http': '127.0.0.1:8866', 'https': '127.0.0.1:8866'}
#Create_rbxSession.proxies = proxies
Create_rbxSession.verify = False
Create_rbxSession.cookies[".ROBLOSECURITY"] = ROBLOSECURITY
Create_req = Create_rbxSession.post("https://auth.roblox.com")
Create_rbxSession.headers["X-CSRF-Token"] = Create_req.headers["X-CSRF-Token"]

sessionDiscord = requests.Session()
sessionDiscord.headers["authorization"] = "Ticket_Renamer_Token" # a normal user-account that has access to the ticket channels
sessionDiscord.verify = False

def getrbxSession():
  global Create_rbxSession
  req = Create_rbxSession.post("https://auth.roblox.com")
  try:
    Create_rbxSession.headers["X-CSRF-Token"] = req.headers["X-CSRF-Token"]
  except Exception:
    pass
  return Create_rbxSession

def openCON():
  con = mysql.connector.connect(user='root', password='2jinot21ever', host='localhost', database='am_data')
  cur = con.cursor(dictionary=True)
  return con, cur

def closeCON(cur,con):
  cur.close()
  con.close()

def shorten_btc(number):
  return float("{:.8f}".format(number))

def getFriendsIds():
  rbxSession = getrbxSession()
  whitelist = [
    # p_ap3
    4447189943,]
  ids = []
  res = rbxSession.get('https://friends.roblox.com/v1/users/4010518799/friends')
  for user in res.json()['data']:
    if user['id'] not in whitelist:
      ids.append(user['id'])
  return ids

def snowflake2ts(snowflake):
  D_EPOCH = 1420070400000
  snowflake = int(snowflake)
  ts_bin = bin(snowflake >> 22)
  ts_dec = int(ts_bin, 0)
  ts_unix = (ts_dec + D_EPOCH) / 1000
  return int(ts_unix)

def ts2snowflake(ts):
  D_EPOCH = 1420070400000
  ts = int(ts)
  ts_dec = (ts*1000)-D_EPOCH
  ts_bin = bin(ts_dec << 22)
  snowflake = int(ts_bin, 0)
  return int(snowflake)

def find_between( s, first, last ):
  try:
    start = s.index( first ) + len( first )
    end = s.index( last, start )
    return s[start:end]
  except ValueError:
      return ""

def getErrorMsg(code):
  if code == 5:
    return "**The bot has already sent you a friend request. Accept the friend request from `AutoMMvip`.**"
  elif code == 31:
    return "**You have max friends.**"
  else:
    return "**Unknown error.**"

def rbx_send_request(username):
  rbxSession = Create_rbxSession
  # if username valid
  res1 = rbxSession.post('https://users.roblox.com/v1/usernames/users', json={'usernames': [username], 'excludeBannedUsers': True})
  if len(res1.json()['data']) == 0:
    return "Invalid username."
  # send friend request
  userid = res1.json()['data'][0]['id']
  res2 = rbxSession.post(f'https://friends.roblox.com/v1/users/{userid}/request-friendship', json={'friendshipOriginSourceType': 'Unknown'})
  # check token
  token_failed = False
  if ("message" in res2.json()) and (res2.json()['message'] == "Token Validation Failed"):
    token_failed = True
  if token_failed == True:
    rbxSession = getrbxSession()
    res2 = rbxSession.post(f'https://friends.roblox.com/v1/users/{userid}/request-friendship', json={'friendshipOriginSourceType': 'Unknown'})
  # check errors
  if "errors" in res2.json():
    error = res2.json()['errors']
    return getErrorMsg(error[0]['code'])
  # successful
  return "Successful"

def editNotifi(content):
  data = '------WebKitFormBoundaryFB3WeWADcOAo1Kvo\r\nContent-Disposition: form-data; name="payload_json"\r\n\r\n{"content":null,"embeds":null}\r\n------WebKitFormBoundaryFB3WeWADcOAo1Kvo\r\nContent-Disposition: form-data; name="file[0]"; filename="notifi.txt"\r\nContent-Type: application/octet-stream\r\n\r\n'+str(content)+'\r\n------WebKitFormBoundaryFB3WeWADcOAo1Kvo--\r\n'
  headers = {'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryFB3WeWADcOAo1Kvo'}
  res = requests.patch('https://discord.com/api/v10/webhooks/1026060543599059025/AVgQxBy7JiRgrdoA0WbxVTKFnco5uvwvorJrazE4dpxz00hlXWJLQ5-aSzPm_XlzH2YN/messages/1026060745374437427', headers=headers, data=data, verify=False)

async def readNotifi():
  c = bot.get_channel(1026057875635839017)
  data_msg = await c.fetch_message(1026060745374437427)
  file = data_msg.attachments[0]
  cont = await file.read()
  notifioff_data = ast.literal_eval(cont.decode('utf-8'))
  return notifioff_data

async def readSubs():
  dbchannel = bot.get_channel(SUBS_ID)
  logsdata_msg = await dbchannel.fetch_message(1038542781083291721)
  file = logsdata_msg.attachments[0]
  cont = await file.read()
  data = ast.literal_eval(cont.decode('utf-8'))
  return data

def editSubs(content):
  content = str(content)
  headers = {'content-type': 'multipart/form-data; boundary=----WebKitFormBoundarywnrKNaQYpci6u4ue'}
  data = '------WebKitFormBoundarywnrKNaQYpci6u4ue\r\nContent-Disposition: form-data; name="payload_json"\r\n\r\n{"content":null,"embeds":null}\r\n------WebKitFormBoundarywnrKNaQYpci6u4ue\r\nContent-Disposition: form-data; name="file[0]"; filename="mm_passes.txt"\r\nContent-Type: application/octet-stream\r\n\r\n'+content+'\r\n------WebKitFormBoundarywnrKNaQYpci6u4ue--\r\n'
  sessionDiscord.patch('https://discord.com/api/v10/webhooks/1038522301391585331/HRj-28HuDrlIVIaobkidH1Zb7-7xXh0hrk4yHr8RWnYi7Nr1xpz0_R1SMj_8AzcEt0mH/messages/1038542781083291721', headers=headers, data=data)

async def getSellers():
  msg = await bot.get_channel(1013217798685741066).fetch_message(1031259642317250601)
  msglist = msg.content.splitlines()
  listlen = len(msglist)
  msglist = msglist[1:][:listlen-2]
  return msglist

async def getVipServerCode():
  msg = await bot.get_channel(1002209255052546170).fetch_message(1024711611006595122)
  return msg.content

async def getBuyers():
  msg = await bot.get_channel(1013219330080645241).fetch_message(1031269593613860894)
  msglist = msg.content.splitlines()
  listlen = len(msglist)
  msglist = msglist[1:][:listlen-2]
  return msglist

async def editSellers(content):
  msg = await bot.get_channel(1013217798685741066).fetch_message(1031259642317250601)
  await msg.edit(content)

async def editBuyers(content):
  msg = await bot.get_channel(1013219330080645241).fetch_message(1031269593613860894)
  await msg.edit(content)

async def getTicketCount():
  msg = await bot.get_channel(1006524375106863107).fetch_message(1006524626790256670)
  number = int(msg.content)
  return number

async def updateTicketCount(number):
  msg = await bot.get_channel(1006524375106863107).fetch_message(1006524626790256670)
  await msg.edit(int(number))

async def readSendTradeTab():
  msg = await bot.get_channel(1002208657288732722).fetch_message(1002210811219034217)
  content = msg.embeds[0].description
  return ast.literal_eval(content)

async def readPlayerList():
  msg = await bot.get_channel(1002208762616090726).fetch_message(1002211596698914826)
  return ast.literal_eval(msg.content)

def updateSendTradeTab(data):
  global sessionCheck
  json_data = {
    'content': None,
    'embeds': [
        {
            'description': str(data),
        },
    ],
    'attachments': [],
  }
  webhook = "1002210693170352128/JE4tsp0we1XmWQx83wMRQuVJ6Pr0Ta76tGFAKEcadz5-0ZcsuDBF4_hrpiDk1QxjNsc2"
  message = "1002210811219034217"
  sessionCheck.patch(f'https://discord.com/api/v10/webhooks/{webhook}/messages/{message}', json=json_data)

def updateAddItems(data):
  global sessionCheck
  json_data = {
    'content': str(data),
    'embeds': None,
    'attachments': [],
  }
  webhook = "1002210971382730953/_9ffSq_Voi2rtUqcNWs_1L3fJjxhWfMukJpd-eri5AbhYB01f4qxPhJwya7vviO5DKa8"
  message = "1002211139914047599"
  sessionCheck.patch(f'https://discord.com/api/v10/webhooks/{webhook}/messages/{message}', json=json_data)

def updateSentTrades(data):
  global sessionCheck
  json_data = {
    'content': str(data),
    'embeds': None,
    'attachments': [],
  }
  webhook = "1002211329295253637/MRWOEEWXLhi2iCRxQMgATbVcs5mNIArEx8fX14prEuwUsCVLI01fU90hvSK9DIzQ8AdB"
  message = "1002211402167099463"
  sessionCheck.patch(f'https://discord.com/api/v10/webhooks/{webhook}/messages/{message}', json=json_data)

def updateAccOrDec(data):
  global sessionCheck
  json_data = {
    'content': str(data),
    'embeds': None,
    'attachments': [],
  }
  webhook = "1002210408435826718/pXWmly--zmVj-ZTz7voxiozEOCsYwaHZbYbG277_K9lJnmfElO2qYxlZuKsLTHwDCEGM"
  message = "1002210536299175996"
  sessionCheck.patch(f'https://discord.com/api/v10/webhooks/{webhook}/messages/{message}', json=json_data)

def updateChannel(name, channelid):
  global sessionDiscord
  json_data = {'name': name}
  sessionDiscord.patch(f'https://discord.com/api/v9/channels/{channelid}', json=json_data)

def updateVC(name):
  global sessionDiscord
  json_data = {'name': name}
  sessionDiscord.patch(f'https://discord.com/api/v9/channels/{TRADETAB_STATUS_ID}', json=json_data)

subsToAdd = []
subsToChange = []
isWorking_subs = False
@tasks.loop(seconds=2)
async def addsubs():
  global isWorking_subs
  if isWorking_subs == True:
    return

  if len(subsToAdd) != 0:
    if isWorking_subs == True:
      return
    isWorking_subs = True
    msglist = await readSubs()
    msglist.extend(subsToAdd)
    for item in subsToAdd[:]:
      subsToAdd.remove(item)
    editSubs(msglist)
    isWorking_subs = False

  if len(subsToChange) != 0:
    if isWorking_subs == True:
      return
    isWorking_subs = True
    msglist = await readSubs()
    newInfo = []
    for item1 in subsToChange[:]:
      for passi in msglist[:]:
        if item1['userID'] == passi['userID']:
          msglist.remove(passi)
          newInfo.append({'userID': item1['userID'], 'boughtAt': item1['boughtAt'], 'endsAt': item1['endsAt'], 'extended': item1['extended']})
          break
      subsToChange.remove(item1)
    msglist.extend(newInfo)
    editSubs(msglist)
    isWorking_subs = False

@tasks.loop(hours=1)
async def checkvouch():
  con,cur = openCON()
  cur.execute(f"SELECT * FROM channels WHERE ticket_status='Closed'")
  resSQL = cur.fetchall()
  if len(resSQL) == 0:
    closeCON(cur,con)
    return

  ticketlogs = bot.get_channel(AUTOAMP_LOGS_ID)
  transcripts = bot.get_channel(AUTOAMP_TRANSCRIPTS_ID)
  for ticketsql in resSQL:
    ticketc = bot.get_channel(int(ticketsql['channel_id']))

    try:
      print(f"Saving: [Done] {ticketc.name}")
    except Exception:
      pass
    users={}
    channelownerid = ticketsql['channel_owner_id']
    sellerid = ticketsql['trader_seller_id']
    buyerid = ticketsql['trader_receiver_id']
    tradeid1 = ticketsql['trade_id']
    tradeid2 = ticketsql['redeem_trade_id']
    recuser = ticketsql['receiver_username']
    senduser = ticketsql['seller_username']
    passid = ticketsql['gamepass_id']

    await ticketc.send(embed=discord.Embed(description=f'Deleting this ticket..', color=MAINCOLOR))

    cur.execute(f"UPDATE channels SET ticket_status='Delete' WHERE channel_id='{ticketc.id}'")
    con.commit()
    logembed = discord.Embed(color=MAINCOLOR)
    logembed = discord.Embed(description=f"Author: **Autodeletion** | ID: {bot.user.id}\nTicket: **{ticketc.name}** | ID: {ticketc.id}\nAction: **Deleted Ticket**", color=0xed4245)

    await ticketlogs.send(embed=logembed)
    transcript = await chat_exporter.export(channel=ticketc, limit=None, tz_info="Asia/Singapore")
    if transcript is None:
      return
    transcript_file = discord.File(io.BytesIO(transcript.encode()), filename=f"transcript-{ticketc.name}.html")
    transcriptembed = discord.Embed(color=0x1EC45C)
    transcriptembed.add_field(name="Author", value=f"{bot.user.mention} | {bot.user.id}", inline=True)
    transcriptembed.add_field(name="Ticket", value=f"{ticketc.name} | {ticketc.id}", inline=True)
    transcriptembed.add_field(name="Category", value=f"{ticketc.category.name} | {ticketc.category.id}", inline=True)
    transcriptembed.add_field(name="Info", value=f"Owner: <@{channelownerid}>\nSeller: <@{sellerid}>\nBuyer: <@{buyerid}>\nFirst Trade ID: {tradeid1}\nSecond Trade ID: {tradeid2}\nSender Username: `{senduser}`\nReceiver Username: `{recuser}`\nGamepass ID: `{passid}`", inline=False)
    mess = await transcripts.send(embed=transcriptembed, file=transcript_file)
    attachment = mess.attachments[0]
    messages = await ticketc.history(limit=None).flatten()
    for msg in messages[::1]:
        if msg.author.id in users.keys():
          users[msg.author.id]+=1
        else:
          users[msg.author.id]=1
    user_string,user_transcript_string="",""
    b = sorted(users.items(), key=lambda x: x[1], reverse=True)
    try:
      for k in b:
        user = await bot.fetch_user(int(k[0]))
        user_string+=f"{k[1]} | {user.mention} | {user.name}#{user.discriminator}\n"
    except NotFound:
      pass
    await mess.edit(embed=transcriptembed.add_field(name="**Direct Transcript**", value=f"[Direct Transcript](https://mahto.id/chat-exporter?url={attachment.url})", inline=True))
    await mess.edit(embed=transcriptembed.add_field(name="**Users in transcript**", value=f"{user_string}", inline=True))
    await ticketc.delete()
  closeCON(cur,con)

@tasks.loop(seconds=2)
async def tradeTabStatus():
  c = bot.get_channel(AUTOAMP_CATEGORY_ID)
  if c == None:
    return

  if len(c.text_channels) == 0:
    return

  try:
    vc = bot.get_channel(TRADETAB_STATUS_ID)
    data = await readSendTradeTab()
    openName = "TradeTab: Available"
    closedName = "TradeTab: Being Used"
  except Exception:
    return

  if data['isOpen'] == False:
    isTradeTabAvailable = True
  else:
    isTradeTabAvailable = False

  if (isTradeTabAvailable == True) and (vc.name == openName):
    return
  if (isTradeTabAvailable == False) and (vc.name == closedName):
    return
  
  if isTradeTabAvailable == True:
    updateVC(openName)
  else:
    updateVC(closedName)

@tasks.loop(seconds=2)
async def checkTradesSucc():

  c = bot.get_channel(AUTOAMP_CATEGORY_ID)
  if c == None:
    return

  if len(c.text_channels) == 0:
    return

  con,cur = openCON()
  cur.execute(f"SELECT * FROM channels WHERE ticket_status='Active' AND is_waiting_for_check='Yes'")
  resSQL = cur.fetchall()
  if len(resSQL) == 0:
    closeCON(cur,con)
    return

  for ticketsql in resSQL:

    IsThBeingUpdated = await bot.get_channel(IsThBeingUpdated_CHANNEL).fetch_message(IsThBeingUpdated_MESSAGE)
    if IsThBeingUpdated.content == "Yes":
      continue
    
    dbchannel = bot.get_channel(1002208531434450974)
    logsdata_msg = await dbchannel.fetch_message(1002209717923369030)

    if int(ticketsql['accepted_trade_timestamp']) > int(logsdata_msg.edited_at.timestamp()):
      continue

    ticketsql['trade_id'] = ast.literal_eval(ticketsql['trade_id'])

    succ_num = ticketsql['successful_trades_num']
    try:
      tradeID = ticketsql['trade_id'][succ_num]
    except IndexError:
      continue
    
    ticketchannel = bot.get_channel(int(ticketsql['channel_id']))
    
    sellerID = ticketsql['trader_seller_id']
    buyerID = ticketsql['trader_receiver_id']
    
    file = logsdata_msg.attachments[0]
    cont = await file.read()
    tradehistory_data = ast.literal_eval(cont.decode('utf-8'))
    tradeids = []
    for i in tradehistory_data:
      tradeids.append(i['tradeID'])
    
    tradeFound = False
    if tradeID in tradeids:
      tradeFound = True

    TradeTabInfo = await readSendTradeTab()

    if (TradeTabInfo['tradeID'] != tradeID): # if im not trading with the person
      if tradeFound == False: # if the trade wasn't found in history
        ticketsql['trade_id'][succ_num] = "No"
        ticketsql['trade_id'] = str(ticketsql['trade_id']).replace("'", "\"")
        cur.execute(f"UPDATE channels SET trade_id='{str(ticketsql['trade_id'])}', is_waiting_for_check='No', accepted_trade_timestamp='0' WHERE channel_id='{ticketsql['channel_id']}'")
        con.commit()
        await ticketchannel.send(f"<@{sellerID}> Please use the `$send` command again.", embed=discord.Embed(description="<:redci:879849638855852112>  **The Trade Has Failed**  <:redci:879849638855852112>", color=redcolor))
        continue
    else:
      continue

    selc_trades = ticketsql['selected_trades_num']
    succ_trades = ticketsql['successful_trades_num']
    succ_trades = succ_trades+1
    
    cur.execute(f"UPDATE channels SET successful_trades_num='{succ_trades}' WHERE channel_id='{ticketsql['channel_id']}'")
    if selc_trades == succ_trades:
      cur.execute(f"UPDATE channels SET pets_received='Yes', is_waiting_for_check='No', accepted_trade_timestamp='0' WHERE channel_id='{ticketsql['channel_id']}'")
      con.commit()
      await ticketchannel.send(embed=discord.Embed(title="<:succ:926608308033441792>  **The Bot Has Successfully Received The Items**  <:succ:926608308033441792>", color=MAINCOLOR))
      embed1 = discord.Embed(title="・ Step `2`", description=f"> <@{buyerID}> Pay your trader whatever you guys agreed on.", color=MAINCOLOR)
      embed2 = discord.Embed(title="・ Step `3`", description=f"> <@{sellerID}> Type `$confirm`, once your trader has paid you.", color=MAINCOLOR)
      embed3 = discord.Embed(title="・ Step `4`", description=f"> Pay the middleman fee (if none of you are subscribed)", color=MAINCOLOR)
      embed4 = discord.Embed(title="・ Step `5`", description=f"> <@{buyerID}> Join the VIP server via `$am` command.\n> Then type `$redeem` in Roblox chat to withdraw your items.", color=MAINCOLOR)
      embed5 = discord.Embed(title="・Additional Commands:", description=f"> `$inv` - Display Bot's Inventory.\n> `$th` - Display Bot's Trade History.\n> `$am`/`$mm2`/`$psx` - Sends VIP servers links.", color=MAINCOLOR)
      await ticketchannel.send(embeds=[embed1,embed2,embed3,embed4,embed5], view=CancelTrade())
      continue
    cur.execute(f"UPDATE channels SET is_waiting_for_check='No', accepted_trade_timestamp='0' WHERE channel_id='{ticketsql['channel_id']}'")
    con.commit()
    await ticketchannel.send(embed=discord.Embed(title="<:succ:926608308033441792>  **The Bot Has Successfully Received The Items**  <:succ:926608308033441792>", description="Use the `$send` command again and give the rest of the items to the bot.", color=MAINCOLOR))
  closeCON(cur,con)

@tasks.loop(seconds=2)
async def checkIfAccepted():

    c = bot.get_channel(AUTOAMP_CATEGORY_ID)
    if c == None:
      return

    if len(c.text_channels) == 0:
      return
  
    global AreThoseYourItems_List

    try:
      data = await readSendTradeTab()
    except Exception:
      return

    if data['isOpen'] == False or data['channelID'] == 0 or data['sendtoName'] == "0":
      return

    tradeID = data['tradeID']
    try:
      senderName = data['senderName']
    except KeyError:
      return
    recName = data['recName']
    RecItemsInfo = data['RecItemsInfo']
    channelID = data['channelID']

    try:
      con,cur = openCON()
      cur.execute(f"SELECT * FROM channels WHERE channel_id='{channelID}'")
      resSQL = cur.fetchall()[0]
      test = resSQL['gave_redeemer']
    except Exception as e:
      closeCON(cur,con)
      #print(e)
      return

    if resSQL['gave_redeemer'] == "No": # if didn't redeem pets
      if resSQL['receiver_username'] == recName or (resSQL['ticket_status'] == "Pending" and resSQL['receiver_username'] != recName):
        if resSQL['trade_confirmed'] == "Yes": # if trade confirmed
          if data['askedTrader'] == "No": # if didn't ask trader
            if data['stage'] == "negotiation":
              data['askedTrader'] = "Yes"

              updateSendTradeTab(data)

              buyerID = resSQL['trader_receiver_id']
              sellerID = resSQL['trader_seller_id']
              
              class isThebotTradingwithu(discord.ui.View):
                def __init__(self):
                  super().__init__(timeout=None)
                @discord.ui.button(row=0, label="Yes", style=discord.ButtonStyle.green, custom_id="yesItsIs", disabled=False)
                async def button_callback1(self, button, interaction):
                  
                  con,cur = openCON()
                  cur.execute(f"SELECT * FROM channels WHERE channel_id='{interaction.channel.id}'")
                  resSQL = cur.fetchall()[0]

                  if resSQL['ticket_status'] == "Active":
                    isKookie = False
                    if interaction.user.id in TicketAccess:
                      isKookie = True
                    if isKookie == False:
                      if interaction.user.id != int(buyerID):
                        closeCON(cur,con)
                        await interaction.response.defer()
                        return await interaction.channel.send(content=f"{interaction.user.mention} **You can't use this**", delete_after=2)
                    
                    for child in self.children:
                      child.disabled = True
                    await interaction.message.edit(view=self)
                  
                    try:
                      await interaction.response.defer()
                    except NotFound:
                      pass

                    await interaction.channel.send(embed=discord.Embed(description="<a:loading:1002330071043944501>  **Processing**  <a:loading:1002330071043944501>", color=grey), delete_after=4)

                    await asyncio.sleep(2)
                                      
                    datac = await readSendTradeTab()
                    
                    if datac['tradeID'] != tradeID:
                      closeCON(cur,con)
                      await interaction.message.reply(embed=discord.Embed(description="<a:oklol:858377249949220904>  **Huh.. seems like the trade has been declined, you may try again**  <a:oklol:858377249949220904>", color=grey))
                      return
                    
                    dbchannel = bot.get_channel(1002208531434450974)
                    logsdata_msg = await dbchannel.fetch_message(1002209717923369030)
                    file = logsdata_msg.attachments[0]
                    cont = await file.read()
                    tradehistory_data = ast.literal_eval(cont.decode('utf-8'))
                    tradeids = []
                    for i in tradehistory_data:
                      tradeids.append(i['tradeID'])
                    
                    resSQL['redeem_trade_id'] = ast.literal_eval(resSQL['redeem_trade_id'])
                    resSQL['trade_id'] = ast.literal_eval(resSQL['trade_id'])
                    trade_num = 0
                    for redeemtradeID in resSQL['redeem_trade_id']:
                      if redeemtradeID not in tradeids:
                        break
                      trade_num = trade_num+1
                    addItems_tradeID = resSQL['trade_id'][trade_num]

                    jsdata = addItems_tradeID
                    updateAddItems(jsdata)
    
                    try:
                      clientRole = interaction.guild.get_role(CLIENT_ROLE_ID)
                      userRole1 = interaction.guild.get_member(buyerID)
                      userRole2 = interaction.guild.get_member(sellerID)
                      if userRole1 != None:
                        await userRole1.add_roles(clientRole)
                      if userRole2 != None:
                        await userRole2.add_roles(clientRole)
                    except Exception:
                      pass

                    await asyncio.sleep(2)
                    selc_trades = resSQL['selected_trades_num']
                    if (selc_trades-1) == trade_num:
                      await interaction.message.reply(embed=discord.Embed(description="**Alright, the bot has added the items into the trade and accepted it.**\nYou may use the command again if the trade fails in-game, please leave a feedback/vouch in <#1136411635733495969> 🥰", color=MAINCOLOR), view=Closed_Button())
                    else:
                      await interaction.message.reply(embed=discord.Embed(description="**Alright, the bot has added the items into the trade and accepted it.**\nYou may use the command again if the trade fails in-game, re-use the command to withdraw the rest of your items.", color=MAINCOLOR))
                    resSQL['redeem_trade_id'][trade_num] = tradeID

                    resSQL['redeem_trade_id'] = str(resSQL['redeem_trade_id']).replace("'", "\"")
                    cur.execute(f"UPDATE channels SET redeem_trade_id='{resSQL['redeem_trade_id']}', gave_redeemer='Yes' WHERE channel_id='{interaction.channel.id}'")
                    con.commit()
                    closeCON(cur,con)

                  elif resSQL['ticket_status'] == "Pending":
                    closeCON(cur,con)

                    isKookie = False
                    if interaction.user.id in TicketAccess:
                      isKookie = True
                    if isKookie == False:
                      await interaction.response.defer()
                      return await interaction.channel.send(content=f"{interaction.user.mention} **You can't use this**", delete_after=2)
                    
                    for child in self.children:
                      child.disabled = True
                    await interaction.message.edit(view=self)
                  
                    try:
                      await interaction.response.defer()
                    except NotFound:
                      pass

                    await interaction.channel.send(embed=discord.Embed(description="<a:loading:1002330071043944501>  **Processing**  <a:loading:1002330071043944501>", color=grey), delete_after=4)

                    await asyncio.sleep(2)
                                      
                    datac = await readSendTradeTab()
                    
                    if datac['tradeID'] != tradeID:
                      await interaction.message.reply(embed=discord.Embed(description="<a:oklol:858377249949220904>  **Huh.. seems like the trade has been declined, you may try again**  <a:oklol:858377249949220904>", color=grey))
                      return
                    
                    dbchannel = bot.get_channel(1002208531434450974)
                    logsdata_msg = await dbchannel.fetch_message(1002209717923369030)
                    file = logsdata_msg.attachments[0]
                    cont = await file.read()
                    tradehistory_data = ast.literal_eval(cont.decode('utf-8'))
                    tradeids = []
                    for i in tradehistory_data:
                      tradeids.append(i['tradeID'])

                    resSQL['redeem_trade_id'] = ast.literal_eval(resSQL['redeem_trade_id'])
                    resSQL['trade_id'] = ast.literal_eval(resSQL['trade_id'])
                    trade_num = 0
                    for redeemtradeID in resSQL['redeem_trade_id']:
                      if redeemtradeID not in tradeids:
                        break
                      trade_num = trade_num+1
                    addItems_tradeID = resSQL['trade_id'][trade_num]

                    jsdata = addItems_tradeID
                    updateAddItems(jsdata)
    
                    await asyncio.sleep(2)
                    await interaction.message.reply(embed=discord.Embed(description="**Alright, the bot has added the items into the trade and accepted it.**", color=MAINCOLOR))
                  
                @discord.ui.button(row=0, label="No", style=discord.ButtonStyle.red, custom_id="itIsfNot", disabled=False)
                async def button_callback2(self, button, interaction):
                  try:
                    await interaction.response.defer()
                  except NotFound:
                    pass

                  con,cur = openCON()
                  cur.execute(f"SELECT * FROM channels WHERE channel_id='{interaction.channel.id}'")
                  resSQL = cur.fetchall()[0]
                  closeCON(cur,con)

                  if resSQL['ticket_status'] == "Active":
                    isKookie = False
                    if interaction.user.id in TicketAccess:
                      isKookie = True
                    if isKookie == False:
                      if interaction.user.id != int(buyerID):
                        return await interaction.channel.send(content=f"{interaction.user.mention} **You can't use this**", delete_after=2)
                      
                    for child in self.children:
                      child.disabled = True
                    await interaction.message.edit(view=self)
                    
                    await interaction.channel.send(embed=discord.Embed(description="<a:loading:1002330071043944501>  **Processing**  <a:loading:1002330071043944501>", color=grey), delete_after=2)

                    await asyncio.sleep(2)

                    datac = await readSendTradeTab()
                    
                    if datac['tradeID'] != tradeID:
                      await interaction.message.reply(embed=discord.Embed(description="<:redci:879849638855852112>  **The Trade Has Already Been Declined**  <:redci:879849638855852112>", color=redcolor))
                      return
                    
                    jsdata = "decline"
                    updateAccOrDec(jsdata)
                    
                    await interaction.message.reply(embed=discord.Embed(description="<:redci:879849638855852112>  **The Trade Has Been Declined**  <:redci:879849638855852112>", color=redcolor))
                    return
                  elif resSQL['ticket_status'] == "Pending":
                    isKookie = False
                    if interaction.user.id in TicketAccess:
                      isKookie = True
                    if isKookie == False:
                      return await interaction.channel.send(content=f"{interaction.user.mention} **You can't use this**", delete_after=2)
                      
                    for child in self.children:
                      child.disabled = True
                    await interaction.message.edit(view=self)
                    
                    await interaction.channel.send(embed=discord.Embed(description="<a:loading:1002330071043944501>  **Processing**  <a:loading:1002330071043944501>", color=grey), delete_after=2)

                    await asyncio.sleep(2)

                    datac = await readSendTradeTab()
                    
                    if datac['tradeID'] != tradeID:
                      await interaction.message.reply(embed=discord.Embed(description="<:redci:879849638855852112>  **The Trade Has Already Been Declined**  <:redci:879849638855852112>", color=redcolor))
                      return
                    
                    jsdata = "decline"
                    updateAccOrDec(jsdata)
                    
                    await interaction.message.reply(embed=discord.Embed(description="<:redci:879849638855852112>  **The Trade Has Been Declined**  <:redci:879849638855852112>", color=redcolor))
                    return

              if resSQL['ticket_status'] == "Active":
                channel = bot.get_channel(int(channelID))
                                  
                datac = await readSendTradeTab()
                
                if datac['tradeID'] != tradeID:
                  closeCON(cur,con)
                  await channel.send(embed=discord.Embed(description="<a:oklol:858377249949220904>  **Huh.. seems like the trade has been declined, you may use the command again**  <a:oklol:858377249949220904>", color=grey))
                  return
                
                dbchannel = bot.get_channel(1002208531434450974)
                logsdata_msg = await dbchannel.fetch_message(1002209717923369030)
                file = logsdata_msg.attachments[0]
                cont = await file.read()
                tradehistory_data = ast.literal_eval(cont.decode('utf-8'))
                tradeids = []
                for i in tradehistory_data:
                  tradeids.append(i['tradeID'])
                
                resSQL['redeem_trade_id'] = ast.literal_eval(resSQL['redeem_trade_id'])
                resSQL['trade_id'] = ast.literal_eval(resSQL['trade_id'])
                trade_num = 0
                for redeemtradeID in resSQL['redeem_trade_id']:
                  if redeemtradeID not in tradeids:
                    break
                  trade_num = trade_num+1
                addItems_tradeID = resSQL['trade_id'][trade_num]

                jsdata = str(addItems_tradeID)
                updateAddItems(f"{jsdata}\n{channelID}")

                try:
                  clientRole = channel.guild.get_role(CLIENT_ROLE_ID)
                  userRole1 = channel.guild.get_member(resSQL['trader_receiver_id'])
                  userRole2 = channel.guild.get_member(resSQL['trader_seller_id'])
                  if userRole1 != None:
                    await userRole1.add_roles(clientRole)
                  if userRole2 != None:
                    await userRole2.add_roles(clientRole)
                except Exception:
                  pass

                await asyncio.sleep(3)
                selc_trades = resSQL['selected_trades_num']
                if (selc_trades-1) == trade_num:
                  await channel.send(embed=discord.Embed(description="**Alright, the bot has added the items into the trade and accepted it.**\nYou may use the command again if the trade fails in-game, please leave a feedback/vouch in <#1136411635733495969> 🥰", color=MAINCOLOR), view=Closed_Button())
                else:
                  await channel.send(embed=discord.Embed(description="**Alright, the bot has added the items into the trade and accepted it.**\nYou may use the command again if the trade fails in-game, re-use the command to withdraw the rest of your items.", color=MAINCOLOR))
                resSQL['redeem_trade_id'][trade_num] = tradeID
                resSQL['redeem_trade_id'] = str(resSQL['redeem_trade_id']).replace("'", "\"")
                cur.execute(f"UPDATE channels SET redeem_trade_id='{resSQL['redeem_trade_id']}' WHERE channel_id='{channelID}'")
                con.commit()
                closeCON(cur,con)
                return
              elif resSQL['ticket_status'] == "Pending":
                channel = bot.get_channel(int(channelID))
                                  
                datac = await readSendTradeTab()
                
                if datac['tradeID'] != tradeID:
                  closeCON(cur,con)
                  await channel.send(embed=discord.Embed(description="<a:oklol:858377249949220904>  **Huh.. seems like the trade has been declined, you may use the command again**  <a:oklol:858377249949220904>", color=grey))
                  return
            
                dbchannel = bot.get_channel(1002208531434450974)
                logsdata_msg = await dbchannel.fetch_message(1002209717923369030)
                file = logsdata_msg.attachments[0]
                cont = await file.read()
                tradehistory_data = ast.literal_eval(cont.decode('utf-8'))
                tradeids = []
                for i in tradehistory_data:
                  tradeids.append(i['tradeID'])

                resSQL['redeem_trade_id'] = ast.literal_eval(resSQL['redeem_trade_id'])
                resSQL['trade_id'] = ast.literal_eval(resSQL['trade_id'])
                trade_num = 0
                for redeemtradeID in resSQL['redeem_trade_id']:
                  if redeemtradeID not in tradeids:
                    break
                  trade_num = trade_num+1
                addItems_tradeID = resSQL['trade_id'][trade_num]

                jsdata = str(addItems_tradeID)
                updateAddItems(f"{jsdata}\n{channelID}")

                await asyncio.sleep(2)
                selc_trades = resSQL['selected_trades_num']
                if (selc_trades-1) == trade_num:
                  await channel.send(embed=discord.Embed(description="**Alright, the bot has added the items into the trade and accepted it.**", color=MAINCOLOR))
                else:
                  await channel.send(embed=discord.Embed(description="**Alright, the bot has added the items into the trade and accepted it.**\nThere are more items to return", color=MAINCOLOR))
                resSQL['redeem_trade_id'][trade_num] = tradeID
                resSQL['redeem_trade_id'] = str(resSQL['redeem_trade_id']).replace("'", "\"")
                cur.execute(f"UPDATE channels SET redeem_trade_id='{resSQL['redeem_trade_id']}' WHERE channel_id='{channelID}'")
                con.commit()
                closeCON(cur,con)
                return
  
    if data['askedTrader'] == "Yes" or data['hasAccepted'] == "No":
      closeCON(cur,con)
      return
    try:
      if resSQL['pets_received'] == "Yes":
        closeCON(cur,con)
        return
    except IndexError:
      closeCON(cur,con)
      return

    data['askedTrader'] = "Yes"
    updateSendTradeTab(data)
    buyerID = resSQL['trader_receiver_id']

    class isThisYourTrade(discord.ui.View):
      def __init__(self):
        super().__init__(timeout=None)
      @discord.ui.button(row=0, label="Accept", style=discord.ButtonStyle.green, custom_id="yesItIs", disabled=False)
      async def button_callback1(self, button, interaction):

        isKookie = False
        if interaction.user.id in TicketAccess:
          isKookie = True
        if isKookie == False:
          if interaction.user.id != int(buyerID):
            await interaction.response.defer()
            return await interaction.channel.send(content=f"{interaction.user.mention} **You can't accept your own trade! Your trader has to use the button.**", delete_after=4)
        
        for child in self.children:
          child.disabled = True
        await interaction.message.edit(view=self)

        try:
          await interaction.response.defer()
        except NotFound:
          pass
        
        await interaction.channel.send(embed=discord.Embed(description="<a:loading:1002330071043944501>  **Processing**  <a:loading:1002330071043944501>", color=grey), delete_after=2)

        await asyncio.sleep(2)

        datac = await readSendTradeTab()
        
        for aret in AreThoseYourItems_List:
          if interaction.message.id == aret['msg_id']:
            tradeID = aret['tr_id']
            AreThoseYourItems_List.remove(aret)
            break

        con,cur = openCON()
        cur.execute(f"SELECT * FROM channels WHERE channel_id='{interaction.channel.id}'")
        resSQL = cur.fetchall()[0]

        if datac['tradeID'] != tradeID:
          closeCON(cur,con)
          await interaction.channel.send(embed=discord.Embed(description="<a:oklol:858377249949220904>  **Seems like the trade has been declined or timed out**  <a:oklol:858377249949220904>", color=grey))
          await interaction.channel.send(f"<@{resSQL['trader_seller_id']}> Please use the `$send` command again and give the items to the bot.")
          return
        
        if datac['hasModifiedTrade'] == "Yes":
          closeCON(cur,con)
          jsdata = "decline"
          updateAccOrDec(jsdata)
          
          await interaction.message.reply(embed=discord.Embed(description="<:redci:879849638855852112>  **Your trader has modified the trade, therefore the bot has declined the trade in-game**  <:redci:879849638855852112>", color=redcolor))
          await interaction.channel.send(f"<@{resSQL['trader_seller_id']}> If you weren't aware already, you cannot add or remove items from the trade after you've accepted it in-game, your trade has been declined.\nPlease use the `$send` command again and make sure you select every promised item before accepting the trade.")
          return

        jsdata = "accept"
        updateAccOrDec(jsdata)

        await interaction.message.reply(embed=discord.Embed(description="<a:loading:1002330071043944501>  **Alright, the trade is now processing in-game, please wait until the bot receives the items..**  <a:loading:1002330071043944501>", color=grey))
        cur.execute(f"SELECT * FROM channels WHERE channel_id='{interaction.channel.id}'")
        resSQL = cur.fetchall()[0]
        resSQL['trade_id'] = ast.literal_eval(resSQL['trade_id'])
        succ_num = resSQL['successful_trades_num']
        resSQL['trade_id'][succ_num] = tradeID
        resSQL['trade_id'] = str(resSQL['trade_id']).replace("'", "\"")
        cur.execute(f"UPDATE channels SET trade_process='{int(time.time())}', is_waiting_for_check='Yes', accepted_trade_timestamp='{int(datetime.now().timestamp())}', trade_id='{resSQL['trade_id']}' WHERE channel_id='{interaction.channel.id}'")
        con.commit()
        closeCON(cur,con)
        
      @discord.ui.button(row=0, label="Decline", style=discord.ButtonStyle.red, custom_id="itIsNot", disabled=False)
      async def button_callback2(self, button, interaction):
        try:
          await interaction.response.defer()
        except NotFound:
          pass

        isKookie = False
        if interaction.user.id in TicketAccess:
          isKookie = True
        if isKookie == False:
          if interaction.user.id != int(buyerID):
            return await interaction.channel.send(content=f"{interaction.user.mention} **You can't use this**", delete_after=2)
          
        for child in self.children:
          child.disabled = True
        await interaction.message.edit(view=self)
        
        await interaction.channel.send(embed=discord.Embed(description="<a:loading:1002330071043944501>  **Processing**  <a:loading:1002330071043944501>", color=grey), delete_after=2)

        await asyncio.sleep(2)
                
        datac = await readSendTradeTab()
        
        for aret in AreThoseYourItems_List:
          if interaction.message.id == aret['msg_id']:
            tradeID = aret['tr_id']
            AreThoseYourItems_List.remove(aret)
            break

        if datac['tradeID'] != tradeID:          
          await interaction.message.reply(embed=discord.Embed(description="<:redci:879849638855852112>  **The Trade Has Already Been Declined**  <:redci:879849638855852112>", color=redcolor))
          return
        
        jsdata = "decline"
        updateAccOrDec(jsdata)
        
        await interaction.message.reply(embed=discord.Embed(description="<:redci:879849638855852112>  **The Trade Has Been Declined**  <:redci:879849638855852112>", color=redcolor))
        return
    
    ### Items Positions
    row1_left_x = 381
    row1_left_y = 43
    items_place = [
        (row1_left_x, row1_left_y), # 0 - first
        (row1_left_x+82, row1_left_y), # 1 - second
        (row1_left_x+82+82, row1_left_y), # 2 - third
        (row1_left_x, row1_left_y+82), # 3 - fourth
        (row1_left_x+82, row1_left_y+82), # 4 - fifth
        (row1_left_x+82+82, row1_left_y+82), # 5 - sixth
        (row1_left_x, row1_left_y+82+82), # 6 - seventh
        (row1_left_x+82, row1_left_y+82+82), # 7 - eighth
        (row1_left_x+82+82, row1_left_y+82+82) # 8 - ninth
    ]

    ### Pots Positions
    rightdown_pots_x = 58
    rightdown_pots_y = 58
    pots_place = [
        (rightdown_pots_x, rightdown_pots_y), # right (Ride) - 0
        (rightdown_pots_x-18, rightdown_pots_y), # middle (Fly) - 1
        (rightdown_pots_x-18-18, rightdown_pots_y) # left (Mega/Neon) - 2
    ]

    ### Pots Storage
    pots = {
        "fly": Image.open("Potions/fly.png"),
        "ride": Image.open("Potions/ride.png"),
        "neon": Image.open("Potions/neon.png"),
        "mega": Image.open("Potions/mega.png")
    }

    ### Open Background & Font
    font = ImageFont.truetype("SourceSansPro-Bold.ttf", size=27)
    bg = Image.open("background.png")
    bg2 = Image.open("background.png")
    ### Add Users
    txt_h = 5
    draw = ImageDraw.Draw(bg)
    user = senderName
    draw.text(xy=(17,txt_h/2), text=user, fill=(51,51,51), font=font)
    #
    draw2 = ImageDraw.Draw(bg)
    user2 = recName
    un1, un2, text_w, text_h = draw.textbbox(xy=(0,0), text='"Hidden"', font=font)
    draw2.text(xy=(626 - text_w, txt_h / 2), text='"Hidden"', fill=(51,51,51), font=font)
    #

    ### Add Items & Pots
    itemcount = 0
    resete = False
    for i1 in RecItemsInfo:
      if itemcount == 9:
        resete = True
        itemcount = 0

      if resete == True:
        itembox = Image.open("itembox.png")
        itembox = itembox.convert(mode="RGB")
        item = Image.open(f"ImagesFolder/{i1['itemName']}.png")
        if i1['itemType'] == "pets":
          ###
          if len(i1['isRide']) != 0 and len(i1['isFly']) == 0 and len(i1['isNeon']) == 0 and len(i1['isMega']) == 0:
            item.paste(pots['ride'], box=pots_place[0], mask=pots['ride'])

          elif len(i1['isFly']) != 0 and len(i1['isRide']) == 0 and len(i1['isNeon']) == 0 and len(i1['isMega']) == 0:
            item.paste(pots['fly'], box=pots_place[0], mask=pots['fly'])

          elif len(i1['isFly']) != 0 and len(i1['isRide']) != 0 and len(i1['isNeon']) == 0 and len(i1['isMega']) == 0:
            item.paste(pots['ride'], box=pots_place[0], mask=pots['ride'])
            item.paste(pots['fly'], box=pots_place[1], mask=pots['fly'])
          ###
          elif len(i1['isNeon']) != 0 and len(i1['isFly']) == 0 and len(i1['isRide']) == 0 and len(i1['isMega']) == 0:
            item.paste(pots['neon'], box=pots_place[0], mask=pots['neon'])
          
          elif len(i1['isNeon']) != 0 and len(i1['isRide']) != 0 and len(i1['isFly']) == 0 and len(i1['isMega']) == 0:
            item.paste(pots['ride'], box=pots_place[0], mask=pots['ride'])
            item.paste(pots['neon'], box=pots_place[1], mask=pots['neon'])

          elif len(i1['isNeon']) != 0 and len(i1['isFly']) != 0 and len(i1['isRide']) == 0 and len(i1['isMega']) == 0:
            item.paste(pots['fly'], box=pots_place[0], mask=pots['fly'])
            item.paste(pots['neon'], box=pots_place[1], mask=pots['neon'])

          elif len(i1['isNeon']) != 0 and len(i1['isFly']) != 0 and len(i1['isRide']) != 0 and len(i1['isMega']) == 0:
            item.paste(pots['ride'], box=pots_place[0], mask=pots['ride'])
            item.paste(pots['fly'], box=pots_place[1], mask=pots['fly'])
            item.paste(pots['neon'], box=pots_place[2], mask=pots['neon'])
          ###
          elif len(i1['isMega']) != 0 and len(i1['isFly']) == 0 and len(i1['isRide']) == 0 and len(i1['isNeon']) == 0:
            item.paste(pots['mega'], box=pots_place[0])
          
          elif len(i1['isMega']) != 0 and len(i1['isRide']) != 0 and len(i1['isFly']) == 0 and len(i1['isNeon']) == 0:
            item.paste(pots['ride'], box=pots_place[0], mask=pots['ride'])
            item.paste(pots['mega'], box=pots_place[1])

          elif len(i1['isMega']) != 0 and len(i1['isFly']) != 0 and len(i1['isRide']) == 0 and len(i1['isNeon']) == 0:
            item.paste(pots['fly'], box=pots_place[0], mask=pots['fly'])
            item.paste(pots['mega'], box=pots_place[1])

          elif len(i1['isMega']) != 0  and len(i1['isFly']) != 0 and len(i1['isRide']) != 0 and len(i1['isNeon']) == 0:
            item.paste(pots['ride'], box=pots_place[0], mask=pots['ride'])
            item.paste(pots['fly'], box=pots_place[1], mask=pots['fly'])
            item.paste(pots['mega'], box=pots_place[2])
          ###
        item = item.resize((76,76), Image.Resampling.LANCZOS)
        itembox.paste(item, mask=item)
        bg2.paste(itembox, box=items_place[itemcount])
        itemcount = itemcount+1

      elif resete == False:
        itembox = Image.open("itembox.png")
        itembox = itembox.convert(mode="RGB")
        item = Image.open(f"ImagesFolder/{i1['itemName']}.png")
        if i1['itemType'] == "pets":
          ###
          if len(i1['isRide']) != 0 and len(i1['isFly']) == 0 and len(i1['isNeon']) == 0 and len(i1['isMega']) == 0:
            item.paste(pots['ride'], box=pots_place[0], mask=pots['ride'])

          elif len(i1['isFly']) != 0 and len(i1['isRide']) == 0 and len(i1['isNeon']) == 0 and len(i1['isMega']) == 0:
            item.paste(pots['fly'], box=pots_place[0], mask=pots['fly'])

          elif len(i1['isFly']) != 0 and len(i1['isRide']) != 0 and len(i1['isNeon']) == 0 and len(i1['isMega']) == 0:
            item.paste(pots['ride'], box=pots_place[0], mask=pots['ride'])
            item.paste(pots['fly'], box=pots_place[1], mask=pots['fly'])
          ###
          elif len(i1['isNeon']) != 0 and len(i1['isFly']) == 0 and len(i1['isRide']) == 0 and len(i1['isMega']) == 0:
            item.paste(pots['neon'], box=pots_place[0], mask=pots['neon'])
          
          elif len(i1['isNeon']) != 0 and len(i1['isRide']) != 0 and len(i1['isFly']) == 0 and len(i1['isMega']) == 0:
            item.paste(pots['ride'], box=pots_place[0], mask=pots['ride'])
            item.paste(pots['neon'], box=pots_place[1], mask=pots['neon'])

          elif len(i1['isNeon']) != 0 and len(i1['isFly']) != 0 and len(i1['isRide']) == 0 and len(i1['isMega']) == 0:
            item.paste(pots['fly'], box=pots_place[0], mask=pots['fly'])
            item.paste(pots['neon'], box=pots_place[1], mask=pots['neon'])

          elif len(i1['isNeon']) != 0 and len(i1['isFly']) != 0 and len(i1['isRide']) != 0 and len(i1['isMega']) == 0:
            item.paste(pots['ride'], box=pots_place[0], mask=pots['ride'])
            item.paste(pots['fly'], box=pots_place[1], mask=pots['fly'])
            item.paste(pots['neon'], box=pots_place[2], mask=pots['neon'])
          ###
          elif len(i1['isMega']) != 0 and len(i1['isFly']) == 0 and len(i1['isRide']) == 0 and len(i1['isNeon']) == 0:
            item.paste(pots['mega'], box=pots_place[0])
          
          elif len(i1['isMega']) != 0 and len(i1['isRide']) != 0 and len(i1['isFly']) == 0 and len(i1['isNeon']) == 0:
            item.paste(pots['ride'], box=pots_place[0], mask=pots['ride'])
            item.paste(pots['mega'], box=pots_place[1])

          elif len(i1['isMega']) != 0 and len(i1['isFly']) != 0 and len(i1['isRide']) == 0 and len(i1['isNeon']) == 0:
            item.paste(pots['fly'], box=pots_place[0], mask=pots['fly'])
            item.paste(pots['mega'], box=pots_place[1])

          elif len(i1['isMega']) != 0  and len(i1['isFly']) != 0 and len(i1['isRide']) != 0 and len(i1['isNeon']) == 0:
            item.paste(pots['ride'], box=pots_place[0], mask=pots['ride'])
            item.paste(pots['fly'], box=pots_place[1], mask=pots['fly'])
            item.paste(pots['mega'], box=pots_place[2])
          ###
        item = item.resize((76,76), Image.Resampling.LANCZOS)
        itembox.paste(item, mask=item)
        bg.paste(itembox, box=items_place[itemcount])
        itemcount = itemcount+1
        bg.save(fp="finalimg.png")
    #bg.save(fp="finalimg.png")
    if resete == True:
      bg2.save(fp="finalimg2.png")
    file = discord.File("finalimg.png")
    file2 = discord.File("finalimg2.png")
    #file2 = discord.File("finalimg.png")
    #embed = discord.Embed(description=f"__**General Info**__\nTrade between **`{senderName}`** and **`{recName}`**.\nTrade Unique ID: [`{tradeID}`]", color=MAINCOLOR)
    channel = bot.get_channel(int(channelID))
    img_channel = bot.get_channel(IMAGECHANNEL_ID)
    if resete == False:
      image_msg = await img_channel.send(content=f"{channelID}\n{user2}\n{tradeID}", file=file)
    elif resete == True:
      image_msg = await img_channel.send(content=f"{channelID}\n{user2}\n{tradeID}", files=[file, file2])
          
    if resete == False:
      image_link = image_msg.attachments[0].url
      masa = await channel.send(f"> <@{buyerID}> Are those the items you are trading for? [.]({image_link})", view=isThisYourTrade())
    elif resete == True:
      image_link = image_msg.attachments[0].url
      image_link2 = image_msg.attachments[1].url
      masa = await channel.send(f"> <@{buyerID}> Are those the items you are trading for? [.]({image_link}) [.]({image_link2})", view=isThisYourTrade())
      
    AreThoseYourItems_List.append( {'msg_id': masa.id, 'tr_id': tradeID} )

@bot.command()
async def editpaste(ctx, msgid):
  if ctx.author.id in TicketAccess:
    msg = await ctx.channel.fetch_message(int(msgid))
    await msg.edit(view=PasteAddress())

class isTheTradeSuccessful(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
  @discord.ui.button(row=0, label="Proceed", style=discord.ButtonStyle.green, custom_id="tradeissucc", disabled=False)
  async def button_callback1(self, button, interaction):
    
    con,cur = openCON()
    cur.execute(f"SELECT * FROM channels WHERE channel_id='{interaction.channel.id}'")
    resSQL = cur.fetchall()[0]

    isKookie = False
    if interaction.user.id in TicketAccess:
      isKookie = True
    if isKookie == False:
      if interaction.user.id != resSQL['trader_seller_id']:
        await interaction.response.defer()
        return await interaction.channel.send(content=f"{interaction.user.mention} **You can't use this**", delete_after=2)
    
    for child in self.children:
      child.disabled = True
    await interaction.message.edit(view=self)

    try:
      await interaction.response.defer()
    except NotFound:
      pass

    await interaction.channel.send(embed=discord.Embed(description="<a:loading:1002330071043944501>  **Processing**  <a:loading:1002330071043944501>", color=grey), delete_after=3)

    await asyncio.sleep(3)

    IsThBeingUpdated = await bot.get_channel(IsThBeingUpdated_CHANNEL).fetch_message(IsThBeingUpdated_MESSAGE)
    if IsThBeingUpdated.content == "Yes":
      closeCON(cur,con)
      await interaction.message.edit(view=isTheTradeSuccessful())
      return await interaction.message.reply(embed=discord.Embed(description="<a:loading:1002330071043944501>  **The trade history is being updated, re-click this button**  <a:loading:1002330071043944501>", color=grey), delete_after=5)
    
    resSQL['trade_id'] = ast.literal_eval(resSQL['trade_id'])
    
    succ_num = resSQL['successful_trades_num']
    tradeID = resSQL['trade_id'][succ_num]
    sellerID = resSQL['trader_seller_id']
    buyerID = resSQL['trader_receiver_id']
    
    dbchannel = bot.get_channel(1002208531434450974)
    logsdata_msg = await dbchannel.fetch_message(1002209717923369030)
    file = logsdata_msg.attachments[0]
    cont = await file.read()
    tradehistory_data = ast.literal_eval(cont.decode('utf-8'))
    tradeids = []
    for i in tradehistory_data:
      tradeids.append(i['tradeID'])
    
    tradeFound = False
    if tradeID in tradeids:
      tradeFound = True

    TradeTabInfo = await readSendTradeTab()

    if (TradeTabInfo['tradeID'] != tradeID): # if im not trading with the person
      if tradeFound == False: # if the trade wasn't found in history
        resSQL['trade_id'][succ_num] = "No"
        resSQL['trade_id'] = str(resSQL['trade_id']).replace("'", "\"")
        cur.execute(f"UPDATE channels SET trade_id='{resSQL['trade_id']}' WHERE channel_id='{interaction.channel.id}'")
        closeCON(cur,con)
        return await interaction.channel.send(f"<@{sellerID}> Please use the `$send` command again.", embed=discord.Embed(description="<:redci:879849638855852112>  **The Trade Has Failed**  <:redci:879849638855852112>", color=redcolor))
    else:
      if tradeFound == False: # if trade not found in history
        closeCON(cur,con)
        await interaction.message.edit(view=isTheTradeSuccessful())
        return await interaction.message.reply(embed=discord.Embed(description="<a:loading:1002330071043944501>  **The Trade is Still Processing**  <a:loading:1002330071043944501>", color=grey), delete_after=3)
    
    selc_trades = resSQL['selected_trades_num']
    succ_trades = resSQL['successful_trades_num']
    succ_trades = succ_trades+1
    cur.execute(f"UPDATE channels SET successful_trades_num='{succ_trades}' WHERE channel_id='{interaction.channel.id}'")
    if selc_trades == succ_trades:
      cur.execute(f"UPDATE channels SET pets_received='Yes' WHERE channel_id='{interaction.channel.id}'")
      con.commit()
      closeCON(cur,con)
      await interaction.channel.send(embed=discord.Embed(title="<:succ:926608308033441792>  **The Bot Has Successfully Received The Items**  <:succ:926608308033441792>", color=MAINCOLOR))
      embed = discord.Embed(title="Next Steps", color=MAINCOLOR)
      embed.add_field(name="<:number_1:919632178671915139> - `First` - <:number_1:919632178671915139>  |  Buyer", value=f"> <@{buyerID}> Give/Pay your trader the promised items/money.", inline=False)
      embed.add_field(name="<:number_2:919632196908777523> - `Second` - <:number_2:919632196908777523>  | Seller", value=f"> <@{sellerID}> Use the `$confirm` command once your trader has given you your stuff.", inline=False)
      embed.add_field(name="<:number_3:919632227606880286> - `Third` - <:number_3:919632227606880286>  | Buyer", value=f"> <@{buyerID}> Join the VIP server via `$am` command and use `$redeem` cmd to withdraw your items.", inline=False)
      embed.add_field(name="Additional Commands", value=f"> `$inventory/$inv` - Sends an embed with the current items of the bot's inventory.\n> `$tradehistory/$th` - Sends you the trade history of the bot.", inline=False)
      await interaction.channel.send(embed=embed)
      return
    await interaction.channel.send(embed=discord.Embed(title="<:succ:926608308033441792>  **The Bot Has Successfully Received The Items**  <:succ:926608308033441792>", description="Use the `$send` command again and give the rest of the items to the bot.", color=MAINCOLOR))
    con.commit()
    closeCON(cur,con)

@tasks.loop(minutes=5)
async def inactive_tickets():
  con,cur = openCON()
  cur.execute(f"SELECT channel_id FROM channels WHERE ticket_status='Open' AND trade_stated='No'")
  resSQL = cur.fetchall()
  if len(resSQL) == 0:
    closeCON(cur,con)
    return
  for i in resSQL:
    c = bot.get_channel(int(i['channel_id']))
    if time.time() - c.created_at.timestamp() > 600:
      await c.delete()
  closeCON(cur,con)

@tasks.loop(hours=3)
async def tradeEdit():
  try:
    channel = bot.get_channel(1041179801827950662)
    msg = await channel.fetch_message(1044375052658946058)

    mainC = bot.get_channel(1057448251592290366)
    mainM = await mainC.fetch_message(1057454177145598042)

    if msg.content != mainM.embeds[0].description:
      embed = discord.Embed(description=msg.content, color=0x6704E8)
      await mainM.edit(embed=embed)
  except Exception:
    pass

@tasks.loop(hours=1)
async def subsChecker():
  users = []
  con,cur = openCON()
  curentTS = int(time.time())
  cur.execute(f"SELECT * FROM sub_tickets WHERE (ends_at+extended < {curentTS}) AND (status='Active')")
  resSQL = cur.fetchall()
  if len(resSQL) == 0:
    return

  cur.execute(f"UPDATE sub_tickets SET status='Expired' WHERE (ends_at+extended < {curentTS}) AND (status='Active')")
  con.commit()

  emb = discord.Embed(title="> __Subscribers Notification__", description="・**Your subscription has ended.**", color=0x6704e8)
  guild = bot.get_guild(GUILD_ID)
  subrole = guild.get_role(SUBSCRIBER_ROLE)
  cryptoLog = bot.get_channel(1038216652447305808)
  for i in resSQL:
    users.append(int(i['owner_id']))
    await cryptoLog.send(i)
    
  for i in users:
    try:
      user = guild.get_member(i)
      await user.remove_roles(subrole)
      dmchannel = await user.create_dm()
      await dmchannel.send(embed=emb)
      time.sleep(1)
    except Exception:
      pass

rainbow_colors_hex = [0xFF0000, # Red
                      0xFFA500, # Orange
                      0xFFFF00, # Yellow
                      0x008000, # Green
                      0x0000FF, # Blue
                      0x4B0082, # Indigo
                      0xEE82EE, # Violet
                      0xFFC0CB, # Pink
                      0xFF6347, # Tomato
                      0xFF4500, # Orange Red
                      0xFF8C00, # Dark Orange
                      0xFFD700, # Gold
                      0xFFFFE0, # Light Yellow
                      0x9ACD32, # Yellow Green
                      0x00FF7F, # Spring Green
                      0x00FA9A, # Medium Spring Green
                      0x00FFFF, # Cyan / Aqua
                      0x1E90FF, # Dodger Blue
                      0x8A2BE2, # Blue Violet
                      0x9400D3, # Dark Violet
                      0xBA55D3, # Medium Orchid
                      0xC71585, # Medium Violet Red
                      0xDB7093, # Pale Violet Red
                      0xFF69B4, # Hot Pink
                      0xFF1493, # Deep Pink
                      0xFF00FF, # Fuchsia / Magenta
                      0xFF00FF, # Purple (same as Fuchsia / Magenta)
                      0x6A5ACD, # Slate Blue
                      0x7B68EE, # Medium Slate Blue
                      0x9370DB, # Medium Purple
                      0x8B008B, # Dark Magenta
                      0x9400D3, # Dark Violet
                      0x9932CC, # Dark Orchid
                      0x8FBC8F, # Dark Sea Green
                      0x20B2AA, # Light Sea Green
                      0x00CED1, # Dark Turquoise
                      0x40E0D0, # Turquoise
                      0x48D1CC, # Medium Turquoise
                      0x008080, # Teal
                      0x2E8B57, # Sea Green
                      0x3CB371, # Medium Sea Green
                      0x66CDAA, # Medium Aquamarine
                      0x7FFFD4, # Aquamarine
                      0xB0E0E6, # Powder Blue
                      0xADD8E6, # Light Blue
                      0x87CEEB, # Sky Blue
                      0x87CEFA, # Light Sky Blue
                      0x00BFFF, # Deep Sky Blue
                      0x1E90FF, # Dodger Blue (same as earlier)
                      0x6495ED, # Cornflower Blue
                      0x7B68EE, # Medium Slate Blue (same as earlier)
                      0x4169E1, # Royal Blue
                      0x0000CD, # Medium Blue
                      0x00008B  # Dark Blue
                     ]

def mm_req_embed():
  async def func1():
    c1 = bot.get_channel(REQUEST_CHANNEL_ID)
    while True:
      try:
        for color in rainbow_colors_hex:
          msg1 = await c1.fetch_message(1081955630971101184)
          embed = msg1.embeds[0]
          embed.color = color
          await msg1.edit(embed=embed)
          await asyncio.sleep(5)
      except Exception:
        pass
      await asyncio.sleep(5)
  loop = bot.loop
  fut = asyncio.run_coroutine_threadsafe(func1(), loop)
  return fut.result()

@tasks.loop(seconds=30)
async def time_status():
    my_date = datetime.now(pytz.timezone('Europe/Berlin'))
    time = my_date.strftime('%I:%M %p')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"GMT+1: {time}"), status=discord.Status.dnd)

global guild1, guild2, impLogs

@bot.event
async def on_ready():  
    global guild1, guild2, impLogs
    
    guild1 = bot.get_guild(GUILD_ID)
    #guild2 = bot.get_guild(1081263064776716299)
    #impLogs = bot.get_channel(929644119691780156)
  
    bot.add_view(AMP_Tickets())
    bot.add_view(SellerOrBuyer())
    bot.add_view(Closed_Msgs())
    bot.add_view(Closed_Button())
    bot.add_view(Delete_Button_Before())
    bot.add_view(TradesAmount())
    bot.add_view(MUST_READ())
    bot.add_view(TurnOffNotifi())
    bot.add_view(WriteUserView())
    bot.add_view(TradeInfo())
    bot.add_view(PasteGamepass())
    bot.add_view(PasteAddress())
    bot.add_view(CancelTrade())
    #bot.add_view(CancelConfirmation())
    bot.add_view(OpenCancelTrade())

    #if not addsubs.is_running():
    #  addsubs.start()

    if not checkIfAccepted.is_running():
      checkIfAccepted.start()

    #if not inactive_tickets.is_running():
    #  inactive_tickets.start()

    if not checkTradesSucc.is_running():
      checkTradesSucc.start()

    #if not checkvouch.is_running():
    #  checkvouch.start()

    if not subsChecker.is_running():
      subsChecker.start()

    if not time_status.is_running():
      time_status.start()

    #threading.Thread(target=mm_req_embed).start()

    #await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Online"), status=discord.Status.online)
    print(f"Connected To Discord User: {bot.user.name}#{bot.user.discriminator}")


class TurnOffNotifi(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
  @discord.ui.button(row=0, label='Turn Off Notifications', style=discord.ButtonStyle.blurple, custom_id="turnoffnotifi", disabled=False)
  async def button_callback1(self, button, interaction):
    try:
      await interaction.response.send_message(content=f"**Prepearing..**", ephemeral=True)
    except NotFound:
      return
    users_list = await readNotifi()
    if interaction.user.id in users_list:
      return await interaction.edit_original_response(content=f"**You have already turned off your notifications.**")
    users_list.append(interaction.user.id)
    editNotifi(users_list)
    await interaction.edit_original_response(content=f"**Your notifications have been turned off.**")

class Off_AMP_Tickets(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
    button = discord.ui.Button(row=1, label='Buy Sub', style=discord.ButtonStyle.url, url=f"https://kookiepy.sellix.io/product/64cfcef34d653", disabled=True)
    self.add_item(button)
    
  @discord.ui.button(row=0, label='Create Ticket', style=discord.ButtonStyle.red, custom_id="amp_tickettt", disabled=True)
  async def button_callback1(self, button, interaction):        
    return
  #@discord.ui.button(row=0, label='Subscribe', style=discord.ButtonStyle.red, custom_id="amp_subsssc", disabled=True)
  #async def button_callback2(self, button, interaction):        
  #  return
  @discord.ui.button(row=0, label='FAQ', style=discord.ButtonStyle.red, custom_id="faqqqe", disabled=True)
  async def button_callback5(self, button, interaction):        
    return
    
  @discord.ui.button(row=0, label='Tutorial', style=discord.ButtonStyle.red, custom_id="tutoriaaalea", disabled=True)
  async def button_callback6(self, button, interaction):
    return  

  @discord.ui.button(row=1, label="Redeem Sub", style=discord.ButtonStyle.red, custom_id="RedeemSubBtn_idd", disabled=True)
  async def button_callback7(self, button, interaction2:discord.Interaction):
    return

class RedeemSubModal(Modal):
    def __init__(self, *args, **kwargs) -> None:
      super().__init__(*args, **kwargs)
      self.add_item(InputText(label="Serial Code:", min_length=40, max_length=40, required=True, style=discord.InputTextStyle.short))
    async def callback(self, interaction2: discord.Interaction):
        serial_code = self.children[0].value
        file = open("serials.txt", "r", encoding="utf8")
        file_content = file.read()
        file.close()
        serials_list = file_content.split("\n")
        if serial_code not in serials_list:
          try:
            await interaction2.response.send_message(content=f"**Serial is invalid.**", ephemeral=True)
          except Exception:
            return
          return

        con,cur = openCON()
        cur.execute(f"SELECT * FROM sub_tickets WHERE (serial='{serial_code}')")
        resSQL = cur.fetchall()
        serial_statement = len(resSQL) == 0
        if serial_statement == False: # serial found
          try:
            await interaction2.response.send_message(content=f"**Serial Has Already Been Redeemed.**", ephemeral=True)
          except Exception:
            return
          closeCON(cur,con)
          return

        cur.execute(f"SELECT * FROM sub_tickets WHERE (owner_id='{interaction2.user.id}') AND (status='Active')")
        resSQL2 = cur.fetchall()
        found_user = len(resSQL2) != 0
        if found_user == True:
          try:
            await interaction2.response.send_message(content=f"**You Already Have a Subscription Active.**", ephemeral=True)
          except Exception:
            return
          closeCON(cur,con)
          return
        
        boughtAt_ts = datetime.now();                 endsAt_ts = boughtAt_ts+timedelta(days=30)
        boughtAt_ts = int(boughtAt_ts.timestamp());   endsAt_ts = int(endsAt_ts.timestamp())
        cur.execute(f"INSERT INTO sub_tickets (owner_id, serial, bought_at, ends_at, extended) VALUES ('{interaction2.user.id}', '{serial_code}', '{boughtAt_ts}','{endsAt_ts}', '0')")
        con.commit()
        closeCON(cur,con)
        
        subrole = interaction2.guild.get_role(SUBSCRIBER_ROLE)
        await interaction2.user.add_roles(subrole)
        
        embed1 = discord.Embed(title="🟢 Sub Redeemed 🟢", description=f">>> Thank you for using our services!\nYour subscription will end on <t:{endsAt_ts}:f>\nYou can view your subscription information by typing the command `$sub` in commands channel, such info as expiration date, purchase date and additional extension time period will be displayed.", color=SUCCCOLOR)
        await interaction2.response.send_message(embed=embed1, ephemeral=True)
        
        embed = discord.Embed(title="🟢 Sub Redeemed 🟢", description=f"User: {interaction2.user.mention}\nSerial: {serial_code}\nType: Adopt Me\nStarted: <t:{boughtAt_ts}:f> `{boughtAt_ts}`\nEnds: <t:{endsAt_ts}:f> `{endsAt_ts}`", color=SUCCCOLOR)
        c = bot.get_channel(CRYPTO_LOGS)
        await c.send(embed=embed)

users_oncooldown = []

class AMP_Tickets(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
    button = discord.ui.Button(row=1, label='Buy Sub', style=discord.ButtonStyle.url, url=f"https://kookiepy.sellix.io/product/64cfcef34d653")
    self.add_item(button)
    
  @discord.ui.button(row=0, label='Create Ticket', style=discord.ButtonStyle.green, custom_id="amp_ticket", disabled=False)
  async def button_callback1(self, button, interaction):        
    global users_oncooldown
    verified = interaction.guild.get_role(1116136541656465462)
    
    try:
      await interaction.response.send_message(content=f"**Prepearing..**", ephemeral=True)
    except NotFound:
      return

    if verified not in interaction.user.roles:
      await interaction.edit_original_response(content=f"**You are not verified!**\n> Consider verifying from <#1104590684616400989> then try again.")
      return

    if interaction.user.id in users_oncooldown:
      return
    else:
      users_oncooldown.append(interaction.user.id)
      
      con,cur = openCON()
      cur.execute(f"SELECT * FROM channels WHERE (channel_owner_id='{interaction.user.id}') AND (ticket_status='Active' OR ticket_status='Open')")
      resSQL = cur.fetchall()
      has_ticket = len(resSQL)!=0
      
      if has_ticket == True:
        closeCON(cur,con)
        try:
          users_oncooldown.remove(interaction.user.id)
        except ValueError:
          pass
        await interaction.edit_original_response(content=f"**You Already Have a Ticket Created!** -> <#{resSQL[0]['channel_id']}>")
        return

      if has_ticket == False:
        await interaction.edit_original_response(content=f"**Creating ticket..**")

        guild = interaction.guild
        ticketlogs = bot.get_channel(AUTOAMP_LOGS_ID)
        ###
        tickets_category = bot.get_channel(AUTOAMP_CATEGORY_ID)
        ###
        tnrole = interaction.guild.get_role(TICKET_RENAMER_ROLE)
        mmTeamBadge = interaction.guild.get_role(1148742254673002598)
        staffBadge = interaction.guild.get_role(1148972169657856170)
        adminBadge = interaction.guild.get_role(1148968169462042664)
        ownerBadge = interaction.guild.get_role(1148972044151685251)
        
        overwrites = {
          guild.default_role: discord.PermissionOverwrite(view_channel=False),
          interaction.user: discord.PermissionOverwrite(send_messages=False, view_channel=True, attach_files=True, embed_links=True, read_message_history=True, use_slash_commands=True),
          tnrole: discord.PermissionOverwrite(view_channel=True, manage_channels=True),
          mmTeamBadge: discord.PermissionOverwrite(view_channel=None),
          staffBadge: discord.PermissionOverwrite(view_channel=None),
          adminBadge: discord.PermissionOverwrite(view_channel=None),
          ownerBadge: discord.PermissionOverwrite(view_channel=None),
        }
        cur.execute("SELECT * FROM ticket_count WHERE uni_id='1'")
        oldcount = cur.fetchall()[0]['count']
        count = oldcount+1
        cur.execute(f"UPDATE ticket_count SET count='{count}' WHERE uni_id='1'")
        con.commit()
        
        channel = await guild.create_text_channel(f"pending-{interaction.user.name}-{count}", category=tickets_category, overwrites=overwrites)
        await interaction.edit_original_response(content=f"**Ticket Created!** -> {channel.mention}")

        cur.execute(f"INSERT INTO channels (channel_id, channel_owner_id) VALUES ({channel.id}, {interaction.user.id})")
        cur.execute(f"INSERT INTO added_users (user_id, channel_id) VALUES ({interaction.user.id}, {channel.id})")
        con.commit()
        closeCON(cur,con)
        
        try:
          users_oncooldown.remove(interaction.user.id)
        except ValueError:
          pass
        
        logembed = discord.Embed(description=f"Author: **{interaction.user.name}#{interaction.user.discriminator}** | ID: {interaction.user.id}\nTicket: **{channel.name}** | ID: {channel.id}\nAction: **Created Ticket**", color=0x57f287)
        logembed.set_author(name=f"{interaction.user.name}#{interaction.user.discriminator}", icon_url=f"{interaction.user.display_avatar.url}")
        await ticketlogs.send(embed=logembed)
        embed = discord.Embed(title="<a:wave:1101249815892996228>﹒Jace's Middleman Service", description=f"━━━━━━━━━━━━━━━━━━\nHello {interaction.user.mention}! Welcome to our automated middleman service.\nPlease follow the steps below to complete your cross-trade transaction.",color=MAINCOLOR)
        embed.set_footer(icon_url=f'{interaction.user.display_avatar.url}', text=f'{interaction.user} | {interaction.user.id}')
        await channel.send(f"{interaction.user.mention}", embed=embed, view=Delete_Button_Before())
        await asyncio.sleep(1)
        embed2 = discord.Embed(title="<:role:1101255852482117762>・Select your role", description=">>> Select:\n\"__**Seller**__\" if you are __giving__ items to the bot.\n\"__**Buyer**__\" if you are __not giving__ items to the bot", color=MAINCOLOR)
        embed2.set_footer(text="Selected: ")
        await channel.send(embed=embed2, view=SellerOrBuyer())

  #@discord.ui.button(row=0, label='Subscription Benefits', style=discord.ButtonStyle.red, custom_id="subBenifi", disabled=False)
  #async def button_callback4(self, button, interaction):        

  #  emb1 = discord.Embed(title="> __Subscription Benefits__", description=f"・**Free usage for 30 days of our automated services.**\n\n・**<@&{SUBSCRIBER_ROLE}> Role**", color=0xa340ff)

  #  try:
  #    await interaction.response.send_message(embed=emb1, ephemeral=True)
  #  except NotFound:
  #    return
  
  #@discord.ui.button(row=0, label='Subscribe', style=discord.ButtonStyle.red, custom_id="amp_subscribe", disabled=False)
  #async def button_callback3(self, button, interaction):        
  #  global users_oncooldown

  #  try:
  #    await interaction.response.send_message(content=f"**Prepearing..**", ephemeral=True)
  #  except NotFound:
  #    return

  #  if interaction.user.id in users_oncooldown:
  #    return
  #  else:
  #    users_oncooldown.append(interaction.user.id)

  #    con,cur = openCON()
  #    cur.execute(f"SELECT * FROM sub_tickets WHERE (channel_owner_id='{interaction.user.id}') AND (ticket_status='Active')")
  #    resSQL = cur.fetchall()
  #    has_ticket = len(resSQL)!=0
  #    
  #    if has_ticket == True:
  #      closeCON(cur,con)
  #      try:
  #        users_oncooldown.remove(interaction.user.id)
  #      except ValueError:
  #        pass
  #      await interaction.edit_original_response(content=f"**You Already Have a Ticket Created!** -> <#{resSQL[0]['channel_id']}>")
  #      return

  #    subsList = await readSubs()
  #    for subi in subsList:
  #      if subi['userID'] == interaction.user.id:
  #        closeCON(cur,con)
  #        await interaction.edit_original_response(content=f"**You Have Aready Subscribed!**")
  #        return

  #    if has_ticket == False:    
  #      await interaction.edit_original_response(content=f"**Creating ticket..**")
  #      
  #      guild = interaction.guild
  #      ticketlogs = bot.get_channel(MMPASS_LOGS_ID)
  #      ###
  #      tickets_category = bot.get_channel(MMPASS_CATEGORY_ID)
  #      ###
  #      tnrole = interaction.guild.get_role(TICKET_RENAMER_ROLE)
  #      overwrites = {
  #        guild.default_role: discord.PermissionOverwrite(view_channel=False),
  #        interaction.user: discord.PermissionOverwrite(send_messages=True, view_channel=True, attach_files=True, embed_links=True, read_message_history=True, use_slash_commands=True),
  #        tnrole: discord.PermissionOverwrite(view_channel=True, manage_channels=True)
  #      }
  #      
  #      channel = await guild.create_text_channel(f"sub-{interaction.user.id}", category=tickets_category, overwrites=overwrites)
  #      await interaction.edit_original_response(content=f"**Ticket Created!** -> {channel.mention}")

  #      embed = discord.Embed(title="<a:wave:1101249815892996228>・Jace's Middleman Service", description=f"━━━━━━━━━━━━━━━━━━\nHello {interaction.user.mention}! Welcome to our automated middleman service.",color=MAINCOLOR)
  #      embed.set_footer(icon_url=f'{interaction.user.display_avatar.url}', text=f'{interaction.user} | {interaction.user.id}')
  #      await channel.send(f"{interaction.user.mention}", embed=embed, view=Delete_Button_Before())

  #      key = PrivateKey()
  #      wif = key.to_wif()
  #      usdprice = float(sessionCheck.get('https://blockchain.info/ticker').json()['USD']['last'])
  #      usd_sat = int(currency_to_satoshi(5, "usd"))
  #      btc_amount = float(satoshi_to_currency(usd_sat, "btc"))
  #      embinfo = discord.Embed(title="", description=f"> **Before you subscribe to our automated middleman service, there are things that you should know and terms to follow.**\n\n**・__ToS__**\n> Once you subscribe, there is no going back, therefore we will not refund you what you have paid under any circumstances.\n・\n> There may be times when we turn off the bot for like a day, which the reason could be for maintenance or implementing new features or because Roblox is down. During these times, your subscription will be extended according to the period of time the bot was offline. So if the bot was offline for a day, your subscription will be extended by one day.\n・\n> You have to keep in your mind, that this service will not last forever. Although we would inform you a month beforehand in case we wanted to discontinue the service.\n・\n> The server rules apply here as well, so if you break any rules and get banned for it then it's your problem. Subscribing to our automated service will not give you immunity against getting banned.\n\n**・__Benefits__**\n> - Free usage for 30 days of our automated services.\n> - <@&{SUBSCRIBER_ROLE}> Role.\n> More features are coming soon if you guys continue to support us :D", color=MAINCOLOR)
  #      embed2 = discord.Embed(title="Payment Information",description=f"Please consider reading the information sent above before paying, if you changed your mind then you may close the ticket with the button that was sent at the very top.\nClick the **Paid** button once you have sent the funds to the payment address.", color=MAINCOLOR)
  #      embed2.add_field(name="USD Amount", value=f"$5.00", inline=True)
  #      embed2.add_field(name="Crypto Amount (BTC)", value=f"{btc_amount}", inline=True)
  #      embed2.add_field(name="Payment Address", value=f"```{key.address}```", inline=False)
  #      embed2.set_footer(text=f"Current BTC Price = ${usdprice}")
  #      await channel.send(interaction.user.mention, embeds=[embinfo,embed2], view=PasteAddress())

  #      cryptoLogs = bot.get_channel(CRYPTO_LOGS)
  #      msgeea = await cryptoLogs.send(embed=discord.Embed(title="⚪ Payment Started ⚪", description=f"Type: Subscription\nChannel: {channel.mention} {channel.id}\nUser: {interaction.user.mention}\nWIF: {wif}\nAddress: {key.address}\nUSD: $5.00\nBTC: {btc_amount}", color=0xf8f8f8))

  #      cur.execute(f"INSERT INTO sub_tickets (channel_id, channel_owner_id, crypto_address, crypto_wif, btc_amount, usd_price, message_id) VALUES ({channel.id}, {interaction.user.id}, '{key.address}', '{wif}', {btc_amount}, {usdprice}, {msgeea.id})")
  #      con.commit()
  #      closeCON(cur,con)
  #      
  #      try:
  #        users_oncooldown.remove(interaction.user.id)
  #      except ValueError:
  #        pass
  #      
  #      logembed = discord.Embed(description=f"Author: **{interaction.user.name}#{interaction.user.discriminator}** | ID: {interaction.user.id}\nTicket: **{channel.name}** | ID: {channel.id}\nAction: **Created Ticket**", color=0x57f287)
  #      logembed.set_author(name=f"{interaction.user.name}#{interaction.user.discriminator}", icon_url=f"{interaction.user.display_avatar.url}")
  #      await ticketlogs.send(embed=logembed)

  @discord.ui.button(row=0, label='FAQ', style=discord.ButtonStyle.gray, custom_id="faqqq", disabled=False)
  async def button_callback5(self, button, interaction):        

    embed2 = discord.Embed(title="> __? FAQ ?__", description="・**How does this bot work?**\n*╰-> The bot holds the adopt me items until both traders are done with their transaction.*\nㅤㅤ*__Steps__:*\nㅤㅤ`1.` - The trader gives the bot the adopt me items by typing `$send` in Roblox chat.\nㅤㅤ`2.` - The buyer accepts the trade in the ticket chat.\nㅤㅤ`3.` - Both traders will do the 2nd part of their transaction.\nㅤㅤ`4.` - The seller confirms the trade by typing `$confirm`.\nㅤㅤ`5.` - The buyer redeems their items by typing `$redeem` in Roblox chat.\n\n・**How do I cancel the trade / get my items back / I am facing problems?**\n*╰-> Ping <@358594990982561792> and they will handle it.*\nㅤㅤㅤㅤ*(**do not ping** any other staff member)*\n\n・**My seller is not confirming the trade although I paid them?**\n*╰-> Ping <@358594990982561792> and they will handle it.*\nㅤㅤㅤㅤ*(**do not ping** any other staff member)*\nㅤㅤ*(make sure you have evidence of the payment)*", color=MAINCOLOR)
    
    try:
      await interaction.response.send_message(embed=embed2, ephemeral=True)
    except NotFound:
      return
    
  @discord.ui.button(row=0, label='Tutorial', style=discord.ButtonStyle.red, custom_id="tutoriaaale", disabled=False)
  async def button_callback6(self, button, interaction):        
    try:
      await interaction.response.send_message("https://www.youtube.com/watch?v=xwln6aX-Szw", ephemeral=True)
    except NotFound:
      return
    
  @discord.ui.button(row=1, label="Redeem Sub", style=discord.ButtonStyle.primary, custom_id="RedeemSubBtn_id")
  async def button_callback7(self, button, interaction2:discord.Interaction):
      modal = RedeemSubModal(title="Paste your serial code.")
      try:
        await interaction2.response.send_modal(modal)
      except Exception:
        return

class Delete_Button_Before(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
  @discord.ui.button(row=0, label='﹒delete ticket', style=discord.ButtonStyle.red, custom_id="delete_before_autots", disabled=False, emoji="🔒")
  async def button_callback3(self, button, interaction):

    if interaction.channel.category.id == MMPASS_CATEGORY_ID:      
      for child in self.children:
        child.disabled = True
      await interaction.message.edit(view=self)

      try:
        await interaction.response.defer()
      except NotFound:
        pass

      transcripts = bot.get_channel(MMPASS_TRANSCRIPTS_ID)
      ticketlogs = bot.get_channel(MMPASS_LOGS_ID)
      
      con,cur = openCON()
      cur.execute(f"SELECT * FROM sub_tickets WHERE channel_id='{interaction.channel.id}'")
      resSQL = cur.fetchall()[0]
      closeCON(cur,con)

      channelownerid = resSQL['channel_owner_id']
      crypto_address = resSQL['crypto_address']
      usd_amount = resSQL['usd_amount']
      btc_amount = resSQL['btc_amount']
      usd_price = resSQL['usd_price']
      msg_id = resSQL['message_id']

      transcript = await chat_exporter.export(channel=interaction.channel, limit=None, tz_info="Asia/Singapore")
      if transcript is None:
        return
      transcript_file = discord.File(io.BytesIO(transcript.encode()), filename=f"transcript-{interaction.channel.name}.html")
      transcriptembed = discord.Embed(color=0x1EC45C)
      transcriptembed.add_field(name="Ticket", value=f"{interaction.channel.name} | {interaction.channel.id}", inline=True)
      transcriptembed.add_field(name="Category", value=f"{interaction.channel.category.name} | {interaction.channel.category.id}", inline=True)
      transcriptembed.add_field(name="Info", value=f"Owner: <@{channelownerid}>\nAddress: {crypto_address}\nUSD: {usd_amount}\nBTC: {btc_amount}\nUSD Price: {usd_price}\nMessage ID: {msg_id}", inline=False)
      mess = await transcripts.send(embed=transcriptembed, file=transcript_file)
      attachment = mess.attachments[0]
      messages = await interaction.channel.history(limit=None).flatten()
      users={}
      for msg in messages[::1]:
          if msg.author.id in users.keys():
            users[msg.author.id]+=1
          else:
            users[msg.author.id]=1
      user_string,user_transcript_string="",""
      b = sorted(users.items(), key=lambda x: x[1], reverse=True)
      try:
        for k in b:
          user = await bot.fetch_user(int(k[0]))
          user_string+=f"{k[1]} | {user.mention} | {user.name}#{user.discriminator}\n"
      except NotFound:
        pass
      await mess.edit(embed=transcriptembed.add_field(name="**Direct Transcript**", value=f"[Direct Transcript](https://mahto.id/chat-exporter?url={attachment.url})", inline=True))
      await mess.edit(embed=transcriptembed.add_field(name="**Users in transcript**", value=f"{user_string}", inline=True))
      await interaction.channel.delete()

      logembed = discord.Embed(color=MAINCOLOR)
      logembed = discord.Embed(description=f"Author: **{interaction.user.name}#{interaction.user.discriminator}** | ID: {interaction.user.id}\nTicket: **{interaction.channel.name}** | ID: {interaction.channel.id}\nAction: **Deleted Ticket**", color=0xed4245)
      logembed.set_author(name=f"{interaction.user.name}#{interaction.user.discriminator}", icon_url=f"{interaction.user.display_avatar.url}")
      await ticketlogs.send(embed=logembed)
      return

    con,cur = openCON()
    cur.execute(f"SELECT * FROM channels WHERE channel_id='{interaction.channel.id}'")
    resSQL = cur.fetchall()[0]
    closeCON(cur,con)

    if resSQL['ticket_status'] == "Open" and resSQL['trade_stated'] == "No":
      for child in self.children:
        child.disabled = True
      await interaction.message.edit(view=self)

      try:
        await interaction.response.defer()
      except NotFound:
        pass

      await interaction.channel.delete()

      ticketlogs = bot.get_channel(AUTOAMP_LOGS_ID)
      logembed = discord.Embed(color=MAINCOLOR)
      logembed = discord.Embed(description=f"Author: **{interaction.user.name}#{interaction.user.discriminator}** | ID: {interaction.user.id}\nTicket: **{interaction.channel.name}** | ID: {interaction.channel.id}\nAction: **Deleted Ticket**", color=0xed4245)
      logembed.set_author(name=f"{interaction.user.name}#{interaction.user.discriminator}", icon_url=f"{interaction.user.display_avatar.url}")
      await ticketlogs.send(embed=logembed)
    else:
      for child in self.children:
        child.disabled = True
      await interaction.message.edit(view=self)

      try:
        await interaction.response.defer()
      except NotFound:
        pass


class Closed_Button(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
  @discord.ui.button(row=0, label='﹒close', style=discord.ButtonStyle.blurple, custom_id="close_autots", disabled=False, emoji="🔒")
  async def button_callback3(self, button, interaction):

    for child in self.children:
      child.disabled = True
    await interaction.message.edit(view=self)

    try:
      await interaction.response.defer()
    except NotFound:
      pass

    con,cur = openCON()
    cur.execute(f"SELECT * FROM channels WHERE channel_id='{interaction.channel.id}'")
    resSQL = cur.fetchall()[0]
    resSQL['redeem_trade_id'] = ast.literal_eval(resSQL['redeem_trade_id'])

    tradehistory = bot.get_channel(1002208531434450974)
    logsdata_msg = await tradehistory.fetch_message(1002209717923369030)
    file = logsdata_msg.attachments[0]
    cont = await file.read()
    tradehistory_data = ast.literal_eval(cont.decode('utf-8'))
    tradeids = []
    for i in tradehistory_data:
      tradeids.append(i['tradeID'])
    
    tradeID = resSQL['redeem_trade_id'][-1]

    tradeFound = False
    if tradeID in tradeids:
      tradeFound = True

    if tradeFound == True: # if the trade found in history
      cur.execute(f"UPDATE channels SET gave_redeemer='Yes' WHERE channel_id='{interaction.channel.id}'")
      con.commit()
    else:
      cur.execute(f"UPDATE channels SET gave_redeemer='No' WHERE channel_id='{interaction.channel.id}'")
      con.commit()
      closeCON(cur,con)
      await interaction.message.edit(view=Closed_Button())
      return

    rolereq = MM_ROLE_ID
    Toggle = True
    if str(resSQL['ticket_status']) == "Closed" or str(resSQL['ticket_status']) == "Delete":
      closeCON(cur,con)
      await interaction.message.reply("*Ticket is already closed!*", delete_after=3)
      Toggle = False
      await interaction.message.edit(view=Closed_Button())
      return
    if Toggle == True:
      ticketlogs = bot.get_channel(AUTOAMP_LOGS_ID)
      for i in interaction.channel.overwrites:
        if type(i) == discord.member.Member:
          irolelistid = []
          for i2 in i.roles:
            irolelistid.append(i2.id)
          if rolereq not in irolelistid:
            await interaction.channel.set_permissions(i, overwrite=None)
      logembed = discord.Embed(description=f"Author: **{interaction.user.name}#{interaction.user.discriminator}** | ID: {interaction.user.id}\nTicket: **{interaction.channel.name}** | ID: {interaction.channel.id}\nAction: **Closed Ticket**", color=0xFFEE58)
      logembed.set_author(name=f"{interaction.user.name}#{interaction.user.discriminator}", icon_url=f"{interaction.user.display_avatar.url}")
      await ticketlogs.send(embed=logembed)
      msg1 = await interaction.channel.send(embed=discord.Embed(description=f"***{interaction.user.mention} closed the ticket***", color=0xFFEE58), view=Closed_Msgs())
      
      cur.execute(f"UPDATE channels SET ticket_status='Closed', closed_msg_id='{msg1.id}' WHERE channel_id='{interaction.channel.id}'")
      con.commit()
      closeCON(cur,con)
      
      closedcat = bot.get_channel(CLOSED_CATEGORY_ID)
      await interaction.channel.edit(category=closedcat)

class Closed_Msgs(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
  @discord.ui.button(row=0, label='﹒delete', style=discord.ButtonStyle.red, custom_id="deleteticket", disabled=False, emoji="<a:No:914566121460486184>")
  async def button_callback1(self, button, interaction):
    for child in self.children:
      child.disabled = True
    await interaction.message.edit(view=self)

    try:
      await interaction.response.defer()
    except NotFound:
      pass

    transcripts = bot.get_channel(AUTOAMP_TRANSCRIPTS_ID)
    ticketlogs = bot.get_channel(AUTOAMP_LOGS_ID)
    users = {}

    await interaction.channel.send(embed=discord.Embed(description=f'Deleting this ticket..', color=0x303135))

    con,cur = openCON()
    cur.execute(f"SELECT * FROM channels WHERE channel_id='{interaction.channel.id}'")
    resSQL = cur.fetchall()[0]

    channelownerid = resSQL['channel_owner_id']
    sellerid = resSQL['trader_seller_id']
    buyerid = resSQL['trader_receiver_id']
    tradeid1 = resSQL['trade_id']
    tradeid2 = resSQL['redeem_trade_id']
    recuser = resSQL['receiver_username']
    senduser = resSQL['seller_username']
    passid = resSQL['gamepass_id']

    Status = True
    transcript = await chat_exporter.export(channel=interaction.channel, limit=None, tz_info="Asia/Singapore")
    if str(resSQL['ticket_status']) == "Delete":
      closeCON(cur,con)
      await interaction.message.reply("*The ticket is already being deleted!*")
      Status = False
      return
    if Status == True:
      cur.execute(f"UPDATE channels SET ticket_status='Delete' WHERE channel_id='{interaction.channel.id}'")
      con.commit()
      closeCON(cur,con)

      await interaction.message.delete()
      logembed = discord.Embed(description=f"Author: **{interaction.user.name}#{interaction.user.discriminator}** | ID: {interaction.user.id}\nTicket: **{interaction.user.name}** | ID: {interaction.user.id}\nAction: **Deleted Ticket**", color=0xed4245)
      logembed.set_author(name=f"{interaction.user.name}#{interaction.user.discriminator}", icon_url=f"{interaction.user.display_avatar.url}")
      await ticketlogs.send(embed=logembed)
      if transcript is None:
        return
      transcript_file = discord.File(io.BytesIO(transcript.encode()), filename=f"transcript-{interaction.channel.name}.html")
      transcriptembed = discord.Embed(color=0x1EC45C)
      transcriptembed.add_field(name="Author", value=f"{interaction.user.mention} | {interaction.user.id}", inline=True)
      transcriptembed.add_field(name="Ticket", value=f"{interaction.channel.name} | {interaction.channel.id}", inline=True)
      transcriptembed.add_field(name="Category", value=f"{interaction.channel.category.name} | {interaction.channel.category.id}", inline=True)
      transcriptembed.add_field(name="Info", value=f"Owner: <@{channelownerid}>\nSeller: <@{sellerid}>\nBuyer: <@{buyerid}>\nFirst Trade ID: {tradeid1}\nSecond Trade ID: {tradeid2}\nSender Username: `{senduser}`\nReceiver Username: `{recuser}`\nGamepass ID: `{passid}`", inline=False)
      mess = await transcripts.send(embed=transcriptembed, file=transcript_file)
      attachment = mess.attachments[0]
      messages = await interaction.channel.history(limit=None).flatten()
      for msg in messages[::1]:
          if msg.author.id in users.keys():
            users[msg.author.id]+=1
          else:
            users[msg.author.id]=1
      user_string,user_transcript_string="",""
      b = sorted(users.items(), key=lambda x: x[1], reverse=True)
      try:
        for k in b:
          user = await bot.fetch_user(int(k[0]))
          user_string+=f"{k[1]} | {user.mention} | {user.name}#{user.discriminator}\n"
      except NotFound:
        pass
      await mess.edit(embed=transcriptembed.add_field(name="**Direct Transcript**", value=f"[Direct Transcript](https://mahto.id/chat-exporter?url={attachment.url})", inline=True))
      await mess.edit(embed=transcriptembed.add_field(name="**Users in transcript**", value=f"{user_string}", inline=True))
      await interaction.channel.delete()

  @discord.ui.button(row=0, label='﹒reopen', style=discord.ButtonStyle.grey, custom_id="reopenticket", disabled=False, emoji="<:aero_unlock:914566214859255879>")
  async def button_callback2(self, button, interaction):
    for child in self.children:
      child.disabled = True
    await interaction.message.edit(view=self)

    try:
      await interaction.response.defer()
    except NotFound:
      pass

    guild = interaction.message.guild
    ticketlogs = bot.get_channel(AUTOAMP_LOGS_ID)

    con,cur = openCON()
    cur.execute(f"SELECT * FROM channels WHERE channel_id='{interaction.channel.id}'")
    resSQL = cur.fetchall()[0]

    cur.execute(f"SELECT user_id FROM added_users WHERE channel_id='{interaction.channel.id}'")
    added_users = cur.fetchall()

    guild = interaction.message.guild
    cat = bot.get_channel(AUTOAMP_CATEGORY_ID)
    try:
      closed_msg = await interaction.channel.fetch_message(int(resSQL['closed_msg_id']))
      await closed_msg.delete()
    except NotFound:
      pass
    await interaction.channel.edit(category=cat)
    for y in added_users:
      users = guild.get_member(int(y['user_id']))
      await interaction.channel.set_permissions(users, send_messages=True, view_channel=True, attach_files=True, embed_links=True, read_message_history=True, use_slash_commands=True)
    await interaction.channel.send(f"*{interaction.user.mention} Reopened the ticket*")
    logembed = discord.Embed(description=f"Author: **{interaction.user.name}#{interaction.user.discriminator}** | ID: {interaction.user.id}\nTicket: **{interaction.channel.name}** | ID: {interaction.channel_id}\nAction: **Reopened Ticket**", color=0x29B5F6)
    logembed.set_author(name=f"{interaction.user.name}#{interaction.user.discriminator}", icon_url=f"{interaction.user.display_avatar.url}")
    await ticketlogs.send(embed=logembed)
    
    cur.execute(f"UPDATE channels SET ticket_status='Active', closed_msg_id='0' WHERE channel_id='{interaction.channel.id}'")
    con.commit()
    closeCON(cur,con)

  @discord.ui.button(row=0, label='﹒save transcript', style=discord.ButtonStyle.blurple, custom_id="savets", disabled=False, emoji="<:savets:914566985327726614>")
  async def button_callback3(self, button, interaction):
    for child in self.children:
      child.disabled = True

    transcripts = bot.get_channel(AUTOAMP_TRANSCRIPTS_ID)
    loading_embed = discord.Embed(color = 0xffffff)
    loading_embed.set_author(name="Loading Chat, Users, Messages and Time!", icon_url="https://cdn.discordapp.com/emojis/806591946730504212.gif?v=1 ")
    users={}

    con,cur = openCON()
    cur.execute(f"SELECT * FROM channels WHERE channel_id='{interaction.channel.id}'")
    resSQL = cur.fetchall()[0]
    closeCON(cur,con)

    await interaction.message.edit(view=self)

    channelownerid = resSQL['channel_owner_id']
    sellerid = resSQL['trader_seller_id']
    buyerid = resSQL['trader_receiver_id']
    tradeid1 = resSQL['trade_id']
    tradeid2 = resSQL['redeem_trade_id']
    recuser = resSQL['receiver_username']
    senduser = resSQL['seller_username']
    passid = resSQL['gamepass_id']

    await interaction.response.send_message(content=f"{interaction.user.mention}", embed=loading_embed, ephemeral=False)
    transcript = await chat_exporter.export(channel=interaction.channel, limit=None, tz_info="Asia/Singapore")
    if transcript is None:
      return
    transcript_file = discord.File(io.BytesIO(transcript.encode()), filename=f"transcript-{interaction.channel.name}.html")
    transcriptembed = discord.Embed(color=0x1EC45C)
    transcriptembed.add_field(name="Author", value=f"{bot.user.mention} | {bot.user.id}", inline=True)
    transcriptembed.add_field(name="Ticket", value=f"{interaction.channel.name} | {interaction.channel.id}", inline=True)
    transcriptembed.add_field(name="Category", value=f"{interaction.channel.category.name} | {interaction.channel.category.id}", inline=True)
    transcriptembed.add_field(name="Info", value=f"Owner: <@{channelownerid}>\nSeller: <@{sellerid}>\nBuyer: <@{buyerid}>\nFirst Trade ID: {tradeid1}\nSecond Trade ID: {tradeid2}\nSender Username: `{senduser}`\nReceiver Username: `{recuser}`\nGamepass ID: `{passid}`", inline=False)
    mess = await transcripts.send(embed=transcriptembed, file=transcript_file)
    attachment = mess.attachments[0]
    messages = await interaction.channel.history(limit=None).flatten()
    user_string,user_transcript_string="",""
    for msge in messages[::1]:
        if msge.author.id in users.keys():
          users[msge.author.id]+=1
        else:
          users[msge.author.id]=1
    b = sorted(users.items(), key=lambda x: x[1], reverse=True)
    try:
      for k in b:
        user = await bot.fetch_user(int(k[0]))
        user_string+=f"{k[1]} | {user.mention} | {user.name}#{user.discriminator}\n"
    except NotFound:
      pass
    await mess.edit(embed=transcriptembed.add_field(name="**Direct Transcript**", value=f"[Direct Transcript](https://mahto.id/chat-exporter?url={attachment.url})", inline=True))
    await mess.edit(embed=transcriptembed.add_field(name="**Users in transcript**", value=f"{user_string}", inline=True))
    loading_embed1 = discord.Embed(description=f"**Transcript was saved in <#{AUTOAMP_TRANSCRIPTS_ID}>**",color = 0xffffff)
    await interaction.edit_original_response(content=f"{interaction.user.mention}", embed=loading_embed1)
    await interaction.message.edit(view=Closed_Msgs())

class WriteUserView(discord.ui.View):
  def __init__(self):
      super().__init__(timeout=None)
  @discord.ui.button(label="Input Username", style=discord.ButtonStyle.primary, custom_id="writeusername")
  async def button_callback1(self, button, interaction:discord.Interaction):
      modal = WriteUserModal(title="Write here your own username!")
      try:
        await interaction.response.send_modal(modal)
      except Exception:
        return


class WriteUserModal(Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_item(InputText(label="Your Username", min_length=3, max_length=20, required=True, style=discord.InputTextStyle.short))

    async def callback(self, interaction: discord.Interaction):
        username = str(self.children[0].value)

        if interaction.user.id != interaction.message.mentions[0].id:
          return await interaction.response.send_message(content="You can't use this!", ephemeral=True)

        con,cur = openCON()
        cur.execute(f"SELECT * FROM channels WHERE channel_id='{interaction.channel.id}'")
        resSQL = cur.fetchall()[0]

        await interaction.message.edit(view=None)
        await interaction.response.send_message(content=f"**Saving Username..**", ephemeral=True)

        sessionCheck = getrbxSession()

        if resSQL['trader_added'] == "Yes":
          if resSQL['receiver_username'] == "No" or resSQL['seller_username'] == "No":

            if resSQL['receiver_username'] == "No":
              traderType = "receiver"
            elif resSQL['seller_username'] == "No":
              traderType = "seller"

            json_data = {
                'usernames': [
                    username,
                ],
                'excludeBannedUsers': True,
            }
            res = sessionCheck.post('https://users.roblox.com/v1/usernames/users', json=json_data)
            if len(res.json()['data']) == 0:
              closeCON(cur,con)
              try:
                await interaction.edit_original_response(embed=discord.Embed(description="<:redci:879849638855852112>  **The username was not found, please try again**  <:redci:879849638855852112>", color=redcolor))
                await interaction.message.edit(view=WriteUserView())
              except Exception:
                pass
              return

            okeuser = res.json()['data'][0]['name']

            if traderType == "seller":
              cur.execute(f"SELECT channel_id FROM channels WHERE (ticket_status='Open' OR ticket_status='Active' OR ticket_status='Pending') AND (seller_username='{okeuser}' OR receiver_username='{okeuser}')")
              resSQL2 = cur.fetchall()
              user_found = len(resSQL2) != 0
              if user_found == True:
                closeCON(cur,con)
                try:
                  await interaction.edit_original_response(embed=discord.Embed(description="<:redci:879849638855852112>  **The username has already been used! Please use another username or close your other ticket.**  <:redci:879849638855852112>", color=redcolor))
                  await interaction.message.edit(view=WriteUserView())
                except Exception:
                  pass
                return

              cur.execute(f"UPDATE channels SET seller_username='{okeuser}' WHERE channel_id='{interaction.channel.id}'")
            elif traderType == "receiver":
              cur.execute(f"SELECT channel_id FROM channels WHERE (ticket_status='Open' OR ticket_status='Active' OR ticket_status='Pending') AND (seller_username='{okeuser}' OR receiver_username='{okeuser}')")
              resSQL2 = cur.fetchall()
              user_found = len(resSQL2) != 0
              if user_found == True:
                closeCON(cur,con)
                try:
                  await interaction.edit_original_response(embed=discord.Embed(description="<:redci:879849638855852112>  **The username has already been used! Please use another username or close your other ticket.**  <:redci:879849638855852112>", color=redcolor))
                  await interaction.message.edit(view=WriteUserView())
                except Exception:
                  pass
                return

              cur.execute(f"UPDATE channels SET receiver_username='{okeuser}' WHERE channel_id='{interaction.channel.id}'")

            timenow = datetime.now()
            timenow = int(timenow.timestamp())

            cur.execute(f"UPDATE channels SET trade_stated='Yes', ticket_status='Active', timestarted='{timenow}', has_paid_fee='No' WHERE channel_id='{interaction.channel.id}'")
            con.commit()
            closeCON(cur,con)
            
            await interaction.edit_original_response(embed=discord.Embed(title="<:succ:926608308033441792>  **Username Has Been Saved**  <:succ:926608308033441792>", color=MAINCOLOR))
            await interaction.message.edit(view=None)
            await interaction.channel.set_permissions(interaction.user, send_messages=True, view_channel=True, attach_files=True, embed_links=True, read_message_history=True, use_slash_commands=True)

            embed = discord.Embed(title="<:profile:1101249417824186409>・Middleman Account Information", description=f"# **⁙ Username:** `{MMACC_USER}`\n**⁙ ID:** `{MMACC_ID}`\n**⁙ Profile Link:** [LINK](https://www.roblox.com/users/{MMACC_ID}/profile)", color=MAINCOLOR)
            vip_code = await getVipServerCode()
            embedaa1 = discord.Embed(title="<:rules:1101248874397581332>・Terms of Service", description="**By using our service, you agree to our ToS.**\n**Please read before continuing:**\n>>> <#1135522597468131414>\n<#1135516341319761960>", color=MAINCOLOR)
            embedaa = discord.Embed(title=f"<:link:1101251650674495539>・Adopt Me VIP Server", description=f"> **Link: https://www.roblox.com/games/920587237?privateServerLinkCode={vip_code} **", color=MAINCOLOR)
            embedaa.set_thumbnail(url="https://cdn.discordapp.com/attachments/816304640063963156/896318333639610419/imagen-hints-adopt-me-walkthrough-2019-0thumb.jpeg")
            embs = []
            embs.append(embedaa1)
            embs.append(embed)
            embs.append(embedaa)
            await interaction.channel.send(embeds=embs, view=TradeInfo())

            subrole = interaction.guild.get_role(SUBSCRIBER_ROLE)
            trader1 = interaction.guild.get_member(resSQL['trader_seller_id'])
            trader2 = interaction.guild.get_member(resSQL['trader_receiver_id'])
            tradersliste = [trader1, trader2]
            isSubto = False
            for tr in tradersliste:
              if subrole in tr.roles:
                isSubto = True
                break

            embades = []
            if isSubto == False:
              embad1 = discord.Embed(title="This Service is PAID", description="> Service Fee: `150 Robux b/t`", color=redcolor)
              embad1.set_footer(text="One of you has to pay the fee after your trade is completed.")
              embades.append(embad1)
              
            embad3 = discord.Embed(title="⚠ Security Reminder ⚠", description="> ・**Staff** & **Bots** __**will never**__ DM you about auto-tickets. If you get a DM claiming to be staff, it's probably a __**scammer!**__\n> Verify staff roles by typing: `<@paste_staff_id>`.\n\n> ・Watch out for in-game bot impersonators. Check usernames before giving your items.", color=0xffff00)
            embades.append(embad3)
            
            embad2 = discord.Embed(title="・ Step `1`", description=f"> # <@{resSQL['trader_seller_id']}> Join vip server -> Type `$send` in Roblox chat -> Give items to `{MMACC_USER}`", color=MAINCOLOR)
            embad2.set_footer(text="If you are experiencing issues, ping @Kookie")
                        
            embades.append(embad2)

            await interaction.channel.send(f"<@{resSQL['trader_seller_id']}>", embeds=embades)

            namelist = interaction.channel.name.split("-")
            namelist[0] = "auto"
            newname = "-".join(namelist)
            updateChannel(newname, interaction.channel.id)
            return

        json_data = {
            'usernames': [
                username,
            ],
            'excludeBannedUsers': True,
        }
        res = sessionCheck.post('https://users.roblox.com/v1/usernames/users', json=json_data)
        if len(res.json()['data']) == 0:
          closeCON(cur,con)
          try:
            await interaction.edit_original_response(embed=discord.Embed(description="<:redci:879849638855852112>  **The username was not found, please try again**  <:redci:879849638855852112>", color=redcolor))
            await interaction.message.edit(view=WriteUserView())
          except Exception:
            return
          return

        okeuser = res.json()['data'][0]['name']

        if interaction.user.id == resSQL['trader_receiver_id']:
          cur.execute(f"SELECT channel_id FROM channels WHERE (ticket_status='Open' OR ticket_status='Active' OR ticket_status='Pending') AND (seller_username='{okeuser}' OR receiver_username='{okeuser}')")
          resSQL2 = cur.fetchall()
          user_found = len(resSQL2) != 0
          if user_found == True:
            closeCON(cur,con)
            try:
              await interaction.edit_original_response(embed=discord.Embed(description="<:redci:879849638855852112>  **The username has already been used! Please use another username or close your other ticket.**  <:redci:879849638855852112>", color=redcolor))
              await interaction.message.edit(view=WriteUserView())
            except Exception:
              pass
            return

          cur.execute(f"UPDATE channels SET receiver_username='{okeuser}' WHERE channel_id='{interaction.channel.id}'")
        elif interaction.user.id == resSQL['trader_seller_id']:
          cur.execute(f"SELECT channel_id FROM channels WHERE (ticket_status='Open' OR ticket_status='Active' OR ticket_status='Pending') AND (seller_username='{okeuser}' OR receiver_username='{okeuser}')")
          resSQL2 = cur.fetchall()
          user_found = len(resSQL2) != 0
          if user_found == True:
            closeCON(cur,con)
            try:
              await interaction.edit_original_response(embed=discord.Embed(description="<:redci:879849638855852112>  **The username has already been used! Please use another username or close your other ticket.**  <:redci:879849638855852112>", color=redcolor))
              await interaction.message.edit(view=WriteUserView())
            except Exception:
              pass
            return

          cur.execute(f"UPDATE channels SET seller_username='{okeuser}' WHERE channel_id='{interaction.channel.id}'")
        cur.execute(f"UPDATE channels SET first_user_stated='Yes' WHERE channel_id='{interaction.channel.id}'")
        con.commit()
        closeCON(cur,con)

        await interaction.edit_original_response(embed=discord.Embed(title="<:succ:926608308033441792>  **Username Has Been Saved**  <:succ:926608308033441792>", color=MAINCOLOR))
        await interaction.message.edit(view=None)
        await interaction.channel.set_permissions(interaction.user, send_messages=True, view_channel=True, attach_files=True, embed_links=True, read_message_history=True, use_slash_commands=True)
        
        embed = discord.Embed(title="Who's your trader?", description=">>> Type either their Discord ID, full username, or mention.\n`(Note: do not include \"@\" if you are unable to ping your trader)`", color=MAINCOLOR)
        await interaction.channel.send(embed=embed)

class CancelTrade(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
  @discord.ui.button(row=0, label="Cancel Trade", style=discord.ButtonStyle.red, custom_id="canceltrade", disabled=False)
  async def button_callback1(self, button, interaction):
    
    con,cur = openCON()
    cur.execute(f"SELECT trade_confirmed FROM channels WHERE channel_id='{interaction.channel.id}'")
    resSQL = cur.fetchall()[0]
    closeCON(cur,con)
    if resSQL['trade_confirmed'] == "Yes":
      for child in self.children:
        child.disabled = True
      await interaction.message.edit(view=self)
      return
    
    embed1 = discord.Embed(title="Are you sure you want to cancel the trade?", description=">>> If you click \"Yes\", the channel will be locked and staff will be notified to review the ticket.\nIn the meantime, **DO NOT** ping or dm anyone! Doing so will get you __blacklisted__.\nAlso, you cannot revert this action after its done.", color=redcolor)
    try:
      await interaction.response.send_message(embed=embed1, view=CancelConfirmation(), ephemeral=True)
    except NotFound:
      return

class CancelConfirmation(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
    self.used = False
  @discord.ui.button(row=0, label="Yes", style=discord.ButtonStyle.red, custom_id="cancelyes", disabled=False)
  async def button_callback1(self, button, interaction):

    if self.used == True:
      return
    self.used = True

    ref_message = await interaction.channel.fetch_message(interaction.message.reference.message_id)
    await ref_message.edit(view=None)

    try:
      await interaction.response.defer()
    except NotFound:
      pass
    
    con,cur = openCON()
    cur.execute(f"SELECT user_id FROM added_users WHERE channel_id='{interaction.channel.id}'")
    added_users = cur.fetchall()
    closeCON(cur,con)
    for y in added_users:
      try:
        users = interaction.guild.get_member(y['user_id'])
        await interaction.channel.set_permissions(users, send_messages=False, view_channel=True, attach_files=True, embed_links=True, read_message_history=True, use_slash_commands=True)
      except Exception:
        pass
    embed = discord.Embed(title="The trade has been set on cancel.", description=f">>> Author: `{interaction.user.name}#{interaction.user.discriminator}` - [`{interaction.user.id}`]\nA staff member will review this soon.\n**Do not ping or dm** any staff member, doing so will get you __blacklisted__.", color=redcolor)
    await interaction.channel.send("<@358594990982561792>", embed=embed, view=OpenCancelTrade())

class OpenCancelTrade(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
  @discord.ui.button(row=0, label="Open Trade (Staff)", style=discord.ButtonStyle.blurple, custom_id="opencanceltrade", disabled=False)
  async def button_callback1(self, button, interaction):
    
    try:
      await interaction.response.defer()
    except NotFound:
      pass
    
    if interaction.user.id not in TicketAccess:
      return
    
    for child in self.children:
      child.disabled = True
    await interaction.message.edit(view=self)
    
    con,cur = openCON()
    cur.execute(f"SELECT user_id FROM added_users WHERE channel_id='{interaction.channel.id}'")
    added_users = cur.fetchall()
    closeCON(cur,con)
    mentions = ""
    for i in added_users:
      mentions += f"<@{i['user_id']}> "
    for y in added_users:
      try:
        users = interaction.guild.get_member(y['user_id'])
        await interaction.channel.set_permissions(users, send_messages=True, view_channel=True, attach_files=True, embed_links=True, read_message_history=True, use_slash_commands=True)
      except Exception:
        pass
    embed = discord.Embed(title="Opened Trade", color=SUCCCOLOR)
    await interaction.channel.send(mentions, embed=embed)

friendReq_oncooldown = []
friendReq_timestamps = {}

class TradeInfo(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
  @discord.ui.button(row=0, label="View Trade Information", style=discord.ButtonStyle.blurple, custom_id="tradeinformation", disabled=False)
  async def button_callback1(self, button, interaction):

    con,cur = openCON()
    cur.execute(f"SELECT * FROM channels WHERE channel_id='{interaction.channel.id}'")
    resSQL = cur.fetchall()[0]
    closeCON(cur,con)
    
    userType = ""
    desc = ""

    if interaction.user.id in TicketAccess:
      userType = "ADMIN"
      s_user = resSQL['seller_username']
      b_user = resSQL['receiver_username']
      ########
      disc_sID = resSQL['trader_seller_id']
      disc_bID = resSQL['trader_receiver_id']
      ########
      desc = f"**__Seller__**\n> Discord: <@{disc_sID}>\n> Roblox: `{s_user}`\n\n**__Buyer__**\n> Discord: <@{disc_bID}>\n> Roblox: `{b_user}`"
    elif interaction.user.id == resSQL['trader_seller_id']:
      userType = "SELLER"
      rbxuser = resSQL['seller_username']
      desc = f">>> You are the one who gives the items to the bot. (selling items)\nYour Roblox username is **`{rbxuser}`**"
    elif interaction.user.id == resSQL['trader_receiver_id']:
      userType = "BUYER"
      rbxuser = resSQL['receiver_username']
      desc = f">>> You are the one who is supposed to redeem the items later from the bot. (buying items)\nYour Roblox username is **`{rbxuser}`**"
    else:
      return await interaction.response.send_message("You can't use this!", ephemeral=True)
    
    embed = discord.Embed(title=f"You are the **{userType}**", description=desc, color=redcolor)
    await interaction.response.send_message(embed=embed, ephemeral=True)

  @discord.ui.button(row=0, label="View Commands", style=discord.ButtonStyle.blurple, custom_id="viewbotcommands", disabled=False)
  async def button_callback4(self, button, interaction):
    embed1 = discord.Embed(title="> __COMMANDS__", description="・**$inventory** / **$inv**\n*╰-> Sends the current inventory of the bot.*\n\n・**$tradehistory** / **$th**\n*╰-> Sends the bot's in-game trade history.*\n\n・**$am**\n*╰-> Sends the adopt me vip server link.*\n\n・**$setuser**\n*╰-> Changes your Roblox username in the ticket.*\n\n・**$close**\n*╰-> Closes your ticket.*\nㅤ", color=MAINCOLOR)
    embed1.add_field(name="> __Seller's Commands__", value="・**$send**\n*╰-> Bot sends you a trade, to give it the items.*\n・**$confirm**\n*╰-> Gives your buyer permission to withdraw their items.*", inline=True)
    embed1.add_field(name="> __Buyer's Commands__", value="・**$redeem**\n*╰-> Bot sends you a trade, to redeem your items.*", inline=True)
    try:
      await interaction.response.send_message(embed=embed1, ephemeral=True)
    except NotFound:
      return

  @discord.ui.button(row=1, label="Send Friend Request", style=discord.ButtonStyle.green, custom_id="sendfriendreq", disabled=False)
  async def button_callback2(self, button, interaction):
    global friendReq_oncooldown

    if interaction.user.id in friendReq_oncooldown:
      first_ts = friendReq_timestamps[f"{interaction.user.id}"]
      second_ts = int(time.time())
      return await interaction.response.send_message(f"You are on cooldown, try again after `{20-(second_ts-first_ts)}` seconds.", ephemeral=True)

    friendReq_oncooldown.append(interaction.user.id)
    friendReq_timestamps[f"{interaction.user.id}"] = int(time.time())

    con,cur = openCON()
    cur.execute(f"SELECT * FROM channels WHERE channel_id='{interaction.channel.id}'")
    resSQL = cur.fetchall()[0]
    seller_username = resSQL['seller_username']
    receiver_username = resSQL['receiver_username']
    trader_seller_id = resSQL['trader_seller_id']
    trader_receiver_id = resSQL['trader_receiver_id']
    closeCON(cur,con)

    if interaction.user.id == trader_seller_id:
      username = seller_username
    elif interaction.user.id == trader_receiver_id:
      username = receiver_username
    else:
      await interaction.response.send_message("You can't use this!", ephemeral=True)
      await asyncio.sleep(20)
      friendReq_oncooldown.remove(interaction.user.id)
      del friendReq_timestamps[f"{interaction.user.id}"]
      return
    
    await interaction.response.send_message("Sending...", ephemeral=True)

    friend_req = rbx_send_request(username)
    if friend_req == "Successful":
      await interaction.edit_original_response(content=f"✅ **Friend Request Sent** ✅\n> **Accept the friend request from `AutoMMvip`**.")
    else:
      await interaction.edit_original_response(content=f"❌ {friend_req} ❌")

    await asyncio.sleep(20)
    friendReq_oncooldown.remove(interaction.user.id)
    del friendReq_timestamps[f"{interaction.user.id}"]

  @discord.ui.button(row=1, label="I Can't Join The VIP?", style=discord.ButtonStyle.red, custom_id="cantjointhevip", disabled=False)
  async def button_callback3(self, button, interaction):
    embed = discord.Embed(color=MAINCOLOR)
    embed.add_field(name="・**Error: \"You do not have permission to join this game. (Error Code: 524)\"**", value="> Go to your `Roblox Settings` -> `Privacy` -> Set \"`Who can make me a member of their private server?`\" to \"`Everyone`\".", inline=False)
    embed.add_field(name="・**Error: \"This VIP Server link is no longer valid.\"**", value="> Type the command $am to get the new link. VIP links are regenerated regularly.", inline=False)
    embed.add_field(name="・**\"I can't join because I'm on mobile.\"**", value="> You can join on mobile by logging in your browser and pressing the link.", inline=False)
    try:
      await interaction.response.send_message(embed=embed, ephemeral=True)
    except NotFound:
      return

class TradesAmount(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
  @discord.ui.button(row=0, label="One Trade (max. 18 items)", style=discord.ButtonStyle.blurple, custom_id="onetrade", disabled=False)
  async def button_callback1(self, button, interaction):
    
    msgs = await interaction.channel.history(limit=None, oldest_first=True).flatten()
    user = msgs[0].mentions[0]

    if interaction.user.id != user.id:
      await interaction.response.defer()
      return

    for child in self.children:
      child.disabled = True
    await interaction.message.edit(view=self)

    try:
      await interaction.response.defer()
    except NotFound:
      pass

    con,cur = openCON()
    cur.execute(f"SELECT * FROM channels WHERE channel_id='{interaction.channel.id}'")
    resSQL = cur.fetchall()[0]
    cur.execute(f"UPDATE channels SET selected_trades_num='1' WHERE channel_id='{interaction.channel.id}'")
    con.commit()
    closeCON(cur,con)

    if resSQL['owner_trader_type'] == "seller":
      mesag = "> Input the username that you are going to give the items from."
    elif resSQL['owner_trader_type'] == "buyer":
      mesag = "> Input the username that you want to redeem the items on."

    embed = discord.Embed(title="<:profile:1101249417824186409>・Your Roblox username?", description=mesag, color=MAINCOLOR)
    await interaction.channel.send(interaction.user.mention, embed=embed, view=WriteUserView())
  
    editedembed = interaction.message.embeds[0]
    editedembed.set_footer(text="Selected: 1")
    await interaction.message.edit(embed=editedembed)

  @discord.ui.button(row=0, label="Two Trades (max. 36 items)", style=discord.ButtonStyle.blurple, custom_id="twotrade", disabled=False)
  async def button_callback2(self, button, interaction):
    
    msgs = await interaction.channel.history(limit=None, oldest_first=True).flatten()
    user = msgs[0].mentions[0]

    if interaction.user.id != user.id:
      await interaction.response.defer()
      return

    for child in self.children:
      child.disabled = True
    await interaction.message.edit(view=self)

    try:
      await interaction.response.defer()
    except NotFound:
      pass

    con,cur = openCON()
    cur.execute(f"SELECT * FROM channels WHERE channel_id='{interaction.channel.id}'")
    resSQL = cur.fetchall()[0]
    cur.execute(f"UPDATE channels SET selected_trades_num='2', trade_id='[\"No\", \"No\"]', redeem_trade_id='[\"No\", \"No\"]' WHERE channel_id='{interaction.channel.id}'")
    con.commit()
    closeCON(cur,con)

    if resSQL['owner_trader_type'] == "seller":
      mesag = "> Input the username that you are going to give the items from."
    elif resSQL['owner_trader_type'] == "buyer":
      mesag = "> Input the username that you want to redeem the items on."

    embed = discord.Embed(title="<:profile:1101249417824186409>・Your Roblox username?", description=mesag, color=MAINCOLOR)
    await interaction.channel.send(interaction.user.mention, embed=embed, view=WriteUserView())
  
    editedembed = interaction.message.embeds[0]
    editedembed.set_footer(text="Selected: 2")
    await interaction.message.edit(embed=editedembed)

  @discord.ui.button(row=1, label="Three Trades (max. 54 items)", style=discord.ButtonStyle.blurple, custom_id="threetrade", disabled=False)
  async def button_callback3(self, button, interaction):
    
    msgs = await interaction.channel.history(limit=None, oldest_first=True).flatten()
    user = msgs[0].mentions[0]

    if interaction.user.id != user.id:
      await interaction.response.defer()
      return

    for child in self.children:
      child.disabled = True
    await interaction.message.edit(view=self)

    try:
      await interaction.response.defer()
    except NotFound:
      pass

    con,cur = openCON()
    cur.execute(f"SELECT * FROM channels WHERE channel_id='{interaction.channel.id}'")
    resSQL = cur.fetchall()[0]
    cur.execute(f"UPDATE channels SET selected_trades_num='3', trade_id='[\"No\", \"No\", \"No\"]', redeem_trade_id='[\"No\", \"No\", \"No\"]' WHERE channel_id='{interaction.channel.id}'")
    con.commit()
    closeCON(cur,con)

    if resSQL['owner_trader_type'] == "seller":
      mesag = "> Input the username that you are going to give the items from."
    elif resSQL['owner_trader_type'] == "buyer":
      mesag = "> Input the username that you want to redeem the items on."

    embed = discord.Embed(title="<:profile:1101249417824186409>・Your Roblox username?", description=mesag, color=MAINCOLOR)
    await interaction.channel.send(interaction.user.mention, embed=embed, view=WriteUserView())
  
    editedembed = interaction.message.embeds[0]
    editedembed.set_footer(text="Selected: 3")
    await interaction.message.edit(embed=editedembed)

  @discord.ui.button(row=1, label="Four Trades (max. 72 items)", style=discord.ButtonStyle.blurple, custom_id="fourtrade", disabled=False)
  async def button_callback4(self, button, interaction):
    
    msgs = await interaction.channel.history(limit=None, oldest_first=True).flatten()
    user = msgs[0].mentions[0]

    if interaction.user.id != user.id:
      await interaction.response.defer()
      return

    for child in self.children:
      child.disabled = True
    await interaction.message.edit(view=self)

    try:
      await interaction.response.defer()
    except NotFound:
      pass

    con,cur = openCON()
    cur.execute(f"SELECT * FROM channels WHERE channel_id='{interaction.channel.id}'")
    resSQL = cur.fetchall()[0]
    cur.execute(f"UPDATE channels SET selected_trades_num='4', trade_id='[\"No\", \"No\", \"No\", \"No\"]', redeem_trade_id='[\"No\", \"No\", \"No\", \"No\"]' WHERE channel_id='{interaction.channel.id}'")
    con.commit()
    closeCON(cur,con)

    if resSQL['owner_trader_type'] == "seller":
      mesag = "> Input the username that you are going to give the items from."
    elif resSQL['owner_trader_type'] == "buyer":
      mesag = "> Input the username that you want to redeem the items on."

    embed = discord.Embed(title="<:profile:1101249417824186409>・Your Roblox username?", description=mesag, color=MAINCOLOR)
    await interaction.channel.send(interaction.user.mention, embed=embed, view=WriteUserView())
  
    editedembed = interaction.message.embeds[0]
    editedembed.set_footer(text="Selected: 4")
    await interaction.message.edit(embed=editedembed)

  @discord.ui.button(row=2, label="Five Trades (max. 90 items)", style=discord.ButtonStyle.blurple, custom_id="fivetrade", disabled=False)
  async def button_callback5(self, button, interaction):
    
    msgs = await interaction.channel.history(limit=None, oldest_first=True).flatten()
    user = msgs[0].mentions[0]

    if interaction.user.id != user.id:
      await interaction.response.defer()
      return

    for child in self.children:
      child.disabled = True
    await interaction.message.edit(view=self)

    try:
      await interaction.response.defer()
    except NotFound:
      pass

    con,cur = openCON()
    cur.execute(f"SELECT * FROM channels WHERE channel_id='{interaction.channel.id}'")
    resSQL = cur.fetchall()[0]
    cur.execute(f"UPDATE channels SET selected_trades_num='5', trade_id='[\"No\", \"No\", \"No\", \"No\", \"No\"]', redeem_trade_id='[\"No\", \"No\", \"No\", \"No\", \"No\"]' WHERE channel_id='{interaction.channel.id}'")
    con.commit()
    closeCON(cur,con)

    if resSQL['owner_trader_type'] == "seller":
      mesag = "> Input the username that you are going to give the items from."
    elif resSQL['owner_trader_type'] == "buyer":
      mesag = "> Input the username that you want to redeem the items on."

    embed = discord.Embed(title="<:profile:1101249417824186409>・Your Roblox username?", description=mesag, color=MAINCOLOR)
    await interaction.channel.send(interaction.user.mention, embed=embed, view=WriteUserView())
  
    editedembed = interaction.message.embeds[0]
    editedembed.set_footer(text="Selected: 5")
    await interaction.message.edit(embed=editedembed)


class SellerOrBuyer(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
  @discord.ui.button(row=0, label="Seller", style=discord.ButtonStyle.blurple, custom_id="imseller", disabled=False)
  async def button_callback1(self, button, interaction):
    
    msgs = await interaction.channel.history(limit=None, oldest_first=True).flatten()
    user = msgs[0].mentions[0]

    if interaction.user.id != user.id:
      await interaction.response.defer()
      return

    for child in self.children:
      child.disabled = True
    await interaction.message.edit(view=self)

    try:
      await interaction.response.defer()
    except NotFound:
      pass
    
    con,cur = openCON()
    cur.execute(f"UPDATE channels SET trader_seller_id='{interaction.user.id}', owner_trader_type='seller' WHERE channel_id='{interaction.channel.id}'")
    con.commit()
    closeCON(cur,con)

    embed = discord.Embed(title="🔢・Number of trades", description="> Select the __**number**__ of trades you will do with the Adopt Me bot.", color=MAINCOLOR)
    await interaction.channel.send(embed=embed, view=TradesAmount())

    editedembed = interaction.message.embeds[0]
    editedembed.set_footer(text="Selected: Seller")
    await interaction.message.edit(embed=editedembed)

  @discord.ui.button(row=0, label="Buyer", style=discord.ButtonStyle.blurple, custom_id="imbuyer", disabled=False)
  async def button_callback2(self, button, interaction):
    msgs = await interaction.channel.history(limit=None, oldest_first=True).flatten()
    user = msgs[0].mentions[0]

    if interaction.user.id != user.id:
      await interaction.response.defer()
      return

    for child in self.children:
      child.disabled = True
    await interaction.message.edit(view=self)

    try:
      await interaction.response.defer()
    except NotFound:
      pass

    con,cur = openCON()
    cur.execute(f"UPDATE channels SET trader_receiver_id='{interaction.user.id}', owner_trader_type='buyer' WHERE channel_id='{interaction.channel.id}'")
    con.commit()
    closeCON(cur,con)

    embed = discord.Embed(title="Number of trades", description="> Select __**number**__ of trades with the Adopt Me bot?", color=MAINCOLOR)
    await interaction.channel.send(embed=embed, view=TradesAmount())

    editedembed = interaction.message.embeds[0]
    editedembed.set_footer(text="Selected: Buyer")
    await interaction.message.edit(embed=editedembed)


@bot.command()
async def amp(ctx):
  if ctx.author.id in TicketAccess:
    embed = discord.Embed(title="> <:ShadowDragon:1135522019635634237>・__Automated Adopt Me Middleman__・<:ShadowDragon:1135522019635634237>", color=MAINCOLOR)
    embed.add_field(name="・Service Fee", value="> ・__**One-time-usage**__  *(for one trade)* --> **`150`** <:Robux:914568435583836171> *(Robux)*\n> *Note: The fee is paid __after__ the trade is completed.*\n> ㅤㅤㅤor\n> ・__**Monthly subscription**__ --> **`$5`** <:BTC:1068572950275571763>/<:LTC:992768413279735888>/<:ETH:992768323429355540>", inline=False)
    embed.add_field(name="・Bot Info", value="> ・The bot can hold up to `90` items per ticket.\n> ・<#1135522597468131414> apply here.\n> ・Although, we have never faced an issue with account termination, if the bot gets termed mid-trade, then we are not responsible for any refunds.", inline=False)
    embed.set_footer(text='For more information, click the "FAQ" under this message.')
    embed.set_image(url="https://cdn.discordapp.com/attachments/707169952154779688/1081240963613208746/amj.jpg")
    await ctx.send(embed=embed)
    await ctx.send(view=AMP_Tickets())


@bot.event
async def on_guild_channel_delete(channel):
  if channel.guild.id == GUILD_ID:
    try:
      if (channel.category.id == AUTOAMP_CATEGORY_ID) or (channel.category.id == CLOSED_CATEGORY_ID) or (channel.category.id == MMPASS_CATEGORY_ID):
        con,cur = openCON()
        cur.execute(f"DELETE FROM channels WHERE channel_id='{channel.id}'")
        cur.execute(f"DELETE FROM added_users WHERE channel_id='{channel.id}'")
        con.commit()
        closeCON(cur,con)
    except AttributeError:
      pass


messages_oncooldown = []

def putOnCD(userID1):
  messages_oncooldown.append(userID1)
  time.sleep(10)
  messages_oncooldown.remove(userID1)

@bot.event
async def on_message(message):
  if type(message.channel) == discord.TextChannel:
    await bot.process_commands(message)

    if message.author.bot:
      return
    
    try:
      channelcheck = message.channel.category.id
    except AttributeError:
      return

    category_id = AUTOAMP_CATEGORY_ID
    if (message.channel.category.id) == category_id:
      if message.channel.name.split("-")[0] == "pending":
        con,cur = openCON()
        cur.execute(f"SELECT * FROM channels WHERE channel_id='{message.channel.id}'")
        try:
          resSQL = cur.fetchall()[0]
        except Exception:
          return
        
        SellerAndRecIds = [resSQL['trader_seller_id'], resSQL['trader_receiver_id']]

        if message.author.id not in SellerAndRecIds:
          closeCON(cur,con)
          return

        if (resSQL['trade_stated'] == "No") and (resSQL['selected_trades_num'] != 0):          
          if (resSQL['first_user_stated'] == "Yes"):
            if (resSQL['trader_added'] == "No"):
              blrole = message.guild.get_role(BLACKLIST_ROLE_ID)
              try:
                if message.mentions:
                  user = message.mentions[0]
                elif message.content.isdigit():
                  getuser = message.content
                  user = message.guild.get_member(int(getuser))
                else:
                  content = message.content
                  user = discord.utils.get(message.guild.members, name=content)

                try:
                  if user.id == message.author.id:
                    closeCON(cur,con)
                    return await message.reply(embed=discord.Embed(description="<a:oklol:858377249949220904>  **You can't add yourself**  <a:oklol:858377249949220904>", color=grey))
                except Exception:
                  pass
                
                if user.bot:
                  closeCON(cur,con)
                  return await message.reply(embed=discord.Embed(description="<a:oklol:858377249949220904>  **You can't add a bot**  <a:oklol:858377249949220904>", color=grey))
                
                if blrole in user.roles:
                  closeCON(cur,con)
                  return await message.reply(embed=discord.Embed(description=f"<:redci:879849638855852112>  **{user.mention} is blacklisted from using this mm service**  <:redci:879849638855852112>", color=redcolor))
                
                verified = message.guild.get_role(1116136541656465462)
                if verified not in user.roles:
                  closeCON(cur,con)
                  return await message.reply(embed=discord.Embed(description=f"<:redci:879849638855852112>  **Your trader is not verified!**  <:redci:879849638855852112>", color=redcolor))
                  
                await message.channel.set_permissions(user, send_messages=False, view_channel=True, attach_files=True, embed_links=True, read_message_history=True, use_slash_commands=True)
                await message.reply(embed=discord.Embed(description=f'***{user.mention} was added to the ticket {message.channel.mention}***', color=SUCCCOLOR))
              
                if resSQL['owner_trader_type'] == "seller":
                  cur.execute(f"UPDATE channels SET trader_receiver_id='{user.id}' WHERE channel_id='{message.channel.id}'")
                  mesag = "> Input the username that you want to redeem the items on."
                elif resSQL['owner_trader_type'] == "buyer":
                  cur.execute(f"UPDATE channels SET trader_seller_id='{user.id}' WHERE channel_id='{message.channel.id}'")
                  mesag = "> Input the username that you are going to give the items from."

                cur.execute(f"UPDATE channels SET trader_added='Yes' WHERE channel_id='{message.channel.id}'")
                cur.execute(f"INSERT INTO added_users (user_id, channel_id) VALUES ({user.id}, {message.channel.id})")
                con.commit()
                closeCON(cur,con)

                embed = discord.Embed(title="<:profile:1101249417824186409>・Your Roblox username?", description=mesag, color=MAINCOLOR)
                await message.channel.send(user.mention, embed=embed, view=WriteUserView())

                ticketlogs = bot.get_channel(AUTOAMP_LOGS_ID)
                logembed = discord.Embed(description=f"Author: **{message.author.name}#{message.author.discriminator}** | ID: {message.author.id}\nTicket: **{message.channel.name}** | ID: {message.channel.id}\nAction: **Added {user.name}#{user.discriminator} | ID: {user.id}**", color=0x66BB6A)
                logembed.set_author(name=f"{message.author.name}#{message.author.discriminator}", icon_url=f"{message.author.display_avatar.url}")
                await ticketlogs.send(embed=logembed)

                return
              except ValueError:
                await message.reply(embed=discord.Embed(description="***User wasn't found, double check the username/ID and make sure the user is in this server!***", color=0xed4245))
              except AttributeError:
                await message.reply(embed=discord.Embed(description="***User wasn't found, double check the username/ID and make sure the user is in this server!***", color=0xed4245))


async def getInventory():
  dbchannel = bot.get_channel(1002208502921580596)
  logsdata_msg = await dbchannel.fetch_message(1002209142456451123)
  file = logsdata_msg.attachments[0]
  cont = await file.read()
  data = ast.literal_eval(cont.decode('utf-8'))
  try:
    data['FinishedPetsList'] = sorted(data['FinishedPetsList'].replace("-#####-", "\n").split("\n"))
    data['FinishedPetwearList'] = sorted(data['FinishedPetwearList'].replace("-#####-", "\n").split("\n"))
    data['FinishedStrollersList'] = sorted(data['FinishedStrollersList'].replace("-#####-", "\n").split("\n"))
    data['FinishedVehiclesList'] = sorted(data['FinishedVehiclesList'].replace("-#####-", "\n").split("\n"))
    data['FinishedFoodList'] = sorted(data['FinishedFoodList'].replace("-#####-", "\n").split("\n"))
    data['FinishedToysList'] = sorted(data['FinishedToysList'].replace("-#####-", "\n").split("\n"))
    data['FinishedGiftsList'] = sorted(data['FinishedGiftsList'].replace("-#####-", "\n").split("\n"))
  except Exception:
    pass
  return data

@bot.command(aliases=['inv'])
@commands.cooldown(1, 15, commands.BucketType.channel)
async def inventory(ctx):
  if (ctx.message.channel.category.id == AUTOAMP_CATEGORY_ID):
    data = await getInventory()
    await ctx.reply(embed=discord.Embed(description="**Use the select menu in order to display certain information in the inventory**", color=MAINCOLOR), view=Inventory(invdata=data))

#@bot.command()
#@commands.cooldown(1, 15, commands.BucketType.user)
#async def passes(ctx):
#  pass_count = 0
#  passesList = await readPasses()
#  for passi in passesList:
#    if passi['userID'] == ctx.author.id:
#      pass_count = passi['passes']
#      break
#  embed = discord.Embed(title=f"You have `{pass_count}` mm-passes.", color=MAINCOLOR)
#  await ctx.reply(embed=embed)

@bot.command()
async def addsub(ctx, user:discord.Member=None):
  if ctx.author.id not in TicketAccess:
    return
  if user == None:
    return await ctx.reply("User missing!")
  
  con,cur = openCON()
  cur.execute(f"SELECT * FROM sub_tickets WHERE (owner_id='{user.id}')")
  resSQL2 = cur.fetchall()
  found_user = len(resSQL2) != 0

  if found_user == True:
    closeCON(cur,con)
    return await ctx.reply("User is already a subscriber!")
  
  boughtAt_ts = datetime.now()
  endsAt_ts = boughtAt_ts+timedelta(days=30)

  boughtAt_ts = int(boughtAt_ts.timestamp())
  endsAt_ts = int(endsAt_ts.timestamp())
  
  cur.execute(f"INSERT INTO sub_tickets (owner_id, serial, bought_at, ends_at, extended) VALUES ('{user.id}', 'GIVEN', '{boughtAt_ts}','{endsAt_ts}', '0')")
  con.commit()
  closeCON(cur,con)

  subrole = ctx.guild.get_role(SUBSCRIBER_ROLE)
  await user.add_roles(subrole)
  await ctx.reply(f"✅ {user.mention} is now a subscriber!")


@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def sub(ctx, argUser:discord.User=None):    
  if argUser == None:
    checkThisUser = ctx.author.id
    argUser = ctx.author
  else:
    checkThisUser = argUser.id

  foundUser = False
  con,cur = openCON()
  cur.execute(f"SELECT * FROM sub_tickets WHERE (owner_id='{checkThisUser}') AND (status='Active')")
  resSQL2 = cur.fetchall()
  closeCON(cur,con)
  foundUser = len(resSQL2) != 0
    
  if foundUser == False:
    if checkThisUser == ctx.author.id:
      return await ctx.reply("You do not have a subscription.")
    else:
      return await ctx.reply("The user does not have a subscription.")

  resSQL2 = resSQL2[0]
  extended_ts = 0
  extended = False
  if resSQL2['extended'] != 0:
    extended = True
    extended_ts = resSQL2['extended']
  bought_ts = resSQL2['bought_at']
  end_ts = resSQL2['ends_at']

  if extended == True:
    daysAdded = round(extended_ts/86400, 2)
    new_end = end_ts+extended_ts
    purchMsg = f">>> <t:{bought_ts}:f>"
    expMsg = f">>> <t:{end_ts}:f> (`+{daysAdded} Days`)\n**Actual Date:** <t:{new_end}:f>\n**Ends in:** <t:{new_end}:R>"
  else:
    purchMsg = f">>> <t:{bought_ts}:f>"
    expMsg = f">>> <t:{end_ts}:f>\n**Ends in:** <t:{end_ts}:R>"

  embed = discord.Embed(title="Subscription Info", color=MAINCOLOR)
  embed.add_field(name="Purchased Date", value=purchMsg, inline=False)
  embed.add_field(name="Expiration Date", value=expMsg, inline=False)
  embed.set_footer(text=f"{argUser.name}'s Subscription")
  await ctx.reply(embed=embed)

@bot.command()
async def extendsub(ctx, user:discord.User=None, duration=None):
  if ctx.author.id not in TicketAccess:
    return
  if user == None:
    return await ctx.reply("User missing!")
  if duration == None:
    return await ctx.reply("Duration missing!")
  
  foundUser = False
  subsList = await readSubs()
  userTable = None
  index = 0
  for subi in subsList:
    if subi['userID'] == user.id:
      foundUser = True
      userTable = subi
      break
    index = index+1
  if foundUser == False:
    return await ctx.reply("User is not a subscriber!")
  
  time_convert = {"s":1, "m":60, "h":3600,"d":86400}
  timetoAdd = int(duration[:-1]) * time_convert[duration[-1]]
  userTable['extended'] = userTable['extended']+timetoAdd
  editSubs(subsList)
  await ctx.reply(f"✅ {user.mention}'s subscription has been extended by `{duration[:-1]}{duration[-1]}+`")

async def getTradeHistory(isAdmin=None):
  dbchannel = bot.get_channel(1002208531434450974)
  logsdata_msg = await dbchannel.fetch_message(1002209717923369030)
  file = logsdata_msg.attachments[0]
  cont = await file.read()
  data = ast.literal_eval(cont.decode('utf-8'))
  lastFetched = f"<t:{int(logsdata_msg.edited_at.timestamp())}:R>"
  embedss = []
  if isAdmin != None:
    for i in data:
      embaLis = []
      tradeID = i['tradeID']
      timestamp = i['timestamp']
      senderName = i['senderName']
      senderID = i['senderID']
      recName = i['recName']
      recID = i['recID']
      senderItems = i['FinishedSenderList'].replace("-#####-", "\n")
      recItems = i['FinishedRecList'].replace("-#####-", "\n")
      embed = discord.Embed(title="Adopt Me Trade History", description=f"__**General Info**__\nTrade between **[`{senderName}`](https://www.roblox.com/users/{senderID})** and **[`{recName}`](https://www.roblox.com/users/{recID})**.\nDate: <t:{timestamp}:F> | <t:{timestamp}:R>\nLast Fetched: {lastFetched}\nTrade ID: `[{tradeID}]`", color=MAINCOLOR)
      embed2 = discord.Embed(title=f"First Trader | `{senderName}` - ID: [`{senderID}`]", description=f">>> **__Offer__**\n{senderItems}", color=MAINCOLOR)
      embed3 = discord.Embed(title=f"Second Trader | `{recName}` - ID: [`{recID}`]", description=f">>> **__Offer__**\n{recItems}", color=MAINCOLOR)
      embaLis.append(embed); embaLis.append(embed2); embaLis.append(embed3)
      embedss.append(embaLis)
  else:
    for i in data:
      embaLis = []
      tradeID = i['tradeID']
      timestamp = i['timestamp']
      senderName = i['senderName']
      senderID = i['senderID']
      recName = i['recName']
      recID = i['recID']
      senderItems = i['FinishedSenderList'].replace("-#####-", "\n")
      recItems = i['FinishedRecList'].replace("-#####-", "\n")
      embed = discord.Embed(title="Adopt Me Trade History", description=f"Date: <t:{timestamp}:F> | <t:{timestamp}:R>\nLast Fetched: {lastFetched}", color=MAINCOLOR)      
      embed2 = discord.Embed(title=f"First Trader | `{senderName}` - ID: [`{senderID}`]", description=f">>> **__Offer__**\n{senderItems}", color=MAINCOLOR)
      embed3 = discord.Embed(title=f"Second Trader | `\"Hidden\"`", description=f">>> **__Offer__**\n{recItems}", color=MAINCOLOR)
      embaLis.append(embed); embaLis.append(embed2); embaLis.append(embed3)
      embedss.append(embaLis)
  return embedss

def chunk(it, size):
  it = iter(it)
  return iter(lambda: tuple(islice(it, size)), ())

@bot.command(aliases=['th'])
@commands.cooldown(1, 15, commands.BucketType.channel)
async def tradehistory(ctx):
  #staffrole = ctx.guild.get_role(STAFF_ROLE_ID)
  if (ctx.message.channel.category.id == AUTOAMP_CATEGORY_ID):
    #loop = bot.loop
    #embedss = await loop.run_in_executor(None, getTradeHistory)
    if ctx.author.id in TicketAccess:
      embedss = await getTradeHistory(isAdmin="Yes")
    else:
      embedss = await getTradeHistory()

    paginator = pages.Paginator(pages=embedss, show_disabled=True, show_indicator=True, timeout=None)
    paginator.add_button(pages.PaginatorButton("next", style=discord.ButtonStyle.green))
    paginator.add_button(pages.PaginatorButton("prev", style=discord.ButtonStyle.green))
    paginator.add_button(pages.PaginatorButton("first", style=discord.ButtonStyle.blurple))
    paginator.add_button(pages.PaginatorButton("last", style=discord.ButtonStyle.blurple))

    if ctx.author.id in TicketAccess:
      dmchannel = await ctx.author.create_dm()
      await paginator.send(ctx, target=dmchannel)
      await ctx.reply("The trade history has been sent your dms.")
    else:
      await paginator.send(ctx, reference=ctx.message)


class Inventory(discord.ui.View):
  def __init__(self, invdata):
    super().__init__(timeout=None)
    self.data = invdata
  @discord.ui.select(placeholder='Select a Category to Display',
                     min_values=1,
                     max_values=1,
                     custom_id="inventorylist",
                     options=[
                      discord.SelectOption(label='Pets'),
                      discord.SelectOption(label='Pet Accessories'),
                      discord.SelectOption(label='Strollers'),
                      discord.SelectOption(label='Food'),
                      discord.SelectOption(label='Vehicles'),
                      discord.SelectOption(label='Toys'),
                      discord.SelectOption(label='Gifts')
                      ])
  
  async def select_callback(self, select, interaction):

    await interaction.response.send_message(content=f"**Fetching..**", ephemeral=True)

    data = self.data

    if select.values[0] == "Pets":

      if len(data['FinishedPetsList']) == 1:
        return await interaction.edit_original_response(content="**This category is empty!**")
      
      if len(data['FinishedPetsList']) > 30:
        newlist = chunk(data['FinishedPetsList'], 30)
        embedslist = []
        for items in newlist:
          merge = ""
          for items2 in items:
            if len(items2) != 0:
              merge += f"{items2}\n"
          embed = discord.Embed(title="Inventory | Pets", description=f"__**Pets List**__\n>>> {merge}")
          embedslist.append(embed)
        await interaction.edit_original_response(content=None, embeds=embedslist)
      else:
        newlist = data['FinishedPetsList']
        merge = ""
        for items in newlist:
          if len(items) != 0:
            merge += f"{items}\n"
        embed = discord.Embed(title="Inventory | Pets", description=f"__**Pets List**__\n>>> {merge}")
        await interaction.edit_original_response(content=None, embed=embed)

    elif select.values[0] == "Pet Accessories":
          
      if len(data['FinishedPetwearList']) == 1:
        return await interaction.edit_original_response(content="**This category is empty!**")

      if len(data['FinishedPetwearList']) > 30:
        newlist = chunk(data['FinishedPetwearList'], 30)
        embedslist = []
        for items in newlist:
          merge = ""
          for items2 in items:
            if len(items2) != 0:
              merge += f"{items2}\n"
          embed = discord.Embed(title="Inventory | Pet Accessories", description=f"__**Pet Accessories List**__\n>>> {merge}")
          embedslist.append(embed)
        await interaction.edit_original_response(content=None, embeds=embedslist)
      else:
        newlist = data['FinishedPetwearList']
        merge = ""
        for items in newlist:
          if len(items) != 0:
            merge += f"{items}\n"
        embed = discord.Embed(title="Inventory | Pet Accessories", description=f"__**Pet Accessories List**__\n>>> {merge}")
        await interaction.edit_original_response(content=None, embed=embed)

    elif select.values[0] == "Strollers":
      
      if len(data['FinishedStrollersList']) == 1:
        return await interaction.edit_original_response(content="**This category is empty!**")

      if len(data['FinishedStrollersList']) > 30:
        newlist = chunk(data['FinishedStrollersList'], 30)
        embedslist = []
        for items in newlist:
          merge = ""
          for items2 in items:
            if len(items2) != 0:
              merge += f"{items2}\n"
          embed = discord.Embed(title="Inventory | Strollers", description=f"__**Strollers List**__\n>>> {merge}")
          embedslist.append(embed)
        await interaction.edit_original_response(content=None, embeds=embedslist)
      else:
        newlist = data['FinishedStrollersList']
        merge = ""
        for items in newlist:
          if len(items) != 0:
            merge += f"{items}\n"
        embed = discord.Embed(title="Inventory | Strollers", description=f"__**Strollers List**__\n>>> {merge}")
        await interaction.edit_original_response(content=None, embed=embed)

    elif select.values[0] == "Food":
      
      if len(data['FinishedFoodList']) == 1:
        return await interaction.edit_original_response(content="**This category is empty!**")

      if len(data['FinishedFoodList']) > 30:
        newlist = chunk(data['FinishedFoodList'], 30)
        embedslist = []
        for items in newlist:
          merge = ""
          for items2 in items:
            if len(items2) != 0:
              merge += f"{items2}\n"
          embed = discord.Embed(title="Inventory | Food", description=f"__**Food List**__\n>>> {merge}")
          embedslist.append(embed)
        await interaction.edit_original_response(content=None, embeds=embedslist)
      else:
        newlist = data['FinishedFoodList']
        merge = ""
        for items in newlist:
          if len(items) != 0:
            merge += f"{items}\n"
        embed = discord.Embed(title="Inventory | Food", description=f"__**Food List**__\n>>> {merge}")
        await interaction.edit_original_response(content=None, embed=embed)

    elif select.values[0] == "Vehicles":
      
      if len(data['FinishedVehiclesList']) == 1:
        return await interaction.edit_original_response(content="**This category is empty!**")

      if len(data['FinishedVehiclesList']) > 30:
        newlist = chunk(data['FinishedVehiclesList'], 30)
        embedslist = []
        for items in newlist:
          merge = ""
          for items2 in items:
            if len(items2) != 0:
              merge += f"{items2}\n"
          embed = discord.Embed(title="Inventory | Vehicles", description=f"__**Vehicles List**__\n>>> {merge}")
          embedslist.append(embed)
        await interaction.edit_original_response(content=None, embeds=embedslist)
      else:
        newlist = data['FinishedVehiclesList']
        merge = ""
        for items in newlist:
          if len(items) != 0:
            merge += f"{items}\n"
        embed = discord.Embed(title="Inventory | Vehicles", description=f"__**Vehicles List**__\n>>> {merge}")
        await interaction.edit_original_response(content=None, embed=embed)

    elif select.values[0] == "Toys":
      
      if len(data['FinishedToysList']) == 1:
        return await interaction.edit_original_response(content="**This category is empty!**")

      if len(data['FinishedToysList']) > 30:
        newlist = chunk(data['FinishedToysList'], 30)
        embedslist = []
        for items in newlist:
          merge = ""
          for items2 in items:
            if len(items2) != 0:
              merge += f"{items2}\n"
          embed = discord.Embed(title="Inventory | Toys", description=f"__**Toys List**__\n>>> {merge}")
          embedslist.append(embed)
        await interaction.edit_original_response(content=None, embeds=embedslist)
      else:
        newlist = data['FinishedToysList']
        merge = ""
        for items in newlist:
          if len(items) != 0:
            merge += f"{items}\n"
        embed = discord.Embed(title="Inventory | Toys", description=f"__**Toys List**__\n>>> {merge}")
        await interaction.edit_original_response(content=None, embed=embed)

    elif select.values[0] == "Gifts":
      
      if len(data['FinishedGiftsList']) == 1:
        return await interaction.edit_original_response(content="**This category is empty!**")

      if len(data['FinishedGiftsList']) > 30:
        newlist = chunk(data['FinishedGiftsList'], 30)
        embedslist = []
        for items in newlist:
          merge = ""
          for items2 in items:
            if len(items2) != 0:
              merge += f"{items2}\n"
          embed = discord.Embed(title="Inventory | Gifts", description=f"__**Gifts List**__\n>>> {merge}")
          embedslist.append(embed)
        await interaction.edit_original_response(content=None, embed=embedslist)
      else:
        newlist = data['FinishedGiftsList']
        merge = ""
        for items in newlist:
          if len(items) != 0:
            merge += f"{items}\n"
        embed = discord.Embed(title="Inventory | Gifts", description=f"__**Gifts List**__\n>>> {merge}")
        await interaction.edit_original_response(content=None, embed=embed)

isCmdBeingUsed = False

class DeleteTicketConfirm(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
  @discord.ui.button(row=0, label="Confirm", style=discord.ButtonStyle.red, custom_id="yesdeleteticket", disabled=False)
  async def button_callback1(self, button, interaction):

    con,cur = openCON()
    cur.execute(f"SELECT * FROM channels WHERE channel_id='{interaction.channel.id}'")
    resSQL = cur.fetchall()[0]

    trader_ids = []
    trader_ids.append(int(resSQL['trader_receiver_id']))
    trader_ids.append(int(resSQL['trader_seller_id']))

    await interaction.response.defer()

    if interaction.user.id not in trader_ids:
      return

    if str(resSQL['ticket_status']) == "Delete":
      closeCON(cur,con)
      await interaction.message.reply("*The ticket is already being closed!*")
      return

    msg_embed = interaction.message.embeds[0]
    field = msg_embed.fields[0]
    agreed_users = None
    if field.value == "`None`":
      closeCON(cur,con)
      msg_embed.fields[0].value = f"{interaction.user.mention} has agreed on closing this ticket."
      await interaction.message.edit(embed=msg_embed)
      return

    if agreed_users == None:
      msglist = field.value.splitlines(True)
      if len(msglist) == 1:
        signed_user_id = int(find_between(msglist[0], "<@", ">"))
        if signed_user_id == interaction.user.id:
          closeCON(cur,con)
          return

        for child in self.children:
          child.disabled = True

        newmsg = f"\n{interaction.user.mention} has agreed on closing this ticket."
        msg_embed.fields[0].value = msg_embed.fields[0].value + newmsg
        await interaction.message.edit(embed=msg_embed, view=self)
        cur.execute(f"UPDATE channels SET ticket_status='Delete' WHERE channel_id='{interaction.channel.id}'")
        con.commit()
        closeCON(cur,con)
        await interaction.channel.send(embed=discord.Embed(description=f'Closing this ticket..', color=MAINCOLOR))

        ticketlogs = bot.get_channel(AUTOAMP_LOGS_ID)
        transcripts = bot.get_channel(AUTOAMP_TRANSCRIPTS_ID)

        channelownerid = resSQL['channel_owner_id']
        sellerid = resSQL['trader_seller_id']
        buyerid = resSQL['trader_receiver_id']
        tradeid1 = resSQL['trade_id']
        tradeid2 = resSQL['redeem_trade_id']
        recuser = resSQL['receiver_username']
        senduser = resSQL['seller_username']
        passid = resSQL['gamepass_id']

        logembed = discord.Embed(color=MAINCOLOR)
        logembed = discord.Embed(description=f"Author: **Both Traders**\nTicket: **{interaction.channel.name}** | ID: {interaction.channel.id}\nAction: **Deleted Ticket**", color=0xed4245)

        await ticketlogs.send(embed=logembed)
        transcript = await chat_exporter.export(channel=interaction.channel, limit=None, tz_info="Asia/Singapore")
        if transcript is None:
          return
        transcript_file = discord.File(io.BytesIO(transcript.encode()), filename=f"transcript-{interaction.channel.name}.html")
        transcriptembed = discord.Embed(color=0x1EC45C)
        transcriptembed.add_field(name="Ticket", value=f"{interaction.channel.name} | {interaction.channel.id}", inline=True)
        transcriptembed.add_field(name="Category", value=f"{interaction.channel.category.name} | {interaction.channel.category.id}", inline=True)
        transcriptembed.add_field(name="Info", value=f"Owner: <@{channelownerid}>\nSeller: <@{sellerid}>\nBuyer: <@{buyerid}>\nFirst Trade ID: {tradeid1}\nSecond Trade ID: {tradeid2}\nSender Username: `{senduser}`\nReceiver Username: `{recuser}`\nGamepass ID: `{passid}`", inline=False)
        mess = await transcripts.send(embed=transcriptembed, file=transcript_file)
        attachment = mess.attachments[0]
        messages = await interaction.channel.history(limit=None).flatten()
        users={}
        for msg in messages[::1]:
            if msg.author.id in users.keys():
              users[msg.author.id]+=1
            else:
              users[msg.author.id]=1
        user_string,user_transcript_string="",""
        b = sorted(users.items(), key=lambda x: x[1], reverse=True)
        try:
          for k in b:
            user = await bot.fetch_user(int(k[0]))
            user_string+=f"{k[1]} | {user.mention} | {user.name}#{user.discriminator}\n"
        except NotFound:
          pass
        await mess.edit(embed=transcriptembed.add_field(name="**Direct Transcript**", value=f"[Direct Transcript](https://mahto.id/chat-exporter?url={attachment.url})", inline=True))
        await mess.edit(embed=transcriptembed.add_field(name="**Users in transcript**", value=f"{user_string}", inline=True))
        await interaction.channel.delete()


@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def close(ctx):
  if ctx.message.channel.category.id == AUTOAMP_CATEGORY_ID:

    con,cur = openCON()
    cur.execute(f"SELECT * FROM channels WHERE channel_id='{ctx.channel.id}'")
    resSQL = cur.fetchall()
    if len(resSQL) == 0:
      closeCON(cur,con)
      return await ctx.reply("This channel isn't a ticket.")
    resSQL = resSQL[0]
    closeCON(cur,con)

    if resSQL['ticket_status'] == "Pending":
      return await ctx.reply(embed=discord.Embed(description="<:redci:879849638855852112>  **You can't use this while the ticket is set on pending**  <:redci:879849638855852112>", color=redcolor))

    if resSQL['ticket_status'] == "Active":

      usersIds = []
      usersIds.append(resSQL['trader_seller_id'])
      usersIds.append(resSQL['trader_receiver_id'])
      if ctx.author.id not in usersIds:
        return

      embed = discord.Embed(title="Are you sure you want to close this ticket?", description='Clicking "**Confirm**" will close the ticket.\nBoth traders are required to click this button for it to go through.', color=redcolor)
      embed.add_field(name="Agreed", value="`None`", inline=False)
      await ctx.send(embed=embed, view=DeleteTicketConfirm())

@bot.command()
async def editsubview(ctx, msgid):
  if ctx.author.id != 358594990982561792:
    return
  msg = await ctx.channel.fetch_message(int(msgid))
  await msg.edit(view=PasteAddress())

class PasteAddress(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
  @discord.ui.button(row=0, label="Paid", style=discord.ButtonStyle.green, custom_id="paidcash", disabled=False)
  async def button_callback2(self, button, interaction):

    if (interaction.user.id not in TicketAccess) and (interaction.user.id != interaction.message.mentions[0].id):
      return await interaction.response.defer()
        
    subuser_id = interaction.message.mentions[0].id
    subuser = interaction.guild.get_member(subuser_id)

    con,cur = openCON()
    cur.execute(f"SELECT * FROM sub_tickets WHERE channel_id='{interaction.channel.id}'")
    resSQL = cur.fetchall()[0]

    for child in self.children:
      child.disabled = True
    await interaction.message.edit(view=self)

    await interaction.response.defer()

    key = PrivateKey(resSQL['crypto_wif'])
    req_amount = resSQL['btc_amount']
    req_btc = shorten_btc(req_amount-0.000015)
    btc_bal = float(key.get_balance(currency='btc'))
    if btc_bal >= req_btc:
      cur.execute(f"UPDATE sub_tickets SET has_paid='Yes' WHERE channel_id='{interaction.channel.id}'")
      con.commit()
      closeCON(cur,con)
      
      boughtAt_ts = datetime.now()
      endsAt_ts = boughtAt_ts+timedelta(days=30)

      boughtAt_ts = int(boughtAt_ts.timestamp())
      endsAt_ts = int(endsAt_ts.timestamp())

      embeda = discord.Embed(title="🟢 Payment Received 🟢", description=f">>> Thank you for using our services!\nYour subscription will end on <t:{endsAt_ts}:f>\nYou can view your subscrition information by typing the command `$sub`, such info as expiration date, purchased date and additional extension period.", color=SUCCCOLOR)
      await interaction.channel.send(embed=embeda)

      subrole = interaction.guild.get_role(SUBSCRIBER_ROLE)
      await subuser.add_roles(subrole)

      dataToSend = {'userID': subuser.id, 'boughtAt': boughtAt_ts, 'endsAt': endsAt_ts, 'extended': 0}
      subsToAdd.append(dataToSend)

      embed = discord.Embed(title="🟢 Paid 🟢", color=SUCCCOLOR)
      c = bot.get_channel(CRYPTO_LOGS)
      msgreply = await c.fetch_message(resSQL['message_id'])
      await msgreply.reply(embed=embed)

    elif btc_bal == 0:
      closeCON(cur,con)
      await interaction.message.edit(view=PasteAddress())
      return await interaction.channel.send(f"{interaction.user.mention} No transactions were detected.", delete_after=5)
    else:
      closeCON(cur,con)
      await interaction.message.edit(view=PasteAddress())
      usd_am = key.get_balance(currency='usd')
      rem_btc = req_amount-btc_bal
      await interaction.channel.send(f"The bot received only `{btc_bal}` BTC (`${usd_am}`). Please send `{rem_btc}` BTC more!", delete_after=10)
      return

  @discord.ui.button(row=0, label="Paste Address", style=discord.ButtonStyle.blurple, custom_id="pasteaddress", disabled=False)
  async def button_callback1(self, button, interaction):

    if interaction.user.id != interaction.message.mentions[0].id:
      return await interaction.response.defer()

    address = interaction.message.embeds[1].fields[2].value.replace(f"```", "")
    await interaction.response.send_message(content=address, ephemeral=True)

class PasteGamepass(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
  @discord.ui.button(row=0, label="Paid", style=discord.ButtonStyle.green, custom_id="paidrobux", disabled=False)
  async def button_callback2(self, button, interaction):
    global sessionCheck

    con,cur = openCON()
    cur.execute(f"SELECT * FROM channels WHERE channel_id='{interaction.channel.id}'")
    resSQL = cur.fetchall()[0]

    if resSQL['has_paid_fee'] == "Yes":
      closeCON(cur,con)
      await interaction.response.defer()
      return

    isKookie = False
    if interaction.user.id in TicketAccess:
      isKookie = True
    if isKookie == False:
      usersIds = []
      usersIds.append(resSQL['trader_seller_id'])
      usersIds.append(resSQL['trader_receiver_id'])
      if interaction.user.id not in usersIds:
        closeCON(cur,con)
        await interaction.response.defer()
        return

    for child in self.children:
      child.disabled = True
    await interaction.message.edit(view=self)

    try:
      await interaction.response.defer()
    except NotFound:
      pass

    paymmsg = await interaction.message.reply(f"Checking payment.. this may take a while")

    passid = int(resSQL['gamepass_id'])
    ticketstarted = resSQL['gamepass_start_ts']

    sessionCheck = getrbxSession()
    txFound = False
    params = {'transactionType': 'Sale', 'limit': '100'}
    try:
      res = sessionCheck.get(f'https://economy.roblox.com/v2/users/{GAMEPASS_ACCID}/transactions', params=params)
      resData = res.json()['data']
    except Exception:
      closeCON(cur,con)
      await interaction.message.edit(view=PasteGamepass())
      await interaction.channel.send(f"{interaction.user.mention} No transactions were detected.", delete_after=5)
      await paymmsg.delete()
      return
    if len(resData) != 0:
      for i in res.json()['data']:
        passid_new = i['details']['id']
        try:
          namepass = int(i['details']['name'])
          timepass = int(arrow.get(i['created']).timestamp())          
          if (passid == passid_new) and (interaction.channel.id == namepass) and (timepass > ticketstarted):
            txFound = True
            break
        except ValueError:
          pass

    if txFound == False:
      closeCON(cur,con)
      await interaction.message.edit(view=PasteGamepass())
      await paymmsg.delete()
      return await interaction.channel.send(f"{interaction.user.mention} No transactions were detected.", delete_after=5)

    json_data = {'id': passid, 'name': 'AM Fee'}
    sessionCheck.post('https://www.roblox.com/game-pass/update', json=json_data)

    cur.execute(f"UPDATE channels SET has_paid_fee='Yes' WHERE channel_id='{interaction.channel.id}'")
    con.commit()
    closeCON(cur,con)

    await interaction.channel.send(f"> <@{resSQL['trader_receiver_id']}> Join the vip server via `$am` command, then type `$redeem` in Roblox chat.", embed=discord.Embed(title="<:succ:926608308033441792> **The Fee Has Been Paid** <:succ:926608308033441792>", color=MAINCOLOR))
    await paymmsg.delete()
  @discord.ui.button(row=0, label="Paste Gamepass Link", style=discord.ButtonStyle.blurple, custom_id="pastegamepass", disabled=False)
  async def button_callback1(self, button, interaction):
    global session
    link = interaction.message.embeds[0].fields[1].value.replace("> [Link](", "").replace(")", "")
    await interaction.response.send_message(content=link, ephemeral=True)

  @discord.ui.button(row=0, label="Bypass (ADMIN)", style=discord.ButtonStyle.gray, custom_id="bypassbutton1", disabled=False)
  async def button_callback3(self, button, interaction):

    if interaction.user.id not in TicketAccess:
      await interaction.response.send_message(content="You cannot use this button!", ephemeral=True)
      return

    for child in self.children:
      child.disabled = True
    await interaction.message.edit(view=self)

    await interaction.response.defer()

    con,cur = openCON()
    cur.execute(f"SELECT * FROM channels WHERE channel_id='{interaction.channel.id}'")
    resSQL = cur.fetchall()[0]

    sessionCheck = getrbxSession()
    passid = resSQL['gamepass_id']
    json_data = {'id': passid, 'name': 'AM Fee'}
    sessionCheck.post('https://www.roblox.com/game-pass/update', json=json_data)

    cur.execute(f"UPDATE channels SET has_paid_fee='Yes' WHERE channel_id='{interaction.channel.id}'")
    con.commit()
    closeCON(cur,con)
    await interaction.channel.send(f"> <@{resSQL['trader_receiver_id']}> Join the vip server via `$am` command, then type `$redeem` in Roblox chat.", embed=discord.Embed(title="<:succ:926608308033441792> **Bypassed** <:succ:926608308033441792>", color=MAINCOLOR))

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def confirm(ctx):
  if ctx.message.channel.category.id == AUTOAMP_CATEGORY_ID:

    con,cur = openCON()
    cur.execute(f"SELECT * FROM channels WHERE channel_id='{ctx.channel.id}'")
    resSQL = cur.fetchall()
    if len(resSQL) == 0:
      closeCON(cur,con)
      return await ctx.reply("This channel isn't a ticket.")
    resSQL = resSQL[0]
    closeCON(cur,con)

    if resSQL['ticket_status'] == "Pending":
      return await ctx.reply(embed=discord.Embed(description="<:redci:879849638855852112>  **You can't use this while the ticket is set on pending**  <:redci:879849638855852112>", color=redcolor))

    if resSQL['ticket_status'] == "Active":
      isKookie = False
      if ctx.author.id in TicketAccess:
        isKookie = True
      if isKookie == False:
        if ctx.author.id != resSQL['trader_seller_id']:
          return await ctx.reply(embed=discord.Embed(description="<:redci:879849638855852112>  **You do not have permissions to use this**  <:redci:879849638855852112>", color=redcolor))
      
      if resSQL['pets_received'] == "No":
        return await ctx.reply(embed=discord.Embed(description="<:redci:879849638855852112>  **The bot has not received any items yet, the seller must use the `$send` command**  <:redci:879849638855852112>", color=redcolor))
      
      if resSQL['trade_confirmed'] == "Yes":
        return await ctx.reply(embed=discord.Embed(description="<:redci:879849638855852112>  **The trade has already been confirmed**  <:redci:879849638855852112>", color=redcolor))

      class haveYouBeenPaid(discord.ui.View):
        def __init__(self):
          super().__init__(timeout=None)
        @discord.ui.button(row=0, label="Yes", style=discord.ButtonStyle.green, custom_id="lolYes", disabled=False)
        async def button_callback1(self, button, interaction):
          con,cur = openCON()
          cur.execute(f"SELECT * FROM channels WHERE channel_id='{interaction.channel.id}'")
          resSQL = cur.fetchall()[0]

          isKookie = False
          if interaction.user.id in TicketAccess:
            isKookie = True
          if isKookie == False:
            if interaction.user.id != resSQL['trader_seller_id']:
              closeCON(cur,con)
              await interaction.response.defer()
              return await interaction.channel.send(content=f"{interaction.user.mention} **You can't use this**", delete_after=2)
          
          for child in self.children:
            child.disabled = True
          await interaction.message.edit(view=self)

          try:
            await interaction.response.defer()
          except NotFound:
            pass

          cur.execute(f"UPDATE channels SET trade_confirmed='Yes' WHERE channel_id='{interaction.channel.id}'")
          con.commit()

          if FEE_MODE == False:
            cur.execute(f"UPDATE channels SET has_paid_fee='Yes' WHERE channel_id='{interaction.channel.id}'")
            con.commit()
            closeCON(cur,con)
            await interaction.channel.send(f"> <@{resSQL['trader_receiver_id']}> Join the vip server via `$am` command, then type `$redeem` in Roblox chat.")
            return
          
          elif FEE_MODE == True:
            #hasSub = False
            #userWithSub = ""
            #subsList = await readSubs()
            #users_inticket = [resSQL['trader_seller_id'], resSQL['trader_receiver_id']]
            subrole = interaction.guild.get_role(SUBSCRIBER_ROLE)
            tradersliste = [interaction.guild.get_member(resSQL['trader_seller_id']), interaction.guild.get_member(resSQL['trader_receiver_id'])]
            isSubto = False
            for tr in tradersliste:
              if subrole in tr.roles:
                isSubto = True
                userWithSub = tr.id
                break
            #for subi in subsList:
            #  if subi['userID'] in users_inticket:
            #    hasSub = True
            #    userWithSub = subi['userID']
            #    break

            if isSubto == True:
              cur.execute(f"UPDATE channels SET has_paid_fee='Yes' WHERE channel_id='{interaction.channel.id}'")
              con.commit()
              closeCON(cur,con)
              await interaction.channel.send(f"> <@{resSQL['trader_receiver_id']}> Join the vip server via `$am` command, then type `$redeem` in Roblox chat.", embed=discord.Embed(title="<:succ:926608308033441792> **Fee Skipped** <:succ:926608308033441792>", description=f"The fee has been skipped because <@{userWithSub}> is a subscriber.", color=MAINCOLOR))
              return
            else:
              sessionCheck = getrbxSession()
              params = {'sortOrder': 'Asc', 'limit': '50'}
              res = sessionCheck.get(f'https://games.roblox.com/v1/games/{GAME_PASS}/game-passes', params=params)
              selectedpass = 0
              try:
                abc = res.json()['data']
              except Exception:
                time.sleep(3)
                res = sessionCheck.get(f'https://games.roblox.com/v1/games/{GAME_PASS}/game-passes', params=params)
              for i in res.json()['data']:
                passid = i['id']
                passname = i['name']
                if passname == "AM Fee":
                  json_data = {'id': passid, 'name': str(interaction.channel.id)}
                  sessionCheck.post('https://www.roblox.com/game-pass/update', json=json_data)
                  selectedpass = passid
                  break
                
              cur.execute(f"UPDATE channels SET gamepass_id='{selectedpass}', gamepass_start_ts='{int(time.time())}'  WHERE channel_id='{interaction.channel.id}'")
              con.commit()
              closeCON(cur,con)
              embed = discord.Embed(title="Middleman Fee", description="**One** of you has to buy the gamepass that is linked to this message in order for the trade to proceed. Refusal of paying the fee will result in a permanent ban.", color=MAINCOLOR)
              embed.add_field(name="Fee", value="> **150 b/t** <:Robux:914568435583836171>", inline=True)
              embed.add_field(name="Gamepass Link", value=f"> [Link](https://www.roblox.com/game-pass/{selectedpass})", inline=True)
              embed.set_footer(text="Click the \"Paid\" button once you have bought the gamepass.")
              await interaction.channel.send(f"<@{resSQL['trader_seller_id']}>, <@{resSQL['trader_receiver_id']}>", embed=embed, view=PasteGamepass())
            
        @discord.ui.button(row=0, label="No", style=discord.ButtonStyle.red, custom_id="Nopee", disabled=False)
        async def button_callback2(self, button, interaction):
          
          try:
            await interaction.response.defer()          
          except NotFound:
            pass

          isKookie = False
          if interaction.user.id in TicketAccess:
            isKookie = True
          if isKookie == False:
            if interaction.user.id != resSQL['trader_seller_id']:
              return await interaction.channel.send(content=f"{interaction.user.mention} **You can't use this**", delete_after=2)

          await interaction.message.delete()
      
      embed=discord.Embed(title="⚠ Are you sure you have received your items/money? ⚠", description=f"> Clicking \"**Yes**\", will give your buyer permission to withdraw their adopt me items.\n> # **This __does not__ cancel the trade! You are allowing <@{resSQL['trader_receiver_id']}> to take the items!**", color=redcolor)
      await ctx.reply(embed=embed, view=haveYouBeenPaid())


@bot.command(aliases=['rti'])
@commands.cooldown(1, 10, commands.BucketType.user)
async def returnitems(ctx):
  if ctx.message.channel.category.id == AUTOAMP_CATEGORY_ID:
    global sessionCheck
    global isCmdBeingUsed

    isKookie = False
    if ctx.author.id in TicketAccess:
      isKookie = True
    if isKookie == False:
      return await ctx.reply(embed=discord.Embed(description="<:redci:879849638855852112>  **You do not have permissions to use this**  <:redci:879849638855852112>", color=redcolor))

    con,cur = openCON()
    cur.execute(f"SELECT * FROM channels WHERE channel_id='{ctx.channel.id}'")
    resSQL = cur.fetchall()
    if len(resSQL) == 0:
      closeCON(cur,con)
      return await ctx.reply("This channel isn't a ticket.")
    resSQL = resSQL[0]
    closeCON(cur,con)

    if resSQL['ticket_status'] != "Pending":
      return await ctx.reply(embed=discord.Embed(description="<:redci:879849638855852112>  **You can't use this while the ticket is active**  <:redci:879849638855852112>", color=redcolor))

    dbmain = bot.get_channel(MAIN_INFOID)
    maindata_msg = await dbmain.history(limit=1, oldest_first=True).flatten();maindata_msg=maindata_msg[0]
    maindata = maindata_msg.content
    if maindata == "No":
      await ctx.reply(embed=discord.Embed(description="<:redci:879849638855852112>  **The bot is currently not in the vip server, it will rejoin in a minute**  <:redci:879849638855852112>", color=redcolor))
      return
    
    traderusername = resSQL['seller_username']

    dbchannel = bot.get_channel(1002208531434450974)
    logsdata_msg = await dbchannel.fetch_message(1002209717923369030)
    file = logsdata_msg.attachments[0]
    cont = await file.read()
    tradehistory_data = ast.literal_eval(cont.decode('utf-8'))
    tradeids = []
    for i in tradehistory_data:
      tradeids.append(i['tradeID'])

    resSQL['redeem_trade_id'] = ast.literal_eval(resSQL['redeem_trade_id'])
    resSQL['trade_id'] = ast.literal_eval(resSQL['trade_id'])
    tradesFound = False
    trade_num = 0
        
    for redeemtradeID in resSQL['redeem_trade_id']:
      if redeemtradeID not in tradeids:
        break
      trade_num = trade_num+1
    try:
      tradeID = resSQL['trade_id'][trade_num]
    except IndexError:
      tradesFound = True

    if tradesFound == True: # if the trade found in history
      return await ctx.reply(embed=discord.Embed(description="<a:oklol:858377249949220904>  **The trader has already got their items**  <a:oklol:858377249949220904>", color=grey))

    plrlist = await readPlayerList()
    plrliste = []
    for i in plrlist:
      plrliste.append(i['username'])
    if traderusername not in plrliste:
      return await ctx.reply(embed=discord.Embed(description="<:redci:879849638855852112>  **The trader is not in the vip server, please join it via `$am` command**  <:redci:879849638855852112>", color=redcolor))

    datayes = await readSendTradeTab()

    if datayes['isOpen'] == True:
      return await ctx.reply(embed=discord.Embed(description="<:redci:879849638855852112>  **The bot is currently trading with someone, try again once <#1081234786443603979> is named as `Available`**  <:redci:879849638855852112>", color=redcolor))
    
    if isCmdBeingUsed == True:
      return await ctx.reply(embed=discord.Embed(description="<:redci:879849638855852112>  **The bot is currently trading with someone**  <:redci:879849638855852112>", color=redcolor))

    isCmdBeingUsed = True
    jsdata = f"{ctx.channel.id}-#####-{traderusername}-#####-{tradeID}"
    updateSentTrades(jsdata)
    await ctx.reply(embed=discord.Embed(title="<:succ:926608308033441792>  **Trade Sent**  <:succ:926608308033441792>", description="You didn't get a trade? Make sure you have your trades set so everyone can send you a trade. If that's not the case, consider pinging @Kookie", color=MAINCOLOR))
    await ctx.send("https://cdn.discordapp.com/attachments/886224596150403112/1007340286399238294/unknown.png")
    await asyncio.sleep(2)
    isCmdBeingUsed = False
    return

@bot.command()
async def remove(ctx, user : discord.Member):
  rolereq = ctx.guild.get_role(MM_ROLE_ID)
  if rolereq in ctx.author.roles:
    if (ctx.channel.category.id == AUTOAMP_CATEGORY_ID):
      ticketlogs = bot.get_channel(AUTOAMP_LOGS_ID)

      con,cur = openCON()
      cur.execute(f"SELECT * FROM channels WHERE channel_id='{ctx.channel.id}'")
      resSQL = cur.fetchall()
      if len(resSQL) == 0:
        closeCON(cur,con)
        return await ctx.reply("This channel isn't a ticket.")
      resSQL = resSQL[0]

      if rolereq in user.roles:
        return await ctx.reply("BRO! Why are you trying to remove your crew mate 😭")

      Toggle = True
      if str(resSQL['ticket_status']) == "Closed" or str(resSQL['ticket_status']) == "Delete":
        closeCON(cur,con)
        await ctx.reply("*You can't use this while the ticket is closed!*")
        Toggle = False
        return
      if Toggle == True:
        await ctx.message.channel.set_permissions(user, overwrite=None)
        await ctx.send(f"{user.mention}", embed=discord.Embed(description=f'***{user.mention} was removed from the ticket {ctx.channel.mention}***', color=0xed4245))
        logembed = discord.Embed(description=f"Author: **{ctx.author.name}#{ctx.author.discriminator}** | ID: {ctx.author.id}\nTicket: **{ctx.channel.name}** | ID: {ctx.channel.id}\nAction: **Removed {user.name}#{user.discriminator} | ID: {user.id}**", color=0xed4245)
        logembed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=f"{ctx.author.display_avatar.url}")
        await ticketlogs.send(embed=logembed)

        cur.execute(f"UPDATE channels SET channel_owner_id='0' WHERE (channel_id='{ctx.channel.id}' AND channel_owner_id='{user.id}')")
        cur.execute(f"DELETE FROM added_users WHERE (user_id='{user.id}' AND channel_id='{ctx.channel.id}')")
        con.commit()
        closeCON(cur,con)

@remove.error
async def remove_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.reply(embed=discord.Embed(description=f"***User is missing!***\n***Usage: `{PREFIX}remove @user` or `{PREFIX}remove userID`***", color=0xed4245))
  if isinstance(error, commands.MemberNotFound):
    await ctx.reply(embed=discord.Embed(description="***User wasn't found!***", color=0xed4245))

@bot.command()
async def transcript(ctx):
  users={}
  rolereq = ctx.guild.get_role(MM_ROLE_ID)
  if (rolereq in ctx.author.roles):
    if (ctx.channel.category.id == AUTOAMP_CATEGORY_ID) or (ctx.channel.category.id == CLOSED_CATEGORY_ID):
      transcripts = bot.get_channel(AUTOAMP_TRANSCRIPTS_ID)
      loading_embed = discord.Embed(description=f"**Transcript was saved in <#{AUTOAMP_TRANSCRIPTS_ID}>**",color = 0xffffff)

      con,cur = openCON()
      cur.execute(f"SELECT * FROM channels WHERE channel_id='{ctx.channel.id}'")
      resSQL = cur.fetchall()
      if len(resSQL) == 0:
        closeCON(cur,con)
        return await ctx.reply("This channel isn't a ticket.")
      resSQL = resSQL[0]
      closeCON(cur,con)

      channelownerid = resSQL['channel_owner_id']
      sellerid = resSQL['trader_seller_id']
      buyerid = resSQL['trader_receiver_id']
      tradeid1 = resSQL['trade_id']
      tradeid2 = resSQL['redeem_trade_id']
      recuser = resSQL['receiver_username']
      senduser = resSQL['seller_username']
      passid = resSQL['gamepass_id']

      msg = await ctx.reply(embed=loading_embed)
      transcript = await chat_exporter.export(channel=ctx.channel, limit=None, tz_info="Asia/Singapore")
      if transcript is None:
        return

      transcript_file = discord.File(io.BytesIO(transcript.encode()), filename=f"transcript-{ctx.channel.name}.html")
      transcriptembed = discord.Embed(color=0x1EC45C)
      transcriptembed.add_field(name="Author", value=f"{ctx.author.mention} | {ctx.author.id}", inline=True)
      transcriptembed.add_field(name="Ticket", value=f"{ctx.channel.name} | {ctx.channel.id}", inline=True)
      transcriptembed.add_field(name="Category", value=f"{ctx.channel.category.name} | {ctx.channel.category.id}", inline=True)
      transcriptembed.add_field(name="Info", value=f"Owner: <@{channelownerid}>\nSeller: <@{sellerid}>\nBuyer: <@{buyerid}>\nFirst Trade ID: {tradeid1}\nSecond Trade ID: {tradeid2}\nSender Username: `{senduser}`\nReceiver Username: `{recuser}`\nGamepass ID: `{passid}`", inline=False)

      mess = await transcripts.send(embed=transcriptembed, file=transcript_file)
      attachment = mess.attachments[0]
      messages = await ctx.channel.history(limit=None).flatten()
      for msg in messages[::1]:
          if msg.author.id in users.keys():
            users[msg.author.id]+=1
          else:
            users[msg.author.id]=1
      user_string,user_transcript_string="",""
      b = sorted(users.items(), key=lambda x: x[1], reverse=True)
      try:
        for k in b:
          user = await bot.fetch_user(int(k[0]))
          user_string+=f"{k[1]} | {user.mention} | {user.name}#{user.discriminator}\n"
      except NotFound:
        pass
      await mess.edit(embed=transcriptembed.add_field(name="**Direct Transcript**", value=f"[Direct Transcript](https://mahto.id/chat-exporter?url={attachment.url})", inline=True))
      await mess.edit(embed=transcriptembed.add_field(name="**Users in transcript**", value=f"{user_string}", inline=True))


@bot.command(aliases=['del'])
@commands.cooldown(1, 10, commands.BucketType.channel)
async def delete(ctx):
  users={}
  #rolereq = ctx.guild.get_role(MM_ROLE_ID)
  loading_embed = discord.Embed(color = 0x99AAB5)
  loading_embed.set_author(name="Loading Chat, Users, Messages and Time!", icon_url="https://cdn.discordapp.com/emojis/806591946730504212.gif?v=1 ")
  if (ctx.author.id in TicketAccess):
    if (ctx.channel.category.id == AUTOAMP_CATEGORY_ID) or (ctx.channel.category.id == CLOSED_CATEGORY_ID):

      con,cur = openCON()
      cur.execute(f"SELECT * FROM channels WHERE channel_id='{ctx.channel.id}'")
      resSQL = cur.fetchall()
      if len(resSQL) == 0:
        closeCON(cur,con)
        return await ctx.reply("This channel isn't a ticket.")
      resSQL = resSQL[0]

      if str(resSQL['ticket_status']) == "Delete":
        await ctx.reply("*The ticket is already being deleted!*")
        return

      ticketlogs = bot.get_channel(AUTOAMP_LOGS_ID)
      transcripts = bot.get_channel(AUTOAMP_TRANSCRIPTS_ID)

      channelownerid = resSQL['channel_owner_id']
      sellerid = resSQL['trader_seller_id']
      buyerid = resSQL['trader_receiver_id']
      tradeid1 = resSQL['trade_id']
      tradeid2 = resSQL['redeem_trade_id']
      recuser = resSQL['receiver_username']
      senduser = resSQL['seller_username']
      passid = resSQL['gamepass_id']

      await ctx.channel.send(embed=discord.Embed(description=f'Deleting this ticket..', color=MAINCOLOR))

      cur.execute(f"UPDATE channels SET ticket_status='Delete' WHERE channel_id='{ctx.channel.id}'")
      con.commit()
      closeCON(cur,con)

      await ctx.message.delete()
      logembed = discord.Embed(color=MAINCOLOR)
      logembed = discord.Embed(description=f"Author: **{ctx.author.name}#{ctx.author.discriminator}** | ID: {ctx.author.id}\nTicket: **{ctx.channel.name}** | ID: {ctx.channel.id}\nAction: **Deleted Ticket**", color=0xed4245)
      logembed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=f"{ctx.author.display_avatar.url}")

      await ticketlogs.send(embed=logembed)
      transcript = await chat_exporter.export(channel=ctx.channel, limit=None, tz_info="Asia/Singapore")
      if transcript is None:
        return
      transcript_file = discord.File(io.BytesIO(transcript.encode()), filename=f"transcript-{ctx.channel.name}.html")
      transcriptembed = discord.Embed(color=0x1EC45C)
      transcriptembed.add_field(name="Author", value=f"{ctx.author.mention} | {ctx.author.id}", inline=True)
      transcriptembed.add_field(name="Ticket", value=f"{ctx.channel.name} | {ctx.channel.id}", inline=True)
      transcriptembed.add_field(name="Category", value=f"{ctx.channel.category.name} | {ctx.channel.category.id}", inline=True)
      transcriptembed.add_field(name="Info", value=f"Owner: <@{channelownerid}>\nSeller: <@{sellerid}>\nBuyer: <@{buyerid}>\nFirst Trade ID: {tradeid1}\nSecond Trade ID: {tradeid2}\nSender Username: `{senduser}`\nReceiver Username: `{recuser}`\nGamepass ID: `{passid}`", inline=False)
      mess = await transcripts.send(embed=transcriptembed, file=transcript_file)
      attachment = mess.attachments[0]
      messages = await ctx.channel.history(limit=None).flatten()
      for msg in messages[::1]:
          if msg.author.id in users.keys():
            users[msg.author.id]+=1
          else:
            users[msg.author.id]=1
      user_string,user_transcript_string="",""
      b = sorted(users.items(), key=lambda x: x[1], reverse=True)
      try:
        for k in b:
          user = await bot.fetch_user(int(k[0]))
          user_string+=f"{k[1]} | {user.mention} | {user.name}#{user.discriminator}\n"
      except NotFound:
        pass
      await mess.edit(embed=transcriptembed.add_field(name="**Direct Transcript**", value=f"[Direct Transcript](https://mahto.id/chat-exporter?url={attachment.url})", inline=True))
      await mess.edit(embed=transcriptembed.add_field(name="**Users in transcript**", value=f"{user_string}", inline=True))
      await ctx.channel.delete()


@bot.listen()
async def on_command_error(ctx, error):
  if isinstance(error, CommandNotFound):
    pass
  elif isinstance(error, commands.CommandOnCooldown):
    hours = int(time.time() + error.retry_after)
    await ctx.reply(embed=discord.Embed(description=f"<a:loading:1002330071043944501>  **You're doing that too quickly, try again <t:{hours}:R>**  <a:loading:1002330071043944501>", color=grey))

@bot.command()
async def guidee(ctx):
  if ctx.author.id in TicketAccess:
    text = "{yourUsername}"
    embed1=discord.Embed(title="__Ticket Progress__", description=f"> You will already be told what to do in the ticket, this is just in case you want a full detailed explanation.\n\n> **1.** Once you create a ticket, you will be asked to specify whether if you are the seller or the buyer and your Roblox username and your trader's Discord user/id/mention, your trader will be asked about their Roblox username.\n\n> **2.** After you're done with the questions part, the seller will be asked to join the vip server via link, there's no alternative way to join the vip server. If you are the seller, join the vip server, then use the `$send` command.\n> The bot will send you a trade in-game, accept it and add the items in the trade and accept, after you've accepted the bot will send an embed in the ticket with a Yes&No buttons, the embed will contain info about the items the seller has placed in the trade. By the way, if you didn't receive a trade, it's either because you have your trades on \"Only Friends Can Trade Me\" or \"No One Can Trade Me\", if you do then make sure to change it to \"Anyone Can Trade Me\" in your Adopt Me settings, you may re-use the command after the cooldown.\n> The bot will either accept or decline the trade according to which button your trader will select, if they select the \"Yes\" button, it'll accept, if they select the \"No\" button then it declines, so yeah it will require both traders to be active during that time.\n\n> **3.** After you've given the items to the bot, select the `Proceed` button. The seller has to select it. The command will make the bot fetch the trade history and double check if the trade went through. If you are still not sure if the bot has your items, you may use the `$tradehistory/$th` and `$inventory/$inv` commands.\n\n> **4.** If the trade was successful (the bot will tell you if it was or not), then the buyer is safe to pay their seller the items or money they promised. So after the seller has been given the stuff the buyer promised to give, they are required to use the `$confirm` command in order for the buyer to be able to redeem their items.\n\n> **5.** After the seller has used the `$confirm` command, the buyer joins the vip server with the `$am` command and once they are in, they should use the `$redeem` command to receive their items, so basically with that command, the bot will send you a trade and will ask you in the ticket if it is currently trading with you (An embed with Yes&No buttons), if you select \"Yes\" then the bot will add the items to the trade and accept it, if you select no, the trade will be declined. For the buyer, the bot will send you a trade to the username that you've stated at the start of the ticket, if you wanted to modify that user, use the `$setuser {text}` to change the username, then you may re-use the command.", color=MAINCOLOR)
    embed2=discord.Embed(title="__Commands__", description=f"**Global Commands** -> *both traders can use*\n> ・`$inventory`/`$inv`\n> Description: Displays the bot's inventory.\n> ・`$tradehistory`/`$th`\n> Description: Displays the latest 500 completed trades from trade history.\n> ・`$am`\n> Description: Sends link to the adopt me vip server.\n> ・`$setuser {text}` -> ||*this is optional in case you wanted to modify the user you want to send or redeem the items on*||\n> Description: Modifies the username that you're going to redeem your items on.\n\n**Seller's Commands** -> *only the seller can use*\n> ・`$send`\n> Description: The bot sends you a trade in-game so you can give it the items.\n> ・`$confirm`\n> Description: Marks the trade as completed, which allows your buyer to receive their adopt me items that you've given.\n\n**Buyer's Commands** -> *only the buyer can use*\n> ・`$redeem`\n> Description: The bot sends you a trade in-game and gives you your items.", color=MAINCOLOR)
    embed3=discord.Embed(title="__Notes__", description=f"・You can only trade with the bot via `$send` or `$redeem` commands.\n\n・The system is not 24/7.\n\n・If you wanted to cancel the trade and the bot has your items, ping either Kookie or Jace and they will return your items. Currently, there is no way to trade back your items via a command, but the tickets will be monitored. In case the system was turned off while the bot is holding your items and Kookie&Jace were off, just relax, all commands and functions will be turned off along with it, therefore the bot won't randomly disturb your items.\n\n・In case your buyer is trolling and they aren't paying you, ping one of the admins and they will get banned. The same goes if the seller didn't want to confirm that they've received their payment.\n\n・It is possible that adopt me or Roblox receives an update while the bot is in the vip server and it might cause it to disconnect from the server, if that happens, ping Kookie and she will fix it.", color=MAINCOLOR)
    embeds = [embed1, embed2, embed3]
    await ctx.send(embeds=embeds)

def updateREQ(name):
  global sessionDiscord
  json_data = {'name': name}
  sessionDiscord.patch(f'https://discord.com/api/v9/channels/{REQUEST_CHANNEL_ID}', json=json_data)

@bot.command()
async def on2(ctx):
  if (ctx.message.author.id in TicketAccess):
    channel = bot.get_channel(REQUEST_CHANNEL_ID)
    await ctx.message.delete()
    msg = await channel.fetch_message(1135525812913848411)
    await msg.edit(view=AMP_Tickets())
    updateREQ("✅・req-adopt-me")

@bot.command()
async def off2(ctx):
  if (ctx.message.author.id in TicketAccess):
    channel = bot.get_channel(REQUEST_CHANNEL_ID)
    await ctx.message.delete()
    msg = await channel.fetch_message(1135525812913848411)
    await msg.edit(view=Off_AMP_Tickets())
    updateREQ("❌・req-adopt-me")


@bot.command(aliases=['cancel'])
async def setpend(ctx):
  if (ctx.message.author.id in TicketAccess) and (ctx.channel.category.id == AUTOAMP_CATEGORY_ID):
    con,cur = openCON()
    cur.execute(f"UPDATE channels SET ticket_status='Pending', trade_confirmed='Yes' WHERE channel_id='{ctx.channel.id}'")
    con.commit()
    closeCON(cur,con)
    await ctx.reply("✅")

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def setuser(ctx):
  if ctx.message.channel.category.id == AUTOAMP_CATEGORY_ID:
    global sessionCheck
    
    con,cur = openCON()
    cur.execute(f"SELECT * FROM channels WHERE channel_id='{ctx.channel.id}'")
    resSQL = cur.fetchall()[0]
    closeCON(cur,con)

    if resSQL['ticket_status'] == "Pending":
      return await ctx.reply(embed=discord.Embed(description="<:redci:879849638855852112>  **You can't use this while the ticket is set on pending**  <:redci:879849638855852112>", color=redcolor))

    if resSQL['ticket_status'] == "Active":
      usersIds = []
      usersIds.append(resSQL['trader_seller_id'])
      usersIds.append(resSQL['trader_receiver_id'])
      if ctx.author.id not in usersIds:
        return

      class ChangeUserView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)

        @discord.ui.button(label="Input Username", style=discord.ButtonStyle.primary, custom_id="changeusername")
        async def button_callback1(self, button, interaction:discord.Interaction):
            modal = ChangeUserModal(title="Write here your own username!")
            await interaction.response.send_modal(modal)

      class ChangeUserModal(Modal):
          def __init__(self, *args, **kwargs) -> None:
              super().__init__(*args, **kwargs)
              self.add_item(InputText(label="Your Username", min_length=3, max_length=20, required=True, style=discord.InputTextStyle.short))

          async def callback(self, interaction: discord.Interaction):
              username = str(self.children[0].value)

              if interaction.user.id != ctx.author.id:
                return await interaction.response.send_message(content="You can't use this!", ephemeral=True)

              await interaction.message.edit(view=None)
              await interaction.response.send_message(content=f"**Changing Username..**", ephemeral=True)

              json_data = {
                  'usernames': [
                      username,
                  ],
                  'excludeBannedUsers': True,
              }
              res = sessionCheck.post('https://users.roblox.com/v1/usernames/users', json=json_data)
              if len(res.json()['data']) == 0:
                await interaction.edit_original_response(embed=discord.Embed(description="<:redci:879849638855852112>  **The username was not found, please try again**  <:redci:879849638855852112>", color=redcolor))
                await interaction.message.edit(view=ChangeUserView())
                return

              okeuser = res.json()['data'][0]['name']
              
              con,cur = openCON()
              cur.execute(f"SELECT * FROM channels WHERE channel_id='{interaction.channel.id}'")
              resSQL = cur.fetchall()[0]

              if interaction.user.id == resSQL['trader_receiver_id']:
                cur.execute(f"SELECT channel_id FROM channels WHERE (ticket_status='Open' OR ticket_status='Active' OR ticket_status='Pending') AND (seller_username='{okeuser}' OR receiver_username='{okeuser}')")
                resSQL2 = cur.fetchall()
                user_found = len(resSQL2) != 0
                if user_found == True:
                  closeCON(cur,con)
                  await interaction.edit_original_response(embed=discord.Embed(description="<:redci:879849638855852112>  **The username has already been used! Please use another username or close your other ticket.**  <:redci:879849638855852112>", color=redcolor))
                  await interaction.message.edit(view=ChangeUserView())
                  return

                cur.execute(f"UPDATE channels SET receiver_username='{okeuser}' WHERE channel_id='{interaction.channel.id}'")
              elif interaction.user.id == resSQL['trader_seller_id']:
                cur.execute(f"SELECT channel_id FROM channels WHERE (ticket_status='Open' OR ticket_status='Active' OR ticket_status='Pending') AND (seller_username='{okeuser}' OR receiver_username='{okeuser}')")
                resSQL2 = cur.fetchall()
                user_found = len(resSQL2) != 0
                if user_found == True:
                  closeCON(cur,con)
                  await interaction.edit_original_response(embed=discord.Embed(description="<:redci:879849638855852112>  **The username has already been used! Please use another username or close your other ticket.**  <:redci:879849638855852112>", color=redcolor))
                  await interaction.message.edit(view=ChangeUserView())
                  return

                cur.execute(f"UPDATE channels SET seller_username='{okeuser}' WHERE channel_id='{interaction.channel.id}'")
              con.commit()
              closeCON(cur,con)
              await interaction.edit_original_response(embed=discord.Embed(title="<:succ:926608308033441792>  **Username Has Been Updated**  <:succ:926608308033441792>", color=MAINCOLOR))
              return

      await ctx.reply(embed=discord.Embed(title="Input your username", color=MAINCOLOR), view=ChangeUserView())


@bot.command()
@commands.cooldown(1, 10, commands.BucketType.channel)
async def am(ctx):
  if ctx.message.channel.category.id == AUTOAMP_CATEGORY_ID:
    vip_code = await getVipServerCode()
    
    embedaa = discord.Embed(title=f"<:link:1101251650674495539>・Adopt Me VIP Server", description=f"> **Link: https://www.roblox.com/games/920587237?privateServerLinkCode={vip_code} **\n\n> Bot's username is **`{MMACC_USER}`**", color=MAINCOLOR)
    embedaa.set_thumbnail(url="https://cdn.discordapp.com/attachments/816304640063963156/896318333639610419/imagen-hints-adopt-me-walkthrough-2019-0thumb.jpeg")
    
    await ctx.reply(embed=embedaa, view=TradeInfo())


async def editVipServerCode(con):
  c = bot.get_channel(1002209255052546170)
  msg = await c.fetch_message(1024711611006595122)
  await msg.edit(con)

@bot.command()
async def ream(ctx):
  if ctx.author.id in TicketAccess:
    rbxSession = getrbxSession()
    data = {"newJoinCode": True}
    Request = rbxSession.patch(f"https://games.roblox.com/v1/vip-servers/{AM_VIP_SERVER}", data=data)
    if Request.status_code == 200:

      a = rbxSession.get(f"https://games.roblox.com/v1/vip-servers/{AM_VIP_SERVER}")
      b = a.json()["joinCode"]

      await editVipServerCode(b)

      await ctx.reply("Regenerated vip server ✅")
    else:
      await ctx.reply(f"Error: `{Request.json()}`")

@bot.command()
async def rblock(ctx, username):
  if ctx.author.id in TicketAccess:
    rbxSession = getrbxSession()
    json_data = {
        'usernames': [
            username,
        ],
        'excludeBannedUsers': True,
    }
    res = rbxSession.post('https://users.roblox.com/v1/usernames/users', json=json_data)

    userid = res.json()['data'][0]['id']

    res1 = rbxSession.post(f'https://accountsettings.roblox.com/v1/users/{userid}/block')

    if res1.status_code == 200:
      await ctx.reply("The user has been blocked ✅")
    elif res1.status_code == 400:
      await ctx.reply("The user is already blocked.")
    else:
      await ctx.reply(f"Error: `{res1.json()}`")

@bot.command()
async def sblocked(ctx):
  if ctx.author.id in TicketAccess:
    rbxSession = getrbxSession()
    res = rbxSession.get('https://accountsettings.roblox.com/v1/users/get-detailed-blocked-users')
    users = ""
    for user in res.json()['blockedUsers']:
      users += f"`{user['name']}`\n"
    embed = discord.Embed(title="Blocked Users", description=users, color=MAINCOLOR)
    await ctx.reply(embed=embed)

@bot.command()
async def shutdown(ctx):
  if ctx.author.id in TicketAccess:
    rbxSession = getrbxSession()
    res = rbxSession.get('https://www.roblox.com/games/920587237/Adopt-Me')
    soup = bs4.BeautifulSoup(res.content, 'html.parser')
    verify_value = soup.find('input', attrs={'name':'__RequestVerificationToken'})['value']
    json_data = {
      '__RequestVerificationToken': verify_value,
      'placeId': 920587237,
      'gameId': '4409a9ef-7076-7bbb-4567-db0837538bda',
      'privateServerId': AM_VIP_SERVER,
    }
    # send to shutdown-requests
    shutdown = bot.get_channel(SHUTDOWN_ID)
    await shutdown.send(1)

    res1 = rbxSession.post('https://www.roblox.com/game-instances/shutdown', json=json_data)
    if res1.status_code == 200:
      await ctx.reply("Vip has been shutdown ✅")
    else:
      await ctx.reply(f"Error: `{res1.json()}`")

@bot.command()
async def friend(ctx, username):
  if ctx.author.id in TicketAccess:
    rbxSession = getrbxSession()
    json_data = {
      'usernames': [
        username,
      ],
      'excludeBannedUsers': True,
    }
    res1 = rbxSession.post('https://users.roblox.com/v1/usernames/users', json=json_data)
    if len(res1.json()['data']) == 0:
      return await ctx.reply("Invalid username.")
    userid = res1.json()['data'][0]['id']
    json_data = {'friendshipOriginSourceType': 'Unknown'}
    res2 = rbxSession.post(f'https://friends.roblox.com/v1/users/{userid}/request-friendship', json=json_data)
    foundError = True
    try:
      errors = res2.json()['errors']
    except KeyError:
      foundError = False
    if foundError == True:
      errorMsg = getErrorMsg(errors[0]['code'])
      return await ctx.send(errorMsg)
    await ctx.send("Friend request has been sent ✅")

class MUST_READ(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
  @discord.ui.button(row=0, label='Must Read', style=discord.ButtonStyle.red, custom_id="must_read_yes", disabled=False)
  async def button_callback1(self, button, interaction):        

    embs = []
    emb1 = discord.Embed(title="⚠ MUST READ ⚠", description="There is a **rare bug** within the Adopt Me game that you probably need to know about if you decide to use this system.\n\n**・Short Explanation**:\n> The latest trade gets reverted after the bot has successfully received the items.\n\n**・Detailed Explanation**:\n> The bug occurs right after the bot receives items from someone due to the game failing to save the data of the client. When it occurs, the latest trade will be reverted and both clients will get kicked from the VIP server (the bot and the person who was trading with it).\n> This bug happened 2 times so far, we have had already added a warning that will be sent to all current active tickets since few weeks ago. We assumed it wouldn't be something to be bothered by, until it happened a 2nd time on the 24th of Sep 2022.\n\n**・What we know so far..**\n> - It happens right after the trade has been confirmed in-game and was successful.\n> - It only reverts the trade it was processing which is the latest trade.\n\n**・You do not have to worry..**\n> - It's recommended for you to wait 1-2 minutes before continuing the deal with your trader once the bot receives the pets, because until then the bot would have warned you about the bug. After you have waited 1-2 minutes, you can double check if the bot still has the items by using the commands `$inv` or `$th`.\n> - You are safe if you have given the items to the bot for longer than 2 minutes even if the bug occurs after that, because the trade would have already been saved and the bug could have been triggered by another user in another ticket.\n\n**・Some additional points..**\n> - This cannot be fixed on our end, this is either an Adopt Me or Roblox bug within their database systems.\n> - This is extremely rare to happen. It happened only 2 times since we have launched the service (8th of Aug, 2022). It's so rare that you cannot even find anything related to it on Google. According to the amount of the successful trades the bot has done, the chances would be then around 2 in a 1000+ for this bug to happen.", color=0xff0000)

    emb2 = discord.Embed(title="Example of The Warning", description="You will be pinged along with this warning in your ticket whenever the bug occurs.", color=0xff0000)
    emb2.set_image(url="https://cdn.discordapp.com/attachments/851189858600353826/1023336909424050256/unknown.png")

    emb3 = discord.Embed(color=0xff0000)
    emb3.set_image(url="https://cdn.discordapp.com/attachments/851189858600353826/1023334990152470669/unknown.png")

    embs.append(emb1)
    embs.append(emb2)
    embs.append(emb3)

    try:
      await interaction.response.send_message(embeds=embs, ephemeral=True)
    except NotFound:
      return

@bot.command()
async def mustread(ctx, msgid):
  if ctx.author.id in TicketAccess:
    msg = await ctx.channel.fetch_message(int(msgid))
    await msg.edit(view=MUST_READ())

def SearchBar(content=None, channel_id=None, author_id=None, mentions=None, min_id=None):
  params = {'content': content, 'channel_id': channel_id, 'author_id': author_id, 'mentions': mentions, 'min_id': min_id}
  res = sessionDiscord.get(f'https://discord.com/api/v9/guilds/{GUILD_ID}/messages/search', params=params)
  data = res.json()
  return data

@bot.command()
async def blacklisted(ctx, msgid):
  if ctx.author.id in TicketAccess:
    global sessionDiscord

    c = bot.get_channel(1136411635733495969)
    aftermsg = await c.fetch_message(int(msgid))
    jumpurl = aftermsg.jump_url
    msgs = await c.history(limit=None, oldest_first=True, after=aftermsg.created_at).flatten()
    role = ctx.guild.get_role(BLACKLIST_ROLE_ID)
    users = ""
    cur_users = []
    for msg in msgs:
      user = ctx.guild.get_member(msg.author.id)
      if user != None:
        if role in user.roles:
          if user.id not in cur_users:
            cur_users.append(user.id)
            result = SearchBar(content=user.id, channel_id=923545414416871444, author_id=[823690963783778334, 885531994111492160])
            if result['total_results'] == 0:
              continue
            msgs1 = result['messages']
            for msg1 in msgs1[0]:
              
              msgid = msg1['id']
              content = msg1['content']
              channel_id = msg1['channel_id']
              author_id = msg1['author']['id']
              sent_timestamp = int(arrow.get(msg1['timestamp']).timestamp())

              try:
                edited_timestamp = arrow.get(msg1['edited_timestamp']).timestamp()
              except TypeError:
                edited_timestamp = None

              e_content = msg1['embeds'][0]['description']

              user_id = find_between(e_content, " | <@", ">\nReason")
              reason = find_between(e_content, "Reason: `", "`")

              users += f"> User: <@{user_id}>\n> Reason: `{reason}`\n> Time: <t:{sent_timestamp}:R>\n> Has been blacklisted **`{result['total_results']}`** times.\n\n"
    embed = discord.Embed(title="Blacklisted Users Who Have Vouched", description=f"{users}{jumpurl}", color=MAINCOLOR)
    await ctx.send(embed=embed)

@bot.command()
async def oktest(ctx, msgid):
  if ctx.author.id == 358594990982561792:
    msg = await ctx.channel.fetch_message(int(msgid))
    await msg.edit(view=PasteGamepass())

@bot.command()
async def eval(ctx: commands.Context, *, code: str):
  if ctx.author.id == 358594990982561792:
    if code.splitlines()[0] == "```python":
      code = code[9:-3]
    elif code.splitlines()[0] == "```":
      code = code[3:-3]
    elif code.splitlines()[0] == "```py":
      code = code[5:-3]
    else:
      code = code
    local_variables = {
      "discord": discord,
      "bot": ctx.bot,
      "ctx": ctx,
      "message": ctx.message,
      "author": ctx.message.author,
      "guild": ctx.message.guild,
      "channel": ctx.message.channel
    }
    try:
      await aexec(code, local_variables)
      await ctx.message.add_reaction("✅")
    except:
      await ctx.message.add_reaction("❌")
      ee = discord.Embed(title="Error", description=f"**Traceback:**\n```\n{traceback.format_exc()}\n```", color=redcolor)
      dmchannel = await ctx.author.create_dm()
      await dmchannel.send(embed=ee)


@bot.command()
@commands.cooldown(1, 15, commands.BucketType.channel)
async def list(ctx):
  if (ctx.message.channel.category.id == AUTOAMP_CATEGORY_ID) or (ctx.author.id in TicketAccess):
    plrsList = await readPlayerList()
    plrText = ""
    for plr in plrsList:
      plrText += f"・**`{plr['username']}`** - [Profile](https://www.roblox.com/users/{plr['user_id']}/profile)\n"
    embed = discord.Embed(title="Users In VIP Server", description=plrText, color=0x6704E8)
    await ctx.reply(embed=embed)

@bot.command()
async def earnings(ctx):
  if (ctx.author.id in TicketAccess):
    rbxSession = getrbxSession()
    params = {
        'timeFrame': 'Day',
        'transactionType': 'summary',
    }
    res = rbxSession.get('https://economy.roblox.com/v2/users/4010518799/transaction-totals', params=params)
    pendRbx = res.json()['pendingRobuxTotal']
    pastDay = res.json()['incomingRobuxTotal']

    res1 = rbxSession.get(f'https://economy.roblox.com/v1/users/{GAMEPASS_ACCID}/currency')
    curRbx = res1.json()['robux']

    embed = discord.Embed(title="Robux Earnings", description=f">>> Income Past Day: `+{pastDay}` <:Robux:914568435583836171>\nBalance: `{curRbx}` <:Robux:914568435583836171>\nPending: `{pendRbx}` <:Robux:914568435583836171>\nTotal: __**`{pendRbx+curRbx}`**__ <:Robux:914568435583836171>", color=MAINCOLOR)
    await ctx.reply(embed=embed)

@bot.command()
async def extendsubs(ctx, timestamp=None):
  if (ctx.author.id == 358594990982561792):
    if timestamp == None:
      return
    con,cur = openCON()
    cur.execute(f"SELECT * FROM sub_tickets WHERE (status='Active')")
    resSQL = cur.fetchall()
    for i in resSQL:
      newVal = i['extended']+int(timestamp)
      cur.execute(f"UPDATE sub_tickets SET extended='{newVal}' WHERE uni_id='{i['uni_id']}'")
    con.commit()
    closeCON(cur,con)
    
    updates_channel = bot.get_channel(1138538437067157657)
    elaps = timedelta(seconds=int(timestamp))
    emb = discord.Embed(title="> __Subscribers Notification__", description=f"・**Your subscription has been extended by +{elaps} due to service maintenance.**", color=0x6704e8)
    emb.set_footer(text="You can view your subscription info by using the command $sub")
    await updates_channel.send(content=f"<@&{SUBSCRIBER_ROLE}>", embed=emb)

    #subsData = await readSubs()
    #for i in subsData:
    #  i['extended'] = i['extended']+int(timestamp)
    #editSubs(subsData)
    #elaps = timedelta(seconds=int(timestamp))
    #emb = discord.Embed(title="> __Subscribers Notification__", description=f"・**Your subscription has been extended by +{elaps} due to service maintenance.**", color=0x6704e8)
    #emb.set_footer(text="You can view your subscription info by using the command $sub")
    #subrole = ctx.guild.get_role(SUBSCRIBER_ROLE)
    #if dmMember == "yes":
    #  for user in subrole.members:
    #    try:
    #      dmchannel = await user.create_dm()
    #      await dmchannel.send(embed=emb)
    #    except Exception:
    #      pass
    #await ctx.reply(f"Subs extended by +{elaps}")

bot.run(TOKEN, reconnect=True)
