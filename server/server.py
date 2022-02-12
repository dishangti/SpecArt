import socketserver as sck
import time as tm
import heapq as hp
import threading as thrd

syn_lock = thrd.Lock()          # Thread synchronization lock

class TCPServer(sck.ThreadingTCPServer):
    allow_reuse_address = True

class Player:
    '''
    Save the basic player infomation.
    '''

    def __init__(self, addr, name, money, goods, sock):
        '''
        addr:(str) IP:port of a player.
        name:(str) Username of a player.
        money:(int) Total money of a player.
        goods:(int) The number of goods of a player.
        sock: Network socket of a player.
        '''
        self.addr = addr
        self.name = name
        self.money = money
        self.goods = goods
        self.sock = sock

class Order:
    '''
    Define a order's information.
    '''
    BUY_ORDER = 0
    SELL_ORDER = 1

    ORDER_PRICE = 0
    ORDER_TIME = 1
    ORDER_NUM = 2
    ORDER_NAME = 3

    sell_queue = []
    buy_queue = []

    def __init__(self, price, time, num, name, mode):
        '''
        price:(int) Price per good.
        time:(float) Timestamp submitting the order.
        num:(int) The number of goods.
        name:(str) Username submitting the order.
        mode:(BUY_ORDER/SELL_ORDER).
        '''
        self.price = price
        self.time = time
        self.num = num
        self.name = name
        self.mode = mode

    def __lt__(self, other):
        '''
        Define a method as an operator < for Order class.
        For SELL_ORDER, it should be sorted in ascending order by price.
        For BUY_ORDER, it should be sorted in descending order by price.
        Both of them should be sorted in ascending order by time as the secondary keyword.
        '''
        swth = 1
        if self.mode == Order.SELL_ORDER: swth = 0
        elif self.mode == Order.BUY_ORDER: swth = 1
        if self.price < other.price: return 1 ^ swth
        elif self.price > other.price: return 0 ^ swth
        else:
            if self.time < other.time: return 1
            else: return 0

