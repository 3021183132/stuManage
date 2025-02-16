import asyncio
from aiohttp import web
from SimpleWebServer.web.myjinja import html
from urllib.parse import parse_qs
from SimpleWebServer.util.txtutil import checkUserAndPwd
from SimpleWebServer.web.model.model import Model
import logging

async def check(info):
#     print(parse_qs(info.query_string))
    username = parse_qs(info.query_string)["username"][0]
    password = parse_qs(info.query_string)["password"][0]
    msg = "fail!"  
#     if username=="wxit" and password=="wxit":
#         msg = "success!"
#     else:
#         pass
    model = Model()
#     if checkUserAndPwd(username, password):
    if model.checkUserSAndpwd(username, password):
        msg = "success!"
    else:
        pass
    return web.Response(body=html("msg.html",**locals()),content_type="text/html")
    

def weblog(weblogstr,ip,path):
    logging.basicConfig(filename=weblogstr,format='%(message)s - %(asctime)s',level="DEBUG")
    msg = ip + " "+path
    logging.info(msg)
    
async def index(request):
    data=""
    
    ip = request._transport_peername[0]
    path = request.message.url
    logfile =os.path.abspath("../../logs/web.log") 
    print(logfile)
    await weblog(logfile,ip, path)

    with open("../views/login.html",encoding="utf-8") as f:
        data = f.read()
    data1 = web.Response(body=data,content_type="text/html")
    return data1
import os
async def init(loop):
    app = web.Application()
#     infos = [r for r in app.router.resources()]
#     print(type(infos))
#     if infos:
#         print(infos[0].split("\n\r")) 
#     
#     logfile = "../../logs/web.log"
#     print(os.path.abspath(logfile))
#     ip = ""
#     path = ""
#     weblog(logfile,ip, path)
    app.router.add_route('GET', '/', index)
    app.router.add_route('GET', '/check', check)    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner=runner,port=9000)
    await site.start()

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()