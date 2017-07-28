import os
#prueba http://localhost/awstats/awstats.pl?config=prueba.com

print "**************INSTALACION AWSTATS************************"
while True:
	print "Do you wish install awstats?[s|N]"
	op=raw_input()
	if op=="n" or op=="N":
		exit()
	else:
		awstats = os.system('rpm -qa | grep awstats')
		httpd=os.system('rpm -qa | grep httpd')
		nginx=os.system('rpm -qa | grep nginx')
		os.system('clear')
		sitio="prueba.com"
		if httpd and nginx == 256:
			print "No tienes instalado un servidor web (Apache-httpd o Nginx)"
			exit()
		if httpd==0:
			print "Tienes Apache-httpd"
			if awstats==256:
				print "Awstats No esta instalado"
				print "***Instalando***"
				os.system('yum install awstats')
				os.system("yum install mod_ssl")
				os.system("yum install httpd-tools")
				os.system('clear') 
				os.system("cp /etc/awstats/awstats.localhost.localdomain.conf /etc/awstats/awstats."+sitio+".conf")	
				os.system('sed -i "s,SiteDomain=\\\"localhost.localdomain\\\",SiteDomain=\\\""'+sitio+'"\\\",g" /etc/awstats/awstats.'+sitio+'.conf')
				os.system("sed -in '168 s/127\.0\.0\.1/127\.0\.0\.1 www.'"+ sitio+"'/g' /etc/awstats/awstats."+sitio+".conf")
				os.system("perl /usr/share/awstats/wwwroot/cgi-bin/awstats.pl -config="+sitio+" -update")

				##auth-basic##
				os.system("sed -i '19 s/^/\<Directory \"\/usr\/share\/awstats\/wwwroot\"\>\\n/g' /etc/httpd/conf.d/awstats.conf")
				os.system("sed -i '20 s/^/\\t AuthName \"Enter Your User Name and Password\"\\n/g' /etc/httpd/conf.d/awstats.conf")
				os.system("sed -i '21 s/^/\\t AuthType Basic\\n/g' /etc/httpd/conf.d/awstats.conf")
				os.system("sed -i '22 s/^/\\t AuthUserFile \/etc\/awstats\/'"+sitio+"'.htpasswd\\n/g' /etc/httpd/conf.d/awstats.conf")
				os.system("sed -i '23 s/^/\\t Require valid\-user\\n/g' /etc/httpd/conf.d/awstats.conf")
				os.system("sed -i '24 s/^/\<\/Directory\>\\n/g' /etc/httpd/conf.d/awstats.conf")
				os.system("sed -in '33 s/^/\#/g' /etc/httpd/conf.d/awstats.conf")

				us=raw_input("Usuario para acceder a estadisticas: ")
				os.system("htpasswd -c /etc/awstats/"+sitio+".htpasswd "+us+"")
				os.system("service httpd restart")
				exit()
			else:
				print "Awstats Ya esta instalado"
				exit()
		if nginx==0:
			site="prueba"
			print "Tienes ngnix"
			if awstats==256:
				print "Awstats No esta instalado"
				print "***Instalando***"
				os.system('yum install awstats')
				os.system("yum install httpd-tools")
				os.system('clear') 
				os.system("cp /etc/awstats/awstats.localhost.localdomain.conf /etc/awstats/awstats."+sitio+".conf")	
				os.system('sed -i "s,SiteDomain=\\\"localhost.localdomain\\\",SiteDomain=\\\""'+sitio+'"\\\",g" /etc/awstats/awstats.'+sitio+'.conf')
				os.system("sed -in '168 s/127\.0\.0\.1/127\.0\.0\.1 '"+ sitio+"'/g' /etc/awstats/awstats."+sitio+".conf")
				os.system('sed -i "s,LogFile=\\\"/var/log/httpd/access.log\\\",LogFile=\\\"/var/log/nginx/access.log\\\",g" /etc/awstats/awstats.'+sitio+'.conf')
				os.system("mkdir /usr/share/nginx/html\/"+site+"")
				os.system("perl /usr/share/awstats/wwwroot/cgi-bin/awstats.pl -config="+sitio+" -update -output > /usr/share/nginx/html\/"+site+"/"+site+".html")
				os.system("cp /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/"+sitio+".conf")
				os.system("sed -i '8 s,\_\;,'"+sitio+"'\;,g' /etc/nginx/conf.d/"+sitio+".conf")
				os.system("sed -i '9 s,\/usr\/share\/nginx\/html,\/usr\/share\/nginx\/html\/'"+site+"',g' /etc/nginx/conf.d/"+sitio+".conf")
				os.system("sed -i '10 s/^/\\tindex '"+site+"'.html;\\n/g' /etc/nginx/conf.d/"+sitio+".conf")	
				os.system('sed -i "s, default\_server,"' '",g" /etc/nginx/conf.d/'+sitio+'.conf')
				os.system("sed -i '11 s/^/\\t listen 443 ssl\;\\n/g' /etc/nginx/conf.d/"+sitio+".conf")	
				os.system("sed -i '12 s/^/\\t ssl on\;\\n/g' /etc/nginx/conf.d/"+sitio+".conf")	
				os.system("sed -i '13 s/^/\\t ssl\_certificate \/etc\/nginx\/ssl\/server\.crt\;\\n/g' /etc/nginx/conf.d/"+sitio+".conf")	
				os.system("sed -i '14 s/^/\\t ssl\_certificate\_key \/etc\/nginx\/ssl\/server\.key\;\\n/g' /etc/nginx/conf.d/"+sitio+".conf")	
				os.system("sed -i '20 s/^/\\t auth_basic \"Basic Auth\"\;\\n/g' /etc/nginx/conf.d/"+sitio+".conf")	
				os.system("sed -i '21 s/^/\\t auth\_basic\_user\_file  \"\/etc\/nginx\/'"+sitio+"'\.htpasswd\"\;\\n/g' /etc/nginx/conf.d/"+sitio+".conf")
				os.system("sed -i '31 s/^/\\t access\_log  \/var\/log\/nginx\/access\.'"+sitio+"'\.log\;\\n/g' /etc/nginx/conf.d/"+sitio+".conf")	
				os.system("sed -i '32 s/^/\\t error\_log  \/var\/log\/nginx\/error\.'"+sitio+"'\.log\;\\n/g' /etc/nginx/conf.d/"+sitio+".conf")	
				us=raw_input("Usuario para acceder a estadisticas: ")
				os.system("htpasswd -c /etc/nginx/"+sitio+".htpasswd "+us+"")
				os.system("service nginx restart")
				exit()

			else:
				print "Awstats is installed"
				exit()
			