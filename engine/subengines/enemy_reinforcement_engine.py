"""
WH40K Enemy & Finite Reinforcement Pool Engine (enemy_reinforcement_engine.py)
Generación procedimental de unidades enemigas con estadísticas completas y control estricto de Límite Finito de Refuerzos.
"""

from typing import Dict, List, Any

class EnemyReinforcementEngine:

    @staticmethod
    def spawn_reinforcements(enemy_type: str, requested_count: int, current_reinforcement_pool: int) -> Dict[str, Any]:
        """
        Calcula la llegada de refuerzos enemigos limitados por la Reserva Finitas del enfrentamiento.
        """
        if current_reinforcement_pool <= 0:
            return {
                "spawned_count": 0,
                "remaining_pool": 0,
                "message": "¡SIN MÁS REFUERZOS ENEMIGOS! La reserva enemiga ha sido completamente agotada."
            }

        actual_spawned = min(requested_count, current_reinforcement_pool)
        new_pool = current_reinforcement_pool - actual_spawned

        return {
            "enemy_type": enemy_type,
            "requested": requested_count,
            "actual_spawned": actual_spawned,
            "remaining_pool": new_pool,
            "message": f"¡LLEGADA DE REFUERZOS! Han ingresado {actual_spawned}x '{enemy_type}'. Reserva enemiga restante: {new_pool} unidades."
        }
