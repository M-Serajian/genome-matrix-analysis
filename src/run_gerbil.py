import cudf
import cupy as cp
import os
import subprocess


def set_of_all_unique_kmers_extractor(genome_file, output_directory, kmer_length, min_threshold, max_threshold, temp_directory):
    """Run the gerbil-DataFrame tool to extract unique k-mers from the given genome file."""
    command = [
        "./include/gerbil-DataFrame/build/gerbil",
        "-k", str(kmer_length),
        "-o", "csv",
        "-l", str(min_threshold),
        "-z", str(max_threshold),
        "-g",
        "-d",
        genome_file,
        temp_directory,
        output_directory
    ]
    
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print(f"Unique k-mers successfully extracted and stored at: {output_directory}")
    except subprocess.CalledProcessError as error:
        print(f"Error: Extraction of unique k-mers failed with return code {error.returncode}.")
        print(f"Standard Output:\n{error.stdout}")
        print(f"Standard Error:\n{error.stderr}")




def single_genome_kmer_extractor(kmer_size, tmp_dir, genome_dir, genome_number):
    """Extract k-mers from a single genome using the gerbil-DataFrame tool."""
    output_file = os.path.join(tmp_dir, f"temporary_output_genome_{genome_number}.csv")
    
    command = [
        "./include/gerbil-DataFrame/build/gerbil",
        "-k", str(kmer_size),
        "-o", "csv",
        "-l", str(1),
        "-z", str(10**9),  # Infinity
        "-g",
        genome_dir,
        tmp_dir,
        output_file
    ]
    
    result = subprocess.run(command, check=True, text=True, capture_output=True)
    
    return output_file




