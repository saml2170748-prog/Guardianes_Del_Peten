class Alerta:
    def __init__(self, codigo, tipo, prioridad, collar, animal, hora):
        self.codigo = codigo
        self.tipo = tipo
        self.prioridad = prioridad
        self.collar = collar
        self.animal = animal
        self.hora = hora
        self.estado = "pendiente"
        self.responsable = None
        self.hora_atencion = None