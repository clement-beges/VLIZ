import netCDF4 as nc
from netCDF4 import Dataset
import numpy as np

from copy_data_to_netcdf import copy_data_to_netcdf_adcp, copy_data_to_netcdf_ps
import parameters

pkl_file_adcp = parameters.pkl_file_adcp
pkl_file_ps = parameters.pkl_file_ps
ncfile_path = parameters.ncfile_path

##---------------------------------------------------------------------------------------------------------------------------

# Creating a new Dataset
try: ncfile.close()
except: pass
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
time_adcp = ncfile.createVariable('time_adcp', np.float64, ('time_adcp',))
surface_el_adcp = ncfile.createVariable('surface_el_adcp', np.float32, ('surface_el_adcp'))
pressure_adcp = ncfile.createVariable('pressure_adcp', np.float32, ('pressure_adcp',))

time_ps = ncfile.createVariable('time_ps', np.float64, ('time_ps',))
pressure_ps = ncfile.createVariable('pressure_ps', np.float32, ('pressure_ps',))

time_buoy = ncfile.createVariable('time_buoy', np.float64, ('time_buoy',))

##---------------------------------------------------------------------------------------------------------------------------

# Defining units
time_adcp.units = time_ps.units = '%Y%m%d %H:%M%S.%f'
pressure_ps.units = 'dBar'
pressure_adcp.units = 'dBar'
surface_el_adcp.units = 'm'

##---------------------------------------------------------------------------------------------------------------------------

# Writing data
copy_data_to_netcdf_adcp(pkl_file_adcp, ncfile_path)
copy_data_to_netcdf_ps(pkl_file_ps, ncfile_path)

# Organise the data in the netcdf : Separation between ADCP / Pressure Sensor / buoy 
adcp = ncfile.createVariable('adcp', np.float64, ('time_adcp', 'surface_el_adcp', 'pressure_adcp'), zlib=True)  # 3D variable for the ADCP data 
ps = ncfile.createVariable('ps', np.float64, ('time_ps', 'pressure_ps'), zlib=True) # 2D variable for the Pressure Sensor data
buoy = ncfile.createvariable('buoy', np.float64, ('time_buoy', '')) # variable for the buoy data


adcp.source = 'Signature1000 Nortek, frequency 4Hz'
ps.source = 'RBR'
buoy.source = ''

##---------------------------------------------------------------------------------------------------------------------------

# Closing a netCDF file
print(ncfile) # print the Dataset object to see what we've got
ncfile.close(); print('Dataset is closed!') # close the Dataset