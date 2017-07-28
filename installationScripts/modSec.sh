#!/bin/bash

####################################################################
# Bash script to install waf-fle. For Debian, Ubuntu and CentOS systems.
# Written by Fernando Marcos Parra Arroyo
#	     Jorge Alberto Hernandez Cuecuecha
# Requirements:
#	Internet Connection
#	User Root
####################################################################

#COLORS
# Reset
Color_Off='\033[0m'       # Text Reset

# Regular Colors
Red='\033[0;31m'          # Red
Green='\033[0;32m'        # Green
Yellow='\033[0;33m'       # Yellow
Purple='\033[0;35m'       # Purple
Cyan='\033[0;36m'         # Cyan


#Detecting Operative System
DISTR=`grep -E "^ID=" /etc/*release | cut -d "=" -f2 |sed -r 's/"//g'`
VERSION=`grep -E "^VERSION_ID=" /etc/*release | cut -d "=" -f2 |sed -r 's/"//g'`
EXCEPT=`grep -i centos /etc/issue`


#Checking root permissions
echo -e "$Cyan \nChecking root permissions.. $Color_Off"
if [ "$(id -u)" != "0" ]; then
   echo -e  "$Red ERROR This script must be run as root $Color_Off" 1>&2
   exit 1
fi

#Detecting Operative System
function dependencies
{
	echo -e "$Cyan \nDetecting System.. $Color_Off"
	if [[ "$EXCEPT" == *"CentOS"*"6"* ]]; then
	        echo "CentOS 6"
	        rpm -Uvh --force https://epel.mirror.constant.com/6/i386/epel-release-6-8.noarch.rpm
	fi
	if [[ "$DISTR" == "centos" && "$VERSION" == "7"* ]]; then
	        echo "CentOS 7"
	        rpm -Uvh --force https://epel.mirror.constant.com/6/i386/epel-release-6-8.noarch.rpm
	fi
	if [[ "$DISTR" == "debian" && "$VERSION" == "8"* ]]; then
	        echo "Debian 8"
	        apt-get update
	fi
	if [[ "$DISTR" == "debian" && "$VERSION" == "9"* ]]; then
	        echo "Debian 9"
			apt-get update
	fi
	if [[ "$DISTR" == "ubuntu" && "$VERSION" == "16"* ]]; then
	        echo "Ubuntu 16"
	        apt-get update
	fi
	if [[ "$DISTR" == "ubuntu" && "$VERSION" == "14"* ]]; then
	        echo "Ubuntu 14"
	        apt-get update
	fi
}


#Detecting Operative System
function installing
{
        echo -e "$Cyan \nDetecting System.. $Color_Off"
        if [[ "$EXCEPT" == *"CentOS"*"6"* || "$DISTR" == "centos" ]]; then
			yum install mod_security  -y
			#Configuring ModSecurity
			echo -e "$Cyan \nConfiguring modsecurity $Color_Off"
			sed -i "s/SecRuleEngine DetectionOnly/SecRuleEngine On/" /etc/httpd/conf.d/mod_security.conf
			sed -i "s/SecResponseBodyAccess On/SecResponseBodyAccess Off/" /etc/httpd/conf.d/mod_security.conf
			echo -e "$Cyan \nRealoading Apache Service $Color_Off"
			service httpd restart
        fi
        if [[ "$DISTR" == "debian" || "$DISTR" == "ubuntu" ]]; then
			apt-get install libapache2-mod-security2 -y
			echo -e "$Cyan \nConfiguring modsecurity $Color_Off"
			if [ -f "/etc/modsecurity/modsecurity.conf-recommended" ]; then
				mv /etc/modsecurity/modsecurity.conf-recommended /etc/modsecurity/modsecurity.conf
			fi			
			sed -i "s/SecRuleEngine DetectionOnly/SecRuleEngine On/" /etc/modsecurity/modsecurity.conf
			sed -i "s/SecResponseBodyAccess On/SecResponseBodyAccess Off/" /etc/modsecurity/modsecurity.conf  
			echo -e "$Cyan \nRealoading Apache Service $Color_Off"
			a2enmod security2
			/etc/init.d/apache2 restart
        fi
}

