"""
WH40K Universal Void Naval Combat & Boarding Operations Engine (naval_combat_engine.py)
Combate navales/espaciales, Escudos Vacíos, Baterías de Lanzas, Abordajes y Toma de Puntos Críticos.
"""

from typing import Dict, List, Any

SHIP_TYPES = {
    "FRAGATA": {"nombre": "Fragata Rápida de Escolta", "escudos_vacios": 2, "casco": 20, "baterias": "Macrocñones Ligeros"},
    "CRUCERO": {"nombre": "Crucero de Batalla Clase Dictador", "escudos_vacios": 4, "casco": 50, "baterias": "Lanzas de Energía y Torpedos"},
    "BARCAZA": {"nombre": "Barcaza de Batalla Astartes / Noble", "escudos_vacios": 6, "casco": 80, "baterias": "Bombardeo Pesado y Torpedos de Abordaje"}
}

class NavalCombatEngine:

    @staticmethod
    def resolve_naval_salvo(attacker_ship: str, defender_ship: str, defender_void_shields: int, defender_hull: int) -> Dict[str, Any]:
        """
        Resuelve una salva de artillería naval o baterías de lanzas contra Escudos Vacíos y Casco.
        """
        # Si tiene Escudos Vacíos, colapsa 1 escudo primero
        if defender_void_shields > 0:
            new_shields = defender_void_shields - 1
            new_hull = defender_hull
            msg = f"¡IMPACTO NAVAL SOBRE ESCUDOS VACÍOS! Un escudo ha colapsado. Escudos restantes: {new_shields}."
        else:
            new_shields = 0
            damage = 5
            new_hull = max(0, defender_hull - damage)
            msg = f"¡IMPACTO DIRECTO EN CASCO! Daño naval: {damage}. Integridad de Casco restante: {new_hull}."

        return {
            "attacker_ship": attacker_ship,
            "defender_ship": defender_ship,
            "new_void_shields": new_shields,
            "new_hull_integrity": new_hull,
            "message": msg
        }

    @staticmethod
    def initiate_boarding_action(target_ship_point: str) -> Dict[str, Any]:
        """
        Mecánica de Abordaje y Toma de Punto Crítico (Puente de Mando, Reactor Warp, Baterías).
        """
        return {
            "critical_point": target_ship_point,
            "boarding_status": "BRECHA_EFECTUADA",
            "message": f"¡TORPEDOS DE ABORDAJE IMPACTADOS! Se ha abierto una brecha en '{target_ship_point}'. Fase de combate interior iniciada."
        }
