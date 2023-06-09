import pandas as pd, os
from zipfile import ZipFile
from typing import List

def create_dataframe(zip_file:str) -> pd.DataFrame:

    data_frame_list = []

    # read the file names in the zip file, create as dataframe and store in dictionary
    with ZipFile(zip_file, "r") as z:
        for file_name in z.namelist():
            try:
                with z.open(file_name) as f:
                    df = pd.read_csv(f, dtype="string").dropna(how="all").fillna(0)
                    data_frame_list.append(df)

            # If we receive a file that is not expected
            except Exception as e:
                print(f"File read error: {e}")
                continue

    # Concat the list of dataframes on column headers
    df = pd.concat(data_frame_list)

    # Clean out the merged source data
    df = df[~(df == df.columns).all(axis=1)]

    return df

def format_dataframe(df:pd.DataFrame) -> pd.DataFrame:

    # Set specific datatypes
    df["Quantity Ordered"] = df["Quantity Ordered"].fillna(0).astype("int8")
    df["Price Each"] = df["Price Each"].fillna(0.00).astype("float32")

    # Round prices to 2 decimals
    df["Price Each"] = df["Price Each"].apply(lambda x: round(x, 2))

    # Add total sales
    df["Total Sales"] = df["Price Each"] * df["Quantity Ordered"]

    # Format order date
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors='coerce')

    # Split the order date out to two seperate columns
    df["Order Time"] = df["Order Date"].dt.time
    df["Order Date"] = df["Order Date"].dt.date

    # Split address out
    df[["Street", "City", "State Zip"]] = df["Purchase Address"].str.split(",", expand=True)
    df[["State", "Zip"]] = df["State Zip"].str.strip().str.split(" ", expand=True)

    return df

def output_to_file(df:pd.DataFrame) -> None:

    output_file = os.path.join(os.getcwd(), "Cleaned Data.parquet")

    df.to_parquet(output_file)

    output_file = os.path.join(os.getcwd(), "Cleaned Data - Sample.csv")

    df.head(20).to_csv(output_file, index=False)

    print(f"Output file created: {output_file}")

def main() -> None:

    source_archive = os.path.join(os.getcwd(), "archive.zip")

    df = create_dataframe(zip_file=source_archive)

    df = format_dataframe(df=df)

    output_to_file(df=df)

if __name__ == "__main__":
    main()