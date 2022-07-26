from elements.player import Player
from game import Game
from eventHandler import EventHandler

def main():
    event_handler = EventHandler()
    players = [Player("Ivo", event_handler), Player("Elrón", event_handler)]
    game = Game(players)
    game.play()

if __name__ == "__main__":
    main()

# Notes to do
# -- Players lock the lock even if they were not at turn
# -- Player now always takes the colored die throw, it should be able to refuse if it took the white one

# -- Player inputs
# -- easier inputs / game analysis to train algorithms on / monte carlo simulation
# Misschien leuk om ipv RL moeilijk te doen, gewoon ff de game tantoe vaak runnen met simpele regels voor strategieen
# En dan kijken welke het meest succesvol is (-- bv altijd hitten op < 2)