"""
WH40K Warp & Umbral Phenomena Engine (warp_engine.py)
Calcula y desata fenómenos disformes, fluctuaciones umbrales y la mirada del Observador Profundo.
"""

import random
from typing import Dict, List, Any

FENOMENOS_UMBRALES = [
    {
        "id": "PHEN_COLD_001",
        "nombre": "Frío Sepulcral e Iluminación Muerta",
        "efecto": "La temperatura cae abruptamente a bajo cero. Las luces parpadean y una capa de escarcha negra cubre paredes y equipo. Muestra una señal del Umbral sin daño directo."
    },
    {
        "id": "PHEN_WHISPERS_002",
        "nombre": "Voces en la Penumbra",
        "efecto": "Murmullos incomprensibles del Umbral susurran secretos y nombres de deudores. Todos los presentes no psíquicos deben superar prueba de Voluntad o recibir +1 de Fatiga."
    },
    {
        "id": "PHEN_SHADOW_BLEED_003",
        "nombre": "Hemorragia de Sombras",
        "efecto": "Las sombras de la sala se extienden y sangran líquido oscuro inodoro. Ocultación y Sigilo obtienen +20 durante 3 turnos."
    },
    {
        "id": "PHEN_OBSERVER_LOOK_004",
        "nombre": "Mirada del Observador Profundo",
        "efecto": "Una presencia inmensa y sin forma fija observa desde la dimensión umbral. Alexander recupera 1 alma en la reserva, pero todos los aparatos mecánicos de la sala sufren interferencia durante 1 ronda."
    },
    {
        "id": "PHEN_WARP_BREACH_005",
        "nombre": "Brecha Menor del Umbral",
        "efecto": "Una fisura física se abre brevemente. Se manifiesta un Ente Sombrío Menor que ataca a la criatura no protegida más cercana antes de colapsar."
    }
]

class WarpEngine:

    @staticmethod
    def check_warp_phenomena(power_forced: bool = False, Push_level: int = 0) -> Dict[str, Any]:
        """
        Determina si el uso de un poder psíquico umbral desencadena un fenómeno disforme.
        """
        base_chance = 15 + (Push_level * 20) + (30 if power_forced else 0)
        roll = random.randint(1, 100)

        if roll <= base_chance:
            phenomenon = random.choice(FENOMENOS_UMBRALES)
            return {
                "triggered": True,
                "roll": roll,
                "threshold": base_chance,
                "phenomenon": phenomenon,
                "message": f"¡FENÓMENO DISFORME DESATADO! [{phenomenon['nombre']}]: {phenomenon['efecto']}"
            }
        
        return {
            "triggered": False,
            "roll": roll,
            "threshold": base_chance,
            "message": "La urdimbre permanece estable. No hay fenómeno disforme."
        }
