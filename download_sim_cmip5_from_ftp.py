##########################
# Este programa se puede utilizar para descargar simulaciones a través del FTP
# Debes solicitar acceso a través de www.cr2.cl
# Existen tres accesos principalmente disponibles
#  - Simulaciones Globales http://www.cr2.cl/simulaciones-globales
#  - Simulaciones Regionales http://www.cr2.cl/simulaciones-regionales
#  - Simulaciones proyecto Ministerio del Medio Ambiente http://www.cr2.cl/simulaciones-regionales-regcm4/
# Cada credencial es diferente, al completar el formulario se enviará un usuario y contraseña para poder acceder.
# En este ejemplo trabajaremos con las simulaciones regionales para Chile RegCM4.
###########################
from ftplib import FTP
from datetime import date

today = date.today()
d3 = today.strftime("%Y%m%d")

ftp=FTP()
#Ingresa el usuario y password de acceso.
user     = ''
password =''
#En este paso se ingresa el usuario y la contraseña de acceso al ftp
ftp.connect('ftp.cr2.cl', 21)
ftp.login(user,password)
#Este comando muestra todas las carpetas que contienen archivos.
ftp.retrlines('LIST')

#Vamos a generalizar la búsqueda normalmente todos los directorios 
#presentan el siguiente orden, escenario, frecuencia, variable, modelo1 y modelo2 para el caso de simulaciones
#regionales, para el caso de simulaciones globales solo se utiliza un modelo.

escenario='historical'
frecuencia='Amon'
variable='tas'
modelo='MPI-ESM-LR'
ensamble='r1i1p1'

# Tratamos de entrar a la carpeta utilizando el comando ftp.cwd()
# En el caso que genere un error, prueba corroborando que existe la carpeta utilizando ftp.retrlines('LIST')
try:
	ftp.cwd(f'Global/CMIP5/{escenario}/{frecuencia}/{variable}/{modelo}/{ensamble}/')
	#ftp.cwd(f'Global/CMIP5/historical')
	ftp.retrlines('LIST')
	file_list=[]
	#Guardaremos todos los archivos en una lista para poder descargarlos
	ftp.retrlines('LIST', lambda x: file_list.append(x.split()))
	for n in range(2,len(file_list)):
	 	print(f'Downloading {file_list[n][-1]}...')
	 	ftp.retrbinary("RETR " + file_list[n][-1] ,open(file_list[n][-1], 'wb').write)
	print(f'**********{d3}***********')
except:
 	print("Error")

ftp.quit()

#Para poder utilizar este código para otras simulaciones ten en consideración que deberas buscar la ruta
#donde se encuentran los archivos. Este será el camino mas difícil, ya encontrando la lista de archivos
#en formato *.nc netCDF la descarga se genera automáticamente ya que el nombre de los archivos también
#siguen un patrón.
#Para cualquier consulta puedes escribirnos a cr2sysadmin@dgf.uchile.cl
#Recuerda que también puedes descargar los archivos usando un software como Filezilla.