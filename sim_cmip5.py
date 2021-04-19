##########################
# Este programa extrae una serie de tiempo un archivo netcdf
# Para este ejemplo puedes utilizar los datos extraidos a través del ftp
# Estas simulaciones fueron realizadas a partir del Proyecto con el Ministerio de Medio Ambiente
# Para mayor información puedes revisar http://www.cr2.cl/simulaciones-regionales-regcm4/
# Cada credencial es diferente, al completar el formulario se enviará un usuario y contraseña para poder acceder.
# En este ejemplo trabajaremos con las simulaciones globales CMIP5.
###########################
import pandas as pd
import time
import netCDF4
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt


def lat_lon_variable_cmip5(filename,latitude,longitude):
	# Obtener la fecha de inicio, termino y variable a partir del nombre del archivo
	start=dt.datetime.strptime(filename.split('_')[-1].split('-')[0],('%Y%m'))
	stop=dt.datetime.strptime(filename.split('_')[-1].split('-')[1].replace('.nc',''),('%Y%m'))
	variable = filename.split('_')[0]
	# Abrir el archivo
	nc = netCDF4.Dataset(filename)
	lat = nc.variables['lat'][:]
	lon = nc.variables['lon'][:]
	time_var = nc.variables['time']
	dtime = netCDF4.num2date(time_var[:],time_var.units)

	# Determino el rango máximo de cobertura regional
	print(lon.min(),lon.max())

	# Especificar la latitud y longitud a encontrar
	lati = latitude; loni = longitude+360.0  # Georges Bank
	# Función para encontrar la cuadrícula dentro de la grilla.
	def near(array,value):
		idx=(abs(array-value)).argmin()
		return idx

	# Con esto encuentro el punto exacto para poder extraer la serie de tiempo
	ix = near(lon, loni)
	iy = near(lat, lati)


	istart = netCDF4.date2index(start,time_var,select='nearest')
	istop = netCDF4.date2index(stop,time_var,select='nearest')
	print(istart,istop)

	# Obtener los valore de la variable [vname]  indices [iy,ix]
	vname = variable
	var = nc.variables[vname]
	hs = var[istart:istop+1,iy,ix]
	tim = dtime[istart:istop+1]
	
	# Crear Pandas time series  una tabla con la información
	ts = pd.Series(hs,index=tim,name=vname+' ['+var.units+']')
	ts.index.name = 'Fecha'
	

	# Guardar la informacion
	ts.to_csv(f'{variable}_CMIP5_time_series_from_netcdf.csv')



lat_lon_variable_cmip5('tas_Amon_MPI-ESM-LR_historical_r1i1p1_185001-200512.nc',-25.07 , -71.98 )