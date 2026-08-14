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
        "penalizacion": "-20 a Percepción visual."
    },
    {
        "id": "CRIT_LEG_004",
        "lugar": "Pierna / Fémur",
        "descripcion": "Desgarro muscular severo / surco de bala.",
        "penalizacion": "Movimiento reducido a la mitad."
    }
]

SURGERY_PROCEDURES = {
    "TORACICA": {
        "nombre": "Cirugía Torácica Mayor / Drenaje Pleural",
        "base_target": 65,
        "pv_recovered": 3,
        "consumes": "1 Tubo torácico + 2 Vendas + 1 Anestésico local"
    },
    "SUTURA_MAYOR": {
        "nombre": "Desbridamiento & Sutura Antiséptica Profunda",
        "base_target": 75,
        "pv_recovered": 2,
        "consumes": "2 Suturas + 1 Antiséptico + 1 Apósitos"
    },
    "INJERTO_TISULAR": {
        "nombre": "Injerto Biológico de Piel / Reparación Tisular",
        "base_target": 60,
        "pv_recovered": 4,
        "consumes": "1 Muestra de tejido biobanco + 1 Coagulante"
    },
    "INFUSION_SHOCK": {
        "nombre": "Estabilización de Shock Hemorrágico & Transfusión",
        "base_target": 70,
        "pv_recovered": 3,
        "consumes": "1 Unidad Sangre (Biobanco) + 1 Salina IV"
    }
}

class BiowareEngine:

    @staticmethod
    def roll_critical_wound(damage_amount: int) -> Dict[str, Any]:
        wound = random.choice(CRITICAL_WOUNDS_TABLE)
        return {
            "wound_id": wound["id"],
            "lugar": wound["lugar"],
            "descripcion": wound["descripcion"],
            "penalizacion": wound["penalizacion"],
            "damage": damage_amount
        }

    @staticmethod
    def perform_surgery(patient_name: str, procedure_key: str, medic_skill: int = 65, use_diagnostor: bool = True, use_blood: bool = False) -> Dict[str, Any]:
        proc = SURGERY_PROCEDURES.get(procedure_key.upper(), SURGERY_PROCEDURES["SUTURA_MAYOR"])
        
        target = medic_skill + (15 if use_diagnostor else 0) + (10 if use_blood else 0)
        roll = random.randint(1, 100)
        is_success = roll <= target
        degrees = abs((target - roll) // 10)

        pv_gain = proc["pv_recovered"] if is_success else 1
        
        return {
            "success": is_success,
            "patient": patient_name,
            "procedure_name": proc["nombre"],
            "target_skill": target,
            "roll": roll,
            "degrees": degrees,
            "pv_healed": pv_gain,
            "consumables_used": proc["consumes"],
            "message": f"{'✅ CIRUGÍA EXITOSA' if is_success else '⚠️ CIRUGÍA COMPLICADA'}: {patient_name} ha recibido {proc['nombre']}. Tirada: {roll} vs {target} ({degrees} Grados). Recuperados: +{pv_gain} PV."
        }
