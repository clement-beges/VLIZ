import pandas as pd
import netCDF4 as nc
from datetime import datetime

def copy_data_to_netcdf_ps(pkl_file_ps, ncfile_path):
    # Load data from the pickle file
    data = pd.read_pickle(pkl_file_ps)

    # Extract the columns 'Time', 'Pressure', and 'Depth'
    time_data = data['Time'].values
    pressure_data = data['Pressure'].values

    # Open the existing NetCDF file in append mode
    ncfile = nc.Dataset(ncfile_path, mode='a')

    # Convert time_data to the desired format
    formatted_time_data = [datetime.strftime(dt, '%Y%m%d %H:%M:%S.%f') for dt in time_data]

    # Assign values to the existing 'time_ps' and 'pressure_ps' variables
    ncfile['time_ps'][:] = formatted_time_data
    ncfile['pressure_ps'][:] = pressure_data

    # Close the NetCDF file
    ncfile.close()


def copy_data_to_netcdf_adcp(pkl_file_adcp, ncfile_path):
    # Load data from the pickle file
    data = pd.read_pickle(pkl_file_adcp)

    # Extract the columns 'Time', 'Pressure', and 'Depth'
    time_data = data['Time'].values
    pressure_data = data['Pressure'].values
    depth_data = data['Depth'].values

    # Open the existing NetCDF file in append mode
    ncfile = nc.Dataset(ncfile_path, mode='a')
    
    # Convert time_data to the desired format
    formatted_time_data = [datetime.strftime(dt, '%Y%m%d %H:%M:%S.%f') for dt in time_data]

    # Assign values to the existing variables
    ncfile['time_adcp'][:] = formatted_time_data
    ncfile['pressure_adcp'][:] = pressure_data
    ncfile['surface_el_adcp'][:] = depth_data

    # Close the NetCDF file
    ncfile.close()

