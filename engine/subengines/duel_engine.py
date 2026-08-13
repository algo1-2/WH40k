"""
WH40K Universal Dueling & Melee Counter Stance Engine (duel_engine.py)
Mecánica universal para duelos de honor, posturas (Ofensiva/Defensiva/Réplica) y contraataques.
"""

from typing import Dict, List, Any

DUEL_STANCES = {
    "OFENSIVA": {"bonus_cc": 10, "penalty_resilience": -1, "desc": "Ataque agresivo (+10% CC, -1 a Resiliencia)."},
    "DEFENSIVA": {"bonus_esquiva": 15, "bonus_resilience": 1, "desc": "Guardia alta y parada (+15% Esquiva, +1 a Resiliencia)."},
    "RÉPLICA": {"bonus_contraataque": True, "desc": "Guardia de respuesta. Contraataque automático si el atacante falla por 20+ puntos."}
}

class DuelEngine:

    @staticmethod
    def resolve_duel_round(attacker_name: str, defender_name: str, defender_stance: str, attacker_roll: Dict[str, Any]) -> Dict[str, Any]:
        stance = DUEL_STANCES.get(defender_stance.upper(), DUEL_STANCES["DEFENSIVA"])
        
        is_fail = attacker_roll.get("resultado_base") == "FALLO"
        distance = attacker_roll.get("distancia", 0)

        counter_triggered = False
        if stance.get("bonus_contraataque") and is_fail and distance >= 20:
            counter_triggered = True

        return {
            "attacker_name": attacker_name,
            "defender_name": defender_name,
            "defender_stance": defender_stance,
            "stance_info": stance,
            "counter_triggered": counter_triggered,
            "message": f"Duelo Universal: {defender_name} en Postura [{defender_stance}]. {'¡CONTRAATAQUE DE RÉPLICA DESATADO!' if counter_triggered else 'Guardia mantenida.'}"
        }
