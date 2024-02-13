from lxml import etree

# Parsear el archivo XML
doc = etree.parse(r"C:\Users\franciscojavier.mart\Documents\programas_scripts\parsear\Asrun Marina\LA1-XML File_2024-02-07_00-00-00 - prueba.marl")

# Consulta para encontrar eventos con hijos
events_with_children = doc.xpath("//event[childEvents]")
events = doc.xpath("//event")

#for event in events:
#    # Verificar si el evento tiene el atributo "reconcileKey"
#    reconcile_key = event.xpath("./properties/event/@reconcileKey")
#    if reconcile_key:
#        print(f"Evento - reconcileKey: {reconcile_key[0]}")
#    else:
#        enabled = event.get("enabled")
#        uid = event.get("uid")
#        print(f"Evento - enabled: {enabled}, uid: {uid}")




# Verificar si hay eventos con hijos
#if events_with_children:
#    print("Se encontraron eventos con hijos.")
#    for event in events_with_children:
#        event_id = event.get("uid")
#        print(f"Evento con ID {event_id} tiene hijos.")
#else:
#    print("No se encontraron eventos con hijos.")
