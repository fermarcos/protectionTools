#!/usr/bin/env python
# -*- coding: utf-8 -*-

#####################################################################
# Python script to analyze logs. For Debian, Ubuntu and CentOS systems.
# Written by Fernando Marcos Parra Arroyo
# ###################################################################



import apache_log_parser
import glob
import logging
import re

# supported log file formats
APACHE_COMBINED="%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\""
APACHE_COMMON="%h %l %u %t \"%r\" %>s %b"

def gulp(log_file_path, pattern=APACHE_COMBINED):
    """ import and parse log files """
    log_data=[]
    line_parser=apache_log_parser.make_parser(pattern)
    for file_name in glob.glob(log_file_path):
        logging.info("file_name: %s" % file_name)
        file = open(file_name, 'r')
        lines = file.readlines()
        file.close()
        logging.info(" read %s lines" % len(lines))
        for line in lines:
            line_data=line_parser(line)
            log_data.append(line_data)
    logging.info("total number of events parsed: %s" % len(log_data))
    return log_data

def analyseAccessLog(fileLog,blacklist,triesPerMinuteWeb,reportFile):
    print "----------------------Analyzing: "+fileLog+" ----------------------------------"
    bruteForce = dict()
    dosAttempt = dict()
    log_data = gulp(fileLog)
    count404=0
    print str(len(log_data))+ " events analyzed\n"
    with open(reportFile , 'a') as r:
        r.write(str(len(log_data))+ " events analyzed\n")
    for l in log_data:
    #    if "POST" in l['request_method']:
        hora = l['time_received'].split("[")[1].split(" ")[0].split(":")[0:3]
        hora = hora[0]+":"+hora[1]+":"+hora[2]
        ip = l['remote_host']
        url = l["request_url"]
        if re.match('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ip) != None:
            dosAttempt[(ip,hora)] = dosAttempt.get((ip,hora) , 0) + 1
            bruteForce[(ip,hora,url)] = bruteForce.get((ip,hora,url) , 0) + 1
    top = sorted(bruteForce, key =bruteForce.get, reverse = True )
    for f in top:
        if int(bruteForce[f]) >= int(triesPerMinuteWeb):
            print bruteForce[f]
            if f[0] not in blacklist:
        		blacklist.append(f[0])
        		print "BLOQUEADAAAAAA "+f[0]
        else:
            break

    with open(reportFile , 'a') as r:
        r.write("--------------------------------------------------------------------------------\n")
        r.write("--------------------------------------------------------------------------------\n")
        r.write("----------------------Analyzing: "+fileLog+" ----------------------------------\n")
        r.write("--------------------------------------------------------------------------------\n\n")
        top = sorted(bruteForce, key =bruteForce.get, reverse = True )
        r.write("\nRequests per minute to the same resource by the same ip\n")
        for x in top[:10]:
            r.write("\tIP: "+x[0]+ "   \tTimes: "+str(bruteForce[x])+"  \tTime: "+x[1]+ "   \URL: "+x[2]+"\n")
        top = sorted(dosAttempt, key =dosAttempt.get, reverse = True )
        r.write("\nRequests per minute by the same IP\n")
        for x in top[:10]:
            r.write("\tIP: "+x[0]+ "   \tTimes: "+str(dosAttempt[x])+"  \tTime: "+x[1]+"\n")
#analyseAccessLog("/var/log/apache2/access.log.old.gz.unc")
#analyseAccessLog("./access.log.old")
