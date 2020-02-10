#################################################################################
#  Print Hardware and System Information in Python                              #
#                                                                               #
#  https://www.thepythoncode.com/article/get-hardware-system-information-python #
#                                                                               #
#  Kevin Scott (C) 2020                                                         #
#                                                                               #
#  NB : Needs psutil & pyinputplus, not in the Python Standard Library          #
#                                                                               #
#################################################################################
#                                                                               #
#    This program is free software: you can redistribute it and/or modify it    #
#    under the terms of the GNU General Public License as published by the Free #
#    Software Foundation, either version 3 of the License, or (at your option)  #
#    any later version.                                                         #
#                                                                               #
#    This program is distributed in the hope that it will be useful, but        #
#    WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY #
#    or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License   #
#    for more details.                                                          #
#                                                                               #
#    You should have received a copy of the GNU General Public License along    #
#    with this program. If not, see <http://www.gnu.org/licenses/>.             #
#                                                                               #
#################################################################################

import re
import sys
import uuid
import psutil
import platform
import textwrap
import argparse
import socket
import pyinputplus as pyip
from datetime import datetime
from _version import __version__


def getSize(bytes, suffix="B"):
    """  Returns a human readable version of a size given in bytes.

        1253656 => "1.20MB"
        1253656678 => "1.17GB"
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def printPlatfrom():
    """   Print Platform specific information.
    """

    uname = platform.uname()
    print(f"System      : {uname.system}")
    print(f"Hostname    : {uname.node}")
    print(f"Release     : {uname.release}")
    print(f"Version     : {uname.version}")
    print(f"Machine     : {uname.machine}")
    print(f"Processor   : {uname.processor}")
    print(f"Architecture: {platform.architecture()[0]}")
    print(f"IP Address  : {socket.gethostbyname(socket.gethostname())}")
    print(f"MAC address : {':'.join(re.findall('..', '%012x' % uuid.getnode()))}")


def printBootTime():
    """  Print Boot Time of the PC.
    """

    bootTime = psutil.boot_time()
    bt       = datetime.fromtimestamp(bootTime)
    print(f"Boot Time: {bt.day:02}/{bt.month:02}/{bt.year:02} {bt.hour:02}:{bt.minute:02}:{bt.second:02}")


def printCPUInfo():
    """  Print CPU specific information.
    """

    # number of cores
    print(f"Physical cores   : {psutil.cpu_count(logical=False)}")
    print(f"Total cores      : {psutil.cpu_count(logical=True)}")

    #  CPU frequencies
    cpuFreq = psutil.cpu_freq()
    print(f"Max Frequency    : {cpuFreq.max:.2f}Mhz")
    print(f"Min Frequency    : {cpuFreq.min:.2f}Mhz")
    print(f"Current Frequency: {cpuFreq.current:.2f}Mhz")

    #  CPU usage
    print("CPU Usage Per Core")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        print(f"  Core {i}     : {percentage}%")
    print(f"Total CPU Usage  : {psutil.cpu_percent()}%")


def printMemoryInfo():
    """  Print Memory specific information.
    """

    #  get the memory details
    svmem = psutil.virtual_memory()
    print(f"Total Memory     : {getSize(svmem.total)}")
    print(f"Available Memory : {getSize(svmem.available)}")
    print(f"Used Memory      : {getSize(svmem.used)}")
    print(f"Percentage Memory: {svmem.percent}%")

    #  get the swap memory details (if exists)
    swap = psutil.swap_memory()
    print(f"Total Swap       : {getSize(swap.total)}")
    print(f"Free Swap        : {getSize(swap.free)}")
    print(f"Used Swap        : {getSize(swap.used)}")
    print(f"Percentage Swap  : {swap.percent}%")


def printDiskInfo():
    """  Print Disk specific information.
    """

    #  get all disk partitions
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print(f"=========== Device: {partition.device} =========")
        print(f"      Mountpoint  : {partition.mountpoint}")
        print(f"  File System Type: {partition.fstype}")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            #  This can be caught due to disk that isn't ready
            continue
        print(f"  Total Size      : {getSize(partition_usage.total)}")
        print(f"  Used            : {getSize(partition_usage.used)}")
        print(f"  Free            : {getSize(partition_usage.free)}")
        print(f"  Percentage      : {getSize(partition_usage.percent)}%")

        #  getIO statistics since bootTime
        diskIO = psutil.disk_io_counters()
    print()
    print(f"Total Read : {getSize(diskIO.read_bytes)}")
    print(f"Total Write: {getSize(diskIO.write_bytes)}")


def printNetworkInfo():
    """  Print Network specific information.
    """

    #  get all network interfaces (virtual and physical)
    ifAddrs = psutil.net_if_addrs()
    for interfaceName, interfaceAddresses in ifAddrs.items():
        for address in interfaceAddresses:
            print(f"=== Interface: {interfaceName} ===")
            if str(address.family) == 'AddressFamily.AF_INET':
                print(f"  IP Address   : {address.address}")
                print(f"  Netmask      : {address.netmask}")
                print(f"  Broadcast IP : {address.broadcast}")
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                print(f"  MAC Address  : {address.address}")
                print(f"  Netmask      : {address.netmask}")
                print(f"  Broadcast MAC: {address.broadcast}")

    # get IO statistics since boot
    netIO = psutil.net_io_counters()
    print()
    print(f"Total Bytes Sent    : {getSize(netIO.bytes_sent)}")
    print(f"Total Bytes Received: {getSize(netIO.bytes_recv)}")


def printShortLicense():
    print(f"""
