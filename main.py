from animal import Animal
from sistema_monitoreo import SistemaMonitoreo


def imprimir_alertas(alertas):
    for a in alertas:
        print(f"{a.codigo} | {a.prioridad.upper():5} | {a.hora} | {a.tipo}")


def main():
    s = SistemaMonitoreo()
    hora = "2026-10-11 18:30"
    print("=== GUARDIANES DEL PETÉN - ENTREGA 4 ===")
    for nombre, tipo in [("Laguna del Tigre", "núcleo"), ("Mirador-Río Azul", "núcleo"),
                         ("El Remate", "amortiguamiento"), ("Uaxactún", "uso múltiple")]:
        s.registrar_zona(nombre, tipo)
    s.registrar_guardarrecursos("GR-07", "Mateo Chayax")
    s.registrar_guardarrecursos("GR-08", "Lucía Pérez")
    s.establecer_turno("GR-07")
    for codigo, bateria in [("GPS-01", 80), ("GPS-02", 5), ("GPS-03", 65)]:
        s.registrar_collar(codigo, bateria)

    print("\nA. REGISTRAR ANIMALES (ENTREGAS 1 Y 2)")
    for datos in [("JAG-001", "Balam", "jaguar", True),
                  ("TAP-001", "Tziquin", "tapir", True),
                  ("GUA-001", "Ixchel", "guacamaya roja", True),
                  ("COC-001", "Chak", "cocodrilo de pantano", False),
                  ("MON-001", "Kuk", "mono aullador", False)]:
        s.registrar_animal(*datos)
    s.registrar_animal("jag001", "Otro", "jaguar", True)
    s.registrar_animal("JAG-001", "Repetido", "jaguar", True)
    s.registrar_animal("TAP-002", "Otro", "tapir", False)

    print("\nB. ASIGNAR COLLARES")
    s.asignar_collar("GPS-01", "JAG-001")
    s.asignar_collar("GPS-02", "TAP-001")
    s.asignar_collar("NO-EXISTE", "JAG-001")
    s.asignar_collar("GPS-01", "GUA-001")
    s.asignar_collar("GPS-03", "JAG-001")
    s.asignar_collar("GPS-03", "GUA-001")

    print("\nC. REPORTAR POSICIÓN")
    s.reportar_posicion("GPS-01", "Laguna del Tigre", hora)
    s.reportar_posicion("GPS-01", "Uaxactún", hora)  # Alerta AL-001, alta
    s.reportar_posicion("GPS-02", "El Remate", hora)  # Alerta AL-002, media
    s.reportar_posicion("GPS-03", "Zona desconocida", hora)
    s.reportar_posicion("NO-EXISTE", "Uaxactún", hora)
    s.reportar_posicion("GPS-03", "El Remate", "2026-02-30 25:00")

    print("\nD. REGISTRAR AVISTAMIENTOS")
    s.registrar_avistamiento("GR-07", "COC-001", "El Remate", hora)
    s.registrar_avistamiento("GR-08", "MON-001", "Uaxactún", hora)
    s.registrar_avistamiento("gr7", "COC-001", "El Remate", hora)
    s.registrar_avistamiento("GR-07", "COC-999", "El Remate", hora)

    print("\nE. ATENDER ALERTAS")
    s.atender_alerta("AL-001", "GR-07", "2026-10-11 19:00")
    s.atender_alerta("AL-001", "GR-08", "2026-10-11 19:10")
    s.atender_alerta("AL-999", "GR-07", hora)

    print("\nF. CAMBIAR BATERÍA Y CONSULTAR MOVIMIENTOS")
    s.cambiar_bateria("GPS-02", "GR-07", 100, "2026-10-11 19:30")
    s.cambiar_bateria("GPS-02", "GR-07", 101, hora)
    s.cambiar_bateria("GPS-02", "GR7", 80, hora)
    s.reportar_posicion("GPS-02", "El Remate", "2026-10-11 19:35")
    s.consultar_movimientos("JAG-001")
    s.consultar_movimientos("GUA-001")
    s.consultar_movimientos("JAG-999")

    print("\nG. HERENCIA Y POLIMORFISMO DE ENTREGA 3")
    for animal in s.animales:
        print("Heredado:", animal.consultar_collar())
        print("Sobrescrito:", animal.mostrar_datos())
        print("Polimórfico:", animal.describir())
    try:
        Animal("GEN-001", "Ejemplo", "animal", False)
    except TypeError as error:
        print("TypeError controlado:", error)

    print("\n=== ENTREGA 4 / PRUEBA 1: ORDENAR ALERTAS ===")
    # Ya había dos alertas. Añadimos cuatro en distinto orden y con horas distintas.
    # Las seis permiten comparar prioridad alta/media y desempatar por hora.
    collar_jaguar = s.buscar(s.collares, "codigo", "GPS-01")
    collar_tapir = s.buscar(s.collares, "codigo", "GPS-02")
    s.crear_alerta("rastro en sendero", "media", collar_tapir, "2026-11-08 09:45")
    s.crear_alerta("riesgo junto al poblado", "alta", collar_jaguar, "2026-11-08 08:15")
    s.crear_alerta("batería en observación", "media", collar_tapir, "2026-11-08 07:30")
    s.crear_alerta("animal en zona crítica", "alta", collar_jaguar, "2026-11-08 06:20")
    print("\nANTES DE ORDENAR:")
    imprimir_alertas(s.alertas)
    s.ordenar_alertas()
    print("\nDESPUÉS DE ORDENAR (alta antes de media; luego hora ascendente):")
    imprimir_alertas(s.alertas)

    print("\n=== ENTREGA 4 / PRUEBA 2: BÚSQUEDA BINARIA ===")
    print("Animales ordenados por código mediante selección:")
    s.ordenar_animales_por_codigo()
    for animal in s.animales:
        print(animal.codigo, "-", animal.nombre)
    codigos = [s.animales[0].codigo, s.animales[-1].codigo, "XYZ-999"]
    for codigo in codigos:
        encontrado = s.buscar_animal(codigo)
        print(f"Buscar {codigo}: " +
              (f"ENCONTRADO -> {encontrado.nombre}, {encontrado.especie}" if encontrado else "None (no existe)"))

    print("\nRESUMEN FINAL")
    print(f"Zonas: {len(s.zonas)} | Animales: {len(s.animales)} | Collares: {len(s.collares)}")
    print(f"Lecturas: {len(s.lecturas)} | Alertas: {len(s.alertas)} | Cambios: {len(s.cambios_bateria)}")
    print(f"SMS simulados: {len(s.sms.envios)}")


if __name__ == "__main__":
    main()
