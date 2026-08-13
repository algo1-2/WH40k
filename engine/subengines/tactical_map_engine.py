"""
WH40K Tactical Map & Position Simulator Engine (tactical_map_engine.py)
Simulador de posicionamiento por zonas, coberturas (Ligera/Pesada/Inmaterial) y flanqueos tácticos.
"""

from typing import Dict, List, Any

COVER_TYPES = {
    "NINGUNA": {"bonus_esquiva": 0, "reduccion_dano": 0, "descripcion": "Sin cobertura. Expuesto en campo abierto."},
    "LIGERA": {"bonus_esquiva": 10, "reduccion_dano": 1, "descripcion": "Cobertura ligera (Barricada de madera, escombros leves)."},
    "PESADA": {"bonus_esquiva": 20, "reduccion_dano": 2, "descripcion": "Cobertura pesada (Plancha de ferroacero, columna gótica)."},
    "INMATERIAL": {"bonus_esquiva": 30, "reduccion_dano": 3, "descripcion": "Materialización parcial en el Umbral (Paso Sombrío R2)."}
}

class TacticalMapEngine:

    @staticmethod
    def initialize_tactical_grid() -> Dict[str, Any]:
        """
        Inicializa una grilla táctica de 3 zonas para combate en la Clínica Rho-9 o subniveles.
        """
        return {
            "zonas": {
                "ZONA_A_QUIRÓFANO": {
                    "nombre": "Zona A: Quirófano y Núcleo de Rho-9",
                    "coberturas_disponibles": ["PESADA", "INMATERIAL"],
                    "unidades_presentes": ["Alexander (En Cobertura Pesada)", "Syra Kol"]
                },
                "ZONA_B_PASILLO": {
                    "nombre": "Zona B: Pasillo de Acceso Principal",
                    "coberturas_disponibles": ["LIGERA"],
                    "unidades_presentes": ["Severan Holt (Guardia de Flanqueo)", "Halven Rusk"]
                },
                "ZONA_C_ELEVADA": {
                    "nombre": "Zona C: Passarela y Conductos Elevados",
                    "coberturas_disponibles": ["LIGERA", "PESADA"],
                    "unidades_presentes": ["Hostiles / Francotiradores"]
                }
            },
            "message": "Grilla táctica inicializada. Zonas A (Quirófano), B (Pasillo) y C (Conductos Elevados) activas."
        }

    @staticmethod
    def evaluate_tactical_shot(attacker_zone: str, target_zone: str, target_cover: str, attacker_elevated: bool = False, target_flanked: bool = False) -> Dict[str, Any]:
        """
        Calcula bonificadores y penalizaciones tácticas para disparos o asaltos entre zonas.
        """
        cover_info = COVER_TYPES.get(target_cover.upper(), COVER_TYPES["NINGUNA"])
        
        modificadores = []
        # Penalización por Cobertura Objetivo
        if cover_info["bonus_esquiva"] > 0:
            modificadores.append(-cover_info["bonus_esquiva"])

        # Bono por Posición Elevada
        if attacker_elevated:
            modificadores.append(+10)

        # Bono por Flanqueo
        if target_flanked:
            modificadores.append(+15)

        total_mod = sum(modificadores)
        
        return {
            "attacker_zone": attacker_zone,
            "target_zone": target_zone,
            "target_cover": target_cover,
            "cover_effects": cover_info,
            "attacker_elevated": attacker_elevated,
            "target_flanked": target_flanked,
            "net_tactical_modifier": total_mod,
            "message": f"Evaluación Táctica: Modificador neto de disparo/asalto: {total_mod:+d}%. (Cobertura objetivo: {target_cover} [-{cover_info['bonus_esquiva']}%], Elevado: {attacker_elevated} [+10%], Flanqueado: {target_flanked} [+15%])."
        }
