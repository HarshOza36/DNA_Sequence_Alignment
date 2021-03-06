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


# def getMemTimeInfo(basic = True, dnc = False):
#   call = basic_alignment if(basic) else dnc_alignment
#   mem_time_info = {}
#   x_axis = []
#   path = 'datapoints'
#   for i,filename in tqdm(enumerate(os.listdir(path))):
#     mem_time_info[i] = {}
#     dnaStrX, dnaStrY = obj.parseInput(f"{path}\\{filename}")
#     # start_time = time.time()
#     time_taken, memory_consumed, _ = call(dnaStrX, dnaStrY, obj.alpha_values, obj.delta_e)
#     # end_time = time.time()

#     mem_time_info[i]['mem'] = memory_consumed
#     # mem_time_info[i]['cpu'] = (end_time - start_time)*1000
#     mem_time_info[i]['cpu'] = time_taken
#     x_axis.append(len(dnaStrX))
#   return x_axis, mem_time_info

# x_axis, basic_ps = getMemTimeInfo(True, False)
# print(x_axis)
# _, dnc_ps = getMemTimeInfo(False, True)
# print(basic_ps)
# print(dnc_ps)

len_input = len(os.listdir('datapoints'))
basic_out_path = "datapoints_output\\Basic"
dnc_out_path = "datapoints_output\\DNC"


basic_ps = {}
dnc_ps = {}

for i in range(len(os.listdir(basic_out_path))):
  basic_ps[i] = {}
  with open(f"{basic_out_path}\\out_{i+1}.txt",'r') as f:
    l = f.readlines()
    basic_ps[i]['cpu'] = float(l[3].rstrip()[:-3])
    basic_ps[i]['mem'] = float(l[4][:-3])
  
  dnc_ps[i] = {}
  with open(f"{dnc_out_path}\\out_dnc_{i+1}.txt",'r') as f:
    l = f.readlines()
    dnc_ps[i]['cpu'] = float(l[3].rstrip()[:-3])
    dnc_ps[i]['mem'] = float(l[4][:-3])
  
print(basic_ps, dnc_ps)

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
# Problem Size (m+n) vs CPU
plt.xlabel("Problem Size (m+n)")
plt.ylabel("CPU Time (in ms)")
plt.title("CPU Time Comparison of Sequence Alignment")
plt.plot(x_axis, y_axis_cpu_basic, label="Basic")
plt.plot(x_axis, y_axis_cpu_dnc, label="Divide_N_Conquer")
plt.legend()
plt.savefig('CPU_Time_Graph_Final.jpg', format='jpg')
plt.clf()

# Problem Size (m+n) vs Memory
plt.xlabel("Problem Size (m+n)")
plt.ylabel("Memory Utilization (in KB)")
plt.title("Memory Utilization Comparison of Sequence Alignment")
plt.plot(x_axis, y_axis_mem_basic, label="Basic")
plt.plot(x_axis, y_axis_mem_dnc, label="Divide_N_Conquer")
plt.legend()
plt.savefig('Memory_Util_Graph_Final.jpg', format='jpg')