"""
WH40K Universal Beast Hunting, Taming & Creature Management Engine (beast_taming_engine.py)
Mecánica universal para caza, rastreo, doma y adiestramiento de bestias del submundo.
"""

from typing import Dict, List, Any

class BeastTamingEngine:

    @staticmethod
    def attempt_taming(creature_name: str, actor_taming_skill: int, creature_ferocity: int = 40) -> Dict[str, Any]:
        """
        Mecánica universal de doma o apaciguamiento de bestias del submundo.
        """
        effective_threshold = actor_taming_skill - (creature_ferocity // 2)
        
        return {
            "creature_name": creature_name,
            "creature_ferocity": creature_ferocity,
            "actor_skill": actor_taming_skill,
            "effective_threshold": effective_threshold,
            "message": f"Intento Universal de Doma de '{creature_name}': Umbral calculado: {effective_threshold}% (Ferocidad: {creature_ferocity})."
        }

    @staticmethod
    def register_tamed_beast(creature_name: str, role: str = "Guardián de Base") -> Dict[str, Any]:
        """
        Registra una bestia adiestrada como activo de defensa o rastreo.
        """
        beast_id = f"BEAST_{hash(creature_name) % 10000:04d}"
        return {
            "beast_id": beast_id,
            "creature_name": creature_name,
            "role": role,
            "status": "ADIESTRADA",
            "message": f"Bestia [{beast_id}] '{creature_name}' registrada con rol: '{role}'."
        }
