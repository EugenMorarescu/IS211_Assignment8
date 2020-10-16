import random
import argparse
import sys
import time

class Player:
    def __init__(self,name):
        self.name=name
        self.hold=False
        self.roll=True
        self.turn=False
        self.total_score=0
        
class ComputerPlayer(Player):

    def r_or_h(self,temp_score):
        
        diff_score = 100 - self.total_score
        
        if (diff_score) < 25:
            ans = diff_score
        else:
            ans = 25
        
        if temp_score >= ans:
            self.hold = True
            self.roll=False
            return('hold')
            
        else:
            self.hold=False
            self.roll = True
            return('roll')  
                

class HumanPlayer(Player):

    def r_or_h(self):
        ans = input("{} do you want to Roll ('r') or Hold ('h')? ".format(self.name))
        ans = ans.lower()
        
        if ans == 'r':
            self.hold=False
            self.roll = True
            return('roll')
            
        
        if ans =='h':
            self.hold = True
            self.roll=False
            return('hold')
            
        else:
            print('Wrong input, try again please')
              
class PlayerFactory:
    
    def comp_or_hum(self,name):
        if name.lower() == 'computer':
            return ComputerPlayer(name)
        else:
            return HumanPlayer(name)

            
class Die:
    def __init__(self):
        self.num=0

    def roll(self):
        self.num = random.randint(1,6)
        return self.num
    
class Game():
    def __init__(self,player1,player2):
        factory = PlayerFactory()
        self.player1=factory.comp_or_hum(player1)
        self.player2=factory.comp_or_hum(player2)
        if self.player1 == 'computer' and self.player2 == 'computer':
            self.player2.name = 'computer 2'
        self.die=Die()
        self.temp_score=0
        
        self.current=self.player1
        print(self.current.name + ' Starts!')

        self.go()
        
    def go(self):
        roll_score = self.die.roll()
        if (roll_score == 1):
            self.temp_score = 0
            print("\n{} rolled a {}, no points for you!\nYour current turn score is {}\nYour total score is {}".format(self.current.name,roll_score,self.temp_score,self.current.total_score))
            self.scores()
            
               
        else:
            self.temp_score+=roll_score
            print("\n{} rolled a {}\nYour current turn score is {}\nYour total score is {}".format(self.current.name,roll_score,self.temp_score,self.current.total_score))
            self.choice()
            
            
    def scores(self):
        self.temp_score=0

        if self.current.total_score >=100:
            print("GAME OVER, {} wins with {} points!".format(self.current.name,self.current.total_score))
            sys.exit()
        
        else:
            if self.current==self.player1:
                self.current=self.player2
                self.go()
                
            else:
                self.current=self.player1
                self.go()
                    
    def choice(self):
        
        if self.current.name.lower() == 'computer' or self.current.name.lower() == 'computer 1' or self.current.name.lower() == 'computer 2':
            result = self.current.r_or_h(self.temp_score)
        else:
            result = self.current.r_or_h()
        
        if result == 'roll':
            self.go()
        elif result == 'hold':
            self.current.total_score+=self.temp_score
            self.scores()
        else:
            self.proxy.timed(self.player1,self.player2)
            self.choice()
            
class TimedGame(Game):
    def __init__(self,player1,player2):
        factory = PlayerFactory()
        self.player1=factory.comp_or_hum(player1)
        self.player2=factory.comp_or_hum(player2)
        if (self.player1.name == 'computer') and (self.player2.name == 'computer'):
            self.player1.name = 'computer 1'
            self.player2.name = 'computer 2'
        self.die=Die()
        self.temp_score=0
        self.proxy=TimedGameProxy()
        
        self.current=self.player1
        print(self.current.name + ' Starts!')

        self.go()
        
    def go(self):
        self.proxy.timed(self.player1,self.player2)
        roll_score = self.die.roll()
        if (roll_score == 1):
            self.temp_score = 0
            print("\n{} rolled a {}, no points for you!\nYour current turn score is {}\nYour total score is {}".format(self.current.name,roll_score,self.temp_score,self.current.total_score))
            self.scores()
               
        else:
            self.temp_score+=roll_score
            print("\n{} rolled a {}\nYour current turn score is {}\nYour total score is {}".format(self.current.name,roll_score,self.temp_score,self.current.total_score))
            self.choice()

class TimedGameProxy(Game):
    
    def __init__(self):
        self.start = time.time()
        self.end = self.start + 60

    def timed(self,player1,player2):
        
        if time.time() <= self.end:
            time_left=(self.end - time.time())
            print("\n{} seconds left".format(round(time_left)))
            
            
        else:
            if player1.total_score > player2.total_score:
                current = player1
                print("Times up! {} wins with {} points!".format(current.name,current.total_score))
            elif player2.total_score > player1.total_score:
                current = player2
                print("Times up! {} wins with {} points!".format(current.name,current.total_score))
            elif player1.total_score == player2.total_score:
                print("TIE GAME!!")
            sys.exit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Number of players')
    parser.add_argument("--player1",type=str)
    parser.add_argument("--player2",type=str)
    parser.add_argument("--timed",type=str)
    args = parser.parse_args()
        
    if args.timed =='on':
        TimedGame(args.player1,args.player2)
    else:
        Game(args.player1,args.player2)
        
         

   

