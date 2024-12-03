fichero = open(r"C:\Users\franciscojavier.mart\Desktop\Asrun Marina\D1231002.rgt")

primera_linea = fichero.readline()

contador=0
for linea in fichero:
    contador = contador + 1

    print()
    print("**********Linea ", contador, "**********")

    A_HORA = linea[0:11]
    B_ID = linea[13:31]
    C_SEGMENTO = linea[33:35]
    D_TITULO = linea[37:69]
    E_DURACION = linea[71:82]
    F_TIPO_DE_PROGRAMA = linea[84:85]
    G_RELACION_DE_ASPECTO = linea[86:87]
    H_CONTRATO_PUBLI = linea[88:94]
    I_PASE_PUBLI = linea[96:99]
    J_LOCALIZADOR_PUBLICIDAD = linea[101:106]
    K_CODIGO_DE_BLOQUE_PUBLI = linea[108:119]
    L_POSICION_SPOT_EN_BLOQUE = linea[121:123]
    M_TITULO_DE_BLOQUE = linea[125:139]
    N_LOGO_1 = linea[141:143]
    O_LOGO_2 = linea[144:146]
    P_CALIFICACION_MORAL = linea[146:147]
    Q_ALERTAS = linea[147:148]
    R_SUBTITULADO = linea[148:149]
    S_AUDIO = linea[149:152]
    T_LIBRE = linea[152:153]
    U_INSERCIONES = linea[153:157]
    V_SERVIDOR_DE_DIRECTOR = linea[157:158]
    W_DIRECTOR = linea[158:159]
    ESPECIAL = linea[159:161]
    X_HORA_ANUNCIADA = linea[162:170]
    Y_DISTINTIVO_PG = linea[171:172]

    # Definición de las variables
    variables = {
        "A_HORA": linea[0:11],
        "B_ID": linea[13:31],
        "C_SEGMENTO": linea[33:35],
        "D_TITULO": linea[37:69],
        "E_DURACION": linea[71:82],
        "F_TIPO_DE_PROGRAMA": linea[84:85],
        "G_RELACION_DE_ASPECTO": linea[86:87],
        "H_CONTRATO_PUBLI": linea[88:94],
        "I_PASE_PUBLI": linea[96:99],
        "J_LOCALIZADOR_PUBLICIDAD": linea[101:106],
        "K_CODIGO_DE_BLOQUE_PUBLI": linea[108:119],
        "L_POSICION_SPOT_EN_BLOQUE": linea[121:123],
        "M_TITULO_DE_BLOQUE": linea[125:139],
        "N_LOGO_1": linea[141:143],
        "O_LOGO_2": linea[144:146],
        "P_CALIFICACION_MORAL": linea[146:147],
        "Q_ALERTAS": linea[147:148],
        "R_SUBTITULADO": linea[148:149],
        "S_AUDIO": linea[149:152],
        "T_LIBRE": linea[152:153],
        "U_INSERCIONES": linea[153:157],
        "V_SERVIDOR_DE_DIRECTOR": linea[157:158],
        "W_DIRECTOR": linea[158:159],
        "ESPECIAL": linea[159:161],
        "X_HORA_ANUNCIADA": linea[162:170],
        "Y_DISTINTIVO_PG": linea[171:172]
    }

    # Imprimir las variables en vertical
    for variable, valor in variables.items():
        print(f"{variable}: {valor}")

fichero.close()

