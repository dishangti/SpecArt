from specart_com import Player, Com
import socket
import threading

soc = socket.socket()

class CON_Com(Com):
    def CON_fresh(self, content):
        self.command_handle(cmd)

def Bsort(B):
    '''
    将买盘按价格降序排列后返回
    B:买盘字典
    返回:字典，形如{'B1':(price, num), 'B2':(price, num)...}
    '''

    B_lst = list(B.items())
    B_lst.sort(key=lambda tpl:int(tpl[0]), reverse=True)
    
    length = len(B_lst)
    if length <= 5:
        n = length + 1
    else:
        n = 6
    ret = {}
    for i in range(1, n):
        ret[f'B{i}'] = B_lst[i-1]
    
    return ret

def Ssort(S):
    '''
    将卖盘按价格升序排列后返回
    S:卖盘字典
    返回:字典，形如{'S1':(price, num), 'S2':(price, num)...}
    '''

    S_lst = list(S.items())
    S_lst.sort(key=lambda tpl:int(tpl[0]), reverse=False)

    length = len(S_lst)
    if length <= 5:
        n = length + 1
    else:
        n = 6
    ret = {}
    for i in range(1, n):
        ret[f'S{i}'] = S_lst[i-1]
    
    return ret

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
                print(Ssort(selling))
            elif cmd[0] == 'buying':
                print(Bsort(buying))
            else:
                print('invalid command')
        except Exception as e:
            print(e)

