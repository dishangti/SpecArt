import Server as ser
import time as tm
import threading as thrd

def init():
    ser.SpecArt('0.0.0.0', 7733)

def controller():
    '''
    Control the server.
    '''
    print('Input b and press enter to begin after all the players in.')
    print('Input q and press enter to quit.')

    while True:
        cmd = input('')
        if cmd == 'b' and ser.SpecArt.begin_flag == False:
            ser.SpecArt.begin_flag = True
            time = tm.time()
            begin_info = 'SpecArt Begins at ' + tm.ctime(time)
            print(begin_info)
            with ser.syn_lock:
                ser.NetHandler.broadcast(begin_info)
                ser.NetHandler.broadcast('begin', time)
                for player in ser.NetHandler.players.values():
                    ser.NetHandler.broadcast('name', player.addr, player.name)

        if cmd == 'q':
            del ser.SpecArt.ser_sock
            exit(0)

print("Welcome to SpecArt Server!")
server = thrd.Thread(target=init)
server.start()
print("Server is running...")
controller()

