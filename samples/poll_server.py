from q3serverquery.server import Quake3Server
from pprint import pprint
import re
import time

start = time.perf_counter()

server = Quake3Server('127.0.0.1', 27960)

server.get_info()
server.get_status()

pprint(server.info)
pprint(server.status)
pprint(server.players)

finish = time.perf_counter()

print(f'Finished in {round(finish-start, 2)} second(s)')