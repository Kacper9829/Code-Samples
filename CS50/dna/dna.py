import csv
import sys


def main():

    args = sys.argv

    # TODO: Check for command-line usage
    if len(args) != 3:
        print("Usage: python dna.py csv txt")
        sys.exit()

    # TODO: Read database file into a variable
    dna_data = []
    with open(args[1], "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            dna_data.append(row)

    # TODO: Read DNA sequence file into a variable
    dna_sequence = []
    with open(args[2], "r") as file:
        dna_sequence = file.read().strip()

    # TODO: Find longest match of each STR in DNA sequence
    STR_names = []
    with open(args[1], "r") as f:
        reader = csv.DictReader(f)
        STR_names = reader.fieldnames[1:]

    dna_runs = {}
    for str in STR_names:
        dna_runs[str] = longest_match(dna_sequence, str)

    # TODO: Check database for matching profiles
    for person in dna_data:
        match = True
        for str in STR_names:
            if int(person[str]) != dna_runs[str]:
                match = False
                break
        if match == True:
            print(f"{person["name"]}")
            break

    if match == False:
        print("No match\n")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
