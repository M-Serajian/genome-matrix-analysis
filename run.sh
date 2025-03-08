#!/bin/bash

# Initialize variables (no default values)
k=""
min=""
max=""
d=""
genome_list=""
temporary_base=""
output_base=""

# Function to display usage
usage() {
    echo "Usage: $0 -k <kmer_size> -min <min_occurrence> -max <max_occurrence> -d <disable_normalization (0 or 1)> -l <genome_list> -t <temporary_directory> -o <output_directory>"
    exit 1
}

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -k) k="$2"; shift; shift ;;
        -min) min="$2"; shift; shift ;;
        -max) max="$2"; shift; shift ;;
        -d) d="$2"; shift; shift ;;
        -l) genome_list="$2"; shift; shift ;;
        -t) temporary_base="$2"; shift; shift ;;
        -o) output_base="$2"; shift; shift ;;
        *) echo "Unknown option: $1"; usage ;;
    esac
done

# Validate required arguments
if [[ -z "$k" || -z "$min" || -z "$max" || -z "$d" || -z "$genome_list" || -z "$temporary_base" || -z "$output_base" ]]; then
    echo "Error: Missing one or more required arguments."
    usage
fi

# Ensure temporary and output directories are valid
temporary_DIR="${temporary_base}/${k}/"
output_DIR="${output_base}/${k}/"

# Echo the variables before running the script
echo "--------------------------------------------------"
echo "Running genome matrix sparsity analysis"
echo "--------------------------------------------------"
echo "K-mer size (-k): $k"
echo "Minimum k-mer occurrence (-min): $min"
echo "Maximum k-mer occurrence (-max): $max"
echo "Disable normalization (-d): $([ "$d" -eq 1 ] && echo "Enabled" || echo "Disabled")"
echo "Genome list (-l): $genome_list"
echo "Temporary directory (-t): $temporary_DIR"
echo "Output directory (-o): $output_DIR"
echo "--------------------------------------------------"
echo ""

# Construct the Python command dynamically
python_cmd="python genome_matrix_sparsity_analysis.py -l ${genome_list} -t ${temporary_DIR} -k ${k} -o ${output_DIR} -min ${min} -max ${max}"

# Add the -d flag only if d=1
if [ "$d" -eq 1 ]; then
    python_cmd+=" -d"
fi

# Run the Python script
echo "Executing command:"
echo "$python_cmd"
echo "--------------------------------------------------"
$python_cmd
