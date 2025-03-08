import os
import sys
import cudf
import cupy as cp

# Get the absolute path of the project root dynamically
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Ensure 'src' directory is added to sys.path
SRC_PATH = os.path.join(PROJECT_ROOT, "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

# Import custom modules from src
from args import parse_arguments
from kmer_cudf_merger import kmer_matrix_sparsity  # Assuming it's used somewhere

if __name__ == "__main__":
    args = parse_arguments()
    
    sparsity = kmer_matrix_sparsity(
        genome_list=os.path.abspath(args.genome_list),
        kmer_size=args.kmer_size,
        tmp_dir=args.tmp,
        min_val=args.min,
        max_val=args.max
    )

    print(f"The sparsity of the genome k-mer matrix is: {sparsity}")
