import os
#prueba http://localhost/awstats/awstats.pl?config=prueba.com

print "**************INSTALACION AWSTATS************************"
awstats = os.system('rpm -qa | grep awstats')
httpd=os.system('rpm -qa | grep httpd')
nginx=os.system('rpm -qa | grep nginx')
os.system('clear')
sitio="prueba.com"
if httpd and nginx == 256:
	print "No tienes instalado un servidor web (Apache-httpd o Nginx)"
	exit()
if nginx==0:
	site="prueba"
	print "Tienes ngnix"
	if awstats==256:
		print "Awstats No esta instalado"
		print "***Instalando***"
		os.system('yum install awstats')
		os.system('clear') 
		os.system("cp /etc/awstats/awstats.localhost.localdomain.conf /etc/awstats/awstats."+sitio+".conf")	
		os.system('sed -i "s,SiteDomain=\\\"localhost.localdomain\\\",SiteDomain=\\\""'+sitio+'"\\\",g" /etc/awstats/awstats.'+sitio+'.conf')
		os.system("sed -in '168 s/127\.0\.0\.1/127\.0\.0\.1 '"+ sitio+"'/g' /etc/awstats/awstats."+sitio+".conf")
		os.system('sed -i "s,LogFile=\\\"/var/log/httpd/access.log\\\",LogFile=\\\"/var/log/nginx/access.log\\\",g" /etc/awstats/awstats.'+sitio+'.conf')
		os.system("mkdir /usr/share/nginx/html\/"+site+"")
		os.system("perl /usr/share/awstats/wwwroot/cgi-bin/awstats.pl -config="+sitio+" -update -output > /usr/share/nginx/html\/"+site+"/"+site+".html")
		os.system("cp /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/"+sitio+".conf")
		os.system("sed -i '9 s,\/usr\/share\/nginx\/html,\/usr\/share\/nginx\/html\/'"+site+"',g' /etc/nginx/conf.d/"+sitio+".conf")
		os.system("sed -i '10 s/^/\\tindex '"+site+"'.html\\n/g' /etc/nginx/conf.d/"+sitio+".conf")	
		os.system('sed -i "s, default\_server,"' '",g" /etc/nginx/conf.d/'+sitio+'.conf')
		#	os.system("sed -i '28 s,localhost,'"+sitio+"',g' /etc/nginx/sites-enabled/"+sitio+"")
		os.system("service nginx restart")
		exit()

	else:
		print "Awstats Ya esta instalado"
		exit()