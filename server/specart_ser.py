import socketserver as sck
import time as tm
import heapq as hp
import threading as thrd

class TCPServer(sck.ThreadingTCPServer):
    allow_reuse_address = True

class Player:
    def __init__(self, addr, name, money, goods, sock):
        self.addr = addr
        self.name = name
        self.money = money
        self.goods = goods
        self.sock = sock

class Order:
    BUY_ORDER = 0
    SELL_ORDER = 1

    ORDER_PRICE = 0
    ORDER_TIME = 1
    ORDER_NUM = 2
    ORDER_NAME = 3

    sell_queue = []
    buy_queue = []

    def __init__(self, price, time, num, name, mode):
        self.price = price
        self.time = time
        self.num = num
        self.name = name
        self.mode = mode

    def __repr__(self):
        return str(self.price) + ' ' + str(self.time) + ' ' + str(self.num)

    def __lt__(self, other):
        swth = 1
        if self.mode == Order.SELL_ORDER: swth = 0
        elif self.mode == Order.BUY_ORDER: swth = 1
        if self.price < other.price: return 1 ^ swth
        elif self.price > other.price: return 0 ^ swth
        else:
            if self.time < other.time: return 1
            else: return 0

class NetHandler(sck.BaseRequestHandler):
    pause = False
    players = {}

    def time_str(self, string):
        return tm.ctime() + " " + string

    def command(self, *strs):
        command = ''
        for string in strs:
            command = command + str(string) + ' '
        command = command.rstrip()
        command = command + '#'
        return command.encode('utf8')

    @classmethod
    def broadcast(cls, *strs):
        command = ''
        for string in strs:
            command = command + str(string) + ' '
        command = command.rstrip()
        command = command + '#'
        command = command.encode('utf8')
        for player in cls.players.values():
            player.sock.sendall(command)

    def winner(self, player):
        WIN_MONEY = len(list(NetHandler.players.values())) * SpecArt.INIT_MONEY * SpecArt.WIN_RATE
        if player.money >= WIN_MONEY:
            NetHandler.broadcast('winner', player.name)

    def buy_order(self, buy_order):
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
            buy_order.num -= deal_num
            buy_player.money += deal_num * (buy_order.num - deal_num)
            buy_player.goods += deal_num
            top_sell.num -= deal_num
            sell_player.money += deal_num * deal_price
            buy_player.sock.sendall(self.command('buydealok', deal_num, deal_price, buy_order.time))
            sell_player.sock.sendall(self.command('selldealok', deal_num, deal_price, top_sell.time))
            NetHandler.broadcast('dealbuy', deal_num, deal_price, tm.time())
            self.winner(sell_player)

            if buy_order.num == 0:
                if top_sell.num != 0:
                    hp.heappush(Order.sell_queue, top_sell)
                break

    def sell_order(self, sell_order):
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
            sell_order.num -= deal_num
            sell_player.money += deal_num * deal_price
            top_buy.num -= deal_num
            buy_player.money += deal_num * (top_buy.num - deal_num)
            buy_player.goods += deal_num
            sell_player.sock.sendall(self.command('selldealok', deal_num, deal_price, sell_order.time))
            buy_player.sock.sendall(self.command('buydealok', deal_num, deal_price, top_buy.time))
            NetHandler.broadcast('dealsell', deal_num, deal_price, tm.time())

            if sell_order.num == 0:
                if top_buy.num != 0:
                    hp.heappush(Order.sell_queue, top_buy)
                break

            self.winner(sell_player)

    def command_handle(self, command):
        if command == []: return
        if self.named == False and SpecArt.begin_flag == False and command[0] == 'name':
            self.named = True
            self.name = command[1]
            self.player = Player(self.addr, self.name, SpecArt.INIT_MONEY, SpecArt.INIT_GOODS, self.sock)
            NetHandler.players[self.name] = self.player
            self.sock.sendall(self.command('nameok', self.name))
            self.sock.sendall(self.command('money', SpecArt.INIT_MONEY))
            self.sock.sendall(self.command('goods', SpecArt.INIT_GOODS))
            print(self.time_str(f"{self.addr} set name as {self.name}."))

        if self.named == False and SpecArt.begin_flag == True:
            self.sock.close()
            self.inuse = False

        if self.named == True and SpecArt.begin_flag == False and command[0] != 'name':
            return

        if command[0] == 'sell':
            num = int(command[1])
            price = int(command[2])
            if num > self.player.goods: return
            self.player.goods -= num
            sell_order = Order(price, tm.time(), num, self.name, Order.SELL_ORDER)
            self.sock.sendall(self.command('sellok', num, price, sell_order.time))
            NetHandler.broadcast('sell', num, price)
            self.sell_order(sell_order)

        if command[0] == 'buy':
            num = int(command[1])
            price = int(command[2])
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
            for i, order in enumerate(Order.buy_queue):
                if order.name == self.name and order.num == num\
                and order.price == -price and order.time == time:
                    Order.buy_queue.pop(i)
                    hp.heapify(Order.buy_queue)
            self.sock.sendall(self.command('backbuyok', num, price, time))
            NetHandler.broadcast('backbuy', num, price)

        if command[0] == 'backsell':
            if Order.sell_queue == []: return
            num = int(command[1])
            price = float(command[2])
            time = float(command[3])
            for i, order in enumerate(Order.sell_queue):
                if order.name == self.name and order.num == num\
                and order.price == price and order.time == time:
                    Order.sell_queue.pop(i)
                    hp.heapify(Order.sell_queue)
            self.sock.sendall(self.command('backsellok', num, price, time))
            NetHandler.broadcast('backsell', num, price)

        if SpecArt.win_flag and SpecArt.ser_sock:
            del SpecArt.ser_sock

    def setup(self):
        self.named = False
        self.inuse = True
        self.addr = self.client_address[0] + ':' + str(self.client_address[1])
        self.sock = self.request
        print(self.time_str(f'Connetion from: {self.addr}.'))

    def handle(self):
        while self.inuse:
            buff = self.request.recv(1024).decode('utf8')
            print(buff)
            commands = buff.split('#')
            for command in commands:
                self.command_handle(command.split(' '))

class SpecArt:
    INIT_MONEY = 100000
    INIT_GOODS = 100000
    WIN_RATE = 0.6
    WIN_MONEY = 0

    win_flag = False
    begin_flag = False
    ser_sock = None

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = TCPServer((host, port), NetHandler)
        self.conn_pool = []
        self.players = {}
        self.sock.serve_forever()

    def __del__(self):
        self.sock.shutdown()
        self.sock.server_close()
        exit(0)

def init():
    SpecArt('0.0.0.0', 7733)

def controller():
    while True:
        cmd = input()
        if cmd == 'b' and SpecArt.begin_flag == False:
            SpecArt.begin_flag = True
            time = tm.time()
            begin_info = 'SpecArt Begins at ' + tm.ctime(time)
            print(begin_info)
            NetHandler.broadcast(begin_info)
            NetHandler.broadcast('begin', time)
            for player in NetHandler.players.values():
                NetHandler.broadcast('name', player.addr, player.name)

ser = thrd.Thread(target=init)
ser.start()
controller()
