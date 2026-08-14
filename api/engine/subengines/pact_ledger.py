"""
WH40K Dark Pact Ledger & Debt Reclamation Engine (pact_ledger.py)
Libro Mayor de Pactos Oscuros, Etapas de Persecución (1-4) y Reclamación de Almas.
"""

from typing import Dict, List, Any

ETAPAS_PACTO = {
    1: {"nombre": "Marca de Frío", "efecto": "Sombra inconstante, frío persistente, sensación de vigilancia."},
    2: {"nombre": "Persecución Umbral", "efecto": "La sombra del deudor se mueve con autonomía. Aislamiento inseguro."},
    3: {"nombre": "Asedio Físico", "efecto": "Luces fallan, frío intenso destruye suministros, congelación corporal parcial."},
    4: {"nombre": "Reclamación Corporal", "efecto": "El Umbral Negro se abre bajo los pies del deudor y lo arrastra físicamente."}
}

class PactLedgerEngine:

    @staticmethod
    def register_pact(debtor_name: str, terms: str, Category: str = "MEDIO") -> Dict[str, Any]:
        pact_id = f"PACT_{hash(debtor_name) % 100000:05d}"
        return {
            "pact_id": pact_id,
            "debtor_name": debtor_name,
            "terms": terms,
            "category": Category,
            "stage": 1,
            "stage_info": ETAPAS_PACTO[1],
            "status": "SELLADO",
            "message": f"Pacto Oscuro [{pact_id}] sellado con '{debtor_name}'. Términos: {terms}."
        }

    @staticmethod
    def advance_debt_stage(pact_id: str, current_stage: int) -> Dict[str, Any]:
        """
        Avanza la etapa de persecución de un deudor por incumplimiento o traición.
        """
        new_stage = min(4, current_stage + 1)
        info = ETAPAS_PACTO[new_stage]
        
        ready_for_reclamation = (new_stage == 4)
        
        return {
            "pact_id": pact_id,
            "previous_stage": current_stage,
            "new_stage": new_stage,
            "stage_info": info,
            "ready_for_soul_harvest": ready_for_reclamation,
            "message": f"¡INCUMPLIMIENTO DE PACTO! Pacto [{pact_id}] avanza a Etapa {new_stage} [{info['nombre']}]: {info['efecto']}"
        }
