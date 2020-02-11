#################################################################################
#  Print Hardware and System Information in Python                              #
#                                                                               #
#  The information is gathered in systemInfo.py and imported                    #
#                                                                               #
#                                                                               #
#  Kevin Scott (C) 2020                                                         #
#                                                                               #
#  NB : Needs psutil & pyinputplus, not in the Python Standard Library          #
#                                                                               #
#  See history.txt for version information.
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

import sys
import textwrap
import argparse
import systemInfo
import pyinputplus as pyip

from _version import __version__


SI = systemInfo.SysInfo()


def printPlatfrom():
    """   Print Platform specific information.
    """

    print(f"System      : {SI.System}")
    print(f"Hostname    : {SI.Hostname}")
    print(f"Release     : {SI.Release}")
    print(f"Version     : {SI.Version}")
    print(f"Machine     : {SI.Machine}")
    print(f"Processor   : {SI.Processor}")
    print(f"Architecture: {SI.Architecture}")
    print(f"IP Address  : {SI.IPaddress}")
    print(f"MAC address : {SI.MACaddress}")


def printBootTime():
    """  Print Boot Time of the PC.
    """

    print(f"Boot Time: {SI.BootTime}")


def printCPUInfo():
    """  Print CPU specific information.
    """

    # number of cores
    print(f"Physical cores   : {SI.PhysicalCores}")
    print(f"Total cores      : {SI.TotalCores}")

    #  CPU frequencies
    print(f"Max Frequency    : {SI.MaxFrequency}")
    print(f"Min Frequency    : {SI.MinFrequency}")
    print(f"Current Frequency: {SI.CurrentFrequency}")

    #  CPU usage
    print("CPU Usage Per Core")
    for i, percentage in enumerate(SI.CPUusage):
        print(f"  Core {i}     : {percentage}%")
    print(f"Total CPU Usage  : {SI.TotalCPUusage}")


def printMemoryInfo():
    """  Print Memory specific information.
    """

    #  get the memory details
    print(f"Total Memory     : {SI.TotalMemory}")
    print(f"Available Memory : {SI.AvailableMemory}")
    print(f"Used Memory      : {SI.UsedMemory}")
    print(f"Percentage Memory: {SI.PercentageMemory}")

    #  get the swap memory details (if exists)
    print(f"Total Swap       : {SI.TotalSwap}")
    print(f"Free Swap        : {SI.AvailableSwap}")
    print(f"Used Swap        : {SI.UsedSwap}")
    print(f"Percentage Swap  : {SI.PercentageSwap}")


def printDiskInfo():
    """  Print Disk specific information.
    """

    #  get all disk partitions
    disks = SI.DiskPartitions
    for partition in disks:
      print(f"=========== Device: {partition} =========")
      print(f"  Mountpoint      : {disks[partition][0]}")
      print(f"  File System Type: {disks[partition][1]}")
      print(f"  Total Size      : {disks[partition][2]}")
      print(f"  Used Space      : {disks[partition][3]}")
      print(f"  Free Space      : {disks[partition][4]}")
      print(f"  Percentage Used : {disks[partition][5]}")

    #  getIO statistics since bootTime
    print()
    print(f"Total Read : {SI.DiskTotalRead}")
    print(f"Total Write: {SI.DiskTotalWrite}")


def printNetworkInfo():
    """  Print Network specific information.
    """

    #  get all network interfaces (virtual and physical)
    nets = SI.Networks

    for net in nets:
      if nets[net][1] == 'AddressFamily.AF_INET':
        print(f"=== Interface: {nets[net][0]} ===")
        print(f"Address Family : {nets[net][1]}")
        print(f"  IP Address   : {nets[net][2]}")
        print(f"  Netmask      : {nets[net][3]}")
        print(f"  Broadcast IP : {nets[net][4]}")
      elif nets[net][1] == 'AddressFamily.AF_PACKET':
        print(f"=== Interface: {nets[net][0]} ===")
        print(f"Address Family : {nets[net][1]}")
        print(f"  MAC Address  : {nets[net][2]}")
        print(f"  Netmask      : {nets[net][3]}")
        print(f"  Broadcast MAC: {nets[net][4]}")

    print()
    print(f"Total Bytes Sent    : {SI.TotalBytesSent}")
    print(f"Total Bytes Received: {SI.TotalBytesReceived}")


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

    if not any(vars(args).values()):  # No command arguments given, run the menu.
        printShortLicense()
        printFromMenu()
        sys.exit(0)

    if args.license:
        printLongLicense()
        sys.exit(0)

    printFromArgs(args)               # Must be command line arguments, so process.

