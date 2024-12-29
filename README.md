# data-cleaning-toolkit

## What is it?
`data-cleaning-toolkit` is a Python toolkit I created to solve a problem I kept running into: the tedious task of cleaning and standardizing textual data in pandas DataFrames. Across multiple projects, I found myself repeatedly writing the same DataFrame cleaning functions. This repetitive workflow became a significant time sink, prompting me to develop this toolkit as a personal solution for streamlining text cleaning within the pandas ecosystem.

## Main Features
The toolkit includes functions to:
- Extract digits from phone numbers while validating minimum length requirements
- Convert messy monetary values and percentages into proper numeric formats
- Standardize email addresses and URLs for consistency
- Transform scientific notation into regular decimal numbers
- Convert roman numerals to standard integers
- Perform basic encryption and decryption of sensitive data

## Installation

### Requirements
- Python 3.9 or higher
- Dependencies listed in requirements.txt

### Setup
```bash
# Get the code
git clone https://github.com/JpCurada/data-cleaning-toolkit.git
cd data-cleaning-toolkit

# Set up Python environment
python -m venv virt
source virt/bin/activate  # For Windows use: virt\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

## How to Use

### Basic Usage
```python
import pandas as pd
from src.main import DataCleaner

# Create a sample DataFrame
df = pd.DataFrame({
    'phone': ['+1-234-567-8901', '123456789'],
    'price': ['$123.45', '1,234'],
    'email': ['user@example.com', 'invalid']
})

# Create cleaner instance and clean data
cleaner = DataCleaner()
df = cleaner.clean_phone_numbers(df, ['phone'])      # Remove non-digits
df = cleaner.clean_monetary_values(df, ['price'])    # Convert to float
df = cleaner.clean_emails(df, ['email'])            # Standardize format
```

### Available Methods
Each method takes a DataFrame and column names as input:

```python
# Phone numbers: Keeps only digits
cleaner.clean_phone_numbers(df, ['phone_col'])  
# Input: '+1-234-567-8901' → Output: '12345678901'

# Money: Converts to float
cleaner.clean_monetary_values(df, ['price_col'])  
# Input: '$123.45' → Output: 123.45

# Percentages: Converts to decimal
cleaner.clean_percentages(df, ['percent_col'])  
# Input: '50%' → Output: 0.5

# Emails: Standardizes format
cleaner.clean_emails(df, ['email_col'])  
# Input: 'User@Example.com' → Output: 'user@example.com'

# URLs: Removes prefixes
cleaner.clean_urls(df, ['url_col'])  
# Input: 'https://example.com/' → Output: 'example.com'

# Scientific notation: Converts to decimal
cleaner.clean_scientific_notation(df, ['scientific_col'])  
# Input: '1.23e-4' → Output: 0.000123

# Roman numerals: Converts to integer
cleaner.clean_roman_numerals(df, ['roman_col'])  
# Input: 'IV' → Output: 4

# Encryption/Decryption
cleaner.encrypt_columns(df, ['sensitive_col'], 'secret123')
cleaner.decrypt_columns(df, ['col_encrypted'], 'secret123')
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Need Help?
- Create an issue on GitHub for bugs or feature requests
- Email: johncurada.work@gmail.com for direct support

## Contributing
To contribute:
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make your changes
4. Run tests to ensure quality
5. Submit a Pull Request

### Code Style Guidelines
- Follow PEP 8 Python style guidelines
- Include docstrings for all functions
- Add type hints for better code clarity
- Comment complex logic sections

**Important Note:** The encryption functions are basic implementations for personal use. For production systems handling sensitive data, please use established encryption libraries.