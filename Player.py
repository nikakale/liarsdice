from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade import message
from spade.message import Message
from random import *
import time

class Player(Agent): 
    class GameBehaviour(FSMBehaviour):
        async def on_start(self):
            print(f"{self.agent.name}: Ulazim u igru!")

        async def on_end(self):
            print(f"{self.agent.name}: Izlazim iz igre!")

    class FirstBet(State):
        async def run(self):            

            if self.agent.previousState == "1stBet":
                msg = Message(to=self.agent.sendTo, body = "alive")
                await self.send(msg)
                self.agent.dealDice()
                self.agent.printHand()
                self.agent.previousState = "ReBet"
                self.set_next_state("ReBet")
               
            else:
                msg = await self.receive(timeout=120)
                self.agent.dealDice()
                self.agent.printHand()

                if self.agent.doubles() == 0:
                    n = randint(1,int(ukk/2))
                    xi = randint(1,6)
                    msg = Message(to=self.agent.sendTo, body=str(self.agent.psi)+str(n)+str(xi))
                    print(f"\n{self.agent.name}: Misli da postoje {msg.body[1]} x {msg.body[2]}")
                    self.agent.lastBet = str(n)+str(xi)
                else:
                    n = self.agent.doubles()[0]
                    xi = self.agent.doubles()[1]
                    msg = Message(to=self.agent.sendTo, body=str(self.agent.psi)+str(n)+str(xi))
                    print(f"\n{self.agent.name}: Misli da postoje {msg.body[1]} x {msg.body[2]}")
                    self.agent.lastBet = str(n)+str(xi)
                await self.send(msg)
                self.set_next_state("ReBet")


    class ReBet(State):
        async def run(self):
            msg = await self.receive(timeout=120)

            if msg.body == "LS8":
                string = ""
                for k in self.agent.hand:
                    string = string + str(k)                
                msg = Message(to=self.agent.sendTo, body=str(self.agent.lastBet)+str(string))
                await self.send(msg)
                self.set_next_state("LS")

            else:
                if int(msg.body[0]) == 0:
                    print(f"{self.agent.name}: Pobjeda woohoo!")
                    await self.agent.stop()

                else:
                    b = randint(1,2)
                    if b==1:
                        print(f"\n{self.agent.name} će ponovno pogađati!")
                        a = randint(1,2)
                        if a == 1:
                            if(int(msg.body[1])<=5):
                                n = int(msg.body[1])+1
                            else:
                                n = 1
                            xi = int(msg.body[2])
                        else:
                            if int(msg.body[2]) < 6:
                                if(int(msg.body[1])<=5):
                                    n = int(msg.body[1])+1
                                else:
                                    n = 1
                                xi = int(msg.body[2])+1
                            else:
                                if(int(msg.body[1])<=5):
                                    n = int(msg.body[1])+1
                                else:
                                    n = 1
                                xi = 1
                        msg = Message(to=self.agent.sendTo, body=str(self.agent.psi)+str(n)+str(xi))
                        self.agent.lastBet = str(n)+str(xi)
                        print(f"{self.agent.name}: Misli da postoje {msg.body[1]} x {msg.body[2]}")
                        time.sleep(2)
                        await self.send(msg)
                        self.set_next_state("ReBet")
                    if b==2:
                        print(f"\n{self.agent.name}: Prihvaća izazov!")
                        msg = Message(to=self.agent.sendTo, body="LS8")
                        time.sleep(2)
                        await self.send(msg)
                        self.set_next_state("LS")

    class LiarSpot(State):
        async def run(self):
            msg = await self.receive(timeout=120)
            
            if msg.body != "welcome":
                
                await self.send(Message(to=self.agent.sendTo, body="welcome"))

                c = randint(1,2)
                nn = int(msg.body[0])
                xxi = int(msg.body[1])
                table = []
                table = self.agent.hand
                for l in range(len(msg.body)-2):
                    table.append(int(msg.body[2+l]))
                print("\nSve kockice na stolu su {}".format(table))
                
                if c == 1:
                    print(f"\n{self.agent.name}: Misli da {self.agent.sendTo} laže!")

                    if nn > self.agent.checkTable(table, xxi):
                        print(f"{self.agent.name}: Pogodak!\n")
                        await self.send(Message(to=self.agent.sendTo, body="youLose"))
                        self.agent.previousState = "1stBet"
                        self.set_next_state("1stBet")

                    else:
                        await self.send(Message(to=self.agent.sendTo, body="youWin"))
                        print(f"{self.agent.name}: Joj, krivo!\n")
                        self.agent.psi = self.agent.psi - 1
                        self.agent.previousState = "LS"
                        self.set_next_state("1stBet")
                        
                else:
                    print(f"\n{self.agent.name}: Misli da je {self.agent.sendTo} u pravu!")

                    if nn <= self.agent.checkTable(table, xxi):
                        await self.send(Message(to=self.agent.sendTo, body="youLose"))
                        print(f"{self.agent.name}: Pogodak!\n")
                        self.agent.previousState = "1stBet"
                        self.set_next_state("1stBet")

                    else:
                        await self.send(Message(to=self.agent.sendTo, body="youWin"))
                        self.agent.psi = self.agent.psi - 1
                        self.agent.previousState = "LS"
                        self.set_next_state("1stBet")
                        print(f"{self.agent.name}: Joj, krivo!\n")

            if msg.body == "welcome": 
                msg = await self.receive(timeout=120)
                if msg.body == "youLose":
                    print(f"\n{self.agent.name}: Joj! Sad gubim kockicu.")
                    self.agent.psi = self.agent.psi - 1
                    self.agent.previousState = "LS"
                    self.set_next_state("1stBet")
                    
                if msg.body == "youWin":
                    print(f"{self.agent.name}: To! sad {self.agent.sendTo} gubi kockicu!\n")
                    self.agent.previousState = "1stBet"
                    self.set_next_state("1stBet")

    async def setup(self):
        fsm = self.GameBehaviour()
        fsm.add_state(name="1stBet", state=self.FirstBet(), initial=True)
        fsm.add_state(name="ReBet", state=self.ReBet())
        fsm.add_state(name="LS", state=self.LiarSpot())

        fsm.add_transition(source="1stBet", dest="ReBet")
        fsm.add_transition(source="ReBet", dest="ReBet")
        fsm.add_transition(source="ReBet", dest="LS")
        fsm.add_transition(source="LS", dest="1stBet")

        self.add_behaviour(fsm)

    def __init__(self, jid, password, goesFirst, sendTo):
        super().__init__(jid, password)
        self.hand = []
        self.psi = 5
        self.sendTo = sendTo
        self.previousState = "LS" if goesFirst else "1stBet" #ako je LS igra prvi a ako je 1stBet drugi
        
    def printHand(self):
        print(f"{self.name}: U ruci imam: {self.hand}")

    def doubles(self): 
        maxnum = 0
        num = 0
        for i in range(6):
            n = 0
            for j in self.hand:
                if j == (i+1):
                    n = n+1
            if n>num:
                maxnum = i+1
                num = n
        return num, maxnum

    def checkTable(self, table, guess):
        n = 0
        for i in table:
            if guess == i:
                n = n+1
        return n

    def dealDice(self):
        self.hand = []
        for x in range(self.psi):
            c = randint(1,6)
            self.hand.append(c)
