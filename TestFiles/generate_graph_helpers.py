# It seems that when we run generate graphs together for both 
# DNC and basic, the memory increases when we run for dnc
# Hence we will run the Problem sets for basic and dnc one after one.
# First we will just run basic
# Then we will restart the program for DNC
# We will save the output in files and then call it in main generate graph file

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

def getMemTimeInfoBasic():
  call = basic_alignment 
  mem_time_info = {}
  path = 'datapoints'
  for i,filename in tqdm(enumerate(os.listdir(path))):
    mem_time_info[i] = {}
    dnaStrX, dnaStrY = obj.parseInput(f"{path}\\{filename}")
    # process = psutil.Process()
    # memory_info = process.memory_info()
    # tracemalloc.start()
    start_time = time.time()
    call(dnaStrX, dnaStrY, obj.alpha_values, obj.delta_e)
    end_time = time.time()
    # memory_consumed = int(memory_info.rss/1024)
    # memory_consumed = tracemalloc.get_traced_memory()[1]/1000
    # tracemalloc.stop()
    memory_consumed = process_memory()
    mem_time_info[i]['mem'] = memory_consumed
    mem_time_info[i]['cpu'] = (end_time - start_time)*1000
  return mem_time_info

def getMemTimeInfoDNC():
  call = dnc_alignment
  mem_time_info = {}
  path = 'datapoints'
  for i,filename in tqdm(enumerate(os.listdir(path))):
    mem_time_info[i] = {}
    dnaStrX, dnaStrY = obj.parseInput(f"{path}\\{filename}")
    # process = psutil.Process()
    # memory_info = process.memory_info()
    # tracemalloc.start()
    start_time = time.time()
    call(dnaStrX, dnaStrY, obj.alpha_values, obj.delta_e)
    end_time = time.time()
    # memory_consumed = int(memory_info.rss/1024)
    # memory_consumed = tracemalloc.get_traced_memory()[1]/1000
    # tracemalloc.stop()
    memory_consumed = process_memory()
    mem_time_info[i]['mem'] = memory_consumed
    mem_time_info[i]['cpu'] = (end_time - start_time)*1000
  return mem_time_info

# basic_ps = getMemTimeInfoBasic()
dnc_ps = getMemTimeInfoDNC()

# with open("basic_ps.txt","w") as f:
#   f.write(str(basic_ps))
#   f.close()

with open("dnc_ps.txt","w") as f:
  f.write(str(dnc_ps))
  f.close()