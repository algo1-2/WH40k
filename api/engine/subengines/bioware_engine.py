"""
WH40K Bioware, Surgery & Critical Wounds Engine (bioware_engine.py)
Gestión de traumas biológicos, heridas críticas, cirugía clandestina en Rho-9 e implantes cibernéticos.
"""

import random
from typing import Dict, List, Any

CRITICAL_WOUNDS_TABLE = [
    {
        "id": "CRIT_CHEST_001",
        "lugar": "Tórax",
        "descripcion": "Perforación intercostal / fragmentos de proyectil. Hemorragia interna tratable.",
        "penalizacion": "-10 a Fuerza y Resistencia hasta estabilización."
    },
    {
        "id": "CRIT_ARM_002",
        "lugar": "Brazo Izquierdo/Derecho",
        "descripcion": "Fractura abierta / daño de tejido. Incapacidad para sostener armas pesadas de dos manos.",
        "penalizacion": "-15 a Cuerpo a Cuerpo y Balística."
    },
    {
        "id": "CRIT_EYE_003",
        "lugar": "Rostro / Ojo",
        "descripcion": "Corte profundo corneal / quemadura de plasma parcial.",
        "penalizacion": "-20 a Percepción visual (compensado parcialmente si usa Visión de Oscuridad R1)."
    },
    {
        "id": "CRIT_LEG_004",
        "lugar": "Pierna / Fémur",
        "descripcion": "Desgarro muscular severo / surco de bala.",
        "penalizacion": "Movimiento reducido a la mitad (2m por 1 PA)."
    }
]

CYBERNETICS_CATALOG = {
    "EYE_BIONIC": {
        "nombre": "Ojo Biónico de Visión Térmica",
        "tipo": "Implante Ocular",
        "bono": "+10 a Percepción y Visión en Infrarrojo",
        "coste_cirugia_cargas": 2
    },
    "ARM_HYDRAULIC": {
        "nombre": "Prótesis de Brazo Hidráulico de Servidor",
        "tipo": "Prótesis Mecánica",
        "bono": "+10 a Fuerza y +1 a Resiliencia en el brazo equipado",
        "coste_cirugia_cargas": 3
    },
    "LUNG_PURIFIER": {
        "nombre": "Filtro de Reaspiración Pulmonar Tox-Clean",
        "tipo": "Implante Pulmonar",
        "bono": "Inmunidad total a gases tóxicos y toxinas del Submundo de Necromunda",
        "coste_cirugia_cargas": 2
    }
}

class BiowareEngine:

    @staticmethod
    def roll_critical_wound(damage_amount: int) -> Dict[str, Any]:
        """
        Determina un trauma biológico crítico ante daño severo.
        """
        wound = random.choice(CRITICAL_WOUNDS_TABLE)
        return {
            "critical_triggered": True,
            "wound": wound,
            "message": f"¡HERIDA CRÍTICA SUFRIDA en {wound['lugar']}! {wound['descripcion']} (Penalización: {wound['penalizacion']})"
        }

    @staticmethod
    def install_cybernetic(cyber_key: str, medic_skill: int = 75) -> Dict[str, Any]:
        """
        Alexander instala una prótesis cibernética en Medicae Station Rho-9.
        """
        cyber = CYBERNETICS_CATALOG.get(cyber_key, CYBERNETICS_CATALOG["EYE_BIONIC"])
        
        # Tirada de cirugía en Rho-9 (Medicina 75)
        d100 = random.randint(1, 100)
        success = d100 <= medic_skill
        
        if success:
            return {
                "surgery_success": True,
                "cybernetic": cyber,
                "d100": d100,
                "threshold": medic_skill,
                "message": f"¡CIRUGÍA EXITOSA! Se ha instalado '{cyber['nombre']}' en Rho-9. Beneficio: {cyber['bono']}."
            }
        else:
            return {
                "surgery_success": False,
                "cybernetic": cyber,
                "d100": d100,
                "threshold": medic_skill,
                "message": f"Complicación en la cirugía de instalación de '{cyber['nombre']}'. Se requiere estabilización médica previa a reintentar."
            }
