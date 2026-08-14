"""
WH40K Alchemy & Clandestine Pharmacology Engine (alchemy_engine.py)
Síntesis de fármacos, stimms de combate y antídotos en la Clínica Rho-9.
"""

from typing import Dict, List, Any

COMPOUND_RECIPES = {
    "STIMM_COMBATE": {
        "key": "STIMM_COMBATE",
        "nombre": "Stimm de Combate Hiper-Adrenal",
        "efecto": "+10 a Reflejos y Fuerza durante 3 turnos; anula penalizadores de fatiga.",
        "requisito_medicina": 50,
        "coste_creditos": 30,
        "categoria": "Farmacología Táctica"
    },
    "VENENO_TOXIC1": {
        "key": "VENENO_TOXIC1",
        "nombre": "Concentrado Neurotóxico E-12 [Toxic(1)]",
        "efecto": "Impregna 1 arma blanca. Inflige daño de veneno continuo al impactar (Tirada de Resistencia con -10 o 1d5 PV/turno).",
        "requisito_medicina": 60,
        "coste_creditos": 40,
        "categoria": "Toxinas & Armamento"
    },
    "ANTIDOTO_UNIVERSAL": {
        "key": "ANTIDOTO_UNIVERSAL",
        "nombre": "Antídoto Químico de Amplio Espectro",
        "efecto": "Neutraliza inmediatamente venenos orgánicos, quimio-toxinas Escher y gases cáusticos.",
        "requisito_medicina": 55,
        "coste_creditos": 35,
        "categoria": "Farmacología Médica"
    },
    "BALSAMO_CAUTERIZANTE": {
        "key": "BALSAMO_CAUTERIZANTE",
        "nombre": "Bálsamo Hemostático Cauterizante",
        "efecto": "Cierra hemorragias profusas al instante (+3 PV inmediatos y previene desangrado).",
        "requisito_medicina": 45,
        "coste_creditos": 25,
        "categoria": "Traumatología"
    },
    "SUERO_UMBRAL": {
        "key": "SUERO_UMBRAL",
        "nombre": "Suero Estabilizador de Mente Umbral",
        "efecto": "+15 de bono de Voluntad contra fenómenos Disformes durante 1 escena completa.",
        "requisito_medicina": 65,
        "coste_creditos": 60,
        "categoria": "Bio-Ocultismo"
    }
}

class AlchemyEngine:

    @staticmethod
    def get_available_recipes() -> List[Dict[str, Any]]:
        return list(COMPOUND_RECIPES.values())

    @staticmethod
    def synthesize_compound(compound_key: str, medic_skill: int = 65, available_credits: int = 1196) -> Dict[str, Any]:
        """
        Sintetiza un fármaco o compuesto químico en el laboratorio de Rho-9.
        """
        recipe = COMPOUND_RECIPES.get(compound_key.upper())
        if not recipe:
            return {"success": False, "error": f"Fórmula química '{compound_key}' no reconocida."}
        
        if medic_skill < recipe["requisito_medicina"]:
            return {
                "success": False,
                "error": f"Habilidad de Medicina insuficiente (Requerida: {recipe['requisito_medicina']}, Alexander: {medic_skill}).",
                "remaining_credits": available_credits
            }

        if available_credits < recipe["coste_creditos"]:
            return {
                "success": False,
                "error": f"Créditos insuficientes para reactivos ({available_credits} ¤ disponibles, requiere {recipe['coste_creditos']} ¤).",
                "remaining_credits": available_credits
            }

        new_credits = available_credits - recipe["coste_creditos"]
        return {
            "success": True,
            "compound_key": recipe["key"],
            "compound_name": recipe["nombre"],
            "effect": recipe["efecto"],
            "cost_paid": recipe["coste_creditos"],
            "remaining_credits": new_credits,
            "message": f"¡SÍNTESIS EXITOSA! Se ha creado 1 dosis de '{recipe['nombre']}'. Añadido a Sombra Infinita."
        }
