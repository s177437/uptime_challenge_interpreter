import Pyro4
class pyroServer() :
    def returnHello(self, name):
        return "hello, this is from server ", name
daemon = Pyro4.Daemon()
ns=Pyro4.locateNS()
uri = daemon.register(pyroServer)
ns.register("testserver", uri)


print "Ready"
daemon.requestLoop()

