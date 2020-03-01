from q3serverquery.masterserver import Quake3MasterServer
from pprint import pprint
import re
import time

start = time.perf_counter()

master = Quake3MasterServer('master.ioquake3.org', 27950, 68)

master.get_servers()
master.poll_now()

servers = master.search_servers('q3dm17')

for server in servers:
    pprint(server.info)
    pprint(server.status)
    pprint(server.players)

finish = time.perf_counter()

print(f'Finished in {round(finish-start, 2)} second(s)')