import re
from datetime import datetime
from jaguar import Jaguar
from tapir import Tapir
from guacamaya_roja import GuacamayaRoja
from cocodrilo_de_pantano import CocodriloDePantano
from mono_aullador import MonoAullador
from collar import Collar
from zona import Zona
from guardarrecursos import Guardarrecursos
from lectura import Lectura
from alerta import Alerta
from cambio_bateria import CambioBateria
from servicio_sms import ServicioSMS

class SistemaMonitoreo:
    # Artículo 10: fecha y hora reales en formato AAAA-MM-DD HH:MM.
    ESPECIES = {"jaguar": True, "tapir": True, "guacamaya roja": True,
                "cocodrilo de pantano": False, "mono aullador": False}
    TIPOS = ("núcleo", "amortiguamiento", "uso múltiple")

    def __init__(self):
        self.animales = []
        self.collares = []
        self.zonas = []
        self.guardarrecursos = []
        self.lecturas = []
        self.alertas = []
        self.cambios_bateria = []
        self.sms = ServicioSMS()
        self.turno = None

    def buscar(self, objetos, atributo, valor):
        # Búsqueda lineal general de las entregas anteriores.
        for objeto in objetos:
            if getattr(objeto, atributo) == valor:
                return objeto
        return None

    def rechazar(self, mensaje):
        print("RECHAZADO: " + mensaje)
        return False

    def hora_valida(self, hora):
        if not isinstance(hora, str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}", hora):
            return False
        try:
            datetime.strptime(hora, "%Y-%m-%d %H:%M")
            return True
        except ValueError:
            return False

    def bateria_valida(self, nivel):
        return type(nivel) in (int, float) and 0 <= nivel <= 100

    def codigo_guardia_valido(self, codigo):
        return isinstance(codigo, str) and re.fullmatch(r"[A-Z]{2}-[0-9]{2}", codigo) is not None

    def registrar_guardarrecursos(self, codigo, nombre):
        if not self.codigo_guardia_valido(codigo):
            return self.rechazar("art. 7: código de guardarrecursos inválido")
        if self.buscar(self.guardarrecursos, "codigo", codigo):
            return self.rechazar("guardarrecursos repetido")
        self.guardarrecursos.append(Guardarrecursos(codigo, nombre))
        return True

    def establecer_turno(self, codigo):
        guardia = self.buscar(self.guardarrecursos, "codigo", codigo)
        if not guardia:
            return self.rechazar("guardarrecursos de turno inexistente")
        self.turno = guardia
        return True

    def registrar_zona(self, nombre, tipo):
        if tipo not in self.TIPOS:
            return self.rechazar("art. 5: tipo de zona inválido")
        if self.buscar(self.zonas, "nombre", nombre):
            return self.rechazar("zona repetida")
        self.zonas.append(Zona(nombre, tipo))
        return True

    def registrar_collar(self, codigo, bateria):
        if not self.bateria_valida(bateria):
            return self.rechazar("art. 3: batería fuera de 0 a 100")
        if self.buscar(self.collares, "codigo", codigo):
            return self.rechazar("collar repetido")
        self.collares.append(Collar(codigo, bateria))
        return True

    def registrar_animal(self, codigo, nombre, especie, en_peligro):
        if not isinstance(codigo, str) or not re.fullmatch(r"[A-Z]{3}-[0-9]{3}", codigo):
            return self.rechazar("art. 1: código animal inválido")
        if self.buscar(self.animales, "codigo", codigo):
            return self.rechazar("art. 1: código animal repetido")
        if especie not in self.ESPECIES:
            return self.rechazar("especie no configurada")
        if type(en_peligro) is not bool or en_peligro != self.ESPECIES[especie]:
            return self.rechazar("art. 2: estado de conservación incorrecto")
        clases = {"jaguar": Jaguar, "tapir": Tapir,
                  "guacamaya roja": GuacamayaRoja,
                  "cocodrilo de pantano": CocodriloDePantano,
                  "mono aullador": MonoAullador}
        self.animales.append(clases[especie](codigo, nombre))
        print(f"Animal registrado: {codigo}, {nombre}")
        return True

    def asignar_collar(self, codigo_collar, codigo_animal):
        collar = self.buscar(self.collares, "codigo", codigo_collar)
        animal = self.buscar(self.animales, "codigo", codigo_animal)
        if not collar or not animal:
            return self.rechazar("collar o animal inexistente")
        if collar.animal:
            return self.rechazar(f"art. 4: collar ocupado por {collar.animal.codigo}")
        if animal.collar:
            return self.rechazar(f"art. 4: animal ya lleva {animal.collar.codigo}")
        collar.animal = animal
        animal.collar = collar
        print(f"Collar {codigo_collar} asignado a {codigo_animal}")
        return True

    def crear_alerta(self, tipo, prioridad, collar, hora):
        if prioridad not in ("alta", "media") or not self.hora_valida(hora):
            return self.rechazar("prioridad u hora de alerta inválida")
        alerta = Alerta(f"AL-{len(self.alertas) + 1:03}", tipo, prioridad,
                        collar, collar.animal if collar else None, hora)
        self.alertas.append(alerta)
        print(f"Alerta {alerta.codigo}: {tipo}, prioridad {prioridad}, {hora}")
        return alerta

    def reportar_posicion(self, codigo_collar, nombre_zona, hora):
        collar = self.buscar(self.collares, "codigo", codigo_collar)
        if not collar:
            return self.rechazar("collar inexistente")
        if collar.bateria < 10:
            if not self.hora_valida(hora):
                return self.rechazar("art. 10: fecha u hora inválida")
            self.crear_alerta("batería baja", "media", collar, hora)
            return self.rechazar("art. 3: batería menor que 10%; lectura no guardada")
        zona = self.buscar(self.zonas, "nombre", nombre_zona)
        if not zona:
            return self.rechazar("art. 5: zona no registrada")
        if not collar.animal:
            return self.rechazar("collar sin animal asignado")
        if not self.hora_valida(hora):
            return self.rechazar("art. 10: fecha u hora inválida")
        riesgo = collar.animal.en_peligro and zona.tipo == "uso múltiple"
        if riesgo and self.turno is None:
            return self.rechazar("art. 6: falta configurar guardarrecursos de turno")
        self.lecturas.append(Lectura(collar.animal, zona, hora, "GPS"))
        print(f"Posición: {collar.animal.codigo}, {zona.nombre}, {hora}")
        if riesgo:
            alerta = self.crear_alerta("acercamiento a comunidad", "alta", collar, hora)
            self.sms.enviar(alerta, self.turno)
        return True

    def registrar_avistamiento(self, codigo_guardia, codigo_animal, nombre_zona, hora):
        if not self.codigo_guardia_valido(codigo_guardia):
            return self.rechazar("art. 7: código de guardarrecursos inválido")
        guardia = self.buscar(self.guardarrecursos, "codigo", codigo_guardia)
        if not guardia:
            return self.rechazar("guardarrecursos no registrado")
        animal = self.buscar(self.animales, "codigo", codigo_animal)
        zona = self.buscar(self.zonas, "nombre", nombre_zona)
        if not animal or not zona:
            return self.rechazar("animal o zona inexistente")
        if not self.hora_valida(hora):
            return self.rechazar("art. 10: fecha u hora inválida")
        self.lecturas.append(Lectura(animal, zona, hora, "avistamiento", guardia))
        print(f"Avistamiento: {animal.codigo} por {guardia.codigo}")
        return True

    def listar_alertas_pendientes(self):
        pendientes = []
        for alerta in self.alertas:
            if alerta.estado == "pendiente":
                pendientes.append(alerta)
                print(f"Pendiente: {alerta.codigo}, {alerta.tipo}")
        if not pendientes:
            print("No hay alertas pendientes")
        return pendientes

    def atender_alerta(self, codigo_alerta, codigo_guardia, hora):
        self.listar_alertas_pendientes()
        alerta = self.buscar(self.alertas, "codigo", codigo_alerta)
        if not alerta:
            return self.rechazar("alerta inexistente")
        if alerta.estado == "atendida":
            return self.rechazar(f"art. 8: ya atendida por {alerta.responsable.codigo}")
        if not self.codigo_guardia_valido(codigo_guardia):
            return self.rechazar("art. 7: código de guardarrecursos inválido")
        guardia = self.buscar(self.guardarrecursos, "codigo", codigo_guardia)
        if not guardia:
            return self.rechazar("guardarrecursos no registrado")
        if not self.hora_valida(hora):
            return self.rechazar("art. 10: fecha u hora inválida")
        alerta.estado = "atendida"
        alerta.responsable = guardia
        alerta.hora_atencion = hora
        print(f"Alerta {codigo_alerta} atendida por {codigo_guardia}, {hora}")
        return True

    def cambiar_bateria(self, codigo_collar, codigo_guardia, nuevo, hora):
        if not self.codigo_guardia_valido(codigo_guardia):
            return self.rechazar("art. 7: código de guardarrecursos inválido")
        guardia = self.buscar(self.guardarrecursos, "codigo", codigo_guardia)
        collar = self.buscar(self.collares, "codigo", codigo_collar)
        if not guardia or not collar:
            return self.rechazar("collar o guardarrecursos inexistente")
        if not self.bateria_valida(nuevo):
            return self.rechazar("arts. 3 y 9: nuevo nivel fuera de 0 a 100")
        if not self.hora_valida(hora):
            return self.rechazar("art. 10: fecha u hora inválida")
        self.cambios_bateria.append(CambioBateria(collar, collar.bateria, nuevo, guardia, hora))
        collar.bateria = nuevo
        print(f"Batería {codigo_collar}: {nuevo}% por {codigo_guardia}, {hora}")
        return True

    def consultar_movimientos(self, codigo_animal):
        animal = self.buscar(self.animales, "codigo", codigo_animal)
        if not animal:
            self.rechazar("animal inexistente; sin resultados")
            return []
        movimientos = []
        for lectura in self.lecturas:
            if lectura.animal is animal:
                movimientos.append(lectura)
        print(f"Movimientos de {codigo_animal}: {len(movimientos)}")
        for lectura in movimientos:
            print(f"    {lectura.hora} | {lectura.zona.nombre} | {lectura.origen}")
        return movimientos

    # ENTREGA 4: Selección por prioridad, y después por hora.
    def ordenar_alertas(self):
        def nivel(alerta):
            if alerta.prioridad == "alta":
                return 1
            return 2

        for i in range(len(self.alertas) - 1):
            minimo = i
            for j in range(i + 1, len(self.alertas)):
                actual = self.alertas[j]
                menor = self.alertas[minimo]
                if (nivel(actual) < nivel(menor) or
                        (nivel(actual) == nivel(menor) and actual.hora < menor.hora)):
                    minimo = j
            if minimo != i:
                self.alertas[i], self.alertas[minimo] = self.alertas[minimo], self.alertas[i]
        return self.alertas

    # ENTREGA 4: Selección por código de animal, sin sort() ni sorted().
    def ordenar_animales_por_codigo(self):
        for i in range(len(self.animales) - 1):
            minimo = i
            for j in range(i + 1, len(self.animales)):
                if self.animales[j].codigo < self.animales[minimo].codigo:
                    minimo = j
            if minimo != i:
                self.animales[i], self.animales[minimo] = self.animales[minimo], self.animales[i]
        return self.animales

    # ENTREGA 4: Búsqueda binaria en la lista ya ordenada por selección.
    def buscar_animal(self, codigo):
        self.ordenar_animales_por_codigo()
        inicio = 0
        fin = len(self.animales) - 1
        while inicio <= fin:
            medio = (inicio + fin) // 2
            if self.animales[medio].codigo == codigo:
                return self.animales[medio]
            if codigo < self.animales[medio].codigo:
                fin = medio - 1
            else:
                inicio = medio + 1
        return None
