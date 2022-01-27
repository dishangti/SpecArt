from ast import Pass
import socket
import threading

class Player(object):
    def __init__(self):
        '''
        username:用户名
        initGoods:初始物资
        initMoney:初始资金
        soc:使用的socket对象
        '''

        self.username = ""
        self.goods = 0
        self.money = 0
        self.transaction = {}       #keys:挂单时间 values:指令按空格切分后的列表

class Com:
    def __init__(self, mode):
        '''
        mode (integer): 0 (consle), 1 (GUI)
        '''
        self.mode = mode
        self.soc = socket.socket()
        self.player = Player()
        self.initGoods = 0
        self.initMoney = 0

    def connect(self, host, port = 7733):
        self.soc.connect((host, port))
        thread = threading.Thread(target=self.soc_recv, name='socRecvThread')
        thread.start()
        self.soc.sendall(f'name {self.player.username}#'.encode('utf8'))

    def output(self, content):
        if self.mode == 0:
            # Console mode
            self.CON_display(content)
        elif self.mode == 1:
            self.GUI_fresh()

    def CON_display(self, content):
        pass

    def GUI_fresh(self):     # 于GUI中实现显示
        pass

    def send_cmd(self, cmd):
        if type(cmd) == str:
            cmd = cmd.strip().split()
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