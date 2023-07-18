import pandas as pd
import netCDF4 as nc
from datetime import datetime

def extract_data_to_netcdf(pkl_file, ncfile_path):
    # Load data from the pickle file
    data = pd.read_pickle(pkl_file)

    # Ask the user which columns to copy (excluding the 'time' column)
    available_columns = [col for col in data.columns if col != 'time']
    print("Available columns:")
    for col in available_columns:
        print(col)

    selected_columns = input("Enter column names to copy (separated by commas): ").split(",")

    # Open the existing NetCDF file in append mode
    ncfile = nc.Dataset(ncfile_path, mode='a')

    # Create or update the 'time' variable in the NetCDF file
    if 'time' not in ncfile.variables:
        ncfile.createDimension('time', None)
        time_var = ncfile.createVariable('time', 'str', ('time',))
        time_var.units = 'formatted string: %Y%m%d %H:%M:%S.%f'
    else:
        time_var = ncfile.variables['time']

    # Convert the pandas datetime to formatted strings in the desired format
    time_values = data.index.strftime('%Y%m%d %H:%M:%S.%f')

    # Write the data to the NetCDF 'time' variable
    time_var[:] = time_values

    # Loop through the selected columns and copy the data to NetCDF variables
    for col_name in selected_columns:
        # Check if the column exists in the DataFrame and is not 'time'
        if col_name in available_columns:
            # Create a new NetCDF variable with the same name as the column
            ncfile.createVariable(col_name, data[col_name].dtype.str, ('time',), fill_value=None)
            # Write the data to the NetCDF variable
            ncfile.variables[col_name][:] = data[col_name].values
            print(f"Column '{col_name}' copied to NetCDF variable successfully.")
        else:
            print(f"Column '{col_name}' does not exist in the DataFrame or is 'time'. Skipping...")

    # Close the NetCDF file
    ncfile.close()


