from typing import List
import pandas as pd

def clean_phone_numbers(df: pd.DataFrame, col_names: List[str]) -> pd.DataFrame:

    # Input validation
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame")
        
    if not isinstance(col_names, list):
        raise TypeError("col_names must be a list")
        
    if len(col_names) == 0:
        raise ValueError("col_names cannot be empty")
        
    # Create copy of dataframe to avoid modifying original
    df = df.copy()

    def extract_digits(phone):
        try:
            # Return None for null values
            if pd.isna(phone):
                return None
                
            # Extract only digits from phone number    
            cleaned = ""
            for char in str(phone):
                if char.isdigit():
                    cleaned = cleaned + char
            
            # Return None if less than 9 digits        
            if len(cleaned) < 9:
                return None
                
            return cleaned
            
        except Exception as e:
            print(f"Error processing value {phone}: {str(e)}")
            return None

    # Process each column in the list
    for col in col_names:
        try:
            # Skip if column doesn't exist
            if col not in df.columns:
                print(f"Warning: Column '{col}' not found in DataFrame")
                continue
                
            # Apply cleaning to the column    
            df[col] = df[col].apply(extract_digits)
            
        except Exception as e:
            print(f"Error processing column {col}: {str(e)}")
            continue

    return df


def clean_monetary_values(df: pd.DataFrame, col_names: List[str]) -> pd.DataFrame:
    # Input validation
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame")
        
    if not isinstance(col_names, list):
        raise TypeError("col_names must be a list")
        
    if len(col_names) == 0:
        raise ValueError("col_names cannot be empty")

    # Create copy of dataframe to avoid modifying original
    df = df.copy()

    def extract_numbers(value):
        try:
            # Return None for null values
            if pd.isna(value):
                return None
                
            # Extract only digits and decimal point
            cleaned = ""
            for char in str(value):
                if char.isdigit() or char == '.':
                    cleaned = cleaned + char
                    
            # Convert to float
            return float(cleaned) if cleaned else None
            
        except Exception as e:
            print(f"Error processing value {value}: {str(e)}")
            return None

    # Process each column in the list
    for col in col_names:
        try:
            # Skip if column doesn't exist
            if col not in df.columns:
                print(f"Warning: Column '{col}' not found in DataFrame")
                continue
                
            # Apply cleaning to the column    
            df[col] = df[col].apply(extract_numbers)
            
        except Exception as e:
            print(f"Error processing column {col}: {str(e)}")
            continue

    return df