# SpecArt
A tactical game about transaction and speculation.

## Introduction
In this game, players are connected by the central server, and allocated **equal money and goods**. The same as the **continuous auction transaction** rules of a stock market or a futures market, you can pend buying and selling orders on the server, and then the server will process the order queue and decide which pair to deal. Noticed that the number of your money and goods have changed, your goal is to gain **60% money of all** the players and win the game. 

## Requirements
* Python 3.
* A server with network.
* Clients as players able to connect to the server.

## Server Operations
* Allow the 7733 port on the firewall.
* Open the file `server/specart_ser.py` and wait for connections from clients (players).
* After all the players in, type `b` and press `Enter` to begin the game.

## Client Operations
* Set a unique name for each player.
* Type the address of the server.
* Wait for the signal of beginning.
* Follow the hints and enjoy it!

## Attention
* **No Space** in user name.
* Players **CANNOT** have the same name.
* Players **CANNOT** quit the game while playing.
* New player **CANNOT** join the game after game beginning.
* There are some problems quitting the game, so just **click ×** on the window to force to quit.
<<<<<<< HEAD

# SpecArt
这是一个关于交易和投机的策略性游戏。

## 简介
在这个游戏里，玩家们通过一个中心服务器相连，被分配以*等量的钱和物资*。和股票以及期货市场里的*连续竞价*交易规则一样，你可以在服务器上挂买卖单，然后服务器将会处理订单队列并且决定那一对订单成交。注意到此时你的钱和物资数量将会发生变化，而你的目的则是得到*所有玩家60 %的钱*来赢得这场游戏。
=======
* This version has potentional thread security problem.
>>>>>>> 6b5b8b1f0bb8e48fda0e3430513e8ca1630e6bb4
