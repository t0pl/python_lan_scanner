import argparse
import socket
import subprocess
import threading

import getmac

parser = argparse.ArgumentParser(description="Network scanner")
parser.add_argument("-a",'--all',help="Scan from 10.10.0.1 to 10.10.255.1",action="store_true")
parser.add_argument("-s",'--subnetwork',help="Specify a range or a number or even several numbers, eg: 1-25 or 1 or 1,50,24 -> scan 10.10.0.1 to 10.10.5.1")
parser.add_argument("-p","--prettyprint",help="Makes output prettier",action="store_true")
parser.add_argument("hostnumber",help="The range of ip that will be scanned (per subnetwork), for eg: 1-25 -> 10.10.1.1 to 10.10.1.25",type=str)
args = parser.parse_args()

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except:
        ip = False
    finally:
        s.close()
    return ip

def test_internet():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        test = s.connect(("google.com",80))
    except:
        test = False
    finally:
        return test
if test_internet() == False:
    print("** No internet")
def ping(ip:str):
    ping = subprocess.Popen(['ping','-n','1',ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
    if 'ttl' in str(ping) or 'TTL' in str(ping):
        ups.append(ip)

def nslookup(ip:str):
    dns_lookup = subprocess.Popen(['nslookup',ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
    """if b"*" not in dns_lookup:
        #print(dns_lookup)"""
    result[ip] = dns_lookup.split(b":")[-2].replace(b" ",b"").split(b"\r\n")[0]

vendors = {}
def retreive_vendors():
    try:
        a=open("mac_vendors_.txt",encoding="utf-8").read()
    except FileNotFoundError:
        return False
    for i in a.split("\n"):
        ii = i.split("\t\t")
        vendors[ii[0].strip()] = ii[1]
def get_mac_vendor(mac:str):
        if mac == None:
            return None
        try:
            id = [i.upper() for i in "".join(mac.split(":")[:3]).split()][0]
        except IndexError as e:
            return e
        for identifier in vendors.keys():
            if id == identifier:
                return vendors[identifier]
def int_list(liste:list):
    l=[]
    for i in liste:
        try:
            l.append(int(i))
        except ValueError:
            return False
    return l
        

retreive_vendors()
local_ip = get_local_ip()
third = ".".join(local_ip.split(".")[0:-1])+"."
first_and_second = ".".join(local_ip.split(".")[:2])+"."
result = {}
ups=[]
streds = []
result_lenght = int
scan_duration = float
if not "-" in args.hostnumber:
    exit("*Hostnumber must be as : 1-66 for eg")
hostnumber = int_list(args.hostnumber.split("-"))
all_network = args.all
subnetwork = args.subnetwork
pretty_print = args.prettyprint

if all_network and subnetwork:
    exit("Arguments all and subnetwork can't be used at the same time")
if not hostnumber:
    exit("*hostnumber requires integers")
if hostnumber[0] > hostnumber[1]:
    exit("*First part of '1-25' for hostnumber must be greater that the second one")
if hostnumber[0] < 0 or hostnumber[1] > 256:
    exit("*Hostnumber must be between 1 and 256")
if subnetwork != None:
    if "-" in subnetwork:
        subnetwork = int_list(subnetwork.split("-"))
        if not subnetwork:
            exit("*SUBNETWORK requires integers")
        if len(subnetwork) != 2:
            exit("*SUBNETWORK must be like : 1-25, not 1-25-25 for eg")
        if subnetwork[0] > subnetwork[1]:
            exit("*First part of '1-25' for subnetwork should be greater that the second one")
        if subnetwork[0] < 0 or subnetwork[1] > 256:
            exit("*Subnetwork must be between 1 and 256")
        #Scan:
        #10.10.x.1 to 10.10.x.1/25
        for subnet in range(subnetwork[0],subnetwork[1]):
            thr = first_and_second+str(subnet)+"."
            for i in range(hostnumber[0],hostnumber[1]):
                stred = threading.Thread(target=ping,args=[thr+str(i),])
                streds.append(stred)
                stred.start()
            for x in streds:
                stred.join()
            #Get hostname from ups with nslookup.exe
        for ipadr in ups:
            stred = threading.Thread(target=nslookup,args=[ipadr,])
            streds.append(stred)
            stred.start()
        for x in streds:
            stred.join()

    elif "," in subnetwork:
        subnetwork = int_list(subnetwork.split(","))
        if not subnetwork:
            exit("*SUBNETWORK requires integers")
        for subnet in subnetwork:
            if subnet < 1 or subnet > 256:
                exit("*Each digit in subnetwork argument must be between 1 and 256")
            #Scan:
            #10.10.x.1 to 10.10.x.1/25
            #1,25,50
            thr = first_and_second+str(subnet)+"."#10.10.x.
            for i in range(hostnumber[0],hostnumber[1]):
                stred = threading.Thread(target=ping,args=[thr+str(i),])
                streds.append(stred)
                stred.start()
            for x in streds:
                stred.join()
        for ipadr in ups:
            stred = threading.Thread(target=nslookup,args=[ipadr,])
            streds.append(stred)
            stred.start()
        for x in streds:
            stred.join()
            
    else:
        try:
            subnetwork=int(subnetwork)
        except ValueError:
            exit("*SUBNETWORK requires integers")
        if subnetwork < 1 or subnetwork > 256:
            exit("*The subnetwork argument must be between 1 and 256")
        thr = first_and_second+str(subnetwork)+"."
        for i in range(int(hostnumber[0]),int(hostnumber[1])):
            stred = threading.Thread(target=ping,args=[thr+str(i),])
            streds.append(stred)
            stred.start()
        for x in streds:
            stred.join()
        for ipadr in ups:
            stred = threading.Thread(target=nslookup,args=[ipadr,])
            streds.append(stred)
            stred.start()
        for x in streds:
            stred.join()

if all_network:
    #10.10.0.1 to 10.10.255.1
    #Ping from x to y
    for subnet in range(1,25):
        thr = first_and_second+str(subnet)+"."
        for i in range(int(hostnumber[0]),int(hostnumber[1])):
            #print(thr+str(i))
            stred = threading.Thread(target=ping,args=[thr+str(i),])
            streds.append(stred)
            stred.start()
        for x in streds:
            stred.join()
        #Get hostname from ups with nslookup.exe
    for ipadr in ups:
        stred = threading.Thread(target=nslookup,args=[ipadr,])
        streds.append(stred)
        stred.start()
    for x in streds:
        stred.join()

#print(result)
r={}
for ip in ups:
    r[ip] = {}
    mac = getmac.get_mac_address(ip=ip)
    hostname = result[ip]
    vendor = get_mac_vendor(mac)
    r[ip]["mac"] = mac
    r[ip]["hostname"] = hostname
    r[ip]["vendor"] = vendor
    """if pretty_print:
        
        if ip == ups[0]:
            print("+-----------------------------------------------------------------------------------------------------+")
        print("| ",ip)
        print(" "*len(ip),"     ",hostname)
        print(" "*(len(ip)+len(hostname)),"        ",mac)
        print(" "*(len(ip)+len(hostname)+17),"          ",vendor)
        if ip == ups[-1]:
            #print("+-----------------------------------------------------------------------------------------------------+")
    else:
        print(ip, hostname, mac,vendor)"""
import pprint
pprint.pprint(r)