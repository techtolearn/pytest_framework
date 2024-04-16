import itertools
import os
import pandas as pd

import xlrd


class Excel_Parser:

    def read_from_excel(self, sheet_name, excel_path):
        rows_val = []
        # read from file
        work_book = xlrd.open_workbook(self, excel_path)
        sheet = work_book.sheet_by_name(sheet_name)

        # get all values, iterating through rows and columns
        num_cols = sheet.ncols  # Number of columns
        for row_idx, col_idx in itertools.product(
                range(1, sheet.nrows), range(num_cols)
        ):
            cell_obj = sheet.cell(row_idx, col_idx)  # Get cell object by row, col
            # Convert cell to string,split it according to "'" and take the second cell in the array created
            # e.g.: cell_obj == "text:'something'" --> after convert and splitting == "something"
            rows_val.append(str(cell_obj).split("'")[1])
        return rows_val

    @staticmethod
    def get_csv_data(df, selected_columns, selected_values, retrieve_columns):
        # Filter the dataFrame based on Selected columns and values
        filtered_df = df[
            (df[selected_columns[0]] == selected_values[0]) & (df[selected_columns[1]] == selected_values[1])]
        filter_df = filtered_df.sort_values(by='column_name', ascending=True)
        column1 = []
        column2 = []
        column3 = []
        for index, row in filtered_df.iterrows():
            column1.append(row[retrieve_columns[0]])
            column2.append(row[retrieve_columns[1]])
            column3.append(row[retrieve_columns[2]])

        return {"col1": column1, "col2": column2, "col3": column3}
