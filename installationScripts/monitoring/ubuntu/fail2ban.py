import os
import subprocess

print "**************INSTALLING Fail2ban************************"
while True:
	print "Do you wish install fail2ban?[s|N]"
	op=raw_input()
	if op=="n" or op=="N":
		exit()
	else:
		
		fail2ban=os.system('dpkg --get-selections | grep -w fail2ban | grep -w install')
		apache=os.system('dpkg --get-selections | grep -w apache2 | grep -w install')
		nginx=os.system('dpkg --get-selections | grep -w nginx | grep -w install')
		postgres=os.system('dpkg --get-selections | grep -w postgresql | grep -w install')
		mysql=os.system('dpkg --get-selections | grep -w mysql | grep -w install')
		os.system('clear')
		if apache and nginx == 256:
			print "You don't have install a web server (Apache o Nginx)"
		if mysql==256:
			print "You don't have mysql"
		if postgres==256:
			print "You don't have postgresql"
		if fail2ban==256:
			print "fail2ban is not installed"
			print "***Installing***"
			#os.system('apt-get update')	
			os.system('apt-get install build-essential fail2ban')
			os.system('cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.conf.back')
			os.system('clear')
			#Mysqsl
			os.system("sed -in '402 s/false/true/g' /etc/fail2ban/jail.conf ")	
			os.system("sed -in '405 s,mysqld\.q,mysql\.log,g' /etc/fail2ban/jail.conf ")	
			#Postgresql
			
			#mail
			nombre="modulo4"
			dominio=subprocess.check_output('cat /etc/hostname', shell=True)
			correo=nombre+"@"+dominio.rstrip('\n')
			os.system("sed -in '57 s/root\@localhost/'"+correo+"'/g' /etc/fail2ban/jail.conf ")	
			os.system("sed -in '102 s/action\_/action_mwl/g' /etc/fail2ban/jail.conf ")

			if apache==0:
				os.system("sed -in '210 s/false/true/g' /etc/fail2ban/jail.conf")
				os.system("sed -in '213 s,apache\*\/\*error.log,apache2\/error.log,g' /etc/fail2ban/jail.conf ")
				os.system("service fail2ban restart")
				os.system("fail2ban-client status")
				exit()
			if nginx==0:
				os.system("sed -in '278 s/false/true/g' /etc/fail2ban/jail.conf")
				os.system("service fail2ban restart")
				os.system("fail2ban-client status")
				exit()


		else:
			print "Fail2ban is not installed"	
			exit()