PySystemInfo {__version__}   Copyright (C) 2020  Kevin Scott
This program comes with ABSOLUTELY NO WARRANTY; for details type `PySystemInfo -l''.
This is free software, and you are welcome to redistribute it under certain conditions.
    """, flush=True)


def printLongLicense():
    print("""
    Copyright (C) 2020  Kevin Scott

    This program is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    """, end="")


def printSeperator(title):
    print("="*30, title, "="*30)


def printFromArgs(args):
    """  Print the specified information from the command line arguments.
    """
    print("args")
    if args.platform or args.all:
        printSeperator("Platform Information")
        printPlatfrom()

    if args.bootTime or args.all:
        printSeperator("Boot Time")
        printBootTime()

    if args.cpu or args.all:
        printSeperator("CPU Information")
        printCPUInfo()

    if args.memory or args.all:
        printSeperator("Memory Information")
        printMemoryInfo()

    if args.disk or args.all:
        printSeperator("Disk Information")
        printDiskInfo()

    if args.network or args.all:
        printSeperator("Network Information")
        printNetworkInfo()


def printFromMenu():
    """  Print the specified information from the menu option chosen.
    """

    while True:
        print()
        responce = pyip.inputMenu(["Platform", "Boot Time",
                                   "CPU", "Memory", "Disk", "Network",
                                   "All", "Quit"], numbered=True)

        if responce == "Platform" or responce == "All":
            printSeperator("Platform Information")
            printPlatfrom()

        if responce == "Boot Time" or responce == "All":
            printSeperator("Boot Time")
            printBootTime()

        if responce == "CPU" or responce == "All":
            printSeperator("CPU Information")
            printCPUInfo()

        if responce == "Memory" or responce == "All":
            printSeperator("Memory Information")
            printMemoryInfo()

        if responce == "Disk" or responce == "All":
            printSeperator("Disk Information")
            printDiskInfo()

        if responce == "Network" or responce == "All":
            printSeperator("Network Information")
            printNetworkInfo()

        if responce == "Quit":
            break

if __name__ == "__main__":
    """  Main program bit.
         Either process the command line arguments or the menu options.
    """

    parser = argparse.ArgumentParser(
        formatter_class = argparse.RawTextHelpFormatter,
        description=textwrap.dedent("""\
        System and hardware Information from Python.
        -----------------------
        Prints a lot of stuff about the Platform, CPU and Network."""),
        epilog = """ If no arguments are given, a Menu will be displayed.

        Kevin Scott (C) 2020""")

    parser.add_argument("-a", "--all",      action="store_true", help="Print All the Info.")
    parser.add_argument("-p", "--platform", action="store_true", help="Print the Platform Info.")
    parser.add_argument("-b", "--bootTime", action="store_true", help="Print the Boot Time.")
    parser.add_argument("-c", "--cpu",      action="store_true", help="Print the CPU Info.")
    parser.add_argument("-m", "--memory",   action="store_true", help="Print the Memory Info.")
    parser.add_argument("-d", "--disk",     action="store_true", help="Print the Disk Info.")
    parser.add_argument("-n", "--network",  action="store_true", help="Print the NetWork Info.")
    parser.add_argument("-v", "--version",  action="version",    version=f"%(prog)s {__version__}")
    parser.add_argument("-l", "--license",  action="store_true", help="Print the Software License.")
    args = parser.parse_args()

    if not any(vars(args).values()):  #  No command arguments given, run the menu.
        printShortLicense()
        printFromMenu()
        sys.exit(0)

    if args.license:
        printLongLicense()
        sys.exit(0)

    printFromArgs(args)               #  Must be command line arguments, so process.


