from animal import Animal

class Jaguar(Animal):
    def __init__(self, codigo, nombre, territorio_km2=40):
        super().__init__(codigo, nombre, 'jaguar', True)
        self.territorio_km2 = territorio_km2

    def mostrar_datos(self):
        return super().mostrar_datos() + f" | territorio_km2: {self.territorio_km2}"

    def rugir(self):
        return f"Rugido de jaguar: {self.nombre}"

    def describir(self):
        return f"{self.nombre} (jaguar) es carnívoro, caza en la selva, camina y nada; territorio_km2: {self.territorio_km2}."
