"""
WH40K Entity Registry Engine (entity_registry_engine.py)
Authoritative, structured database & query engine for all Campaign NPCs, Retinue Members, Patients,
Security Personnel, External Contacts, Debtors, and Shadow Figures.

Eliminates ambiguity between Retinue vs NPCs vs Clinical Patients vs Debtors.
"""

from typing import Dict, List, Any, Optional
import re

RETINUE_MEMBERS = [
    {
        "entity_id": "NPC-MARA-VEYL-001",
        "member_id": "MEMBER.ALEXANDER.MARA-VEYL",
        "nombre_completo": "Mara Veyl",
        "familia": "Familia Veyl (Hermana y protectora de Sael Veyl)",
        "categoria": "SEQUITO_PACTADO",
        "rol_principal": "Mantenimiento de precisión técnica y logística",
        "base_incorporacion": "Pacto de servicio personal vitalicio como pago por salvar la vida de su hermano Sael Veyl.",
        "estado_vital": "VIVA (10/10 PV) · Móvil · Abstinencia activa no crítica",
        "ubicacion_actual": "Medicae Station Rho-9 // Cuarto C-03",
        "personalidad": "Directa, seca, leal a los términos del pacto, protectora feroz de Sael.",
        "competencias": ["Mantenimiento industrial", "Electrónica básica", "Soporte logístico de campo"],
        "inventario": ["Herramientas de precisión", "Mono de trabajo reforzado", "Raciones estándar"]
    },
    {
        "entity_id": "NPC-ILYRA-VENN-001",
        "member_id": "MEMBER.ALEXANDER.ILYRA-VENN",
        "nombre_completo": "Ilyra Venn",
        "familia": "Independiente",
        "categoria": "SEQUITO_PACTADO",
        "rol_principal": "Operadora de apoyo táctico y exploración",
        "base_incorporacion": "Miembro incorporado formalmente bajo pacto de lealtad y servicio.",
        "estado_vital": "VIVA (10/10 PV) · Operativa",
        "ubicacion_actual": "Medicae Station Rho-9 // Puesto perimetral",
        "personalidad": "Atenta, reservada, pragmática.",
        "competencias": ["Exploración urbana", "Armas cortas", "Sigilo en subniveles"]
    },
    {
        "entity_id": "NPC-HALVEN-RUSK-001",
        "member_id": "MEMBER.ALEXANDER.HALVEN-RUSK",
        "nombre_completo": "Halven Rusk",
        "familia": "Independiente",
        "categoria": "SEQUITO_PACTADO",
        "rol_principal": "Auxiliar de triaje y asistencia de pacientes en Rho-9",
        "base_incorporacion": "Miembro de séquito asignado al soporte de cuidados.",
        "estado_vital": "VIVO (10/10 PV) · Operativo",
        "ubicacion_actual": "Medicae Station Rho-9 // Área de recuperación C-03",
        "personalidad": "Metódico, paciente, obediente a las órdenes médicas.",
        "competencias": ["Cuidados básicos", "Movilización de heridos", "Desinfección de material"]
    }
]

