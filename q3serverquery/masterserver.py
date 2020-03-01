import socket
import concurrent.futures
import re
from .server import Server

class MasterServer(object):
    
    def __init__(
        self,
        hostname,
        port,
        game_id,
        timeout=1,
    ):
        """
            MasterServer class init statement

            Args:
                hostname (str): Resolvable DNS name or IP address for the
                    Master Server you'd wish to poll.
                port (int): The port number the master server is
                    listening on
                game_id (int): The game ID for the game server to return
                    a server list for.

                    For example: ioquake3 uses a game_id of '68' for its client.
        """

        self.hostname = hostname
        self.port = port
        self.game_id = game_id
        self.servers = []

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(timeout)
        self.server = (self.hostname, self.port)

    def get_servers(self):
        """
            Poll the Master Server for a client list and sets the class
            attribute of 'servers' to a list of Server objects.

            Returns: None
        """

        # The Quake style queries to end clients (whether they be Master Servers
        # or server clients), need a header of 4 \xFF bytes

        prefix = b"\xFF\xFF\xFF\xFF"
        command = bytes(
            'getservers ' + str(self.game_id),
            encoding='utf-8'
        )

        self.sock.sendto(prefix + command, self.server)

        try:
            data, _ = self.sock.recvfrom(4096)
        except socket.timeout as e:
            raise e

        for i in range(len(data)):
            try:
                if chr(data[i]) == '\\' and chr(data[i + 7]) == '\\':
                    
                    ip_octets = []
                    for j in range(1, 5):
                        ip_octets.append(str(data[i + j]))

                    self.servers.append(
                        Server(
                            ".".join(ip_octets),
                            (data[i + 5]<<8) + data[i + 6]
                        )
                    )

            except IndexError:
                continue

    def search_servers(self, query):
        """
            Search for a given query in any of the values in the server dict
            keys.

            Args:
                query (str): the search query to look for in the dictionary keys

            Returns: A list of Servers
        """
        if not self.servers:
            return

        return_list = []

        for server in self.servers:
            info_results = [key for key, val in server.info.items() if re.search(query, val)]
            search_results = [key for key, val in server.info.items() if re.search(query, val)]

            if info_results or search_results:
                return_list.append(server)

        return return_list

    

    def poll_now(self):
        """
            Concurrently poll all servers captured from the Master Server and
            capture info and status headers.

            Returns: None
        """

        def get_server_status_and_info(server):
            server.get_status()
            server.get_info()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(get_server_status_and_info, self.servers)

    