from utils import parseInput
from fixed_constants import acgt_indices, alpha_values, delta_e
import sys




if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 filename.py inputFile.txt")
        sys.exit()
    dnaStrX, dnaStrY = parseInput(sys.argv[1])
    print(dnaStrX, dnaStrY)