import os.path
import psutil as p
import cProfile


def system_info():
	# CPU Section.

	'''
	Returns the number of logical CPUs in the system or none if undetermined.
	logical cores means the number of physical cores multiplied by the number of threads that can run on each core
	(this is known as Hyper Threading).  If logical is False return the number of physical cores only
	(Hyper Thread CPUs are excluded) or none if undetermined.
	'''
	cpuTrue = p.cpu_count(logical=True)
	cpuFalse = p.cpu_count(logical=False)

	# Return a float representing the current system-wide CPU utilization as a percentage.
	cpuPercent = p.cpu_percent(interval=.1, percpu=True)

	'''
	Return system CPU times as a named tuple. 
	Every attribute represents the seconds the CPU has spent in the given mode. 
	The attributes availability varies depending on the platform:
	'''
	cpuTimes = p.cpu_times()

	# Memory section

	'''
	Return statistics about system memory usage as a named tuple including the following fields, expressed in bytes. Main metrics:

	*   total: total physical memory (exclusive swap).
	*   available: the memory that can be given instantly to processes without the system going into swap. 
		This is calculated by summing different memory values depending on the platform 
		and it is supposed to be used to monitor actual memory usage in a cross platform fashion.
	'''
	totalMemory = p.virtual_memory()

	# Disk section
	'''
	Return all mounted disk partitions as a list of named tuples including device, mount point and filesystem type, similarly 
	to “df” command on UNIX. If all parameter is False it tries to distinguish and return physical devices only 
	(e.g. hard disks, cd-rom drives, USB keys) 
	and ignore all others (e.g. pseudo, memory, duplicate, inaccessible filesystems).
	'''
	diskPart = p.disk_partitions()

	# this will show the disk usage
	diskUse = p.disk_usage('/')

	# the id to the process
	pid = os.getpid()

	# this will get the process id to the program
	process = p.Process(pid)

	# The memory process info
	memoryUse = process.memory_full_info()

	# array of the sytem info
	arr = [cpuTrue, cpuFalse, cpuPercent, cpuTimes.user, cpuTimes.system, cpuTimes.idle, totalMemory.total,
	       totalMemory.available, totalMemory.used, totalMemory.free, diskPart, diskUse.percent, diskUse.free,
	       pid, memoryUse.rss, memoryUse.vms, memoryUse.pfaults]
	for i in range(len(arr)):
		if arr[i] == arr[0]:
			print("The number of logical cores are " + arr[0].__str__())
		elif arr[i] == arr[1]:
			print("The number of physical cores are " + arr[1].__str__())
		elif arr[i] == arr[2]:
			k: int
			for k in range(arr[0]):
				print("CPU " + (k + 1).__str__() + " in use " + arr[2][k].__str__() + "%")
		elif arr[i] == arr[3]:
			print("Time on user mode " + arr[3].__str__())
		elif arr[i] == arr[4]:
			print("Time on system (kernel) mode " + arr[4].__str__())
		elif arr[i] == arr[5]:
			print("Time on idle " + arr[5].__str__())
		elif arr[i] == arr[6]:
			print("Total memory is " + round(arr[6] / 1024 ** 3, 2).__str__() + " GB")
		elif arr[i] == arr[7]:
			print("Total memory available is " + round(arr[7] / 1024 ** 3, 2).__str__() + " GB")
		elif arr[i] == arr[8]:
			print("Total memory used is " + round(arr[8] / 1024 ** 3, 2).__str__() + " GB")
		elif arr[i] == arr[9]:
			print("Total memory free is " + round(arr[9] / 1024 ** 3, 2).__str__() + " GB")
		elif arr[i] == arr[10]:
			print("all disk mounted are " + arr[10].__str__())
		elif arr[i] == arr[11]:
			print("Disk use " + arr[11].__str__() + "%")
		elif arr[i] == arr[12]:
			print("Disk free " + round(arr[12] / 1024 ** 3, 2).__str__() + " GB")
		elif arr[i] == arr[13]:
			print("PID is " + arr[13].__str__())
		elif arr[i] == arr[14]:
			print("The Resident set size is " + round(arr[14] / 1024 ** 3, 2).__str__() + " GB")
		elif arr[i] == arr[15]:
			print("The VMS is " + round(arr[15] / 1024 ** 3, 2).__str__() + " GB")
		elif arr[i] == arr[16]:
			print("The page fault size is " + arr[16].__str__())


''' The queue algorithm '''


class Queue:
	# makes a queue constructor
	def __init__(self):
		self.list = []

	# check if the queue is empty
	def isEmpty(self):
		return self.list == []

	# will insert in the queue
	def enqueue(self, list):
		self.list.append(list)

	# will remove from the queue
	def dequeue(self):
		return self.list.pop()

	# checks the size of the queue
	def size(self):
		return len(self.list)


# this will make the list for the queue
e = Queue()


# This will test the insert function in the queue
def insertElement():
	i: int
	for i in range(1000000):
		e.enqueue(i)


# this will test the remove function in the queue
def removeElement():
	i: int
	for i in range(1000000):
		e.dequeue()


# This will test the size of the queue
def checkSize():
	i: int
	for i in range(1000000):
		e.size()


'''
ncalls
for the number of calls.

tottime
for the total time spent in the given function (and excluding time made in calls to sub-functions)

percall
is the quotient of tottime divided by ncalls

cumtime
is the cumulative time spent in this and all subfunctions (from invocation till exit). This figure is accurate even for recursive functions.

percall
is the quotient of cumtime divided by primitive calls

filename:lineno(function)
provides the respective data of each function
'''
print("System info before Queue\n\n")
system_info()
print("\nProfiling when queue called\n\n")
profiling = cProfile.Profile()
profiling.enable()
insertElement()
removeElement()
e.isEmpty()
checkSize()
profiling.disable()
profiling.print_stats()
print("System info after Queue\n\n")
system_info()
