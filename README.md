# Data-Cleaning-and-Validation

Simple examples using sample data from [https://www.kaggle.com/](https://www.kaggle.com/datasets/knightbearr/sales-product-data), data contained in the file is synthetic.

Summary of data_cleaning.py

1) Reads csv files directly from zip file, cleans and concatenate data.
2) Define specific data types and creation of "Total Sales" and split out address data.
3) Output the file as .parquet (retention of data types) and top 20 rows as a flat sample csv file.
