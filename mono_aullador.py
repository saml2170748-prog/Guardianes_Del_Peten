from animal import Animal

class MonoAullador(Animal):
    def __init__(self, codigo, nombre, altura_m=1):
        super().__init__(codigo, nombre, 'mono aullador', False)
        self.altura_m = altura_m

    def mostrar_datos(self):
        return super().mostrar_datos() + f" | altura_m: {self.altura_m}"

    def aullar(self):
        return f"El mono aullador aúlla: {self.nombre}"

    def describir(self):
        return f"{self.nombre} (mono aullador) come hojas, vive en las copas de los árboles y trepa; altura_m: {self.altura_m}."
