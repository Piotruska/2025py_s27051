# Purpose: This program allows the user to generate, read, and delete DNA sequences in FASTA format.
# It also provides nucleotide statistics for sequences.
# Context: Bioinformatics programming exercise with file I/O, DNA processing, and statistics.

# IMPROVEMENTS:
# 1. Input validation for sequence length to prevent invalid values
# 2. Reproducibility via fixed random seed (e.g., for testing/debugging)
# 3. Unique FASTA filename generation using timestamp to avoid overwrites
# 4. Name validation to disallow only uppercase A, T, G, C (allows lowercase)
# 5. Cleanly rounded and aligned nucleotide statistics display
# 6. Numbered menu for selecting or deleting FASTA files (improves usability)
# 7. Ability to delete FASTA files via menu
# 8. Ability to read and show FASTA file contents and computed stats via menu
# 9. Addition of a main menu for improved navigation and user experience

import random
import os
import re  # IMPROVEMENT 10: used to remove user's name case-insensitively
from datetime import datetime  # IMPROVEMENT 3

# Generates a random DNA sequence and saves it to a FASTA file
def generate_sequence():
    # IMPROVEMENT 1:
    # ORIGINAL:
    # sequence_length = int(input("Enter the sequence length: "))
    # MODIFIED (justification: prevents invalid input like negative numbers or text):
    while True:
        try:
            sequence_length = int(input("Enter the sequence length: "))
            if sequence_length > 0:
                break
            else:
                print("Length must be positive.")
        except ValueError:
            print("Please enter a valid integer.")

    sequence_id = input("Enter the sequence ID: ")
    sequence_description = input("Provide a description of the sequence: ")

    # IMPROVEMENT 4:
    # ORIGINAL:
    # if any(ch.upper() in "ATGC" for ch in user_name):
    # MODIFIED (justification: block only uppercase DNA letters to allow lowercase in names):
    while True:
        user_name = input("Enter your name (avoid uppercase letters A, T, G, C): ")
        if any(ch in "ATGC" for ch in user_name):
            print("Name cannot contain uppercase letters A, T, G, or C.")
        else:
            break

    # IMPROVEMENT 3:
    # ORIGINAL:
    # filename = f"{sequence_id}.fasta"
    # MODIFIED (justification: prevent overwriting by adding timestamp to filename):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{sequence_id}_{timestamp}.fasta"

    # IMPROVEMENT 2:
    # ORIGINAL:
    # dna_sequence = ''.join(random.choices(['A', 'C', 'G', 'T'], k=sequence_length))
    # MODIFIED (justification: make randomness deterministic for debugging):
    random.seed(42)
    dna_bases = ['A', 'C', 'G', 'T']
    dna_sequence = ''.join(random.choices(dna_bases, k=sequence_length))

    insert_position = random.randint(0, sequence_length)
    dna_with_name = dna_sequence[:insert_position] + user_name + dna_sequence[insert_position:]

    with open(filename, 'w') as fasta_file:
        fasta_file.write(f">{sequence_id} {sequence_description}\n")
        fasta_file.write(dna_with_name + "\n")

    print(f"\nThe sequence was saved to the file {filename}")
    print_sequence_stats(dna_with_name, user_name)

# Calculates and displays nucleotide composition and CG ratio
def print_sequence_stats(sequence, user_name):
    # IMPROVEMENT 10:
    # ORIGINAL:
    # sequence = sequence.upper()
    # MODIFIED (justification: remove all case-insensitive occurrences of user's name from sequence):
    pattern = re.compile(re.escape(user_name), re.IGNORECASE)
    sequence_cleaned = pattern.sub('', sequence)
    sequence_cleaned = ''.join([ch for ch in sequence_cleaned if ch.upper() in 'ACGT']).upper()

    a_count = sequence_cleaned.count('A')
    c_count = sequence_cleaned.count('C')
    g_count = sequence_cleaned.count('G')
    t_count = sequence_cleaned.count('T')
    total = len(sequence_cleaned)

    if total == 0:
        print("Empty sequence — no statistics to show.")
        return

    # IMPROVEMENT 5:
    a_pct = round((a_count / total) * 100, 1)
    c_pct = round((c_count / total) * 100, 1)
    g_pct = round((g_count / total) * 100, 1)
    t_pct = round((t_count / total) * 100, 1)
    cg_pct = round(((c_count + g_count) / total) * 100, 1)

    print("Sequence statistics:")
    print(f"A: {a_pct:>5}%")
    print(f"C: {c_pct:>5}%")
    print(f"G: {g_pct:>5}%")
    print(f"T: {t_pct:>5}%")
    print(f"%CG: {cg_pct:>4}")

# IMPROVEMENT 8:
# ORIGINAL:
# (no file-reading functionality in base requirements)
# MODIFIED (justification: allows user to read FASTA files, see contents and stats):
def read_fasta_file():
    fasta_files = [f for f in os.listdir() if f.endswith(".fasta")]

    if not fasta_files:
        print("No FASTA files found.")
        return

    # IMPROVEMENT 6:
    print("\nAvailable FASTA files:")
    for i, f in enumerate(fasta_files, 1):
        print(f"{i}. {f}")

    try:
        choice = int(input("Enter the number of the file to read: "))
        if 1 <= choice <= len(fasta_files):
            file_name = fasta_files[choice - 1]
        else:
            print("Invalid selection.")
            return
    except ValueError:
        print("Invalid input.")
        return

    print(f"\nContents of {file_name}:")
    with open(file_name, 'r') as file:
        lines = file.readlines()
        for line in lines:
            print(line.strip())

    if len(lines) >= 2:
        sequence = lines[1].strip()
        user_name = input("To calculate statistics, please re-enter the name that was inserted: ")
        print_sequence_stats(sequence, user_name)

# IMPROVEMENT 7:
# ORIGINAL:
# (no file-deletion functionality in base requirements)
# MODIFIED (justification: allows cleanup of FASTA files through the interface):
def delete_fasta_file():
    fasta_files = [f for f in os.listdir() if f.endswith(".fasta")]

    if not fasta_files:
        print("No FASTA files to delete.")
        return

    print("\nFASTA files available for deletion:")
    for i, f in enumerate(fasta_files, 1):
        print(f"{i}. {f}")

    try:
        choice = int(input("Enter the number of the file to delete: "))
        if 1 <= choice <= len(fasta_files):
            file_to_delete = fasta_files[choice - 1]
            confirm = input(f"Are you sure you want to delete '{file_to_delete}'? (y/n): ")
            if confirm.lower() == 'y':
                os.remove(file_to_delete)
                print(f"'{file_to_delete}' has been deleted.")
            else:
                print("Deletion canceled.")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input.")

# IMPROVEMENT 9:
# ORIGINAL:
# (no menu system in base requirements; user would run one task at a time)
# MODIFIED (justification: adds a persistent interface for user navigation and usability):
def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Create new DNA sequence")
        print("2. Read FASTA file")
        print("3. Delete FASTA file")
        print("4. Exit")

        choice = input("Choose an option (1–4): ")

        if choice == '1':
            generate_sequence()
        elif choice == '2':
            read_fasta_file()
        elif choice == '3':
            delete_fasta_file()
        elif choice == '4':
            print("Exiting the program.")
            break
        else:
            print("Invalid option. Please choose 1–4.")

if __name__ == "__main__":
    main_menu()
