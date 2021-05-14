import base
import player  #student's player

"""
This program is a simplified version of the Gemblo game between two players.
The game is simplified by assumptions:
a) all players return valid stones that point to board 
b) no error occurs when calling .move
c) rules of the games are NOT checked here

The points a-c are however checked by Brute.

"""



size = 11

stones = base.loadStones("stones.txt")

p1 = player.Player(1, size, stones)  #player no. 1
p2 = player.Player(-1, size, stones) #player no -1

iteration = 0
while True:
    
    move1 = p1.move()  #move1 should be a list of stones or [] if no stone can be placed

    base.updatePlayers(p2, move1, p1.player)  #write stones to board of both players
    base.updatePlayers(p1, move1, p1.player)  

    p1.saveImage("{}-a.png".format(iteration))


    move2 = p2.move()

    base.updatePlayers(p1, move2, p2.player)  #write stones to board of both players
    base.updatePlayers(p2, move2, p2.player)  
    
    p2.saveImage("{}-b.png".format(iteration))
    iteration+=1


    if len(move1) == 0 and len(move2) == 0:
        print("End of game, both players return [] ")
        break
    
