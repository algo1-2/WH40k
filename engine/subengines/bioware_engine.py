"""
WH40K Bioware, Surgery, Cybernetics & Trauma Engine v2.0 (bioware_engine.py)
Incluye:
- Diagnóstico anatómico zonal (Cabeza, Tórax, Abdomen, Extremidades)
- Simulador de Cirugías en 4 Fases Clínicas
- Fabricación de Implantes Cibernéticos y Prótesis Mecatrónicas de Khepra-9
"""

import random
from typing import Dict, List, Any

ANATOMICAL_ZONES = {
    "CABEZA": {
        "nombre": "Cráneo & Red Neural",
        "trauma_default": "Conmoción / Presión Intracraneal",
        "procedures": ["TREPANACION_DESCOMPRESION", "NEURO_ESTIMULACION"]
    },
    "TORAX": {
        "nombre": "Caja Torácica & Pulmones",
        "trauma_default": "Perforación Pleural / Hemorragia Interna",
        "procedures": ["TORACICA", "PERFUSION_TISULAR"]
    },
    "ABDOMEN": {
        "nombre": "Abdomen & Vísceras",
        "trauma_default": "Laceración Esplénica / Shock Hipovolémico",
        "procedures": ["SUTURA_MAYOR", "INFUSION_SHOCK"]
    },
    "BRAZO_IZQ": {
        "nombre": "Brazo Izquierdo",
        "trauma_default": "Fractura Expuesta / Amputación Traumática",
        "procedures": ["INJERTO_TISULAR", "INSTALACION_BIONICA"]
    },
    "BRAZO_DER": {
        "nombre": "Brazo Derecho",
        "trauma_default": "Desgarro Muscular Profundo",
        "procedures": ["INJERTO_TISULAR", "INSTALACION_BIONICA"]
    },
    "PIERNAS": {
        "nombre": "Extremidades Inferiores",
        "trauma_default": "Impacto de Metralla / Pérdida de Movilidad",
        "procedures": ["EXTRACCION_METRALLA", "SUTURA_MAYOR"]
    }
}

CYBERNETICS_CATALOG = {
    "BRAZO_BIONICO_MECANICO": {
        "nombre": "Prótesis Mecatrónica de Brazo Industrial (Khepra-9)",
        "cost_credits": 90,
        "materials": "1 Servo-articulador + 2 Placas de acero",
        "bonus": "+10 a Fuerza, +1d5 daño en combate desarmado y permite reparar al 2º deudor",
        "recipient": "Jarek Venn / Deudor de Sombra"
    },
    "OJO_BIONICO_AUSPEX": {
        "nombre": "Ojo Biónico con Visor Auspex Retiniano",
        "cost_credits": 120,
        "materials": "1 Micro-lente + 1 Circuito óptico",
        "bonus": "+15 a Percepción visual, visión térmica e inmunidad al deslumbramiento",
        "recipient": "Severan Holt / Alexander"
    },
    "FILTRO_PULMONAR_TOX": {
        "nombre": "Filtro Respiratorio Biomecánico Anti-Tox",
        "cost_credits": 80,
        "materials": "1 Membrana filtrante + 2 Válvulas de latón",
        "bonus": "Inmunidad total a gases venenosos, humo de combate y asfixia en sumideros",
        "recipient": "Cualquier miembro del séquito"
    },
    "SUBDERMO_BLINDAJE": {
        "nombre": "Placas de Subdermo-Blindaje de Aleación",
        "cost_credits": 150,
        "materials": "4 Placas de polímero denso + Suturas de titanio",
        "bonus": "+1 Punto de Armadura permanente en todas las localizaciones corporales",
        "recipient": "Severan Holt / Jarek Venn"
    }
}

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
    },
    "PERFUSION_TISULAR": {
        "nombre": "Mantenimiento de Perfusión Tisular & Desintubación (Quartus)",
        "base_target": 70,
        "pv_recovered": 3,
        "consumes": "1 Ampolla neuro-sedante + Solución oxigenada"
    },
    "INSTALACION_BIONICA": {
        "nombre": "Implante & Sincronización Neural de Prótesis Biónica",
        "base_target": 65,
        "pv_recovered": 2,
        "consumes": "1 Conector bio-sináptico + Anestesia espinal"
    }
}

