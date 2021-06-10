#################################################################################
#  Collect the Hardware and System Information in Python                        #
#                                                                               #
#  https://www.thepythoncode.com/article/get-hardware-system-information-python #
#                                                                               #
#  Kevin Scott (C) 2020-2021                                                    #
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
import uuid
import psutil
import socket
import platform

from datetime import datetime

class SysInfo:
    """  A class that collects and returns information about the system.

    Returned information

    Platform [All returned as Strings]
        System           : Name of the OS i.e. Windows.
        HostName         : Name of the host PC.
        Release          : Release version of the OS [Major number].
        Version          : Version of the OS         [Full Version].
        Machine          : Major name of the CPU.
        Processor        : Full info of CPU.
        Architecture     : Machine architecture i.e. 32/64 bit.
        IPaddress        : IP Address of the host PC.
        MACaddress       : MAC address of the host PC.

        BootTime         : The time of the last time the PC was booted.

      CPU [All returned as Strings]
        PhysicalCores    : The number of physical cores of the CPU.
        TotalCores       : The number of Total cores of the CPU.
        MaxFrequency     : The maximum frequency of the CPU [in MHz].
        MinFrequency     : The minimum frequency of the CPU [in MHz].
        CurrentFrequency : The current frequency of the CPU [in MHz].
        CPUusage         : A *list* containing the usage for each individual core [in %].
        TotalCPUusage    : The current overall usage of the CPU [in %].

      Memory [All returned as Strings]
        TotalMemory      : Total Memory installed in the host PC [in suitable format].
        AvailableMemory  : Total available [un-used] memory in host PC [in suitable format].
        UsedMemory       : Total used memory in host PC [in suitable format].
        PercentageMemory : Percentage of used memory [in %].
      Swap [All returned as Strings]
        TotalSwap        : Total Swap Memory installed in the host PC [in suitable format].
        AvailableSwap    : Total available [un-used] Swap Memory in host PC [in suitable format].
        UsedSwap         : Total used Swap Memory in host PC [in suitable format].
        PercentageSwap   : Percentage of used Swap Memory [in %].

      Disk [Returned as a Dictionary]
        key  [string]          : Device name..
        data [list of strings] : Mountpoint
                               : File System Type
                               : Total Size
                               : Used Space
                               : Free Space
                               : Percentage used

        DiskTotalRead  [string]: Total read from all disks since boot time.
        DiskTotalWrite [string]: Total written to all disks since boot time.

      Networks [Returned as a Dictionary]
        key                    : unique integer ID
        data [list of strings] : Interface Name
                               : Family
                               : IP Address or MAC Address
                               : Netmask
                               : Broadcast IP

          TotalBytesReceived [string]: Total Bytes Received over network since boot time.
          TotalBytesSent [string]    : Total Bytes Sent over network since boot time.
          
      Python Compiler [A wrapper for the values returned by platform, the descriptions are copied from there]
          PythonBuild          : Returns a tuple (buildno, builddate) stating the Python build number and date as strings.
          PythonCompiler       : Returns a string identifying the compiler used for compiling Python.
          PythonBranch         : Returns a string identifying the Python implementation SCM branch.
          PythonImplementation : Returns a string identifying the Python implementation. Possible return values are: ‘CPython’, ‘IronPython’, ‘Jython’, ‘PyPy’.
          PythonRevision       : Returns a string identifying the Python implementation SCM revision.
          PythonVersion        : Returns the Python version as string 'major.minor.patchlevel'.
    """


    def getSize(self, bytes, suffix="B"):
        """  Returns a human readable format of a size given in bytes.

            1253656 => "1.20MB"
            1253656678 => "1.17GB"
        """
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor


    uname = platform.uname()

    @property
    def System(self):
        return self.uname.system

    @property
    def Hostname(self):
        return self.uname.node

    @property
    def Release(self):
        return self.uname.release

    @property
    def Version(self):
        return self.uname.version

    @property
    def Machine(self):
        return self.uname.machine

    @property
    def Processor(self):
        return self.uname.processor

    @property
    def Architecture(self):
        return platform.architecture()[0]

    @property
    def IPaddress(self):
        return socket.gethostbyname(socket.gethostname())

    @property
    def MACaddress(self):
        return ':'.join(re.findall('..', '%012x' % uuid.getnode()))

    @property
    def BootTime(self):
        bootTime = psutil.boot_time()
        bt       = datetime.fromtimestamp(bootTime)
        return f"Boot Time: {bt.day:02}/{bt.month:02}/{bt.year:02} {bt.hour:02}:{bt.minute:02}:{bt.second:02}"

    # number of cores
    @property
    def PhysicalCores(self):
        return psutil.cpu_count(logical=False)

    @property
    def TotalCores(self):
        return psutil.cpu_count(logical=True)

    #  CPU frequencies
    cpuFreq = psutil.cpu_freq()

    @property
    def MaxFrequency(self):
        return f"{self.cpuFreq.max:.2f}MHz"

    @property
    def MinFrequency(self):
        return f"{self.cpuFreq.min:.2f}MHz"

    @property
    def CurrentFrequency(self):
        return f"{self.cpuFreq.current:.2f}MHz"

    #  CPU usage
    @property
    def CPUusage(self):
        p = []           #  create empty list.

        for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
            p.append(percentage)
        return p

    @property
    def TotalCPUusage(self):
        return f"{psutil.cpu_percent()}%"

    #  get the memory details
    svmem = psutil.virtual_memory()

    @property
    def TotalMemory(self):
        return self.getSize(self.svmem.total)

    @property
    def AvailableMemory(self):
        return self.getSize(self.svmem.available)

    @property
    def UsedMemory(self):
        return self.getSize(self.svmem.used)

    @property
    def PercentageMemory(self):
        return f"{self.svmem.percent}%"

    #  get the swap memory details (if exists)
    swap = psutil.swap_memory()

    @property
    def TotalSwap(self):
        return self.getSize(self.swap.total)

    @property
    def AvailableSwap(self):
        return self.getSize(self.swap.free)

    @property
    def UsedSwap(self):
        return self.getSize(self.swap.used)

    @property
    def PercentageSwap(self):
        return f"{self.swap.percent}%"


    #  get all disk partitions
    partitions = psutil.disk_partitions()

    @property
    def DiskPartitions(self):
        p = {}           #  Create empty dictionary

        for partition in self.partitions:
            l = []           #  create empty list.
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                #  This can be caught due to disk that isn't ready
                continue
            l.append(partition.mountpoint)
            l.append(partition.fstype)
            l.append(self.getSize(partition_usage.total))
            l.append(self.getSize(partition_usage.used))
            l.append(self.getSize(partition_usage.free))
            l.append(f"{self.getSize(partition_usage.percent)}%")

            p[partition.device] = l
        return p

    #  getIO statistics since bootTime
    diskIO = psutil.disk_io_counters()

    @property
    def DiskTotalRead(self):
        return self.getSize(self.diskIO.read_bytes)

    @property
    def DiskTotalWrite(self):
        return self.getSize(self.diskIO.write_bytes)

    #  get all network interfaces (virtual and physical)
    ifAddrs = psutil.net_if_addrs()

    @property
    def Networks(self):
        p = {}           #  Create empty dictionary
        n = 0

        for interfaceName, interfaceAddresses in self.ifAddrs.items():
            for address in interfaceAddresses:
                l = []           #  create empty list.

                l.append(interfaceName)
                l.append(str(address.family))

                l.append(address.address)
                l.append(address.netmask)
                l.append(address.broadcast)

                p[n] = l
                n += 1

        return p

    # get IO statistics since boot
    netIO = psutil.net_io_counters()

    @property
    def TotalBytesSent(self):
        return self.getSize(self.netIO.bytes_sent)

    @property
    def TotalBytesReceived(self):
        return self.getSize(self.netIO.bytes_recv)
      
    # Python information
  
    @property
    def PythonBuild(self):
        return platform.python_build()
      
    @property
    def PythonCompiler(self):
        return platform.python_compiler()
      
    @property
    def PythonBranch(self):
        return platform.python_branch()
      
    @property
    def PythonImplementation(self):
        return platform.python_implementation()
      
    @property
    def PythonRevision(self):
        return platform.python_revision()
      
    @property
    def PythonVersion(self):
        return platform.python_version()