class NetHandler(sck.BaseRequestHandler):
    '''
    Inherited from socketserver.BaseRequestHandler.
    Handle network request.
    '''

    pause = False
    players = {}

    def time_str(self, string):
        '''
        string:(str) The string to process.
        Return a new string by adding a time information on the string.
        '''
        return tm.ctime() + " " + string

    def command(self, *strs):
        '''
        Wrap strs and encode it by UTF-8.
        '''
        command = ''
        for string in strs:
            command = command + str(string) + ' '
        command = command.rstrip()
        command = command + '#'
        return command.encode(SpecArt.CODE)

    @classmethod
    def broadcast(cls, *strs):
        '''
        Wrap strs and broadcast it to all the players by UTF-8.
        '''
        command = ''
        for string in strs:
            command = command + str(string) + ' '
        command = command.rstrip()
        command = command + '#'
        command = command.encode(SpecArt.CODE)
        for player in cls.players.values():
            player.sock.sendall(command)

    def winner(self, player):
        '''
        player:(Player)
        Check whether the player is a winner.
        '''
        WIN_MONEY = len(list(NetHandler.players.values())) * SpecArt.INIT_MONEY * SpecArt.WIN_RATE
        if player.money >= WIN_MONEY:
            print(self.time_str(f"{player.name} wins the game."))
            NetHandler.broadcast('winner', player.name)
            SpecArt.win_flag = True

    def buy_order(self, buy_order):
        '''
        buy_order:(Order)
        Process a buying order by always comparing it with the top of the sell heap queue.
        '''
        buy_player = NetHandler.players[buy_order.name]

        while True:
            if Order.sell_queue == []:
                if buy_order.num != 0:
                    hp.heappush(Order.buy_queue, buy_order)
                break
            top_sell = hp.heappop(Order.sell_queue)
            sell_player = NetHandler.players[top_sell.name]

            if buy_order.price < top_sell.price:
                hp.heappush(Order.buy_queue, buy_order)
                hp.heappush(Order.sell_queue, top_sell)
                break

            deal_num = min(top_sell.num, buy_order.num)
            deal_price = top_sell.price
            buy_player.money += deal_price * (buy_order.num - deal_num)           # Return redundant money
            buy_player.goods += deal_num
            top_sell.num -= deal_num
            buy_order.num -= deal_num
            sell_player.money += deal_num * deal_price
            buy_player.sock.sendall(self.command('buydealok', deal_num, deal_price, buy_order.time))        # Buy initiatively
            sell_player.sock.sendall(self.command('selldealok', deal_num, deal_price, top_sell.time))       # Sell initiatively
            NetHandler.broadcast('dealbuy', deal_num, deal_price, tm.time())    # Have a deal
            self.winner(sell_player)

            if buy_order.num == 0:
                if top_sell.num != 0:
                    hp.heappush(Order.sell_queue, top_sell)
                break

    def sell_order(self, sell_order):
        '''
        sell_order:(Order)
        Process a selling order by always comparing it with the top of the buy heap queue.
        '''
        sell_player = NetHandler.players[sell_order.name]
        
        while True:
            if Order.buy_queue == []:
                if sell_order.num != 0:
                    hp.heappush(Order.sell_queue, sell_order)
                break
            top_buy = hp.heappop(Order.buy_queue)
            buy_player = NetHandler.players[top_buy.name]

            if sell_order.price > top_buy.price:
                hp.heappush(Order.sell_queue, sell_order)
                hp.heappush(Order.buy_queue, top_buy)
                break

            deal_num = min(top_buy.num, sell_order.num)
            deal_price = top_buy.price
            sell_player.money += deal_num * deal_price
            sell_order.num -= deal_num
            top_buy.num -= deal_num
            buy_player.goods += deal_num
            sell_player.sock.sendall(self.command('selldealok', deal_num, deal_price, sell_order.time))     # Buy initiatively
            buy_player.sock.sendall(self.command('buydealok', deal_num, deal_price, top_buy.time))          # Sell initiatively
            NetHandler.broadcast('dealsell', deal_num, deal_price, tm.time())      # Have a deal

            self.winner(sell_player)
            if sell_order.num == 0:
                if top_buy.num != 0:
                    hp.heappush(Order.buy_queue, top_buy)
                break
            

    def command_handle(self, command):
        '''
        command:(list<str>) A single command stripped into a string list.
        '''

        if command == []: return
        if self.named == False and SpecArt.begin_flag == False and command[0] == 'name':
            self.named = True
            self.name = command[1]
            self.player = Player(self.addr, self.name, SpecArt.INIT_MONEY, SpecArt.INIT_GOODS, self.sock)
            NetHandler.players[self.name] = self.player
            with syn_lock:
                self.sock.sendall(self.command('nameok', self.name))
                self.sock.sendall(self.command('money', SpecArt.INIT_MONEY))        # Set money for a player
                self.sock.sendall(self.command('goods', SpecArt.INIT_GOODS))        # Set goods for a player
            print(self.time_str(f"{self.addr} set name as {self.name}."))

        if self.named == False and SpecArt.begin_flag == True:
            self.sock.close()
            self.inuse = False

        if self.named == True and SpecArt.begin_flag == False and command[0] != 'name':
            return

        if SpecArt.win_flag:
            return

        if command[0] == 'sell':
            num = int(command[1])
            price = int(command[2])
            with syn_lock:
                if num > self.player.goods: return
                self.player.goods -= num
                sell_order = Order(price, tm.time(), num, self.name, Order.SELL_ORDER)
                self.sock.sendall(self.command('sellok', num, price, sell_order.time))
                NetHandler.broadcast('sell', num, price)
                self.sell_order(sell_order)

        if command[0] == 'buy':
            num = int(command[1])
            price = int(command[2])
            with syn_lock:
                if price * num > self.player.money: return
                self.player.money -= price * num
                buy_order = Order(price, tm.time(), num, self.name, Order.BUY_ORDER)
                self.sock.sendall(self.command('buyok', num, price, buy_order.time))
                NetHandler.broadcast('buy', num, price)
                self.buy_order(buy_order)

        if command[0] == 'backbuy':
            if Order.buy_queue == []: return
            num = int(command[1])
            price = int(command[2])
            time = float(command[3])
            with syn_lock:
                for i, order in enumerate(Order.buy_queue):
                    if order.name == self.name and order.num == num\
                    and order.price == price and abs(order.time - time) < 1e-3:
                        Order.buy_queue.pop(i)
                        hp.heapify(Order.buy_queue)
                self.sock.sendall(self.command('backbuyok', num, price, time))
                NetHandler.broadcast('backbuy', num, price)

        if command[0] == 'backsell':
            if Order.sell_queue == []: return
            num = int(command[1])
            price = int(command[2])
            time = float(command[3])
            with syn_lock:
                for i, order in enumerate(Order.sell_queue):
                    if order.name == self.name and order.num == num\
                    and order.price == price and abs(order.time - time) < 1e-3:
                        Order.sell_queue.pop(i)
                        hp.heapify(Order.sell_queue)
                self.sock.sendall(self.command('backsellok', num, price, time))
                NetHandler.broadcast('backsell', num, price)

    def setup(self):
        '''
        Initialize the new player.
        '''
        self.named = False
        self.inuse = True
        self.addr = self.client_address[0] + ':' + str(self.client_address[1])
        self.sock = self.request
        print(self.time_str(f'Connetion from: {self.addr}.'))

    def handle(self):
        '''
        Handle commands recieved from the player.
        '''
        while self.inuse:
            try:
                buff = self.request.recv(1024).decode(SpecArt.CODE)
            except Exception:
                print('Network error, game forcely stopped...')
                SpecArt.stop_flag = True
                break
            commands = buff.split('#')
            for command in commands:
                self.command_handle(command.split(' '))

class SpecArt:
    '''
    Save some game settings.
    '''
    VERSION = "v0.2.0-beta"
    INIT_MONEY = 100000
    INIT_GOODS = 100000
    WIN_RATE = 0.6
    WIN_MONEY = 0
    CODE = 'utf8'

    win_flag = False
    begin_flag = False
    stop_flag = False
    ser_sock = None

    def __init__(self, host, port):
        self.host = host
        self.port = port
        SpecArt.ser_sock = TCPServer((host, port), NetHandler)
        self.conn_pool = []
        self.players = {}
        SpecArt.ser_sock.serve_forever()

    def __del__(self):
        for player in NetHandler.players:
            player.sock.close()
        SpecArt.ser_sock.shutdown()
        SpecArt.ser_sock.server_close()
