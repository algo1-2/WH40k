"""
WH40K Favors Ledger & Faction Obligations Engine (favors_ledger.py)
Libro Mayor de Favores Pendientes, Deudas Faccionales y Cobros en Necromunda.
"""

from typing import Dict, List, Any

FACTIONS_DATA = [
    {
        "key": "BREN_ORSTAG",
        "name": "Caldereros de Bren Orstag",
        "reputation": 30,
        "stance": "Aliada / Proveedores Industriales",
        "stance_color": "green",
        "favors_available": 2,
        "claimable_perks": [
            {"id": "PERK_BREN_PLATES", "title": "Lote de Blindaje Pesado", "cost_favors": 1, "effect": "+15% resistencia estructural a barricadas de Rho-9."},
            {"id": "PERK_BREN_FUEL", "title": "Carga Extraordinaria de Prometio", "cost_favors": 1, "effect": "Rellena los tanques de plasma al 100% de capacidad."}
        ]
    },
    {
        "key": "BLACK_MARKET",
        "name": "Mercado Negro de Dust Falls",
        "reputation": 25,
        "stance": "Comercial / Venta Clandestina",
        "stance_color": "green",
        "favors_available": 1,
        "claimable_perks": [
            {"id": "PERK_MK_AMMO", "title": "Cajón de Munición Filtrada", "cost_favors": 1, "effect": "+300 proyectiles de diversos calibres entregados a Sombra."},
            {"id": "PERK_MK_DOCS", "title": "Identidades Falsas de Trabajador", "cost_favors": 1, "effect": "Reduce la atención de los Enforcers en un 20%."}
        ]
    },
    {
        "key": "ESCHER",
        "name": "Casa Escher (Distribución Farmacéutica)",
        "reputation": 15,
        "stance": "Tratado Comercial / Intercambio de Químicos",
        "stance_color": "green",
        "favors_available": 1,
        "claimable_perks": [
            {"id": "PERK_ESCHER_STIMMS", "title": "Cofre de Quimio-Estimulantes", "cost_favors": 1, "effect": "+12 Dosis de analgésicos de grado quirúrgico."},
            {"id": "PERK_ESCHER_ANTIDOTE", "title": "Fórmula Maestra de Contraveneno", "cost_favors": 1, "effect": "Añade +15% a tiradas de síntesis de antídotos."}
        ]
    },
    {
        "key": "WATER_GUILD",
        "name": "Gremio del Agua (Nautican)",
        "reputation": 0,
        "stance": "Neutral Estricto / Comercio Regulado",
        "stance_color": "amber",
        "favors_available": 0,
        "claimable_perks": [
            {"id": "PERK_WATER_RATION", "title": "Entrega de Cisterna Sellada (40L)", "cost_favors": 1, "effect": "Añade +40 botellas de agua purificada a la despensa."}
        ]
    },
    {
        "key": "ENFORCERS",
        "name": "Enforcers Palatinos (Nodo D-17)",
        "reputation": -10,
        "stance": "Vigilancia Tensa / Investigación Abierta",
        "stance_color": "amber",
        "favors_available": 1,
        "claimable_perks": [
            {"id": "PERK_ENFORCER_BRIBE", "title": "Desvío de Patrullas por Soborno", "cost_favors": 1, "effect": "Congela cualquier redada o investigación hacia Rho-9 durante 48 horas."}
        ]
    },
    {
        "key": "DELAQUE",
        "name": "Casa Delaque (Vigilancia de Sombras)",
        "reputation": -20,
        "stance": "Sospecha / Interceptación Pasiva",
        "stance_color": "crimson",
        "favors_available": 0,
        "claimable_perks": [
            {"id": "PERK_DELAQUE_SECRETS", "title": "Dossier de Inteligencia del Submundo", "cost_favors": 1, "effect": "Revela planes de bandas rivales antes de que actúen."}
        ]
    }
]

class FavorsLedgerEngine:

    _factions = list(FACTIONS_DATA)

    @classmethod
    def get_factions_status(cls) -> List[Dict[str, Any]]:
        return cls._factions

    @classmethod
    def claim_favor(cls, faction_key: str, perk_id: str) -> Dict[str, Any]:
        fac = next((f for f in cls._factions if f["key"] == faction_key), None)
        if not fac:
            return {"success": False, "error": f"Facción '{faction_key}' no encontrada."}
        
        perk = next((p for p in fac["claimable_perks"] if p["id"] == perk_id), None)
        if not perk:
            return {"success": False, "error": f"Beneficio '{perk_id}' no encontrado en la facción."}
        
        if fac["favors_available"] < perk["cost_favors"]:
            return {"success": False, "error": f"Favores insuficientes con '{fac['name']}' (Disponibles: {fac['favors_available']}, Requeridos: {perk['cost_favors']})."}
        
        fac["favors_available"] -= perk["cost_favors"]
        return {
            "success": True,
            "faction_name": fac["name"],
            "perk_title": perk["title"],
            "effect": perk["effect"],
            "remaining_favors": fac["favors_available"],
            "message": f"¡FAVOR RECLAMADO CON ÉXITO! {fac['name']} ha entregado: '{perk['title']}'. Efecto: {perk['effect']}"
        }
