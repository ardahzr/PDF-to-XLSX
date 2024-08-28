import tabula
import pandas as pd
import os

def pdf_to_excel(pdf_file_path, master_df):
    # Read PDF file and extract the desired tables
    tables = tabula.read_pdf(pdf_file_path, pages='all', multiple_tables=True)
    df = tables[2]
    df2 = tables[3] # Edit for your PDF table format
    df3 = tables[4]
    
    # Concatenate
    combined_df = pd.concat([df.reset_index(drop=True), df2.reset_index(drop=True), df3.reset_index(drop=True)], axis=1)
    
    # Append the combined DataFrame
    master_df = pd.concat([master_df, combined_df], ignore_index=True)
    
    # Add a blank row after each PDF's data
    blank_row = pd.DataFrame([[None] * combined_df.shape[1]], columns=combined_df.columns)
    master_df = pd.concat([master_df, blank_row], ignore_index=True)
    
    return master_df

def process_pdfs_in_folder(folder_path, output_excel_file):
    master_df = pd.DataFrame()  # Initialize an empty DataFrame
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_file_path = os.path.join(folder_path, filename)
            master_df = pdf_to_excel(pdf_file_path, master_df)
    
    # Write the master DataFrame to a single Excel file
    master_df.to_excel(output_excel_file, sheet_name='Sheet1', index=False)

folder_path = '/home/libuntu/Desktop/Desktop'
output_excel_file = os.path.join(folder_path, 'combined_output.xlsx')
process_pdfs_in_folder(folder_path, output_excel_file)
