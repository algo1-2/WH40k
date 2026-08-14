"""
WH40K Favors Ledger & Faction Obligations Engine v3.0 (favors_ledger.py)
Incluye:
- Matriz de Facciones & Favores
- Bolsa de Contratos Clandestinos
- Tienda del Mercado Negro de Dust Falls (Materiales de Mejora & Reactivos)
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

CLANDESTINE_CONTRACTS = [
    {
        "id": "CONTRACT_ORSTAG_01",
        "faction": "BREN_ORSTAG",
        "faction_name": "Caldereros de Bren Orstag",
        "title": "Suministro de Estimulantes de Asalto",
        "description": "Orstag necesita 3 dosis de Stimm Hiper-Adrenal para su cuadrilla de escolta pesada.",
        "reward_credits": 160,
        "reward_favors": 1,
        "status": "DISPONIBLE"
    },
    {
        "id": "CONTRACT_ESCHER_02",
        "faction": "ESCHER",
        "faction_name": "Casa Escher",
        "title": "Antídoto Clandestino de Urgencia",
        "description": "Una líder de banda Escher ha sido envenenada por neurotoxina Delaque y requiere neutralización inmediata.",
        "reward_credits": 180,
        "reward_favors": 1,
        "status": "DISPONIBLE"
    },
    {
        "id": "CONTRACT_MARKET_03",
        "faction": "BLACK_MARKET",
        "faction_name": "Mercado Negro de Dust Falls",
        "title": "Extracción y Entrega de Implante Mecatrónico",
        "description": "Un intermediario busca un brazo o conector biónico restaurado por Khepra-9 para un cliente noble del Spire.",
        "reward_credits": 240,
        "reward_favors": 1,
        "status": "DISPONIBLE"
    }
]

BLACK_MARKET_ITEMS = [
    {
        "id": "MAT_TUBING",
        "name": "Tuberías Clínicas & Válvulas de Presión",
        "category": "Material de Mejora",
        "price": 50,
        "effect": "Requisito para mejoras de Quirófano Q-01 y Esterilización E-01"
    },
    {
        "id": "MAT_ALLOY_PLATES",
        "name": "Placas de Aleación de Acero Pesado",
        "category": "Blindaje Estructural",
        "price": 60,
        "effect": "Requisito para blindaje de Compuerta GATE-01 y Taller T-01"
    },
    {
        "id": "MAT_CRYO_TANKS",
        "name": "Tanques Criogénicos de Nitrógeno",
        "category": "Equipo Médico Avanzado",
        "price": 100,
        "effect": "Requisito para Biobanco Celular F-02 y Cama Crítica C-03"
    },
    {
        "id": "MAT_HEPA_FILTERS",
        "name": "Filtros de Flujo Laminar de Grado Militar",
        "category": "Sanidad Hospitalaria",
        "price": 80,
        "effect": "Requisito para Esterilización Nivel 3 y reducción de sepsis al 0%"
    },
    {
        "id": "MAT_PLASMA_CELLS",
        "name": "Batería de Células de Plasma (Carga Completa)",
        "category": "Energía",
        "price": 75,
        "effect": "Recarga el generador de plasma de Rho-9 al 100%"
    }
]

class FavorsLedgerEngine:

    _factions = list(FACTIONS_DATA)
    _contracts = list(CLANDESTINE_CONTRACTS)
    _market = list(BLACK_MARKET_ITEMS)

    @classmethod
    def get_factions_status(cls) -> List[Dict[str, Any]]:
        return cls._factions

    @classmethod
    def get_contracts(cls) -> List[Dict[str, Any]]:
        return cls._contracts

    @classmethod
    def get_market_items(cls) -> List[Dict[str, Any]]:
        return cls._market

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
            "faction": fac["name"],
            "perk_claimed": perk["title"],
            "applied_effect": perk["effect"],
            "favors_remaining": fac["favors_available"],
            "message": f"¡FAVOR COBRADO! Has ejercido tu influencia sobre '{fac['name']}'. Concedido: {perk['title']} ({perk['effect']})."
        }

    @classmethod
    def complete_contract(cls, contract_id: str, current_credits: int) -> Dict[str, Any]:
        c = next((item for item in cls._contracts if item["id"] == contract_id), None)
        if not c:
            return {"success": False, "error": f"Contrato '{contract_id}' no encontrado."}
        
        reward = c["reward_credits"]
        new_credits = current_credits + reward
        
        fac = next((f for f in cls._factions if f["key"] == c["faction"]), None)
        if fac:
            fac["favors_available"] += c.get("reward_favors", 1)
            fac["reputation"] += 5

        c["status"] = "COMPLETADO"

        return {
            "success": True,
            "contract_title": c["title"],
            "faction_name": c["faction_name"],
            "reward_credits": reward,
            "new_credits": new_credits,
            "message": f"🏆 ¡CONTRATO CUMPLIDO! '{c['title']}' para {c['faction_name']}. Recompensa: +{reward} ¤ y +1 Favor ganado."
        }

    @classmethod
    def buy_market_item(cls, item_id: str, current_credits: int) -> Dict[str, Any]:
        item = next((i for i in cls._market if i["id"] == item_id), None)
        if not item:
            return {"success": False, "error": f"Artículo '{item_id}' no disponible en el mercado negro."}
        
        price = item["price"]
        if current_credits < price:
            return {"success": False, "error": f"Créditos insuficientes ({current_credits} ¤ disponibles, requiere {price} ¤)."}
        
        new_credits = current_credits - price
        return {
            "success": True,
            "item_name": item["name"],
            "category": item["category"],
            "price_paid": price,
            "remaining_credits": new_credits,
            "effect": item["effect"],
            "message": f"📦 ¡COMPRA EFECTUADA! Has adquirido '{item['name']}' por {price} ¤. Almacenado en la despensa de Rho-9."
        }