function configuringRules
{
        if [[ "$EXCEPT" == *"CentOS"*"6"* || "$DISTR" == "centos" ]]; then

			echo -e "$Cyan \nDetecting Apache Version $Color_Off"
			httpd -v | grep version | cut -d" " -f3 
			V1=`httpd -v | grep version | cut -d" " -f3 | cut -d"/" -f2 | cut -d"." -f1`
			V2=`httpd -v | grep version | cut -d" " -f3 | cut -d"/" -f2 | cut -d"." -f2`
			V3=`httpd -v | grep version | cut -d" " -f3 | cut -d"/" -f2 | cut -d"." -f3`

			if [[ "$V1" -lt "2" || "$V2" -lt "4" || "$V3" -lt "11" ]]; then
			    echo "You need to upgrade Apache to a version equal to or greater than Apache 2.4.11 to apply the OWASP rule set. For more information visit https://github.com/SpiderLabs/owasp-modsecurity-crs/blob/v3.0.0-rc2/KNOWN_BUGS."

			    echo -e "$Cyan \nConfiguring Default Rules $Color_Off"
				sed -i "s/IncludeOptional \/etc\/modsecurity\/\*\.conf/IncludeOptional \/etc\/modsecurity\/\*\.conf \n\tIncludeOptional \/usr\/share\/modsecurity-crs\/\*\.conf \n\tIncludeOptional \/usr\/share\/modsecurity-crs\/activated_rules\/\*\.conf    /" /etc/apache2/mods-enabled/security2.conf
				yum install mod_security_crs -y
				mv /etc/httpd/modsecurity.d/activated_rules/modsecurity_crs_50_outbound.conf /etc/httpd/modsecurity.d/activated_rules/modsecurity_crs_50_outbound.conf.example
				mv /etc/httpd/modsecurity.d/activated_rules/modsecurity_crs_21_protocol_anomalies.conf /etc/httpd/modsecurity.d/activated_rules/modsecurity_crs_21_protocol_anomalies.conf.example
				mv /etc/httpd/modsecurity.d/activated_rules/modsecurity_crs_30_http_policy.conf /etc/httpd/modsecurity.d/activated_rules/modsecurity_crs_30_http_policy.conf.example
				service httpd restart	
			else
			    echo -e "$Cyan \nConfiguring OWASP Rules $Color_Off"
				#rm -rf /usr/share/modsecurity-crs
				#yum install -y git
				#git clone https://github.com/SpiderLabs/owasp-modsecurity-crs.git /usr/share/modsecurity-crs
				#cp /usr/share/modsecurity-crs/crs-setup.conf.example /usr/share/modsecurity-crs/crs-setup.conf
				#cp  /etc/apache2/mods-enabled/security2.conf /etc/apache2/mods-enabled/security2.conf.bak
				#sed -i "s/IncludeOptional \/etc\/modsecurity\/\*\.conf/IncludeOptional \/etc\/modsecurity\/\*\.conf \n\tIncludeOptional \/usr\/share\/modsecurity-crs\/\*\.conf \n\tIncludeOptional \/usr\/share\/modsecurity-crs\/rules\/\*\.conf    /" /etc/apache2/mods-enabled/security2.conf
				#/etc/init.d/apache2 restart
			fi
        fi

        if [[ "$DISTR" == "debian" && "$VERSION" == "8"* ]] || [ "$DISTR" == "ubuntu" ]; then

			echo -e "$Cyan \nDetecting Apache Version $Color_Off"
			apachectl -v | grep version | cut -d" " -f3 
			V1=`apachectl -v | grep version | cut -d" " -f3 | cut -d"/" -f2 | cut -d"." -f1`
			V2=`apachectl -v | grep version | cut -d" " -f3 | cut -d"/" -f2 | cut -d"." -f2`
			V3=`apachectl -v | grep version | cut -d" " -f3 | cut -d"/" -f2 | cut -d"." -f3`

			#echo $V1 $V2 $V3

			if [[ "$V1" -lt "2" || "$V2" -lt "4" || "$V3" -lt "11" ]]; then
				echo "You need to upgrade Apache to a version equal to or greater than Apache 2.4.11 to apply the OWASP rule set. For more information visit https://github.com/SpiderLabs/owasp-modsecurity-crs/blob/v3.0.0-rc2/KNOWN_BUGS."

				echo -e "$Cyan \nConfiguring Default Rules $Color_Off"
				sed -i "s/IncludeOptional \/etc\/modsecurity\/\*\.conf/IncludeOptional \/etc\/modsecurity\/\*\.conf \n\tIncludeOptional \/usr\/share\/modsecurity-crs\/\*\.conf \n\tIncludeOptional \/usr\/share\/modsecurity-crs\/activated_rules\/\*\.conf    /" /etc/apache2/mods-enabled/security2.conf
				cd /usr/share/modsecurity-crs/activated_rules
				ln -s ../base_rules/modsecurity_crs_41_xss_attacks.conf .
				ln -s ../base_rules/modsecurity_40_generic_attacks.data .
				ln -s ../base_rules/modsecurity_crs_40_generic_attacks.conf .
				ln -s ../base_rules/modsecurity_crs_41_sql_injection_attacks.conf .
				/etc/init.d/apache2 restart
				/etc/init.d/apache2 restart	
			else
				echo -e "$Cyan \nConfiguring OWASP Rules $Color_Off"
				rm -rf /usr/share/modsecurity-crs
				apt-get install -y git
				git clone https://github.com/SpiderLabs/owasp-modsecurity-crs.git /usr/share/modsecurity-crs
				cp /usr/share/modsecurity-crs/crs-setup.conf.example /usr/share/modsecurity-crs/crs-setup.conf
				cp  /etc/apache2/mods-enabled/security2.conf /etc/apache2/mods-enabled/security2.conf.bak
				sed -i "s/IncludeOptional \/etc\/modsecurity\/\*\.conf/IncludeOptional \/etc\/modsecurity\/\*\.conf \n\tIncludeOptional \/usr\/share\/modsecurity-crs\/\*\.conf \n\tIncludeOptional \/usr\/share\/modsecurity-crs\/rules\/\*\.conf    /" /etc/apache2/mods-enabled/security2.conf
				/etc/init.d/apache2 restart
			fi
        fi
}

dependencies
installing
configuringRules