class BiowareEngine:

    @staticmethod
    def get_anatomical_status(patient_name: str) -> Dict[str, Any]:
        if "Quartus" in patient_name:
            return {
                "patient": "Quartus Holt",
                "vital_hp": "4 / 11",
                "status": "Coma / Perfusión Tisular Activa",
                "zones": {
                    "CABEZA": {"status": "ESTABLE", "damage": 0, "condition": "Sedación controlada"},
                    "TORAX": {"status": "CRÍTICO", "damage": 6, "condition": "Perforación torácica profunda por proyectil"},
                    "ABDOMEN": {"status": "MODERADO", "damage": 1, "condition": "Laceración superficial"},
                    "BRAZO_IZQ": {"status": "ESTABLE", "damage": 0, "condition": "Línea IV insertada"},
                    "BRAZO_DER": {"status": "ESTABLE", "damage": 0, "condition": "Monitores de pulso"},
                    "PIERNAS": {"status": "ESTABLE", "damage": 0, "condition": "Perfusión normal"}
                }
            }
        elif "Tertius" in patient_name:
            return {
                "patient": "Tertius Holt",
                "vital_hp": "8 / 11",
                "status": "Consciente / Drenaje Activo",
                "zones": {
                    "CABEZA": {"status": "ESTABLE", "damage": 0, "condition": "Alerta y orientado"},
                    "TORAX": {"status": "MODERADO", "damage": 3, "condition": "Drenaje intercostal funcionando"},
                    "ABDOMEN": {"status": "ESTABLE", "damage": 0, "condition": "Normal"},
                    "BRAZO_IZQ": {"status": "ESTABLE", "damage": 0, "condition": "Normal"},
                    "BRAZO_DER": {"status": "LEVE", "damage": 1, "condition": "Contusión por retroceso"},
                    "PIERNAS": {"status": "ESTABLE", "damage": 0, "condition": "Reposo"}
                }
            }
        else:
            return {
                "patient": patient_name,
                "vital_hp": "5 / 10",
                "status": "Urgencia Clandestina",
                "zones": {
                    "CABEZA": {"status": "LEVE", "damage": 1, "condition": "Contusión"},
                    "TORAX": {"status": "MODERADO", "damage": 2, "condition": "Herida de esquirlas"},
                    "ABDOMEN": {"status": "LEVE", "damage": 1, "condition": "Impacto amortiguado"},
                    "BRAZO_IZQ": {"status": "ESTABLE", "damage": 0, "condition": "Normal"},
                    "BRAZO_DER": {"status": "ESTABLE", "damage": 0, "condition": "Normal"},
                    "PIERNAS": {"status": "LEVE", "damage": 1, "condition": "Rozadura de bala"}
                }
            }

    @staticmethod
    def craft_cybernetic(implant_key: str, available_credits: int, tech_skill: int = 65) -> Dict[str, Any]:
        implant = CYBERNETICS_CATALOG.get(implant_key.upper())
        if not implant:
            return {"success": False, "error": f"Implante '{implant_key}' no encontrado en el catálogo."}
        
        cost = implant["cost_credits"]
        if available_credits < cost:
            return {"success": False, "error": f"Créditos insuficientes ({available_credits} ¤ disponibles, requiere {cost} ¤)."}
        
        roll = random.randint(1, 100)
        target = tech_skill + 10 # Bono por banco mecatrónico de Rho-9
        is_success = roll <= target
        degrees = abs((target - roll) // 10)
        
        new_credits = available_credits - cost
        return {
            "success": is_success,
            "implant_key": implant_key,
            "name": implant["nombre"],
            "recipient": implant["recipient"],
            "bonus": implant["bonus"],
            "spent_credits": cost,
            "remaining_credits": new_credits,
            "roll": roll,
            "target": target,
            "degrees": degrees,
            "message": f"⚙️ ¡FABRICACIÓN {'EXITOSA' if is_success else 'DEFECTUOSA'}! Khepra-9 ensambló '{implant['nombre']}'. Tirada: {roll} vs {target} ({degrees} Grados). Bono: {implant['bonus']}"
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
