from typing import List, Optional
import pandas as pd

class DataCleaner:
    """
    A data cleaning toolkit for pandas DataFrames that provides functions to:
    1. Clean and standardize data types
    2. Format numeric values and text
    3. Convert between different formats
    4. Encrypt/decrypt sensitive information
    
    Each method takes a DataFrame and column names as input, returning a cleaned copy.
    Invalid or malformed values are converted to None.
    
    Example:
        cleaner = DataCleaner()
        df = cleaner.clean_phone_numbers(df, ['phone_col'])
        df = cleaner.clean_monetary_values(df, ['price_col'])
    """
    
    def __init__(self):
        # Mapping for roman numeral conversion
        self.roman_values = {
            'I': 1, 'V': 5, 'X': 10, 
            'L': 50, 'C': 100, 'D': 500, 'M': 1000
        }
        # Common URL prefixes to be removed during cleaning
        self.url_prefixes = ['http://', 'https://', 'www.']

    def _validate_inputs(self, df: pd.DataFrame, col_names: List[str]) -> None:
        """
        Validate input parameters before processing.
        
        Args:
            df: Input DataFrame to validate
            col_names: List of column names to validate
            
        Raises:
            TypeError: If df is not DataFrame or col_names not list
            ValueError: If col_names is empty
        """
        if not isinstance(df, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame")
        if not isinstance(col_names, list):
            raise TypeError("Column names must be provided as a list")
        if not col_names:
            raise ValueError("Column names list cannot be empty")

    def _process_columns(self, df: pd.DataFrame, col_names: List[str], cleaning_func) -> pd.DataFrame:
        """
        Apply cleaning function to specified columns in DataFrame.
        
        Args:
            df: Input DataFrame
            col_names: List of columns to process
            cleaning_func: Function to apply to each column
            
        Returns:
            DataFrame with cleaned columns
        """
        self._validate_inputs(df, col_names)
        df = df.copy()
        
        for col in col_names:
            try:
                if col not in df.columns:
                    print(f"Warning: Column '{col}' not found in DataFrame")
                    continue
                df[col] = df[col].apply(cleaning_func)
            except Exception as e:
                print(f"Error processing column '{col}': {str(e)}")
                continue
                
        return df

    def _encrypt_value(self, value: str, code_name: str) -> Optional[str]:
        """
        Encrypt a single value using simple ASCII shift.
        
        Args:
            value: Value to encrypt
            code_name: Key used for encryption
            
        Returns:
            Encrypted string or None if input is null
        """
        if pd.isna(value):
            return None
            
        # Create numeric key from code_name
        numeric_key = sum(ord(c) for c in code_name)
        
        # Shift each character by key
        encrypted = ""
        for char in str(value):
            shifted = chr((ord(char) + numeric_key) % 128)
            encrypted += shifted
            
        return encrypted

    def _decrypt_value(self, value: str, code_name: str) -> Optional[str]:
        """
        Decrypt a previously encrypted value.
        
        Args:
            value: Encrypted value to decrypt
            code_name: Same key used for encryption
            
        Returns:
            Decrypted string or None if input is null
        """
        if pd.isna(value):
            return None
            
        # Use same numeric key as encryption
        numeric_key = sum(ord(c) for c in code_name)
        
        # Reverse the character shift
        decrypted = ""
        for char in str(value):
            shifted = chr((ord(char) - numeric_key) % 128)
            decrypted += shifted
            
        return decrypted

    def clean_phone_numbers(self, df: pd.DataFrame, col_names: List[str], min_digits: int = 9) -> pd.DataFrame:
        """
        Clean phone numbers in specified columns.
        
        Args:
            df: Input DataFrame
            col_names: Columns containing phone numbers
            min_digits: Minimum required digits (default: 9)
            
        Returns:
            DataFrame with cleaned phone numbers (digits only)
        
        Example:
            '+1 (234) 567-8901' -> '12345678901'
            '123-456' -> None (too few digits)
        """
        def clean_phone(phone) -> Optional[str]:
            if pd.isna(phone):
                return None
                
            # Extract only digits
            cleaned = ''.join(char for char in str(phone) if char.isdigit())
            return cleaned if len(cleaned) >= min_digits else None
            
        return self._process_columns(df, col_names, clean_phone)

    def clean_monetary_values(self, df: pd.DataFrame, col_names: List[str]) -> pd.DataFrame:
            """
            Clean monetary values by keeping only numbers and decimal points.
            
            Args:
                df: Input DataFrame
                col_names: Columns containing monetary values
                
            Returns:
                DataFrame with cleaned monetary values as floats
            
            Example:
                '$123.45' -> 123.45
                '1,234' -> 1234.0
                'free' -> None
            """
            def clean_amount(value) -> Optional[float]:
                if pd.isna(value):
                    return None
                    
                # Keep only digits and decimal point
                cleaned = ''.join(char for char in str(value) 
                                if char.isdigit() or char == '.')
                
                return float(cleaned) if cleaned else None
                
            return self._process_columns(df, col_names, clean_amount)

    def clean_percentages(self, df: pd.DataFrame, col_names: List[str]) -> pd.DataFrame:
        """
        Convert percentage strings to decimal values.
        
        Args:
            df: Input DataFrame
            col_names: Columns containing percentage values
            
        Returns:
            DataFrame with percentages as decimal floats
        
        Example:
            '50%' -> 0.5
            '12.5%' -> 0.125
            'invalid' -> None
        """
        def clean_percentage(value) -> Optional[float]:
            if pd.isna(value):
                return None
                
            # Extract numbers and decimal point
            cleaned = ''.join(char for char in str(value) 
                            if char.isdigit() or char == '.')
                            
            # Convert to decimal form
            return float(cleaned)/100 if cleaned else None
            
        return self._process_columns(df, col_names, clean_percentage)

    def clean_emails(self, df: pd.DataFrame, col_names: List[str]) -> pd.DataFrame:
        """
        Standardize email addresses.
        
        Args:
            df: Input DataFrame
            col_names: Columns containing email addresses
            
        Returns:
            DataFrame with standardized email addresses
        
        Example:
            'User@Example.com ' -> 'user@example.com'
            'invalid' -> None (no @ symbol)
        """
        def clean_email(email) -> Optional[str]:
            if pd.isna(email):
                return None
                
            cleaned = str(email).strip().lower()
            return cleaned if '@' in cleaned else None
            
        return self._process_columns(df, col_names, clean_email)

    def clean_urls(self, df: pd.DataFrame, col_names: List[str]) -> pd.DataFrame:
        """
        Standardize URLs by removing common prefixes and trailing slashes.
        
        Args:
            df: Input DataFrame
            col_names: Columns containing URLs
            
        Returns:
            DataFrame with standardized URLs
        
        Example:
            'https://example.com/' -> 'example.com'
            'www.test.com' -> 'test.com'
        """
        def clean_url(url) -> Optional[str]:
            if pd.isna(url):
                return None
                
            # Convert to lowercase and remove whitespace
            cleaned = str(url).strip().lower()
            
            # Remove standard prefixes
            for prefix in self.url_prefixes:
                if cleaned.startswith(prefix):
                    cleaned = cleaned[len(prefix):]
                    
            return cleaned.rstrip('/') if cleaned else None
            
        return self._process_columns(df, col_names, clean_url)

    def clean_scientific_notation(self, df: pd.DataFrame, col_names: List[str]) -> pd.DataFrame:
        """
        Convert scientific notation to decimal numbers.
        
        Args:
            df: Input DataFrame
            col_names: Columns containing scientific notation
            
        Returns:
            DataFrame with values as decimal floats
        
        Example:
            '1.23e-4' -> 0.000123
            '1e3' -> 1000.0
            'invalid' -> None
        """
        def clean_scientific(value) -> Optional[float]:
            if pd.isna(value):
                return None
                
            str_val = str(value).lower()
            
            if 'e' in str_val:
                try:
                    # Split into base and exponent
                    base, exp = str_val.split('e')
                    base = float(''.join(c for c in base if c.isdigit() or c == '.'))
                    exp = float(''.join(c for c in exp if c.isdigit() or c == '-'))
                    return base * (10 ** exp)
                except:
                    return None
                    
            # Handle regular decimal numbers
            cleaned = ''.join(char for char in str_val 
                            if char.isdigit() or char == '.')
            return float(cleaned) if cleaned else None
            
        return self._process_columns(df, col_names, clean_scientific)

    def clean_roman_numerals(self, df: pd.DataFrame, col_names: List[str]) -> pd.DataFrame:
        """
        Convert roman numerals to integers.
        
        Args:
            df: Input DataFrame
            col_names: Columns containing roman numerals
            
        Returns:
            DataFrame with values as integers
            
        Example:
            'IV' -> 4
            'XII' -> 12
            'ABC' -> None (invalid roman numeral)
        """
        def clean_roman(roman_str) -> Optional[int]:
            if pd.isna(roman_str):
                return None
                
            # Convert to uppercase and remove spaces
            roman = str(roman_str).strip().upper()
            
            # Validate characters
            if not all(char in self.roman_values for char in roman):
                return None
                
            # Convert to integer using roman numeral rules
            result = 0
            for i in range(len(roman)):
                # If next numeral is larger, subtract current
                if (i + 1 < len(roman) and 
                    self.roman_values[roman[i]] < self.roman_values[roman[i + 1]]):
                    result -= self.roman_values[roman[i]]
                else:
                    result += self.roman_values[roman[i]]
                    
            return result
            
        return self._process_columns(df, col_names, clean_roman)

    def encrypt_columns(self, df: pd.DataFrame, col_names: List[str], code_name: str) -> pd.DataFrame:
        """
        Encrypt column values and rename columns with '_encrypted' suffix.
        
        Args:
            df: Input DataFrame
            col_names: Columns to encrypt
            code_name: Encryption key
            
        Returns:
            DataFrame with encrypted values in renamed columns
            
        Note: This is a simple encryption for demonstration. Use proper
        encryption libraries for sensitive data.
        """
        df = df.copy()
        
        for col in col_names:
            if col not in df.columns:
                print(f"Warning: Column '{col}' not found")
                continue
                
            # Create encrypted column
            new_col = f"{col}_encrypted"
            df[new_col] = df[col].apply(lambda x: self._encrypt_value(x, code_name))
            
            # Remove original column
            df = df.drop(col, axis=1)
            
        return df

    def decrypt_columns(self, df: pd.DataFrame, col_names: List[str], code_name: str) -> pd.DataFrame:
        """
        Decrypt previously encrypted columns and restore original names.
        
        Args:
            df: Input DataFrame
            col_names: Encrypted columns (must end with '_encrypted')
            code_name: Same key used for encryption
            
        Returns:
            DataFrame with decrypted values in renamed columns
        """
        df = df.copy()
        
        for col in col_names:
            if col not in df.columns:
                print(f"Warning: Column '{col}' not found")
                continue
                
            # Restore original column name
            new_col = col.replace('_encrypted', '')
            df[new_col] = df[col].apply(lambda x: self._decrypt_value(x, code_name))
            
            # Remove encrypted column
            df = df.drop(col, axis=1)
            
        return df
    
