import os
print "***************INSTALACION LOGWATCH***********************"
while True:
	print "Do you wish install logwatch?[s|N]"
	op=raw_input()
	if op=="n" or op=="N":
		exit()
	else:
		correo="modulo4@localhost"
		prog1 = os.system('rpm -qa | grep logwatch')
		os.system('clear') 
		if prog1==256:
			print "Logwatch No esta instalado"
			print "***Instalando***"
			os.system('yum install -y logwatch')
			os.system('clear') 
			os.system('sed -i "s/root/"'+correo+'"/g" /usr/share/logwatch/default.conf/logwatch.conf')
			os.system('logwatch --detail Low --mailto '+correo+' --service all --range today')
			exit()
		else:
			print "Logwatch is installed"
			exit()