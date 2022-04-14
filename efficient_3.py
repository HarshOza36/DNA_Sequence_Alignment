import sys
import time
import psutil


class Utils:
    def __init__(self):
        self.alpha_values = {'A': {'A': 0, 'C': 110, 'G': 48, 'T': 94},
                             'C': {'A': 110, 'C': 0, 'G': 118, 'T': 48},
                             'G': {'A': 48, 'C': 118, 'G': 0, 'T': 110},
                             'T': {'A': 94, 'C': 48, 'G': 110, 'T': 0}}
        self.delta_e = 30

    def generateString(self,xy_str,indices):
        original_len = len(xy_str)
        for i in indices:
            xy_str = xy_str[:i+1] + xy_str + xy_str[i+1:]
            
        # Checking is the generated string matches the required length
        assert len(xy_str) == ((2**len(indices)) * original_len), ">>> New String generated is not matching the expected length!"
        return xy_str

    def parseInput(self,filename):
        with open(filename, 'r') as f:
            # using rstrip to remove \n at the last
            baseStrX = f.readline().rstrip()

            X_indices = []
            for line in f:
                line = line.rstrip()
                if line.isnumeric() is False: # Hence Indices are over the next base string started
                    break
                X_indices.append(int(line))

            baseStrY = line.rstrip()
            Y_indices = []
            for line in f:
                line = line.rstrip()
                Y_indices.append(int(line))

        if(baseStrX is None or baseStrY is None):
            print(">>> The Base Strings are None.\nPlease try again!")
        dnaStrX = self.generateString(baseStrX, X_indices)
        dnaStrY = self.generateString(baseStrY, Y_indices)
        return (dnaStrX.upper(), dnaStrY.upper())

    def write_output(self, op_file, data, time_taken, memory_consumed):
        with open(op_file, 'w') as f:
            f.write(f"{opt_cost}\n")
            for line in data:
                f.write(line + '\n')
            f.write(f"{time_taken:.2f} ms\n")
            f.write(f"{memory_consumed} KB")
            f.close()

def align(X,Y,alpha, delta):
    len_x = len(X)+1
    len_y = len(Y)+1
    #seq_1 = []
    #seq_2 = []

    #dp_matrix = [[] for _ in range(len_y)]
    dp_matrix = [[None for _ in range(len_y)] for _ in range(len_x)]
    #print(dp_matrix)
    for i in range(len_x):
        dp_matrix[i][0] = i*delta

    for i in range(1,len_y):
        dp_matrix[0][i] = i*delta

    #print(len(dp_matrix))
    for j in range(1,len_y):
        for i in range(1,len_x):
            #print(i,j)
            dp_matrix[i][j] = min(
                dp_matrix[i-1][j-1] + alpha[X[i-1]][Y[j-1]],
                dp_matrix[i][j-1] + delta,
                dp_matrix[i-1][j] + delta
            )
    #FOR THE NEXT TWO LINES. WE ARE FILLING TOP DOWN SO BASED ON MY UNDERSTANDING THE LAST ROW WILL RETURN
    #THE DESIRED THING THAT WE WANT
    #IN THE SIMILAR VEIN THE ROW J-1 FOR THE CURRENT COMPUTATION WILL NO LONGER BE NEEDED FOR THE NEXT COMPUTATION HENCE DELETE
        dp_matrix[j-1] = [] #REMOVE ROWS THAT ARENT NEEDED

    return dp_matrix[-1] #RETURN THAT CENTER ROW THINGY

def basic_alignment(X, Y, alpha, delta):
    len_x = len(X)+1
    len_y = len(Y)+1
    seq_1 = []
    seq_2 = []

    #dp_matrix = [[] for _ in range(len_y)]
    dp_matrix = [[None for _ in range(len_y)] for _ in range(len_x)]
    #print(dp_matrix)
    for i in range(len_x):
        dp_matrix[i][0] = i*delta

    for i in range(1,len_y):
        dp_matrix[0][i] = i*delta

    #print(len(dp_matrix))
    for j in range(1,len_y):
        for i in range(1,len_x):
            #print(i,j)
            dp_matrix[i][j] = min(
                dp_matrix[i-1][j-1] + alpha[X[i-1]][Y[j-1]],
                dp_matrix[i][j-1] + delta,
                dp_matrix[i-1][j] + delta
            )

    i = len_x-1
    j = len_y-1

    while i > 0 and j > 0:
        if dp_matrix[i-1][j-1] + alpha[X[i-1]][Y[j-1]] == dp_matrix[i][j]:
            seq_1.append(X[i-1])
            seq_2.append(Y[j-1])
            i-=1
            j-=1

        elif dp_matrix[i][j-1] + delta == dp_matrix[i][j]:
            seq_1.append('_')
            seq_2.append(Y[j-1])
            j-=1

        else:
            seq_1.append(X[i-1])
            seq_2.append('_')
            i-=1
    
    while i > 0:
        seq_1.append(X[i-1])
        seq_2.append('_')
        i-=1

    while j > 0:
        seq_1.append('_')
        seq_2.append(Y[j-1])
        j-=1

    return [dp_matrix[-1][-1], ''.join(seq_1[::-1]), ''.join(seq_2[::-1])]

def dnc_alignment(X,Y, alpha, delta):


   n = len(X)
   m = len(Y)
   if n < 2 or m < 2:
        return basic_alignment(X, Y)
   #DIVIDE 
   left = align(X[:n//2], Y, alpha, delta)
   right = align(X[n//2:][::-1], Y[::-1], alpha, delta) 
   #SINCE THE PATH OF THE OPTIMAL SOLUTION WILL GO FROM LEFT TO RIGHT FROM TOP TO BOTTOM
   #THE MAX SCORE WILL BE FROM SOME i IN LEFT to some m-i in RIGHT
   part = [left[i] + right[m-i] for i in range(m+1)]
   cut = part.index(min(part)) #MIN SCORE SINCE WE WANT LOWEST COST PATH
   left,right,part = [], [], []

   left_half = dnc_alignment(X[:n/2],Y[:cut], alpha, delta)
   right_half = dnc_alignment(X[n/2:],Y[cut:], alpha, delta) 
   return [(left_half[i] + right_half[i]) for i in range(len(left_half))]

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 filename.py inputFile.txt outputFile.txt")
        sys.exit()
    obj = Utils()
    dnaStrX, dnaStrY = obj.parseInput(sys.argv[1])
    output_file = sys.argv[2]
    process = psutil.Process()
    memory_info = process.memory_info()
    start_time = time.time()
    data = dnc_alignment(dnaStrX, dnaStrY, obj.alpha_values, obj.delta_e)
    end_time = time.time()
    time_taken = (end_time - start_time)*1000
    memory_consumed = int(memory_info.rss/1024)
    print(f"{memory_consumed} KB")
    print(f"{time_taken:.2f} s")
    obj.write_output(output_file, data, time_taken, memory_consumed)
   
