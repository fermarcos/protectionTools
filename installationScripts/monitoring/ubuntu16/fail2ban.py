import os
import subprocess

print "**************INSTALLING Fail2ban ubuntu 16************************"
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
			os.system("sed -i '690 s/^/enabled\=true/g' /etc/fail2ban/jail.conf")
			os.system("sed -in '688 s,%(mysql\_log)s,\/var\/log\/mysql\/error\.log,g' /etc/fail2ban/jail.conf")	
			#Postgresql
			
			#mail
			nombre="modulo4"
			dominio=subprocess.check_output('cat /etc/hostname', shell=True)
			correo=nombre+"@"+dominio.rstrip('\n')
			os.system("sed -in '129 s/root\@localhost/'"+correo+"'/g' /etc/fail2ban/jail.conf ")	
			os.system("sed -in '204 s/action\_/action_mwl/g' /etc/fail2ban/jail.conf ")

			if apache==0:
				os.system("sed -i '250 s/^/enabled\=true/g' /etc/fail2ban/jail.conf")
				os.system("sed -i '259 s/^/enabled\=true/g' /etc/fail2ban/jail.conf")
				os.system("sed -i '266 s/^/enabled\=true/g' /etc/fail2ban/jail.conf")
				os.system("sed -i '273 s/^/enabled\=true/g' /etc/fail2ban/jail.conf")
				os.system("sed -i '280 s/^/enabled\=true/g' /etc/fail2ban/jail.conf")
				os.system("sed -i '295 s/^/enabled\=true/g' /etc/fail2ban/jail.conf")
				os.system("sed -i '302 s/^/enabled\=true/g' /etc/fail2ban/jail.conf")
				os.system("sed -i '308 s/^/enabled\=true/g' /etc/fail2ban/jail.conf")
				os.system("sed -i '308 s/^/enabled\=true/g' /etc/fail2ban/jail.conf")
				os.system("sed -i 's,%(apache\_error\_log)s,\/var\/log\/apache2\/error\.log,g' /etc/fail2ban/jail.conf")
				os.system("service fail2ban restart")
				os.system("fail2ban-client status")
				exit()
			if nginx==0:
				os.system("sed -i '313 s/^/enabled\=true/g' /etc/fail2ban/jail.conf")
				os.system("sed -i '319 s/^/enabled\=true/g' /etc/fail2ban/jail.conf")
				os.system("sed -in '312 s,%(nginx\_error\_log)s,\/var\/log\/nginx\/error\.log,g' /etc/fail2ban/jail.conf")
				os.system("sed -in '317 s,%(nginx\_error\_log)s,\/var\/log\/nginx\/error\.log,g' /etc/fail2ban/jail.conf")
				os.system("service fail2ban restart")
				os.system("fail2ban-client status")
				exit()


		else:
			print "Fail2ban is not installed"	
			exit()