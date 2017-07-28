#!/usr/bin/python
#####################################################################
# Python script to analyze logs. For Debian, Ubuntu and CentOS systems.
# Written by Fernando Marcos Parra Arroyo
# ###################################################################
import csv
import operator
from collections import OrderedDict
import re
import sys
import os
import itertools
import ConfigParser
from optparse import OptionParser
from re import match
from csv_parser import *
from parser import *

#Funcion para cargar la configuracion
def loadConfig(fileConf):
    global apache2_Path, httpd_Path, nginx_Path, mysql_Path, postgresql_Path
    global filesApache, filesHttpd, filesMysql,filesPostgres
    global triesPerMinuteWeb, triesMysql, triesPostgresql
    global blacklist
    #Cargando configuraciones
    config = ConfigParser.ConfigParser()
    config.read(fileConf)
    #Path de los logs
    apache2_Path = config.get("logs", "apache2")
    httpd_Path = config.get("logs", "httpd")
    nginx_Path = config.get("logs", "nginx")
    mysql_Path = config.get("logs", "mysql")
    postgresql_Path = config.get("logs", "postgresql")
    #Nombres de los archivos a analizar
    filesApache = config.get("filenames", "apache2").replace(" ", "").split(',')
    filesMysql = config.get("filenames", "mysql").replace(" ", "").split(',')
    filesPostgres = config.get("filenames", "postgresql").replace(" ", "").split(',')
    filesHttpd = config.get("filenames", "httpd").replace(" ", "").split(',')
    #Configuracion de bruteForce
    triesPerMinuteWeb = config.get("bruteForce", "triesPerMinuteWeb")
    triesMysql = config.get("bruteForce", "triesMysql")
    triesPostgresql = config.get("bruteForce", "triesPostgresql")

    blacklist = []
#Funcion para imprimir mensaje de eror y salir
def printError(message):
    sys.stderr.write("Error: %s" % message)
    sys.exit(1)

def checkOptions(opts):
    if opts.out is None: printError("Please enter the name of the report with -o\n")
    if opts.blacklist is None: printError("Please enter the name of the blacklist with -l\n")
    if opts.config is None: printError("Please enter the name of the configuration file with -c\n")

def addOptions():
    parser = OptionParser()
    parser.add_option("-c", "--config", dest="config", default=None, help="File config")
    parser.add_option("-o", "--out", dest="out", default=None, help="Name for the report")
    parser.add_option("-l", "--blacklist", dest="blacklist", default=None, help="Name for the blacklist")
    return parser

#Funcion que obtiene una lista de las bitacoras a analizar
def getFilesToAnalize(files, logFiles):
    filesToAnalize = []
    for f in logFiles:
        filesToAnalize.append([s for s in files if f in s])
    filesToAnalize = list(itertools.chain.from_iterable(filesToAnalize))
    for i,f in enumerate(filesToAnalize):
        if "gz" in f and ".unc" not in f:
            file_uncompressed = f+".unc"
            cmd = "zcat "+f+" | head -n -1 > "+file_uncompressed
            x = os.popen(cmd)
            now = x.read()
            print now
            print cmd
            filesToAnalize[i] = file_uncompressed
    print filesToAnalize
    return  filesToAnalize

#Funcion para analizar los logs de servicios web
def analyzeApacheLogs(files, filesApache,reportFile):
    logs = getFilesToAnalize(files, filesApache)
    for l in logs:
        if os.path.isfile(l):
            analyseAccessLog(l,blacklist,triesPerMinuteWeb,reportFile)
            report_lorg= os.path.basename(l)+".csv"
            print "\n\n------------------------------------Analyzing: "+l+" with lorg... wait a moment please--------------------"
            cmd = "./lorg -d phpids -o csv -u -g "+l+" "+report_lorg
            print cmd
            f = os.popen(cmd)
            now = f.read()
        if os.path.isfile("./"+report_lorg) and os.stat("./"+report_lorg).st_size > 0:
            parse_CSV(report_lorg,blacklist,reportFile)
        else:
            print "ERROR: "+l+" doesn't exist or it doesn't have attacks"

