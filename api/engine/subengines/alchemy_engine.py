"""
WH40K Alchemy & Clandestine Pharmacology Engine (alchemy_engine.py)
Síntesis de fármacos, stimms de combate y antídotos en la Clínica Rho-9.
"""

from typing import Dict, List, Any

COMPOUND_RECIPES = {
    "STIMM_COMBATE": {
        "nombre": "Stimm de Combate Hiper-Adrenal",
        "efecto": "+10 a Fuerza y Resistencia durante 3 rondas (-1 a Fatiga al terminar).",
        "requisito_medicina": 50,
        "coste_creditos": 30
    },
    "ANTÍDOTO_ESCHER": {
        "nombre": "Antídoto Universal de Toxinas Escher",
        "efecto": "Neutraliza inmediatamente venenos, toxinas paralizantes y quemaduras químicas.",
        "requisito_medicina": 60,
        "coste_creditos": 45
    },
    "SUERO_UMBRAL": {
        "nombre": "Suero Estabilizador de Mente Umbral",
        "efecto": "+15 de bono de Voluntad contra fenómenos Disformes durante 1 escena.",
        "requisito_medicina": 70,
        "coste_creditos": 80
    }
}

class AlchemyEngine:

    @staticmethod
    def synthesize_compound(compound_key: str, medic_skill: int = 75, available_credits: int = 450) -> Dict[str, Any]:
        """
        Sintetiza un fármaco o compuesto químico en el laboratorio de Rho-9.
        """
        recipe = COMPOUND_RECIPES.get(compound_key.upper(), COMPOUND_RECIPES["STIMM_COMBATE"])
        
        if medic_skill < recipe["requisito_medicina"]:
            return {
                "synthesized": False,
                "reason": f"Habilidad de Medicina insuficiente. Se requiere Medicina {recipe['requisito_medicina']}, pero el cirujano tiene {medic_skill}.",
                "remaining_credits": available_credits
            }

        if available_credits < recipe["coste_creditos"]:
            return {
                "synthesized": False,
                "reason": f"Créditos insuficientes para insumos químicos. Se requieren {recipe['coste_creditos']} Créditos, pero hay {available_credits}.",
                "remaining_credits": available_credits
            }

        new_credits = available_credits - recipe["coste_creditos"]
        return {
            "synthesized": True,
            "compound_name": recipe["nombre"],
            "effect": recipe["efecto"],
            "cost_paid": recipe["coste_creditos"],
            "remaining_credits": new_credits,
            "message": f"¡SÍNTESIS EXITOSA! Se ha creado '{recipe['nombre']}' en Rho-9. Efecto: {recipe['efecto']} Saldo restante: {new_credits} Créditos."
        }
