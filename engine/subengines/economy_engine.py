"""
WH40K Necromunda Credits & Black Market Economy Engine (economy_engine.py)
Transacciones financieras en Créditos de Necromunda y comercio en Dust Falls.
"""

from typing import Dict, List, Any

ITEM_PRICES = {
    "CARGA_MEDIKIT": 50,
    "MUNICION_BOLTER": 75,
    "CELULA_PLASMA": 150,
    "STIMM_COMBATE": 60,
    "IMPLANTE_BIONICO": 350
}

class EconomyEngine:

    @staticmethod
    def buy_item(item_key: str, current_credits: int) -> Dict[str, Any]:
        price = ITEM_PRICES.get(item_key, 100)
        
        if current_credits < price:
            return {
                "transaction": "RECHAZADA",
                "reason": f"Créditos insuficientes. Se requerían {price} Créditos de Necromunda, pero solo se disponen de {current_credits}.",
                "remaining_credits": current_credits
            }

        new_total = current_credits - price
        return {
            "transaction": "EXITOSA",
            "item_bought": item_key,
            "price_paid": price,
            "remaining_credits": new_total,
            "message": f"¡COMPRA EXITOSA! Se adquirió '{item_key}' por {price} Créditos de Necromunda. Saldo restante: {new_total} Créditos."
        }

    @staticmethod
    def add_credits(current_credits: int, amount: int, source: str) -> Dict[str, Any]:
        new_total = current_credits + amount
        return {
            "transaction": "ABONO",
            "amount_added": amount,
            "source": source,
            "new_total_credits": new_total,
            "message": f"Se abonaron +{amount} Créditos de Necromunda por '{source}'. Nuevo saldo: {new_total} Créditos."
        }
