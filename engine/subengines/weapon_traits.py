"""
WH40K Weapon Traits & Physical Status Engine (weapon_traits.py)
Catálogo oficial de armas, rasgos de combate (Perforante, Toxina, Sobrecalentamiento, Área), estados físicos y fichas técnicas completas.
"""

import random
from typing import Dict, List, Any

WEAPON_CATALOG = {
    "PISTOLA_BOLTER": {
        "nombre": "Pistola Bólter Patrón Lokii",
        "tipo": "Balística Pesada / Armamento Inquisitorial",
        "dano_base": 7,
        "ap": 2,
        "cadencia": "Semiautomática",
        "capacidad_cargador": 12,
        "rasgos": ["PERFORANTE_2", "IMPACTO_REDUCCIÓN", "PROYECTIL_EXPLOSIVO"],
        "estado": "LIMPIA",
        "descripcion": "Bólter de puño con chasis reforzado de ferroacero y cargador recto de 12 proyectiles reactivos de masa."
    },
    "ESPADA_ENERGIA": {
        "nombre": "Espada de Energía Monomolecular",
        "tipo": "Cuerpo a Cuerpo de Energía",
        "dano_base": 6,
        "ap": 4,
        "cadencia": "Cuerpo a Cuerpo",
        "capacidad_cargador": None,
        "rasgos": ["PERFORANTE_4", "DESINTEGRACIÓN", "CORTE_LIMPIO"],
        "estado": "LIMPIA",
        "descripcion": "Hoja de acero templado envuelta en un campo de rozamiento disruptor que desintegra la materia a nivel molecular."
    },
    "RIFLE_PLASMA": {
        "nombre": "Rifle de Plasma de Submundo Patrón Ryza",
        "tipo": "Energía Térmica de Gran Calibre",
        "dano_base": 9,
        "ap": 4,
        "cadencia": "Individual / Sobrecarga",
        "capacidad_cargador": 10,
        "rasgos": ["PERFORANTE_4", "SOBRECALENTAMIENTO", "DESINTEGRACIÓN"],
        "estado": "LIMPIA",
        "descripcion": "Arma de energía solar comprimida. El plasma incandescente derrite armaduras pesadas y cubiertas de acero."
    },
    "CUCHILLO_TOXINA": {
        "nombre": "Cuchillo de Toxina Escher",
        "tipo": "Cuerpo a Cuerpo Químico",
        "dano_base": 4,
        "ap": 1,
        "cadencia": "Cuerpo a Cuerpo",
        "capacidad_cargador": None,
        "rasgos": ["TOXINA_PARALIZANTE", "SILENCIOSA"],
        "estado": "LIMPIA",
        "descripcion": "Daga de aleación liviana con microconductos inyectores de neurotoxina paralizante fabricada en los laboratorios Escher."
    },
    "ESCOPETA_ASALTO": {
        "nombre": "Escopeta de Asalto Enforcer Patrón Sanctis",
        "tipo": "Proyectil Pesado de Dispersión",
        "dano_base": 6,
        "ap": 1,
        "cadencia": "Ráfaga Corta",
        "capacidad_cargador": 8,
        "rasgos": ["DISPERSIÓN", "IMPACTO_CONTUNDENTE"],
        "estado": "LIMPIA",
        "descripcion": "Escopeta antimotines de cañón recortado utilitaria empleada por los Palatine Enforcers para control de masas."
    }
}

