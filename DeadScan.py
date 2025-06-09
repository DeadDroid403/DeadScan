#!/usr/bin/python3
import socket
import argparse
import sys
from threading import Thread
import time

class DeadScan:
    def __init__(self):
        """
            Constructor Function to Initialize variables.
        """
        self.openports = []
        self.open_udp_port_filtered = []
        self.thrds = []

    def scanone(self,port):
        """
            Function To Scan 1 TCP Port, We'll Call This Func To Scan Ports Concurrently.
        """
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # Creating a Socket 
            s.settimeout(0.5)
            # Trying To Connect To a Port and Saving Result.
            result = s.connect_ex((self.ip,port))
            # Checking if Port is open or close.
            if result == 0:
               print(f"[+] Port {port} is OPEN (got response) ")
               self.openports.append(port)
            s.close() # Closing the Socket.
        except Exception as e:
            pass # Simply Ignoring The Exceptions.
    
    def scanoneudp(self,port):
        """
            Function to Scan 1 UDP Port, We'll Call This Func to Scan UDP Ports Concurrently.
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Creating a Socket 
            s.settimeout(3)
            # Trying To Connect To a UDP Port and Wait for Response.
            s.connect((self.ip,port))
            s.send(b"") # Sending Empty Payload to UDP. 
            data = s.recv(1024)  # if we recieve data then the port is open. 
            print(f"[+] Port {port} is OPEN (got response)")
            self.openports.append(port)
        except socket.timeout: # if timeouts then port is probably open or filtered. 
            self.open_udp_port_filtered.append(port)
        except Exception as e: # For every other Exception, we are declaring port as closed. like ICMP error...
            pass
        finally:
            s.close() # Finally closing the connection.

    def scanloop(self):
        """
            Function To Create Multiple Threads and Call Scanone Func Concurrently.
        """
        # Loop To Scan All Ports Given By User.
        if self.port_type == "T":
            scanning_port = self.scanone
        elif self.port_type == "U":
            scanning_port = self.scanoneudp
        else:
            print(f"[-] The -p flag only supports T or U for TCP or UDP respectively")
            sys.exit(1)
        for port in range (self.start, (self.end + 1)):
            th = Thread(target=scanning_port, args=(port,)) # Creating Thread.
            self.thrds.append(th) # Appending Threads In a List.
            th.start() # Starting Thread.
            if len(self.thrds) >= self.threads: # Ensuring a Limit For Concurrent Threads.
                for th in self.thrds:
                    th.join()
                self.thrds = []
        # Finishing All Remaining Threads.
        for th in self.thrds:
            th.join()
    
    def arguments(self):
        """
            Function To Create Arguments and Switches For This Tool.
        """
        self.parser = argparse.ArgumentParser(description="Fastest Port Scanner By DeadDroid...",
                                         usage="%(prog)s -h < ip >",
                                         epilog="""
                                         Example:
                                                %(prog)s -h 192.168.1.100 -sp 20 -ep 8080 -t 500
                                         """,)
        self.parser.add_argument("-i","--ip",
                            metavar='',
                            dest="ip",
                            help="Input Target IP Address",
                            type=str)
        self.parser.add_argument("-sp","--start-port",
                            help="Starting Port Value [def = 1]",
                            dest="sp",
                            metavar='',
                            type=int,
                            default=1)
        self.parser.add_argument("-ep", "--end-port",
                                 help="Ending Port Value [def = 65535]",
                                 dest="ep",
                                 metavar='',
                                 type=int,
                                 default=65535)
        self.parser.add_argument("-t", "--threads",
                                 help="Number of threads to use [def = 500]",
                                 metavar='',
                                 dest="threads",
                                 type=int,
                                 default=500)
        self.parser.add_argument("-T", "--Time",
                                 help="Display Time Taken In The Scanning",
                                 dest="Time",
                                 action="store_true")
        self.parser.add_argument("-p","--port-type",
                                 help="Type of Port Scan T / U for TCP or UDP [def = T]",
                                 dest="port_type",
                                 metavar='',
                                 default="T")
        self.args = self.parser.parse_args() # Parsing All Args.

    def argscheck(self):
        """
            Checking Arguments Provided By User And Raising Error if IP Not
        """
        if len(sys.argv) == 1:
            self.parser.print_help()
            sys.exit(1)
        else:
            if self.args.ip:
                self.ip = self.args.ip
                self.start = self.args.sp
                self.end = self.args.ep
                self.threads = self.args.threads
                self.Time = self.args.Time
                self.port_type = self.args.port_type
            else:
                self.parser.print_help()
                sys.exit(1)
        

if __name__=="__main__":
    obj = DeadScan()
    obj.arguments()
    obj.argscheck()
    if obj.ip:
        if obj.Time:
            stime = time.time()
            print("*"*70)
            print(f"Started Scanning Port From {obj.start} - {obj.end} on IP {obj.ip}")
            obj.scanloop()
            if obj.open_udp_port_filtered:
                if len(obj.open_udp_port_filtered) > 50:
                    print(f"\nList of Filterded Ports is too big...")
                else:
                    print(f"\nList of Filterded Ports = {sorted(obj.open_udp_port_filtered)}")
            if obj.openports:
                print(f"\nList of Ports = {sorted(obj.openports)}")
            etime = time.time()
            print(f"\nTime Taken in This Scan is {etime - stime} Seconds")
            print("*"*70)
        else:
            print("*"*70)
            print(f"Started Scanning Port From {obj.start} - {obj.end} on IP {obj.ip}")
            obj.scanloop()
            if obj.open_udp_port_filtered:
                if len(obj.open_udp_port_filtered) > 50:
                    print(f"\nList of Filterded Ports is too big...")
                else:
                    print(f"\nList of Filterded Ports = {sorted(obj.open_udp_port_filtered)}")
            if obj.openports:
                print(f"\nList of Ports = {sorted(obj.openports)}")
            print("*"*70)
    else:
        obj.parser.print_help()
        sys.exit(1)
        
