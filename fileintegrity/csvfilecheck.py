import csv

def read_csv(file_path):
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        return list(reader)

def compare_csv(file1, file2):
    csv1 = read_csv(file1)
    csv2 = read_csv(file2)

    if len(csv1) != len(csv2):
        print("The files have different number of rows.")
        return

    for row_index, (row1, row2) in enumerate(zip(csv1, csv2)):
        if len(row1) != len(row2):
            print(f"Row {row_index + 1} has different number of columns.")
            continue

        for col_index, (cell1, cell2) in enumerate(zip(row1, row2)):
            if cell1 != cell2:
                print(f"Difference found at Row {row_index + 1}, Column {col_index + 1}: '{cell1}' != '{cell2}'")

if __name__ == "__main__":
    file1 = 'path/to/first.csv'
    file2 = 'path/to/second.csv'
    compare_csv(file1, file2)