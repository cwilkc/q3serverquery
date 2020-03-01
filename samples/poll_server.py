from q3serverquery.server import Server
import socket
from pprint import pprint
import re
import time

start = time.perf_counter()

server = Server('lan.fubar.gg', 27960)

server.get_info()
server.get_status()

pprint(server.info)
pprint(server.status)
pprint(server.players)

finish = time.perf_counter()

print(f'Finished in {round(finish-start, 2)} second(s)')