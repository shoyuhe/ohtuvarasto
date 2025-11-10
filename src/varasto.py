"""Varasto"""

class Varasto:
    """Define varasto"""
    def __init__(self, tilavuus, alku_saldo = 0):
        self.tilavuus = tilavuus

        self.saldo = alku_saldo

    # huom: ominaisuus voidaan myös laskea.
    # Ei tarvita erillistä kenttää viela_tilaa tms.
    def paljonko_mahtuu(self):
        """Check how much space"""
        return self.tilavuus - self.saldo

    def lisaa_varastoon(self, maara):
        """Add to storage"""
        self.saldo = self.saldo + maara

    def ota_varastosta(self, maara):
        """Take from storage"""
        self.saldo = self.saldo - maara
        return maara

    # def __str__(self):
    #     return f"saldo = {self.saldo}, vielä tilaa {self.paljonko_mahtuu()}"
