from ast import Pass
import socket
import specart_cli
import threading

class Player(object):
    def __init__(self, username, initGoods, initMoney, soc:socket.socket):
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

class Com:
    def __init__(self, mode, player:Player):
        '''
        mode (integer): 0 (consle), 1 (GUI)
        '''
        self.mode = mode
        self.soc = socket.socket()
        self.player = player

    def connect(self, host, port = 7733):
        self.player.soc.connect((host, port))
        thread = threading.Thread(target=self.soc_recv, name='socRecvThread')
        thread.start()
        self.soc.sendall(f'name {self.player.username}#'.encode('utf8'))
      
    def output(self , type, content):
        if self.mode == 0:
            # Console mode
            specart_cli.command_handle(content)
        elif self.mode == 1:
            # GUI mode
            pass

    def send_cmd(self, cmd):
        if cmd[0] == 'sell':
            self.player.sell(int(cmd[1]), int(cmd[2]))
        elif cmd[0] == 'buy':
            self.player.buy(int(cmd[1]), int(cmd[2]))
        elif cmd[0] == 'backsell':
            self.player.backsell(cmd[1], cmd[2], cmd[3])
        elif cmd[0] == 'backbuy':
            self.player.backbuy(cmd[1], cmd[2], cmd[3])

    def soc_recv(self):
        while True:
            buff = self.player.soc.recv(1024).decode('utf8')
            command = buff.split('#')
            for i in command[:]:                    #去除空指令
                if not i:
                    command.remove(i)
            for item in command:
                out = item.strip().split()
                self.output(out)