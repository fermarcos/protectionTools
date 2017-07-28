import os
import subprocess

print "**************INSTALLING LOGWATCH************************"
while True:
	print "Do you wish install logwatch?[s|N]"
	op=raw_input()
	if op=="n" or op=="N":
		exit()
	else:
		nombre="modulo4"
		dominio=subprocess.check_output('cat /etc/hostname', shell=True)
		correo=nombre+"@"+dominio.rstrip('\n')
		prog1 = os.system('dpkg --get-selections | grep -w logwatch | grep -w install')
		os.system('clear') 
		if prog1==256:
			print "Logwatch is not install"
			print "***Instalando***"
			os.system('apt-get install logwatch')
			os.system('clear') 
			os.system('sed -i "s/root/"'+correo+'"/g" /usr/share/logwatch/default.conf/logwatch.conf')
			os.system('sed -i "8 s/^/\/usr\/sbin\/logwatch \-\-mailto"'+correo+'"/g" /etc/cron.daily/00logwatch')
			os.system('logwatch --detail Low --mailto '+correo+' --service all --range today')
			exit()

		else:
			print "Logwatch is installed"
			os.system('sed -i "8 s/^/\/usr\/sbin\/logwatch \-\-mailto "'+correo+'"/g" /etc/cron.daily/00logwatch')

			exit()