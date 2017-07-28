import os
import subprocess

VERCENT = subprocess.check_output("awk '{print $4}' /etc/centos-release", shell=True)
DISTRCENT = subprocess.check_output("awk '{print $1}' /etc/centos-release", shell=True)
print VERCENT
if DISTRCENT == "['CenOS']":
	print "Es cents"
elif DISTRCENT == "['CentOS']":
	print "Es cents"
else:
	print "problemas"