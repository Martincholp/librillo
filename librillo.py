#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  librillo.py
#  
#  Copyright 2017 Martin Sebastian <martin@caro>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
# importamos el módulo para hacer llamadas a programas externos
import subprocess

def main(args):
	# "librillo.py" entrada.pdf 12 H salida.pdf
	# Desempaqueto los argumentos de entrada
	librillo, arch_entrada, numero, criterio, arch_salida = args
	
	# Obtenemos informacion del archivo
	salida = subprocess.Popen(['pdftk', arch_entrada, 'dump_data'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	err = salida.stderr.read()
	sal = salida.stdout.read()
	salida.stderr.close()
	salida.stdout.close()
	

	# Si hay errores aviso y salgo
	if err <> "":
		print "*************ERRORES************************"
		print "Ocurrieron errores al recopilar los datos"
		print err
		return 1
		
	#~ print "*************SALIDA**************************"
	#~ print sal
	
	# Obtengo el numero de paginas
	aux_ini = sal.find("NumberOfPages: ") + len("NumberOfPages: ")
	aux_fin = sal.find(chr(10),aux_ini,aux_ini + 10)
	num_paginas = int(sal[aux_ini:aux_fin])
	if num_paginas%4:
		num_paginas_impresas = (num_paginas/4) + 1
	else:
		num_paginas_impresas = (num_paginas/4) 
	
	print num_paginas
	print num_paginas_impresas
	
	# Verifico si el criterio de ordenamiento es por Hojas o por Librillos
	if criterio == "h" or criterio == "H":
		porHojas(int(numero), num_paginas)
	elif criterio == "l" or criterio == "L":
		porLibrillos(int(numero), num_paginas)
	else:
		print "*************ERRORES************************"
		print "Ocurrieron errores al recopilar los datos"
		print "El parametro ", criterio, " no es valido"
		return 1
		
def porHojas(hojas, paginas):
	# Cantidad de paginas de cada librillo
	pag_librillo = hojas * 4 # En cada hoja imprimo 4 paginas
	
	# Paginas para el ultimo librillo (si la cantidad de paginas totales no es multiplo de la cant de librillos)
	pag_ultimo = paginas % pag_librillo
	
	# Cantidad de librillos
	if pag_ultimo:
		num_librillos = (paginas/pag_librillo) + 1 
	else:
		num_librillos = (paginas/pag_librillo)
		
	#  Cantidad de hojas (sin doblar) del ultimo librillo
	
	if pag_ultimo%4:
		hojas_ultimo = (pag_ultimo / 4)+1
		print "Por hojas: habran ", num_librillos - 1, " librillos de ", hojas, " hojas y uno al ultimo de ", hojas_ultimo, " hojas."
	else:
		print "Por hojas: habran ", num_librillos, " librillos de ", hojas, " hojas."

			
	
def porLibrillos(librillos, paginas):
	# Cantidad de hojas sin doblar en total
	if paginas % 4:
		hojas = (paginas / 4) + 1
	else:
		paginas / 4
		
	# Cantidad de hojas de cada librillo
	hojas_ultimo = hojas % librillos # Si el total de hojas no fuera multiplo de la cant de librillos

	if hojas_ultimo:
		hojas_librillo = hojas / (librillos - 1)
		hojas_ultimo = hojas % (librillos - 1)
		print "Por librillos: habran ", librillos - 1, " librillos de ", hojas_librillo, " hojas y uno al ultimo de ", hojas_ultimo, " hojas."
 
	else:	
		hojas_librillo = hojas / librillos
		print "Por librillos: habran ", librillos, " librillos de ", hojas_librillo, " hojas."
		
		
	
	

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
