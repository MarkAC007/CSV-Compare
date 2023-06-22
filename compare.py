import pandas as pd
import csv


def read_csv(file_path):
    try:
        return pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        return pd.read_csv(file_path, encoding='ISO-8859-1')

def compare_csvs(csv1, csv2):
    # Merge DataFrames on the 'ID' column
    merged_csv = csv1.merge(csv2, on='ID', how='outer', suffixes=('_csv1', '_csv2'))

    # Initialize an empty DataFrame to store the comparison results
    comparison = pd.DataFrame()

    # Iterate through the columns, excluding the 'ID' column
    for column in merged_csv.columns:
        if column != 'ID':
            # Compare the columns from csv1 and csv2
            column_comparison = merged_csv[column].compare(merged_csv[column.replace('_csv1', '_csv2')], keep_shape=True)
            
            # Add the 'ID' column to the comparison result
            column_comparison['ID'] = merged_csv.loc[column_comparison.index, 'ID']
            
            # Set the column names for the comparison result
            column_comparison.columns = [column.replace('_csv1', '') + '_' + col for col in column_comparison.columns]
            
            # Concatenate the comparison result to the overall comparison DataFrame
            comparison = pd.concat([comparison, column_comparison], axis=1)

    # Set the 'ID' column as the index and remove it from the DataFrame
    if 'ID' in comparison.columns:
        comparison.index = comparison['ID']
        comparison.drop('ID', axis=1, inplace=True)
    else:
        print("No differences found between the CSV files.")

    return comparison


def generate_report(comparison, output_file):
    if comparison.empty:
        print("No differences found between the CSV files. No report generated.")
        return

    with open(output_file, 'w', newline='', encoding='utf-8') as report:
        writer = csv.writer(report)

        # Write the header row
        writer.writerow(['ID', 'Column', 'Value in CSV1', 'Value in CSV2'])

        # Iterate through the columns in the comparison DataFrame
        for column in comparison.columns[::2]:
            # Extract the changes for the current column
            column_changes = comparison[[column, column.replace('_self', '_other')]].dropna(how='all')

            # Iterate through the rows in the column_changes DataFrame
            for index, row in column_changes.iterrows():
                # Write a row for each change in the report
                writer.writerow([index, column.replace('_self', ''), row[column], row[column.replace('_self', '_other')]])


if __name__ == "__main__":
    file1 = "files/FedRAMP_Security_Controls_Baseline_Moderate_rev4.csv"
    file2 = "files/FedRAMP_Security_Controls_Baseline_Moderate_rev5.csv"
    output_report = "reports/rev4_rev5_compare.txt"

    csv1 = read_csv(file1)
    csv2 = read_csv(file2)

    comparison = compare_csvs(csv1, csv2)
    generate_report(comparison, output_report)

    print(f"Comparison report generated: {output_report}")