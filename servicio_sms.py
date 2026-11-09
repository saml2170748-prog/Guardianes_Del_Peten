class ServicioSMS:
    def __init__(self):
        self.envios = []
    def enviar(self, alerta, guardarrecursos):
        self.envios.append((alerta.codigo, guardarrecursos.codigo))
        print(f"SMS SIMULADO: {alerta.codigo} para {guardarrecursos.codigo}")