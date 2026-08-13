"""
WH40K World Context & Planetary Sector Navigation Engine (world_context_engine.py)
Gestión de contexto de mundos, sectores de Necromunda (Hive Primus, Dust Falls, Waste Ashes) y viajes galácticos.
"""

from typing import Dict, List, Any

PLANETARY_LOCATIONS = {
    "DUST_FALLS": {
        "nombre": "Dust Falls (Caídas de Polvo)",
        "tipo": "Asentamiento Principal de Puerta de Submundo",
        "descripcion": "Encrucijada comercial, refugio de fugitivos y centro neutral entre pandillas en el límite inferior de Hive Primus.",
        "peligro_ambiental": "Medio (Polvo de Prometio y filtraciones ácidas)",
        "facciones_dominantes": ["Guilders de la Colmena", "Casa Escher", "Casa Delaque"]
    },
    "HIVE_PRIMUS_UPPER": {
        "nombre": "Aguja Superior de Hive Primus",
        "tipo": "Cúpula de Nobles y Casas Comerciales",
        "descripcion": "Cúpula de lujo, cristal opulento y aire filtrado. Dominada por las Casas Nobles (Helmawr, Greim, Ulanti).",
        "peligro_ambiental": "Bajo (Seguridad Inquisitorial y Enforcers de élite)",
        "facciones_dominantes": ["Casa Helmawr", "Palatine Enforcers de Alta Cúpula"]
    },
    "ASH_WASTES": {
        "nombre": "Desiertos de Ceniza (Ash Wastes)",
        "tipo": "Superficie Planetaria Exterior",
        "descripcion": "Mar de polvo tóxico, tormentas de ceniza radiactiva y convoyes de nómadas en vehículos pesados.",
        "peligro_ambiental": "Extremo (Radiación y tormentas corrosivas)",
        "facciones_dominantes": ["Nómadas de las Cenizas", "Convoyes de Guilders"]
    }
}

class WorldContextEngine:

    @staticmethod
    def get_location_info(location_key: str = "DUST_FALLS") -> Dict[str, Any]:
        """
        Consulta la ficha de contexto del mundo o sector.
        """
        loc = PLANETARY_LOCATIONS.get(location_key.upper(), PLANETARY_LOCATIONS["DUST_FALLS"])
        
        return {
            "location_key": location_key,
            "info": loc,
            "message": f"Contexto de Mundo [{loc['nombre']}]: {loc['descripcion']} Facciones Dominantes: {', '.join(loc['facciones_dominantes'])}."
        }