class WeaponTraitsEngine:

    @staticmethod
    def get_weapon_dossier(weapon_key: str) -> Dict[str, Any]:
        """
        Devuelve el expediente técnico completo de un arma con sus características, rasgos y munición.
        """
        weapon = WEAPON_CATALOG.get(weapon_key.upper(), WEAPON_CATALOG["PISTOLA_BOLTER"])
        
        cargador_str = f"{weapon['capacidad_cargador']} cartuchos" if weapon['capacidad_cargador'] is not None else "Infinito / C-a-C"
        rasgos_str = ", ".join(weapon["rasgos"])

        formatted_text = (
            f"--- [REGISTRO TÉCNICO DE ARMA - WH40K] ---\n"
            f"Arma: {weapon['nombre']}\n"
            f"Tipo: {weapon['tipo']}\n"
            f"Daño Base: {weapon['dano_base']} | Penetración (AP): {weapon['ap']}\n"
            f"Cadencia: {weapon['cadencia']}\n"
            f"Capacidad de Cargador: {cargador_str} | Estado: {weapon['estado']}\n"
            f"Rasgos Especiales: [{rasgos_str}]\n"
            f"Descripción: {weapon['descripcion']}\n"
            f"-------------------------------------------"
        )

        return {
            "weapon_key": weapon_key,
            "dossier": weapon,
            "formatted_text": formatted_text
        }

    @staticmethod
    def process_weapon_attack(weapon_key: str, current_ammo: int, current_status: str, roll_result: Dict[str, Any], target_resilience: int = 3) -> Dict[str, Any]:
        weapon = WEAPON_CATALOG.get(weapon_key, WEAPON_CATALOG["PISTOLA_BOLTER"])
        
        if current_status == "ENCASQUILLADA":
            return {
                "attack_executed": False,
                "damage_dealt": 0,
                "new_status": "ENCASQUILLADA",
                "ammo_remaining": current_ammo,
                "message": f"¡CLICK! El arma {weapon['nombre']} está ENCASQUILLADA. Requiere 1 PA para limpiar el mecanismo."
            }
        elif current_status == "SOBRECALENTADA":
            return {
                "attack_executed": False,
                "damage_dealt": 0,
                "new_status": "SOBRECALENTADA",
                "ammo_remaining": current_ammo,
                "message": f"¡ALERTA TÉRMICA! El arma {weapon['nombre']} está SOBRECALENTADA. Debe enfriarse durante 1 ronda."
            }

        if weapon["capacidad_cargador"] is not None:
            if current_ammo <= 0:
                return {
                    "attack_executed": False,
                    "damage_dealt": 0,
                    "new_status": "SIN_MUNICIÓN",
                    "ammo_remaining": 0,
                    "message": f"¡SIN MUNICIÓN! El cargador de {weapon['nombre']} está vacío."
                }
            new_ammo = current_ammo - 1
        else:
            new_ammo = current_ammo

        d100 = roll_result.get("d100_val", 50)
        if "SOBRECALENTAMIENTO" in weapon["rasgos"] and d100 >= 90:
            return {
                "attack_executed": True,
                "damage_dealt": 0,
                "new_status": "SOBRECALENTADA",
                "ammo_remaining": new_ammo,
                "user_damage": 3,
                "message": f"¡CRÍTICO TÉRMICO! {weapon['nombre']} se sobrecalentó y causó 3 de daño térmico a Alexander."
            }

        if weapon["capacidad_cargador"] is not None and d100 >= 96:
            return {
                "attack_executed": False,
                "damage_dealt": 0,
                "new_status": "ENCASQUILLADA",
                "ammo_remaining": new_ammo,
                "message": f"¡FALLO DE MECANISMO! {weapon['nombre']} se encasquilló durante la expulsión del casquillo."
            }

        if roll_result.get("resultado_base") == "FALLO":
            return {
                "attack_executed": True,
                "damage_dealt": 0,
                "new_status": current_status,
                "ammo_remaining": new_ammo,
                "message": f"El ataque con {weapon['nombre']} falló sin causar impacto."
            }

        ap = weapon["ap"]
        base_damage = weapon["dano_base"]
        degrees = roll_result.get("grados_num", 0)

        effective_armor = max(0, target_resilience - ap)
        damage_dealt = max(1, (base_damage + degrees) - effective_armor)

        toxin_triggered = False
        if "TOXINA_PARALIZANTE" in weapon["rasgos"]:
            toxin_triggered = True

        return {
            "attack_executed": True,
            "damage_dealt": damage_dealt,
            "new_status": current_status,
            "ammo_remaining": new_ammo,
            "traits_applied": weapon["rasgos"],
            "toxin_triggered": toxin_triggered,
            "message": f"¡IMPACTO DE {weapon['nombre'].upper()}! Daño infligido: {damage_dealt} (Penetración AP {ap} redujo armadura a {effective_armor}). Rasgos activos: {', '.join(weapon['rasgos'])}."
        }

    @staticmethod
    def unjam_weapon(weapon_name: str) -> Dict[str, Any]:
        return {
            "status": "LIMPIA",
            "cost_pa": 1,
            "message": f"Se ha tirado del cerrojo de {weapon_name} y extraído el casquillo atascado. Arma limpia y lista para disparar."
        }


    @staticmethod
    def resolve_attack_with_traits(weapon_key: str, is_success: bool, target_resilience: int = 3) -> Dict[str, Any]:
        roll_mock = {"resultado_base": "ÉXITO" if is_success else "FALLO"}
        return WeaponTraitsEngine.process_weapon_attack(weapon_key, 12, "LIMPIA", roll_mock, target_resilience)
