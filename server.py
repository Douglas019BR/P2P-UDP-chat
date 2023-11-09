from twisted.internet import protocol
from twisted.internet import reactor


class Server(protocol.DatagramProtocol):
    def __init__(self):
        self.users = None

    def startProtocol(self):
        self.users = set()

    def send_message(self, data: str, addr):
        self.transport.write(data.encode("utf-8"), addr)

    def datagramReceived(self, datagram, addr):
        print(datagram, addr)

        try:
            addresses = "\n".join(str(user) for user in self.users)
            self.send_message(addresses, addr)
            for user in self.users:
                self.send_message("New address connected: " + str(addr), user)
        except Exception as exc:
            print(exc)
            self.send_message("No users online", addr)
        else:
            self.users.add(addr)


if __name__ == "__main__":
    reactor.listenUDP(1000, Server())
    reactor.run()
