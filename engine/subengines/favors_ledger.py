"""
WH40K Favors Ledger & Faction Obligations Engine (favors_ledger.py)
Libro Mayor de Favores Pendientes, Deudas Faccionales y Cobros en Necromunda.
"""

from typing import Dict, List, Any

class FavorsLedgerEngine:

    @staticmethod
    def register_favor(faction_name: str, favor_value: str, origin: str, collateral: str = "Respeto mutuo") -> Dict[str, Any]:
        """
        Registra un favor adeudado o concedido por una facción (Casa Escher, Delaque, Enforcers, etc.).
        """
        favor_id = f"FAVOR_{hash(faction_name + origin) % 100000:05d}"
        return {
            "favor_id": favor_id,
            "faction_name": faction_name,
            "favor_value": favor_value, # MENOR, MEDIO, MAYOR
            "origin": origin,
            "collateral": collateral,
            "status": "PENDIENTE_DE_COBRO",
            "message": f"Favor [{favor_id}] registrado con la facción '{faction_name}' ({favor_value}). Origen: {origin}."
        }

    @staticmethod
    def claim_favor(favor_id: str, faction_name: str) -> Dict[str, Any]:
        """
        Cobra un favor adeudado para obtener recursos, inmunidad o información.
        """
        return {
            "favor_id": favor_id,
            "faction_name": faction_name,
            "status": "COBRADO",
            "message": f"Favor [{favor_id}] cobrado exitosamente ante '{faction_name}'. La obligación ha sido saldada."
        }
