import socket

class Server(object):
    
    def __init__(
        self,
        hostname,
        port,
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
        self.info = {}
        self.status = {}
        self.players = {}

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(timeout)
        self.server = (self.hostname, self.port)

    def get_info(
        self,
        challenge='xxx',
    ):
        """
            Poll the server for the information header and apply to the class
            attribute of 'info'

            Returns: None
        """

        # The Quake style queries to end clients (whether they be Master Servers
        # or server clients), need a header of 4 \xFF bytes

        prefix = b"\xFF\xFF\xFF\xFF"
        command = bytes(
            'getinfo ' + challenge,
            encoding='utf-8'
        )

        self.sock.sendto(prefix + command, self.server)

        try:
            data, _ = self.sock.recvfrom(4096)
        except socket.timeout:
            return

        # The response will include a 4 byte header that we need to ignore.
        # Then we want to split on new line characters and '\\'. This will
        # create a list that always has a blank first element so we slice it off
        attr_list = data[4:].split(b'\n')[1].split(b'\\')[1:]

        element = zip(attr_list[::2], attr_list[1::2])

        for el in element:
            self.info[el[0].decode('utf-8')] = el[1].decode('utf-8')

    def get_status(
        self,
        challenge='xxx',
    ):
        """
            Poll the server for the status header and apply to the class
            attribute of 'status'. This same header also provides current
            player and bot data which is stored on the class attribute of
            'player'

            Returns: None
        """

        # The Quake style queries to end clients (whether they be Master Servers
        # or server clients), need a header of 4 \xFF bytes

        prefix = b"\xFF\xFF\xFF\xFF"
        command = bytes(
            'getstatus ' + challenge,
            encoding='utf-8'
        )

        self.sock.sendto(prefix + command, self.server)

        try:
            data, _ = self.sock.recvfrom(4096)
        except socket.timeout:
            return

        # The response will include a 4 byte header that we need to ignore.
        # Then we want to split on new line characters and '\\'. This will
        # create a list that always has a blank first element so we slice it off
        status_list = data[4:].split(b'\n')[1].split(b'\\')[1:]
        player_list = data[4:].split(b'\n')[2:-1]

        element = zip(status_list[::2], status_list[1::2])

        for el in element:
            self.status[el[0].decode('utf-8')] = el[1].decode('utf-8')

        for player in player_list:
            player_parse = player.decode('utf-8').split(" ")
            self.players[player_parse[2].strip("\"")] = {
                'frags': player_parse[0],
                'ping': player_parse[1]
            }