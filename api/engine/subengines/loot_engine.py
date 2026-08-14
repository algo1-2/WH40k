"""
WH40K Loot, Black Market & Arqueotech Engine (loot_engine.py)
Generación procedimental de botín, suministros médicos y objetos raros del Submundo.
"""

import random
from typing import Dict, List, Any

LOOT_TABLES = {
    "RHO9_SUBNIVELES": [
        {"item": "Cargador Bólter de Alta Capacidad (12 cartuchos)", "raridad": "COMÚN"},
        {"item": "Cargas Quirúrgicas de Medikit (+2 Cargas)", "raridad": "COMÚN"},
        {"item": "Dosis de Estimulante Stimm de Combate", "raridad": "POCO_COMÚN"},
        {"item": "Implante Ocular Térmico Descalibrado", "raridad": "RARA"},
        {"item": "Célula de Energía de Plasma Antiguo", "raridad": "RARA"},
        {"item": "Fragmento de Arqueotecnología de Cogitador", "raridad": "ÉPICA"}
    ],
    "ENEMIGOS_CAÍDOS": [
        {"item": "Bolsa de Créditos de Necromunda (+85 Créditos)", "raridad": "COMÚN"},
        {"item": "Autopistola de Pandillero", "raridad": "COMÚN"},
        {"item": "Inyector de Narcóticos Escher", "raridad": "POCO_COMÚN"},
        {"item": "Micro-comunicador Codificado Enforcer", "raridad": "RARA"}
    ]
}

class LootEngine:

    @staticmethod
    def generate_loot(table_key: str = "RHO9_SUBNIVELES") -> Dict[str, Any]:
        table = LOOT_TABLES.get(table_key, LOOT_TABLES["RHO9_SUBNIVELES"])
        loot_item = random.choice(table)
        
        return {
            "loot_found": loot_item["item"],
            "rarity": loot_item["raridad"],
            "table_used": table_key,
            "message": f"¡BOTÍN ENCONTRADO! [{loot_item['raridad']}]: {loot_item['item']}."
        }
