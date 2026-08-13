"""
WH40K NPC Generator Engine (npc_generator.py)
Generador determinista de PNJ y Enemigos con estadísticas de Salud, WS/BS, Armadura, Daño, Moral y Habilidades Especiales.
"""

from typing import Dict, List, Any
import random

class NPCGenerator:

    NPC_TEMPLATES = {
        # IMPERIUM OF MAN
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
        },
        "GUARDIA_IMPERIAL": {
            "nombre": "Guardián Imperial de Línea",
            "salud": 10, "ws": 35, "bs": 40, "armadura": 3, "dano": "1d10+2",
            "arma": "Rifle Láser M36", "moral": 50,
            "rasgo": "Disciplina de Pelotón (+10% BS en formación)"
        },
        "COMISARIO": {
            "nombre": "Comisario de Campo",
            "salud": 18, "ws": 50, "bs": 50, "armadura": 4, "dano": "1d10+4",
            "arma": "Pistola de Plasma / Espada de Energía", "moral": 90,
            "rasgo": "Ejecución Sumaria (Reinicia la moral del pelotón)"
        },
        "OGRYN": {
            "nombre": "Ogryn de Choque",
            "salud": 35, "ws": 55, "bs": 20, "armadura": 5, "dano": "2d10+4",
            "arma": "Ripper Gun en Melé", "moral": 60,
            "rasgo": "Cuerpo Robusto (-2 al daño recibido)"
        },
        "ASTARTES": {
            "nombre": "Space Marine Astartes",
            "salud": 40, "ws": 65, "bs": 65, "armadura": 9, "dano": "2d10+6",
            "arma": "Bólter Pesado Modelo Godwyn", "moral": 95,
            "rasgo": "Servonúcleo, Voluntad 75%, Implantes Astartes"
        },
        "INTERCESSOR": {
            "nombre": "Space Marine Intercessor",
            "salud": 35, "ws": 60, "bs": 60, "armadura": 8, "dano": "2d10+4",
            "arma": "Rifle Bólter Boltstorm", "moral": 90,
            "rasgo": "Códice de Batalla (+10% disciplina, inmune a miedos)"
        },
        "TERMINATOR": {
            "nombre": "Terminator de Asalto Astartes",
            "salud": 50, "ws": 70, "bs": 65, "armadura": 11, "dano": "2d10+8",
            "arma": "Martillo del Trueno / Escudo de Tormenta", "moral": 95,
            "rasgo": "Escudo de Tormenta (+3 Armadura Invulnerable)"
        },
        "CUSTODES": {
            "nombre": "Custodian Guard",
            "salud": 65, "ws": 75, "bs": 75, "armadura": 12, "dano": "2d10+8",
            "arma": "Lanza Guardiana de Plasma", "moral": 100,
            "rasgo": "Aegis del Emperador (Invulnerable 4+ a psíquica)"
        },
        "SISTER_OF_SILENCE": {
            "nombre": "Sister of Silence Vigilator",
            "salud": 25, "ws": 65, "bs": 60, "armadura": 6, "dano": "2d10+5",
            "arma": "Mandoble de Ejecución", "moral": 90,
            "rasgo": "Aura de Paria Nula (Anula poderes psíquicos en 15m)"
        },
        "VINDICARE": {
            "nombre": "Asesino Vindicare",
            "salud": 25, "ws": 50, "bs": 90, "armadura": 4, "dano": "3d10+6",
            "arma": "Rifle de Francotirador Exitus", "moral": 95,
            "rasgo": "Disparo Exitus (Ignora invulnerables y escudos)"
        },

        # CHAOS
        "CHAOS_MARINE": {
            "nombre": "Legionario Traidor de la Black Legion",
            "salud": 38, "ws": 65, "bs": 60, "armadura": 8, "dano": "2d10+5",
            "arma": "Bólter Traidor", "moral": 85,
            "rasgo": "Furia del Caos (Repite daño fallido en asalto)"
        },
        "BERSERKER": {
            "nombre": "Berserker de Khorne",
            "salud": 42, "ws": 75, "bs": 30, "armadura": 8, "dano": "2d10+7",
            "arma": "Hacha de Cadena Dientediablo", "moral": 100,
            "rasgo": "¡Sangre para el Dios de la Sangre! (Ataca al morir)"
        },
        "PLAGUE_MARINE": {
            "nombre": "Plague Marine de Nurgle",
            "salud": 50, "ws": 55, "bs": 55, "armadura": 9, "dano": "2d10+4",
            "arma": "Lanza-plagas / Espada Infecta", "moral": 90,
            "rasgo": "Disgustosamente Resistente (Sana 1d10/turno)"
        },
        "BLOODLETTER": {
            "nombre": "Bloodletter de Khorne",
            "salud": 20, "ws": 65, "bs": 0, "armadura": 4, "dano": "2d10+6",
            "arma": "Espada de Sangre", "moral": 100,
            "rasgo": "Espada Decapitadora (Crítico 1-10 en d100)"
        },

        # XENOS
        "NECRON_GUERRERO": {
            "nombre": "Guerrero Necrón",
            "salud": 25, "ws": 40, "bs": 50, "armadura": 6, "dano": "2d10+4",
            "arma": "Blaster Gauss de Desintegración", "moral": 100,
            "rasgo": "Protocolo de Autorreparación (1d10 Salud/turno)"
        },
        "LYCHGUARD": {
            "nombre": "Lychguard Necrón",
            "salud": 45, "ws": 70, "bs": 40, "armadura": 10, "dano": "2d10+7",
            "arma": "Espada Hiperfásica / Escudo de Dispersión", "moral": 100,
            "rasgo": "Reflejo de Dispersión (Devuelve disparos)"
        },
        "ORK_BOY": {
            "nombre": "Ork Boy / Pez de Asalto",
            "salud": 20, "ws": 50, "bs": 25, "armadura": 3, "dano": "2d10+3",
            "arma": "Choppa Pesada y Pistola Pipaz", "moral": 60,
            "rasgo": "Furia Waaagh! (+10 WS si ataca en grupo)"
        },
        "ORK_NOB": {
            "nombre": "Ork Nob en Mega-Armadura",
            "salud": 45, "ws": 65, "bs": 30, "armadura": 10, "dano": "3d10+6",
            "arma": "Garra de Combate Orka", "moral": 85,
            "rasgo": "Cabeza Dura (Reduce daño de armas ligeras a la mitad)"
        },
        "TAU_GUERRERO": {
            "nombre": "Guerrero de la Casta del Fuego T'au",
            "salud": 12, "ws": 25, "bs": 50, "armadura": 4, "dano": "1d10+5",
            "arma": "Rifle de Pulso T'au", "moral": 65,
            "rasgo": "Marcador Táctico (+15% BS si fue marcado)"
        },
        "KROOT": {
            "nombre": "Kroot Carnivore",
            "salud": 14, "ws": 55, "bs": 40, "armadura": 2, "dano": "1d10+4",
            "arma": "Rifle Kroot con Cuchilla", "moral": 60,
            "rasgo": "Devorador Fisiológico (Regenera salud al matar)"
        },
        "VOTANN_HEARTHKYN": {
            "nombre": "Hearthkyn Warrior (Kin)",
            "salud": 18, "ws": 45, "bs": 50, "armadura": 6, "dano": "1d10+4",
            "arma": "Bolter Autarca Kin", "moral": 85,
            "rasgo": "Rencor Registrado (+10% tiradas contra enemigos marcados)"
        }
    }

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
