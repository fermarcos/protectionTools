#!/bin/bash

####################################################################
# Bash script to install modsecurity. For Debian, Ubuntu and CentOS systems.
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

#Checking root permissions
echo -e "$Cyan \nChecking root permissions.. $Color_Off"
if [ "$(id -u)" != "0" ]; then
   echo -e  "$Red ERROR This script must be run as root $Color_Off" 1>&2
   exit 1
fi

#Detecting Operative System
echo -e "$Cyan \nDetecting System.. $Color_Off"

DISTRC=`grep "^Cen" /etc/centos-release | awk '{print $1}'`
VERSIONC=`awk '{print $3}' /etc/centos-release | cut -d"". -f1`
VERSIONC7=`awk '{print $4}' /etc/centos-release | cut -d "." -f1`
DISTR=`grep -E "^ID=" /etc/*release | cut -d "=" -f2 |sed -r 's/"//g'` 
VERSION=`grep -E "^VERSION_ID=" /etc/*release | cut -d "=" -f2 |sed -r 's/"//g'`

case $DISTRC in
  CentOS)
       echo "CentOS "$VERSION $VERSIONC" detected"
       if [[ "$VERSIONC" == "7" ]]; then
         if [ -e "centos7/awstats.py" ]; then
          python centos/awstats.py
         else
           echo -e "$Red Script awstats.py not found $Color_Off"
           read -n 1 -s -r -p "Press [s|S] to exit: [Continue]" op
           echo $op
           if [[ "$op" == "s" || "$op" == "S" ]]; then
             exit 1
           fi
           echo -e "\n"
         fi
       fi
       if [[ "$VERSIONC" == "6" ]]; then
         if [ -e "centos/awstats.py" ]; then
           python centos/awstats.py
         else
           echo -e "$Red Script awstats.py not found $Color_Off"
           read -n 1 -s -r -p "Press [s|S] to exit: [Continue]" op
           echo $op
           if [[ "$op" == "s" || "$op" == "S" ]]; then
             exit 1
           fi
           echo -e "\n"
         fi
       fi
       if [ -e "centos/fail2ban.py" ]; then
         python centos/fail2ban.py
       else
         echo -e "\n $Red Script fail2ban.py not found $Color_Off"
         read -n 1 -s -r -p "Press [s|S] to exit: [Continue] " op
         if [[ "$op" == "s" || "$op" == "S" ]]; then
           exit 1
         fi
         echo -e "\n"
       fi
       if [ -e "centos/logwatch.py" ]; then
         python centos/logwatch.py
       else
         echo -e "\n $Red Script logwatch.py not found $Color_Off"
         read -n 1 -s -r -p "Press [s|S] to exit: [Continue] " op
         if [[ "$op" == "s" || "$op" == "S" ]]; then
           exit 1
         fi
         echo -e "\n"

       fi
       if [ -e "centos/ossec.py" ]; then
         python centos/ossec.py
       else
         echo -e "\n $Red Script ossec.py not found $Color_Off"
         read -n 1 -s -r -p "Press [s|S] to exit: [Continue] " op
         if [[ "$op" == "s" || "$op" == "S" ]]; then
           exit 1
         fi
         echo -e "\n"
       fi
       ;;
esac

case $DISTR in
     ubuntu)
          echo "ubuntu "$VERSION" detected"
          if [[ "$VERSION" == "14.04" ]]; then
            if [ -e "ubuntu/awstats.py" ]; then
              python centos/awstats.py
            else
              echo -e "$Red Script awstats.py not found $Color_Off"
              read -n 1 -s -r -p "Press [s|S] to exit: [Continue]" op
              echo $op
              if [[ "$op" == "s" || "$op" == "S" ]]; then
                exit 1
              fi
                echo -e "\n"
            fi
          fi
          if [[ "$VERSION" == "16.04" ]]; then
              if [ -e "ubuntu16/awstats.py" ]; then
                python centos/awstats.py
              else
                echo -e "$Red Script awstats.py not found $Color_Off"
                read -n 1 -s -r -p "Press [s|S] to exit: [Continue]" op
                echo $op
                if [[ "$op" == "s" || "$op" == "S" ]]; then
                  exit 1
                fi
                  echo -e "\n"
              fi
            
          fi
          if [[ "$VERSION" == "14.04" ]]; then
            if [ -e "ubuntu/fail2ban.py" ]; then
              python ubuntu/fail2ban.py
            else
              echo -e "$Red Script fail2ban.py not found $Color_Off"
              read -n 1 -s -r -p "Press [s|S] to exit: [Continue]" op
              echo $op
              if [[ "$op" == "s" || "$op" == "S" ]]; then
                exit 1
              fi
              echo -e "\n"
            fi
          fi
          if [[ "$VERSION" == "16.04" ]]; then
            if [ -e "ubuntu/fail2ban.py" ]; then
              python ubuntu/fail2ban.py
            else
              echo -e "$Red Script fail2ban.py not found $Color_Off"
              read -n 1 -s -r -p "Press [s|S] to exit: [Continue]" op
              echo $op
              if [[ "$op" == "s" || "$op" == "S" ]]; then
                exit 1
              fi
              echo -e "\n"
            fi
          fi
          if [ -e "ubuntu/logwatch.py" ]; then
            python ubuntu/logwatch.py
          else
            echo -e "\n $Red Script logwatch.py not found $Color_Off"
            read -n 1 -s -r -p "Press [s|S] to exit: [Continue] " op
            if [[ "$op" == "s" || "$op" == "S" ]]; then
              exit 1
            fi
            echo -e "\n"

          fi
          if [ -e "ubuntu/ossec.py" ]; then
            python ubuntu/ossec.py
          else
            echo -e "\n $Red Script ossec.py not found $Color_Off"
            read -n 1 -s -r -p "Press [s|S] to exit: [Continue] " op
            if [[ "$op" == "s" || "$op" == "S" ]]; then
              exit 1
            fi
            echo -e "\n"
          fi
          ;;

     debian)
          echo "Debian "$VERSION" detected"
          if [ -e "ubuntu/awstats.py" ]; then
            python centos/awstats.py
          else
            echo -e "$Red Script awstats.py not found $Color_Off"
            read -n 1 -s -r -p "Press [s|S] to exit: [Continue]" op
            echo $op
            if [[ "$op" == "s" || "$op" == "S" ]]; then
              exit 1
            fi
              echo -e "\n"
          fi
  
          if [ -e "debian/fail2ban.py" ]; then
            python debian/fail2ban.py
          else
            echo -e "$Red Script fail2ban.py not found $Color_Off"
            read -n 1 -s -r -p "Press [s|S] to exit: [Continue]" op
            echo $op
            if [[ "$op" == "s" || "$op" == "S" ]]; then
              exit 1
            fi
            echo -e "\n"
          fi
      
          if [ -e "ubuntu/logwatch.py" ]; then
            python ubuntu/logwatch.py
          else
            echo -e "\n $Red Script logwatch.py not found $Color_Off"
            read -n 1 -s -r -p "Press [s|S] to exit: [Continue] " op
            if [[ "$op" == "s" || "$op" == "S" ]]; then
              exit 1
            fi
            echo -e "\n"

          fi
          if [ -e "ubuntu/ossec.py" ]; then
            python ubuntu/ossec.py
          else
            echo -e "\n $Red Script ossec.py not found $Color_Off"
            read -n 1 -s -r -p "Press [s|S] to exit: [Continue] " op
            if [[ "$op" == "s" || "$op" == "S" ]]; then
              exit 1
            fi
            echo -e "\n"
          fi
          ;; 
esac
