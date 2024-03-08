import asyncio, ast, websockets, requests
import mysql.connector

def openCON(database=None):
  con = mysql.connector.connect(user='root', password='pass', host='localhost', database=database)
  cur = con.cursor(dictionary=True)
  return con, cur

def closeCON(cur,con):
  cur.close()
  con.close()

PORT = 8070
print("Server listening on Port " + str(PORT))

connected = set()

session = requests.Session()
session.verify = False

async def echo(websocket, path):
  print("A client just connected")
  connected.add(websocket)
  try:
    async for message in websocket:
      print("Received message from client: " + message)
      for conn in connected:
        if conn != websocket:
          await conn.send(message)

      #closeRoblox = True
      #try:
      #  jsdata = ast.literal_eval(message)
      #  test = jsdata['close_roblox']
      #except Exception:
      #  closeRoblox = False
      #if closeRoblox == True:
      #  roblox_opened_ts = int(jsdata['close_roblox'])
      #  handles = get_roblox_handles()
      #  if len(handles) != 0:
      #    for handle in handles:
      #      original_opened = int(handle.create_time())
      #      diff = roblox_opened_ts-original_opened
      #      if diff <= 6:
      #        handle.terminate()
      #        print("closed handle")
      #        break

      readData = True
      try:
        jsdata = ast.literal_eval(message)
        test = jsdata['action']
      except Exception:
        readData = False
      if readData:
        if jsdata['action'] == "sendHTTPreq":
          datan = None
          jsone = None
          if jsdata['Method'] == "POST":
            method = session.post
          elif jsdata['Method'] == "GET":
            method = session.get
          elif jsdata['Method'] == "PATCH":
            method = session.patch
          
          if "WebKitFormBoundaryATrHMos3WI5ylq5F" in str(jsdata['Headers']):
            datan = jsdata['Body']
          else:
            jsone = ast.literal_eval(jsdata['Body'])
          
          method(url=jsdata['Url'], headers=jsdata['Headers'], json=jsone, data=datan)
          
            
        elif jsdata['action'] == "getDataByUsername":
          con,cur = openCON(database=jsdata['database'])
          cur.execute(f"SELECT * FROM channels WHERE ((ticket_status='Active') OR (ticket_status='Pending' AND pets_received='Yes')) AND (receiver_username='{jsdata['target']}' OR seller_username='{jsdata['target']}')")
          resSQL = cur.fetchall()
          if len(resSQL) == 0:
            dataReturned = "None"
          else:
            if jsdata['database'] == "am_data":
              resSQL[0]['trade_id'] = ast.literal_eval(resSQL[0]['trade_id'])
              resSQL[0]['redeem_trade_id'] = ast.literal_eval(resSQL[0]['redeem_trade_id'])
            dataReturned = resSQL[0]
          jsdata['returned'] = dataReturned
          jsdata = str(jsdata).replace("'", '"')
          await websocket.send(str(jsdata))
          closeCON(cur,con)
        elif jsdata['action'] == "getDataByChannelID":
          con,cur = openCON(database=jsdata['database'])
          cur.execute(f"SELECT * FROM channels WHERE channel_id='{jsdata['target']}'")
          resSQL = cur.fetchall()
          if len(resSQL) == 0:
            dataReturned = "None"
          else:
            if jsdata['database'] == "am_data":
              resSQL[0]['trade_id'] = ast.literal_eval(resSQL[0]['trade_id'])
              resSQL[0]['redeem_trade_id'] = ast.literal_eval(resSQL[0]['redeem_trade_id'])
            dataReturned = resSQL[0]
          jsdata['returned'] = dataReturned
          jsdata = str(jsdata).replace("'", '"')
          await websocket.send(str(jsdata))
          closeCON(cur,con)
  except websockets.exceptions.ConnectionClosed as e:
    print("A client just disconnected")
  finally:
    connected.remove(websocket)

start_server = websockets.serve(echo, "156.227.0.178", PORT)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
