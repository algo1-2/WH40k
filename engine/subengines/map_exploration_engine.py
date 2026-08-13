"""
WH40K Map & Underhive Sector Exploration Engine (map_exploration_engine.py)
Generación procedimental y exploración de los subniveles de Medicae Station Rho-9.
"""

import random
from typing import Dict, List, Any

SUBNIVELES_CATALOG = [
    {
        "nivel": "Subnivel -1",
        "nombre": "Conductos de Ventilación y Depósitos de Prometio",
        "descripcion": "Tuberías industriales oxidadas, gas residual y filtraciones de agua salobre.",
        "amenaza": "Baja (Ratas de las sombras y filtraciones tóxicas)",
        "botin_potencial": "Células de energía y piezas mecánicas de repuesto"
    },
    {
        "nivel": "Subnivel -2",
        "nombre": "Antiguo Quirófano del Mechanicus y Taller Olvidado",
        "descripcion": "Terminales cogitadoras desconectadas, mesas de amputación de acero pesado y servotores inactivos.",
        "amenaza": "Media (Servidor de combate descalibrado)",
        "botin_potencial": "Arqueotecnología médica e implantes cibernéticos"
    },
    {
        "nivel": "Subnivel -3",
        "nombre": "Catacumbas del Umbral y Fosa Profunda",
        "descripcion": "Estructura gótica pre-Imperial sumergida en penumbra absoluta. El velo del Umbral es extremadamente delgado.",
        "amenaza": "Alta (Manifestaciones umbrales y distorsión espacial)",
        "botin_potencial": "Reliquias de almas y pergaminos de conocimiento prohibido"
    }
]

class MapExplorationEngine:

    @staticmethod
    def explore_sector(sublevel_index: int = 1) -> Dict[str, Any]:
        """
        Genera el informe de exploración de un sector de los subniveles de Rho-9.
        """
        idx = max(0, min(len(SUBNIVELES_CATALOG) - 1, sublevel_index - 1))
        sector = SUBNIVELES_CATALOG[idx]
        
        hazard_triggered = random.choice([True, False])
        
        return {
            "explored_sublevel": sector["nivel"],
            "sector_name": sector["nombre"],
            "description": sector["descripcion"],
            "threat_level": sector["amenaza"],
            "potential_loot": sector["botin_potencial"],
            "hazard_triggered": hazard_triggered,
            "message": f"¡EXPLORACIÓN DE {sector['nivel'].upper()}!: {sector['nombre']}. {sector['descripcion']} Amenaza: {sector['amenaza']}."
        }
