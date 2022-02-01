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

if __name__ == '__main__':
    username = input('Hey! What\'s your name? ')
    host = input('host: ')

    initGoods = None        #初始化
    initMoney = None        #初始化
    beginTime = None        #初始化
    myself = Player(username, initGoods, initMoney, soc)
    com = Com(0, myself)
    com.connect(host)

    buying = {}             #买盘，key为价格value为该价格挂单总数量
    selling = {}            #卖盘，key为价格value为该价格挂单总数量

    while initGoods == None or initMoney == None or beginTime == None:  #等待从服务器读取数据再继续主线程
        pass

    print('''\nrules:
    sell (num) (price)
    buy (num) (price)
    backsell (num) (price) (time)
    backbuy (num) (price) (time)
    transaction
    account
    selling
    buying\n''')       #提示操作指令

    while True:
        try:
            cmd = input().split()
            if cmd[0] == 'transaction':
                Mytransaction()
            elif cmd[0] == 'account':
                Myaccount()
            elif cmd[0] == 'selling':
                print(com.selling)
            elif cmd[0] == 'buying':
                print(com.buying)
            else:
                print('invalid command')
        except Exception as e:
            print(e)

