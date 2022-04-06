def generateString(xy_str,indices):
  original_len = len(xy_str)
  for i in indices:
      xy_str = xy_str[:i+1] + xy_str + xy_str[i+1:]
    
  # Checking is the generated string matches the required length
  assert len(xy_str) == ((2**len(indices)) * original_len), ">>> New String generated is not matching the expected length!"
  return xy_str

def parseInput(filename):
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
  dnaStrX = generateString(baseStrX, X_indices)
  dnaStrY = generateString(baseStrY, Y_indices)
  return (dnaStrX.upper(), dnaStrY.upper())