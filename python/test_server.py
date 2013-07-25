import socket

import SocketServer

class MyTCPHandler(SocketServer.BaseRequestHandler):
  """
  The RequestHandler class for our server.

  It is instantiated once per connection to the server, and must
  override the handle() method to implement communication to the
  client.
  """

  def handle(self):
    # self.request is the TCP socket connected to the client
    self.data = self.request.recv(1024).strip()
    print("{} wrote:".format(self.client_address[0]))
    print(self.data)
    self.request.sendall(self.data)


def main():
  HOST, PORT = "localhost", 9999
  server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
  try:
    server.serve_forever()
  except:
    server.shutdown()
  return

########## RUN MAIN ##########
if __name__ == '__main__':
  main()