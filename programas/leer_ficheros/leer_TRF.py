fichero = open(r"C:\Users\franciscojavier.mart\Documents\parseo\trf programa\S5231004_10031723.TRF")

primera_linea = fichero.readline()

eventos = {}

cabecera = """<?xml version="1.0" encoding="UTF-8"?>
<marinaPlaylist version="3.1">
<properties>
<history>
</history>
</properties>
<eventList>
</eventList>
</marinaPlaylist>
"""

print(cabecera)

contador=0
for linea in fichero:
    if linea[0:1] == '1':
        #print("**********Tipo 1**********")
        contador = contador + 1

        print()
        #print("**********Linea ", contador, "**********")

        # Referencia Tipo 1

        TIPOREG = linea[0:1]
        INDMULTI = linea[1:3]
        TICODELEMENMIN = linea[3:18]
        TITIPELEME = linea[18:19]
        TIHOINMIN = linea[19:30] # HORA DE INICIO
        TIDUMINUT = linea[30:41]
        TITITELEME = linea[41:107]
        LENGUAJE_DE_SIGNOS = linea[107:108]
        AUDIODESCRIPCION = linea[108:109]
        RELACION_DE_ASPECTO = linea[110:111]
        TIPO_DE_AUDIO  = linea[111:114]
        CALIFMORAL = linea[114:118]
        INDELEMFIJO = linea[118:119]
        CONTRATO = linea[119:126]
        PASE = linea[126:129]
        CODLOCALI = linea[129:132]
        NO_PA = linea[132:134]
        DIRGRAB = linea[134:135]
        SUBTITULADO = linea[135:136]
        INDLOGO = linea[136:137]
        NUMERO_DE_LOGO = linea[137:139]
        DISTINTIVO_DE_CALIFMORAL = linea[140:141]

        # Definición de las variables
        variables = {
        "TIPOREG": linea[0:1],
        "INDMULTI": linea[1:3],
        "TICODELEMENMIN": linea[3:18],
        "TITIPELEME": linea[18:19],
        "TIHOINMIN": linea[19:30],
        "TIDUMINUT": linea[30:41],
        "TITITELEME": linea[41:107],
        "LENGUAJE_DE_SIGNOS": linea[107:108],
        "AUDIODESCRIPCION": linea[108:109],
        "RELACION_DE_ASPECTO": linea[110:111],
        "TIPO_DE_AUDIO": linea[111:114],
        "CALIFMORAL": linea[114:118],
        "INDELEMFIJO": linea[118:119],
        "CONTRATO": linea[119:126],
        "PASE": linea[126:129],
        "CODLOCALI": linea[129:132],
        "NO_PA": linea[132:134],
        "DIRGRAB": linea[134:135],
        "SUBTITULADO": linea[135:136],
        "INDLOGO": linea[136:137],
        "NUMERO_DE_LOGO": linea[137:139],
        "DISTINTIVO_DE_CALIFMORAL": linea[140:141],
        }

        # Linea donde vamos a gener la reconcilekey

        if CALIFMORAL == "    ":
            CLASIFICACION = "0"
        elif CALIFMORAL == "ERI ":
            CLASIFICACION = "1"
        elif CALIFMORAL == "NR12":
            CLASIFICACION = "2"
        elif CALIFMORAL == "NR13":
            CLASIFICACION = "3"
        elif CALIFMORAL == "NR16":
            CLASIFICACION = "4"
        elif CALIFMORAL == "NR18":
            CLASIFICACION = "5"
        elif CALIFMORAL == "NR7 ":
            CLASIFICACION = "6"
        elif CALIFMORAL == "PT  ":
            CLASIFICACION = "7"
        elif CALIFMORAL == "SC  ":
            CLASIFICACION = "8"
        elif CALIFMORAL == "X   ":
            CLASIFICACION = "9"
        
        if SUBTITULADO == " " and AUDIODESCRIPCION == " " and LENGUAJE_DE_SIGNOS == " ":
            TXTAUD = "0"
        elif SUBTITULADO == "S" and AUDIODESCRIPCION == " " and LENGUAJE_DE_SIGNOS == " ":
            TXTAUD = "1"
        elif SUBTITULADO == " " and AUDIODESCRIPCION != " " and LENGUAJE_DE_SIGNOS == " ":
            TXTAUD = "2"
        elif SUBTITULADO == " " and AUDIODESCRIPCION == " " and LENGUAJE_DE_SIGNOS != " ":
            TXTAUD = "3"
        elif SUBTITULADO == "S" and AUDIODESCRIPCION != " " and LENGUAJE_DE_SIGNOS == " ":
            TXTAUD = "4"
        elif SUBTITULADO == " " and AUDIODESCRIPCION != " " and LENGUAJE_DE_SIGNOS != " ":
            TXTAUD = "5"
        elif SUBTITULADO == "S" and AUDIODESCRIPCION != " " and LENGUAJE_DE_SIGNOS != " ":
            TXTAUD = "6"
        elif SUBTITULADO == "I" and AUDIODESCRIPCION == " " and LENGUAJE_DE_SIGNOS == " ":
            TXTAUD = "7"
        elif SUBTITULADO == "I" and AUDIODESCRIPCION != " " and LENGUAJE_DE_SIGNOS == " ":
            TXTAUD = "8"
        elif SUBTITULADO == "I" and AUDIODESCRIPCION == " " and LENGUAJE_DE_SIGNOS != " ":
            TXTAUD = "9"
        elif SUBTITULADO == "I" and AUDIODESCRIPCION != " " and LENGUAJE_DE_SIGNOS != " ":
            TXTAUD = "A"


        #print(CLASIFICACION+RELACION_DE_ASPECTO+TXTAUD+TITIPELEME+CONTRATO+PASE+TICODELEMENMIN+TICODELEMENMIN[11:]+"_"+TIHOINMIN[:8])
        RECONCILEKEY = CLASIFICACION+RELACION_DE_ASPECTO+TXTAUD+TITIPELEME+CONTRATO+PASE+TICODELEMENMIN[:11]+TICODELEMENMIN[11:13]+"_"+TIHOINMIN[:8]
        #print(RECONCILEKEY.replace(" ", "*")) 
        
        eventos[contador] = [TIPOREG]

        # Imprimir las variables en vertical
        #for variable, valor in variables.items():
        #    print(f"{variable}: {valor}")

        #print(TIPOREG,INDMULTI,TICODELEMENMIN,TITIPELEME,TIHOINMIN,TIDUMINUT,TITITELEME,LENGUAJE_DE_SIGNOS,AUDIODESCRIPCION,RELACION_DE_ASPECTO,TIPO_DE_AUDIO,CALIFMORAL,INDELEMFIJO,CONTRATO,PASE,CODLOCALI,NO_PA,DIRGRAB,SUBTITULADO,INDLOGO,NUMERO_DE_LOGO,DISTINTIVO_DE_CALIFMORAL)




    elif linea[0:1] == '2':
        #print("Tipo 2")

        print()
        #print("**********Linea ", contador, "**********")

        # Referencia de Tipo 2

        TIPOREG = linea[0:1]
        TIPOCINTA = linea[1:2]
        CODCINTA = linea[2:12]
        HORINIEMI = linea[12:23]
        HORFINEMI = linea[23:34]
        NUMSEGMENTO = linea[34:35]
        ULTIMO = linea[35:36]
        Literal1 = linea[37:39]
        HORA_ANUNCIADA = linea[40:48]
        Literal2 = linea[50:52]
        NOCOMPUTA = linea[53:]

        # Definición de las variables
        variables = {
       "TIPOREG": linea[0:1],
       "TIPOCINTA": linea[1:2],
       "CODCINTA": linea[2:12],
       "HORINIEMI": linea[12:23],
       "HORFINEMI": linea[23:34],
       "NUMSEGMENTO": linea[34:35],
       "ULTIMO": linea[35:36],
       "Literal1": linea[37:39],
       "HORA_ANUNCIADA": linea[40:48],
       "Literal2": linea[50:52],
       "NOCOMPUTA": linea[53:]
        }

        # Imprimir las variables en vertical
        #for variable, valor in variables.items():
        #    print(f"{variable}: {valor}")

        #print(TIPOREG,TIPOCINTA,CODCINTA,HORINIEMI,HORFINEMI,NUMSEGMENTO,ULTIMO,Literal1,HORA_ANUNCIADA,Literal2,NOCOMPUTA)
        eventos[contador].append(TIPOREG)

    elif linea[0:1] == '3':
        #print("Tipo 3")

        print()
        #print("**********Linea ", contador, "**********")

        # Referencia de Tipo 3

        TIPOREG = linea[0:1]
        TIPO_DE_INSERCION = linea[1:2]
        NUMERO_DE_LA_INCRUSTACION = linea[3:7]
        HORA_DE_COMIENZO = linea[8:19]
        DURACION = linea[20:31]

        # Definición de las variables
        variables = {
        "TIPOREG": linea[0:1],
        "TIPO_DE_INSERCION": linea[1:2],
        "NUMERO_DE_LA_INCRUSTACION": linea[3:7],
        "HORA_DE_COMIENZO": linea[8:19],
        "DURACION": linea[20:31]
        }

        # Imprimir las variables en vertical
        #for variable, valor in variables.items():
        #    print(f"{variable}: {valor}")

        #print(TIPOREG,TIPO_DE_INSERCION,NUMERO_DE_LA_INCRUSTACION,HORA_DE_COMIENZO,DURACION)

        eventos[contador].append(TIPOREG)

    elif linea[0:1] == '4':
        #print("Tipo 4")
        contador = contador + 1

        print()
        #print("**********Linea ", contador, "**********")

        # Referencia de Tipo 4

        TIPOREG = linea[0:1]
        IDBLOQUE = linea[1:40]

        # Definición de las variables
        variables = {
        "TIPOREG": linea[0:1],
        "IDBLOQUE": linea[1:40]
        }

        # Imprimir las variables en vertical
        #for variable, valor in variables.items():
        #    print(f"{variable}: {valor}")

        #print(TIPOREG,IDBLOQUE)

        eventos[contador] = [TIPOREG]

    elif linea[0:1] == '5':
        #print("Tipo 5")
        contador = contador + 1

        print()
        #print("**********Linea ", contador, "**********")
        

        # Referencia de Tipo 5

        TIPOREG = linea[0:1]
        ESPACIO = linea[1:2]
        OBSERVACIONES = linea[2:34]

        # Definición de las variables
        variables = {
        "TIPOREG": linea[0:1],
        "ESPACIO": linea[1:2],
        "OBSERVACIONES": linea[2:34]
        }

        # Imprimir las variables en vertical
        #for variable, valor in variables.items():
        #    print(f"{variable}: {valor}")

        #print(TIPOREG,ESPACIO,OBSERVACIONES)

        eventos[contador] = [TIPOREG]


fichero.close()

print(eventos)