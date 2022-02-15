import socket
import threading
import bisect
from abc import abstractmethod
from time import localtime, ctime

class OrderQueue():
    """
    An order queue is a list of orders ordered by price.
    """

    def __init__(self, dir):
        """
        typ(int): 0(selling list in descending order), 1(buying list in ascending order).
        dir(int): 0(sell queue), 1(buy queue).
        """

        self.__ord_lst = []
        self.__dir = dir

    def add_order(self, order):
        """
        order: a tuple in (price, num)
        """

        # Bugs here

        price, num = order
        ord_lst = self.__ord_lst
        if len(ord_lst) == 0:
            ord_lst.append(order)
            return

        ord_price_lst = list(map(lambda x: x[0], self.__ord_lst))
        pos = bisect.bisect_left(ord_price_lst, order[0])
        if pos >= len(ord_lst):
            ord_lst.insert(pos, order)
        else:
            if order[0] == ord_lst[pos][0]:
                num += ord_lst[pos][1]
                ord_lst[pos] = (price, num)
            else: ord_lst.insert(pos, order)

    def del_order(self, order):
        """
        order: a tuple in (price, num)
        """

        price, num = order
        ord_lst = self.__ord_lst
        if len(ord_lst) == 0: return

        
        if self.__dir == 0:
            ord_price_lst = list(map(lambda x: -x[0], self.__ord_lst))
            ord_price_lst.reverse()
            pos = bisect.bisect_left(ord_price_lst, -order[0])
            pos = len(ord_lst) - pos - 1
        elif self.__dir == 1:
            ord_price_lst = list(map(lambda x: x[0], self.__ord_lst))
            pos = bisect.bisect_left(ord_price_lst, order[0])
        if order[0] == ord_lst[pos][0]:
            num = ord_lst[pos][1] - num
            ord_lst[pos] = (price, num)
        if ord_lst[pos][1] <= 0:
            ord_lst.pop(pos)

    def match_del(self, order):
        """
        Match and delete all the orders in the queue.
        """
        ord_lst = self.__ord_lst.copy()
        price = order[0]
        num = order[1]
        if self.__dir == 1:
            ord_lst.reverse()
        for order in ord_lst:
            if num == 0: break
            ord_price = order[0]
            ord_num = order[1]
            if ord_price != price and (self.__dir ^ (ord_price > price)): break   # Absolutely greater for selling and less for buying
            if ord_num <= num:
                num -= ord_num
                self.del_order((ord_price, ord_num))
            else:
                self.del_order((ord_price, num))
                num = 0

    def get_order(self):
        rev = self.__ord_lst.copy()
        rev.reverse()
        return rev


