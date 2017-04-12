import socket
import string
import random
import re

def PRIVMSG(channel, MSG):
    return bytes('PRIVMSG {0} :{1}\r\n'  .format(channel, MSG), 'utf-8')

QAdata = {"9487":"94狂", "東馬":"小三", "雪菜":"碧池", "全家":"就是你家", "Beep Beep":"I'm a Sheep", "たーのしー！":"すごーい！", "たのしー！":"おもしろーい！"}

if __name__ == '__main__':

    server = "chat.freenode.net"
    port = 6667
    channel = "#fcucetest03"
    realname = "PythonIRCBot_V"

    maxnamechar = 8
    nick = "".join(random.choice(string.ascii_letters) for _ in range(maxnamechar))
    login = "".join(random.choice(string.ascii_letters) for _ in range(maxnamechar))
    print("Nick:  {0}\nlogin: {1}".format(nick, login))

    recvBuff = bytes("", 'utf-8')
    recvCount = 0
    lines = []

    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #defines the socket
    print("Connecting to: {0}".format(server))

    irc.connect( (server, port) )
    irc.send(bytes('NICK {0}\r\n'                       .format(nick)                           , 'utf-8'))
    irc.send(bytes('USER {0} {1} {2} :{3}\r\n'          .format(login, login, login, realname)  , 'utf-8'))
    irc.send(bytes('JOIN {0}\r\n'                       .format(channel)                        , 'utf-8'))
    irc.send(PRIVMSG(channel, "Hello! I'm Bot, use `~HELP~` read HELP message."))
  # irc.send(bytes('QUIT\r\n'                                                                   , 'utf-8'))
    print("Connecting Success!")


    while True:
        recvBuff = irc.recv(1024)
        recvCount += 1
      # print("{0}: {1}".format(str(recvCount).zfill(3), repr(recvBuff.decode('utf-8'))))   # Print RAW message.
        lines = str.splitlines(recvBuff.decode('utf-8'))
        print("{0:03d}({2:02d}): {1}".format(recvCount, lines, lines.__len__()))            # Split message per line.

        temp = str.split(recvBuff.decode('utf-8'), "\n")
        readbuffer = temp.pop()

        lineNum = 0
        for line in lines:
            lineNum += 1
            words = line.split()
            print(" -> {1:02d} - {0}".format(line, lineNum))
          # print(" -> {0}".format(words))


            m = re.match("PING :(.*)", line)
            if (m):
                irc.send(bytes("PONG {0}\r\n".format(m[1]), 'utf-8'))
                print("PING PONG!")


            m = re.match(":([^!]*)!(\S*) PRIVMSG (#\S+) :(.*)", line)
            if (m):
                msg = m[4]
                print("MSG = {0}".format(msg))

                if (msg == ("~HELP~" or "~help~")):
                    # irc.send(PRIVMSG(channel, QAdata.__str__()))
                    Smsg = "I know these words: "
                    for QA in QAdata:
                        Smsg = Smsg + QA + ", "
                    irc.send(PRIVMSG(channel, Smsg))
                    irc.send(PRIVMSG(channel, "USE ~set~ [A] as [B], (like this: `~set~ 9487 as 94狂`), to set a Q&A pair."))
                else:
                    mm = re.match("~set~ (.+) as (.+)", msg)
                    if (mm):
                        QAdata.update({mm[1]:mm[2]})
                        irc.send(PRIVMSG(channel, "DATA SET SUCCESSFUL: {0} as {1}.".format(mm[1],mm[2])))
                    else:
                        for QA in QAdata:
                           if (msg == QA): irc.send(PRIVMSG(channel, QAdata[QA]))



        print()

    irc.close()
