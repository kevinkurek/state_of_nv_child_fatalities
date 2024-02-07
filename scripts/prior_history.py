import os
import pandas as pd
import fitz  # PyMuPDF
import re
from .child_fatality_scrape import *

# Function to count dates in the "G." section of a PDF
def count_dates_in_g_section(pdf_data):
    # Open the PDF from the binary data
    doc = fitz.open(stream=pdf_data, filetype="pdf")
    text = ""
    # Extract text from each page
    for page in doc:
        text += page.get_text()
    doc.close()
    
    # Find the section starting with "G." and ending before "H." or the end of the document
    section_g = re.search(r'(?<=G\.).+?(?=H\.|\Z)', text, re.DOTALL)
    if not section_g:
        return 0  # If "G." section is not found, return 0

    section_g_text = section_g.group(0)
    # print(section_g_text)
    # Define a regex pattern for dates (MM/DD/YYYY or MM/DD/YY)
    date_pattern = re.compile(r'\b\d{1,2}/\d{1,2}/\d{2,4}\b')
    # Find all dates in the "G." section
    dates = date_pattern.findall(section_g_text)

    # kevin intervention, ChatGPT cannot see multi-line 0400 12/03/2021 date from footer, simply subtract 1
    if len(dates)==0:
        total_dates = len(dates)
    else:
        total_dates = len(dates) - 1

    return total_dates

def count_pdf_paths(pdf_paths):
    # Dictionary to hold the counts of dates for each PDF
    date_counts = {}

    # Process each PDF file and count the dates in the "G." section
    for pdf_path in pdf_paths:
        # Read the binary data of the PDF file
        with open(pdf_path, "rb") as f:
            pdf_data = f.read()
        # Count the dates in the "G." section
        date_counts[pdf_path] = count_dates_in_g_section(pdf_data)

    return date_counts

def turn_pdf_counts_into_dataframe(pdf_paths):

    # calls count_pdf_paths(count_dates_in_g_section()) for each pdf
    count_pdf_dict = count_pdf_paths(pdf_paths)

    # display(count_pdf_dict)
    processed_dict = {'/'.join(key.split('/')[-2:]): value for key, value in count_pdf_dict.items()}
    # processed_dict
    df = pd.DataFrame(list(processed_dict.items()), columns=['original_pdf', 'prior_cases_count'])
    df[['original_region', 'original_pdf']] = df['original_pdf'].str.split('/', expand=True)

    # Remove '_pdfs' from the 'original_region' column
    df['original_region'] = df['original_region'].str.replace('_pdfs', '')

    # Get a list of all other columns excluding 'original_region' and 'original_pdf'
    other_columns = [col for col in df.columns if col not in ['original_region', 'original_pdf']]

    # Define the new column order with 'original_region' and 'original_pdf' first
    new_column_order = ['original_region', 'original_pdf'] + other_columns

    # Reassign the DataFrame with the new column order
    df = df[new_column_order]
    
    return df

def list_files_and_folders(directory):

    items = os.listdir(directory)
    files_and_folders = [(item, "folder" if os.path.isdir(os.path.join(directory, item)) else "file") for item in items]

    folders = [os.path.join(directory, i[0]) for i in files_and_folders if i[-1]=='folder']
    return folders

def list_csv_files(directory):

    # List everything in the directory
    items = os.listdir(directory)
    
    # Filter for files that end with .csv
    csv_files = [item for item in items if item.endswith('.csv') and os.path.isfile(os.path.join(directory, item))]
    
    return csv_files

def dataframe_for_each_region(directory_path):
    
    pdf_folders = list_files_and_folders(directory_path)

    for pdf_folder in pdf_folders:
        print(pdf_folder)
        pdf_paths = list_files(pdf_folder, append_base_path=True)
        df = turn_pdf_counts_into_dataframe(pdf_paths=pdf_paths)

        # output count csvs to folder
        df_name = pdf_folder.split("/")[-1]
        df.to_csv(os.path.join(directory_path, f"{df_name}_prior_counts.csv"), index=False)

def merge_and_save_csv(directory):
    files_to_merge = [
        ('Rural_pdfs_prior_counts.csv', 'child_fatality_Rural.csv'),
        ('Washoe_pdfs_prior_counts.csv', 'child_fatality_Washoe.csv'),
        ('Clark_pdfs_prior_counts.csv', 'child_fatality_Clark.csv')
    ]

    # BUG: Does not work for FOLDER implementation for merging













    # Append the directory to each file in the tuple pairs and update the region name extraction
    files_to_merge_with_path = [
        (os.path.join(directory, file1), os.path.join(directory, file2), file1.split('_')[0])
        for file1, file2 in files_to_merge
    ]

    # Iterate over the files to merge them
    for prior_counts_file, child_fatality_file, region_name in files_to_merge_with_path:
        # Read the DataFrames from the files
        df_prior_counts = pd.read_csv(prior_counts_file)
        df_child_fatality = pd.read_csv(child_fatality_file)




        ### BUG: original_region in df_prior_counts is now "output_files" rather than county


        # so they are not merging properly

    # df_prior_counts
        
        # original_region                          original_pdf  prior_cases_count
    # 0    output_files         Rural_pdfs\1453180_5_2_23.pdf                  8
    # 1    output_files  Rural_pdfs\1462383_60_day_update.pdf                  0
        
        # df_child_fatality

        # original_region                original_pdf
        #    Rural                          1453180_5_2_23.pdf



        ###




        
        # Merge the DataFrames on 'original_region' and 'original_pdf'
        merged_df = pd.merge(df_child_fatality, 
                             df_prior_counts[['original_region', 'original_pdf', 'prior_cases_count']],
                             on=['original_region', 'original_pdf'], how='left')
        
        # some that don't span multi-pages end up with -1 and needs to be a zero instead
        merged_df['prior_cases_count'] = merged_df['prior_cases_count'].replace(-1, 0)
        # print(merged_df.head())

        # Get a list of all column names
        columns = list(merged_df.columns)

        # Remove 'prior_cases_count' from the list
        columns.remove('prior_cases_count')

        # Insert 'prior_cases_count' at the desired new position (index 2 for the third position, as indexing starts at 0)
        columns.insert(2, 'prior_cases_count')

        # Reindex the DataFrame with the new column order
        merged_df = merged_df[columns]
        
        # Construct the output filename
        output_filename = f"{region_name}_merged.csv"
        
        # Save the merged DataFrame to the specified directory
        output_filepath = os.path.join(directory, output_filename)
        print(output_filepath)
        merged_df.to_csv(output_filepath, index=False)
        print(f"Saved merged file to {output_filepath}")

def run_and_merge_prior_history_counts(directory):

    # creates an output csv for each dataframe of counts
    dataframe_for_each_region(directory)

    # merge original fatality scraping and newly created prior history counts together
    merge_and_save_csv(directory)


if __name__ == "__main__":

    run_and_merge_prior_history_counts()

