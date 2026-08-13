"""
WH40K Base Defense & Domain Upkeep Engine (base_engine.py)
Gestión de suministros, defensas y eventos de asedio en Medicae Station Rho-9.
"""

import random
from typing import Dict, List, Any

SIEGE_EVENTS = [
    {
        "id": "SIEGE_ESCHER_001",
        "atacantes": "Pandilla Escher de las Cubiertas Inferiores",
        "motivo": "Saqueo de suministros quirúrgicos y medicamentos",
        "peligro": "Intento de asalto por la escotilla de ventilación norte"
    },
    {
        "id": "SIEGE_ENFORCER_002",
        "atacantes": "Patrulla de Registro de los Palatine Enforcers",
        "motivo": "Inspección de cuarentena clandestina",
        "peligro": "Exige cierre hermético de plastiacero y sigilo absoluto"
    },
    {
        "id": "SIEGE_DELAQUE_003",
        "atacantes": "Infiltradores Delaque",
        "motivo": "Espionaje de los subniveles de Rho-9 y material anómalo de Demer Vhal",
        "peligro": "Infiltración silenciosa mediante hacks de consola"
    }
]

class BaseDefenseEngine:

    @staticmethod
    def check_base_upkeep(resources: Dict[str, int]) -> Dict[str, Any]:
        """
        Verifica los niveles de Prometio, Agua Purificada y Capacidad de Conservación en Frío de Rho-9.
        """
        promethium = resources.get("prometio_tanques", 85)
        water = resources.get("agua_purificada_litros", 420)
        cold_storage = resources.get("congeladores_organos_status", "OPERATIVO")

        warning = None
        if promethium < 20:
            warning = "¡ALERTA DE ENERGÍA! Tanques de prometio por debajo del 20%. Los congeladores de órganos corren peligro."
        elif water < 50:
            warning = "¡ALERTA DE AGUA! Filtros de agua purificada agotándose."

        return {
            "status": "OPERATIVO" if not warning else "ADVERTENCIA",
            "promethium_level": f"{promethium}%",
            "water_liters": water,
            "cold_storage": cold_storage,
            "warning": warning
        }

    @staticmethod
    def trigger_random_siege_event() -> Dict[str, Any]:
        """
        Genera un evento de asedio o amenaza sobre Medicae Station Rho-9.
        """
        event = random.choice(SIEGE_EVENTS)
        return {
            "siege_active": True,
            "event": event,
            "message": f"¡ALERTA EN RHO-9! Threat: {event['atacantes']} — Motivo: {event['motivo']}. Peligro: {event['peligro']}."
        }
