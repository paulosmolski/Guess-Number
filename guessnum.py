from random import randint 
from datetime import datetime, timedelta
import re
from functools import reduce
from operator import add
import click

class FoundException(Exception):
    pass

class Guess:
    def __init__(self, minnum, maxnum):
        self.number = randint(minnum, maxnum)
        self.count = 0
        self.time = datetime.now()
        self.timetaken = timedelta(0)
        self.isfound = False
    def guess(self, number):
        if self.isfound:
            raise FoundException("Numer został już odnaleziony")
        self.count += 1
        self.timetaken = datetime.now() - self.time
        if number == self.number:
            self.isfound = True
            print(f"Gratulacje. Numer to {self.number}, a ty zgadłeś go za {self.count} razem")
        elif number < self.number:
            print(f"Niestety nie zgadłeś. Szukany numer jest większy. Liczba podejść: {self.count}")
        else:
            print(f"Niestety nie zgadłeś. Szukany numer jest mniejszy. Liczba podejść: {self.count}")
    def __lt__(self, other):
        if self.isfound == True and other.isfound == False:
            return True
        elif self.isfound == False and other.isfound == True:   
            return False
        elif self.count != other.count:
            return self.count < other.count    
        else:
            return self.timetaken < other.timetaken
    def __repr__(self):
        a = self.time.strftime("%H:%M:%S")
        return f"liczba podejść: {self.count:3} | Znaleziona liczba: {self.number:4} | Godzina: {a} | Czas: {self.timetaken}"

@click.command()
@click.option('--minnum', default=0, help="Najmniejsza możliwa liczba")
@click.option('--maxnum', default=150, help="Największa możliwa liczba")
def game(minnum, maxnum):
    """
    Gra polegająca na jak najszybszym zgadnięciu dowolnej liczby
    """
    scores = []
    while True:
        action = input("Wpisz co chcesz zrobić: Gra, Wyniki, Stop\n")
        if re.match("Gra", action, re.IGNORECASE):
            game = Guess(minnum, maxnum)
            while True:
                if not game.isfound:
                    g = input(f"Podaj liczbę w przedziale {minnum}-{maxnum}\n")
                    while not g.isdigit():
                        g = input("Niepoprawna liczba. Podaj inną\n")
                    g = int(g)
                    game.guess(g)
                else:
                    scores.append(game)
                    scores.sort()
                    break
        elif re.match("Wyniki?", action, re.IGNORECASE):
            if scores:
                gamesum = len(scores)
                countsum = sum(x.count for x in scores)
                timesum = reduce(add, (x.timetaken for x in scores))
                countavrg = countsum/gamesum
                timeavrg = timesum / gamesum
                for x in scores:
                    ind = scores.index(x) + 1
                    print(f"{ind:3}. {x}")
                print("-"*60)
                print(f"Ilość gier: {gamesum}, czas łącznie: {timesum}, próby łącznie: {countsum}, czas średnio: {timeavrg}, próby średnio: {countavrg}")
            else:
                print("Póki co nie rozegrałeś żadnej gry")
        elif re.match("Stop|Koniec", action, re.IGNORECASE):
            print("Dziękujemy za grę")
            break
        else:
            print("Niewłaściwy wybór")
            continue

if __name__ == "__main__":
    game()
