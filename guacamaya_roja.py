from animal import Animal

class GuacamayaRoja(Animal):
    def __init__(self, codigo, nombre, envergadura_cm=100):
        super().__init__(codigo, nombre, 'guacamaya roja', True)
        self.envergadura_cm = envergadura_cm

    def mostrar_datos(self):
        return super().mostrar_datos() + f" | envergadura_cm: {self.envergadura_cm}"

    def volar(self):
        return f"La guacamaya vuela: {self.nombre}"

    def describir(self):
        return f"{self.nombre} (guacamaya roja) come semillas, habita el dosel del bosque y vuela; envergadura_cm: {self.envergadura_cm}."
