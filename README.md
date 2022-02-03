# SpecArt(English)
A tactical game about transaction and speculation.

## Introduction
In this game, players are connected by the central server, and allocated **equal money and goods**. The same as the **continuous auction transaction** rules of a stock market or a futures market, you can pend buying and selling orders on the server, and then the server will process the order queue and decide which pair to deal. Noticed that the number of your money and goods have changed, your goal is to gain **60% money of all** the players and win the game. 

## Requirements
* 3.5 <= Python 3 <= 3.8.
* A server with TCP/IP network.
* Clients as players able to connect to the server.

## Server Operations
* Allow the `7733` port on the firewall.
* Run file `server/run_server.cmd`(Windows) or `server/run_server.sh`(Linux) and wait for connections from clients(players).
* After all the players in, type `b` and press Enter to begin the game.

## Client Operations (Console)
* Run file `client/run_cli.cmd`(Windows) or `client/run_cli.sh`(Linux).
* Set a unique name for each player.
* Type the address of the server.
* Wait for the signal of beginning from the server.
* Follow the hints and enjoy it!

## Client Operations (GUI)
* Run file `client/run_gui.cmd`(Windows) or `client/run_gui.sh`(Linux).
* ~~Learn by "Local Teaching" method.~~
* Choose "Online Play" to begin the game.
* Set a unique name for each player, type the address of the server, click "Login" botton.
* Wait for the signal of beginning from the server.
* Follow the hints and enjoy it!

## Attention
* **No Space** in player's name.
* Players **CANNOT** have the same name.
* Players **CANNOT** quit the game while playing.
* New player **CANNOT** join the game after game beginning.
* There are some problems quitting the game, so just **click ×** on the window to force to quit.
* Possible thread safety problems.

# SpecArt(简体中文)
这是一个关于交易和投机的策略性游戏。

## 简介
在这个游戏里，玩家们通过一个中心服务器相连，被分配以**等量的钱和物资**。和股票以及期货市场里的**连续竞价**交易规则一样，你可以在服务器上挂买卖单，然后服务器将会处理订单队列并且决定那一对订单成交。注意到此时你的钱和物资数量将会发生变化，而你的目的则是得到**所有玩家60%的钱**来赢得这场游戏。

## 配置要求
* 3.5 <= Python 3 <= 3.8。
* 带有TCP/IP网络的服务器。
* 能连接到服务器的玩家客户端。

## 服务器操作
* 开放防火墙`7733`端口。
* 运行文件`server/specart_ser.py`并等待客户端（玩家）连接。
* 当所有玩家连接后，输入`b`并回车来开始游戏。

## 客户端操作（命令行）
* 运行文件 `client/run_cli.cmd`(Windows) 或者 `client/run_cli.sh`(Linux).
* 为玩家设置一个唯一的用户名。
* 输入服务器地址。
* 等待服务器的开始信号。
* 根据提示游戏，玩得愉快！

## 客户端操作（图形界面）
* 运行文件 `client/run_gui.cmd`(Windows) 或者 `client/run_gui.sh`(Linux).
* ~~通过“单机教学”模式进行学习。~~
* 选择“局域网联机”模式开始游戏。
* 为玩家设置一个唯一的用户名，输入服务器的地址，点击“登录”。
* 等待服务器的开始信号。
* 根据提示游戏，玩得愉快！

## 注意
* 玩家的用户名**不应该有空格**。
* 玩家**不能**有相同的用户名。
* 在游戏中玩家**不能**退出游戏。
* 新玩家在游戏开始后**不能**加入游戏。
* 退出游戏时候会有一些问题，所以直接**点击窗口上的×**来强制退出游戏。
* 可能存在线程安全问题。
