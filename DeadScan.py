#!/usr/bin/python3
import socket
import argparse
import sys
from threading import Thread
import time
from rich.console import Console
import random 

class Decoration:
    console = Console()
    def __init__(self):
        """
            Constructor Function to Initialize attributes and Constants.
        """
        self.is_decoration = True 
        self.console = Console()
        self.color = ["#FF0000","#FF7F00","#FFFF00","#00FF00","#00FFFF","#0000FF","#8B00FF","#FF1493","#FFD700","#00FF7F","#1E90FF","#FF4500"]

    def runRocket(self):
        """
            Decoration Function to Run a Rocket animation
        """
        rocket_length = 66
        color = str(random.choice(self.color))
        for i in range(rocket_length):
            if i%3==0:
                color = str(random.choice(self.color))
            rocket_design = f'[bold {color}]~~==>[/bold {color}]'
            time.sleep(0.020)
            if i != (rocket_length-1):
                self.console.print(" "*i + rocket_design, end='\r')
            else:   
                self.console.print(" "*i + rocket_design)

    def runLine2(self):
        """
            Decoration Function to print a multi color line
        """
        line_length = 70
        color = str(random.choice(self.color))
        for i in range(line_length):
            color = str(random.choice(self.color))
            line_char = f'[bold {color}]^[/bold {color}]'
            if i != (line_length-1):
                self.console.print(line_char , end='')
            else:   
                self.console.print(line_char )

    def runLine(self):
        """
            Decoration Function to print a single color line
        """
        line_length = 70
        color = "#FF4500"
        self.console.print(f'[bold {color}]{"-"*line_length}[/bold {color}]')


    def logo(self):
        """
            this function is used to print the Logo.
        """
        print("""
██████╗ ███████╗ █████╗ ██████╗     ███████╗ ██████╗ █████╗ ███╗   ██╗
██╔══██╗██╔════╝██╔══██╗██╔══██╗    ██╔════╝██╔════╝██╔══██╗████╗  ██║
██║  ██║█████╗  ███████║██║  ██║    ███████╗██║     ███████║██╔██╗ ██║
██║  ██║██╔══╝  ██╔══██║██║  ██║    ╚════██║██║     ██╔══██║██║╚██╗██║
██████╔╝███████╗██║  ██║██████╔╝    ███████║╚██████╗██║  ██║██║ ╚████║
╚═════╝ ╚══════╝╚═╝  ╚═╝╚═════╝     ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
    
Author:     DeadDroid
Version:    1.3                                                                   
            """)


