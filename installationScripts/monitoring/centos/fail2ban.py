import os


print "**************INSTALACION Fail2ban************************"
while True:
	print "Do you wish install fail2ban?[s|N]"
	op=raw_input()
	if op=="n" or op=="N":
		exit()
	else:
		fail2ban=os.system('rpm -qa | grep fail2ban')
		apache=os.system('rpm -qa | grep httpd')
		nginx=os.system('rpm -qa | grep nginx')
		postgres=os.system('rpm -qa | grep postgresql')
		mysql=os.system('rpm -qa | grep mysql')
		os.system('clear')
		if apache and nginx == 256:
			print "No tienes instalado un servidor web (Apache o Nginx)"
			exit()
		if mysql==256:
			print "No tienes mysql"
			exit()
		if postgres==256:
			print "No tienes postgresql"
		if fail2ban==256:
			print "fail2ban No esta instalado"
			print "***Instalando***"
			#os.system('apt-get update')	
			os.system('rpm -q http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm')
			os.system('yum install fail2ban')
			os.system('clear')
			#Mysqsl	
			os.system("sed -in '730 s,%(mysql\_log)s,\/var\/log\/mysqld\.log,g' /etc/fail2ban/jail.conf ")
			os.system("sed -i '732 s/^/enabled\=true/g' /etc/fail2ban/jail.conf")	
			#Postgresql

			#mail
			correo="centos6@localhost"
			#dominio = subprocess.Popen("awk '{print $1}' /etc/centos-release", stdout=subprocess.PIPE, shell=True)
			#correo=nombre+"@"+dominio.rstrip('\n')
			os.system("sed -in '130 s/root\@localhost/'"+correo+"'/g' /etc/fail2ban/jail.conf ")	
			os.system("sed -in '213 s/action\_/action_mwl/g' /etc/fail2ban/jail.conf ")

			if apache==0:
				print "Tiene httpd"
				os.system("sed -in '369 s,%(lighttpd\_error\_log)s,\/var\/log\/httpd\/error\_log,g' /etc/fail2ban/jail.conf")
				os.system("sed -i '370 s/^/enabled\=true/g' /etc/fail2ban/jail.conf")	
				os.system("service fail2ban restart")
				os.system("fail2ban-client status")
				
			if nginx==0:
				print "Tienes nginx"
				os.system("sed -in '331 s,%(nginx\_error\_log)s,\/var\/log\/nginx\/error\.log,g' /etc/fail2ban/jail.conf")
				os.system("sed -i '332 s/^/enabled\=true/g' /etc/fail2ban/jail.conf")	
				os.system("service fail2ban restart")
				os.system("fail2ban-client status")
				exit()

		else:
			print "Fail2ban Ya esta instalado"	
			exit()