RHO9_STATION_PERSONNEL = [
    {
        "entity_id": "NPC-SEVERAN-HOLT-001",
        "nombre_completo": "Severan Holt",
        "familia": "Familia Holt (Hermano/compañero de Tertius, Quartus y Kerrin Holt)",
        "categoria": "SEGURIDAD_TERRITORIAL",
        "rol_principal": "Maestro de Seguridad y Guardia de Contención del Refugio",
        "base_pacto": "Dos ciclos (2 años) de protección territorial estricta de Rho-9 (1 ciclo por salvarlo del tiroteo + 1 ciclo por rescatar a Tertius).",
        "estado_vital": "VIVO (11/11 PV) · Operativo",
        "ubicacion_actual": "Medicae Station Rho-9 // Puesto de mando y esclusas",
        "es_sequito": False,
        "armadura": "Armadura de campaña (Cuerpo 3; Cabeza/Extremidades 2)",
        "armas": ["Carabina gremial 24/24 (custodia)", "Pistola de servicio"],
        "equipo_especial": ["Visor multispectral", "Filtro sellado"],
        "estadisticas": {"CC": 40, "Balistica": 48, "Fuerza": 38, "Resistencia": 42, "Agilidad": 43, "Inteligencia": 42, "Percepcion": 49, "Voluntad": 46},
        "personalidad": "Disciplinado, frío, desconfiado por entrenamiento. Separa tajantemente deber y amistad. No es amigo ni devoto.",
        "limites_conocimiento": "Conoce la clínica y la defensa; desconoce los secretos profundos del Umbral y los pactos privados de Alexander."
    },
    {
        "entity_id": "NPC-KHEPRA-9-001",
        "nombre_completo": "Khepra-9",
        "familia": "Adeptus Mechanicus / Leximecánica Independiente",
        "categoria": "PERSONAL_TECNICO",
        "rol_principal": "Leximecánica y Evaluadora Biomecánica (Futura encargada del Taller Técnico)",
        "base_relacion": "Colaboración técnica independiente y reciprocidad estricta tras extirpación consentida de masa dorsal.",
        "estado_vital": "VIVA (10/10 PV) · 49.982% máquina integrada",
        "ubicacion_actual": "Medicae Station Rho-9 // Laboratorio y Taller previsto",
        "es_sequito": False,
        "personalidad": "Bivalente, ultra-racional, data-driven, orientada a la eficiencia y el respeto a los Espíritus Máquina.",
        "tarea_activa": "Evaluación neurobiomecánica de las interfaces anómalas de Demer Vhal."
    },
    {
        "entity_id": "NPC-SYRA-KOL-001",
        "nombre_completo": "Syra Kol",
        "familia": "Familia Kol (Vinculada administrativamente al difunto Dervan Kol)",
        "categoria": "PERSONAL_ADMINISTRATIVO",
        "rol_principal": "Auxiliar de Registros, Contabilidad, Logística y Sombra Infinita",
        "base_relacion": "Trabajadora no pactada; alojamiento y comida en Rho-9 a cambio de clasificación y orden de suministros.",
        "estado_vital": "VIVA · Móvil y estable",
        "ubicacion_actual": "Medicae Station Rho-9 // ADM-01",
        "es_sequito": False,
        "personalidad": "Práctica, directa, con humor sombrío bajo presión. No asume mando de seguridad ni cirugías mayores.",
        "logro_clave": "Compartimentó el archivo clínico de Rho-9 (los expedientes comunes omiten lo sobrenatural; casos anómalos pasan a Aislamiento)."
    }
]

