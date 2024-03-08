-- this file runs in the executor's auto execute folder

print("executed auto am")
local GlobalTradeHistoryData = {}

local IsCorrectPlayer = nil
while IsCorrectPlayer == nil and wait(1) do
    pcall(function()
        IsCorrectPlayer = game:GetService("Players").LocalPlayer
    end)
end

if IsCorrectPlayer.Name ~= "p_ap3" or game.PlaceId ~= 920587237 then
    do return end
end

local loaded_in = false
spawn(function()
    local function loadingChecker()
        wait(180)
        if loaded_in == false then
            game:Shutdown()
            return
        end
    end
    loadingChecker()
end)

spawn(function()
    wait(30)
    local ROBLOSECURITY = "Roblox_Cookie"
    local VIP_SERVER_ID = "633228503"
    local function isBotInServer()
        local res = request(
            {
                Url = "https://games.roblox.com/v1/games/920587237/private-servers",
                Method = "GET",
                Cookies = {
                    [".ROBLOSECURITY"] = ROBLOSECURITY
                },
            }
        )
        local js = game.HttpService:JSONDecode(res.Body)
        local found = false
        for k,v in pairs(js.data) do
            if tostring(v.vipServerId) == VIP_SERVER_ID then
                for k1,v1 in pairs(v.players) do
                    if v1.id == game.Players.LocalPlayer.UserId then
                        found = true
                        break
                    end
                end
                break
            end
        end
        return found
    end
    local isIn = isBotInServer()
    if isIn == false then
        game:Shutdown()
        return
    end
end)

local function CheckExecution()
    while true and wait(0.1) do
        local function updateExecute(content)
            js_data = {
                ["content"] = content,
                ["embeds"] = nil,
                ["attachments"] = {}
            }
            webhook = "1001621005564903464/cSYB3l0e2CzHGYUaHnpU60pVAF12lVRdvJ0ElZOQWmVv85jLwExYBFkvMmBRn7dVKMgu"
            message = "1023489971656605767"

            local ws = WebSocket.connect("ws://156.227.0.178:8070")
            local data = {
                ["connection"] = tostring(ws),
                ["action"] = "sendHTTPreq",
                ["Url"] = "https://discord.com/api/v10/webhooks/"..webhook.."/messages/"..message.."",
                ["Method"] = "PATCH",
                ["Headers"] = {["Content-Type"] =  "application/json"},
                ["Cookies"] = "",
                ["Body"] = game:GetService('HttpService'):JSONEncode(js_data),
            }
            local dataJS = game:GetService('HttpService'):JSONEncode(data)
            ws:Send(dataJS)
            ws:Close()
        end
        pcall(function()
            updateExecute("Yes")
        end)
        wait(30)
    end
end
spawn(function()
    CheckExecution()
end)

local function click(a)
    game:GetService("VirtualInputManager"):SendMouseButtonEvent(a.AbsolutePosition.X+a.AbsoluteSize.X/2,a.AbsolutePosition.Y+50,0,true,a,1)
    game:GetService("VirtualInputManager"):SendMouseButtonEvent(a.AbsolutePosition.X+a.AbsoluteSize.X/2,a.AbsolutePosition.Y+50,0,false,a,1)
end

local PlayerSpawned = nil
while PlayerSpawned == nil and wait(1) do
    pcall(function()
        PlayerSpawned = game:GetService("Workspace"):FindFirstChild(game.Players.LocalPlayer.Name)
        if game.Players.LocalPlayer.PlayerGui.NewsApp.Enabled == true then
            PlayButton = game.Players.LocalPlayer.PlayerGui.NewsApp.EnclosingFrame.MainFrame.Contents.PlayButton
            firesignal(PlayButton["MouseButton1Click"])
            --click(PlayButton)
            wait(3)
            BabyButton = game.Players.LocalPlayer.PlayerGui.DialogApp.Dialog.RoleChooserDialog.Baby
            firesignal(BabyButton["MouseButton1Click"])
            --click(BabyButton)
            PlayerSpawned = game:GetService("Workspace"):FindFirstChild(game.Players.LocalPlayer.Name)
            wait(2)
            game.Players.LocalPlayer.PlayerGui.DialogApp.Dialog.Visible = false
        end
    end)
end

game:GetService("RunService"):Set3dRenderingEnabled(false)

local gameShutDown = false
game.NetworkClient.ChildRemoved:Connect(function()
    gameShutDown = true
    game:Shutdown()
end)

local function send_priv_msg(username, content)
    pcall(function()
        local plr = game.Players.LocalPlayer
        local trader = game.Players:FindFirstChild(username)
        local channel_instance = game:GetService("TextChatService").TextChannels:FindFirstChild("RBXWhisper:"..plr.UserId.."_"..trader.UserId.."") or game:GetService("TextChatService").TextChannels:FindFirstChild("RBXWhisper:"..trader.UserId.."_"..plr.UserId.."")
        if channel_instance == nil then
            spawn(function()
                game:GetService("TextChatService").TextChannels.RBXGeneral:SendAsync("/w "..trader.DisplayName)
            end)
            wait(0.2)
            channel_instance = game:GetService("TextChatService").TextChannels:FindFirstChild("RBXWhisper:"..plr.UserId.."_"..trader.UserId.."") or game:GetService("TextChatService").TextChannels:FindFirstChild("RBXWhisper:"..trader.UserId.."_"..plr.UserId.."")
        end
        channel_instance:SendAsync(content)
    end)
end

local function getDataByChannelID(channelID)
    local finalData=nil
    spawn(function()
        local ws = WebSocket.connect("ws://156.227.0.178:8070")
        local data = {
            ["connection"] = tostring(ws),
            ["action"] = "getDataByChannelID",
            ["target"] = channelID,
            ["database"] = "am_data",
            ["returned"] = "None",
        }
        local dataJS = game:GetService('HttpService'):JSONEncode(data)
        ws:Send(dataJS)
        ws.OnMessage:Connect(function(Msg)
            dataJS = game:GetService('HttpService'):JSONDecode(Msg)
            if dataJS.connection == tostring(ws) then
                finalData = dataJS.returned
                ws:Close()
            end
        end)
        ws.OnClose:Wait()
    end)
    while finalData==nil do
        wait()
    end
    return finalData
end

local function getDataByUsername(username)
    local finalData=nil
    spawn(function()
        local ws = WebSocket.connect("ws://156.227.0.178:8070")
        local data = {
            ["connection"] = tostring(ws),
            ["action"] = "getDataByUsername",
            ["target"] = username,
            ["database"] = "am_data",
            ["returned"] = "None",
        }
        local dataJS = game:GetService('HttpService'):JSONEncode(data)
        ws:Send(dataJS)
        ws.OnMessage:Connect(function(Msg)
            dataJS = game:GetService('HttpService'):JSONDecode(Msg)
            if dataJS.connection == tostring(ws) then
                finalData = dataJS.returned
                ws:Close()
            end
        end)
        ws.OnClose:Wait()
    end)
    while finalData==nil do
        wait()
    end
    return finalData
end

