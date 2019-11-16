import time

timers = []
containers = []


class TimerContainer:
    def isTimer(self):
        return False
    def __init__(self, loopCount=1):
        self.loopCount = loopCount
        self.timers = []
        self.cindex = len(containers)
        self.timerIndex = 0
        self.currentLoop = 1
        self.nextContainer = None

    def advance(self):
        output = None
        if(self.timers[self.timerIndex]['type'] == 'container'):
            output = containers[self.timers[self.timerIndex]['index']].advance()
        if(output == None): # It's our time to shine! We get to do the advancing!
            self.timerIndex = (self.timerIndex + 1) % len(self.timers)
            print("Timer index " + str(self.timerIndex))
            if(self.timerIndex == 0):
                self.currentLoop += 1
                if(self.currentLoop > self.loopCount):
                    return None # We too are at the end of our sequence
            return self.cindex
        else:
            return output

    def getCurrentTimer(self):
        if(self.timers[self.timerIndex]["type"] == 'container'):
            return containers[self.timers[self.timerIndex]["index"]].getCurrentTimer()
        else:
            return timers[self.timers[self.timerIndex]["index"]]

    def addNextContainer(self, containerIndex):
        self.nextContainer = containerIndex

    def __str__(self):
        output = ""
        output += "Container:\nLoops: " + str(self.loopCount) + "\nContains:\n"
        for c in self.timers:
            if(c['type'] == 'container'):
                output += '\t' + str(containers[c['index']]) + '\n'
            else:
                output += '\t' + str(timers[c['index']]) + '\n'
        return output
    
    
        
    
    
            
class Timer:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration
        self.tindex = len(timers)
    def __str__(self):
        return str(self.name) + " : " + str(self.duration) + "s"
    def isTimer(self):
        return True

def printContainers():
    for i in range(len(containers)):
        print(str(i) + ": " + str(containers[i]))


def addTimer():
    print("Name the timer:")
    name = input()
    print("Duration (s):")
    dur = int(input())
    tindex = len(timers)
    timers.append(Timer(name, dur))
    return tindex


def addTimerContainer():
    tindex = addTimer()
    print("Loops (default 1):")
    loops = int(input())
    cindex = len(containers)
    containers.append(TimerContainer(loops))
    containers[cindex].timers.append({'type': 'timer', 'index': tindex})
    return cindex

def addTimerContainerToContainer():
    cindex = addTimerContainer()
    printContainers()
    print("Which container would you like to add this container to?")
    pcindex = int(input())
    containers[pcindex].timers.append({'type': 'container', 'index': cindex})


def addTimerToContainer():
    tindex = addTimer()
    printContainers()
    print("Which container would you like to add this timer to?")
    cindex = int(input())
    containers[cindex].timers.append({'type': 'timer', 'index': tindex})
    
def resetAllTimers():
    for c in containers:
        c.currentLoop = 1
    
def runIntervalTimer():
    resetAllTimers()
    print("RUNNING")
    curContainer = 0
    timr = containers[curContainer].getCurrentTimer()
    while(timr != None):
        print("Executing : " + str(timr))
        time.sleep(timr.duration)
        output = containers[curContainer].advance()
        if(output == None):
            timr = None
        else:
            curContainer = output
            timr = containers[curContainer].getCurrentTimer()
    
    
    
def mainLoop():
    while(1):
        print("Menu:")
        print("i  : initialize new top level container")
        print("at : append timer to container")
        print("c  : show containers")
        print("ac : append container to another container")
        print("t  : show timers")
        print("r  : run timer sequence\n")
        s = input()
        if(not (s in ['i', 'a', 'c', 't', 'ac', 'at', 'r'])):
            print("not a valid selection")
        else:
            if(s == 'c'):
                printContainers()
            if(s == 'i'):
                addTimerContainer()
            if(s == 'r'):
                runIntervalTimer()
            if(s == 'at'):
                addTimerToContainer()
            if(s == 'ac'):
                addTimerContainerToContainer()

                



if(__name__ == '__main__'):
    mainLoop()
        
