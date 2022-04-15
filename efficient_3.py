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

def getSequences(X,Y,path,alpha,delta):
    s1=""
    s2=""
    score=0
    n=len(path) # n has to be equal to len(Y) 
    i=0
    j=0
    while(i!=n and j!=n): # assuming i is increasing upwards and j is increasing towards the right
        if (path[i]==path[i+1]):# next node is in the same column (upper row)
            s1 = s1+X[i]
            s2 = s2+'_'
            score += delta
            i += 1
        elif (path[i]+1 == path[i+1]):# next node is one col to the right (upper row)
            s1 = s1+X[i]
            s2 = s2+Y[j]
            score += alpha[X[i]][Y[j]]
            i+=1
            j+=1
        else:  # next node is more than one col to the right, thus go right one col
            s1 = s1+'_'
            s2 = s2+Y[j]
            score += delta
            j += 1
    return [str(score),s1,s2]
    


def basic_alignment(X, Y, alpha, delta):
    len_x = len(X)+1
    len_y = len(Y)+1

    #dp_matrix = [[] for _ in range(len_y)]
    dp_matrix = [[None for _ in range(len_y)] for _ in range(len_x)]
    #print(dp_matrix)
    for i in range(len_x):  # leftmost column
        dp_matrix[i][0] = i*delta

    for i in range(1, len_y):  # bottom row
        dp_matrix[0][i] = i*delta

    # down to top left to right
    for i in range(1, len_x):
        for j in range(1, len_y):
            dp_matrix[i][j] = min(
                dp_matrix[i-1][j-1] + alpha[X[i-1]][Y[j-1]],
                dp_matrix[i][j-1] + delta,
                dp_matrix[i-1][j] + delta
            )
        dp_matrix[i-1] = [] # removing rows to save space

    return dp_matrix[-1]  # returning topmost row


def findMiddleNode(X, Y, n, alpha, delta):

    # XL and all of Y
    left_array = basic_alignment(
        X[:n//2], Y, alpha, delta)

    # XR and all of Y
    right_array = basic_alignment(
        X[n//2:][::-1], Y[::-1], alpha, delta)

    # To find lowest among middle column of y
    # left matrix has y values in last row(lenx-1) from 1 to leny-1
    # right matrix has y values in first row(0) from 1 to leny-1 in reverse order

    low = 1
    m = len(left_array)
    for j in range(1, m):
        if(left_array[j]+right_array[m-1-j] < left_array[low]+right_array[m-1-low]):
            low = j

    # return index of j
    return low


def dnc_alignment(X, Y, ystart, alpha, delta):
    n = len(X)
    m = len(Y)
    
    # [TO DO] BASE CONDITION: CAN'T SEEM TO UNDERSTAND WHAT THE BASE CONDITION COULD BE TO RETURN J
#     https://www.youtube.com/watch?v=3TfDm8GpWRU&list=LL&index=1&t=126s     Video has some of the algorithm in it
    if n < 2 or m < 2:
        return [ystart+1]
    # DIVIDE STEP
    ycut = findMiddleNode(X, Y, n, alpha, delta)
    ycut = ycut + ystart # added ystart to ycut so that the j remains consistent for its position in Y[]

    # CONQUER RECURSIVE STEP gives the optimal solution (not value) (basically same as the top down pass)
    left = dnc_alignment(X[:n//2], Y[:ycut], ystart, alpha, delta)
    right = dnc_alignment(X[n//2:], Y[ycut:], ycut, alpha, delta)


    # COMBINE STEP JUST CONCATENATE
#     print(len(left+[ycut]+right))
#     print(left+[ycut]+right) # Check if the final list is increasing from j = 0 to n-1

    return left+[ycut]+right


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
#     data = dnc_alignment(dnaStrX, dnaStrY, obj.alpha_values, obj.delta_e)

    aligned_path = dnc_alignment(
        dnaStrX, dnaStrY, 0, obj.alpha_values, obj.delta_e)
    
    # iterate through all indices to know the score and the alignment
    data = getSequences(dnaStrX, dnaStrY, aligned_path,
                             obj.alpha_values, obj.delta_e)
    end_time = time.time()
    time_taken = (end_time - start_time)*1000
    memory_consumed = int(memory_info.rss/1024)
    print(f"{memory_consumed} KB")
    print(f"{time_taken:.2f} s")
    obj.write_output(output_file, data, time_taken, memory_consumed)
   



# For testing comment out above main and run using this one. This is the input1 from the sample test cases.


# if __name__ == '__main__':
#     obj = Utils()
#     dnaStrX, dnaStrY = "ACACACTGACTACTGACTGGTGACTACTGACTGGACTGACTACTGACTGGTGACTACTGACTGG", "TATTATTATACGCTATTATACGCGACGCGGACGCGTATACGCTATTATACGCGACGCGGACGCG"
#     aligned_path = dnc_alignment(
#         dnaStrX, dnaStrY, 0, obj.alpha_values, obj.delta_e)
    
#     # iterate through all indices to know the score and the alignment
#     data = getSequences(dnaStrX, dnaStrY, aligned_path,
#                              obj.alpha_values, obj.delta_e)
#     print(data)
    
    
    # required output: 
    # 1296,
    # _A_CA_CACT__G__A_C_TAC_TGACTG_GTGA__C_TACTGACTGGACTGACTACTGACTGGTGACTACT_GACTG_G
    # TATTATTA_TACGCTATTATACGCGAC_GCG_GACGCGTA_T_AC__G_CT_ATTA_T_AC__GCGAC_GC_GGAC_GCG
