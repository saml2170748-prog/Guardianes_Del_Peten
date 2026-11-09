from animal import Animal

class Tapir(Animal):
    def __init__(self, codigo, nombre, peso_kg=220):
        super().__init__(codigo, nombre, 'tapir', True)
        self.peso_kg = peso_kg

    def mostrar_datos(self):
        return super().mostrar_datos() + f" | peso_kg: {self.peso_kg}"

    def nadar(self):
        return f"El tapir nada: {self.nombre}"

    def describir(self):
        return f"{self.nombre} (tapir) es herbívoro, come frutos, vive en bosques y camina y nada; peso_kg: {self.peso_kg}."
