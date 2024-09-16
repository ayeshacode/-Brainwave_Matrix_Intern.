import pandas as pd

# Load the dataset
data = pd.read_csv('dataset.csv')

# Display the first few rows of the dataset
print(data.head())

# Display basic information about the dataset
print(data.info())

# Display summary statistics for numerical columns
print(data.describe())
import numpy as np

# Clean the 'Price' column by handling non-standard formats
def extract_price(price):
    if isinstance(price, str):
        # If the price contains a range, take the average of the two prices
        if 'through' in price:
            try:
                # Extract both prices, convert to float, and take the average
                prices = [float(p) for p in price.replace('through', '-').split('-')]
                return np.mean(prices)
            except:
                return np.nan
        else:
            try:
                return float(price.replace('$', '').strip())
            except:
                return np.nan
    return np.nan

# Apply the function to clean the 'Price' column
data['Price'] = data['Price'].apply(extract_price)

# Extract the rating value and convert it to numeric
data['Rating Value'] = data['Rating'].str.extract(r'Rated ([\d.]+) out of 5').astype(float)

# Extract the number of reviews and convert it to numeric
data['Review Count'] = data['Rating'].str.extract(r'based on (\d+) reviews').astype(float)

# Check for missing values and data types after conversion
print(data.info())
# Descriptive statistics for numeric columns
numeric_summary = data[['Price', 'Rating Value', 'Review Count']].describe()
print(numeric_summary)

# Identify top categories by total sales
top_categories = data.groupby('Sub Category')['Price'].sum().sort_values(ascending=False)
print(top_categories)

# Identify top-rated products
top_rated_products = data[data['Rating Value'] == 5][['Title', 'Price', 'Review Count']].sort_values(by='Review Count', ascending=False)
print(top_rated_products)

# Identify most reviewed products
most_reviewed_products = data.sort_values(by='Review Count', ascending=False)[['Title', 'Rating Value', 'Review Count', 'Price']]
print(most_reviewed_products.head(10))
import matplotlib.pyplot as plt
import seaborn as sns

# Set the style for seaborn
sns.set(style="whitegrid")

# Visualization 1: Price Distribution
plt.figure(figsize=(10, 6))
sns.histplot(data['Price'], bins=30, kde=True)
plt.title('Price Distribution of Products')
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.show()

# Visualization 2: Total Sales by Sub Category
plt.figure(figsize=(12, 6))
sales_by_category = data.groupby('Sub Category')['Price'].sum().reset_index()
sns.barplot(x='Price', y='Sub Category', data=sales_by_category, palette='viridis')
plt.title('Total Sales by Sub Category')
plt.xlabel('Total Sales (in $)')
plt.ylabel('Sub Category')
plt.show()

# Visualization 3: Ratings vs. Review Count
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Rating Value', y='Review Count', data=data, hue='Sub Category', palette='Set2')
plt.title('Ratings vs. Review Count')
plt.xlabel('Rating Value')
plt.ylabel('Review Count')
plt.legend(title='Sub Category', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()
