import netCDF4 as nc
from netCDF4 import Dataset
import numpy as np

from copy_data_to_netcdf import extract_data_to_netcdf
import parameters

pkl_file = parameters.pkl_file
ncfile_path = parameters.ncfile_path

##---------------------------------------------------------------------------------------------------------------------------

# Creating a new Dataset
try: 
    ncfile.close()
except: 
    pass
ncfile = nc.Dataset('ncfile_path', mode = 'w', format = 'NETCDF4_CLASSIC')

##---------------------------------------------------------------------------------------------------------------------------

# Creating dimensions
time_dim = ncfile.createDimension('time', None)  
surface_el_adcp = ncfile.createDimension('surface_el_adcp', None)  # Surface elevation measurements from the ADCP sensor
pressure_adcp = ncfile.createDimension('press_adcp', None)  # Pressure conversion from the surface elevation using linear wave theory, ADCP sensor
pressure_ps = ncfile.createDimension('pressure_ps', None)  # Pressure measurements from the Pressure Sensor


##---------------------------------------------------------------------------------------------------------------------------

# Creating global attributes
ncfile.title='PS2201-campaign 2022-2023 Trapegeer / CB2.0'
ncfile.institution = 'VLIZ'
ncfile.source = 'ADCP model: Signature1000 Nortek, Pressure sensor model: RBR, buoy model: '
ncfile.comment = 'instrument frequency 4Hz'

##---------------------------------------------------------------------------------------------------------------------------

# Creating variables 
time_adcp = ncfile.createVariable('time_adcp', np.float64, ('time_adcp',), zlib=True)
surface_el_adcp = ncfile.createVariable('surface_el_adcp', np.float32, ('surface_el_adcp'), zlib=True)
pressure_adcp = ncfile.createVariable('pressure_adcp', np.float32, ('pressure_adcp',), zlib=True)

time_ps = ncfile.createVariable('time_ps', np.float64, ('time_ps',), zlib=True)
pressure_ps = ncfile.createVariable('pressure_ps', np.float32, ('pressure_ps',), zlib=True)

time_buoy = ncfile.createVariable('time_buoy', np.float64, ('time_buoy',), zlib=True)

##---------------------------------------------------------------------------------------------------------------------------

# Defining units
time_adcp.units = time_ps.units = '%Y%m%d %H:%M%S.%f'
pressure_ps.units = 'dBar'
pressure_adcp.units = 'dBar'
surface_el_adcp.units = 'm'

##---------------------------------------------------------------------------------------------------------------------------

# Defining attributes for variables
time_adcp.source = '%Y%m%d %H:%M:%S.%f date format'
surface_el_adcp.source = 'surface elevation measured by the AST component of the ADCP'
pressure_adcp.source = 'pressure measured at the same time as surface elevation by a pressure sensor in the ADCP'

time_ps.source = '%Y%m%d %H:%M:%S.%f date format'

time_buoy.source = ''

##---------------------------------------------------------------------------------------------------------------------------

# Writing data
# Select data
extract_data_to_netcdf(pkl_file, ncfile_path)


##---------------------------------------------------------------------------------------------------------------------------

# Closing a netCDF file
print(ncfile) # print the Dataset object to see what we've got
ncfile.close(); print('Dataset is closed!') # close the Dataset