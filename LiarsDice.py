import Player
import random
import spade
import time


    
        
def InitializeGame(player1, player2):
    
    print(
        '''
 
      __       _______    __       ____    _____  
     / /|     /__  __/|  /  |     / _  \  /  __/|
    / / /     |_/ /|_|/ /   |    / /_| |  \ \__|/ 
   / / /       / / /   / /| |   / _   /|   \ \     
  / /_/_   __ / /_/   / __  |  / / | |/ __ / /|   
 /_____/| /_______/| /_/|_|_| /_/ /|_| /____/ /   
 |_____|/ |_______|/ |_|/ |_| |_|/ |_| |____|/    
 
      ____      _______    _____    ______
     / _  \    /__  __/|  / ___/|  / ____/|
    / / | |    |_/ /|_|/ / /|__|/ / /___ |/
   / / / /|     / / /   / / /    / ____/|
  / /_/ / / __ / /_/   / /_/_   / /____|/
 /_____/ / /_______/|  |____/| /______/|
 |_____|/  |_______|/  |____|/ |______|/
''')
    
    time.sleep(1)
    print("————————————————————————————————————————————————")
    print("•••••••••••••••• ZAPOČINJE IGRA ••••••••••••••••")
    time.sleep(1)
    print("————————————————————————————————————————————————")
    print(f"•••••••••••• IGRAJU: {player1.name} i {player2.name} ••••••••••••")
    print("————————————————————————————————————————————————\n")
    time.sleep(1)

    

if __name__ == '__main__':   
    
    player1 = Player.Player("nkale@rec.foi.hr", "lozinka", True, "nkale1@rec.foi.hr")
    player2 = Player.Player("nkale1@rec.foi.hr", "lozinka1", False, "nkale@rec.foi.hr")

    InitializeGame(player1, player2)

    input("Pritisnite ENTER za početak i za kraj.\n")
    player1.start()
    animation = "|/-\\"
    idx = 0
    a = 0
    while a < 30:
        print("Učitavanje agenata",animation[idx % len(animation)], end="\r")
        idx += 1
        time.sleep(0.1)
        a = a+1
    
    player2.start()
    input("")
    player1.stop()
    player2.stop() 
    spade.quit_spade()


