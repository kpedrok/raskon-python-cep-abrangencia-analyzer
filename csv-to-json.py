import csv
import json

csvfile = open('input-abrangencia.csv', 'r', encoding='cp860')
jsonfile = open('file.json', 'w')

fieldnames = ("Transportadora","Metodo de Envio","UF","Cidade", 'CEP Inicial', 'CEP Final', 'Tarifa', 'Prazo de Entrega')
reader = csv.DictReader( csvfile, fieldnames,  delimiter=';')
for row in reader:
    print (row)
    json.dump(row, jsonfile, ensure_ascii=False)
    jsonfile.write('\n')


