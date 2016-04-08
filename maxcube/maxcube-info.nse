local shortport = require "shortport"
local stdnse = require "stdnse"

description = [[
Get basic information from a eQ-3 MAX! Cube LAN Gateway.

Product info:
http://www.eq-3.de/produkte/max-heizungssteuerung/max-hausloesung/bc-lgw-o-tw.html
]]

---
-- @output
-- PORT      STATE SERVICE
-- 62910/tcp open  unknown
-- | maxcube-info: 
-- |   MAX Serial:: KMD1016788
-- |   RF Address: 099c3e
-- |_  Firmware Version: 0113
--

author = "Niklaus Schiess <nschiess@ernw.de>"
license = "Same as Nmap--See https://nmap.org/book/man-legal.html"
categories = {"discovery", "safe"}
portrule = shortport.portnumber(62910, "tcp")

action = function(host, port)
  -- Wait for some time to make sure there is no open TCP connection.
  stdnse.sleep(1)

  local sock = nmap.new_socket()
  local status, err = sock:connect(host, port, "tcp")

  if not status then
    stdnse.debug1("%s", err)
    return
  end

  local status, data = sock:receive()

  if not status or not data then
    stdnse.debug1("%s", "Could not receive any data")
    return
  end

  local output = stdnse.output_table()
  local serial, rf_address, firmware

  for serial,rf_address,firmware in data:gmatch("H:(%u%u%u%d%d%d%d%d%d%d),(%x%x%x%x%x%x),(%d%d%d%d),") do
      output["MAX Serial:"] = serial
      output["RF Address"] = rf_address
      output["Firmware Version"] = firmware
  end

  return output
end
