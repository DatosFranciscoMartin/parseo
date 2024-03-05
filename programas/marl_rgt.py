import xml.etree.ElementTree as ET

# Nombre del archivo XML
xml_file = r'C:\Scripts\RTVE\EJEMPLOS\CS1 AsRun_2024-02-22_07-00-00.marl'

# Parsear el XML desde el archivo
tree = ET.parse(xml_file)
root = tree.getroot()
# Convertir el árbol XML a una cadena de texto
xml_str = ET.tostring(root, encoding='unicode', method='xml')

# Mostrar por pantalla el XML leído

# Recorrer los eventos dentro de eventlist excluyendo los eventos dentro de properties y childEvents
#'.//event[not(parent::properties) and not(parent::childEvents)]' [parent::eventList]
for event in root.findall('.//eventList/event'):

    A = event.find('.//asRun').get('endTime').split('T')[1]
    B = event.find('.//properties/event').get('houseId')
    #C = DEFAULT[:2]
    D = event.find('.//properties/event').get('title')
    E = event.find('.//asRun').get('duration')
    F = event.find('.//properties/event').get('reconcileKey')[3:4]
    G = event.find('.//properties/event').get('reconcileKey')[1:2]
    if G == " " or G == "0":
        G = "2"
    H = event.find('.//properties/event').get('reconcileKey')[4:11]
    I = event.find('.//properties/event').get('reconcileKey')[11:14]
    #J = DEFAULT[:5]
    K = event.find('.//properties/event').get('reconcileKey')[14:25]
    L = event.find('.//properties/event').get('reconcileKey')[25:27]
    #M = DEFAULT[:14]
    #N = DEFAULT[:2]
    #O = DEFAULT[:2]
    P = event.find('.//properties/event').get('reconcileKey')[0:1]
    if P == " " or P == "0":
        P = "7"
    #Q = DEFAULT[:1]
    R = event.find('.//properties/event').get('reconcileKey')[2:3]
    #S = DEFAULT[:3]
    #if S == "   ":
    #    S = "EST"
    #T = DEFAULT[:1]
    #U = DEFAULT[:4]
    #V = DEFAULT[:1]
    #W = DEFAULT[:1]
    #ESPECIAL = DEFAULT[:2]
    X = event.find('.//properties/event').get('reconcileKey')[28:]
    # Aquí puedes realizar cualquier operación necesaria con cada evento
    print(A)
    print(B)
    #print(C)
    print(D)
    print(E)
    print(F)
    print(G)
    print(H)
    print(I)
    #print(J)
    print(K)
    print(L)
    #print(M)
    #print(N)
    #print(O)
    print(P)
    #print(Q)
    print(R)
    #print(S)
    #print(T)
    #print(U)
    #print(V)
    #print(W)
    print(X)
    #print(Y)
    #print(Z)


    print ("---------------------------------------------------")
