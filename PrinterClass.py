class Printer:
    from printrun.pronsole import pronsole

    def __init__(self):
        print("...Instantiating Printer object")

        # Creates object from pronsole class
        self.pronsoleObject = self.connectedpronsole() 
        self.connected = False
        self.running = False
        self.connect()
    
    def connect(self):
        try:
            self.pronsoleObject.do_connect("")
            self.connected = True
        except:
            print("Error connecting to printer")
    
    def isConnected(self):
        return self.connected

    def getETA(self):
        # Returns (secondsremain, secondsestimate, progress)
        print("...Running getETA method")
    
        # Calls get_eta method in pronsoleObject, initiated above
        result = self.pronsoleObject.get_eta()
        if result == (1, 1, 0):
            print("Not printing")
            eta = 1000000
        else:
            print("ETA = ", eta, " seconds")
            eta = result[0]

        self.disconnect()
        return eta

    def recursive_getETA(self, ETA_secondsLimit, iteration, iterationLimit, delay):
        print("...Running recursive getETA method, iteration # =", iteration)
        # Calls get_eta method in pronsoleObject, initiated above

        for i in range(iteration, iterationLimit+1):
            if (i < iterationLimit):
                eta = self.getETA()
                print(eta)
                if (eta >= ETA_secondsLimit): # Printer is still running
                    state = False
                else: # Print ETA is lower than set threshold, nearing completion
                    print("ETA threshold of ", ETA_secondsLimit, "has been crossed")
                    state = True
                time.sleep(delay) # Waits X second
                iteration += 1 
            else:
                print("Max iteration = ", iterationLimit, "has been reached")
                state = False
        return eta
        
    def disconnect(self):
        print("...Disconnecting")
        self.pronsoleObject.do_disconnect("")
