import matplotlib.pyplot as plt
import os
import sys
import time
import psutil
import tracemalloc
from basic_3 import basic_alignment, Utils
from efficient_3 import dnc_alignment
from tqdm import tqdm
obj = Utils()

def process_memory():
  process = psutil.Process()
  memory_info = process.memory_info()
  memory_consumed = int(memory_info.rss/1024)
  return memory_consumed

def getMemTimeInfo(basic = True, dnc = False):
  call = basic_alignment if(basic) else dnc_alignment
  mem_time_info = {}
  path = 'datapoints'
  for i,filename in tqdm(enumerate(os.listdir(path))):
    mem_time_info[i] = {}
    dnaStrX, dnaStrY = obj.parseInput(f"{path}\\{filename}")
    start_time = time.time()
    memory_consumed, _ = call(dnaStrX, dnaStrY, obj.alpha_values, obj.delta_e)
    end_time = time.time()

    mem_time_info[i]['mem'] = memory_consumed
    mem_time_info[i]['cpu'] = (end_time - start_time)*1000
  return mem_time_info

basic_ps = getMemTimeInfo(True, False)
dnc_ps = getMemTimeInfo(False, True)
print(basic_ps)
print(dnc_ps)

len_input = len(os.listdir('datapoints'))
x_axis = [16,64,128,256,384,512,768,1024,1280,1536,2048,2560,3072,3584,3968]
y_axis_cpu_basic = []
y_axis_mem_basic = []
y_axis_cpu_dnc = []
y_axis_mem_dnc = []
for i in range(len_input):
  y_axis_mem_basic.append(basic_ps[i]['mem'])
  y_axis_cpu_basic.append(basic_ps[i]['cpu'])
  y_axis_cpu_dnc.append(dnc_ps[i]['cpu'])
  y_axis_mem_dnc.append(dnc_ps[i]['mem'])
# Problem Size vs CPU
plt.xlabel("Problem Size")
plt.ylabel("CPU Time (in s)")
plt.title("CPU Time Comparison of Sequence Alignment")
plt.plot(x_axis, y_axis_cpu_basic, label="Basic")
plt.plot(x_axis, y_axis_cpu_dnc, label="Divide_N_Conquer")
plt.legend()
plt.savefig('CPU_Time_Graph_Final.jpg', format='jpg')
plt.clf()

# Problem Size vs Memory
plt.xlabel("Problem Size")
plt.ylabel("Memory Utilization (in KB)")
plt.title("Memory Utilization Comparison of Sequence Alignment")
plt.plot(x_axis, y_axis_mem_basic, label="Basic")
plt.plot(x_axis, y_axis_mem_dnc, label="Divide_N_Conquer")
plt.legend()
plt.savefig('Memory_Util_Graph_Final.jpg', format='jpg')