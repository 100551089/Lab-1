# Design of Telematics Systems 2025-26
# Universidad Carlos III de Madrid
#
# Ship with no interaction with the captain, moving randomly
# This program handles the ship's movement and interactions with the map
#
# The program receives as parameters:
# - The map file path (by default map.txt)
# --pos x0 y0 The ship's initial position (x0, y0)
# --food <amount> The amount of food the ship has
# How to move the ship: 
# --random N s1: move the ship randomly N steps, with a speed of s1 seconds between movements
# --captain: follow the captain's orders
# --captain and --random cannot be used together
#
# This version implements only the random movement
# The ship will try to move randomly N steps, while there is enough food
#
# All its messages are printed to stderr
#

import os
import time
from map import Map
import argparse, sys
import random

class Ship:
    DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    def __init__(self, mapa, pos, food):
        self.mapa = mapa
        self.pos = pos
        self.mapa.set_ship(self.pos[0], self.pos[1])
        self.food = food
        self.gold = 0
        self.pid = os.getpid()

    def __str__(self):
        return f"Ship {self.pid} at {self.pos} with {self.food} food and {self.gold} gold."

    def get_position(self):
        return self.pos

    def move_randomly(self):
        if self.food < 5:
            print("Not enough food to move.", file=sys.stderr)
            return
        dx, dy = random.choice(Ship.DIRECTIONS)
        if self.mapa.can_sail(self.pos[0] + dx, self.pos[1] + dy):
            self.mapa.remove_ship(self.pos[0], self.pos[1])
            self.pos = (self.pos[0] + dx, self.pos[1] + dy)
            self.mapa.set_ship(self.pos[0], self.pos[1])
            self.food -= 5
            where = self.mapa.get_cell_type(self.pos[0], self.pos[1])
            if where == Map.BAR:
                self.gold += 10
                print(f"Ship {self.pid} reached an island {self.pos}, gold increased to {self.gold}.", file=sys.stderr)
            elif where == Map.HOME:
                self.food += 20
                print(f"Ship {self.pid} reached a port {self.pos}, food increased to {self.food}.", file=sys.stderr)
        
    def move_captain(self):
        # TO BE IMPLEMENTED in the following steps
        valid = False
        while valid != True:
            direction = input("Direction: ")
            if direction == "up" and self.mapa.can_sail():
                self.pos = (self.pos[0], self.pos[1] + 1)
                valid = True
            elif direction == "down":
                self.pos = (self.pos[0], self.pos[1] - 1)
                valid = True
            elif direction == "left":
                self.pos = (self.pos[0] - 1, self.pos[1])
                valid = True
            elif direction == "right":
                self.pos = (self.pos[0] + 1, self.pos[1])
                valid = True
            elif direction == "exit":
                ffff
                valid = True
            else:
                print("Invalid input")



        pass

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description='Pirate Ship')
    ap.add_argument("--map", type=str, default="map.txt", help="Path to the map file, by default map.txt")
    ap.add_argument("--pos", type=int, nargs=2, metavar=("x", "y"), default=(0, 0), help="Initial position of the ship (x, y), by default (0, 0)")
    ap.add_argument("--food", type=int, default=100, help="Amount of food the ship has")
    ap.add_argument("--random", type=int, nargs=2, metavar=("N", "s1"), help="Move the ship randomly N steps, with a speed of s1 seconds between movements")
    ap.add_argument("--captain", action="store_true", help="Follow the captain's orders")
    args = ap.parse_args()

    if args.random is None:
        sys.exit("Must specify --random N to move the ship randomly.")
    if args.captain and args.random:
        sys.exit("Cannot use --captain and --random together. Choose one.")

    mapa = Map(args.map)
    if mapa.can_sail(args.pos[0], args.pos[1]):
        ship = Ship(mapa, args.pos, args.food)
    else:
        sys.exit("Invalid initial position.")

    # It should print its PID to stderr
    print(f"Ship PID: {os.getpid()}", file=sys.stderr)
    if args.captain:
        ship.move_captain()
    else:
        for _ in range(args.random[0]):
            # waits args.random[1] seconds
            time.sleep(args.random[1])
            ship.move_randomly()
            print(ship)
            #print(mapa)
    print(f"Ship {ship.pid} has finished with status {ship.gold}.", file=sys.stderr)
    sys.exit(ship.gold)


   