#Funcion para analizar los logs de mysql
def analyzeMysqlLogs(files, filesMysql,reportFile):
    logs = getFilesToAnalize(files, filesMysql)
    for l in logs:
        failedTries =dict()
        connections = []
        print "\n\Analyzing "+l
        with open(l) as f:
            lines = f.readlines()
            for line in lines:
                if re.match(".*Connect.*denied.*password: YES", line) is not None:
                    badIP = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)
                    if badIP  is not None:
                        failedTries[badIP.group()] = failedTries.get(badIP.group() , 0) + 1
        for f in failedTries:
            if failedTries[f] >= triesPostgresql:
                if f not in blacklist:
                    blacklist.append(f)
                    print "BLOCKED "+f
        top = sorted(failedTries, key =failedTries.get, reverse = True )
        for f in top:
            if int(failedTries[f]) >= int(triesPostgresql):
                print failedTries[f]
                if f not in blacklist:
                    blacklist.append(f)
                    print "BLOCKED "+f
            else:
                break

        with open(reportFile, 'a') as out:
            out.write("----------------------------------------------------------------------------------------------\n")
            out.write("----------------------------------------------------------------------------------------------\n")
            out.write("--------------------------"+l+"-----------------------------------------\n")
            out.write("----------------------------------------------------------------------------------------------\n")
            out.write("----------------------------------------------------------------------------------------------\n")
            out.write("---------------------MySQL Failed Authentication Tries----------------------------------------\n\n")
            for f in failedTries:
                out.write("\tIP: "+f+"   \tTimes: "+str(failedTries[f])+"\n")

def createBlackList(iplist,blacklistFile):
    with open(blacklistFile, 'w') as out:
        for ip in iplist:
             out.write(ip+"\n")
#Funcion para analizar los logs de mysql
def analyzePostgresLogs(files, filesMysql,reportFile):
    logs = getFilesToAnalize(files, filesMysql)
    for l in logs:
        failedTries =dict()
        connections = []
        print "\n\Analyzing "+l
        with open(l) as f:
            lines = f.readlines()
            for line in lines:
                if re.match(".*password authentication failed for user.*", line) is not None:
                    badIP = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)
                    fecha = re.search(r'\d\d\d\d-\d\d-\d\d', line)
                    hora = re.search(r'\d\d:\d\d:', line)
                    user = re.search(r'[A-Z0-9a-z_-]+@[A-Za-z0-9_-]+', line)
                    if badIP  is not None and user is not None:
                        failedTries[(badIP.group(),fecha.group(),hora.group(),user.group())] = failedTries.get((badIP.group(),fecha.group(),hora.group(),user.group()) , 0) + 1

        top = sorted(failedTries, key =failedTries.get, reverse = True )
        for f in top:
            if int(failedTries[f]) >= int(triesPostgresql):
                print bruteForce[f]
                if f[0] not in blacklist:
                    blacklist.append(f[0])
                    print "BLOQUEADAAAAAA "+f[0]
            else:
                break


        with open(reportFile, 'a') as out:
            out.write("----------------------------------------------------------------------------------------------\n")
            out.write("----------------------------------------------------------------------------------------------\n")
            out.write("--------------------------"+l+"-----------------------------------------\n")
            out.write("----------------------------------------------------------------------------------------------\n")
            out.write("----------------------------------------------------------------------------------------------\n")
            out.write("---------------------postgresql Failed Authentication Tries----------------------------------------\n\n")
            top = sorted(failedTries, key =failedTries.get, reverse = True )
            for f in top[:10]:
                out.write("\tIP: "+f[0]+"   \tTimes: "+str(failedTries[f])+"\tUser: "+f[3]+"\tTime: "+f[1]+" "+f[2]+"\n")


#Funcion para listar los archivos de un directorio
def listFiles(path):
    files = []
    for file in os.listdir(path):
        if "log" in file or file.endswith(".gz") or file.endswith("old") :
            files.append(os.path.join(path, file))
    return files

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding("utf8")
    parser = addOptions()
    opts, args = parser.parse_args()
    checkOptions(opts)
    reportFile = opts.out
    blacklistFile = opts.blacklist
    configFile = opts.config
    try:
        loadConfig(configFile)
        with open(reportFile,'w') as r :
            r.write('Log Analyzer Report\n\n')
        if os.path.isdir(apache2_Path):
            print "\n\n--------------------------------------------------------"
            print "Analyzing apache2 logs"
            files = listFiles(apache2_Path)
            analyzeApacheLogs(files, filesApache,reportFile)
        if os.path.isdir(httpd_Path):
            print "\n\n--------------------------------------------------------"
            print "Analyzing httpd logs"
            files = listFiles(httpd_Path)
            analyzeApacheLogs(files, filesHttpd,reportFile)
        if os.path.isdir(nginx_Path):
            print "\n\n--------------------------------------------------------"
            print "Analyzing nginx logs"
            files = listFiles(nginx_Path)
            analyzeApacheLogs(files, filesApache,reportFile)
        if os.path.isdir(mysql_Path):
            print "\n\n--------------------------------------------------------"
            print "Analyzing mysql logs"
            files = listFiles(mysql_Path)
            analyzeMysqlLogs(files, filesMysql,reportFile)
        if os.path.isdir(postgresql_Path):
            print "\n\n--------------------------------------------------------"
            print "Analyzing postgresql logs"
            files = listFiles(postgresql_Path)
            analyzePostgresLogs(files, filesPostgres,reportFile)
        createBlackList(blacklist,blacklistFile)
        print reportFile + "has been created"
        print blacklistFile + "has been created"
    except Exception as e:
        print(e)
