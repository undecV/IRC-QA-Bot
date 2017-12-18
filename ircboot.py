import socket
import string
import random
import re

import yaml

import irc_msg


def main():
    server = "chat.freenode.net"
    port = 6667
    channel = "#fcucetest03"
    realname = "PythonIRCBot_V"

    data = {}

    with open("./data.yaml", "r", encoding="UTF-8") as f:
        data.update(yaml.load(f))
        print("File {} OK.".format("./data.yaml"))
    print(data)

    maxnamechar = 8
    nick = "".join(random.choice(string.ascii_letters) for _ in range(maxnamechar))
    login = "".join(random.choice(string.ascii_letters) for _ in range(maxnamechar))
    print("Nick:  {0}\nlogin: {1}".format(nick, login))

    recv_count = 0

    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # defines the socket
    print("Connecting to: {0}".format(server))

    irc.connect((server, port))
    irc.send(irc_msg.nick(nick))
    irc.send(irc_msg.user(login, login, login, realname))
    irc.send(irc_msg.join(channel))
    irc.send(irc_msg.privmsg(channel, "Hello! I'm Bot, use `~HELP~` read HELP message."))
    # irc.send(irc_msg.quit())
    print("Connecting Success!")

    while True:
        recv_buff = irc.recv(1024)
        recv_count += 1
        # print("{0}: {1}".format(str(recv_count).zfill(3), repr(recv_buff.decode('utf-8'))))   # Print RAW message.
        lines = str.splitlines(recv_buff.decode('utf-8'))
        print("{0:03d}({2:02d}): {1}".format(recv_count, lines, lines.__len__()))  # Split message per line.

        temp = str.split(recv_buff.decode('utf-8'), "\n")
        readbuffer = temp.pop()

        line_num = 0
        for line in lines:
            line_num += 1
            words = line.split()
            print(" -> {1:02d} - {0}".format(line, line_num))
            # print(" -> {0}".format(words))

            m = re.match("PING :(.*)", line)
            if m:
                irc.send(irc_msg.pong(m[1]))
                print("PING PONG!")

            m = re.match(":([^!]*)!(\S*) PRIVMSG (#\S+) :(.*)", line)
            if m:
                msg = m[4]
                print("MSG = {0}".format(msg))

                if msg == "~HELP~":
                    # irc.send(PRIVMSG(channel, data.__str__()))
                    s_msg = "I know these words: "
                    for qa in data:
                        s_msg = s_msg + qa + ", "
                    irc.send(irc_msg.privmsg(channel, s_msg))
                    irc.send(
                        irc_msg.privmsg(channel,
                                        "USE ~set~ [A] as [B], (like this: `~set~ 9487 as 94狂`), to set a Q&A pair."))
                else:
                    mm = re.match("~set~ (.+) as (.+)", msg)
                    if mm:
                        data.update({mm[1]: mm[2]})
                        irc.send(irc_msg.privmsg(channel, "DATA SET SUCCESSFUL: {0} as {1}.".format(mm[1], mm[2])))
                    else:
                        if msg in data:
                            irc.send(irc_msg.privmsg(channel, data[msg]))
        print()
    # irc.close()


if __name__ == '__main__':
    main()
