import cudf
import cupy as cp
import os
import subprocess
#import cupyx
from src.run_gerbil import set_of_all_unique_kmers_extractor, single_genome_kmer_extractor


def kmer_matrix_sparsity (genome_list, kmer_size, tmp_dir, min_val=1, max_val=10**9):
    """Processes genome data and generates a Compressed Sparse Row (CSR) matrix representation."""
    
    # Define the output directory for extracted k-mers
    set_of_all_unique_kmers_dir = os.path.join(
        os.path.abspath(tmp_dir),
        f"temporary_set_of_all_unique_kmers_min{min_val}_max{max_val}_kmer{kmer_size}_no_d.csv"
    )
    
    # # Extract unique k-mers for the provided genome list
    # set_of_all_unique_kmers_extractor(genome_list, set_of_all_unique_kmers_dir, kmer_size, min_val, max_val, tmp_dir)

    # Load extracted k-mers into a cuDF DataFrame
    set_of_all_unique_kmers_dataframe = cudf.read_csv(set_of_all_unique_kmers_dir)
    set_of_all_unique_kmers_dataframe = set_of_all_unique_kmers_dataframe[["K-mer"]]


    # Read the genome list file and extract directory paths
    
    
    with open(genome_list, "r", encoding="utf-8") as file:
        genome_dirs = [line.strip() for line in file if line.strip()]

    # Counter for the total number of non-zero elements in the k-mer frequency matrix (int64)
    nnz_count = cp.int64(0)


    # Total size of the feature matrix (rows: unique k-mers, columns: genome count)
    feature_matrix_size = cp.int64(len(set_of_all_unique_kmers_dataframe) * len(genome_dirs))

    # Iterate over each genome directory and extract k-mer frequency data
    for genome_num, genome_dir in enumerate(genome_dirs):

        #tmp_dataframe_dir = single_genome_kmer_extractor(kmer_size, tmp_dir, genome_dir, genome_num)

        tmp_dataframe_dir = os.path.join(tmp_dir, f"temporary_output_genome_{genome_num}.csv")

        df_csv = cudf.read_csv(tmp_dataframe_dir)
        
        df_comp = set_of_all_unique_kmers_dataframe.reset_index()
        df_comp = df_comp.merge(df_csv, on="K-mer", how="right")
        df_comp.dropna(inplace=True)
        
        idx = df_comp["index"].values.astype(cp.uint32)

        size = idx.size

        nnz_count = nnz_count + size

        if genome_num % 10 == 0 and genome_num != 0:
            print(f"Processed {genome_num} genomes :", flush=True)
            print(f"Number of non-zero elements so far {nnz_count}", flush=True)
            print(f"Current density is : {round (100*nnz_count/(len(set_of_all_unique_kmers_dataframe)*genome_num+1),2)}%")

    
    return round (100*nnz_count/feature_matrix_size,2)