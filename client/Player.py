#import socket

class Player(object):
    def __init__(self, username, initGoods, initMoney, soc):
        '''
        username:用户名
        initGoods:初始物资
        initMoney:初始资金
        soc:使用的socket对象
        '''

        self.username = username
        self.goods = initGoods
        self.money = initMoney
        self.soc = soc
        self.transaction = {}       #keys:挂单时间 values:指令按空格切分后的列表

    # def sendMessage(self, port):
    #     '''
    #     port:端口
    #     '''

    #     soc = socket.socket()
    #     host = socket.gethostname()

    #     soc.connect((host, port))
    #     print(soc.recv(1024))
    #     soc.close()

    def sell(self, num, price):
        '''
        num:数量
        price:单价
        '''
        
        if self.goods >= num:
            command = f'sell {num} {price}#'
            self.soc.sendall(command.encode('utf8'))
        else:
            print('no enough goods')

    def buy(self, num, price):
        '''
        num:数量
        price:单价
        '''

        if self.money >= num * price:
            command = f'buy {num} {price}#'
            self.soc.sendall(command.encode('utf8'))
        else:
            print('no enough money')

    def backsell(self, num, price, time):
        '''
        撤回指定num、price、time的卖单
        '''

        command = f'backsell {num} {price} {time}#'
        self.soc.sendall(command.encode('utf8'))
    
    def backbuy(self, num, price, time):
        '''
        撤回指定num、price、time的买单
        '''

        command = f'backbuy {num} {price} {time}#'
        self.soc.sendall(command.encode('utf8'))

    def Myaccount(self):
        '''
        查看个人账户
        '''

        print(f'Current Money:{self.money}\nCurrent Goods:{self.goods}')

    def Mytransaction(self):
        '''
        查看个人在途交易
        self.transaction的values是指令按空格切分后的列表
        '''
        
        print(tuple(map(' '.join, self.transaction.values())))
