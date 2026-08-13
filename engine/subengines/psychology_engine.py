"""
WH40K Psychology, Loyalty, Faith, Machine Spirit & DM Conduct Engine (psychology_engine.py)
Gobierna la Lealtad/Vínculos de PNJ, Fe/Fanatismo Imperial y Apaciguamiento de Espíritus Máquina.
"""

from typing import Dict, List, Any

class PsychologyEngine:

    @staticmethod
    def evaluate_loyalty_and_bonds(npc_name: str, loyalty_val: int, player_action: str) -> Dict[str, Any]:
        """
        Evalúa el impacto de las acciones del jugador sobre la lealtad, confianza o afecto de un PNJ/Séquito.
        """
        status = "ESTABLE"
        if loyalty_val >= 80:
            status = "DEVOCIÓN_ABSOLUTA / VÍNCULO PROFUNDO"
        elif loyalty_val >= 50:
            status = "LEALTAD_RESPECTUOSA"
        elif loyalty_val >= 30:
            status = "DUDA / RESENTIMIENTO_DISIMULADO"
        else:
            status = "RIESGO_DE_TRAICIÓN_INMINENTE"

        return {
            "npc_name": npc_name,
            "loyalty_level": loyalty_val,
            "status": status,
            "message": f"Nivel de lealtad de {npc_name}: {loyalty_val}% [{status}]."
        }

    @staticmethod
    def evaluate_imperial_faith(faith_points: int, zealotry_active: bool) -> Dict[str, Any]:
        """
        Calcula la protección espiritual y la voluntad fanática frente a la corrupción o el terror.
        """
        corruption_resistance_bonus = faith_points // 2
        morale_bonus = +20 if zealotry_active else +0

        return {
            "faith_points": faith_points,
            "zealotry_active": zealotry_active,
            "corruption_resistance_bonus": corruption_resistance_bonus,
            "morale_bonus": morale_bonus,
            "message": f"Fe en el Emperador: {faith_points} | Protección contra Corrupción: +{corruption_resistance_bonus} | Bono de Zelo: +{morale_bonus}%"
        }

    @staticmethod
    def Machine_spirit_appeasement(tech_skill: int, ritual_performed: bool) -> Dict[str, Any]:
        """
        Apaciguamiento de los Espíritus Máquina del Adeptus Mechanicus / Cogitadores / Vehículos.
        """
        bonus = +15 if ritual_performed else -10
        effective_target = tech_skill + bonus
        
        return {
            "ritual_performed": ritual_performed,
            "bonus_applied": bonus,
            "effective_threshold": effective_target,
            "message": f"Apaciguamiento del Espíritu Máquina: {'Ritual sagrado efectuado (+15%)' if ritual_performed else 'Sin ritual sagrado (-10%)'}. Umbral final: {effective_target}%."
        }
