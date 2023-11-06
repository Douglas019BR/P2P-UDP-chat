from twisted.internet import reactor, protocol


class Server(protocol.DatagramProtocol):
    def __init__(self):
        self.users = {}

    def startProtocol(self):
        self.users = set()

    def send_message(self, data: str, addr):
        self.transport.write(data, addr)

    def datagramReceived(self, datagram, address):
        print(f"Received {datagram} from{address}")
        try:
            addresses = "\n".join(str(usr) for usr in self.users).enconde("utf-8")
        except Exception as exc:
            print(exc)
            self.send_message("No users online", address)
        else:
            self.send_message(addresses, address)

            for user in self.users:
                self.send_message("New address connected: " + address, user)
        finally:
            self.users.add(address)


if __name__ == "__main__":
    reactor.listenUDP(1000, Server())
    reactor.run()