class DeadScan(Decoration):
    def __init__(self):
        """
            Constructor Function to Initialize variables.
        """
        super().__init__()
        self.openports = []
        self.open_udp_port_filtered = []
        self.allow_print = 1
        self.thrds = []
        self.logo()

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
                if self.allow_print:
                    self.console.print(f"[bold #00FF7F][+] Port {port} is OPEN (got response)[/bold #00FF7F]")
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
            if self.allow_print:
                self.console.print(f"[bold #00FF7F][+] Port {port} is OPEN (got response)[/bold #00FF7F]")
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
        else:
            scanning_port = self.scanoneudp
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
        self.parser.add_argument("-r","--reliability",
                                 help="After the initial scan, initiate the riliability scans in bg [def = 0]",
                                 dest="riliability",
                                 metavar='',
                                 type=int,
                                 default=0)
        self.parser.add_argument("-rt",
                                 help="Number of Threads used in riliability scans [def = 100]",
                                 dest="riliability_threads",
                                 metavar='',
                                 type=int,
                                 default=100)
        self.args = self.parser.parse_args() # Parsing All Args.

    def argscheck(self):
        """
            Checking Arguments Provided By User And Raising Error if IP Not
        """
        if len(sys.argv) == 1:
            self.console.print('[bold #FF0000 ]Error: Target not specified. Please provide an IP address or domain. Use -h for usage details.[/bold #FF0000 ]')
            sys.exit(1)
        else:
            if self.args.ip:
                self.ip = self.args.ip
                self.start = self.args.sp
                self.end = self.args.ep
                self.threads = self.args.threads
                self.Time = self.args.Time
                self.port_type = self.args.port_type
                self.riliability = self.args.riliability
                self.riliability_threads = self.args.riliability_threads
            else:
                self.console.print('[bold #FF0000 ]Error: Target not specified. Please provide an IP address or domain. Use -h for usage details.[/bold #FF0000 ]')
                sys.exit(1)
            if self.port_type =='U':
                self.scan_type = 'UDP Scan'
            elif self.port_type == 'T':
                self.scan_type = "TCP Scan"
            else:
                self.console.print(f"[bold #FF0000 ]Error: Invalid protocol. The -p flag supports only 'T' (TCP) or 'U' (UDP).[/bold #FF0000 ]")
                sys.exit(1)

    def workOnArgs(self):
        """
            Process and handle the arguments provided by the user.
        """
        self.runRocket()  # Runs the Rocket 
        # checking if user asked to display time taken in the initial scan.
        if self.Time:
            stime = time.time() # setting the time start point
            self.console.print(f"""
[bold #00FF00]------------------------------------------------------------[/bold #00FF00]
[bold #00FF00][ [/bold #00FF00][bold #FFFF00]Starting Master Scan on Host {self.ip}...[bold #00FF00] ][/bold #00FF00]     
[bold #00FF00][ [/bold #00FF00]Ports Range: {self.start} - {self.end}[bold #00FF00] ][/bold #00FF00]
[bold #00FF00][ [/bold #00FF00]Scan Type: {self.scan_type}[bold #00FF00] ][/bold #00FF00]
[bold #00FF00][ [/bold #00FF00]Threads: {self.threads}[bold #00FF00] ][/bold #00FF00][/bold #FFFF00]
[bold #00FF00]------------------------------------------------------------[/bold #00FF00]\n""")
            self.scanloop()
            # checking if udp filtered ports are opens and printing list of open ports
            if self.open_udp_port_filtered:
                if len(self.open_udp_port_filtered) > 50:
                    self.console.print(f"\n[bold #FF7F00]Filtered UDP ports: {len(self.open_udp_port_filtered)} Entries ! Too big To Display...[/bold #FF7F00]")
                else:
                    self.console.print(f"\n[bold #00FF00]Filtered UDP ports {len(self.open_udp_port_filtered)}: {sorted(self.open_udp_port_filtered)}[/bold #00FF00]")
            # checking if tcp ports are opens and printing list of open ports
            if self.openports:
                self.console.print(f"\n[bold #00FF00]Open Ports {len(self.openports)}: {sorted(self.openports)}[/bold #00FF00]")
            etime = time.time() # setting the time end point
            # printing ( no ports open ) if both lists are empty
            if not self.open_udp_port_filtered and not self.openports:
                self.console.print(f"[bold #FF7F00]Scan result: no open ports detected[/bold #FF7F00]")
            # printing the time taken in the scan
            self.console.print(f"\n[bold #00FFFF]Time Taken in This Scan is {etime - stime} Seconds[/bold #00FFFF]")
            self.runLine() # prints a simple line
        else:
            # same functionality as above, just removing the time checking statements
            self.console.print(f"""
[bold #00FF00]------------------------------------------------------------[/bold #00FF00]
[bold #00FF00][ [/bold #00FF00][bold #FFFF00]Starting Master Scan on Host {self.ip}...[bold #00FF00] ][/bold #00FF00]     
[bold #00FF00][ [/bold #00FF00]Ports Range: {self.start} - {self.end}[bold #00FF00] ][/bold #00FF00]
[bold #00FF00][ [/bold #00FF00]Scan Type: {self.scan_type}[bold #00FF00] ][/bold #00FF00]
[bold #00FF00][ [/bold #00FF00]Threads: {self.threads}[bold #00FF00] ][/bold #00FF00][/bold #FFFF00]
[bold #00FF00]------------------------------------------------------------[/bold #00FF00]\n""")
            self.scanloop()
            if self.open_udp_port_filtered:
                if len(self.open_udp_port_filtered) > 50:
                    self.console.print(f"\n[bold #FF7F00]Filtered UDP ports: {len(self.open_udp_port_filtered)} Entries ! Too big To Display...[/bold #FF7F00]")
                else:
                    self.console.print(f"\n[bold #00FF00]Filtered UDP ports {len(self.open_udp_port_filtered)}: {sorted(self.open_udp_port_filtered)}[/bold #00FF00]")
            if self.openports:
                self.console.print(f"\n[bold #00FF00]Open Ports {len(self.openports)}: {sorted(self.openports)}[/bold #00FF00]")
            if not self.open_udp_port_filtered and not self.openports:
                self.console.print(f"[bold #FF7F00]Scan result: no open ports detected[/bold #FF7F00]")
            self.runLine()

        # Processing riliablity scans now
        if self.riliability:
            # checking number of riliability scans provided by the user.
            if self.riliability > 0 and isinstance(self.riliability, int) and self.riliability < 11:
                self.allow_print = 0  # stops printing open ports while running riliability scans
                self.threads = self.riliability_threads
                for i in range(1,(self.riliability+1)):
                    self.openports = []
                    self.open_udp_port_filtered = []
                    self.console.print(f'[bold #FFFF00]Starting riliability scan {i}/{self.riliability} with {self.threads} Threads...[/bold #FFFF00]')
                    self.scanloop()
                    if self.open_udp_port_filtered:
                        if len(self.open_udp_port_filtered) > 50:
                            self.console.print(f"\n[bold #FF7F00]Filtered UDP ports: {len(self.open_udp_port_filtered)} Entries ! Too big To Display...[/bold #FF7F00]")
                        else:
                            self.console.print(f"\n[bold #00FF00]Filtered UDP ports {len(self.open_udp_port_filtered)}: {sorted(self.open_udp_port_filtered)}[/bold #00FF00]")
                    if self.openports:
                        self.console.print(f"\n[bold #00FF00]Open Ports {len(self.openports)}: {sorted(self.openports)}[/bold #00FF00]")
                    if not self.open_udp_port_filtered and not self.openports:
                        self.console.print(f"[bold #FF7F00]Scan result: no open ports detected[/bold #FF7F00]")
                    self.runLine()


if __name__=="__main__":
    obj = DeadScan()
    obj.arguments()
    obj.argscheck()
    obj.workOnArgs()