RHO9_PATIENTS = [
    {
        "entity_id": "NPC-CANDELA-TERTIUS-001",
        "nombre_completo": "Tertius Holt",
        "familia": "Familia Holt (Hermano/compañero de Severan y Quartus Holt)",
        "categoria": "PACIENTE_CLINICO",
        "estado_clinico": "EN_RECUPERACION",
        "ubicacion_actual": "Medicae Station Rho-9 // Cuarto de Recuperación C-01",
        "telemetria": {"pulso_bpm": 94, "ritmo": "Débil pero rítmico", "herida": "Extracción torácica de metralla metálica"},
        "estado_deuda": "Deudor bajo pacto médico por extracción y cirugía. Conserva plena autonomía para negociar términos tras el alta.",
        "es_sequito": False
    },
    {
        "entity_id": "NPC-CANDELA-QUARTUS-001",
        "nombre_completo": "Quartus Holt",
        "familia": "Familia Holt (Hermano de Severan y Tertius)",
        "categoria": "PACIENTE_CLINICO",
        "estado_clinico": "CRITICO_ESTABLE",
        "ubicacion_actual": "Medicae Station Rho-9 // Cuarto C-03 (Soporte Vital Continuo)",
        "telemetria": {"salud": "4/11 PV", "estado": "Inconsciente e intubado", "herida": "Trauma pélvico, vascular e intestinal masivo reparado"},
        "estado_deuda": "Deudor bajo pacto. Términos congelados hasta que recupere la consciencia y pueda hablar.",
        "es_sequito": False
    },
    {
        "entity_id": "NPC-DEMER-VHAL-001",
        "alias_historico": "NPC-M01-SUBJECT-04 / Sujeto M-01 IV",
        "nombre_completo": "Demer Vhal",
        "familia": "Independiente / Sujeto de Investigación M-01",
        "categoria": "PACIENTE_ANOMALO",
        "estado_clinico": "AISLAMIENTO_ESTABLE",
        "ubicacion_actual": "Medicae Station Rho-9 // Sala de Aislamiento Privado",
        "diagnostico": "Integración híbrida neurovascular humano + máquina + anomalía del Umbral (marca enigmática '63%').",
        "pistas_secretas": ["Recuerda autorizaciones firmadas por 'Sarda'", "Escuchó: 'Orven quiere los resultados antes de moverlo'"],
        "estado_deuda": "Paciente libre bajo protección médica y confidencialidad. Sin servidumbre ni pacto oscuro.",
        "es_sequito": False
    },
    {
        "entity_id": "NPC-SAEL-VEYL-001",
        "nombre_completo": "Sael Veyl",
        "familia": "Familia Veyl (Hermano de Mara Veyl)",
        "categoria": "PACIENTE_LIBRE",
        "estado_clinico": "EN_RECUPERACION",
        "ubicacion_actual": "Medicae Station Rho-9 // Cuarto C-03",
        "telemetria": {"salud": "10/10 PV", "estado": "Estable con drenaje torácico", "movilidad": "Inmovilizado temporalmente"},
        "estado_deuda": "COMPLETAMENTE LIBRE DE DEUDA. Su rescate fue pagado por Mara Veyl mediante su pacto vitalicio.",
        "personalidad": "Sarcástico, calculador, inteligente. Posee libros de cuentas y rutas memorizadas de los Caldereros.",
        "es_sequito": False
    }
]

EXTERNAL_CONTACTS_AND_FACTIONS = [
    {
        "entity_id": "NPC-KERRIN-HOLT-001",
        "nombre_completo": "Kerrin Holt",
        "familia": "Familia Holt",
        "categoria": "CONTACTO_EXTERIOR",
        "rol_principal": "Lugarteniente operativo de Darrik Vane",
        "estado": "VIVO · Crítico estable posoperatorio",
        "ubicacion": "Emplazamiento exterior de Darrik Vane en Dust Falls"
    },
    {
        "entity_id": "NPC-DARRIK-VANE-001",
        "nombre_completo": "Darrik Vane",
        "categoria": "CONTRATISTA_EXTERIOR",
        "rol_principal": "Traficante local y contratante semanal del Médico Negro en Dust Falls",
        "estado": "VIVO · Operativo"
    },
    {
        "entity_id": "NPC-ENFORCER-UMBRAL-001",
        "nombre_completo": "Especialista Enforcer Umbral",
        "categoria": "CONTRAPARTE_PACTADA",
        "rol_principal": "Antiguo perseguidor obligado por pacto a transporte de mercancías e inteligencia",
        "estado": "VIVO · Bajo pacto de transporte"
    },
    {
        "entity_id": "NPC-BREN-ORSTAG-001",
        "nombre_completo": "Bren Orstag",
        "categoria": "FACCION_CALDEREROS",
        "rol_principal": "Líder de grupo armado Calderero vinculado a Kappa-Nueve y la búsqueda de Sael",
        "estado": "VIVO · Hostilidad latente"
    },
    {
        "entity_id": "NPC-HADRIX-VALE-001",
        "nombre_completo": "Hadrix Vale",
        "categoria": "AUXILIA_TECHNICA",
        "rol_principal": "Técnico cibernético de la estación bajo Elevador Doce; descubrió derivaciones clandestinas",
        "estado": "VIVO"
    },
    {
        "entity_id": "NPC-JOREN-PELL-001",
        "nombre_completo": "Joren Pell",
        "categoria": "RECUPERADOR",
        "rol_principal": "Recuperador independiente rescatado de un millisaur por Alexander; confidente de E-12",
        "estado": "VIVO"
    },
    {
        "entity_id": "NPC-SARDA-E12-001",
        "nombre_completo": "Sarda (E-12)",
        "categoria": "FIGURA_EN_LA_SOMBRA",
        "rol_principal": "Autoridad desconocida de la estación E-12 que ordenaba traslados de sujetos M-01",
        "estado": "DESCONOCIDO"
    },
    {
        "entity_id": "NPC-ORVEN-UNKNOWN-001",
        "nombre_completo": "M. Orven",
        "categoria": "FIGURA_EN_LA_SOMBRA",
        "rol_principal": "Supervisor de investigación ('NO VOX') que esperaba los resultados de Demer Vhal",
        "estado": "DESCONOCIDO"
    },
    {
        "entity_id": "NPC-DERVAN-KOL-001",
        "nombre_completo": "Dervan Kol",
        "familia": "Familia Kol",
        "categoria": "ALMA_COSECHADA",
        "rol_principal": "Deudor ejecutado. Su alma está almacenada en la Reserva Umbral de Alexander.",
        "estado": "FALLECIDO / ALMA ALMACENADA"
    },
    {
        "entity_id": "NPC-PELL-E12-001",
        "nombre_completo": "Pell del puesto E-12",
        "categoria": "ALMA_COSECHADA",
        "rol_principal": "Guardia de E-12 ejecutado. Su alma saldó el pacto médico de 2 almas.",
        "estado": "FALLECIDO / COSECHADO"
    }
]

