from twisted.internet import reactor, protocol


class Client(protocol.DatagramProtocol):
    def __init__(self):
        super(Client, self).__init__()
        self.server = None
        self.usr_addr = None

    def startProtocol(self):
        print("Client started")

        self.server = ("127.0.0.1", 1000)
        self.send_data("Hello Server from client", self.server)
        reactor.callInThread(self.send_message)

    def choose_client(self):
        self.usr_addr = input("Write the address:"), int(input("Write the port:"))

    def datagramReceived(self, datagram, addr):
        datagram = datagram.decode("utf-8")

        if addr == self.server:
            print("Server says: " + datagram)

        print(f"User {addr} says: " + datagram)

    def send_data(self, data: str, addr):
        self.transport.write(data.encode("utf-8"), addr)

    def send_message(self):
        while True:
            message = input("Enter message: ")

            if message == "choose_client":
                self.choose_client()
                continue

            self.send_data(message, self.usr_addr)


if __name__ == "__main__":
    port = int(input("Write the port:"))
    reactor.listenUDP(port, Client())
    reactor.run()
