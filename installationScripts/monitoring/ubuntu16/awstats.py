import os


print "**************INSTALLING AWSTATS ubuntu16************************"
correo="prueba@prueba.com"
sitio="www.localhost.com"
while True:
	print "Do you wish install awstats?[s|N]"
	op=raw_input()
	if op=="n" or op=="N":
		exit()
	else:
		
		apache=os.system('dpkg --get-selections | grep -w apache2 | grep -w install')
		nginx=os.system('dpkg --get-selections | grep -w nginx | grep -w install')
		prog1 = os.system('dpkg --get-selections | grep -w awstats | grep -w install')
		os.system('clear')
		if apache and nginx == 256:
			print "You don't have install a web server (Apache o Nginx)"
			exit()
		elif apache==0:
			print "You have apache"
			if prog1==256:
				print "Awstats is not install"
				print "***Instalando***"
				os.system('apt-get install awstats')
				os.system("apt-get install apache2-utils")
				os.system('clear') 
				os.system("cp /etc/awstats/awstats.conf /etc/awstats/awstats."+sitio+".conf")
				os.system('sed -i "50 s,access,access."'+sitio+'",g" /etc/awstats/awstats.'+sitio+'.conf')	
				os.system('sed -i "s,SiteDomain=\\\"\\\",SiteDomain=\\\""'+sitio+'"\\\",g" /etc/awstats/awstats.'+sitio+'.conf')
				os.system("sed -in '169 s/127\.0\.0\.1/127\.0\.0\.1 '"+ sitio+"'/g' /etc/awstats/awstats."+sitio+".conf")
				os.system("/usr/lib/cgi-bin/awstats.pl -config="+sitio+" -update")
				os.system("a2enmod cgi")
				os.system("sed -i '20 s/error/error.'"+sitio+"'/g' /etc/apache2/sites-available/000-default.conf")
				os.system("sed -i '21 s/access/access.'"+sitio+"'/g' /etc/apache2/sites-available/000-default.conf")
				os.system("sed -i '22 s/^/\\tAlias \/awstatsclasses \"\/usr\/share\/awstats\/lib\/\"\\n/g' /etc/apache2/sites-available/000-default.conf")
				os.system("sed -i '23 s/^/\\tAlias \/awstats\-icon \"\/usr\/share\/awstats\/icon\/\"\\n/g' /etc/apache2/sites-available/000-default.conf")
				os.system("sed -i '24 s/^/\\tAlias \/awstatscss \"\/usr\/share\/doc\/awstats\/examples\/css\"\\n/g' /etc/apache2/sites-available/000-default.conf")
				os.system("sed -i '25 s/^/\\tScriptAlias \/awstats\/ \/usr\/lib\/cgi\-bin\/\\n/g' /etc/apache2/sites-available/000-default.conf")
				os.system("sed -i '26 s/^/\\tOptions \+ExecCGI \-MultiViews \+SymLinksIfOwnerMatch\\n/g' /etc/apache2/sites-available/000-default.conf")
				os.system("sed -i '27 s/^/\\t \<Directory \/usr\/lib\/cgi\-bin\/\>\\n/g' /etc/apache2/sites-available/000-default.conf")
				os.system("sed -i '28 s/^/\\t AuthName \"Enter Your User Name and Password\"\\n/g' /etc/apache2/sites-available/000-default.conf")
				os.system("sed -i '29 s/^/\\t AuthType Basic\\n/g' /etc/apache2/sites-available/000-default.conf")
				os.system("sed -i '30 s/^/\\t AuthUserFile \/etc\/apache2\/auth\_users\\n/g' /etc/apache2/sites-available/000-default.conf")
				os.system("sed -i '31 s/^/\\t Require valid\-user\\n/g' /etc/apache2/sites-available/000-default.conf")
				os.system("sed -i '32 s/^/\\t \<\/Directory\>\\n/g' /etc/apache2/sites-available/000-default.conf")
				###HTTPS###
				os.system("sed -i '13 s/error/error.'"+sitio+"'/g' /etc/apache2/sites-available/default-ssl.conf")
				os.system("sed -i '14 s/access/access.'"+sitio+"'/g' /etc/apache2/sites-available/default-ssl.conf")
				os.system("sed -i '100 s/^/#/g' /etc/apache2/sites-available/default-ssl.conf")
				os.system("sed -i '101 s/^/\\t AuthName \"Enter Your User Name and Password\"\\n/g' /etc/apache2/sites-available/default-ssl.conf")
				os.system("sed -i '102 s/^/\\t AuthType Basic\\n/g' /etc/apache2/sites-available/default-ssl.conf")
				os.system("sed -i '103 s/^/\\t AuthUserFile \/etc\/apache2\/auth\_users\\n/g' /etc/apache2/sites-available/default-ssl.conf")
				os.system("sed -i '104 s/^/\\t Require valid\-user\\n/g' /etc/apache2/sites-available/default-ssl.conf")
				os.system("sed -i '106 s/^/\\tAlias \/awstatsclasses \"\/usr\/share\/awstats\/lib\/\"\\n/g' /etc/apache2/sites-available/default-ssl.conf")
				os.system("sed -i '107 s/^/\\tAlias \/awstats\-icon \"\/usr\/share\/awstats\/icon\/\"\\n/g' /etc/apache2/sites-available/default-ssl.conf")
				os.system("sed -i '108 s/^/\\tAlias \/awstatscss \"\/usr\/share\/doc\/awstats\/examples\/css\"\\n/g' /etc/apache2/sites-available/default-ssl.conf")
				os.system("sed -i '109 s/^/\\tScriptAlias \/awstats\/ \/usr\/lib\/cgi\-bin\/\\n/g' /etc/apache2/sites-available/default-ssl.conf")
				os.system("sed -i '110 s/^/\\tOptions \+ExecCGI \-MultiViews \+SymLinksIfOwnerMatch\\n/g' /etc/apache2/sites-available/default-ssl.conf")
				os.system("a2ensite default-ssl")
				os.system("a2enmod ssl")
				us=raw_input("Usuario para acceder a estadisticas: ")
				os.system("htpasswd -c /etc/apache2/auth_users "+us+"")
				os.system("service apache2 restart")
				exit()
			else:
				print "Awstats is installed"
				exit()
		elif nginx==0:
			site="prueba"
			print "You have ngnix"
			if prog1==256:
				print "Awstats is not install"
				print "***Instalando***"
				os.system('apt-get install awstats')
				os.system("apt-get install apache2-utils")
				os.system('clear') 
				os.system("cp /etc/awstats/awstats.conf /etc/awstats/awstats."+sitio+".conf")
				os.system('sed -i "s,SiteDomain=\\\"\\\",SiteDomain=\\\""'+sitio+'"\\\",g" /etc/awstats/awstats.'+sitio+'.conf')
				os.system("sed -in '169 s/127\.0\.0\.1/127\.0\.0\.1 '"+ sitio+"'/g' /etc/awstats/awstats."+sitio+".conf")
				os.system('sed -i "s,LogFile=\\\"/var/log/apache2/access.log\\\",LogFile=\\\"/var/log/nginx/access\."'+sitio+'"\.log\\\",g" /etc/awstats/awstats.'+sitio+'.conf')
				os.system("mkdir /var/www/html\/"+site+"")
				os.system("/usr/lib/cgi-bin/awstats.pl -config="+sitio+" -update -output > /var/www/html\/"+site+"/"+site+".html")
				os.system("cp /etc/nginx/sites-enabled/default /etc/nginx/sites-enabled/"+sitio+"")
				os.system("sed -i 's,\/var\/www\/html,\/var\/www\/html\/'"+site+"',g' /etc/nginx/sites-enabled/"+sitio+"")
				os.system("sed -i '39 s,index\.htm*,'"+site+"'.htm,g' /etc/nginx/sites-enabled/"+sitio+"")
				os.system('sed -i "s, default\_server,"' '",g" /etc/nginx/sites-enabled/'+sitio+'')
				os.system('sed -i "s, ipv6only\=on,"' '",g" /etc/nginx/sites-enabled/'+sitio+'')
				os.system("sed -i '22 s/#/'" "'/g' /etc/nginx/sites-enabled/"+sitio+"")	
				os.system("sed -i '34 s/#/'" "'/g' /etc/nginx/sites-enabled/"+sitio+"")	
				us=raw_input("Usuario para acceder a estadisticas: ")
				os.system("htpasswd -c /etc/nginx/"+sitio+".htpasswd "+us+"")
				os.system("sed -i '47 s/^/auth\_basic \"Basic Auth\"\;\\n/g' /etc/nginx/sites-enabled/"+sitio+"")
				os.system("sed -i '48 s/^/auth_basic_user_file  \"\/etc\/nginx\/'"+sitio+"'.htpasswd\"\;\\n/g' /etc/nginx/sites-enabled/"+sitio+"")
				os.system("sed -i '50 s/^/access_log \/var\/log\/nginx\/access.'"+sitio+"'\.log\;\\n/g' /etc/nginx/sites-enabled/"+sitio+"")
				os.system("sed -i '51 s/^/error_log \/var\/log\/nginx\/error.'"+sitio+"'\.log\;\\n/g' /etc/nginx/sites-enabled/"+sitio+"")	
				#os.system("apt-get install apache2-utils")
				#	os.system("sed -i '28 s,localhost,'"+sitio+"',g' /etc/nginx/sites-enabled/"+sitio+"")
				os.system("service nginx restart")
				exit()
			else:
				print "Awstats is installed	"
				exit()
		else:
			print "Error"