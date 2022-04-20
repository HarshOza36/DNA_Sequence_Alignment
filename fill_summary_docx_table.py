# Using basic_ps and dnc_ps from generate_graphs output

x_axis = [16,64,128,256,384,512,768,1024,1280,1536,2048,2560,3072,3584,3968]

basic_ps = {0: {'cpu': 0.0, 'mem': 14172.0}, 1: {'cpu': 1.997232, 'mem': 14176.0}, 2: {'cpu': 2.997637, 'mem': 14196.0}, 3: {'cpu': 19.002199, 'mem': 14620.0}, 4: {'cpu': 33.00333, 'mem': 15500.0}, 5: {'cpu': 166.996479, 'mem': 16892.0}, 6: {'cpu': 168.00189, 'mem': 20296.0}, 7: {'cpu': 299.001455, 'mem': 24844.0}, 8: {'cpu': 566.999674, 'mem': 30940.0}, 9: {'cpu': 1076.993465, 'mem': 38280.0}, 10: {'cpu': 1292.025805, 'mem': 57204.0}, 11: {'cpu': 1947.019815, 'mem': 81940.0}, 12: {'cpu': 3743.002415, 'mem': 109924.0}, 13: {'cpu': 4435.030222, 'mem': 143408.0}, 14: {'cpu': 4987.976551, 'mem': 172488.0}} 
dnc_ps = {0: {'cpu': 0.0, 'mem': 14532.0}, 1: {'cpu': 1.997709, 'mem': 14396.0}, 2: {'cpu': 8.998394, 'mem': 14412.0}, 3: {'cpu': 29.978275, 'mem': 14444.0}, 4: {'cpu': 236.997366, 'mem': 14564.0}, 5: {'cpu': 143.009424, 'mem': 15016.0}, 6: {'cpu': 387.995005, 'mem': 15420.0}, 7: {'cpu': 599.000216, 'mem': 15692.0}, 8: {'cpu': 1035.977364, 'mem': 15612.0}, 9: {'cpu': 1415.992975, 'mem': 15780.0}, 10: {'cpu': 2401.023149, 'mem': 15344.0}, 11: {'cpu': 4241.99605, 
'mem': 15764.0}, 12: {'cpu': 5636.972666, 'mem': 16184.0}, 13: {'cpu': 9122.020721, 'mem': 16596.0}, 14: {'cpu': 8392.023563, 'mem': 16324.0}}

df = {"m+n":[],"Time in MS (Basic)":[],	"Time in MS (Efficient)":[],	"Memory in KB (Basic)":[],	"Memory in KB (Efficient)":[]}


for i in range(len(basic_ps)):
  df["m+n"].append(x_axis[i])
  df["Time in MS (Basic)"].append(basic_ps[i]['cpu'])
  df["Time in MS (Efficient)"].append(dnc_ps[i]['cpu'])
  df["Memory in KB (Basic)"].append(basic_ps[i]['mem'])
  df["Memory in KB (Efficient)"].append(dnc_ps[i]['mem'])

import pandas as pd

final = pd.DataFrame(df)
print(final)

final.to_csv("final_output.csv",index = False)