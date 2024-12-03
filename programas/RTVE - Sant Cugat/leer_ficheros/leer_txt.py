fichero = open(r"C:\Users\franciscojavier.mart\Desktop\parsear\Asrun Marina\LA1-Marina Text 20240207_000000 Marina.txt")

for _ in range(8):
    next(fichero)

contador=0

for linea in fichero:
    contador=contador+1
    if linea[1:2] == "S" or linea[1:2] == "P":
        # Formato fichero

        print()
        print("**********Linea ", contador, "**********")
        
    
        TYPE = linea[1:6]
        START_TIME = linea[6:29]
        END_TIME = linea[29:52]
        MEDIA_ID = linea[52:85]
        EVENT = linea[85:106]
        TITLE = linea[106:139]
        SOM = linea[139:151]
        SEGMENT = linea[151:184]
        DURATION = linea[184:196]
        START_TYPE = linea[196:209]
        STRT_OFFSET = linea[209:221]
        END_TYPE = linea[221:234]
        END_OFFSET = linea[234:246]
        DEVICE_STREAM = linea[246:279]
        RECONCILE_KEY = linea[279:312]
 
        # Iteramos sobre cada carácter en la cadena
        for caracter in RECONCILE_KEY:
            # Ignoramos los espacios en blanco
            if caracter == " ":
            # Incrementamos el recuento para el carácter actual
                RECONCILE_KEY = " " * 27
                print("NO ES VALIDO")
        
        HOUSE_ID = linea[312:345]
        STATUS = linea[345:371]

        variables = {
        "TYPE": linea[1:6],
        "START_TIME": linea[6:29],
        "END_TIME": linea[29:52],
        "MEDIA_ID": linea[52:85],
        "EVENT": linea[85:106],
        "TITLE": linea[106:139],
        "SOM": linea[139:151],
        "SEGMENT": linea[151:184],
        "DURATION": linea[184:196],
        "START_TYPE": linea[196:209],
        "STRT_OFFSET": linea[209:221],
        "END_TYPE": linea[221:234],
        "END_OFFSET": linea[234:246],
        "DEVICE_STREAM": linea[246:279],
        "RECONCILE_KEY": RECONCILE_KEY,
        "HOUSE_ID": linea[312:345],
        "STATUS": linea[345:371]
        }

        # Imprimir las variables en vertical
        for variable, valor in variables.items():
            print(f"{variable}: {valor}")

