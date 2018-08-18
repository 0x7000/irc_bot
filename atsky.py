#!/usr/bin/env python3
import ssl
import socket
import threading
import random
import time


def main():
	SSLIRC.connect((SERVER, PORT))
	sendmsg("NICK "+IRCUSER+my_nick())
	sendmsg("USER "+IRCUSER+" "+IRCUSER+" "+IRCUSER+" :ATSKY_AI")
	privmsg("identify "+IRCUSER+" "+IRCPASS, "nickserv")
	sendmsg("JOIN "+CHAN)
	while 1:
		try:
			time.sleep(0.1)
			buff = SSLIRC.recv(4096)
			buff = buff.decode("UTF-8").strip()
			t1 = threading.Thread(target=console, args=(buff,))
			t1.start()
			if QUIT == 1:
				break
		except Exception as e:
			print("Sorunlu bağlantı... {}".format(e))
			

def sendmsg(mesaj):
	SSLIRC.send(bytes(mesaj+"\r\n", "UTF-8"))


def privmsg(mesaj, nick):
	sendmsg("PRIVMSG "+nick+" :"+mesaj)


def console(mesaj):
	# :command!~command@unaffiliated/command PRIVMSG #dedeler :selam olsun
	# :command!~command@unaffiliated/command PRIVMSG atsky_qxh :VERSION
	msg_array = mesaj.split(" ")
	if msg_array[0] == "PING":
		# ping pong bağlantı kontrolü
		sendmsg("PONG "+msg_array[1])
		print(SAAT+" PONG "+msg_array[1])
	else:
		ircnick = msg_array[0].split("!")[0].lstrip(":")
		# irckanal bazı durumlarda privmsg gönderen kişidir yani mesajı gönderen neyse odur
		irckanal = msg_array[2]
		try:
			ircmesaj = msg_array[3:]
		except Exception as e:
			ircmesaj = ["Hatalı", "Mesaj", e]
		if ircmesaj:
			# versiyon "non print" karakterler var silmeden önce iki kez düşünün
			if ircmesaj[0] == ":VERSION":
				privmsg("VERSION ATSKY IRC BOT", ircnick)
			if ircmesaj[0] == ":!kill" and ircnick in ADMIN:
				global QUIT
				QUIT = 1
			else:
				if irckanal.startswith("#"):
					print("{} {} {} {}".format(SAAT, irckanal, ircnick, ircmesaj))


def my_nick():
	nick = "_"
	rng = "1a2s3d4q5w6e7z8x9c0h"
	for i in range(1, 4):
		nick += random.choice(rng)
	return nick


SAAT = time.strftime("%H:%M:%S")
IRC = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
IRC.settimeout(300)
SSLIRC = ssl.wrap_socket(IRC)
SERVER = "chat.freenode.net"
CHAN = "#dedeler"
IRCUSER = "atsky"
IRCPASS = "sanane123456"
PORT = 6697
QUIT = 0
ADMIN = ["command", "cmdexe", "0x7000"]


if __name__ == "__main__":
	main()