ALL_ENTITIES = RETINUE_MEMBERS + RHO9_STATION_PERSONNEL + RHO9_PATIENTS + EXTERNAL_CONTACTS_AND_FACTIONS

class EntityRegistryEngine:

    @classmethod
    def get_all_entities(cls, category_filter: Optional[str] = None, search: Optional[str] = None) -> List[Dict[str, Any]]:
        results = ALL_ENTITIES
        if category_filter:
            cf = category_filter.upper()
            results = [e for e in results if cf in e.get("categoria", "").upper()]
        if search:
            s = search.lower()
            results = [
                e for e in results 
                if s in e.get("nombre_completo", "").lower() 
                or s in e.get("entity_id", "").lower() 
                or s in e.get("familia", "").lower()
                or s in e.get("rol_principal", "").lower()
            ]
        return results

    @classmethod
    def get_entity_by_id_or_name(cls, identifier: str) -> Optional[Dict[str, Any]]:
        clean_id = identifier.strip().lower()
        for e in ALL_ENTITIES:
            if (
                e.get("entity_id", "").lower() == clean_id 
                or e.get("nombre_completo", "").lower() == clean_id
                or clean_id in e.get("nombre_completo", "").lower()
                or e.get("alias_historico", "").lower() == clean_id
            ):
                return e
        return None

    @classmethod
    def get_retinue(cls) -> Dict[str, Any]:
        return {
            "total_members": len(RETINUE_MEMBERS),
            "members": RETINUE_MEMBERS,
            "rule": "Solo Mara Veyl, Ilyra Venn y Halven Rusk forman parte del séquito pactado de Alexander."
        }

    @classmethod
    def get_rho9_inhabitants(cls) -> Dict[str, Any]:
        return {
            "seguridad": [e for e in RHO9_STATION_PERSONNEL if e["categoria"] == "SEGURIDAD_TERRITORIAL"],
            "personal_tecnico_y_admin": [e for e in RHO9_STATION_PERSONNEL if e["categoria"] in ["PERSONAL_TECNICO", "PERSONAL_ADMINISTRATIVO"]],
            "pacientes_clinicos": RHO9_PATIENTS
        }

    @classmethod
    def get_patients_telemetry(cls) -> List[Dict[str, Any]]:
        return RHO9_PATIENTS

    @classmethod
    def get_family_tree(cls, family_name: str = "Holt") -> List[Dict[str, Any]]:
        fn = family_name.lower()
        return [e for e in ALL_ENTITIES if fn in e.get("familia", "").lower() or fn in e.get("nombre_completo", "").lower()]
