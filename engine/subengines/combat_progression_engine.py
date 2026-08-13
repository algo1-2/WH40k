"""
WH40K Combat Dominance & Progression Bar Engine (combat_progression_engine.py)
Barra de Progresión de Combate (0-100%), moral enemiga y cálculo automático de victoria o cumplimiento de objetivo.
"""

from typing import Dict, List, Any

class CombatProgressionEngine:

    @staticmethod
    def update_combat_progression(current_percentage: int, delta: int, cause: str) -> Dict[str, Any]:
        """
        Actualiza la Barra de Progresión de Combate de 0 a 100%.
        """
        new_percentage = max(0, min(100, current_percentage + delta))
        
        status = "EN_PROGRESO"
        victory = False
        
        if new_percentage >= 100:
            status = "VICTORIA_ABSOLUTA / OBJETIVO_CUMPLIDO"
            victory = True
        elif new_percentage >= 75:
            status = "DOMINIO_TOTAL / ENEMIGO_EN_RETIRADA"
        elif new_percentage >= 50:
            status = "PUNTO_DE_INFLEXIÓN / MORAL_ENEMIGA_ROTA"
        elif new_percentage >= 25:
            status = "VENTAJA_INICIAL"

        formatted_bar = "█" * (new_percentage // 5) + "░" * (20 - (new_percentage // 5))

        return {
            "previous_percentage": current_percentage,
            "delta_applied": delta,
            "new_percentage": new_percentage,
            "cause": cause,
            "status": status,
            "victory_achieved": victory,
            "progress_bar": f"[{formatted_bar}] {new_percentage}%",
            "message": f"¡BARRA DE PROGRESIÓN DE COMBATE!: [{formatted_bar}] {new_percentage}% [{status}]. Causa: {cause}."
        }