class Player():
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
    VERSION = "v0.2.0-beta"

    def __init__(self, mode):
        '''
        mode(integer): 0(consle), 1(GUI)
        '''
        self.mode = mode
        self.window = None
        self.soc = socket.socket()
        self.player = Player()
        self.initGoods = 0              # Inited money and goods
        self.initMoney = 0
        self.beginTime = ""
        self.totalPlayerMoney = 0      # Total money of all the players
        self.logFile = open("client.log", "w")

        # Here are varieties for GUI to fresh
        self.price = 0
        self.buying = OrderQueue(1)
        self.selling = OrderQueue(0)
        self.deal = ""
        self.playerList = []
        self.winner = ""

    def connect(self, username, host, port = 7733):
        self.player.username = username
        try:
            self.soc.connect((host, port))
        except Exception as e:
            raise e
        thread = threading.Thread(target=self.soc_recv, name='socRecvThread')
        thread.start()
        self.soc.sendall(f'name {self.player.username}#'.encode('utf8'))

    def recv_cmd_handle(self, cmd):
        '''
        cmd(list) :指令字符串按空格分割后的指令列表
        '''

        core_cmd = cmd[0]
        
        # Private commands
        if core_cmd == 'nameok':
            #nameok (name)
            # Successfully set usernamename as (name) 
            name = cmd[1]
            self.notice(f'Successfully set your name as {name}.')
            self.write_log(f'Set name as {name}.')

        elif core_cmd == 'money':
            #money (initMoney)
            # Set initial money (initMoney)
            initMoney = int(cmd[1])
            self.player.money = self.initMoney = initMoney
            self.notice(f'Initial money: {initMoney}', False)
            self.write_log(f"Set Initial money {initMoney}.")
            if self.mode == 1:
                self.window.freshStatusBar.emit()
                self.window.freshWinProcessBar.emit()

        elif core_cmd == 'goods':
            #goods (initGoods)
            # Set initial goods (initGoods)
            initGoods = int(cmd[1])
            self.player.goods = self.initGoods = initGoods
            self.notice(f'Initial goods: {initGoods}', False)
            self.write_log(f"Set Initial goods {initGoods}.")
            if self.mode == 1:
                self.window.freshStatusBar.emit()

        elif core_cmd == 'sellok':
            #sellok (num) (price) (time)
            # Successfully sold (num) goods at the price of (price) at (time)
            cmd[0] = 'sell'
            self.player.transaction[cmd[3]] = cmd
            self.player.goods -= int(cmd[1])
            self.notice(f'Successfully sold {cmd[1]} goods at the price {cmd[2]}.', False)
            self.write_log(f"Sell {num} goods at the price {price}, remain goods {self.player.goods}.")
            if self.mode == 1:
                self.window.freshSellTableWidget.emit()
                self.window.freshTransTableWidget.emit()
                self.window.freshStatusBar.emit()

        elif core_cmd == 'buyok':
            #buyok (num) (price) (time)
            # Successfully bought (num) goods at the price of (price) at (time)
            cmd[0] = 'buy'
            self.player.transaction[cmd[3]] = cmd
            self.player.money -= int(cmd[1])*int(cmd[2])
            self.notice(f'Successfully bought {cmd[1]} goods at the price {cmd[2]}.', False)
            self.write_log(f"Buy {num} goods at the price {price}, remain money {self.player.money}.")
            if self.mode == 1:
                self.window.freshTransTableWidget.emit()
                self.window.freshStatusBar.emit()
                self.window.freshWinProcessBar.emit()

        elif core_cmd == 'backsellok':
            #backsellok (num) (price) (time)
            # Successfully withdrawing a selling order (num) goods at the price of (price) at (time)
            self.player.goods += int(self.player.transaction[cmd[3]][1])
            del self.player.transaction[cmd[3]]
            self.notice("Managed to withdraw the selling order.", False)
            self.write_log(f"Withdraw a selling order of {num} goods at the price {price}, remain goods {self.player.goods}.")
            if self.mode == 1:
                self.window.freshTransTableWidget.emit()
                self.window.freshStatusBar.emit()

        elif core_cmd == 'backbuyok':
            #backbuyok (num) (price) (time)
            # Successfully withdrawing a buying order (num) goods at the price of (price) at (time)
            self.player.money += int(self.player.transaction[cmd[3]][1])*int(self.player.transaction[cmd[3]][2])
            del self.player.transaction[cmd[3]]
            self.notice("Managed to withdraw the buying order.", False)
            self.write_log(f"Withdraw a buying order of {num} goods at the price {price}, remain money {self.player.money}.")
            if self.mode == 1:
                self.window.freshTransTableWidget.emit()
                self.window.freshStatusBar.emit()
                self.window.freshWinProcessBar.emit()

        elif core_cmd == 'buydealok':
            #buydealok (num) (price) (time)
            # Deal a buying order of (num) goods at the price of (price) at (time)
            num = int(cmd[1])
            price = int(cmd[2])
            time = cmd[3]

            #处理余额
            if price == self.player.transaction[time][2]:
                pass
            elif price < int(self.player.transaction[time][2]):
                self.player.money += (int(self.player.transaction[time][2]) - price) * num
            else:
                self.player.money -= (price - int(self.player.transaction[cmd[3]][2])) * num
            
            #处理物资
            self.player.goods += num
            num_ordered = int(self.player.transaction[time][1])
            num_ordered -= num
            if num_ordered == 0:
                del self.player.transaction[time]
            else:
                self.player.transaction[time][1] = str(num_ordered)
            
            self.notice(f"Made a buying deal of {num} goods at the price {price}.", False)
            self.write_log(f"Deal a buying order of {num} goods at the price {price}, remain money {self.player.money} and goods {self.player.goods}.")
            if self.mode == 1:
                self.window.freshTransTableWidget.emit()
                self.window.freshStatusBar.emit()
                self.window.freshWinProcessBar.emit()
            
        elif core_cmd == 'selldealok':
            #selldealok (num) (price) (time)
            # Deal a selling order of (num) goods at the price of (price) at (time)
            num = int(cmd[1])
            price = int(cmd[2])
            time = cmd[3]

            #处理余额
            self.player.money += price * num
            
            #处理物资
            num_ordered = int(self.player.transaction[time][1])
            num_ordered -= num
            if num_ordered == 0:
                del self.player.transaction[time]
            else:
                self.player.transaction[time][1] = str(num_ordered)
            
            self.notice(f"Made a selling deal of {num} goods at the price {price}.", False)
            self.write_log(f"Deal a selling order of {num} goods at the price {price}, remain money {self.player.money} and goods {self.player.goods}.")
            if self.mode == 1:
                self.window.freshTransTableWidget.emit()
                self.window.freshStatusBar.emit()
                self.window.freshWinProcessBar.emit()
        
        #广播指令
        elif core_cmd == 'sell':
            #sell (num) (price)
            # Someone is selling (num) goods at the price of (price)
            num = int(cmd[1])
            price = int(cmd[2])
            self.selling.add_order((price, num))
            self.write_log(f"Someone sells {num} goods at the price {price}.")
            if self.mode == 1:
                self.window.freshSellTableWidget.emit()
        elif core_cmd == 'buy':
            #buy (num) (price)
            # Someone is buying (num) goods at the price of (price)
            num = int(cmd[1])
            price = int(cmd[2])
            self.buying.add_order((price, num))
            self.write_log(f"Someone buys {num} goods at the price {price}.")
            if self.mode == 1:
                self.window.freshBuyTableWidget.emit()   
        elif core_cmd == 'backsell':
            #backsell (num) (price)
            # Someone withdrawed a selling order of (num) goods at the price of (price)
            num = int(cmd[1])
            price = int(cmd[2])
            self.selling.del_order((price, num))
            self.write_log(f"Someone withdraws a selling order of {num} goods at the price {price}.")
            if self.mode == 1:
                self.window.freshSellTableWidget.emit()
        elif core_cmd == 'backbuy':
            #backbuy (num) (price)
            # Someone withdrawed a buying order of (num) goods at the price of (price)
            num = int(cmd[1])
            price = int(cmd[2])
            self.buying.del_order((price, num))
            self.write_log(f"Someone withdraws a buying order of {num} goods at the price {price}.")
            if self.mode == 1:
                self.window.freshBuyTableWidget.emit()
        elif core_cmd == 'dealsell':
            #dealsell (num) (price) (dealtime)
            # Someone deal a selling order of (num) goods at the price of (price)
            price = int(cmd[2])
            num = int(cmd[1])
            deal_time = localtime(float(cmd[3]))[3:6]
            #处理卖盘
            self.selling.match_del((price, num))
            #处理买盘
            self.buying.del_order((price, num))
            # Display on GUI
            self.price = price
            self.new_deal(1, price, num, deal_time)
            self.notice(f"A new selling deal of {cmd[1]} goods at the price {cmd[2]}.", False)
            self.write_log(f"Someone deals a selling order of {num} goods at the price {price}.")
            if self.mode == 1:
                self.window.freshBuyTableWidget.emit()
                self.window.freshSellTableWidget.emit()
                self.window.freshLCD.emit()
        elif core_cmd == 'dealbuy':
            #dealbuy (num) (price) (dealtime)
            # Someone deal a buying order of (num) goods at the price of (price)
            price = int(cmd[2])
            num = int(cmd[1])
            deal_time = localtime(float(cmd[3]))[3:6]
            #处理买盘
            self.buying.match_del((price, num))
            #处理卖盘
            self.selling.del_order((price, num))
            # Display on GUI
            self.price = price
            self.new_deal(0, price, num, deal_time)
            self.notice(f"A new buying deal of {cmd[1]} goods at the price {cmd[2]}.", False)
            self.write_log(f"Someone deals a buying order of {num} goods at the price {price}.")
            if self.mode == 1:
                self.window.freshBuyTableWidget.emit()
                self.window.freshSellTableWidget.emit()
                self.window.freshLCD.emit()
        elif core_cmd == 'name':
            #name (IP):(port) (name)
            # A new player named (name) at (IP):(port)
            addr = cmd[1]
            name = cmd[2]
            self.notice(f'Players: {name} at {addr}', False)
            self.write_log(f"A new player named {name} at {addr}.")
            self.playerList.append((addr, name))
            if self.mode == 1:
                self.window.updatePlayer.emit()
                self.window.freshWinProcessBar.emit()
        elif core_cmd == 'begin':
            #begin (time)
            # Game began at (time)
            self.beginTime = cmd[1]
            self.notice('GAME START!')
            self.write_log(f"Game starts at {time}.")
            if self.mode == 1:
                self.window.beginGame.emit()
        elif core_cmd == 'winner':
            #winner (name)
            # (name) is the winner
            self.winner = cmd[1]
            self.write_log(f'{self.winner} wins the game!')
            self.notice(f'{self.winner} wins the game!')

    def notice(self, content, on_GUI=True):  # Give a notice to the player
        if self.mode == 0:
            # Console mode
            print(content, sep='')
        elif self.mode == 1:    # Display by a messagebox
            # GUI mode
            if on_GUI:
                self.GUI_msgbox(content)

    def new_deal(self, dir, price, num, deal_time):
        """
        dir(int) The positive direction for the deal: 0(buy), 1(sell).
        price(int): Price of the deal.
        num(int): Number of the deal.
        """
        if self.mode == 0:
            # Console mode
            if dir == 0:
                print("Positive Buy: ", end='')
            elif dir == 1:
                print("Positive Sell: ", end='')
            print(f"num {num}, price {price}.")
        elif self.mode == 1:
            # GUI mode
            # Handle commands from server and then fresh the GUI
            self.GUI_newDeal(dir, price ,num, deal_time)

    def send_cmd(self, cmd):
        if type(cmd) == str:
            cmd = cmd.strip().split()
        if cmd[0] == 'sell':
            self.sell(int(cmd[1]), int(cmd[2]))
        elif cmd[0] == 'buy':
            self.buy(int(cmd[1]), int(cmd[2]))
        elif cmd[0] == 'backsell':
            self.backsell(cmd[1], cmd[2], cmd[3])
        elif cmd[0] == 'backbuy':
            self.backbuy(cmd[1], cmd[2], cmd[3])

    def soc_recv(self):     # Recieve data from the server
        while True:
            try:
                buff = self.soc.recv(1024).decode('utf8')
            except Exception:
                self.notice("Network error! Game stopped...")
                break
            command = buff.split('#')
            for i in command[:]:                    #去除空指令
                if not i:
                    command.remove(i)
            for item in command:
                cmd = item.strip().split()
                self.recv_cmd_handle(cmd)

    def sell(self, num, price):
        '''
        num:数量
        price:单价
        '''
        
        if self.player.goods >= num:
            command = f'sell {num} {price}#'
            self.soc.sendall(command.encode('utf8'))
        else:
            self.notice('No enough goods!')

    def buy(self, num, price):
        '''
        num:数量
        price:单价
        '''

        if self.player.money >= num * price:
            command = f'buy {num} {price}#'
            self.soc.sendall(command.encode('utf8'))
        else:
            self.notice('No enough money!')

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

    def CON_fresh(self, content):
        self.recv_cmd_handle(content)

    def write_log(self, log):
        log = ctime() + " " + log
        print(log)
        self.logFile.write(log + '\n')
        self.logFile.flush()

    @abstractmethod
    def GUI_msgbox(self, content):
        pass

    @abstractmethod
    def GUI_newDeal(self, dir, price, num, deal_time):     # Called when new deal is finished
        """
        dir(int) The positive direction for the deal: 0(buy), 1(sell).
        price(int): Price of the deal.
        num(int): Number of the deal.
        """
        pass
