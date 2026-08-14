"""
WH40K Bioware, Surgery, Cybernetics & Trauma Engine v3.0 (bioware_engine.py)
Incluye:
- Diagnóstico anatómico zonal (Cabeza, Tórax, Abdomen, Extremidades)
- Simulador de Cirugías Avanzadas con generación de reportes canónicos para ChatGPT
- Fabricación de Implantes Cibernéticos de Khepra-9
"""

import random
from typing import Dict, List, Any

ANATOMICAL_ZONES = {
    "CABEZA": {
        "nombre": "Cráneo & Red Neural",
        "trauma_default": "Conmoción / Presión Intracraneal",
        "procedures": ["TREPANACION_DESCOMPRESION", "ESTIMULACION_NEURAL_COMA"]
    },
    "TORAX": {
        "nombre": "Caja Torácica & Pulmones",
        "trauma_default": "Perforación Pleural / Hemorragia Interna",
        "procedures": ["TORACICA", "PERFUSION_TISULAR", "TRAQUEOTOMIA_EMERGENCIA"]
    },
    "ABDOMEN": {
        "nombre": "Abdomen & Vísceras",
        "trauma_default": "Laceración Esplénica / Shock Hipovolémico",
        "procedures": ["SUTURA_MAYOR", "INFUSION_SHOCK", "EXTRACCION_PARASITOS"]
    },
    "BRAZO_IZQ": {
        "nombre": "Brazo Izquierdo",
        "trauma_default": "Fractura Expuesta / Amputación Traumática",
        "procedures": ["INJERTO_TISULAR", "AMPUTACION_LIMPIA", "INSTALACION_BIONICA"]
    },
    "BRAZO_DER": {
        "nombre": "Brazo Derecho",
        "trauma_default": "Desgarro Muscular Profundo",
        "procedures": ["INJERTO_TISULAR", "AMPUTACION_LIMPIA", "INSTALACION_BIONICA"]
    },
    "PIERNAS": {
        "nombre": "Extremidades Inferiores",
        "trauma_default": "Impacto de Metralla / Pérdida de Movilidad",
        "procedures": ["SUTURA_MAYOR", "EXTRACCION_PARASITOS", "INJERTO_TISULAR"]
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
    "PERFUSION_TISULAR": {
        "nombre": "Mantenimiento de Perfusión Tisular & Desintubación (Quartus)",
        "base_target": 70,
        "pv_recovered": 3,
        "consumes": "1 Ampolla neuro-sedante + Solución oxigenada"
    },
    "TORACICA": {
        "nombre": "Cirugía Torácica Mayor / Drenaje Pleural",
        "base_target": 65,
        "pv_recovered": 3,
        "consumes": "1 Tubo torácico + 2 Vendas + 1 Anestésico local"
    },
    "TRAQUEOTOMIA_EMERGENCIA": {
        "nombre": "Traqueotomía de Emergencia & Desobstrucción Aérea",
        "base_target": 70,
        "pv_recovered": 2,
        "consumes": "1 Cánula traqueal + 1 Antiséptico"
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
    "AMPUTACION_LIMPIA": {
        "nombre": "Amputación Quirúrgica Limpia & Cauterización con Láser",
        "base_target": 60,
        "pv_recovered": 2,
        "consumes": "1 Sierra quirúrgica + 1 Cauterizador + 2 Vendas hemostáticas"
    },
    "EXTRACCION_PARASITOS": {
        "nombre": "Extracción de Parásitos & Quistes del Sumidero",
        "base_target": 65,
        "pv_recovered": 3,
        "consumes": "1 Antiséptico concentrado + 1 Pinza de biopsia"
    },
    "ESTIMULACION_NEURAL_COMA": {
        "nombre": "Electro-Estimulación Neural para Despertar de Coma",
        "base_target": 55,
        "pv_recovered": 2,
        "consumes": "1 Estimulador galvánico + 1 Ampolla neuro-trópica"
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
                    "CABEZA": {"status": "ESTABLE", "damage": 0, "condition": "Sedación controlada", "rec_proc": "ESTIMULACION_NEURAL_COMA"},
                    "TORAX": {"status": "CRÍTICO", "damage": 6, "condition": "Perforación torácica profunda por proyectil", "rec_proc": "PERFUSION_TISULAR"},
                    "ABDOMEN": {"status": "MODERADO", "damage": 1, "condition": "Laceración superficial", "rec_proc": "SUTURA_MAYOR"},
                    "BRAZO_IZQ": {"status": "ESTABLE", "damage": 0, "condition": "Línea IV insertada", "rec_proc": "INJERTO_TISULAR"},
                    "BRAZO_DER": {"status": "ESTABLE", "damage": 0, "condition": "Monitores de pulso", "rec_proc": "INJERTO_TISULAR"},
                    "PIERNAS": {"status": "ESTABLE", "damage": 0, "condition": "Perfusión normal", "rec_proc": "SUTURA_MAYOR"}
                }
            }
        elif "Tertius" in patient_name:
            return {
                "patient": "Tertius Holt",
                "vital_hp": "8 / 11",
                "status": "Consciente / Drenaje Activo",
                "zones": {
                    "CABEZA": {"status": "ESTABLE", "damage": 0, "condition": "Alerta y orientado", "rec_proc": "ESTIMULACION_NEURAL_COMA"},
                    "TORAX": {"status": "MODERADO", "damage": 3, "condition": "Drenaje intercostal funcionando", "rec_proc": "TORACICA"},
                    "ABDOMEN": {"status": "ESTABLE", "damage": 0, "condition": "Normal", "rec_proc": "SUTURA_MAYOR"},
                    "BRAZO_IZQ": {"status": "ESTABLE", "damage": 0, "condition": "Normal", "rec_proc": "INJERTO_TISULAR"},
                    "BRAZO_DER": {"status": "LEVE", "damage": 1, "condition": "Contusión por retroceso", "rec_proc": "INJERTO_TISULAR"},
                    "PIERNAS": {"status": "ESTABLE", "damage": 0, "condition": "Reposo", "rec_proc": "SUTURA_MAYOR"}
                }
            }
        else:
            return {
                "patient": patient_name,
                "vital_hp": "5 / 10",
                "status": "Urgencia Clandestina",
                "zones": {
                    "CABEZA": {"status": "LEVE", "damage": 1, "condition": "Contusión por culatazo", "rec_proc": "ESTIMULACION_NEURAL_COMA"},
                    "TORAX": {"status": "MODERADO", "damage": 2, "condition": "Herida de esquirlas", "rec_proc": "TRAQUEOTOMIA_EMERGENCIA"},
                    "ABDOMEN": {"status": "LEVE", "damage": 1, "condition": "Impacto amortiguado", "rec_proc": "EXTRACCION_PARASITOS"},
                    "BRAZO_IZQ": {"status": "ESTABLE", "damage": 0, "condition": "Normal", "rec_proc": "AMPUTACION_LIMPIA"},
                    "BRAZO_DER": {"status": "ESTABLE", "damage": 0, "condition": "Normal", "rec_proc": "INSTALACION_BIONICA"},
                    "PIERNAS": {"status": "LEVE", "damage": 1, "condition": "Rozadura de bala", "rec_proc": "SUTURA_MAYOR"}
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
        target = tech_skill + 10
        is_success = roll <= target
        degrees = abs((target - roll) // 10)
        
        new_credits = available_credits - cost

        chat_prompt = (
            f"[ACCIÓN COGITADOR RHO-9 // FORJA MECATRÓNICA]\n"
            f"Khepra-9 ha completado la fabricación de: {implant['nombre']}.\n"
            f"Tirada Técnica: {roll} vs {target} ({degrees} Grados de {'Éxito' if is_success else 'Fallo'}).\n"
            f"Coste: {cost} ¤ (Saldo restante: {new_credits} ¤) | Destinatario: {implant['recipient']}\n"
            f"Bono Permanente: {implant['bonus']}\n"
            f"💬 Khepra-9: \"La carne es débil; el acero del Dios Máquina perdura.\""
        )

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
            "chat_prompt": chat_prompt,
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

        chat_prompt = (
            f"[ACCIÓN COGITADOR RHO-9 // INTERVENCIÓN QUIRÚRGICA]\n"
            f"Alexander ejecutó: {proc['nombre']} sobre {patient_name}.\n"
            f"Tirada Médica: {roll} vs {target} ({degrees} Grados de {'Éxito' if is_success else 'Complicación'}).\n"
            f"Soporte Empleado: {'Diagnostor Multispectral (+15%)' if use_diagnostor else ''} {'Unidad de Sangre (+10%)' if use_blood else ''}\n"
            f"Efecto Vital: +{pv_gain} Puntos de Vida recuperados.\n"
            f"Consumibles: {proc['consumes']}\n"
            f"💬 Alexander: \"El flujo arterial responde y los signos vitales se estabilizan.\""
        )
        
        return {
            "success": is_success,
            "patient": patient_name,
            "procedure_name": proc["nombre"],
            "target_skill": target,
            "roll": roll,
            "degrees": degrees,
            "pv_healed": pv_gain,
            "consumables_used": proc["consumes"],
            "chat_prompt": chat_prompt,
            "message": f"{'✅ CIRUGÍA EXITOSA' if is_success else '⚠️ CIRUGÍA COMPLICADA'}: {patient_name} ha recibido {proc['nombre']}. Tirada: {roll} vs {target} ({degrees} Grados). Recuperados: +{pv_gain} PV."
        }
