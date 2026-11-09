from abc import ABC, abstractmethod

class Animal(ABC):
    def __init__(self, codigo, nombre, especie, en_peligro):
        self.codigo = codigo
        self.nombre = nombre
        self.especie = especie
        self.en_peligro = en_peligro
        self.collar = None

    def mostrar_datos(self):
        return f"{self.codigo} | {self.nombre} | {self.especie} | En peligro: {self.en_peligro}"

    def consultar_collar(self):
        return self.collar.codigo if self.collar else "Sin collar"

    @abstractmethod
    def describir(self):
        """Cada especie explica sus características particulares."""
