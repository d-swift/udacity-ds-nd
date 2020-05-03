import sys
import pandas as pd
from sqlalchemy import create_engine

category_column_list = ['id', 'categories']
message_column_list = ['id', 'message', 'original', 'genre']


def load_data(messages_fpath: str, categories_fpath: str) -> pd.DataFrame:
    """Load and merge dataframes.

    Args:
        messages_fpath: str. File path to a csv containing message data.
        categories_fpath: str. File path to a csv containing categories dta.
    Returns:
        df: pd.DataFrame. Dataframe containing messages and categories.
    """
    messages = pd.read_csv(messages_fpath)
    categories = pd.read_csv(categories_fpath)
    df = messages.merge(categories, on='id')
    return df


def clean_data(df: pd.DataFrame):
    """Remove duplicates and derive category labels for training.

    Args:
        df: pd.DataFrame. The messages and categories merged dataset.
    
    Returns:
        df: pd.DataFrame. Data ready for processing in an ML pipeline.
    """
    categories = df.categories.str.split(';', expand=True)
    row = categories.iloc[0]
    
    category_column_names = [category[:-2] for category in row]
    categories.columns = category_column_names
    
    for column in categories:
        categories[column] = categories[column].str[-1].astype(int)
    
    df.drop(columns='categories', inplace=True)
    
    df = pd.concat([df, categories], axis=1)
    df = df.drop_duplicates(keep='first')
    return df


def save_data(df: pd.DataFrame, sqlite_db_fname: str = 'disaster_project.db'):
    """Save data to SQlite database.

    Args:
        df: pd.DataFrame. Dataframe to save to the database.
        sqlite_db_fname: str. File name for the database.
    
    Returns:
        None
    """
    engine = create_engine(f'sqlite:///{sqlite_db_fname}')
    df.to_sql('messages_categories', engine, index=False)


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()