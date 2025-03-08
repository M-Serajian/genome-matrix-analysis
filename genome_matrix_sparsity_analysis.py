#!/usr/bin/env python3
import os
import sys
import cudf
import cupy as cp
import time  # Import time module for execution time measurement

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

    # Start the timer before executing the function
    start_time = time.time()

    sparsity = kmer_matrix_sparsity(
        genome_list=os.path.abspath(args.genome_list),
        kmer_size=args.kmer_size,
        tmp_dir=args.tmp,
        min_val=args.min,
        max_val=args.max
    )

    # Stop the timer after function execution
    end_time = time.time()
    execution_time = end_time - start_time  # Compute total execution time

    output_text = (
        f"The sparsity of the genome k-mer matrix is: {sparsity}\n"
        f"K-mer size: {args.kmer_size}\n"
        f"Temporary directory: {args.tmp}\n"
        f"Min value: {args.min}\n"
        f"Max value: {args.max}\n"
        f"-d flag activated: {'Yes' if args.d else 'No'}\n"
        f"Execution time: {execution_time:.2f} seconds\n"
    )

    print(output_text)

    # Ensure the output directory exists
    output_dir = os.path.abspath(args.output)  # Assuming -o is stored in args.output
    os.makedirs(output_dir, exist_ok=True)

    # Determine if -d flag is enabled (1 for enabled, 0 for disabled)
    d_status = 1 if args.d else 0

    # Construct the filename dynamically
    output_filename = f"feature_matrix_stats_k_min_{args.min}_max_{args.max}_d_{d_status}.txt"
    output_filepath = os.path.join(output_dir, output_filename)

    # Write output to the specified file
    with open(output_filepath, "w") as f:
        f.write(output_text)

    print(f"Report saved to {output_filepath}")
