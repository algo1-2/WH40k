"""
WH40K Imperial Miracles & Acts of Faith Engine (miracles_engine.py)
Gestión de Actos de Fe, Milagros Imperiales del Dios-Emperador y Exorcismos.
"""

from typing import Dict, List, Any

MIRACLES_CATALOG = {
    "SHIELD_OF_EMPEROR": {
        "nombre": "Escudo del Emperador",
        "tipo": "Interrupción de Reacción Sagrada",
        "coste_fe": 1,
        "efecto": "Niega completamente un impacto letal o daño desastroso entrante mediante un destello de luz dorada."
    },
    "FURIA_DEL_JUSTO": {
        "nombre": "Furia del Justo",
        "tipo": "Potenciador de Asalto",
        "coste_fe": 1,
        "efecto": "Concede Éxito Crítico automático en la siguiente tirada d100 de combate."
    },
    "LUZ_PURIFICADORA": {
        "nombre": "Luz Purificadora",
        "tipo": "Liturgia de Exorcismo",
        "coste_fe": 2,
        "efecto": "Expulsa entes disformes menores y reduce 5 puntos de Corrupción acumulados."
    }
}

class MiraclesEngine:

    @staticmethod
    def invoke_miracle(miracle_key: str, current_faith: int) -> Dict[str, Any]:
        """
        Invoca un Acto de Fe / Milagro Imperial gastando puntos de Fe.
        """
        miracle = MIRACLES_CATALOG.get(miracle_key, MIRACLES_CATALOG["SHIELD_OF_EMPEROR"])
        cost = miracle["coste_fe"]

        if current_faith < cost:
            return {
                "invoked": False,
                "reason": f"Puntos de Fe insuficientes. Se requerían {cost}, pero el personaje tiene {current_faith}.",
                "remaining_faith": current_faith
            }

        new_faith = current_faith - cost
        return {
            "invoked": True,
            "miracle": miracle,
            "faith_spent": cost,
            "remaining_faith": new_faith,
            "message": f"¡MILAGRO IMPERIAL INVOCADO! [{miracle['nombre']}]: {miracle['efecto']} (Puntos de Fe restantes: {new_faith})."
        }
