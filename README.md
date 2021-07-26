# SpecArt
A tactical game about transaction and speculation.

## Introduction
In this game, players are connected by the central server, and allocated **equal money and goods**. The same as the **continuous auction transaction** rules of a stock market or a futures market, you can pend buying and selling orders on the server, and then the server will process the order queue and decide which pair to deal. Noticed that the number of your money and goods have changed, your goal is to gain **60% money of all** the players and win the game. 

## Requirements
* Python 3.
* A server with network.
* Clients as players able to connect to the server.

## Server Operation
* Allow the 7733 port on the firewall.
* Open the file `server/specart_ser.py` and wait for connections from clients (players).
* After all the players in, type `b` and press `Enter` to begin the game.

## Client Operation
* Set a unique name for each player.
* Type the address of the server.
* Wait for the signal of beginning.
* Enjoy it!

## Attention
* Players CANNOT have the same name.
* Players CANNOT quit the game while playing.
* New player CANNOT join the game after game beginning.
* There are some problems quitting the game, so just click × on the window to force to quit.
