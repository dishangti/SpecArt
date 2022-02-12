from specart_com import Player, Com
import socket

soc = socket.socket()

def Myaccount(player:Player):
    '''
    查看个人账户
    '''
    print(f'Current Money:{player.money}\nCurrent Goods:{player.goods}')

def Mytransaction(player:Player):
    '''
    查看个人在途交易
    self.transaction的values是指令按空格切分后的列表
    '''
    print(tuple(map(' '.join, player.transaction.values())))

username = input('Hey! What\'s your name? ')
host = input('host: ')

com = Com(0)
myself = com.player
com.connect(username, host)

while com.beginTime == None:  #等待从服务器读取数据再继续主线程
    pass

print('''\nrules:
sell (num) (price)
buy (num) (price)
backsell (num) (price) (time)
backbuy (num) (price) (time)
trans
account
selling
buying\n''')       #提示操作指令

while True:
    try:
        cmd = input().split()
        if cmd[0] == 'sell':
            com.sell(int(cmd[1]), int(cmd[2]))
        elif cmd[0] == 'buy':
            com.buy(int(cmd[1]), int(cmd[2]))
        elif cmd[0] == 'backsell':
            com.backsell(cmd[1], cmd[2], cmd[3])
        elif cmd[0] == 'backbuy':
            com.backbuy(cmd[1], cmd[2], cmd[3])
        elif cmd[0] == 'trans':
            Mytransaction(myself)
        elif cmd[0] == 'account':
            Myaccount(myself)
        elif cmd[0] == 'selling':
            print(com.selling.get_order)
        elif cmd[0] == 'buying':
            print(com.buying.get_order)
        else:
            print('Invalid command!')
    except Exception as e:
        print(e)

