from functools import cached_property
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from urllib.parse import parse_qsl

curr_uid = 0
players = []

class Player:
    def __init__(self):
        self._pos = (0, 0)

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos):
        self._pos = pos

class GameRequestHandler(BaseHTTPRequestHandler):
    @cached_property
    def form_data(self):    
        content_length = int(self.headers.get('Content-Length', 0))
        return dict(parse_qsl(self.rfile.read(content_length).decode()))

    def do_GET(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        global curr_uid
        global players
        if self.form_data.get('action') == 'new_player':
            
            self.send_response(200)
            self.end_headers()

            out = str(curr_uid) + '\n'
            for i, p in enumerate(players):
                out += f"{i}\n{p.pos[0]}\n{p.pos[1]}\n"
            self.wfile.write(out.encode())

            curr_uid += 1

            p = Player()
            players.append(p)
            print(f"created new player; number of players={len(players)}")

        elif self.form_data.get('action') == 'update':
            uid = int(self.form_data['uid'])
            x = int(self.form_data['x'])
            y = int(self.form_data['y'])
            players[uid].pos = (x, y)

            out = ""
            for i, p in enumerate(players):
                out += f"{i}\n{p.pos[0]}\n{p.pos[1]}\n"

            self.send_response(200)
            self.end_headers()
            self.wfile.write(out.encode())
        else:
            print(self.form_data)
            self.send_error(404)


if __name__ == "__main__":
    server = HTTPServer(('', 8000), GameRequestHandler)
    server.serve_forever()