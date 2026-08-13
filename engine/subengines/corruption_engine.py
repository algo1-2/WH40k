"""
WH40K Corruption & Warp Temptations Engine (corruption_engine.py)
Gestión de Puntos de Corrupción (0-100), alteración del alma, marcas y tentaciones disformes.
"""

from typing import Dict, List, Any

CORRUPTION_STAGES = [
    {
        "min": 0, "max": 10,
        "nivel": "ALMA_LIMPIA",
        "descripcion": "Sin alteración ni manchas espirituales perceptibles.",
        "efecto": "Sin modificadores ni penalizaciones."
    },
    {
        "min": 11, "max": 30,
        "nivel": "SUSURROS_MÍNIMOS",
        "descripcion": "Estática disforme leve en las sombras. Sueños inconstantes.",
        "efecto": "+5 a Percepción en la penumbra, pero -5 a Voluntad ante terror Disforme."
    },
    {
        "min": 31, "max": 60,
        "nivel": "MUTACIÓN / MARCA UMBRAL",
        "descripcion": "Alteración corporal o espiritual ligera. Piel fría, sombras adheridas.",
        "efecto": "+10 a Resistencia contra venenos, pero penumbra constante rodea al personaje."
    },
    {
        "min": 61, "max": 90,
        "nivel": "TENTACIÓN MANIFESTADA",
        "descripcion": "El velo del Umbral se rompe con facilidad alrededor del personaje.",
        "efecto": "+1 al Factor Psíquico, pero las tiradas de Fenómenos Disformes aumentan su probabilidad un +25%."
    },
    {
        "min": 91, "max": 100,
        "nivel": "CONDENACIÓN TOTAL",
        "descripcion": "Pérdida de consistencia mortal. Posesión u obediencia al Umbral.",
        "efecto": "Riesgo terminal de pérdida de control del personaje."
    }
]

class CorruptionEngine:

    @staticmethod
    def get_corruption_status(points: int) -> Dict[str, Any]:
        """
        Devuelve el estado de corrupción actual de 0 a 100.
        """
        current_stage = CORRUPTION_STAGES[0]
        for stage in CORRUPTION_STAGES:
            if stage["min"] <= points <= stage["max"]:
                current_stage = stage
                break

        return {
            "corruption_points": points,
            "stage_info": current_stage,
            "message": f"Nivel de Corrupción: {points}/100 [{current_stage['nivel']}]: {current_stage['descripcion']}"
        }

    @staticmethod
    def add_corruption(current_points: int, added_points: int, cause: str) -> Dict[str, Any]:
        """
        Suma puntos de corrupción por contacto con reliquias anómalas o disformidad.
        """
        new_points = min(100, current_points + added_points)
        status = CorruptionEngine.get_corruption_status(new_points)
        
        return {
            "previous_points": current_points,
            "added_points": added_points,
            "new_points": new_points,
            "cause": cause,
            "status_info": status["stage_info"],
            "message": f"¡CORRUPCIÓN INCREMENTADA en +{added_points} por '{cause}'! Nuevo nivel: {new_points}/100 [{status['stage_info']['nivel']}]."
        }
