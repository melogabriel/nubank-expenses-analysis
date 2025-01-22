# Nubank Expense Dashboard Project

This project consolidates monthly credit card statement data from Nubank into a single CSV file, enabling data visualization through a Google Sheets dashboard in Looker Studio.

## Features

- Combine multiple `.csv` files containing Nubank credit card statements.
- Export a consolidated dataset for analysis.
- Use the dataset in Google Sheets to create a dashboard in Looker Studio.

## Project Workflow

1. **Data Collection**: Download monthly credit card statements from Nubank as `.csv` files.
2. **Data Consolidation**: Use a Python script to merge all `.csv` files into a single dataset.
3. **Data Visualization**: Import the consolidated CSV file into Google Sheets, and create a Looker Studio dashboard for visual insights.

## Prerequisites

- Python 3.x
- Pandas library (`pip install pandas`)

## Project Files

- `faturas_nubank_merge.py`: Python script to combine `.csv` files.
- `faturas_nubank.csv`: The consolidated dataset (generated after running the script).
- **Looker Studio Dashboard**: A visual representation of the data.

## Script Overview

The Python script reads all `.csv` files in a specified directory and combines them into a single file:

```python
import os
import glob
import pandas as pd

# Set the working directory
os.chdir("/path/to/your/folder")

# Get all CSV files in the directory
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

# Combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])

# Export the combined dataset
combined_csv.to_csv("faturas_nubank.csv", index=False, encoding='utf-8-sig')

```

## How to Use the Script

1.Place all the .csv files in a single folder.
2.	Update the os.chdir path in the script to point to your folder.
3.	Run the script to generate faturas_nubank.csv.

## Importing into Google Sheets

1.	Upload the faturas_nubank.csv file to Google Sheets.
2.	Format the data as needed for visualization.

## Looker Studio Integration

1.	Link the Google Sheet to Looker Studio.
2.	Create charts and metrics to visualize your credit card expenses.

## Future Enhancements

- Automate the download of Nubank statements using the API (if supported).
- Add more data cleaning or transformation steps in the script.

## License

This project is licensed under the MIT License.






