"""
WH40K NPC Generator Engine (npc_generator.py)
Generador determinista de PNJ y Pacientes Clandestinos de Trauma.
"""

from typing import Dict, List, Any
import random

class NPCGenerator:

    NPC_TEMPLATES = {
        "PANDILLERO": {
            "nombre": "Pandillero de Submundo",
            "salud": 10, "ws": 35, "bs": 35, "armadura": 2, "dano": "1d10+2",
            "arma": "Pistola Autógena Clandestina", "moral": 40,
            "rasgo": "Miedo a la Oscuridad (-10 a tiradas en penumbra)"
        },
        "ENFORCER": {
            "nombre": "Enforcer Palatino",
            "salud": 15, "ws": 45, "bs": 45, "armadura": 5, "dano": "1d10+4",
            "arma": "Escopeta de Disuasión o Escudo Antimotines", "moral": 70,
            "rasgo": "Formación Antimotines (+2 armadura en escuadra)"
        }
    }

    PATIENT_NAMES = [
        "Vael 'Dedos-Rotos' Karr", "Ilyana Vex", "Borr 'El Yunque' Horgan",
        "Corrin Thorne", "Lysa Var", "Darek 'Ceniza' Mal", "Kira Voss",
        "Titus 'Sombra' Vance", "Marek Rann", "Sylas 'Ojo-Muerto' Vane"
    ]

    PATIENT_PROFILES = [
        {
            "faction": "Contrabandista de Casa Escher",
            "trauma": "Quemadura cáustica por ácido industrial en torso y brazo izquierdo",
            "salud": "2 / 10 (Crítico)",
            "hp_curr": 2, "hp_max": 10,
            "recompensa": "140 Créditos + 1 Frasco de Estimulante Puro",
            "riesgo": "Vapores químicos volátiles en la herida; requiere extractor de aire."
        },
        {
            "faction": "Obrero Fugitivo de Calderas (Orstag)",
            "trauma": "Impacto de esquirla de caldera a presión en cavidad pleural",
            "salud": "3 / 11 (Grave)",
            "hp_curr": 3, "hp_max": 11,
            "recompensa": "95 Créditos + 2 Placas de Aleación Pesada",
            "riesgo": "Hipotermia progresiva si no se le suministra calor en 30 minutos."
        },
        {
            "faction": "Sicario del Mercado Negro",
            "trauma": "Herida de bala de punta hueca alojada en abdomen",
            "salud": "1 / 9 (Crítico Inminente)",
            "hp_curr": 1, "hp_max": 9,
            "recompensa": "210 Créditos + Mapa de Depósitos de Dust Falls",
            "riesgo": "Dos cazarrecompensas están siguiendo su rastro de sangre en el callejón."
        },
        {
            "faction": "Informante Clandestino de Delaque",
            "trauma": "Neurotoxina paralizante inoculada en el torrente sanguíneo",
            "salud": "4 / 10 (Intoxicación Severa)",
            "hp_curr": 4, "hp_max": 10,
            "recompensa": "120 Créditos + Frecuencia Vox de Patrulla Enforcer",
            "riesgo": "Paro respiratorio en 2 turnos si no recibe un antídoto o intubación."
        }
    ]

    @staticmethod
    def generate_npc(npc_type: str, custom_name: str = None) -> Dict[str, Any]:
        template = NPCGenerator.NPC_TEMPLATES.get(npc_type.upper(), NPCGenerator.NPC_TEMPLATES["PANDILLERO"])
        return {
            "npc_id": f"NPC-{hash(custom_name or template['nombre']) % 100000:05d}",
            "nombre": custom_name or template["nombre"],
            "tipo": npc_type.upper(),
            "salud_actual": template["salud"],
            "salud_maxima": template["salud"],
            "ws": template["ws"],
            "bs": template["bs"],
            "armadura": template["armadura"],
            "dano": template["dano"],
            "arma": template["arma"],
            "moral": template["moral"],
            "rasgo_especial": template["rasgo"]
        }

    @classmethod
    def generate_clandestine_patient(cls) -> Dict[str, Any]:
        name = random.choice(cls.PATIENT_NAMES)
        profile = random.choice(cls.PATIENT_PROFILES)
        return {
            "patient_id": f"PATIENT-{hash(name + profile['trauma']) % 100000:05d}",
            "name": name,
            "faction": profile["faction"],
            "trauma": profile["trauma"],
            "vital_status": profile["salud"],
            "hp_current": profile["hp_curr"],
            "hp_max": profile["hp_max"],
            "reward_offered": profile["recompensa"],
            "risk_warning": profile["riesgo"],
            "message": f"¡GOLPE EN LA COMPUERTA! '{name}' ({profile['faction']}) solicita auxilio médico urgente."
        }
