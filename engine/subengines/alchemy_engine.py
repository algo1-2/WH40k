"""
WH40K Alchemy & Clandestine Pharmacology Engine v3.0 (alchemy_engine.py)
Síntesis de fármacos, stimms de combate, antídotos y reactivos alquímicos en la Clínica Rho-9.
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
    "SUERO_VERDAD_ESCHER": {
        "key": "SUERO_VERDAD_ESCHER",
        "nombre": "Suero Químico de la Verdad Escher",
        "efecto": "+20 a tiradas de Interrogatorio y Persuasión contra prisioneros o sospechosos durante 1 escena.",
        "requisito_medicina": 55,
        "coste_creditos": 45,
        "categoria": "Inquisición & Inteligencia"
    },
    "TONICO_FUNGICO_COAGULANTE": {
        "key": "TONICO_FUNGICO_COAGULANTE",
        "nombre": "Tónico Coagulante Fúngico del Submundo",
        "efecto": "Estabiliza automáticamente a un paciente en estado agónico (0 PV) evitando la tirada de muerte.",
        "requisito_medicina": 40,
        "coste_creditos": 20,
        "categoria": "Urgencias Clandestinas"
    },
    "NEURO_BLOQUEADOR_DOLOR": {
        "key": "NEURO_BLOQUEADOR_DOLOR",
        "nombre": "Neuro-Bloqueador de Dolor Grado Militar",
        "efecto": "Permite al portador ignorar todos los penalizadores por heridas críticas y dolor durante 4 turnos.",
        "requisito_medicina": 50,
        "coste_creditos": 35,
        "categoria": "Farmacología Táctica"
    },
    "INCIENSO_PURIFICADOR_SANCTUM": {
        "key": "INCIENSO_PURIFICADOR_SANCTUM",
        "nombre": "Incienso Litúrgico de Purificación Disforme",
        "efecto": "Reduce la perturbación psíquica en Rho-9 y permite a Alexander canalizar +1 Alma en la Reserva Umbral.",
        "requisito_medicina": 60,
        "coste_creditos": 50,
        "categoria": "Bio-Ocultismo"
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
    def synthesize_compound(compound_key: str, medic_skill: int = 65, available_credits: int = 1046) -> Dict[str, Any]:
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
        
        chat_prompt = (
            f"[ACCIÓN COGITADOR RHO-9 // ALQUIMIA & FARMACOLOGÍA]\n"
            f"Alexander sintetizó 1 dosis de {recipe['nombre']}.\n"
            f"Categoría: {recipe['categoria']} | Coste: {recipe['coste_creditos']} ¤ (Saldo restante: {new_credits} ¤)\n"
            f"Efecto Activo: {recipe['efecto']}\n"
            f"Estado: Añadido al alijo de Sombra Infinita."
        )

        return {
            "success": True,
            "compound_key": recipe["key"],
            "compound_name": recipe["nombre"],
            "category": recipe["categoria"],
            "effect": recipe["efecto"],
            "cost_paid": recipe["coste_creditos"],
            "remaining_credits": new_credits,
            "chat_prompt": chat_prompt,
            "message": f"¡SÍNTESIS EXITOSA! Se ha creado 1 dosis de '{recipe['nombre']}'. Añadido a Sombra Infinita."
        }
