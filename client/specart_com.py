import socket
import threading
import bisect

class OrderQueue():
    """
    An order queue is a list of orders ordered by price.
    """

    def __init__(self):
        """
        typ(int): 0(selling list in descending order), 1(buying list in ascending order).
        """

        self.ord_lst = []

    def add_order(self, order):
        """
        order: a tuple in (price, num)
        """

        # Bugs here

        price, num = order
        ord_lst = self.ord_lst
        if len(ord_lst) == 0:
            ord_lst.append(order)
            return

        ord_price_lst = list(map(lambda x: x[0], self.ord_lst))
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
        ord_lst = self.ord_lst
        if len(ord_lst) == 0: return

        ord_price_lst = list(map(lambda x: x[0], self.ord_lst))
        pos = bisect.bisect_left(ord_price_lst, order[0])
        if order[0] == ord_lst[pos][0]:
            num = ord_lst[pos][1] - num
            ord_lst[pos] = (price, num)
        if ord_lst[pos][1] <= 0:
            ord_lst.pop(pos)

    def get_order(self):
        rev = self.ord_lst.copy()
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
    def __init__(self, mode):
        '''
        mode(integer): 0(consle), 1(GUI)
        '''
        self.mode = mode
        self.soc = socket.socket()
        self.player = Player()
        self.initGoods = 0              # Inited money and goods
        self.initMoney = 0
        self.beginTime = ""
        self.totalPlayerMoney = 0      # Total money of all the players

        # Here are varieties for GUI to fresh
        self.price = 0
        self.buying = OrderQueue()
        self.selling = OrderQueue()
        self.deal = ""
        self.players = []

    def connect(self, username, host, port = 7733):
        self.player.username = username
        self.soc.connect((host, port))
        thread = threading.Thread(target=self.soc_recv, name='socRecvThread')
        thread.start()
        self.soc.sendall(f'name {self.player.username}#'.encode('utf8'))

    def recv_cmd_handle(self, cmd):
        '''
        cmd(list) :指令字符串按空格分割后的指令列表
        '''

        try:
            core_cmd = cmd[0]
            
            #私人指令
            if core_cmd == 'nameok':                                        #nameok (name)
                self.notice(f'Successfully set your name as {cmd[1]}.')

            elif core_cmd == 'money':                                 #money (initMoney)
                self.player.money = self.initMoney = int(cmd[1])
                self.notice('Initial money: ' + cmd[1])

            elif core_cmd == 'goods':                                       #goods (initGoods)
                self.player.goods = self.initGoods = int(cmd[1])
                self.notice('Initial goods: ' + cmd[1])

            elif core_cmd == 'sellok':                                      #sellok (num) (price) (time)
                #print('Server Instruction: '+' '.join(cmd))
                cmd[0] = 'sell'
                self.player.transaction[cmd[3]] = cmd
                self.player.goods -= int(cmd[1])

            elif core_cmd == 'buyok':                                       #buyok (num) (price) (time)
                #print('Server Instruction: '+' '.join(cmd))
                cmd[0] = 'buy'
                self.player.transaction[cmd[3]] = cmd
                self.player.money -= int(cmd[1])*int(cmd[2])

            elif core_cmd == 'backsellok':                                  #backsellok (num) (price) (time)
                self.player.goods += int(self.player.transaction[cmd[3]][1])
                del self.player.transaction[cmd[3]]
                #print('Server Instruction: '+' '.join(cmd))

            elif core_cmd == 'backbuyok':                                   #backbuyok (num) (price) (time)
                self.player.money += int(self.player.transaction[cmd[3]][1])*int(self.player.transaction[cmd[3]][2])
                del self.player.transaction[cmd[3]]
                #print('Server Instruction: '+' '.join(cmd))

            elif core_cmd == 'buydealok':                                   #buydealok (num) (price) (time)
                #处理余额
                if cmd[2] == self.player.transaction[cmd[3]][2]:
                    pass
                elif int(cmd[2]) < int(self.player.transaction[cmd[3]][2]):
                    self.player.money += (int(self.player.transaction[cmd[3]][2]) - int(cmd[2])) * int(cmd[1])
                else:
                    self.player.money -= (int(cmd[2]) - int(self.player.transaction[cmd[3]][2])) * int(cmd[1])
                
                #处理物资
                self.player.goods += int(cmd[1])
                num_ordered = int(self.player.transaction[cmd[3]][1])
                num_ordered -= int(cmd[1])
                if num_ordered == 0:
                    del self.player.transaction[cmd[3]]
                else:
                    self.player.transaction[cmd[3]][1] = str(num_ordered)
                
                #print('Server Instruction: '+' '.join(cmd))
                
            elif core_cmd == 'selldealok':                                  #selldealok (num) (price) (time)
                #处理余额
                self.player.money += int(cmd[2]) * int(cmd[1])
                
                #处理物资
                num_ordered = int(self.player.transaction[cmd[3]][1])
                num_ordered -= int(cmd[1])
                if num_ordered == 0:
                    del self.player.transaction[cmd[3]]
                else:
                    self.player.transaction[cmd[3]][1] = str(num_ordered)
                
                #print('Server Instruction: '+' '.join(cmd))
            
            
            #广播指令
            elif core_cmd == 'sell':                                        #sell (num) (price)
                self.selling.add_order((int(cmd[2]), int(cmd[1])))
            elif core_cmd == 'buy':                                         #buy (num) (price)
                self.buying.add_order((int(cmd[2]), int(cmd[1])))      
            elif core_cmd == 'backsell':                                    #backsell (num) (price)
                self.selling.del_order((int(cmd[2]), int(cmd[1])))
            elif core_cmd == 'backbuy':                                     #backbuy (num) (price)
                self.buying.del_order((int(cmd[2]), int(cmd[1])))
            elif core_cmd == 'dealsell':                                    #dealsell (num) (price) (dealtime)
                # print('News: '+' '.join(cmd))
                price = int(cmd[2])
                num = int(cmd[1])
                #处理买盘
                self.buying.del_order((price, num))
                #处理卖盘
                self.selling.del_order((price, num))
                # Display on GUI
                self.new_deal(0, price, num)
                self.price = price
            elif core_cmd == 'dealbuy':                                     #dealbuy (num) (price) (dealtime)
                # print('News: '+' '.join(cmd))
                price = int(cmd[2])
                num = int(cmd[1])
                #处理卖盘
                self.selling.del_order((price, num))
                #处理买盘
                self.buying.del_order((price, num))
                # Display on GUI
                self.new_deal(1, price, num)
                self.price = price
            elif core_cmd == 'name':                                        #name (IP):(port) (name)
                print(f'Players: {cmd[2]} {cmd[1]}')
                self.players.append((cmd[1], cmd[2]))
            elif core_cmd == 'begin':                                       #begin (time)
                self.beginTime = cmd[1]
                print('GAME START!')
            
            if self.mode == 1:
                self.GUI_fresh()

        except IndexError:
            print('void cmd')

    def notice(self, content):  # Give a notice to the player
        if self.mode == 0:
            # Console mode
            print(content, sep='')
        elif self.mode == 1:    # Display by a messagebox
            # GUI mode
            self.GUI_msgbox(content)

    def new_deal(self, dir, price, num):
        """
        dir(int) The positive direction for the deal: 0(buy), 1(sell).
        price(int): Price of the deal.
        num(int): Number of the deal.
        """
        if self.mode == 0:
            # Console mode
            if dir == 0:
                print("Positive Buy: ")
            elif dir == 1:
                print("Positive Sell: ")
            print(f"num {num}, price {price}.")
        elif self.mode == 1:
            # GUI mode
            # Handle commands from server and then fresh the GUI
            self.GUI_newDeal(dir, price ,num)

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
            except Exception as e:
                self.notice("Network error!")
                exit()
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

    def GUI_msgbox(self, content):
        pass

    def GUI_fresh(self):     # Fresh values in GUI
        pass

    def GUI_newDeal(self, dir, price, num):     # Called when new deal is finished
        """
        dir(int) The positive direction for the deal: 0(buy), 1(sell).
        price(int): Price of the deal.
        num(int): Number of the deal.
        """
        pass