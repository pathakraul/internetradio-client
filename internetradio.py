#!/usr/bin/python

# Internet Radio Client using Shoutcast service
# to search and play random channels with genre search
# Usage ./internetradio.py --genre <GENRE>


import os
import logging
import argparse
import requests as rq
import xml.etree.ElementTree as et

#----------------------------------------------------------------------------------------
# Set your shoutcast devId here
#----------------------------------------------------------------------------------------
devId = ""

#----------------------------------------------------------------------------------------
logging.basicConfig(format='%(levelname)s %(asctime)s %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)

#----------------------------------------------------------------------------------------
baseUrl = "http://api.shoutcast.com/"
tuneinUrl = "http://yp.shoutcast.com/"
base = "sbin/tunein-station.pls"
randomSearch = "station/randomstations?k={0}&f=xml&mt=audio/mpeg&limit=1&genre=".format(devId)
#----------------------------------------------------------------------------------------

playerCommand = "mplayer -quiet  {0}\n"

#----------------------------------------------------------------------------------------
def keywordSearch(keyword):
    log.debug("Making Keyword Search\n")
    searchurl=baseUrl+randomSearch+keyword
    log.debug("Searching for {0} on Shoutcast".format(keyword))
    res = rq.get(searchurl, proxies=proxies)
    if res.status_code == 200:
        srtContent = res.content
        return str(res.content)
    else:
        log.error("Search response failure from server {0}".format(res.status_code))
#----------------------------------------------------------------------------------------
'''
<response>
    <statusCode>200</statusCode>    #tree[0]
    <statusText>Ok</statusText>     #tree[1]
    <data>                          #tree[2]                          
        <stationlist>               #tree[2][0]
            <tunein base="/sbin/tunein-station.pls" base-m3u="/sbin/tunein-station.m3u" base-xspf="/sbin/tunein-station.xspf"/>     #tree[2][0][0]
            <station name="Bollywood Hits" genre="Hindi" ct="Baamulaiza - Mika Singh Domnique Cerejo Style Bhai" mt="audio/mpeg" id="312131" br="96" lc="13" ml="100"/>     #tree[2][0][1]
        </stationlist>
    </data>
</response>
'''

def getRandomChannel(data):
    tree = et.fromstring(data)
    cid = tree[2][0][1].attrib['id']
    cn =  tree[2][0][1].attrib['name']
    log.info("Playing Channel [{0}], Channel ID [{1}]".format(cn, cid))
    return cid

#----------------------------------------------------------------------------------------
def playChannel(channelId):
    channelurl = tuneinUrl+base+"?id="+ str(channelId)
    channelstream = parseStreamUrl(channelurl)
    print channelstream
    command = playerCommand.format(channelstream)
    print command
    os.system(command)

#----------------------------------------------------------------------------------------
def searchChannelAndPlay(genreKeyword):
    responsedata = keywordSearch(genreKeyword)
    channelid = getRandomChannel(responsedata)
    playChannel(channelid)

#----------------------------------------------------------------------------------------
def parseStreamUrl(channelurl):
    response = rq.get(channelurl, stream=True, proxies=proxies)
    with open("stream.pls", "wb") as handle:
        for data in response.iter_content():
            handle.write(data)
    x = []
    datafile = file('./stream.pls')
    for line in datafile:
        if "File1=" in line:
            x = str(line)
            return x[6:-1]

#----------------------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--genre", help="Search random channel of particular genre")
    args = parser.parse_args()
    if args.genre:
        genreKeyword = args.genre
    else:
        log.error("Provide any genre to search a random channel")
    
    searchChannelAndPlay(genreKeyword)
#----------------------------------------------------------------------------------------


