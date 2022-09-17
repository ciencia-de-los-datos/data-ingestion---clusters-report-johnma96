"""
Ingestión de datos - Reporte de clusteres
-----------------------------------------------------------------------------------------

Construya un dataframe de Pandas a partir del archivo 'clusters_report.txt', teniendo en
cuenta que los nombres de las columnas deben ser en minusculas, reemplazando los espacios
por guiones bajos; y que las palabras clave deben estar separadas por coma y con un solo 
espacio entre palabra y palabra.


"""
import pandas as pd
import re

def clean_line(pos, line):
    
    # Cleaning header
    if pos == 0: 
        line = [re.split(r'[ ]{2,}', element.strip()) 
                for element in line.split('\n')]
        line[1].insert(0,'')
        line[1].append('')
        line = [(a+' '+b).strip().lower() for a,b in zip(line[0],line[1])]
        line = [element.replace(' ', '_') for element in line]

    # Cleaning lines-cluster
    else:
        line = re.sub('[-]+\n', '', line)
        line = re.split(r'[ ]{4,}', line)
        line[3] = ' '.join(line[3:])
        line[3] = line[3].replace('\n', ' ')
        line[3] = re.sub('\s+',' ',line[3]).replace('.', '')
        line = line[0:4]
        line[2] =line[2].split(' ')[0]
        line = [l.strip() for l in line]

    return line


def ingest_data():
    with open("clusters_report.txt") as file:
        # Load data
        df = file.read()
        df = re.sub('\n\s+\n', '\n\n', df) # Check problem with line-cluster 9
        df = df.split('\n\n')[:-1]

        # Cleaning data
        df = [clean_line(pos, line) for pos, line in enumerate(df)]
        df = pd.DataFrame(df, columns=df[0]).drop(0)
        df.iloc[:,2] = df.iloc[:,2].str.replace(',','.')
        types = {
            'cluster':int,
            'cantidad_de_palabras_clave': int,
            'porcentaje_de_palabras_clave': float,
            'principales_palabras_clave':str
        }
        df = df.astype(types)

    return df
