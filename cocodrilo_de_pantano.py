from animal import Animal

class CocodriloDePantano(Animal):
    def __init__(self, codigo, nombre, longitud_m=3):
        super().__init__(codigo, nombre, 'cocodrilo de pantano', False)
        self.longitud_m = longitud_m

    def mostrar_datos(self):
        return super().mostrar_datos() + f" | longitud_m: {self.longitud_m}"

    def sumergirse(self):
        return f"El cocodrilo se sumerge: {self.nombre}"

    def describir(self):
        return f"{self.nombre} (cocodrilo de pantano) come peces, habita humedales y se mueve nadando y caminando; longitud_m: {self.longitud_m}."
