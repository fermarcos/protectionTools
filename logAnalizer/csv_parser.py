#!/usr/bin/env python
#####################################################################
# Python script to analyze logs. For Debian, Ubuntu and CentOS systems.
# Written by Fernando Marcos Parra Arroyo
# ###################################################################

import csv
import operator
from collections import OrderedDict
import re

def parse_CSV(report_lorg, blacklist,reportFile):
    regexes = [".*Nikto.*",".*OpenVAS.*"]
    combined = "(" + ")|(".join(regexes) + ")"

    codeResponses = dict()
    badIPRequests = dict()
    scanners = dict()
    xssAttacks = dict()
    sqliAttacks = dict()
    rfiAttacks = dict()
    lfiAttacks = dict()
    dtAttacks = dict()
    bots = dict()
    with open(report_lorg, 'rb') as csvfile:
        next(csvfile)
        spamreader = csv.reader(csvfile, delimiter=';')
        for row in spamreader:
            #print row
            if "xss" in row[1]: xssAttacks[row[2]] = xssAttacks.get(row[2] , 0) + 1
            if "sqli" in row[1]: sqliAttacks[row[2]] = sqliAttacks.get(row[2] , 0) + 1
            if "rfi" in row[1]: rfiAttacks[row[2]] = rfiAttacks.get(row[2] , 0) + 1
            if "lfi" in row[1]: lfiAttacks[row[2]] = lfiAttacks.get(row[2] , 0) + 1
            if "dt" in row[1]: dtAttacks[row[2]] = dtAttacks.get(row[2] , 0) + 1
            codeResponses[(row[2],row[7])] = codeResponses.get((row[2],row[7]) , 0) + 1
            badIPRequests[row[2]] = badIPRequests.get(row[2] , 0) + 1
            # Make a regex that matches if any of our regexes match.

            for r in regexes:
                if re.match(r, row[10]):
                    scanners[r] = scanners.get(r , 0) + 1
    with open(reportFile, 'a') as out:
        out.write("----------------------------------------------------------------------------------------------\n")
        out.write("----------------------------------------------------------------------------------------------\n")
        out.write("---------------------------------- "+report_lorg+" -------------------------------------------\n")
        out.write("----------------------------------------------------------------------------------------------\n")
        out.write("----------------------------------------------------------------------------------------------\n")
        out.write("----------------------------------------Response Codes----------------------------------------\n\n")
        top = sorted(codeResponses, key =codeResponses.get, reverse = True )
        for x in top[:10]:
            out.write("\tIP: "+x[0]+ "   \tResponse Code: "+str(x[1])+"\tTimes: "+str(codeResponses[x])+"\n")
        out.write("\n----------------------------------------Attack retries----------------------------------------\n\n")
        top = sorted(badIPRequests, key =badIPRequests.get, reverse = True )
        for y in top[:10]:
            out.write("\tIP: "+y+"   \tAttack Retries: "+str(badIPRequests[y])+"\n")
            if y not in blacklist:
                blacklist.append(y)
                print "BLOCKED "+y
        out.write("\n------------------------------------------- Scanners -----------------------------------------\n")
        top = sorted(scanners, key =scanners.get, reverse = True )
        for z in top[:10]:
            out.write("\tScanner: "+z+"   \tRequests: "+str(scanners[z])+"\n")
        out.write("\n-----------------------------------------XSS Attacks------------------------------------------\n")
        top = sorted(xssAttacks, key =xssAttacks.get, reverse = True )
        for x in top[:10]:
            out.write("\tIP: "+x+ "   \tTimes: "+str(xssAttacks[x])+"\n")
        out.write("\n----------------------------------------SQLi Attacks------------------------------------------\n\n")
        top = sorted(sqliAttacks, key =sqliAttacks.get, reverse = True )
        for x in top[:10]:
            out.write("\tIP: "+x+ "   \tTimes: "+str(sqliAttacks[x])+"\n")
        out.write("\n----------------------------------------RFI Attacks------------------------------------------\n\n")
        top = sorted(rfiAttacks, key =rfiAttacks.get, reverse = True )
        for x in top[:10]:
            out.write("\tIP: "+x+ "   \tTimes: "+str(rfiAttacks[x])+"\n")
        out.write("\n----------------------------------------LFI Attacks------------------------------------------\n\n")
        top = sorted(lfiAttacks, key =lfiAttacks.get, reverse = True )
        for x in top[:10]:
            out.write("\tIP: "+x+ "   \tTimes: "+str(lfiAttacks[x])+"\n")
        out.write("\n-------------------------------Directory Traversal Attacks-----------------------------------\n\n")
        top = sorted(dtAttacks, key =dtAttacks.get, reverse = True )
        for x in top[:10]:
            out.write("\tIP: "+x+ "   \tTimes: "+str(dtAttacks[x])+"\n")
#        out.write("\n----------------------------------------BOTS-------------------------------------------------\n\n")
#        top = sorted(bots, key =bots.get, reverse = True )
#        for x in top[:10]:
#            out.write("\tIP: "+x+ "   \tTimes: "+str(bots[x])+"\n")
