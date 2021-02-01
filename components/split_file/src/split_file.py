#!/usr/bin/env python3
import argparse
from pathlib import Path


# Function doing the actual work (Outputs first N lines from a text file)
def split_file(input_file, output_file, no_of_lines):
    for x, line in enumerate(input_file):
        if x >= no_of_lines:
            break
        _ = output_file.write(line)


# Defining and parsing the command-line arguments
parser = argparse.ArgumentParser(description='My program description')
parser.add_argument('--input1-path', type=str,
                    help='Path of the local file containing the Input 1 data.')  # Paths should be passed in, not hardcoded
parser.add_argument('--param1', type=int, default=100, help='Parameter 1.')
parser.add_argument('--output1-path', type=str,
                    help='Path of the local file where the Output 1 data should be written.')  # Paths should be passed in, not hardcoded
args = parser.parse_args()

# Creating the directory where the output file will be created (the directory may or may not exist).
Path(args.output1_path).parent.mkdir(parents=True, exist_ok=True)

with open(args.input1_path, 'r') as input1_file:
    with open(args.output1_path, 'w') as output1_file:
        split_file(input1_file, output1_file, args.param1)