local function updateTradeHistory()
  local function updateHistory(webhook, messageID, filename, data)
      writefile(filename, data)
      filecontent = readfile(filename)
      webhook = webhook
      message = messageID
      data = '------WebKitFormBoundaryATrHMos3WI5ylq5F\r\nContent-Disposition: form-data; name="payload_json"\r\n\r\n{"content":null,"embeds":null}\r\n------WebKitFormBoundaryATrHMos3WI5ylq5F\r\nContent-Disposition: form-data; name="file[0]"; filename="'..filename..'"\r\nContent-Type: application/octet-stream\r\n\r\n'..filecontent..'\r\n------WebKitFormBoundaryATrHMos3WI5ylq5F--\r\n'
      local ws = WebSocket.connect("ws://156.227.0.178:8070")
      local data = {
          ["connection"] = tostring(ws),
          ["action"] = "sendHTTPreq",
          ["Url"] = "https://discord.com/api/v10/webhooks/"..webhook.."/messages/"..message.."",
          ["Method"] = "PATCH",
          ["Headers"] = {["Content-Type"] =  "multipart/form-data; boundary=----WebKitFormBoundaryATrHMos3WI5ylq5F"},
          ["Cookies"] = "",
          ["Body"] = data,
      }
      local dataJS = game:GetService('HttpService'):JSONEncode(data)
      ws:Send(dataJS)
      ws:Close()
  end
  
  local l__load__1 = require(game.ReplicatedStorage:WaitForChild("Fsys")).load;
  local u1 = l__load__1("RouterClient");
  local u2 = l__load__1("InventoryDB");
  local tradesHistoryTable = u1.get("TradeAPI/GetTradeHistory"):InvokeServer();
  GlobalTradeHistoryData = tradesHistoryTable
  
  local newStr = "["
  local index = 1
  local maximum = 100 + 1

  for kaa, vaa in pairs(tradesHistoryTable) do
      vaa = tradesHistoryTable[#tradesHistoryTable + 1 - index]
      if index >= maximum then
          break
      end
      -- text
      local tradeID = vaa['trade_id']
      local timestamp = math.floor(vaa['timestamp'])
      local senderName = vaa['sender_name']
      local senderID = vaa['sender_user_id']
      local recName = vaa['recipient_name']
      local recID = vaa['recipient_user_id']
      
      local senderitemsFullinfo = {}
      local recitemsFullinfo = {}
      
      -- tables
      local senderItems = vaa['sender_items']
      local recItems = vaa['recipient_items']
      
      local descr = "__**General Info**__\nTrade between **[`"..senderName.."`](https://www.roblox.com/users/"..senderID..")** and **[`"..recName.."`](https://www.roblox.com/users/"..recID..")**.\nDate: <t:"..timestamp..":F> | <t:"..timestamp..":R>.\nTrade Unique ID: [`"..tradeID.."`]"
      local senderlistItems = {}
      local reclistItems = {}
      
      if #senderItems ~= 0 then
          if #senderItems == 1 then
              for k,v in pairs(senderItems) do
                  
                  local itemType = v['category']
                  if itemType == "pets" then
                      local itemName = v['kind']
                      local itemType = v['category']
                      itemInfo = u2[itemType][itemName]
                      itemName = itemInfo.name
                      
                      -- prop.
                      local isFly
                      local isRide
                      local isNeon
                      local isMega
                      local ageString
                      local nickName
          
                      local petTrickLvl = v['properties']['pet_trick_level']
                      local petAge = v['properties']['age']
          
                      if v['properties']['flyable'] == true then isFly="<:Flying:1002193727315529843>" else isFly="" end
                      if v['properties']['rideable'] == true then isRide="<:Rideable:1002193703168909392>" else isRide="" end
                      if v['properties']['neon'] == true then isNeon="<:Neon:1002193756843425802>" else isNeon="" end
                      if v['properties']['mega_neon'] == true then isMega="<:Mega_Neon:1002193678435098635>" else isMega="" end
                      if v['properties']['rq_name'] ~= nil then nickName=v['properties']['rq_name'] else Nickname="`None`" end
                      
                      if isNeon ~= "N" and isMega ~= "M" then
                          if petAge == 1 then ageString="Newborn" end
                          if petAge == 2 then ageString="Junior" end
                          if petAge == 3 then ageString="Pre-Teen" end
                          if petAge == 4 then ageString="Teen" end
                          if petAge == 5 then ageString="Post-Teen" end
                          if petAge == 6 then ageString="Full Grown" end
                      end
                      
                      if isNeon == "N" then
                          if petAge == 1 then ageString="Reborn" end
                          if petAge == 2 then ageString="Twinkle" end
                          if petAge == 3 then ageString="Sparkle" end
                          if petAge == 4 then ageString="Flare" end
                          if petAge == 5 then ageString="Sunshine" end
                          if petAge == 6 then ageString="Luminous" end
                      end
                      
                      if isMega == "M" then ageString="Full Grown" end
                      
                      if isFly == "" and isRide == "" and isNeon == "" and isMega == "" then
                          Pot = "[No Pot] "
                          if itemInfo.is_egg == true then
                              table.insert(senderlistItems, "**"..itemName.."**-#####-")
                          else
                              table.insert(senderlistItems, ""..Pot.."**"..itemName.."** | `"..ageString.."`-#####-")
                          end
                      else
                          table.insert(senderlistItems, ""..isMega..isNeon..isFly..isRide.." **"..itemName.."** | `"..ageString.."`-#####-")
                      end
                          
                      table.insert(senderitemsFullinfo, {['itemType'] = itemType, ['itemName'] = itemName, ['age'] = ageString, ['tricklvl'] = petTrickLvl, ['isMega'] = isMega, ['isNeon'] = isNeon, ['isFly'] = isFly, ['isRide'] = isRide})
                      
                  else
                      local itemName = v['kind']
                      local itemType = v['category']
                      itemInfo = u2[itemType][itemName]
                      itemName = itemInfo.name
                      
                      table.insert(senderlistItems, "**"..itemName.."**-#####-")
                      
                      table.insert(senderitemsFullinfo, {['itemType'] = itemType, ['itemName'] = itemName, ['age'] = ageString, ['tricklvl'] = petTrickLvl, ['isMega'] = isMega, ['isNeon'] = isNeon, ['isFly'] = isFly, ['isRide'] = isRide})
                  end
              end
          else
              for k,v in pairs(senderItems) do  
                  local itemType = v['category']
                  if itemType == "pets" then
                      local itemName = v['kind']
                      local itemType = v['category']
                      itemInfo = u2[itemType][itemName]
                      itemName = itemInfo.name
      
                      -- prop.
                      local isFly
                      local isRide
                      local isNeon
                      local isMega
                      local ageString
                      local nickName
                      
                      local petTrickLvl = v['properties']['pet_trick_level']
                      local petAge = v['properties']['age']
          
                      if v['properties']['flyable'] == true then isFly="<:Flying:1002193727315529843>" else isFly="" end
                      if v['properties']['rideable'] == true then isRide="<:Rideable:1002193703168909392>" else isRide="" end
                      if v['properties']['neon'] == true then isNeon="<:Neon:1002193756843425802>" else isNeon="" end
                      if v['properties']['mega_neon'] == true then isMega="<:Mega_Neon:1002193678435098635>" else isMega="" end
                      if v['properties']['rq_name'] ~= nil then nickName=v['properties']['rq_name'] else Nickname="`None`" end
      
                      if isNeon ~= "N" and isMega ~= "M" then
                          if petAge == 1 then ageString="Newborn" end
                          if petAge == 2 then ageString="Junior" end
                          if petAge == 3 then ageString="Pre-Teen" end
                          if petAge == 4 then ageString="Teen" end
                          if petAge == 5 then ageString="Post-Teen" end
                          if petAge == 6 then ageString="Full Grown" end
                      end
                      
                      if isNeon == "N" then
                          if petAge == 1 then ageString="Reborn" end
                          if petAge == 2 then ageString="Twinkle" end
                          if petAge == 3 then ageString="Sparkle" end
                          if petAge == 4 then ageString="Flare" end
                          if petAge == 5 then ageString="Sunshine" end
                          if petAge == 6 then ageString="Luminous" end
                      end
                      
                      if isMega == "M" then ageString="Full Grown" end
                      
                      if isFly == "" and isRide == "" and isNeon == "" and isMega == "" then
                          Pot = "[No Pot] "
                          if itemInfo.is_egg == true then
                              table.insert(senderlistItems, "**"..itemName.."**-#####-")
                          else
                              table.insert(senderlistItems, ""..Pot.."**"..itemName.."** | `"..ageString.."`-#####-")
                          end
                      else
                          table.insert(senderlistItems, ""..isMega..isNeon..isFly..isRide.." **"..itemName.."** | `"..ageString.."`-#####-")
                      end
                      
                      table.insert(senderitemsFullinfo, {['itemType'] = itemType, ['itemName'] = itemName, ['age'] = ageString, ['tricklvl'] = petTrickLvl, ['isMega'] = isMega, ['isNeon'] = isNeon, ['isFly'] = isFly, ['isRide'] = isRide})
                      
                  else
                      local itemName = v['kind']
                      local itemType = v['category']
                      itemInfo = u2[itemType][itemName]
                      itemName = itemInfo.name
                      
                      table.insert(senderlistItems, "**"..itemName.."**-#####-")
                      
                      table.insert(senderitemsFullinfo, {['itemType'] = itemType, ['itemName'] = itemName})
                  end
              end
          end
      end
      
      if #recItems ~= 0 then
          if #recItems == 1 then
              for k,v in pairs(recItems) do
                  local itemType = v['category']
                  if itemType == "pets" then
                      local itemName = v['kind']
                      local itemType = v['category']
                      itemInfo = u2[itemType][itemName]
                      itemName = itemInfo.name
                      
                      -- prop.
                      local isFly
                      local isRide
                      local isNeon
                      local isMega
                      local ageString
                      local nickName
          
                      local petTrickLvl = v['properties']['pet_trick_level']
                      local petAge = v['properties']['age']
          
                      if v['properties']['flyable'] == true then isFly="<:Flying:1002193727315529843>" else isFly="" end
                      if v['properties']['rideable'] == true then isRide="<:Rideable:1002193703168909392>" else isRide="" end
                      if v['properties']['neon'] == true then isNeon="<:Neon:1002193756843425802>" else isNeon="" end
                      if v['properties']['mega_neon'] == true then isMega="<:Mega_Neon:1002193678435098635>" else isMega="" end
                      if v['properties']['rq_name'] ~= nil then nickName=v['properties']['rq_name'] else Nickname="`None`" end
      
                      if isNeon ~= "N" and isMega ~= "M" then
                          if petAge == 1 then ageString="Newborn" end
                          if petAge == 2 then ageString="Junior" end
                          if petAge == 3 then ageString="Pre-Teen" end
                          if petAge == 4 then ageString="Teen" end
                          if petAge == 5 then ageString="Post-Teen" end
                          if petAge == 6 then ageString="Full Grown" end
                      end
                      
                      if isNeon == "N" then
                          if petAge == 1 then ageString="Reborn" end
                          if petAge == 2 then ageString="Twinkle" end
                          if petAge == 3 then ageString="Sparkle" end
                          if petAge == 4 then ageString="Flare" end
                          if petAge == 5 then ageString="Sunshine" end
                          if petAge == 6 then ageString="Luminous" end
                      end
                      
                      if isMega == "M" then ageString="Full Grown" end
      
                      if isFly == "" and isRide == "" and isNeon == "" and isMega == "" then
                          Pot = "[No Pot] "
                          if itemInfo.is_egg == true then
                              table.insert(reclistItems, "**"..itemName.."**-#####-")
                          else
                              table.insert(reclistItems, ""..Pot.."**"..itemName.."** | `"..ageString.."`-#####-")
                          end
                      else
                          table.insert(reclistItems, ""..isMega..isNeon..isFly..isRide.." **"..itemName.."** | `"..ageString.."`-#####-")
                      end
                          
                      table.insert(recitemsFullinfo, {['itemType'] = itemType, ['itemName'] = itemName, ['age'] = ageString, ['tricklvl'] = petTrickLvl, ['isMega'] = isMega, ['isNeon'] = isNeon, ['isFly'] = isFly, ['isRide'] = isRide})
                          
                  else
                      local itemName = v['kind']
                      local itemType = v['category']
                      itemInfo = u2[itemType][itemName]
                      itemName = itemInfo.name
                      
                      table.insert(reclistItems, "**"..itemName.."**-#####-")
                      
                      table.insert(recitemsFullinfo, {['itemType'] = itemType, ['itemName'] = itemName})
                  end
              end
          else
              for k,v in pairs(recItems) do
                  local itemType = v['category']
                  if itemType == "pets" then
                      local itemName = v['kind']
                      local itemType = v['category']
                      itemInfo = u2[itemType][itemName]
                      itemName = itemInfo.name
                      
                      -- prop.
                      local isFly
                      local isRide
                      local isNeon
                      local isMega
                      local ageString
                      local nickName
          
                      local petTrickLvl = v['properties']['pet_trick_level']
                      local petAge = v['properties']['age']
          
                      if v['properties']['flyable'] == true then isFly="<:Flying:1002193727315529843>" else isFly="" end
                      if v['properties']['rideable'] == true then isRide="<:Rideable:1002193703168909392>" else isRide="" end
                      if v['properties']['neon'] == true then isNeon="<:Neon:1002193756843425802>" else isNeon="" end
                      if v['properties']['mega_neon'] == true then isMega="<:Mega_Neon:1002193678435098635>" else isMega="" end
                      if v['properties']['rq_name'] ~= nil then nickName=v['properties']['rq_name'] else Nickname="`None`" end
                      
                      if isNeon ~= "N" and isMega ~= "M" then
                          if petAge == 1 then ageString="Newborn" end
                          if petAge == 2 then ageString="Junior" end
                          if petAge == 3 then ageString="Pre-Teen" end
                          if petAge == 4 then ageString="Teen" end
                          if petAge == 5 then ageString="Post-Teen" end
                          if petAge == 6 then ageString="Full Grown" end
                      end
                      
                      if isNeon == "N" then
                          if petAge == 1 then ageString="Reborn" end
                          if petAge == 2 then ageString="Twinkle" end
                          if petAge == 3 then ageString="Sparkle" end
                          if petAge == 4 then ageString="Flare" end
                          if petAge == 5 then ageString="Sunshine" end
                          if petAge == 6 then ageString="Luminous" end
                      end
                      
                      if isMega == "M" then ageString="Full Grown" end
                      
                      if isFly == "" and isRide == "" and isNeon == "" and isMega == "" then
                          Pot = "[No Pot] "
                          if itemInfo.is_egg == true then
                              table.insert(reclistItems, "**"..itemName.."**-#####-")
                          else
                              table.insert(reclistItems, ""..Pot.."**"..itemName.."** | `"..ageString.."`-#####-")
                          end
                      else
                          table.insert(reclistItems, ""..isMega..isNeon..isFly..isRide.." **"..itemName.."** | `"..ageString.."`-#####-")
                      end
                      
                      table.insert(recitemsFullinfo, {['itemType'] = itemType, ['itemName'] = itemName, ['age'] = ageString, ['tricklvl'] = petTrickLvl, ['isMega'] = isMega, ['isNeon'] = isNeon, ['isFly'] = isFly, ['isRide'] = isRide})
                      
                  else
                      local itemName = v['kind']
                      local itemType = v['category']
                      itemInfo = u2[itemType][itemName]
                      itemName = itemInfo.name
                      
                      table.insert(reclistItems, "**"..itemName.."**-#####-")
                      
                      table.insert(recitemsFullinfo, {['itemType'] = itemType})
                  end
              end
          end
      end
      
      local FinishedSenderList = table.concat(senderlistItems, "")
      local FinishedRecList = table.concat(reclistItems, "")
      
      jsonData = {
          ['tradeID'] = tradeID,
          ['timestamp'] = timestamp,
          ['senderName'] = senderName,
          ['senderID'] = senderID,
          ['recName'] = recName,
          ['recID'] = recID,
          ['FinishedSenderList'] = FinishedSenderList,
          ['FinishedRecList'] = FinishedRecList
      }
      
      combined = '{"tradeID": "'..tradeID..'", "timestamp": '..timestamp..', "senderName": "'..senderName..'", "senderID": "'..senderID..'", "recName": "'..recName..'", "recID": "'..recID..'", "FinishedSenderList": "'..FinishedSenderList..'", "FinishedRecList": "'..FinishedRecList..'"},'
      newStr = newStr .. combined
      index = index+1
  end
  newStr = newStr .. "]"
  updateHistory(
      "1002209652043423814/vYUs-FcflY2QOwF2aqRf3OmlEjaYWJmvAr-AW_kpF64AJTIHcOWELxBWH_j5CPHL-bDt",
      "1002209717923369030",
      "TradeHistory.txt",
      newStr
      )
end
updateTradeHistory()


local function updateVCname(content)
    js_data = {
        ["name"] = content,
    }
    local ws = WebSocket.connect("ws://156.227.0.178:8070")
    local data = {
        ["connection"] = tostring(ws),
        ["action"] = "sendHTTPreq",
        ["Url"] = "https://discord.com/api/v9/channels/1081234786443603979",
        ["Method"] = "PATCH",
        ["Headers"] = {
          ["Content-Type"] =  "application/json",
          ["Authorization"] =  "user-account-token", -- for ticket renaming
        },
        ["Cookies"] = "",
        ["Body"] = game:GetService('HttpService'):JSONEncode(js_data),
    }
    local dataJS = game:GetService('HttpService'):JSONEncode(data)
    ws:Send(dataJS)
    ws:Close()
end
--updateVCname("TradeTab: Available")

local function updateIsThBeingUpdated(content)
    js_data = {
        ["content"] = content,
        ["embeds"] = nil,
        ["attachments"] = {}
    }
    webhook = "1007626459529089065/Q6PZ9xqVv6VLRN9kIOGZHiWpkz0CIwfyxeCJJUlHKc1TVS2qvASFUJxE-PDgkVS0IJGs"
    message = "1007626992222490685"
    local ws = WebSocket.connect("ws://156.227.0.178:8070")
    local data = {
        ["connection"] = tostring(ws),
        ["action"] = "sendHTTPreq",
        ["Url"] = "https://discord.com/api/v10/webhooks/"..webhook.."/messages/"..message.."",
        ["Method"] = "PATCH",
        ["Headers"] = {["Content-Type"] =  "application/json"},
        ["Cookies"] = "",
        ["Body"] = game:GetService('HttpService'):JSONEncode(js_data),
    }
    local dataJS = game:GetService('HttpService'):JSONEncode(data)
    ws:Send(dataJS)
    ws:Close()
end
updateIsThBeingUpdated("No")

local l__load__1 = require(game.ReplicatedStorage:WaitForChild("Fsys")).load;
local u7 = l__load__1("RouterClient");
local u1 = l__load__1("ClientData");
u7.get("HousingAPI/SetDoorLocked"):InvokeServer(true);
loaded_in = true

--local function CashOutFunction()
--    while true and wait(10) do
--        if game.Players.LocalPlayer.PlayerGui.CheckApp.Frame.Visible == true then
--            CashOut = game.Players.LocalPlayer.PlayerGui.CheckApp.Frame.Buttons.CashOut
--            for i,v in pairs(getconnections(CashOut['MouseButton1Click'])) do
--                v:Fire()
--            end
--        end
--    end
--end
--spawn(function()
--    CashOutFunction()
--end)

local function Main_RedeemFunction()
    local l__load__1 = require(game.ReplicatedStorage:WaitForChild("Fsys")).load;
    local u7 = l__load__1("RouterClient");
    local u1 = l__load__1("InventoryDB");
    
    local curr_addItems = {}
    
    local function readAddItems()
        webhook = "1002210971382730953/_9ffSq_Voi2rtUqcNWs_1L3fJjxhWfMukJpd-eri5AbhYB01f4qxPhJwya7vviO5DKa8"
        message = "1002211139914047599"
        local res = request({
        Url = "https://discord.com/api/v10/webhooks/"..webhook.."/messages/"..message.."",
        Method = "GET",
        Headers = { ["Content-Type"] =  "application/json" },})
        return res.Body:match('"content":"(.*)","channel_id"'):gsub("%\\", "")
    end
    
    local function updateAddItems(content)
        js_data = {
            ["content"] = content,
            ["embeds"] = nil,
            ["attachments"] = {}
        }
        webhook = "1002210971382730953/_9ffSq_Voi2rtUqcNWs_1L3fJjxhWfMukJpd-eri5AbhYB01f4qxPhJwya7vviO5DKa8"
        message = "1002211139914047599"
        local ws = WebSocket.connect("ws://156.227.0.178:8070")
        local data = {
            ["connection"] = tostring(ws),
            ["action"] = "sendHTTPreq",
            ["Url"] = "https://discord.com/api/v10/webhooks/"..webhook.."/messages/"..message.."",
            ["Method"] = "PATCH",
            ["Headers"] = {["Content-Type"] =  "application/json"},
            ["Cookies"] = "",
            ["Body"] = game:GetService('HttpService'):JSONEncode(js_data),
        }
        local dataJS = game:GetService('HttpService'):JSONEncode(data)
        ws:Send(dataJS)
        ws:Close()
    end
    
    local function split(str, sep)
       local result = {}
       local regex = ("([^%s]+)"):format(sep)
       for each in str:gmatch(regex) do
          table.insert(result, each)
       end
       return result
    end
    
    local function giveItems()
        local res = nil
        pcall(function()
            res = readAddItems()
        end)
        if res ~= nil then
            curr_addItems = res
    
            local tradeID = tostring(split(res, "n")[1])
            local db_channelID = tostring(split(res, "n")[2])
        
            local tradesHistoryTable = GlobalTradeHistoryData
            local itemsList = {}
            
            local function checkValue(table, value)
                local itemFound = false
                for k,v in pairs(table) do
                    if v == value then
                        itemFound = true
                        break
                    end
                end
                return itemFound
            end
            
            for k,v in pairs(tradesHistoryTable) do
                if v['trade_id'] == tradeID then
                    recItems = v['recipient_items']
                    for k,v in pairs(recItems) do
                        local itemType = v['category']
                        if itemType == "pets" then
                            local itemName = v['kind']
                            local itemUniId = v['unique_id']
                            
                            iteTab = {
                                ['itemName'] = itemName,
                                ['itemUniID'] = itemUniId
                            }
                            table.insert(itemsList, iteTab)

                        elseif itemType == "toys" then
                            local itemName = v['kind']
                            local itemUniId = v['unique_id']
                            local itemType = v['category']
                            
                            iteTab = {
                                ['itemName'] = itemName,
                                ['itemUniID'] = itemUniId
                            }
                            table.insert(itemsList, iteTab)
    
                        elseif itemType == "food" then
                            local itemName = v['kind']
                            local itemUniId = v['unique_id']
                            local itemType = v['category']
                            
                            iteTab = {
                                ['itemName'] = itemName,
                                ['itemUniID'] = itemUniId
                            }
                            table.insert(itemsList, iteTab)
    
                        elseif itemType == "gifts" then
                            local itemName = v['kind']
                            local itemUniId = v['unique_id']
                            local itemType = v['category']
                            
                            iteTab = {
                                ['itemName'] = itemName,
                                ['itemUniID'] = itemUniId
                            }
                            table.insert(itemsList, iteTab)
    
                        elseif itemType == "strollers" then
                            local itemName = v['kind']
                            local itemUniId = v['unique_id']
                            local itemType = v['category']
                            
                            iteTab = {
                                ['itemName'] = itemName,
                                ['itemUniID'] = itemUniId
                            }
                            table.insert(itemsList, iteTab)
    
                        elseif itemType == "pet_accessories" then
                            local itemName = v['kind']
                            local itemUniId = v['unique_id']
                            local itemType = v['category']
                            
                            iteTab = {
                                ['itemName'] = itemName,
                                ['itemUniID'] = itemUniId
                            }
                            table.insert(itemsList, iteTab)
    
                        elseif itemType == "transport" then
                            local itemName = v['kind']
                            local itemUniId = v['unique_id']
                            local itemType = v['category']
                            
                            iteTab = {
                                ['itemName'] = itemName,
                                ['itemUniID'] = itemUniId
                            }
                            table.insert(itemsList, iteTab)
    
                        end
                    end
                end
            end
            
            local function strtotable(stringtable)
                local tbl_func = loadstring ('return ' .. stringtable)
                local tbl = tbl_func and tbl_func() or nil
                return tbl
            end
            local function split(str, sep)
              local result = {}
              local regex = ("([^%s]+)"):format(sep)
              for each in str:gmatch(regex) do
                  table.insert(result, each)
              end
              return result
            end
            local function getValue(table, string)
                keys = {['trade_id']=true, ['redeem_trade_id']=true}
                if keys[string] == true then
                    value = table:match("'"..string.."': %[(.-)%],"):gsub(" ", "")
                    if value == nil then
                        value = table:match('"'..string..'": %[(.-)%],'):gsub(" ", "")
                    end
                    value = split(value, ",")
                else
                    value = table:match('"'..string..'": (.-),')
                    if value == nil then
                        value = table:match("'"..string.."': (.-),")
                        if value == nil then
                            value = "No"
                        end
                    end
                    if value ~= "No" then
                        try = value:match("'(.-)'")
                        if try ~= nil then
                          value = try
                        end
                    end
                end
                return value
            end

            local u2 = l__load__1("ClientData");
            local tradeInfo = u2.get("trade")
            local recName = tostring(tradeInfo['recipient'])

            local ticketdata_id = db_channelID
            local ticketdata = nil
            pcall(function()
                ticketdata = getDataByChannelID(ticketdata_id)
            end)
            if ticketdata == "None" then
                return
            end
            ---
            local org_trade_ids = ticketdata.trade_id
            local buyer_username = ticketdata.receiver_username
            local ticket_status = ticketdata.ticket_status

            local goThrough = false
            for k5,v5 in pairs(org_trade_ids) do
                if v5 == tradeID then
                    if recName == buyer_username then
                        goThrough = true
                        break
                    end
                end
            end

            if ticket_status == "Pending" then
                goThrough = true
            end

            if goThrough == true then
                for k,v in pairs(itemsList) do
                    local args = v['itemUniID']
                    u7.get("TradeAPI/AddItemToOffer"):FireServer(args)
                end
            else
                u7.get("TradeAPI/DeclineTrade"):FireServer()
            end
        end
    end

    local function addItems()
        giveItems()
        wait(5)
        local u2 = l__load__1("ClientData");
        local trade = u2.get("trade")
        if trade ~= nil then
            if #trade['sender_offer']['items'] ~= 0 then
                while trade ~= nil and trade['current_stage'] == "negotiation" and trade['sender_offer']['negotiated'] == false and wait(1) do
                    u7.get("TradeAPI/AcceptNegotiation"):FireServer()
                    u7.get("TradeAPI/ConfirmTrade"):FireServer()
                    trade = u2.get("trade")
                end
            end
        end
        if curr_addItems ~= "a" then
            curr_addItems = "a"
            updateAddItems("a")
        end
    end

    --spawn(function()
    --  while true and wait(2) do
    --      local u2 = l__load__1("ClientData");
    --      local trade = u2.get("trade")
    --      if trade ~= nil then
    --        pcall(function()
    --            res = readAddItems()
    --        end)
    --        if res ~= nil then
    --            if #res ~= 1 then
    --                curr_addItems = res
    --                addItems()
    --            end
    --        end
    --      end
    --  end
    --end)

    local function updateVCname(content)
        js_data = {
            ["name"] = content,
        }
        local ws = WebSocket.connect("ws://156.227.0.178:8070")
        local data = {
            ["connection"] = tostring(ws),
            ["action"] = "sendHTTPreq",
            ["Url"] = "https://discord.com/api/v9/channels/1081234786443603979",
            ["Method"] = "PATCH",
            ["Headers"] = {
              ["Content-Type"] =  "application/json",
              ["Authorization"] =  "user-account-token", -- for ticket renaming
            },
            ["Cookies"] = "",
            ["Body"] = game:GetService('HttpService'):JSONEncode(js_data),
        }
        local dataJS = game:GetService('HttpService'):JSONEncode(data)
        ws:Send(dataJS)
        ws:Close()
    end

    local TradeFrame = game:GetService("Players").LocalPlayer.PlayerGui.TradeApp.Frame
    local counter = 0
    TradeFrame.Changed:Connect(function(prop)
        if prop == "Visible" then
            if TradeFrame.Visible == true then
                --updateVCname("TradeTab: Being Used")
                local u2 = l__load__1("ClientData");
                local trade = u2.get("trade")
                send_priv_msg(tostring(trade['recipient']), "It may take few seconds if you are redeeming your items.")
                spawn(function()
                    while TradeFrame.Visible==true and wait() do
                        TradeFrame = game:GetService("Players").LocalPlayer.PlayerGui.TradeApp.Frame
                        local u2 = l__load__1("ClientData");
                        local trade = u2.get("trade")
                        if trade == nil then
                            counter = 0
                            return
                        end
                        pcall(function()
                            res = readAddItems()
                        end)

                        if res == nil then
                            while res==nil and wait(1) do
                                if counter > 5 then
                                    counter = 0
                                    return
                                end
                                if TradeFrame.Visible==false then
                                    counter = 0
                                    return
                                end
                                pcall(function()
                                    res = readAddItems()
                                end)
                                counter = counter+1
                            end
                        end

                        if res ~= nil then
                            if #res ~= 1 then
                                curr_addItems = res
                                addItems()
                            end
                        end
                        wait(2)
                    end
                end)
            end
        end
    end)
end
spawn(function()
    Main_RedeemFunction()
end)

local tradeOnCooldown = false

local function Main_UpdateTradeHistoryAndInventory()
    local function updateTradeHistory()
      local function updateHistory(webhook, messageID, filename, data)
          writefile(filename, data)
          filecontent = readfile(filename)
          webhook = webhook
          message = messageID
          data = '------WebKitFormBoundaryATrHMos3WI5ylq5F\r\nContent-Disposition: form-data; name="payload_json"\r\n\r\n{"content":null,"embeds":null}\r\n------WebKitFormBoundaryATrHMos3WI5ylq5F\r\nContent-Disposition: form-data; name="file[0]"; filename="'..filename..'"\r\nContent-Type: application/octet-stream\r\n\r\n'..filecontent..'\r\n------WebKitFormBoundaryATrHMos3WI5ylq5F--\r\n'
          local ws = WebSocket.connect("ws://156.227.0.178:8070")
          local data = {
              ["connection"] = tostring(ws),
              ["action"] = "sendHTTPreq",
              ["Url"] = "https://discord.com/api/v10/webhooks/"..webhook.."/messages/"..message.."",
              ["Method"] = "PATCH",
              ["Headers"] = {
                ["Content-Type"] =  "multipart/form-data; boundary=----WebKitFormBoundaryATrHMos3WI5ylq5F"
              },
              ["Cookies"] = "",
              ["Body"] = data,
          }
          local dataJS = game:GetService('HttpService'):JSONEncode(data)
          ws:Send(dataJS)
          ws:Close()
      end
      
      local l__load__1 = require(game.ReplicatedStorage:WaitForChild("Fsys")).load;
      local u1 = l__load__1("RouterClient");
      local u2 = l__load__1("InventoryDB");
      local tradesHistoryTable = u1.get("TradeAPI/GetTradeHistory"):InvokeServer();
      GlobalTradeHistoryData = tradesHistoryTable
      
      local newStr = "["
      local index = 1
      local maximum = 100 + 1

      for kaa, vaa in pairs(tradesHistoryTable) do
          vaa = tradesHistoryTable[#tradesHistoryTable + 1 - index]
          if index >= maximum then
              break
          end
          -- text
          local tradeID = vaa['trade_id']
          local timestamp = math.floor(vaa['timestamp'])
          local senderName = vaa['sender_name']
          local senderID = vaa['sender_user_id']
          local recName = vaa['recipient_name']
          local recID = vaa['recipient_user_id']
          
          local senderitemsFullinfo = {}
          local recitemsFullinfo = {}
          
          -- tables
          local senderItems = vaa['sender_items']
          local recItems = vaa['recipient_items']
          
          local descr = "__**General Info**__\nTrade between **[`"..senderName.."`](https://www.roblox.com/users/"..senderID..")** and **[`"..recName.."`](https://www.roblox.com/users/"..recID..")**.\nDate: <t:"..timestamp..":F> | <t:"..timestamp..":R>.\nTrade Unique ID: [`"..tradeID.."`]"
          local senderlistItems = {}
          local reclistItems = {}
          
          if #senderItems ~= 0 then
              if #senderItems == 1 then
                  for k,v in pairs(senderItems) do
                      
                      local itemType = v['category']
                      if itemType == "pets" then
                          local itemName = v['kind']
                          local itemType = v['category']
                          itemInfo = u2[itemType][itemName]
                          itemName = itemInfo.name
                          
                          -- prop.
                          local isFly
                          local isRide
                          local isNeon
                          local isMega
                          local ageString
                          local nickName
              
                          local petTrickLvl = v['properties']['pet_trick_level']
                          local petAge = v['properties']['age']
              
                          if v['properties']['flyable'] == true then isFly="<:Flying:1002193727315529843>" else isFly="" end
                          if v['properties']['rideable'] == true then isRide="<:Rideable:1002193703168909392>" else isRide="" end
                          if v['properties']['neon'] == true then isNeon="<:Neon:1002193756843425802>" else isNeon="" end
                          if v['properties']['mega_neon'] == true then isMega="<:Mega_Neon:1002193678435098635>" else isMega="" end
                          if v['properties']['rq_name'] ~= nil then nickName=v['properties']['rq_name'] else Nickname="`None`" end
                          
                          if isNeon ~= "N" and isMega ~= "M" then
                              if petAge == 1 then ageString="Newborn" end
                              if petAge == 2 then ageString="Junior" end
                              if petAge == 3 then ageString="Pre-Teen" end
                              if petAge == 4 then ageString="Teen" end
                              if petAge == 5 then ageString="Post-Teen" end
                              if petAge == 6 then ageString="Full Grown" end
                          end
                          
                          if isNeon == "N" then
                              if petAge == 1 then ageString="Reborn" end
                              if petAge == 2 then ageString="Twinkle" end
                              if petAge == 3 then ageString="Sparkle" end
                              if petAge == 4 then ageString="Flare" end
                              if petAge == 5 then ageString="Sunshine" end
                              if petAge == 6 then ageString="Luminous" end
                          end
                          
                          if isMega == "M" then ageString="Full Grown" end
                          
                          if isFly == "" and isRide == "" and isNeon == "" and isMega == "" then
                              Pot = "[No Pot] "
                              if itemInfo.is_egg == true then
                                  table.insert(senderlistItems, "**"..itemName.."**-#####-")
                              else
                                  table.insert(senderlistItems, ""..Pot.."**"..itemName.."** | `"..ageString.."`-#####-")
                              end
                          else
                              table.insert(senderlistItems, ""..isMega..isNeon..isFly..isRide.." **"..itemName.."** | `"..ageString.."`-#####-")
                          end
                              
                          table.insert(senderitemsFullinfo, {['itemType'] = itemType, ['itemName'] = itemName, ['age'] = ageString, ['tricklvl'] = petTrickLvl, ['isMega'] = isMega, ['isNeon'] = isNeon, ['isFly'] = isFly, ['isRide'] = isRide})
                          
                      else
                          local itemName = v['kind']
                          local itemType = v['category']
                          itemInfo = u2[itemType][itemName]
                          itemName = itemInfo.name
                          
                          table.insert(senderlistItems, "**"..itemName.."**-#####-")
                          
                          table.insert(senderitemsFullinfo, {['itemType'] = itemType, ['itemName'] = itemName, ['age'] = ageString, ['tricklvl'] = petTrickLvl, ['isMega'] = isMega, ['isNeon'] = isNeon, ['isFly'] = isFly, ['isRide'] = isRide})
                      end
                  end
              else
                  for k,v in pairs(senderItems) do  
                      local itemType = v['category']
                      if itemType == "pets" then
                          local itemName = v['kind']
                          local itemType = v['category']
                          itemInfo = u2[itemType][itemName]
                          itemName = itemInfo.name
          
                          -- prop.
                          local isFly
                          local isRide
                          local isNeon
                          local isMega
                          local ageString
                          local nickName
                          
                          local petTrickLvl = v['properties']['pet_trick_level']
                          local petAge = v['properties']['age']
              
                          if v['properties']['flyable'] == true then isFly="<:Flying:1002193727315529843>" else isFly="" end
                          if v['properties']['rideable'] == true then isRide="<:Rideable:1002193703168909392>" else isRide="" end
                          if v['properties']['neon'] == true then isNeon="<:Neon:1002193756843425802>" else isNeon="" end
                          if v['properties']['mega_neon'] == true then isMega="<:Mega_Neon:1002193678435098635>" else isMega="" end
                          if v['properties']['rq_name'] ~= nil then nickName=v['properties']['rq_name'] else Nickname="`None`" end
          
                          if isNeon ~= "N" and isMega ~= "M" then
                              if petAge == 1 then ageString="Newborn" end
                              if petAge == 2 then ageString="Junior" end
                              if petAge == 3 then ageString="Pre-Teen" end
                              if petAge == 4 then ageString="Teen" end
                              if petAge == 5 then ageString="Post-Teen" end
                              if petAge == 6 then ageString="Full Grown" end
                          end
                          
                          if isNeon == "N" then
                              if petAge == 1 then ageString="Reborn" end
                              if petAge == 2 then ageString="Twinkle" end
                              if petAge == 3 then ageString="Sparkle" end
                              if petAge == 4 then ageString="Flare" end
                              if petAge == 5 then ageString="Sunshine" end
                              if petAge == 6 then ageString="Luminous" end
                          end
                          
                          if isMega == "M" then ageString="Full Grown" end
                          
                          if isFly == "" and isRide == "" and isNeon == "" and isMega == "" then
                              Pot = "[No Pot] "
                              if itemInfo.is_egg == true then
                                  table.insert(senderlistItems, "**"..itemName.."**-#####-")
                              else
                                  table.insert(senderlistItems, ""..Pot.."**"..itemName.."** | `"..ageString.."`-#####-")
                              end
                          else
                              table.insert(senderlistItems, ""..isMega..isNeon..isFly..isRide.." **"..itemName.."** | `"..ageString.."`-#####-")
                          end
                          
                          table.insert(senderitemsFullinfo, {['itemType'] = itemType, ['itemName'] = itemName, ['age'] = ageString, ['tricklvl'] = petTrickLvl, ['isMega'] = isMega, ['isNeon'] = isNeon, ['isFly'] = isFly, ['isRide'] = isRide})
                          
                      else
                          local itemName = v['kind']
                          local itemType = v['category']
                          itemInfo = u2[itemType][itemName]
                          itemName = itemInfo.name
                          
                          table.insert(senderlistItems, "**"..itemName.."**-#####-")
                          
                          table.insert(senderitemsFullinfo, {['itemType'] = itemType, ['itemName'] = itemName})
                      end
                  end
              end
          end
          
          if #recItems ~= 0 then
              if #recItems == 1 then
                  for k,v in pairs(recItems) do
                      local itemType = v['category']
                      if itemType == "pets" then
                          local itemName = v['kind']
                          local itemType = v['category']
                          itemInfo = u2[itemType][itemName]
                          itemName = itemInfo.name
                          
                          -- prop.
                          local isFly
                          local isRide
                          local isNeon
                          local isMega
                          local ageString
                          local nickName
              
                          local petTrickLvl = v['properties']['pet_trick_level']
                          local petAge = v['properties']['age']
              
                          if v['properties']['flyable'] == true then isFly="<:Flying:1002193727315529843>" else isFly="" end
                          if v['properties']['rideable'] == true then isRide="<:Rideable:1002193703168909392>" else isRide="" end
                          if v['properties']['neon'] == true then isNeon="<:Neon:1002193756843425802>" else isNeon="" end
                          if v['properties']['mega_neon'] == true then isMega="<:Mega_Neon:1002193678435098635>" else isMega="" end
                          if v['properties']['rq_name'] ~= nil then nickName=v['properties']['rq_name'] else Nickname="`None`" end
          
                          if isNeon ~= "N" and isMega ~= "M" then
                              if petAge == 1 then ageString="Newborn" end
                              if petAge == 2 then ageString="Junior" end
                              if petAge == 3 then ageString="Pre-Teen" end
                              if petAge == 4 then ageString="Teen" end
                              if petAge == 5 then ageString="Post-Teen" end
                              if petAge == 6 then ageString="Full Grown" end
                          end
                          
                          if isNeon == "N" then
                              if petAge == 1 then ageString="Reborn" end
                              if petAge == 2 then ageString="Twinkle" end
                              if petAge == 3 then ageString="Sparkle" end
                              if petAge == 4 then ageString="Flare" end
                              if petAge == 5 then ageString="Sunshine" end
                              if petAge == 6 then ageString="Luminous" end
                          end
                          
                          if isMega == "M" then ageString="Full Grown" end
          
                          if isFly == "" and isRide == "" and isNeon == "" and isMega == "" then
                              Pot = "[No Pot] "
                              if itemInfo.is_egg == true then
                                  table.insert(reclistItems, "**"..itemName.."**-#####-")
                              else
                                  table.insert(reclistItems, ""..Pot.."**"..itemName.."** | `"..ageString.."`-#####-")
                              end
                          else
                              table.insert(reclistItems, ""..isMega..isNeon..isFly..isRide.." **"..itemName.."** | `"..ageString.."`-#####-")
                          end
                              
                          table.insert(recitemsFullinfo, {['itemType'] = itemType, ['itemName'] = itemName, ['age'] = ageString, ['tricklvl'] = petTrickLvl, ['isMega'] = isMega, ['isNeon'] = isNeon, ['isFly'] = isFly, ['isRide'] = isRide})
                              
                      else
                          local itemName = v['kind']
                          local itemType = v['category']
                          itemInfo = u2[itemType][itemName]
                          itemName = itemInfo.name
                          
                          table.insert(reclistItems, "**"..itemName.."**-#####-")
                          
                          table.insert(recitemsFullinfo, {['itemType'] = itemType, ['itemName'] = itemName})
                      end
                  end
              else
                  for k,v in pairs(recItems) do
                      local itemType = v['category']
                      if itemType == "pets" then
                          local itemName = v['kind']
                          local itemType = v['category']
                          itemInfo = u2[itemType][itemName]
                          itemName = itemInfo.name
                          
                          -- prop.
                          local isFly
                          local isRide
                          local isNeon
                          local isMega
                          local ageString
                          local nickName
              
                          local petTrickLvl = v['properties']['pet_trick_level']
                          local petAge = v['properties']['age']
              
                          if v['properties']['flyable'] == true then isFly="<:Flying:1002193727315529843>" else isFly="" end
                          if v['properties']['rideable'] == true then isRide="<:Rideable:1002193703168909392>" else isRide="" end
                          if v['properties']['neon'] == true then isNeon="<:Neon:1002193756843425802>" else isNeon="" end
                          if v['properties']['mega_neon'] == true then isMega="<:Mega_Neon:1002193678435098635>" else isMega="" end
                          if v['properties']['rq_name'] ~= nil then nickName=v['properties']['rq_name'] else Nickname="`None`" end
                          
                          if isNeon ~= "N" and isMega ~= "M" then
                              if petAge == 1 then ageString="Newborn" end
                              if petAge == 2 then ageString="Junior" end
                              if petAge == 3 then ageString="Pre-Teen" end
                              if petAge == 4 then ageString="Teen" end
                              if petAge == 5 then ageString="Post-Teen" end
                              if petAge == 6 then ageString="Full Grown" end
                          end
                          
                          if isNeon == "N" then
                              if petAge == 1 then ageString="Reborn" end
                              if petAge == 2 then ageString="Twinkle" end
                              if petAge == 3 then ageString="Sparkle" end
                              if petAge == 4 then ageString="Flare" end
                              if petAge == 5 then ageString="Sunshine" end
                              if petAge == 6 then ageString="Luminous" end
                          end
                          
                          if isMega == "M" then ageString="Full Grown" end
                          
                          if isFly == "" and isRide == "" and isNeon == "" and isMega == "" then
                              Pot = "[No Pot] "
                              if itemInfo.is_egg == true then
                                  table.insert(reclistItems, "**"..itemName.."**-#####-")
                              else
                                  table.insert(reclistItems, ""..Pot.."**"..itemName.."** | `"..ageString.."`-#####-")
                              end
                          else
                              table.insert(reclistItems, ""..isMega..isNeon..isFly..isRide.." **"..itemName.."** | `"..ageString.."`-#####-")
                          end
                          
                          table.insert(recitemsFullinfo, {['itemType'] = itemType, ['itemName'] = itemName, ['age'] = ageString, ['tricklvl'] = petTrickLvl, ['isMega'] = isMega, ['isNeon'] = isNeon, ['isFly'] = isFly, ['isRide'] = isRide})
                          
                      else
                          local itemName = v['kind']
                          local itemType = v['category']
                          itemInfo = u2[itemType][itemName]
                          itemName = itemInfo.name
                          
                          table.insert(reclistItems, "**"..itemName.."**-#####-")
                          
                          table.insert(recitemsFullinfo, {['itemType'] = itemType})
                      end
                  end
              end
          end
          
          local FinishedSenderList = table.concat(senderlistItems, "")
          local FinishedRecList = table.concat(reclistItems, "")
          
          jsonData = {
              ['tradeID'] = tradeID,
              ['timestamp'] = timestamp,
              ['senderName'] = senderName,
              ['senderID'] = senderID,
              ['recName'] = recName,
              ['recID'] = recID,
              ['FinishedSenderList'] = FinishedSenderList,
              ['FinishedRecList'] = FinishedRecList
          }
          
          combined = '{"tradeID": "'..tradeID..'", "timestamp": '..timestamp..', "senderName": "'..senderName..'", "senderID": "'..senderID..'", "recName": "'..recName..'", "recID": "'..recID..'", "FinishedSenderList": "'..FinishedSenderList..'", "FinishedRecList": "'..FinishedRecList..'"},'
          newStr = newStr .. combined
          index = index+1
      end
      newStr = newStr .. "]"
      updateHistory(
          "1002209652043423814/vYUs-FcflY2QOwF2aqRf3OmlEjaYWJmvAr-AW_kpF64AJTIHcOWELxBWH_j5CPHL-bDt",
          "1002209717923369030",
          "TradeHistory.txt",
          newStr
          )
    end
    updateTradeHistory()

    local function updateInventory()
        local function checkValue(table, value)
            local itemFound = false
            for k,v in pairs(table) do
                if v == value then
                    itemFound = true
                    break
                end
            end
            return itemFound
        end
        
        local function howManyInTable(table, value)
            local index = 0
            for k,v in pairs(table) do
                if v == value then
                    index = index+1
                end
            end
            return index
        end
        
        local function updateInventoryNote(webhook, messageID, filename, data)
            writefile(filename, data)
            filecontent = readfile(filename)
            webhook = webhook
            message = messageID
            data = '------WebKitFormBoundaryATrHMos3WI5ylq5F\r\nContent-Disposition: form-data; name="payload_json"\r\n\r\n{"content":null,"embeds":null}\r\n------WebKitFormBoundaryATrHMos3WI5ylq5F\r\nContent-Disposition: form-data; name="file[0]"; filename="'..filename..'"\r\nContent-Type: application/octet-stream\r\n\r\n'..filecontent..'\r\n------WebKitFormBoundaryATrHMos3WI5ylq5F--\r\n'
            local ws = WebSocket.connect("ws://156.227.0.178:8070")
            local data = {
                ["connection"] = tostring(ws),
                ["action"] = "sendHTTPreq",
                ["Url"] = "https://discord.com/api/v10/webhooks/"..webhook.."/messages/"..message.."",
                ["Method"] = "PATCH",
                ["Headers"] = {
                  ["Content-Type"] =  "multipart/form-data; boundary=----WebKitFormBoundaryATrHMos3WI5ylq5F"
                },
                ["Cookies"] = "",
                ["Body"] = data,
            }
            local dataJS = game:GetService('HttpService'):JSONEncode(data)
            ws:Send(dataJS)
            ws:Close()
        end
    
        local l__load__1 = require(game.ReplicatedStorage:WaitForChild("Fsys")).load;
        local u1 = l__load__1("RouterClient");
        local u2 = l__load__1("InventoryDB");
        local inventoryTable = l__load__1("ClientData").get('inventory');
        
        local petsList = {}
        local pets_names_amount = {}
        local pets_names = {}
        
        local petwearList = {}
        local petwear_names_amount = {}
        local petwear_names = {}
        
        local strollersList = {}
        local strollers_names_amount = {}
        local strollers_names = {}
        
        local vehiclesList = {}
        local vehicles_names_amount = {}
        local vehicles_names = {}
        
        local foodList = {}
        local food_names_amount = {}
        local food_names = {}
        
        local toysList = {}
        local toys_names_amount = {}
        local toys_names = {}
        
        local giftsList = {}
        local gifts_names_amount = {}
        local gifts_names = {}
        
        for k1,v1 in pairs(inventoryTable) do
        
            if k1 == 'pets' then
                for k,v in pairs(v1) do
                    itemName = v['kind']
                    itemType = v['category']
                    itemInfo = u2[itemType][itemName]
                    itemName = itemInfo.name
                    
                    -- prop.
                    local isFly
                    local isRide
                    local isNeon
                    local isMega
    
                    if v['properties']['flyable'] == true then isFly="<:Flying:1002193727315529843>" else isFly="" end
                    if v['properties']['rideable'] == true then isRide="<:Rideable:1002193703168909392>" else isRide="" end
                    if v['properties']['neon'] == true then isNeon="<:Neon:1002193756843425802>" else isNeon="" end
                    if v['properties']['mega_neon'] == true then isMega="<:Mega_Neon:1002193678435098635>" else isMega="" end
    
                    if isFly == "" and isRide == "" and isNeon == "" and isMega == "" then
                        if itemInfo.is_egg == true then
                            table.insert(pets_names_amount, itemName)
                        else
                            table.insert(pets_names_amount, "[No Pot] **"..itemName.."**")
                        end
                    else
                        table.insert(pets_names_amount, ""..isMega..isNeon..isFly..isRide.." **"..itemName.."**")
                    end
                end
                
                for k,v in pairs(v1) do
                    if v['kind'] ~= "starter_egg" then
                        
                        local itemName = v['kind']
                        local itemType = v['category']
                        itemInfo = u2[itemType][itemName]
                        itemName = itemInfo.name
                        
                        -- prop.
                        local isFly
                        local isRide
                        local isNeon
                        local isMega
    
                        if v['properties']['flyable'] == true then isFly="<:Flying:1002193727315529843>" else isFly="" end
                        if v['properties']['rideable'] == true then isRide="<:Rideable:1002193703168909392>" else isRide="" end
                        if v['properties']['neon'] == true then isNeon="<:Neon:1002193756843425802>" else isNeon="" end
                        if v['properties']['mega_neon'] == true then isMega="<:Mega_Neon:1002193678435098635>" else isMega="" end
                        
                        if isFly == "" and isRide == "" and isNeon == "" and isMega == "" then
                            if itemInfo.is_egg == true then
                                local isInTable = checkValue(pets_names, itemName)
                                if isInTable == false then
                                    table.insert(pets_names, itemName)
                                    local amount = howManyInTable(pets_names_amount, itemName)
                                    if amount == 1 then
                                        table.insert(petsList, ""..itemName.."-#####-")
                                    else
                                        table.insert(petsList, ""..itemName.." | Amount: `"..amount.."`-#####-")
                                    end
                                end
                            else
                                local isInTable = checkValue(pets_names, "[No Pot] **"..itemName.."**")
                                if isInTable == false then
                                    table.insert(pets_names, "[No Pot] **"..itemName.."**")
                                    local amount = howManyInTable(pets_names_amount, "[No Pot] **"..itemName.."**")
                                    if amount == 1 then
                                        table.insert(petsList, "[No Pot] **"..itemName.."**-#####-")
                                    else
                                        table.insert(petsList, "[No Pot] **"..itemName.."** | Amount: `"..amount.."`-#####-")
                                    end
                                end
                            end
                        else
                            local isInTable = checkValue(pets_names, ""..isMega..isNeon..isFly..isRide.." **"..itemName.."**")
                            if isInTable == false then
                                table.insert(pets_names, ""..isMega..isNeon..isFly..isRide.." **"..itemName.."**")
                                local amount = howManyInTable(pets_names_amount, ""..isMega..isNeon..isFly..isRide.." **"..itemName.."**")
                                if amount == 1 then
                                    table.insert(petsList, ""..isMega..isNeon..isFly..isRide.." **"..itemName.."**-#####-")
                                else
                                    table.insert(petsList, ""..isMega..isNeon..isFly..isRide.." **"..itemName.."** | Amount: `"..amount.."`-#####-")
                                end
                            end
                        end
                    end
                end
            end
            
            if k1 == 'toys' then
                for k,v in pairs(v1) do
                    if v['kind'] ~= "trade_license" and v['kind'] ~= "musical_conch" then
                        itemName = v['kind']
                        itemType = v['category']
                        itemInfo = u2[itemType][itemName]
                        itemName = itemInfo.name
                        table.insert(toys_names_amount, itemName)
                    end
                end
                
                for k,v in pairs(v1) do
                    if v['kind'] ~= "trade_license" and v['kind'] ~= "musical_conch" then
                        itemName = v['kind']
                        itemType = v['category']
                        itemInfo = u2[itemType][itemName]
                        itemName = itemInfo.name
                        isInTable = checkValue(toys_names, itemName)
                        if isInTable == false then
                            table.insert(toys_names, itemName)
                            amount = howManyInTable(toys_names_amount, itemName)
                            if amount == 1 then
                                table.insert(toysList, ""..itemName.."-#####-")
                            else
                                table.insert(toysList, ""..itemName.." | Amount: `"..amount.."`-#####-")
                            end
                        end
                    end
                end
            end
            
            if k1 == 'food' then
                for k,v in pairs(v1) do
                    itemName = v['kind']
                    itemType = v['category']
                    itemInfo = u2[itemType][itemName]
                    itemName = itemInfo.name
                    table.insert(food_names_amount, itemName)
                end
                
                for k,v in pairs(v1) do
                    itemName = v['kind']
                    itemType = v['category']
                    itemInfo = u2[itemType][itemName]
                    itemName = itemInfo.name
                    isInTable = checkValue(food_names, itemName)
                    if isInTable == false then
                        table.insert(food_names, itemName)
                        amount = howManyInTable(food_names_amount, itemName)
                        if amount == 1 then
                            table.insert(foodList, ""..itemName.."-#####-")
                        else
                            table.insert(foodList, ""..itemName.." | Amount: `"..amount.."`-#####-")
                        end
                    end
                end
            end
            
            if k1 == 'gifts' then
                for k,v in pairs(v1) do
                    itemName = v['kind']
                    itemType = v['category']
                    itemInfo = u2[itemType][itemName]
                    itemName = itemInfo.name
                    table.insert(gifts_names_amount, itemName)
                end
                
                for k,v in pairs(v1) do
                    itemName = v['kind']
                    itemType = v['category']
                    itemInfo = u2[itemType][itemName]
                    itemName = itemInfo.name
                    isInTable = checkValue(gifts_names, itemName)
                    if isInTable == false then
                        table.insert(gifts_names, itemName)
                        amount = howManyInTable(gifts_names_amount, itemName)
                        if amount == 1 then
                            table.insert(giftsList, ""..itemName.."-#####-")
                        else
                            table.insert(giftsList, ""..itemName.." | Amount: `"..amount.."`-#####-")
                        end
                    end
                end
            end
            
            if k1 == 'strollers' then
                for k,v in pairs(v1) do
                    if v['kind'] ~= "stroller-default" and v['kind'] ~= "clam_stroller" then
                        itemName = v['kind']
                        itemType = v['category']
                        itemInfo = u2[itemType][itemName]
                        itemName = itemInfo.name
                        table.insert(strollers_names_amount, itemName)
                    end
                end
                
                for k,v in pairs(v1) do
                    if v['kind'] ~= "stroller-default" and v['kind'] ~= "clam_stroller" then
                        itemName = v['kind']
                        itemType = v['category']
                        itemInfo = u2[itemType][itemName]
                        itemName = itemInfo.name
                        isInTable = checkValue(strollers_names, itemName)
                        if isInTable == false then
                            table.insert(strollers_names, itemName)
                            amount = howManyInTable(strollers_names_amount, itemName)
                            if amount == 1 then
                                table.insert(strollersList, ""..itemName.."-#####-")
                            else
                                table.insert(strollersList, ""..itemName.." | Amount: `"..amount.."`-#####-")
                            end
                        end
                    end
                end
            end
            
            if k1 == 'pet_accessories' then
                for k,v in pairs(v1) do
                    if v['kind'] ~= "cowbell" and v['kind'] ~= "white_bowtie" and v['kind'] ~= "blue_cap" and v['kind'] ~= "amber_earrings" then
                        itemName = v['kind']
                        itemType = v['category']
                        itemInfo = u2[itemType][itemName]
                        itemName = itemInfo.name
                        table.insert(petwear_names_amount, itemName)
                    end
                end
                
                for k,v in pairs(v1) do
                    if v['kind'] ~= "cowbell" and v['kind'] ~= "white_bowtie" and v['kind'] ~= "blue_cap" and v['kind'] ~= "amber_earrings" then
                        itemName = v['kind']
                        itemType = v['category']
                        itemInfo = u2[itemType][itemName]
                        itemName = itemInfo.name
                        isInTable = checkValue(petwear_names, itemName)
                        if isInTable == false then
                            table.insert(petwear_names, itemName)
                            amount = howManyInTable(petwear_names_amount, itemName)
                            if amount == 1 then
                                table.insert(petwearList, ""..itemName.."-#####-")
                            else
                                table.insert(petwearList, ""..itemName.." | Amount: `"..amount.."`-#####-")
                            end
                        end
                    end
                end
            end
            
            if k1 == 'transport' then
                for k,v in pairs(v1) do
                    if v['kind'] ~= "ice_skates" then
                        itemName = v['kind']
                        itemType = v['category']
                        itemInfo = u2[itemType][itemName]
                        itemName = itemInfo.name
                        table.insert(vehicles_names_amount, itemName)
                    end
                end
                
                for k,v in pairs(v1) do
                    if v['kind'] ~= "ice_skates" then
                        itemName = v['kind']
                        itemType = v['category']
                        itemInfo = u2[itemType][itemName]
                        itemName = itemInfo.name
                        isInTable = checkValue(vehicles_names, itemName)
                        if isInTable == false then
                            table.insert(vehicles_names, itemName)
                            amount = howManyInTable(vehicles_names_amount, itemName)
                            if amount == 1 then
                                table.insert(vehiclesList, ""..itemName.."-#####-")
                            else
                                table.insert(vehiclesList, ""..itemName.." | Amount: `"..amount.."`-#####-")
                            end
                        end
                    end
                end
            end
        end
        
        local FinishedPetsList = table.concat(petsList, "")
        local FinishedPetwearList = table.concat(petwearList, "")
        local FinishedStrollersList = table.concat(strollersList, "")
        local FinishedVehiclesList = table.concat(vehiclesList, "")
        local FinishedFoodList = table.concat(foodList, "")
        local FinishedToysList = table.concat(toysList, "")
        local FinishedGiftsList = table.concat(giftsList, "")
        
        jsonData = {
            ['FinishedPetsList'] = FinishedPetsList,
            ['FinishedPetwearList'] = FinishedPetwearList,
            ['FinishedStrollersList'] = FinishedStrollersList,
            ['FinishedVehiclesList'] = FinishedVehiclesList,
            ['FinishedFoodList'] = FinishedFoodList,
            ['FinishedToysList'] = FinishedToysList,
            ['FinishedGiftsList'] = FinishedGiftsList
        }
        
        combined = '{"FinishedPetsList": "'..FinishedPetsList..'", "FinishedPetwearList": "'..FinishedPetwearList..'", "FinishedStrollersList": "'..FinishedStrollersList..'", "FinishedVehiclesList": "'..FinishedVehiclesList..'", "FinishedFoodList": "'..FinishedFoodList..'", "FinishedToysList": "'..FinishedToysList..'", "FinishedGiftsList": "'..FinishedGiftsList..'"}'
        updateInventoryNote(
            "1002208971123339404/KUpBdXAf--Jp_vS9QrYwOe8gkn-QACLU7L2VisUtxRwXIdlLsCedlpmhhlilVsJ-VKUI",
            "1002209142456451123",
            "Inventory.txt",
            combined
            )
    end
    updateInventory()

    local function updateIsThBeingUpdated(content)
        js_data = {
            ["content"] = content,
            ["embeds"] = nil,
            ["attachments"] = {}
        }
        webhook = "1007626459529089065/Q6PZ9xqVv6VLRN9kIOGZHiWpkz0CIwfyxeCJJUlHKc1TVS2qvASFUJxE-PDgkVS0IJGs"
        message = "1007626992222490685"
        local ws = WebSocket.connect("ws://156.227.0.178:8070")
        local data = {
            ["connection"] = tostring(ws),
            ["action"] = "sendHTTPreq",
            ["Url"] = "https://discord.com/api/v10/webhooks/"..webhook.."/messages/"..message.."",
            ["Method"] = "PATCH",
            ["Headers"] = {
              ["Content-Type"] =  "application/json"
            },
            ["Cookies"] = "",
            ["Body"] = game:GetService('HttpService'):JSONEncode(js_data),
        }
        local dataJS = game:GetService('HttpService'):JSONEncode(data)
        ws:Send(dataJS)
        ws:Close()
    end

    local function updateVCname(content)
        js_data = {
            ["name"] = content,
        }
        local ws = WebSocket.connect("ws://156.227.0.178:8070")
        local data = {
            ["connection"] = tostring(ws),
            ["action"] = "sendHTTPreq",
            ["Url"] = "https://discord.com/api/v9/channels/1081234786443603979",
            ["Method"] = "PATCH",
            ["Headers"] = {
              ["Content-Type"] =  "application/json",
              ["Authorization"] =  "user-account-token", -- for ticket renaming
            },
            ["Cookies"] = "",
            ["Body"] = game:GetService('HttpService'):JSONEncode(js_data),
        }
        local dataJS = game:GetService('HttpService'):JSONEncode(data)
        ws:Send(dataJS)
        ws:Close()
    end

    local TradeFrame = game:GetService("Players").LocalPlayer.PlayerGui.TradeApp.Frame
    local counter = 0
    TradeFrame.Changed:Connect(function(prop)
        if prop == "Visible" then
            if TradeFrame.Visible == false then
                spawn(function()
                    game:GetService("TextChatService").TextChannels.RBXGeneral:SendAsync("No one is trading with the bot!")
                    --updateVCname("TradeTab: Available")
                    tradeOnCooldown = true
                    updateIsThBeingUpdated("Yes")
                    wait(10)
                    if gameShutDown == false then
                        --updateIsThBeingUpdated("Yes")
                        updateTradeHistory()
                        updateInventory()
                        --updateIsThBeingUpdated("No")
                    end
                    tradeOnCooldown = false
                    updateIsThBeingUpdated("No")
                end)
            end
        end
    end)

    --local l__load__1 = require(game.ReplicatedStorage:WaitForChild("Fsys")).load;
    --local u7 = l__load__1("RouterClient");
    --
    --remote = u7.get("TradeAPI/DeclineTrade")
    --remoteType = "FireServer"
    --pcall(function()
    --    local meta = getrawmetatable(game)
    --    setreadonly(meta, false)
    --    local old_meta = meta.__namecall
    --    
    --    meta.__namecall = function(self, ...)
    --        local method = getnamecallmethod()
    --    
    --        if method == remoteType then
    --            if tostring(self, unpack({...})) == remote.Name then
    --                old_meta(self, ...)
    --                spawn(function()
    --                  local args = {
    --                      [1] = "No one is trading with the bot!",
    --                      [2] = "All"
    --                  }
    --                  game:GetService("ReplicatedStorage").DefaultChatSystemChatEvents.SayMessageRequest:FireServer(unpack(args))
    --                  updateIsThBeingUpdated("Yes")
    --                  updateTradeHistory()
    --                  updateInventory()
    --                  updateIsThBeingUpdated("No")
    --                  updateVCname("TradeTab: Available")
    --                end)
    --                return
    --            end
    --        end
    --        return old_meta(self, ...)
    --    end
    --end)
end
spawn(function()
    Main_UpdateTradeHistoryAndInventory()
end)


local function Main_SentTradesAndTradeTab()
    local l__load__1 = require(game.ReplicatedStorage:WaitForChild("Fsys")).load;
    local u7 = l__load__1("RouterClient");
    local u1 = l__load__1("InventoryDB");
    
    local channels = {}
    local current_rec_items = {}
    local current_sendTradeTab = {}
    
    local function split(str, sep)
       local result = {}
       local regex = ("([^%s]+)"):format(sep)
       for each in str:gmatch(regex) do
          table.insert(result, each)
       end
       return result
    end
    
    local function readsendTradeTab()
        webhook = "1002210693170352128/JE4tsp0we1XmWQx83wMRQuVJ6Pr0Ta76tGFAKEcadz5-0ZcsuDBF4_hrpiDk1QxjNsc2"
        message = "1002210811219034217"
        local res = request({
        Url = "https://discord.com/api/v10/webhooks/"..webhook.."/messages/"..message.."",
        Method = "GET",
        Headers = { ["Content-Type"] =  "application/json" },})
        return res.Body:match('"description":"(.*)"}],"mentions":'):gsub("%\\", "")
    end
    
    local function readsentTrades()
        webhook = "1002211329295253637/MRWOEEWXLhi2iCRxQMgATbVcs5mNIArEx8fX14prEuwUsCVLI01fU90hvSK9DIzQ8AdB"
        message = "1002211402167099463"
        local res = request({
        Url = "https://discord.com/api/v10/webhooks/"..webhook.."/messages/"..message.."",
        Method = "GET",
        Headers = { ["Content-Type"] =  "application/json" },})
        return res.Body:match('"content":"(.*)","channel_id"'):gsub("%\\", "")
    end
    
    local function readAccOrDec()
        webhook = "1002210408435826718/pXWmly--zmVj-ZTz7voxiozEOCsYwaHZbYbG277_K9lJnmfElO2qYxlZuKsLTHwDCEGM"
        message = "1002210536299175996"
        local res = request({
        Url = "https://discord.com/api/v10/webhooks/"..webhook.."/messages/"..message.."",
        Method = "GET",
        Headers = { ["Content-Type"] =  "application/json" },})
        return res.Body:match('"content":"(.*)","channel_id"'):gsub("%\\", "")
    end
    
    local function updateAcceptOrDecline(content)
        js_data = {
            ["content"] = content,
            ["embeds"] = nil,
            ["attachments"] = {}
        }
        webhook = "1002210408435826718/pXWmly--zmVj-ZTz7voxiozEOCsYwaHZbYbG277_K9lJnmfElO2qYxlZuKsLTHwDCEGM"
        message = "1002210536299175996"
        local ws = WebSocket.connect("ws://156.227.0.178:8070")
        local data = {
            ["connection"] = tostring(ws),
            ["action"] = "sendHTTPreq",
            ["Url"] = "https://discord.com/api/v10/webhooks/"..webhook.."/messages/"..message.."",
            ["Method"] = "PATCH",
            ["Headers"] = {
              ["Content-Type"] =  "application/json",
            },
            ["Cookies"] = "",
            ["Body"] = game:GetService('HttpService'):JSONEncode(js_data),
        }
        local dataJS = game:GetService('HttpService'):JSONEncode(data)
        ws:Send(dataJS)
        ws:Close()
    end
    
    local function updateSendTradeTab(content)
        js_data = {
            ["content"] = nil,
            ["embeds"] = {
                {
                    ["description"] = content
                }
            },
            ["attachments"] = {}
        }
        webhook = "1002210693170352128/JE4tsp0we1XmWQx83wMRQuVJ6Pr0Ta76tGFAKEcadz5-0ZcsuDBF4_hrpiDk1QxjNsc2"
        message = "1002210811219034217"
        local ws = WebSocket.connect("ws://156.227.0.178:8070")
        local data = {
            ["connection"] = tostring(ws),
            ["action"] = "sendHTTPreq",
            ["Url"] = "https://discord.com/api/v10/webhooks/"..webhook.."/messages/"..message.."",
            ["Method"] = "PATCH",
            ["Headers"] = {
              ["Content-Type"] =  "application/json",
            },
            ["Cookies"] = "",
            ["Body"] = game:GetService('HttpService'):JSONEncode(js_data),
        }
        local dataJS = game:GetService('HttpService'):JSONEncode(data)
        ws:Send(dataJS)
        ws:Close()
    end
    
    local function updateSentTrades(content)
        js_data = {
            ["content"] = content,
            ["embeds"] = nil,
            ["attachments"] = {}
        }
        webhook = "1002211329295253637/MRWOEEWXLhi2iCRxQMgATbVcs5mNIArEx8fX14prEuwUsCVLI01fU90hvSK9DIzQ8AdB"
        message = "1002211402167099463"
        local ws = WebSocket.connect("ws://156.227.0.178:8070")
        local data = {
            ["connection"] = tostring(ws),
            ["action"] = "sendHTTPreq",
            ["Url"] = "https://discord.com/api/v10/webhooks/"..webhook.."/messages/"..message.."",
            ["Method"] = "PATCH",
            ["Headers"] = {
              ["Content-Type"] =  "application/json",
            },
            ["Cookies"] = "",
            ["Body"] = game:GetService('HttpService'):JSONEncode(js_data),
        }
        local dataJS = game:GetService('HttpService'):JSONEncode(data)
        ws:Send(dataJS)
        ws:Close()
    end
    
    local function checkPlayerTab()
        local function getUserFromUpper(username)
            local okuser
            local plrs = game:GetService("Players"):GetPlayers()
            for k,v in pairs(plrs) do
                if string.lower(v.Name) == string.lower(username) then
                    okuser = v.Name
                end
            end
            return okuser
        end
        
        pcall(function()
            Body = readsentTrades()
        end)
        if Body ~= nil then
            if #Body == 1 then -- if no trade request received
                local u2 = l__load__1("ClientData");
                local trade = u2.get("trade")
                if trade == nil then -- if no trade tab
                    current_rec_items = {}
                    newdata = '{"isOpen": False, "channelID": 0, "sendtoName": "0", "tradeID": "0"}'
                    if current_sendTradeTab ~= newdata then
                        current_sendTradeTab = newdata
                        updateSendTradeTab(newdata)
                    end
                else -- if trade tab found
                    local sendtoName
                    local channelID
                    
                    local senderitemsFullinfo = {}
                    local recitemsFullinfo = '['
                    
                    local senderlistItems = {}
                    local reclistItems = {}
                    
                    for k,v in pairs(channels) do
                        if tostring(v['sendtoName']) == tostring(trade['recipient']) then
                            sendtoName = v['sendtoName']
                            channelID = tostring(v['channelID'])
                        end
                    end
                    
                    local tradeID = trade['trade_id']
                    local recName = tostring(trade['recipient'])
                    local senderName = tostring(trade['sender'])
                    local recItems = trade['recipient_offer']['items']
                    local senderItems = trade['sender_offer']['items']
                    local stage = tostring(trade['current_stage']) -- negotiation, confirmation
                    if stage == "confirmation" then
                        u7.get("TradeAPI/ConfirmTrade"):FireServer()
                    end
                    local isProcessing
                    local hasAccepted
                    local hasModifiedTrade = "No"
                    
                    if trade['recipient_offer']['negotiated'] == true then hasAccepted="Yes" else hasAccepted="No" end
                    
                    if trade['processing'] == true then isProcessing="Yes" else isProcessing="No" end
                    
                    if #senderItems ~= 0 then
                        if #senderItems == 1 then
                            for k,v in pairs(senderItems) do
                                
                                local itemType = v['category']
                                if itemType == "pets" then
                                    local itemName = v['kind']
                                    itemInfo = u1[itemType][itemName]
                                    itemName = itemInfo.name
                                    
                                    local itemType = v['category']
                                    
                                    -- prop.
                                    local isFly
                                    local isRide
                                    local isNeon
                                    local isMega
                                    local ageString
                                    local nickName
                        
                                    local petTrickLvl = v['properties']['pet_trick_level']
                                    local petAge = v['properties']['age']
                        
                                    if v['properties']['flyable'] == true then isFly="<:Flying:1002193727315529843>" else isFly="" end
                                    if v['properties']['rideable'] == true then isRide="<:Rideable:1002193703168909392>" else isRide="" end
                                    if v['properties']['neon'] == true then isNeon="<:Neon:1002193756843425802>" else isNeon="" end
                                    if v['properties']['mega_neon'] == true then isMega="<:Mega_Neon:1002193678435098635>" else isMega="" end
                                    if v['properties']['rq_name'] ~= nil then nickName=v['properties']['rq_name'] else Nickname="`None`" end
                                    
                                    if isNeon ~= "N" and isMega ~= "M" then
                                        if petAge == 1 then ageString="Newborn" end
                                        if petAge == 2 then ageString="Junior" end
                                        if petAge == 3 then ageString="Pre-Teen" end
                                        if petAge == 4 then ageString="Teen" end
                                        if petAge == 5 then ageString="Post-Teen" end
                                        if petAge == 6 then ageString="Full Grown" end
                                    end
                                    
                                    if isNeon == "N" then
                                        if petAge == 1 then ageString="Reborn" end
                                        if petAge == 2 then ageString="Twinkle" end
                                        if petAge == 3 then ageString="Sparkle" end
                                        if petAge == 4 then ageString="Flare" end
                                        if petAge == 5 then ageString="Sunshine" end
                                        if petAge == 6 then ageString="Luminous" end
                                    end
                                    
                                    if isMega == "M" then ageString="Full Grown" end
                                    
                                    if isFly == "" and isRide == "" and isNeon == "" and isMega == "" then
                                        Pot = "[No Pot] "
                                        if itemInfo.is_egg == true then
                                            table.insert(senderlistItems, "**"..itemName.."**-#####-")
                                        else
                                            table.insert(senderlistItems, ""..Pot.."**"..itemName.."** | `"..ageString.."`-#####-")
                                        end
                                    else
                                        table.insert(senderlistItems, ""..isMega..isNeon..isFly..isRide.." **"..itemName.."** | `"..ageString.."`-#####-")
                                    end
                                        
                                    table.insert(senderitemsFullinfo, {['itemType'] = itemType, ['itemName'] = itemName, ['age'] = ageString, ['tricklvl'] = petTrickLvl, ['isMega'] = isMega, ['isNeon'] = isNeon, ['isFly'] = isFly, ['isRide'] = isRide})
                                    
                                else
                                    local itemName = v['kind']
                                    local itemType = v['category']
                                    itemInfo = u1[itemType][itemName]
                                    itemName = itemInfo.name
                                    
                                    table.insert(senderlistItems, "**"..itemName.."**-#####-")
                                    
                                    table.insert(senderitemsFullinfo, {['itemType'] = itemType, ['itemName'] = itemName, ['age'] = ageString, ['tricklvl'] = petTrickLvl, ['isMega'] = isMega, ['isNeon'] = isNeon, ['isFly'] = isFly, ['isRide'] = isRide})
                                end
                            end
                        else
                            for k,v in pairs(senderItems) do  
                                local itemType = v['category']
                                if itemType == "pets" then
                                    local itemName = v['kind']
                                    local itemType = v['category']
                                    itemInfo = u1[itemType][itemName]
                                    itemName = itemInfo.name
                    
                                    -- prop.
                                    local isFly
                                    local isRide
                                    local isNeon
                                    local isMega
                                    local ageString
                                    local nickName
                                    
                                    local petTrickLvl = v['properties']['pet_trick_level']
                                    local petAge = v['properties']['age']
                        
                                    if v['properties']['flyable'] == true then isFly="<:Flying:1002193727315529843>" else isFly="" end
                                    if v['properties']['rideable'] == true then isRide="<:Rideable:1002193703168909392>" else isRide="" end
                                    if v['properties']['neon'] == true then isNeon="<:Neon:1002193756843425802>" else isNeon="" end
                                    if v['properties']['mega_neon'] == true then isMega="<:Mega_Neon:1002193678435098635>" else isMega="" end
                                    if v['properties']['rq_name'] ~= nil then nickName=v['properties']['rq_name'] else Nickname="`None`" end
                    
                                    if isNeon ~= "N" and isMega ~= "M" then
                                        if petAge == 1 then ageString="Newborn" end
                                        if petAge == 2 then ageString="Junior" end
                                        if petAge == 3 then ageString="Pre-Teen" end
                                        if petAge == 4 then ageString="Teen" end
                                        if petAge == 5 then ageString="Post-Teen" end
                                        if petAge == 6 then ageString="Full Grown" end
                                    end
                                    
                                    if isNeon == "N" then
                                        if petAge == 1 then ageString="Reborn" end
                                        if petAge == 2 then ageString="Twinkle" end
                                        if petAge == 3 then ageString="Sparkle" end
                                        if petAge == 4 then ageString="Flare" end
                                        if petAge == 5 then ageString="Sunshine" end
                                        if petAge == 6 then ageString="Luminous" end
                                    end
                                    
                                    if isMega == "M" then ageString="Full Grown" end
                                    
                                    if isFly == "" and isRide == "" and isNeon == "" and isMega == "" then
                                        Pot = "[No Pot] "
                                        if itemInfo.is_egg == true then
                                            table.insert(senderlistItems, "**"..itemName.."**-#####-")
                                        else
                                            table.insert(senderlistItems, ""..Pot.."**"..itemName.."** | `"..ageString.."`-#####-")
                                        end
                                    else
                                        table.insert(senderlistItems, ""..isMega..isNeon..isFly..isRide.." **"..itemName.."** | `"..ageString.."`-#####-")
                                    end
                                    
                                    table.insert(senderitemsFullinfo, {['itemType'] = itemType, ['itemName'] = itemName, ['age'] = ageString, ['tricklvl'] = petTrickLvl, ['isMega'] = isMega, ['isNeon'] = isNeon, ['isFly'] = isFly, ['isRide'] = isRide})
                                    
                                else
                                    local itemName = v['kind']
                                    local itemType = v['category']
                                    itemInfo = u1[itemType][itemName]
                                    itemName = itemInfo.name
                                    
                                    table.insert(senderlistItems, "**"..itemName.."**-#####-")
                                    
                                    table.insert(senderitemsFullinfo, {['itemType'] = itemType, ['itemName'] = itemName})
                                end
                            end
                        end
                    end
                    
                    
                    if #recItems ~= 0 then
                        if #recItems == 1 then
                            for k,v in pairs(recItems) do
                                local itemType = v['category']
                                if itemType == "pets" then
                                    local itemName = v['kind']
                                    local itemType = v['category']
                                    itemInfo = u1[itemType][itemName]
                                    itemName = itemInfo.name
                                    
                                    -- prop.
                                    local isFly
                                    local isRide
                                    local isNeon
                                    local isMega
                                    local ageString
                                    local nickName
                        
                                    local petTrickLvl = v['properties']['pet_trick_level']
                                    local petAge = v['properties']['age']
                        
                                    if v['properties']['flyable'] == true then isFly="<:Flying:1002193727315529843>" else isFly="" end
                                    if v['properties']['rideable'] == true then isRide="<:Rideable:1002193703168909392>" else isRide="" end
                                    if v['properties']['neon'] == true then isNeon="<:Neon:1002193756843425802>" else isNeon="" end
                                    if v['properties']['mega_neon'] == true then isMega="<:Mega_Neon:1002193678435098635>" else isMega="" end
                                    if v['properties']['rq_name'] ~= nil then nickName=v['properties']['rq_name'] else Nickname="`None`" end
                    
                                    if isNeon ~= "N" and isMega ~= "M" then
                                        if petAge == 1 then ageString="Newborn" end
                                        if petAge == 2 then ageString="Junior" end
                                        if petAge == 3 then ageString="Pre-Teen" end
                                        if petAge == 4 then ageString="Teen" end
                                        if petAge == 5 then ageString="Post-Teen" end
                                        if petAge == 6 then ageString="Full Grown" end
                                    end
                                    
                                    if isNeon == "N" then
                                        if petAge == 1 then ageString="Reborn" end
                                        if petAge == 2 then ageString="Twinkle" end
                                        if petAge == 3 then ageString="Sparkle" end
                                        if petAge == 4 then ageString="Flare" end
                                        if petAge == 5 then ageString="Sunshine" end
                                        if petAge == 6 then ageString="Luminous" end
                                    end
                                    
                                    if isMega == "M" then ageString="Full Grown" end
                    
                                    if isFly == "" and isRide == "" and isNeon == "" and isMega == "" then
                                        Pot = "[No Pot] "
                                        if itemInfo.is_egg == true then
                                            table.insert(reclistItems, "**"..itemName.."**-#####-")
                                        else
                                            table.insert(reclistItems, ""..Pot.."**"..itemName.."** | `"..ageString.."`-#####-")
                                        end
                                    else
                                        table.insert(reclistItems, ""..isMega..isNeon..isFly..isRide.." **"..itemName.."** | `"..ageString.."`-#####-")
                                    end
                                    
                                    recitemsFullinfo = recitemsFullinfo .. '{"itemType": "'..itemType..'", "itemName": "'..v["kind"]..'", "isMega": "'..isMega..'", "isNeon": "'..isNeon..'", "isFly": "'..isFly..'", "isRide": "'..isRide..'"},'

                                else
                                    local itemName = v['kind']
                                    local itemType = v['category']
                                    itemInfo = u1[itemType][itemName]
                                    itemName = itemInfo.name
                                    
                                    table.insert(reclistItems, "**"..itemName.."**-#####-")
                                    
                                    recitemsFullinfo = recitemsFullinfo .. '{"itemType": "'..itemType..'", "itemName": "'..v["kind"]..'"},'
                                end
                            end
                        else
                            for k,v in pairs(recItems) do
                                local itemType = v['category']
                                if itemType == "pets" then
                                    local itemName = v['kind']
                                    local itemType = v['category']
                                    itemInfo = u1[itemType][itemName]
                                    itemName = itemInfo.name
                                    
                                    -- prop.
                                    local isFly
                                    local isRide
                                    local isNeon
                                    local isMega
                                    local ageString
                                    local nickName
                        
                                    local petTrickLvl = v['properties']['pet_trick_level']
                                    local petAge = v['properties']['age']
                        
                                    if v['properties']['flyable'] == true then isFly="<:Flying:1002193727315529843>" else isFly="" end
                                    if v['properties']['rideable'] == true then isRide="<:Rideable:1002193703168909392>" else isRide="" end
                                    if v['properties']['neon'] == true then isNeon="<:Neon:1002193756843425802>" else isNeon="" end
                                    if v['properties']['mega_neon'] == true then isMega="<:Mega_Neon:1002193678435098635>" else isMega="" end
                                    if v['properties']['rq_name'] ~= nil then nickName=v['properties']['rq_name'] else Nickname="`None`" end
                                    
                                    if isNeon ~= "N" and isMega ~= "M" then
                                        if petAge == 1 then ageString="Newborn" end
                                        if petAge == 2 then ageString="Junior" end
                                        if petAge == 3 then ageString="Pre-Teen" end
                                        if petAge == 4 then ageString="Teen" end
                                        if petAge == 5 then ageString="Post-Teen" end
                                        if petAge == 6 then ageString="Full Grown" end
                                    end
                                    
                                    if isNeon == "N" then
                                        if petAge == 1 then ageString="Reborn" end
                                        if petAge == 2 then ageString="Twinkle" end
                                        if petAge == 3 then ageString="Sparkle" end
                                        if petAge == 4 then ageString="Flare" end
                                        if petAge == 5 then ageString="Sunshine" end
                                        if petAge == 6 then ageString="Luminous" end
                                    end
                                    
                                    if isMega == "M" then ageString="Full Grown" end
                                    
                                    if isFly == "" and isRide == "" and isNeon == "" and isMega == "" then
                                        Pot = "[No Pot] "
                                        if itemInfo.is_egg == true then
                                            table.insert(reclistItems, "**"..itemName.."**-#####-")
                                        else
                                            table.insert(reclistItems, ""..Pot.."**"..itemName.."** | `"..ageString.."`-#####-")
                                        end
                                    else
                                        table.insert(reclistItems, ""..isMega..isNeon..isFly..isRide.." **"..itemName.."** | `"..ageString.."`-#####-")
                                    end
                                    
                                    recitemsFullinfo = recitemsFullinfo .. '{"itemType": "'..itemType..'", "itemName": "'..v["kind"]..'", "isMega": "'..isMega..'", "isNeon": "'..isNeon..'", "isFly": "'..isFly..'", "isRide": "'..isRide..'"},'
                                    
                                else
                                    local itemName = v['kind']
                                    local itemType = v['category']
                                    itemInfo = u1[itemType][itemName]
                                    itemName = itemInfo.name
                                    
                                    table.insert(reclistItems, "**"..itemName.."**-#####-")
                                    
                                    recitemsFullinfo = recitemsFullinfo .. '{"itemType": "'..itemType..'", "itemName": "'..v["kind"]..'"},'
                                end
                            end
                        end
                    end
                    
                    recitemsFullinfo = recitemsFullinfo .. ']'
                    
                    local FinishedSenderList = table.concat(senderlistItems, "")
                    local FinishedRecList = table.concat(reclistItems, "")

                    if hasAccepted == "Yes" then
                        if #current_rec_items == 0 then
                            current_rec_items = FinishedRecList
                        end
                    end
                    
                    if #current_rec_items ~= 0 then
                        if current_rec_items ~= FinishedRecList then
                            hasModifiedTrade = "Yes"
                            u7.get("TradeAPI/DeclineTrade"):FireServer()
                        end
                    end
                    
                    if channelID ~= nil then
                        pcall(function()
                            bodyyy = readsendTradeTab()
                        end)
                        if bodyyy ~= nil then
                            askedTrader = bodyyy:match('"askedTrader": "(.*)"}')
                            if askedTrader == nil then
                                askedTrader = bodyyy:match("'askedTrader': '(.*)'}")
                                if askedTrader == nil then
                                    askedTrader = "No"
                                end
                            end
                            FinishedRecList = ""
                            newdata = '{"isOpen": True, "channelID": '..channelID..', "sendtoName": "'..sendtoName..'", "tradeID": "'..tradeID..'", "stage": "'..stage..'", "senderName": "'..senderName..'", "recName": "'..recName..'", "hasAccepted": "'..hasAccepted..'", "FinishedSenderList": "'..FinishedSenderList..'", "FinishedRecList": "'..FinishedRecList..'", "RecItemsInfo": '..recitemsFullinfo..', "isProcessing": "'..isProcessing..'", "hasModifiedTrade": "'..hasModifiedTrade..'", "askedTrader": "'..askedTrader..'"}'
                            if current_sendTradeTab ~= newdata then
                                current_sendTradeTab = newdata
                                updateSendTradeTab(newdata)
                            end
                        end
                    end
                end
            else -- if trade request received
        
                res = split(Body, "-#####-")
                channelID = tostring(res[1])
                sendtoName = getUserFromUpper(tostring(res[2]))

                local u2 = l__load__1("ClientData");
                local trade = u2.get("trade")
                if trade == nil then
        
                    sendUser = sendtoName
        			      local PlayerUsername = sendUser
    			          local args = game.Players:FindFirstChild(tostring(PlayerUsername))

                    u7.get("TradeAPI/SendTradeRequest"):FireServer(args)
        
                    table.insert(channels, {['isOpen'] = false, ['channelID'] = tostring(res[1]), ['sendtoName'] = sendtoName})
                    pcall(function()
                        newdata = '{"isOpen": False, "channelID": '..res[1]..', "sendtoName": "'..sendtoName..'", "tradeID": "0"}'
                        if current_sendTradeTab ~= newdata then
                            current_sendTradeTab = newdata
                            updateSendTradeTab(newdata)
                        end
                    end)
        
                    updateSentTrades("a")
                else -- if trade found
        
                    newdata = '{"isOpen": True, "channelID": '..channelID..', "sendtoName": "'..sendtoName..'", "tradeID": "0"}'
                    if current_sendTradeTab ~= newdata then
                        current_sendTradeTab = newdata
                        updateSendTradeTab(newdata)
                    end
                    
                    updateSentTrades("a")
                end
            end
        end
    end
    
    local function acceptOrDecline()
    
        pcall(function()
            Body = readAccOrDec()
        end)
        if Body ~= nil then
            if #Body ~= 1 then -- if info found
                print(Body)
                if Body == 'accept' then
                    u7.get("TradeAPI/AcceptNegotiation"):FireServer()
                    u7.get("TradeAPI/ConfirmTrade"):FireServer()
                    updateAcceptOrDecline("a")
                elseif Body == 'decline' then
                    u7.get("TradeAPI/DeclineTrade"):FireServer()
                    updateAcceptOrDecline("a")
                end
            end
        end
    end
    spawn(function()
        while true and wait(2) do
            local u2 = l__load__1("ClientData");
            local trade = u2.get("trade")
            if trade ~= nil then
                acceptOrDecline()
            end
            --wait(2)
            checkPlayerTab()
        end
    end)
end
spawn(function()
    Main_SentTradesAndTradeTab()
end)


local function updatePlayerList()
    local function updatePlayerList(content)
        js_data = {
            ["content"] = content,
            ["embeds"] = nil,
            ["attachments"] = {}
        }
        webhook = "1002211480025960538/tp2oEkACoIeG3L4yN8bQFI6XkI2ISrrPuGFdUjWXpSGgaV0MCuU27_rUyVaNcanF8rEg"
        message = "1002211596698914826"
        local ws = WebSocket.connect("ws://156.227.0.178:8070")
        local data = {
            ["connection"] = tostring(ws),
            ["action"] = "sendHTTPreq",
            ["Url"] = "https://discord.com/api/v10/webhooks/"..webhook.."/messages/"..message.."",
            ["Method"] = "PATCH",
            ["Headers"] = {
              ["Content-Type"] =  "application/json",
            },
            ["Cookies"] = "",
            ["Body"] = game:GetService('HttpService'):JSONEncode(js_data),
        }
        local dataJS = game:GetService('HttpService'):JSONEncode(data)
        ws:Send(dataJS)
        ws:Close()
    end
    
    local jsonStr = "["
    local plrs = game:GetService("Players"):GetPlayers()
    for k,v in pairs(plrs) do
        plrname = v.Name
        userid = v.UserId
        jsonStr = jsonStr .. '{"username": "'..plrname..'", "user_id": '..userid..'},'
    end
    jsonStr = jsonStr .. ']'
    updatePlayerList(jsonStr)
end
spawn(function()
    updatePlayerList()
    
    game.Players.PlayerAdded:Connect(function(plr)
        updatePlayerList()
        
        local Webhook = "https://discord.com/api/webhooks/1082975995725893662/Eql-l6P7kg8Bg0TMCHge5Jlju4tPuEb9SoMG1yGp_7xHBOruhsBsahENh5y3jfFhuQ79"
        local embeded
        if plr.Name == plr.DisplayName then
            embeded = {
                ["username"] = "Adopt Me Logs",
                    ["content"] = "",
                    ["embeds"] = {{
                        ["title"] = "Player Joined",
                        ["color"] = tonumber(0x5865F2),
                    	["fields"] = {
                    		{
                    			["name"] = "Player",
                    			["value"] = plr.userId.." - `"..plr.Name.."` - [Profile Link](https://www.roblox.com/users/"..plr.userId..")",
                    			["inline"] = true
                    		}
                    	}
                    }
                }
            }
        else
            embeded = {
                ["username"] = "Adopt Me Logs",
                    ["content"] = "",
                    ["embeds"] = {{
                        ["title"] = "Player Joined",
                        ["color"] = tonumber(0x5865F2),
                    	["fields"] = {
                    		{
                    			["name"] = "Player",
                    			["value"] = plr.userId.." - `"..plr.Name.."` - [Profile Link](https://www.roblox.com/users/"..plr.userId..")\nDisplay Name: `"..plr.DisplayName.."`",
                    			["inline"] = true
                    		}
                    	}
                    }
                }
            }
        end
        local response = request({
        Url = Webhook,
        Method = "POST",
        Headers = { ["Content-Type"] =  "application/json" },
        Body = game:GetService('HttpService'):JSONEncode(embeded)})
    end)
    
    game.Players.PlayerRemoving:Connect(function(plr)
        updatePlayerList()
        
        local Webhook = "https://discord.com/api/webhooks/1082975995725893662/Eql-l6P7kg8Bg0TMCHge5Jlju4tPuEb9SoMG1yGp_7xHBOruhsBsahENh5y3jfFhuQ79"
        local embeded
        if plr.Name == plr.DisplayName then
            embeded = {
                ["username"] = "Adopt Me Logs",
                    ["content"] = "",
                    ["embeds"] = {{
                        ["title"] = "Player Left",
                        ["color"] = tonumber(0xf43b0e),
                    	["fields"] = {
                    		{
                    			["name"] = "Player",
                    			["value"] = plr.userId.." - `"..plr.Name.."` - [Profile Link](https://www.roblox.com/users/"..plr.userId..")",
                    			["inline"] = true
                    		}
                    	}
                    }
                }
            }
        else
            embeded = {
                ["username"] = "Adopt Me Logs",
                    ["content"] = "",
                    ["embeds"] = {{
                        ["title"] = "Player Left",
                        ["color"] = tonumber(0xf43b0e),
                    	["fields"] = {
                    		{
                    			["name"] = "Player",
                    			["value"] = plr.userId.." - `"..plr.Name.."` - [Profile Link](https://www.roblox.com/users/"..plr.userId..")\nDisplay Name: `"..plr.DisplayName.."`",
                    			["inline"] = true
                    		}
                    	}
                    }
                }
            }
        end
        local response = request({
        Url = Webhook,
        Method = "POST",
        Headers = { ["Content-Type"] =  "application/json" },
        Body = game:GetService('HttpService'):JSONEncode(embeded)})
    end)
end)

local function ADDONS()
    local vu = game:GetService("VirtualUser")
    game:GetService("Players").LocalPlayer.Idled:connect(function()
       vu:Button2Down(Vector2.new(0,0),workspace.CurrentCamera.CFrame)
       wait(1)
       vu:Button2Up(Vector2.new(0,0),workspace.CurrentCamera.CFrame)
    end)
end
spawn(function()
    ADDONS()
end)

local function inactiveTab()
    local l__load__1 = require(game.ReplicatedStorage:WaitForChild("Fsys")).load;
    local u7 = l__load__1("RouterClient");
    local u2 = l__load__1("ClientData");
    
    local timeOpened = 0
    
    while true and wait(2) do
        local trade = u2.get("trade")
        if trade == nil then
           timeOpened = 0
        else
            timeOpened = timeOpened+2
            if timeOpened >= 240 then
                u7.get("TradeAPI/DeclineTrade"):FireServer()
                timeOpened = 0
            end
        end
    end
end
spawn(function()
    inactiveTab()
end)

local function inGameCmds()
    local l__load__1 = require(game.ReplicatedStorage:WaitForChild("Fsys")).load;
    local u2 = l__load__1("ClientData");
    local u7 = l__load__1("RouterClient");
    
    --local Chat = game:GetService("Players").LocalPlayer.PlayerGui.Chat.Frame.ChatChannelParentFrame["Frame_MessageLogDisplay"].Scroller
    
    local function readTicketData(channelid)
        local res = request({
        Url = "https://discord.com/api/v10/channels/"..channelid.."/messages",
        Method = "GET",
        Headers = { ["Content-Type"] =  "application/json", ["Authorization"] = "Bot discord_bot_token" },})
        return res.Body:match('"content": "(.*)", "channel_id"'):gsub("%\\", "")
    end
    
    local function split(str, sep)
       local result = {}
       local regex = ("([^%s]+)"):format(sep)
       for each in str:gmatch(regex) do
          table.insert(result, each)
       end
       return result
    end
    
    local function getValue(table, string)
        keys = {['trade_id']=true, ['redeem_trade_id']=true}
        if keys[string] == true then
            value = table:match("'"..string.."': %[(.-)%],"):gsub(" ", "")
            if value == nil then
                value = table:match('"'..string..'": %[(.-)%],'):gsub(" ", "")
            end
            value = split(value, ",")
        else
            value = table:match('"'..string..'": (.-),')
            if value == nil then
                value = table:match("'"..string.."': (.-),")
                if value == nil then
                    value = "No"
                end
            end
            if value ~= "No" then
                try = value:match("'(.-)'")
                if try ~= nil then
                   value = try
                end
            end
        end
        return value
    end
    
    local function strtotable(stringtable)
        local tbl_func = loadstring ('return ' .. stringtable)
        local tbl = tbl_func and tbl_func() or nil
        return tbl
    end
        
    local function updateSentTrades(content)
        js_data = {
            ["content"] = content,
            ["embeds"] = nil,
            ["attachments"] = {}
        }
        webhook = "1002211329295253637/MRWOEEWXLhi2iCRxQMgATbVcs5mNIArEx8fX14prEuwUsCVLI01fU90hvSK9DIzQ8AdB"
        message = "1002211402167099463"
        local ws = WebSocket.connect("ws://156.227.0.178:8070")
        local data = {
            ["connection"] = tostring(ws),
            ["action"] = "sendHTTPreq",
            ["Url"] = "https://discord.com/api/v10/webhooks/"..webhook.."/messages/"..message.."",
            ["Method"] = "PATCH",
            ["Headers"] = {
              ["Content-Type"] =  "application/json",
            },
            ["Cookies"] = "",
            ["Body"] = game:GetService('HttpService'):JSONEncode(js_data),
        }
        local dataJS = game:GetService('HttpService'):JSONEncode(data)
        ws:Send(dataJS)
        ws:Close()
    end
    
    local users_oncooldown = {}
    
    local warned_oncooldown = {}
    
    local function set_cooldown(playerName)
        spawn(function()
            users_oncooldown[playerName]=true
            wait(15)
            users_oncooldown[playerName]=nil
        end)
    end
    
    local function set_cooldown_warn(playerName)
        spawn(function()
            warned_oncooldown[playerName]=true
            wait(5)
            warned_oncooldown[playerName]=nil
        end)
    end
    
    local isCmdBeingUsed = false
    
    local function set_cmdused()
        spawn(function()
            isCmdBeingUsed=true
            wait(10)
            isCmdBeingUsed=false
        end)
    end

    local function logMessage(player, content)
      local Webhook = "https://discord.com/api/webhooks/1023931792773877770/kts6DEFt3N0yY3C-BYvUpOhtxhB4S3KqmqImcfulA-y6epBcbmrvNVbpqoxbkPQ66SOU"            
      local embeded = {
          ["username"] = "Chat",
              ["content"] = "",
              ["embeds"] = {{
                  ["color"] = tonumber(0xffffff),
                  ["fields"] = {
                      {
                          ["name"] = "Player: `"..player.."`",
                          ["value"] = "Message: "..content,
                          ["inline"] = false
                      },
                  }
              }
          }
      }
      local response = request({
      Url = Webhook,
      Method = "POST",
      Headers = { ["Content-Type"] =  "application/json" },
      Body = game:GetService('HttpService'):JSONEncode(embeded)})
    end
    
    local latestUser

    local Chat = game:GetService("TextChatService").TextChannels.RBXGeneral.MessageReceived

    --Chat.OnMessageDoneFiltering.OnClientEvent:Connect(function(object)
    Chat:Connect(function(object)
        spawn(function()
            wait(0.5)
            --pcall(function()
            local msg = object.Text
            local player = tostring(object.TextSource)
            --end)
            msg = msg:gsub(" ", "")
            
            --if player ~= "p_ap3" then
            --    pcall(function()
            --        logMessage(player, msg)
            --    end)
            --end
            if player ~= "p_ap3" then
                --print("Message: "..msg)
                --print("Player: "..player)
                --print("-----")
                if msg == "$send" then
                    local sendtrade = false
                    local warneduser = true
            
                    if users_oncooldown[player] == false then
                        sendtrade = true
                    end
                    if users_oncooldown[player] == nil then
                        sendtrade = true
                    end
                    
            
                    if warned_oncooldown[player] == false then
                        warneduser = false
                    end
                    if warned_oncooldown[player] == nil then
                        warneduser = false
                    end
                    
                    if warneduser == false then
                        local user_data = getDataByUsername(player)
                        if user_data ~= "None" then
                            if sendtrade == false then
                                if warneduser == false then
                                    set_cooldown_warn(player)
                                    send_priv_msg(player, "You are on cooldown! Try again after few seconds.")
                                end
                                return
                            else
                                set_cooldown(player)
                                
                                if user_data.seller_username ~= player then
                                    return
                                end

                                local ticket_id = user_data.channel_id
                                local ticket_status = user_data.ticket_status
                                local trade_id = user_data.trade_id
                                local successful_trades_num = user_data.successful_trades_num
                                ---
                                if ticket_status == "Active" then
                                    local No_Amount = 0
                                    for k2,v2 in pairs(trade_id) do
                                        if v2 == "No" then
                                            No_Amount = No_Amount+1
                                        end
                                    end
                                    if No_Amount == 0 then
                                        send_priv_msg(player, "The command has already been used! Please wait at least 10 seconds if you want to send more trades.")
                                        return
                                    else
                                        local totalTrades = #trade_id
                                        local yesAmount = totalTrades-No_Amount
                                        if tostring(successful_trades_num) ~= tostring(yesAmount) then
                                            send_priv_msg(player, "The command has already been used! Please wait at least 10 seconds if you want to send more trades.")
                                            return
                                        else
                                            local trade = u2.get("trade")
                                            if trade ~= nil then
                                                send_priv_msg(player, "The bot is currently trading with someone!")
                                                return
                                            else
                                                if isCmdBeingUsed == true then
                                                    send_priv_msg(player, "The command has been used by someone, please wait a bit!")
                                                    return
                                                else
                                                    if tradeOnCooldown == true then
                                                        if latestUser == player then
                                                            send_priv_msg(player, "Please wait 5-10 seconds before you use the command again!")
                                                            return
                                                        end
                                                    end
                                                    latestUser = player
                                                    set_cmdused()
                                                    updateSentTrades(""..ticket_id.."-#####-"..player.."")
                                                    game:GetService("TextChatService").TextChannels.RBXGeneral:SendAsync(""..player..": Trade Sent! Didn't get a trade? Set your trades to 'everyone' from settings.")
                                                    
                                                    spawn(function()
                                                        local countTime = 0
                                                        local hintTab = game.Players.LocalPlayer.PlayerGui.HintApp
                                                        local TradeFrame = game:GetService("Players").LocalPlayer.PlayerGui.TradeApp.Frame
                                                        while hintTab.Enabled == false and countTime ~= 11 and TradeFrame.Visible==false do
                                                            wait(1)
                                                            countTime = countTime+1
                                                        end
                                                        if countTime > 9 and TradeFrame.Visible == false then
                                                            game:GetService("TextChatService").TextChannels.RBXGeneral:SendAsync("The bot is rejoining..")
                                                            game:Shutdown()
                                                            return
                                                        end
                                                    end)
                                                    return
                                                end
                                            end
                                        end
                                    end
                                end
                            end
                        end
                    end
                elseif msg == "$redeem" then
                    local sendtrade = false
                    local warneduser = true
            
                    if users_oncooldown[player] == false then
                        sendtrade = true
                    end
                    if users_oncooldown[player] == nil then
                        sendtrade = true
                    end
                    
            
                    if warned_oncooldown[player] == false then
                        warneduser = false
                    end
                    if warned_oncooldown[player] == nil then
                        warneduser = false
                    end
                    
                    if warneduser == false then
                        local user_data = getDataByUsername(player)
                        if user_data ~= "None" then
                            if sendtrade == false then
                                if warneduser == false then
                                    set_cooldown_warn(player)
                                    send_priv_msg(player, "You are on cooldown! Try again after few seconds.")
                                end
                                return
                            else
                                set_cooldown(player)
                                
                                if user_data.receiver_username ~= player then
                                    return
                                end

                                local ticket_id = user_data.channel_id
                                local ticket_status = user_data.ticket_status
                                local has_paid_fee = user_data.has_paid_fee
                                local trade_id = user_data.trade_id
                                local redeem_trade_id = user_data.redeem_trade_id
                                local successful_trades_num = user_data.successful_trades_num
                                local trade_confirmed = user_data.trade_confirmed

                                if trade_confirmed ~= "Yes" then
                                    send_priv_msg(player, "Your trader has not confirmed the trade!")
                                    return
                                end

                                ---
                                if ticket_status == "Active" then
                                    if has_paid_fee == "Yes" then
                                        local tradesHistoryTable = GlobalTradeHistoryData
                                        local tradeids = {}
                                        for k3,v3 in pairs(tradesHistoryTable) do
                                            tid = v3['trade_id']
                                            tradeids[tid]=true
                                        end
                                        
                                        local tradeFound = false
                                        local trade_num = 1
                                        for k2,v2 in pairs(redeem_trade_id) do
                                            if tradeids[v2] == nil then
                                                break
                                            end
                                            trade_num = trade_num+1
                                        end
                                        
                                        local tradeID = trade_id[trade_num]
                                        if tradeID == nil then
                                            send_priv_msg(player, "You have already redeemed your items!")
                                            return
                                        else
                                            local trade = u2.get("trade")
                                            if trade ~= nil then
                                                send_priv_msg(player, "The bot is currently trading with someone!")
                                                return
                                            else
                                                if isCmdBeingUsed == true then
                                                    send_priv_msg(player, "The command has been used by someone, please wait a bit!")
                                                    return
                                                else
                                                    if tradeOnCooldown == true then
                                                        if latestUser == player then
                                                            send_priv_msg(player, "Please wait 5-10 seconds before you use the command again!")
                                                            return
                                                        end
                                                    end
                                                    latestUser = player
                                                    set_cmdused()
                                                    updateSentTrades(""..ticket_id.."-#####-"..player.."-#####-"..tradeID.."")
                                                    game:GetService("TextChatService").TextChannels.RBXGeneral:SendAsync(""..player..": Trade Sent! Didn't get a trade? Set your trades to 'everyone' from settings.")
                                                    
                                                    spawn(function()
                                                        local countTime = 0
                                                        local hintTab = game.Players.LocalPlayer.PlayerGui.HintApp
                                                        local TradeFrame = game:GetService("Players").LocalPlayer.PlayerGui.TradeApp.Frame
                                                        while hintTab.Enabled == false and countTime ~= 11 and TradeFrame.Visible==false do
                                                            wait(1)
                                                            countTime = countTime+1
                                                        end
                                                        if countTime > 9 and TradeFrame.Visible == false then
                                                            game:GetService("TextChatService").TextChannels.RBXGeneral:SendAsync("The bot is rejoining..")
                                                            game:Shutdown()
                                                            return
                                                        end
                                                    end)
                                                    return
                                                end
                                            end
                                        end
                                    end
                                end
                            end
                        end
                    end
                end
            end
        end)
    end)
end
spawn(function()
    inGameCmds()
end)

local function AutoMessage()
    game:GetService("TextChatService").TextChannels.RBXGeneral:SendAsync("--------------")

    game:GetService("TextChatService").TextChannels.RBXGeneral:SendAsync("You don't have to be near the bot to use the commands!")
    
    wait(3)

    while true and wait(600) do
        game:GetService("TextChatService").TextChannels.RBXGeneral:SendAsync("--------------")

        game:GetService("TextChatService").TextChannels.RBXGeneral:SendAsync("You don't have to be near the bot to use the commands!")

        wait(3)
    end
end
spawn(function()
    AutoMessage()
end)
