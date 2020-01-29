#################################################################################
#  Print Hardware and System Information in Python                              #
#                                                                               #
#  https://www.thepythoncode.com/article/get-hardware-system-information-python #
#                                                                               #
#  Kevin Scott (C) 2020                                                        #
#                                                                               #
#################################################################################
#    Copyright (C) <2020>  <Kevin Scott>                                        #
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
#    with this program. If not, see <http://www.gnu.org/licenses/>.             #                                              #
#                                                                               #
#################################################################################



import psutil
import platform
from datetime import datetime
from _version import __version__


def getSize(bytes, suffix="B"):
    """
        1253656 => "1.20MB"
        1253656678 => "1.17GB"
    """

    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def printPlatfrom():
    print("="*30, "System Information", "="*30)
    uname = platform.uname()
    print(f"System   : {uname.system}")
    print(f"Node Name: {uname.node}")
    print(f"Release  : {uname.release}")
    print(f"Version  : {uname.version}")
    print(f"Machine  : {uname.machine}")
    print(f"Processor: {uname.processor}")

def printBootTime():
    print("="*30, "Boot Time", "="*30)
    bootTime = psutil.boot_time()
    bt       = datetime.fromtimestamp(bootTime)
    print(f"Boot Time: {bt.day}/{bt.month}/{bt.month} {bt.hour}:{bt.minute}:{bt.second}")

def printCPUInfo():
    print("="*30, "CPU Information", "="*30)

    # number of cores
    print(f"Pysical cores : {psutil.cpu_count(logical=False)}")
    print(f"Toal cores    : {psutil.cpu_count(logical=True)}")

    #  CPU frequencies
    cpuFreq = psutil.cpu_freq()
    print(f"Max Frequencey    : {cpuFreq.max:.2f}Mhz")
    print(f"Min Frequencey    : {cpuFreq.min:.2f}Mhz")
    print(f"Current Frequencey: {cpuFreq.current:.2f}Mhz")

    #  CPU usage
    print("CPU Usage Per Core")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        print(f"Core {i}: {percentage}%")
    print(f"Total CPU Usage: {psutil.cpu_percent()}%")

def printMemoryInfo():
    print("="*30, "Memory Information", "="*30)

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
    print("="*30, "Disk Information", "="*30)

    #  get all disk partitions
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print(f"========= Device: {partition.device} =========")
        print(f"      Mountpoint: {partition.mountpoint}")
        print(f"File System Type: {partition.fstype}")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            #  This can be catched due to disk that isn't ready
            continue
        print(f"Total Size      : {getSize(partition_usage.total)}")
        print(f"Used            : {getSize(partition_usage.used)}")
        print(f"Free            : {getSize(partition_usage.free)}")
        print(f"Percentage      : {getSize(partition_usage.percent)}%")

        #  getIO statistice since bootTime
        diskIO = psutil.disk_io_counters()
        print()
        print(f"Total Read : {getSize(diskIO.read_bytes)}")
        print(f"Total Write: {getSize(diskIO.write_bytes)}")

def printNetworkInfo():
    print("="*30, "Network Information", "="*30)

    #  get all network interfaces (virtual and physical)
    ifAddrs = psutil.net_if_addrs()
    for interfaceName, interfaceAddresses in ifAddrs.items():
        for address in interfaceAddresses:
            print(f"=== Interface: {interfaceName} ===")
            if str(address.family) == 'AddressFamily.AF_INET':
                print(f"  IP Address: {address.address}")
                print(f"  Netmask: {address.netmask}")
                print(f"  Broadcast IP: {address.broadcast}")
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                print(f"  MAC Address: {address.address}")
                print(f"  Netmask: {address.netmask}")
                print(f"  Broadcast MAC: {address.broadcast}")

    # get IO statistics since boot
    netIO = psutil.net_io_counters()
    print()
    print(f"Total Bytes Sent: {getSize(netIO.bytes_sent)}")
    print(f"Total Bytes Received: {getSize(netIO.bytes_recv)}")


if __name__ == "__main__":
    printPlatfrom()
    printBootTime()
    printCPUInfo()
    printMemoryInfo()
    printDiskInfo()
    printNetworkInfo()