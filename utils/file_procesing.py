import pandas as pd
from typing import List
import openpyxl
from sqlalchemy import Engine
from langchain_ollama import OllamaEmbeddings
from sklearn.metrics.pairwise import cosine_similarity


def extract_tables_from_raw_dataframe(df: pd.DataFrame) -> List[pd.DataFrame]:
    """
    Extracts tables from the raw dataframe. A table is defined as a dataframe that has a non-null value in the first
    column. The first column is assumed to be the index column. This function will return a list of dataframes, where
    each dataframe is a table.

    :param df: pd.DataFrame - The raw dataframe
    :return: A list of dataframes, where each dataframe is a table
    """
    tables = []
    for i in range(len(df)):
        for j in range(len(df.columns)):
            if not pd.isnull(df.iloc[i, j]):
                
                bondaries = [i, j, i, j]
                stack = [(i, j)]

                while stack:
                    row, col = stack.pop()

                    if(row < bondaries[0]):
                        bondaries[0] = row
                    if(row > bondaries[2]):
                        bondaries[2] = row

                    if(col < bondaries[1]):
                        bondaries[1] = col
                    if(col > bondaries[3]):
                        bondaries[3] = col
                    
                    for k in range(max(0, row-1), min(len(df), row+2)):
                        for l in range(max(0, col-1), min(len(df.columns), col+2)):
                            if not pd.isnull(df.iloc[k, l]) and (k < bondaries[0] or k > bondaries[2] or l < bondaries[1] or l > bondaries[3]):
                                stack.append((k, l))

                

                # Extract the table and replace the values with None
                table = df.iloc[bondaries[0]+1:bondaries[2]+1, bondaries[1]:bondaries[3]+1].copy()
                table = table.set_axis(df.iloc[bondaries[0], bondaries[1]:bondaries[3]+1].copy(), axis=1)
                table.reset_index(drop=True, inplace=True)

                tables.append(table)
                df.iloc[bondaries[0]:bondaries[2]+1, bondaries[1]:bondaries[3]+1] = None

    return tables

def has_footer(table: pd.DataFrame) -> bool:
    """
    Check if the table has a footer by checking if the last row is far from the other rows in the embedding space

    :param table: pd.DataFrame - The table to check
    :return: bool - True if the table has a footer, False otherwise
    """
    
    embeddings_model = OllamaEmbeddings(model='nomic-embed-text')

    rows = list(map(lambda x: ','.join(str(val) for val in x if str(val) != 'nan'), table.iloc[-min(len(table), 10):].values))

    table_embeddings = embeddings_model.embed_documents(rows)

    # Compute pairwise cosine similarities
    similarity_matrix = cosine_similarity(table_embeddings)

    # Calculate the mean cosine similarity for each embedding
    mean_similarities = similarity_matrix.mean(axis=1)

    # Compare the last embedding's similarity to the mean of all others
    overall_mean_similarity = mean_similarities[:-1].mean()
    last_similarity = mean_similarities[-1]

    return last_similarity < overall_mean_similarity * 0.95


def clean_table(table: pd.DataFrame) -> None:
    """
    Cleans the table by removing any rows or columns that are all null values, remove useless columns, and rename columns

    :param table: pd.DataFrame - The table to clean
    """

    # Drop rows and columns that are all null values
    table.dropna(axis=0, how='all', inplace=True)
    table.dropna(axis=1, how='all', inplace=True)

    # Remove columns that are not strings
    for col in table.columns:
        if type(col) != str:
            table.drop(col, axis=1, inplace=True)

    # Rename the columns
    table.columns = [col.strip().lower().replace(' ', '_') for col in table.columns]

    if has_footer(table):
        table.drop(table.tail(1).index, inplace=True)

def extract_table_from_excel(file) -> List[pd.DataFrame]:
    """
    Extract multiple table from an excel file

    :param file: UploadedFile - The file to process

    :return: List[pd.DataFrame] - A dictionary containing the extracted tables
    """

    tables = []

    # Read the excel file
    xls = openpyxl.load_workbook(file)

    for sheet in xls.sheetnames:
        df = pd.read_excel(file, sheet_name=sheet, header=None)
        
        # Extract the tables from the raw dataframe
        tables += extract_tables_from_raw_dataframe(df)

    return tables

def extract_table_from_csv(file) -> List[pd.DataFrame]:
    """
    Extract multiple table from a csv file

    :param upload_file: UploadedFile - The file to process

    :return: List[pd.DataFrame] - A dictionary containing the extracted tables
    """

    tables = []

    # Read the csv file
    df = pd.read_csv(file, header=None, sep=None)
    
    # Extract the tables from the raw dataframe
    tables += extract_tables_from_raw_dataframe(df)

    return tables

def extract_data_from_file(file) -> List[pd.DataFrame]:
    """
    Extract multiple table from a file

    :param file: UploadedFile - The file to process

    :return: List[pd.DataFrame] - A dictionary containing the extracted tables
    """

    if file.name.endswith('.csv'):
        return extract_table_from_csv(file)
    elif file.name.endswith('.xlsx'):
        return extract_table_from_excel(file)
    else:
        raise ValueError('File type not supported')
    
def process_file(engine: Engine, file, index: int) -> None:
    """
    Process a file and extract the tables

    :param file: UploadedFile - The file to process
    """

    tables = extract_data_from_file(file)

    for table in tables:
        clean_table(table)

    for table in tables:
        table.to_sql(f'table_{index}', con=engine, if_exists='replace', index=False)
        index += 1

    return index


