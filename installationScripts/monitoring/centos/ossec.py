import os


print "**************INSTALACION OSSEC************************"
while True:
	print "Do you wish install awstats?[s|N]"
	op=raw_input()
	if op=="n" or op=="N":
		exit()
	else:
		ossec=os.system('find /var/ossec')
		os.system('clear')
		if ossec==256:
			print "OSSEC No esta instalado"
			print "***Instalando***"
			os.system('yum install inotify-tools')
			os.system('wget -U ossec http://www.ossec.net/files/ossec-hids-2.8.1.tar.gz')
			os.system('tar -zxf ossec-hids-2.8.1.tar.gz')
			os.chdir("ossec-hids-2.8.1")
			print "***********INSTALACION OSSEC**************"
			os.system('./install.sh')
			os.system('clear') 

		else:
			print "OSSEC Ya esta instalado"
			exit()