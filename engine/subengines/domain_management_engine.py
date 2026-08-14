"""
WH40K Domain & Base Management Engine v5.0 (domain_management_engine.py)
Includes:
- Standardized 5/3 Room Upgrade Tree
- Chat Synchronization Bridge (sync_chat_event, get_chat_events)
- Dynamic Character Positions & Real-time Chrono State Tracking
"""

import json
import os
from typing import Dict, List, Any, Optional

DEFAULT_UPGRADES = {
    "GATE-01": 1,
    "ADM-01": 1,
    "Q-01": 1,
    "C-01": 1,
    "C-02": 1,
    "C-03": 2, # Quartus en Nivel 2
    "F-02": 1,
    "E-01": 0,
    "T-01": 1,
    "HAB-01": 1,
    "HAB-02": 1,
    "HAB-03": 1,
    "HAB-04": 0,
    "COMM-01": 1,
    "SUB-01": 0
}

DEFAULT_SUBLEVEL_REVEALED = {
    "SUB-GEN": False,
    "SUB-TUNNEL": False,
    "SUB-STASIS": False,
    "SUB-CHEM": False
}

DEFAULT_POSITIONS = {
    "Alexander": "Q-01",
    "Severan Holt": "GATE-01",
    "Khepra-9": "T-01",
    "Syra Kol": "ADM-01",
    "Halven Rusk": "Q-01",
    "Jarek Venn": "GATE-01",
    "Tertius Holt": "C-01",
    "Quartus Holt": "C-03"
}

DEFAULT_CHRONO = {
    "day": 4,
    "hour": 23,
    "minute": 54,
    "second": 0,
    "turn": 918,
    "phase": "VIGILIA NOCTURNA"
}

DEFAULT_LOGS = [
    {"time": "Día 04 · 23:54", "type": "SECURITY", "text": "Severan Holt completó la ronda perimetral en la compuerta principal. Acceso asegurado."},
    {"time": "Día 04 · 23:15", "type": "MEDICAL", "text": "Tertius Holt estabilizado tras drenaje torácico. Parámetros vitales: 8/11."},
    {"time": "Día 04 · 22:50", "type": "COSECHA", "text": "Halven Rusk ejecutó a los 4 cautivos en la cámara de triaje. +4 Almas transferidas a Alexander."},
    {"time": "Día 04 · 21:30", "type": "LOGISTICS", "text": "Syra Kol registró el botín del depósito: 11 armas de fuego y 1.000+ proyectiles clasificados."},
    {"time": "Día 04 · 20:10", "type": "TECH", "text": "Khepra-9 instaló el banco de trabajo mecatrónico en el Taller T-01."}
]

# CATÁLOGO ESTANDARIZADO DE SALAS Y MEJORAS
ROOM_DEFINITIONS = {
    # === SALAS VITALES (5 NIVELES MÁXIMO) ===
    "Q-01": {
        "is_vital": True,
        "max_level": 5,
        "code": "Q-01",
        "name": "Quirófano Central de Trauma",
        "type": "medical",
        "tiers": {
            1: {
                "title": "Quirófano Parcial Integrado (Nivel 1)",
                "status": "OPERATIVO", "color": "green",
                "equipment": ["Diagnostor de espectro (+15% diagnóstico)", "Mesa quirúrgica hidráulica", "Monitores vitales"],
                "bonus": "+10% ambiental a procedimientos médicos; +15% a diagnóstico dirigido",
                "next": {"title": "Nivel 2: Circuito de Agua Estéril & Lámparas Articuladas", "cost_credits": 200, "cost_mats": "20m Tubería clínica + 2 Filtros clínicos", "effect": "Eleva el bono ambiental a cirugías a +20% y reduce tiempo operatorio a la mitad"}
            },
            2: {
                "title": "Quirófano Aséptico Avanzado (Nivel 2)",
                "status": "OPERATIVO", "color": "green",
                "equipment": ["Circuito de agua estéril", "Lámparas cenitales articuladas", "Diagnostor multispectral"],
                "bonus": "+20% ambiental a cirugías; tiempo operatorio reducido a la mitad",
                "next": {"title": "Nivel 3: Servobrazo Quirúrgico Mecanizado", "cost_credits": 350, "cost_mats": "1 Servobrazo articulado + 4 Cánulas de vacío", "effect": "Eleva el bono a +30% a cirugías; anula penalizadores por fatiga o temblor del cirujano y permite 2 cirugías simultáneas"}
            },
            3: {
                "title": "Quirófano Mecatrónico Asistido (Nivel 3)",
                "status": "OPERATIVO", "color": "green",
                "equipment": ["Servobrazo quirúrgico mecanizado", "Inyectores automáticos de coagulante", "Cauterio láser doble"],
                "bonus": "+30% a cirugías; anula fatiga/temblor del cirujano; permite 2 cirugías simultáneas con Halven",
                "next": {"title": "Nivel 4: Campo de Estasis Focal Intraoperatorio", "cost_credits": 550, "cost_mats": "1 Generador de campo estático + 2 Células energéticas", "effect": "Suspende el desangrado y la muerte clínica durante la operación (0% riesgo de muerte intraoperatoria)"}
            },
            4: {
                "title": "Unidad de Trauma con Campo de Estasis (Nivel 4)",
                "status": "OPERATIVO", "color": "green",
                "equipment": ["Emisor de campo de estasis focal", "Monitores de ondas cerebrales", "Líneas de soporte extracorpóreo"],
                "bonus": "+35% a cirugías; suspende la muerte clínica durante la operación (0% riesgo de parada irreversible)",
                "next": {"title": "Nivel 5: Sanctum de Biotransferencia & Regeneración Tisular Mayor", "cost_credits": 850, "cost_mats": "1 Núcleo de bio-impresión tisular + Aleaciones biológicas", "effect": "+40% a cirugías, regeneración de extremidades amputadas y transplante de órganos genéticos/biónicos sin rechazo"}
            },
            5: {
                "title": "Sanctum de Regeneración Tisular Mayor (Nivel 5 · MÁXIMO)",
                "status": "OPERATIVO", "color": "green",
                "equipment": ["Matriz de bio-impresión tisular", "Campo de estasis focal", "Servobrazo de micro-cirugía", "Diagnostor arcaico"],
                "bonus": "+40% a cirugías; regeneración de miembros amputados e injertos biónicos/genéticos con compatibilidad total",
                "next": None
            }
        }
    },
    "GATE-01": {
        "is_vital": True,
        "max_level": 5,
        "code": "ACCESO-01",
        "name": "Compuerta Principal & Perímetro Defensivo",
        "type": "security",
        "tiers": {
            1: {
                "title": "Barricada Reforzada Simple (Nivel 1)",
                "status": "OPERATIVA", "color": "green",
                "equipment": ["Cerradura codificada", "Troneras de tiro", "Barricadas de chapa pesada"],
                "bonus": "+15% defensa contra asaltos menores; cerrojos mecánicos de emergencia",
                "next": {"title": "Nivel 2: Blindaje de Acero & Alarma Vox Perimetral", "cost_credits": 120, "cost_mats": "2 Placas de aleación + 1 Carrete de cable", "effect": "+25% resistencia estructural y aviso anticipado de 2 turnos ante incursiones"}
            },
            2: {
                "title": "Blindaje de Acero & Alarma Vox (Nivel 2)",
                "status": "OPERATIVA", "color": "green",
                "equipment": ["Chapas de acero remachado", "Sensor de proximidad vox", "Troneras en cruz"],
                "bonus": "+30% resistencia estructural y sensor vox perimetral (2 turnos de aviso anticipado ante redadas)",
                "next": {"title": "Nivel 3: Troneras Automatizadas de Fuego Cruzado", "cost_credits": 240, "cost_mats": "2 Servomotores + 2 Afustes de autopistola", "effect": "Torretas automatizadas que abren fuego defensivo inmediato contra intrusos (1d10+3 daño defensivo)"}
            },
            3: {
                "title": "Paso Fortificado con Torretas Servocontroladas (Nivel 3)",
                "status": "OPERATIVA", "color": "green",
                "equipment": ["Torretas de tiro cruzado", "Cámara de pre-esclusa con mirilla blindada", "Alarma sonora sorda"],
                "bonus": "+45% defensa perimetral; fuego defensivo automático contra asaltantes",
                "next": {"title": "Nivel 4: Esclusa Hidráulica Hermética & Filtros Anti-Gas", "cost_credits": 450, "cost_mats": "1 Pistón hidráulico industrial + 2 Sellos de goma pesada", "effect": "Inmunidad total a arietes pesados, explosivos concentrados y gases cáusticos del submundo"}
            },
            4: {
                "title": "Esclusa Hermética Blindada Anti-Gas (Nivel 4)",
                "status": "OPERATIVA", "color": "green",
                "equipment": ["Pistones hidráulicos de 5 toneladas", "Sellos de aislamiento hermético", "Aspersores de contra-incendio"],
                "bonus": "+55% defensa; inmunidad a arietes, cargas de demolición y proyectiles incendiarios",
                "next": {"title": "Nivel 5: Bastión Blindado Palatino con Campo Refractor Local", "cost_credits": 750, "cost_mats": "1 Emisor refractor Enforcer + Blindaje de ceramita", "effect": "+60% Defensa perimetral, escudo de dispersión energética y esclusa impenetrable"}
            },
            5: {
                "title": "Bastión Palatino con Campo Refractor (Nivel 5 · MÁXIMO)",
                "status": "OPERATIVA", "color": "green",
                "equipment": ["Generador de campo refractor", "Pistones de ceramita", "Torretas duales Kord-24", "Sensor biométrico"],
                "bonus": "+60% defensa total; escudo de dispersión de energía y capacidad de resistir asedios de escuadras de asalto",
                "next": None
            }
        }
    },
    "F-02": {
        "is_vital": True,
        "max_level": 5,
        "code": "F-02",
        "name": "Farmacia, Biobanco & Depósito Químico",
        "type": "storage",
        "tiers": {
            1: {
                "title": "Armario Refrigerado Operativo (Nivel 1)",
                "status": "OPERATIVA", "color": "green",
                "equipment": ["Armario refrigerado", "Depósito separado para 9 frascos E-12", "Stock 200+ fármacos"],
                "bonus": "Cero degradación de medicamentos biológicos y antibióticos",
                "next": {"title": "Nivel 2: Cámara Acorazada de Toxinas & Alquimia", "cost_credits": 90, "cost_mats": "4 Placas de polímero + 2 Sellos", "effect": "Habilita síntesis de antídotos complejos y previene contaminación cruzada"}
            },
            2: {
                "title": "Cámara Acorazada de Toxinas & Alquimia (Nivel 2)",
                "status": "OPERATIVA", "color": "green",
                "equipment": ["Caja fuerte hermética", "Extractores de vapor tóxico", "Frascos de vidrio neutro"],
                "bonus": "Habilita síntesis de antídotos complejos y previene fugas de quimio-toxinas",
                "next": {"title": "Nivel 3: Laboratorio Criogénico de Biobanco Celular", "cost_credits": 220, "cost_mats": "2 Tanques criogénicos + Reguladores de nitrógeno", "effect": "+10 Unidades de sangre compatibles universales, almacenamiento indefinido de órganos y xenomuestras"}
            },
            3: {
                "title": "Laboratorio Criogénico de Biobanco Celular (Nivel 3)",
                "status": "OPERATIVA", "color": "green",
                "equipment": ["2 Tanques criogénicos de nitrógeno", "Centrifugadora hematológica", "Estantes de plasma congelado"],
                "bonus": "Capacidad de albergar 20 unidades de sangre y órganos para trasplantes sin deterioro",
                "next": {"title": "Nivel 4: Matriz Sintetizadora de Quimio-Estimulantes Escher", "cost_credits": 400, "cost_mats": "1 Destilador químico continuo + 6 Serpentines de cobre", "effect": "Reduce a la mitad el coste de todas las fórmulas alquímicas y añade +15% a tiradas de farmacología"}
            },
            4: {
                "title": "Matriz Sintetizadora de Quimio-Estimulantes (Nivel 4)",
                "status": "OPERATIVA", "color": "green",
                "equipment": ["Destilador fraccionado continuo", "Reactores catalíticos de vidrio", "Micro-dosificadores neumáticos"],
                "bonus": "Coste de síntesis alquímica reducido un 50%; +15% a tiradas de formulación química",
                "next": {"title": "Nivel 5: Bóveda de Farmacopea Arcaica & Biomecánica Avanzada", "cost_credits": 680, "cost_mats": "1 Liofilizador molecular + Fórmulas selladas", "effect": "Habilita la síntesis de drogas de combate de élite, reactivos de regeneración celular y sueros umbrales"}
            },
            5: {
                "title": "Bóveda de Farmacopea Arcaica (Nivel 5 · MÁXIMO)",
                "status": "OPERATIVA", "color": "green",
                "equipment": ["Liofilizador molecular", "Cámara criogénica de nitrógeno líquido", "Matriz de síntesis pura"],
                "bonus": "Capacidad de fabricar cualquier compuesto químico, regenerador celular o toxina militar de Necromunda",
                "next": None
            }
        }
    },
    "T-01": {
        "is_vital": True,
        "max_level": 5,
        "code": "T-01",
        "name": "Taller Mecatrónico & Armería",
        "type": "tech",
        "tiers": {
            1: {
                "title": "Taller en Instalación (Nivel 1)",
                "status": "OPERATIVO", "color": "green",
                "equipment": ["Banco de soldadura de arco", "Herramientas de precisión", "Analizador lógico"],
                "bonus": "Mantenimiento y reparación de armas sólidas y láser",
                "next": {"title": "Nivel 2: Banco de Prótesis Biónicas & Fabricación", "cost_credits": 140, "cost_mats": "1 Servo-articulador + 4 Circuitos de control", "effect": "Desbloquea la fabricación de la prótesis mecánica para el brazo del 2º deudor de Sombra"}
            },
            2: {
                "title": "Banco Protésico & Armería Avanzada (Nivel 2)",
                "status": "OPERATIVO", "color": "green",
                "equipment": ["Banco protésico de Khepra-9", "Calibrador de micro-servos", "Soldador de plasma"],
                "bonus": "Habilita la fabricación de prótesis mecánicas e implantes grado 1 para colaboradores",
                "next": {"title": "Nivel 3: Forja de Precisión & Calibrador de Armas de Fuego", "cost_credits": 280, "cost_mats": "1 Torno de precisión + 2 Crisoles de aleación", "effect": "Permite sobrecargar armas, fabricar munición de alta penetración y acoplar miras de precisión"}
            },
            3: {
                "title": "Forja Mecatrónica de Precisión (Nivel 3)",
                "status": "OPERATIVO", "color": "green",
                "equipment": ["Torno de torneado industrial", "Baño de temple por inducción", "Prensa hidráulica de recarga"],
                "bonus": "Permite modificar armas (aumentar daño +1 o alcance +25%) y fabricar munición perforante",
                "next": {"title": "Nivel 4: Ensamblador de Implantes Cibernéticos & Servocráneos", "cost_credits": 500, "cost_mats": "1 Unidad lógica Mechanicus + 2 Chasis de servocráneo", "effect": "Fabricación de ojos biónicos, filtros tox y servocráneos de vigilancia autónoma para Rho-9"}
            },
            4: {
                "title": "Laboratorio Cibernético & Ensamblaje (Nivel 4)",
                "status": "OPERATIVO", "color": "green",
                "equipment": ["Unidad de grabado de micro-circuitos", "Banco de prueba de servocráneos", "Soldador láser de precisión"],
                "bonus": "Fabricación autónoma de implantes cibernéticos grado militar y servocráneos de patrulla",
                "next": {"title": "Nivel 5: Factoría Arcanomecánica Clandestina", "cost_credits": 800, "cost_mats": "1 Generador de energía pura + Códices técnicos", "effect": "Fabricación de armamento de energía/plasma, blindajes biónicos completos y servidores armados"}
            },
            5: {
                "title": "Factoría Arcanomecánica Clandestina (Nivel 5 · MÁXIMO)",
                "status": "OPERATIVO", "color": "green",
                "equipment": ["Reactor de plasma auxiliar", "Forja de ceramita", "Ensamblador de servomotores pesados"],
                "bonus": "Fabricación y mantenimiento de cualquier tecnología avanzada, armamento de energía y biónica de grado militar",
                "next": None
            }
        }
    },
    "C-03": {
        "is_vital": True,
        "max_level": 5,
        "code": "C-03",
        "name": "Cama Clínica 03 (Cuidados Críticos — Quartus Holt)",
        "type": "recovery",
        "tiers": {
            1: {
                "title": "Soporte Vital Crítico (Nivel 1)",
                "status": "CRÍTICO_ESTABLE", "color": "crimson",
                "equipment": ["Respirador asistido", "Bomba de infusión continua", "Monitor multiseñal"],
                "bonus": "Mantiene con vida a pacientes con herida letal a quemarropa en coma farmacológico",
                "next": {"title": "Nivel 2: Sistema de Perfusión Tisular Continua", "cost_credits": 150, "cost_mats": "1 Bomba infusión portátil + 2 Líneas IV", "effect": "Permite iniciar la desintubación segura y despertar progresivo de Quartus"}
            },
            2: {
                "title": "Perfusión Tisular & Desintubación Segura (Nivel 2)",
                "status": "RECUPERACIÓN_ACTIVA", "color": "amber",
                "equipment": ["Bomba de perfusión continua", "Oxigenador de membrana", "Monitor de presión intracraneal"],
                "bonus": "Perfusión activa: Habilita desintubación segura sin colapso pulmonar y recuperación consciente de Quartus",
                "next": {"title": "Nivel 3: Cápsula de Bio-Regeneración Acelerada", "cost_credits": 260, "cost_mats": "1 Módulo de electro-estimulación + Salina rica en oxígeno", "effect": "Recuperación pasiva de +4 PV cada 24h y cicatrización acelerada de órganos internos perforados"}
            },
            3: {
                "title": "Cápsula de Bio-Regeneración Acelerada (Nivel 3)",
                "status": "RECUPERACIÓN_ACTIVA", "color": "green",
                "equipment": ["Módulo de electro-estimulación muscular", "Infusión rica en factores de crecimiento", "Bañera de soporte estéril"],
                "bonus": "Recuperación pasiva de +4 PV cada 24h; regeneración tisular acelerada sin fibrosis pulmonar",
                "next": {"title": "Nivel 4: Matriz Neuro-Estimuladora & Reversión de Coma", "cost_credits": 460, "cost_mats": "1 Casco neuro-estimulador + 4 Sensores sinápticos", "effect": "Elimina secuelas cerebrales y traumas neurológicos irreversibles en 48 horas"}
            },
            4: {
                "title": "Unidad de Terapia Neuro-Sináptica (Nivel 4)",
                "status": "OPERATIVA", "color": "green",
                "equipment": ["Casco de neuro-estimulación sináptica", "Monitores EEG continuo", "Infusor de neuro-protectores"],
                "bonus": "Protección contra daño cerebral hipóxico; reversión de comas profundos en menos de 48 horas",
                "next": {"title": "Nivel 5: Cuna de Preservación Biológica & Clonación Tisular", "cost_credits": 700, "cost_mats": "1 Cápsula sellada de regeneración celular total", "effect": "Inmune a la muerte por shock masivo, regenera daños críticos y permite cirugías de implantes mayores sin rechazo"}
            },
            5: {
                "title": "Cuna de Regeneración Tisular Total (Nivel 5 · MÁXIMO)",
                "status": "OPERATIVA", "color": "green",
                "equipment": ["Cápsula de regeneración total de órganos", "Soporte metabólico ultra-rápido", "Monitores cuánticos"],
                "bonus": "Garantiza la supervivencia de cualquier herido crítico y regenera órganos destruidos en 3 días",
                "next": None
            }
        }
    },

    # === SALAS ESTÁNDAR (3 NIVELES MÁXIMO) ===
    "E-01": {
        "is_vital": False,
        "max_level": 3,
        "code": "E-01",
        "name": "Sala de Esterilización & Filtros",
        "type": "medical",
        "tiers": {
            0: {
                "title": "Autoclave Parcial / Sin Filtros (Nivel 0)",
                "status": "REQUIERE_MEJORA", "color": "amber",
                "equipment": ["Autoclave manual sucio"],
                "bonus": "Esterilización de campo limitada",
                "next": {"title": "Nivel 1: Circuito Completo Limpio/Sucio & Autoclave Térmico", "cost_credits": 80, "cost_mats": "Trabajo de Khepra-9 + 2 Válvulas", "effect": "Elimina al 100% el riesgo de infecciones postoperatorias en toda la clínica"}
            },
            1: {
                "title": "Circuito Aséptico Completo (Nivel 1)",
                "status": "OPERATIVA", "color": "green",
                "equipment": ["Autoclave de vapor a presión", "Filtros de aire adaptados", "Ducha de descontaminación"],
                "bonus": "Elimina al 100% el riesgo de infecciones postoperatorias y septicemia en toda la base",
                "next": {"title": "Nivel 2: Descontaminador Químico & Lámparas de Radiación UV", "cost_credits": 160, "cost_mats": "4 Tubos UV + 1 Tanque desinfectante", "effect": "Inmuniza la clínica contra bio-toxinas de plagas y virus orgánicos del submundo"}
            },
            2: {
                "title": "Descontaminador UV & Filtro Químico (Nivel 2)",
                "status": "OPERATIVA", "color": "green",
                "equipment": ["Batería de lámparas UV bactericidas", "Circuito de niebla desinfectante", "Esclusa aséptica"],
                "bonus": "Inmunidad total contra brotes de plagas, esporas y bio-toxinas volátiles en Rho-9",
                "next": {"title": "Nivel 3: Unidad de Purificación Hospitalaria Militar", "cost_credits": 290, "cost_mats": "1 Purificador de flujo laminar + Filtros HEPA pesados", "effect": "Otorga +10% de velocidad de recuperación natural a todos los pacientes hospitalizados"}
            },
            3: {
                "title": "Unidad de Flujo Laminar Militar (Nivel 3 · MÁXIMO)",
                "status": "OPERATIVA", "color": "green",
                "equipment": ["Filtros de flujo laminar de alta presión", "Monitores de partículas estériles", "Esterilizador flash"],
                "bonus": "Esterilidad quirúrgica de grado hospitalario militar; +10% a recuperación de todos los pacientes",
                "next": None
            }
        }
    },
    "ADM-01": {
        "is_vital": False,
        "max_level": 3,
        "code": "ADM-01",
        "name": "Recepción & Registro Logístico",
        "type": "logistics",
        "tiers": {
            1: {
                "title": "Puesto Contable Manual (Nivel 1)",
                "status": "OPERATIVA", "color": "green",
                "equipment": ["Cogitador de registro", "Caja fuerte de créditos", "Fichas de suministros"],
                "bonus": "Registro exacto de consumibles y contabilidad auditada sin fugas",
                "next": {"title": "Nivel 2: Terminal Vox Interceptora de Red", "cost_credits": 80, "cost_mats": "1 Tester + 12 Conectores electrónicos", "effect": "Monitoreo pasivo de frecuencias Enforcer y rumores del mercado de Dust Falls"}
            },
            2: {
                "title": "Terminal Vox Interceptora (Nivel 2)",
                "status": "OPERATIVA", "color": "green",
                "equipment": ["Receptor de banda ancha de onda corta", "Decodificador de claves", "Antena direccional oculta"],
                "bonus": "Monitoreo de frecuencias policiales y alerta temprana de movimientos de bandas en Dust Falls",
                "next": {"title": "Nivel 3: Central de Inteligencia & Encriptación Clandestina", "cost_credits": 180, "cost_mats": "1 Cripto-procesador + 2 Discos magnéticos", "effect": "Detecta redes de informantes rivales y reduce en un 50% la atención de facciones hostiles"}
            },
            3: {
                "title": "Central de Inteligencia & Cripto-Análisis (Nivel 3 · MÁXIMO)",
                "status": "OPERATIVA", "color": "green",
                "equipment": ["Cripto-procesador militar", "Banco de frecuencias encriptadas", "Terminal de datos cifrada"],
                "bonus": "Información estratégica en tiempo real de Dust Falls; reduce a la mitad la sospecha de los Enforcers",
                "next": None
            }
        }
    },
    "C-01": {
        "is_vital": False,
        "max_level": 3,
        "code": "C-01",
        "name": "Cama Clínica 01 (Postoperatorio — Tertius Holt)",
        "type": "recovery",
        "tiers": {
            1: {
                "title": "Cama Monitoreada (Nivel 1)",
                "status": "OCUPADA", "color": "amber",
                "equipment": ["Drenaje torácico funcional", "Soporte de fluidos IV", "Monitor de pulso"],
                "bonus": "Estabilización garantizada; recuperación pasiva de 1 PV cada 24h",
                "next": {"title": "Nivel 2: Módulo de Oxigenoterapia Regulada", "cost_credits": 60, "cost_mats": "1 Cilindro de oxígeno + 1 Regulador", "effect": "Acelera recuperación de heridas pulmonares y torácicas (+2 PV cada 24h)"}
            },
            2: {
                "title": "Módulo de Oxigenoterapia Regulada (Nivel 2)",
                "status": "OCUPADA", "color": "green",
                "equipment": ["Cilindro de oxígeno con mezclador", "Cánula de alto flujo", "Humidificador térmico"],
                "bonus": "Recuperación acelerada de heridas pulmonares (+2 PV cada 24h) y reducción del dolor torácico",
                "next": {"title": "Nivel 3: Cuna Terapéutica Asistida", "cost_credits": 140, "cost_mats": "Colchón de presión alterna + Calentador", "effect": "+3 PV cada 24h y anula completamente penalizaciones de fatiga al despertar"}
            },
            3: {
                "title": "Cuna Terapéutica Asistida (Nivel 3 · MÁXIMO)",
                "status": "OCUPADA", "color": "green",
                "equipment": ["Colchón de flotación seca", "Regulador de temperatura continuo", "Infusor de suero acelerado"],
                "bonus": "Recuperación de +3 PV cada 24h; Tertius recupera movilidad completa en la mitad de tiempo",
                "next": None
            }
        }
    },
    "C-02": {
        "is_vital": False,
        "max_level": 3,
        "code": "C-02",
        "name": "Cama Clínica 02 (Triaje / Emergencias)",
        "type": "recovery",
        "tiers": {
            1: {
                "title": "Cama Libre para Triaje (Nivel 1)",
                "status": "DISPONIBLE", "color": "green",
                "equipment": ["Líneas IV en espera", "Bandeja de sutura rápida"],
                "bonus": "Capacidad de recepción inmediata de 1 paciente de trauma sin preparación",
                "next": {"title": "Nivel 2: Carro de Reanimación Avanzada", "cost_credits": 100, "cost_mats": "1 Desfibrilador + 1 Kit trauma mayor", "effect": "+20% a tiradas de estabilización de urgencia en los primeros 2 turnos"}
            },
            2: {
                "title": "Carro de Reanimación Avanzada (Nivel 2)",
                "status": "DISPONIBLE", "color": "green",
                "equipment": ["Desfibrilador manual", "Ampollario de adrenalina rápida", "Aspirador de secreciones portátil"],
                "bonus": "+20% a tiradas de estabilización de urgencia en pacientes al borde de la muerte",
                "next": {"title": "Nivel 3: Estación de Trauma Rápido Automatizada", "cost_credits": 210, "cost_mats": "1 Monitor multicanal + Bomba de infusión rápida", "effect": "+30% a tiradas de estabilización de choque y transfusión sanguínea instantánea"}
            },
            3: {
                "title": "Estación de Trauma Rápido (Nivel 3 · MÁXIMO)",
                "status": "DISPONIBLE", "color": "green",
                "equipment": ["Bomba de infusión de choque", "Monitor de gasto cardíaco", "Compresor torácico automático"],
                "bonus": "+30% a estabilización; transfusión inmediata de emergencia sin pérdida de tiempo de acción",
                "next": None
            }
        }
    },
    "HAB-01": {
        "is_vital": False,
        "max_level": 3,
        "code": "HAB-01",
        "name": "Dormitorio de Alexander & Sanctum",
        "type": "living",
        "tiers": {
            1: {
                "title": "Habitación Privada Segura (Nivel 1)",
                "status": "OPERATIVA", "color": "green",
                "equipment": ["Catre reforzado", "Cerradura de llave maestra", "Escritorio táctico"],
                "bonus": "Privacidad absoluta; meditación umbral protegida de miradas ajenas",
                "next": {"title": "Nivel 2: Aislamiento Psico-Acústico & Caja Oculta", "cost_credits": 70, "cost_mats": "Paneles de plomo y espuma acústica", "effect": "Oculta emanaciones psíquicas menores durante el descanso y agrega alijo secreto"}
            },
            2: {
                "title": "Aislamiento Psico-Acústico (Nivel 2)",
                "status": "OPERATIVA", "color": "green",
                "equipment": ["Paneles de plomo en paredes", "Alijo bajo el suelo", "Cerradura biomecánica"],
                "bonus": "Oculta firmas psíquicas de descanso e impide detección mediante auspex externo",
                "next": {"title": "Nivel 3: Sanctum Umbral con Runas de Sombra", "cost_credits": 200, "cost_mats": "4 Placas de obsidiana + Polvo de estasis", "effect": "Permite recuperar +1 Punto de Destino por semana mediante meditación profunda y disipa corrupción"}
            },
            3: {
                "title": "Sanctum Umbral Sellado (Nivel 3 · MÁXIMO)",
                "status": "OPERATIVA", "color": "green",
                "equipment": ["Foco de resonancia de sombra", "Sello de protección disforme", "Alijo reforzado"],
                "bonus": "Recuperación de Puntos de Destino acelerada y protección total contra sondas psíquicas",
                "next": None
            }
        }
    },
    "HAB-02": {
        "is_vital": False,
        "max_level": 3,
        "code": "HAB-02",
        "name": "Dormitorio de Guardia (Severan & Jarek)",
        "type": "living",
        "tiers": {
            1: {
                "title": "Cuartel de Seguridad (Nivel 1)",
                "status": "OPERATIVA", "color": "green",
                "equipment": ["2 Catres de campaña", "Armero de pared cerrado", "Intercomunicador"],
                "bonus": "Tiempo de respuesta de guardias ante intrusiones: Inmediato (1 turno)",
                "next": {"title": "Nivel 2: Acondicionador Térmico & Taquillas Reforzadas", "cost_credits": 50, "cost_mats": "1 Calefactor de chimenea", "effect": "Permite recuperar toda la fatiga del personal de guardia en 4h de reposo"}
            },
            2: {
                "title": "Acondicionador Térmico & Armero Reforzado (Nivel 2)",
                "status": "OPERATIVA", "color": "green",
                "equipment": ["Calefactor radiante", "Taquillas de acero", "Bancos de mantenimiento de armas"],
                "bonus": "Elimina toda la fatiga de Severan y Jarek en solo 4 horas de reposo continuo",
                "next": {"title": "Nivel 3: Puesto Táctico Blindado de Guardia", "cost_credits": 130, "cost_mats": "Placas de blindaje + Tronera de respuesta", "effect": "+1 a la Armadura de todo el personal de seguridad en guardia y armero de recarga rápida"}
            },
            3: {
                "title": "Puesto Táctico Blindado (Nivel 3 · MÁXIMO)",
                "status": "OPERATIVA", "color": "green",
                "equipment": ["Armero blindado de acceso rápido", "Mamparas antibalas interiores", "Monitor de sensores perimetrales"],
                "bonus": "+1 Armadura a guardias en servicio dentro de la base; rearme instantáneo ante alertas",
                "next": None
            }
        }
    },
    "HAB-03": {
        "is_vital": False,
        "max_level": 3,
        "code": "HAB-03",
        "name": "Dormitorio de Personal (Syra & Khepra)",
        "type": "living",
        "tiers": {
            1: {
                "title": "Habitación de Apoyo (Nivel 1)",
                "status": "OPERATIVA", "color": "green",
                "equipment": ["1 Catre estándar", "Estación de recarga de bio-baterías"],
                "bonus": "Descanso y mantenimiento técnico garantizados para la logística de la base",
                "next": {"title": "Nivel 2: Terminal de Consulta y Archivo Clandestino", "cost_credits": 40, "cost_mats": "1 Pantalla fosfórica + cables", "effect": "+10% de velocidad en inventarios y clasificaciones logísticas"}
            },
            2: {
                "title": "Terminal de Archivo & Nicho de Mantenimiento (Nivel 2)",
                "status": "OPERATIVA", "color": "green",
                "equipment": ["Terminal de datos logísticos", "Nicho de recarga de Khepra-9", "Estantes organizados"],
                "bonus": "Aumenta la velocidad de Syra en la contabilidad y el mantenimiento técnico de Khepra",
                "next": {"title": "Nivel 3: Banco de Datos de Necromunda & Estación Ergonómica", "cost_credits": 110, "cost_mats": "1 Banco de datos arcaico + Iluminación cálida", "effect": "Aumenta la ganancia pasiva de información y optimiza consumibles un 15%"}
            },
            3: {
                "title": "Estación Logística Avanzada (Nivel 3 · MÁXIMO)",
                "status": "OPERATIVA", "color": "green",
                "equipment": ["Banco de datos de Necromunda", "Terminal de recarga rápida Mechanicus", "Escritorio archivador"],
                "bonus": "Optimización del 15% en el uso de todos los suministros médicos y logísticos de la base",
                "next": None
            }
        }
    },
    "HAB-04": {
        "is_vital": False,
        "max_level": 3,
        "code": "HAB-04",
        "name": "Dormitorio Clandestino / Colaboradores",
        "type": "living",
        "tiers": {
            0: {
                "title": "Cuarto de Desahogo Sin Acondicionar (Nivel 0)",
                "status": "REQUIERE_LIMPIEZA", "color": "amber",
                "equipment": ["Sin mobiliario", "Escombros de tuberías"],
                "bonus": "Sin uso",
                "next": {"title": "Nivel 1: Acondicionamiento de Catres & Iluminación", "cost_credits": 30, "cost_mats": "Mobiliario simple", "effect": "Habilita alojamiento seguro para 3 colaboradores (Mara, Sael, Ilyra) sin ocupar camas de trauma"}
            },
            1: {
                "title": "Dormitorio de Pasajeros Clandestinos (Nivel 1)",
                "status": "OPERATIVA", "color": "green",
                "equipment": ["3 Catres de campaña", "Lámpara de carburo", "Cortina de separación"],
                "bonus": "Capacidad de alojamiento seguro para 3 personas adicionales",
                "next": {"title": "Nivel 2: Aislamiento de Ventilación & Literas Reforzadas", "cost_credits": 65, "cost_mats": "3 Literas de acero + Filtro de conducto", "effect": "Capacidad ampliada para 6 refugiados o deudores con raciones optimizadas"}
            },
            2: {
                "title": "Cuartel Reforzado para Huéspedes (Nivel 2)",
                "status": "OPERATIVA", "color": "green",
                "equipment": ["3 Literas dobles de acero", "Filtro de aire independiente", "Taquillas de pertenencias"],
                "bonus": "Alojamiento cómodo para 6 personas sin sobrecargar el espacio de la clínica",
                "next": {"title": "Nivel 3: Refugio Hermético Oculto (Habitación de Pánico)", "cost_credits": 150, "cost_mats": "Compuerta de camuflaje + Suministros sellados", "effect": "Totalmente indetectable para registros de Enforcers o escáners auspex exteriores"}
            },
            3: {
                "title": "Habitación de Pánico Camuflada (Nivel 3 · MÁXIMO)",
                "status": "OPERATIVA", "color": "green",
                "equipment": ["Compuerta de camuflaje tras estantería", "Suministro de oxígeno de 48h", "Línea vox interna"],
                "bonus": "Refugio 100% indetectable ante redadas policiales o cazadores de recompensas",
                "next": None
            }
        }
    },
    "COMM-01": {
        "is_vital": False,
        "max_level": 3,
        "code": "COMM-01",
        "name": "Sala Común & Almacén de Víveres",
        "type": "living",
        "tiers": {
            1: {
                "title": "Comedor & Despensa Básica (Nivel 1)",
                "status": "OPERATIVA", "color": "green",
                "equipment": ["Mesa de metal", "Despensa con 48 raciones", "16 botellas de agua 1L"],
                "bonus": "Suministros garantizados para 12 personas durante 4 días",
                "next": {"title": "Nivel 2: Purificador Hidropónico & Cocina de Campo", "cost_credits": 110, "cost_mats": "Filtros + Tubería", "effect": "Generación pasiva de 4 raciones frescas y 4L de agua purificada al día"}
            },
            2: {
                "title": "Purificador Hidropónico & Cocina (Nivel 2)",
                "status": "OPERATIVA", "color": "green",
                "equipment": ["Bandeja de cultivo de hongos nutricionales", "Condensador de humedad", "Hornillo de prometio"],
                "bonus": "Generación pasiva de 4 raciones y 4L de agua pura cada 24 horas",
                "next": {"title": "Nivel 3: Planta de Reciclaje Integral & Dispensador Militar", "cost_credits": 230, "cost_mats": "1 Unidad de destilación pesada + Tanque sellado", "effect": "Autosuficiencia alimentaria e hídrica completa para 20 personas indefinidamente"}
            },
            3: {
                "title": "Planta de Autosuficiencia Nutricional (Nivel 3 · MÁXIMO)",
                "status": "OPERATIVA", "color": "green",
                "equipment": ["Destilador de circuito cerrado", "Dispensador de pasta proteica", "Tanques de agua mineralizada"],
                "bonus": "Autosuficiencia alimentaria total para la base; suministro inagotable de agua pura",
                "next": None
            }
        }
    },
    "SUB-01": {
        "is_vital": False,
        "max_level": 3,
        "code": "SUB-01",
        "name": "Puerta Posterior & Escaleras a Subniveles",
        "type": "fog",
        "tiers": {
            0: {
                "title": "Sector Inexplorado / Niebla de Guerra (Nivel 0)",
                "status": "BLOQUEADO_POR_EXPLORAR", "color": "cyan",
                "equipment": ["Puerta metálica reforzada", "Escaleras descendentes a la oscuridad"],
                "bonus": "Acceso al Subnivel -1 y zonas ocultas de Rho-9",
                "next": {"title": "Nivel 1: Despeje de Acceso & Iluminación Táctica", "cost_credits": 0, "cost_mats": "Orden de Alexander + Lámparas", "effect": "Permite acceder al mapa táctico de las criptas subterráneas"}
            },
            1: {
                "title": "Acceso Subterráneo Operativo (Nivel 1)",
                "status": "OPERATIVO", "color": "green",
                "equipment": ["Lámparas de seguridad en escaleras", "Compuerta con pasador", "Señalizadores de ruta"],
                "bonus": "Acceso libre para patrullas y expediciones al Subnivel -1",
                "next": {"title": "Nivel 2: Montacargas Mecánico de Carga Pesada", "cost_credits": 120, "cost_mats": "1 Cabestrante eléctrico + Guías de acero", "effect": "Permite trasladar maquinaria pesada, generadores y camillas al subnivel sin esfuerzo"}
            },
            2: {
                "title": "Montacargas Mecánico de Carga Pesada (Nivel 2)",
                "status": "OPERATIVO", "color": "green",
                "equipment": ["Plataforma de carga de 2 toneladas", "Motor eléctrico", "Frenos de trinquete"],
                "bonus": "Transporte inmediato de equipo médico pesado y generadores entre la clínica y las criptas",
                "next": {"title": "Nivel 3: Red Ferroviaria Clandestina de Vagonetas", "cost_credits": 260, "cost_mats": "Rieles mineros + 1 Vagoneta motorizada", "effect": "Ruta rápida de transporte y evacuación hacia vertederos profundos y mercados negros"}
            },
            3: {
                "title": "Terminal de Transporte Subterráneo (Nivel 3 · MÁXIMO)",
                "status": "OPERATIVO", "color": "green",
                "equipment": ["Vagoneta motorizada sobre rieles", "Compuerta de túnel blindada", "Desvío a Dust Falls"],
                "bonus": "Transporte rápido de mercancías, heridos y suministros hacia los túneles profundos de Necromunda",
                "next": None
            }
        }
    }
}

class DomainManagementEngine:

    @classmethod
    def _get_state_file(cls) -> str:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(base_dir))
        local_path = os.path.join(project_root, "campaigns", "alexander", "campaign_state.json")
        tmp_path = "/tmp/campaign_state.json"
        if os.path.exists(tmp_path):
            if os.path.exists(local_path):
                if os.path.getmtime(tmp_path) > os.path.getmtime(local_path):
                    return tmp_path
                return local_path
            return tmp_path
        return local_path

    @classmethod
    def _load_domain_data(cls) -> Dict[str, Any]:
        filepath = cls._get_state_file()
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    state = json.load(f)
                    domain = state.get("domain_state", {})
                    upgrades = domain.get("upgrades", {})
                    sublevel = domain.get("sublevel_revealed", {})
                    logs = domain.get("logs", [])
                    chat_events = domain.get("chat_events", [])
                    positions = domain.get("positions", {})
                    chrono = domain.get("chrono", {})
                    
                    merged_upgrades = dict(DEFAULT_UPGRADES)
                    merged_upgrades.update(upgrades)
                    
                    merged_sublevel = dict(DEFAULT_SUBLEVEL_REVEALED)
                    merged_sublevel.update(sublevel)
                    
                    merged_positions = dict(DEFAULT_POSITIONS)
                    merged_positions.update(positions)

                    merged_chrono = dict(DEFAULT_CHRONO)
                    merged_chrono.update(chrono)
                    
                    merged_logs = logs if logs else list(DEFAULT_LOGS)
                    return {
                        "upgrades": merged_upgrades,
                        "sublevel": merged_sublevel,
                        "logs": merged_logs,
                        "chat_events": chat_events,
                        "positions": merged_positions,
                        "chrono": merged_chrono
                    }
            except Exception as e:
                print(f"Error cargando domain_data: {e}")
        return {
            "upgrades": dict(DEFAULT_UPGRADES),
            "sublevel": dict(DEFAULT_SUBLEVEL_REVEALED),
            "logs": list(DEFAULT_LOGS),
            "chat_events": [],
            "positions": dict(DEFAULT_POSITIONS),
            "chrono": dict(DEFAULT_CHRONO)
        }

    @classmethod
    def _save_domain_data(cls, data: Dict[str, Any]):
        filepath = cls._get_state_file()
        state = {}
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    state = json.load(f)
            except Exception:
                pass
        
        state["domain_state"] = {
            "upgrades": data.get("upgrades", DEFAULT_UPGRADES),
            "sublevel_revealed": data.get("sublevel", DEFAULT_SUBLEVEL_REVEALED),
            "logs": data.get("logs", DEFAULT_LOGS)[:35],
            "chat_events": data.get("chat_events", [])[:40],
            "positions": data.get("positions", DEFAULT_POSITIONS),
            "chrono": data.get("chrono", DEFAULT_CHRONO)
        }

        try:
            with open("/tmp/campaign_state.json", "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

        try:
            if not filepath.startswith("/tmp") and os.path.exists(os.path.dirname(filepath)):
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(state, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    @classmethod
    def get_logs(cls) -> List[Dict[str, str]]:
        return cls._load_domain_data()["logs"]

    @classmethod
    def get_live_events(cls) -> Dict[str, Any]:
        data = cls._load_domain_data()
        return {
            "success": True,
            "chrono": data["chrono"],
            "positions": data["positions"],
            "chat_events": data["chat_events"][:15],
            "logs": data["logs"][:15]
        }

    @classmethod
    def sync_chat_event(cls, event_type: str, speaker: str, message: str, target_room: Optional[str] = None, advance_turns: int = 0, advance_minutes: int = 0) -> Dict[str, Any]:
        data = cls._load_domain_data()
        chrono = data["chrono"]
        positions = data["positions"]
        chat_events = data["chat_events"]
        logs = data["logs"]

        # Advance chrono
        if advance_turns > 0:
            chrono["turn"] += advance_turns
            chrono["minute"] = (chrono["minute"] + advance_turns * 5) % 60
            if chrono["minute"] < advance_turns * 5:
                chrono["hour"] = (chrono["hour"] + 1) % 24
        
        if advance_minutes > 0:
            total_mins = chrono["minute"] + advance_minutes
            chrono["minute"] = total_mins % 60
            added_hours = total_mins // 60
            chrono["hour"] = (chrono["hour"] + added_hours) % 24
            if chrono["hour"] < added_hours:
                chrono["day"] += 1

        chrono["phase"] = "CICLO DIURNO" if (6 <= chrono["hour"] < 18) else "VIGILIA NOCTURNA"

        time_str = f"Día {str(chrono['day']).zfill(2)} · {str(chrono['hour']).zfill(2)}:{str(chrono['minute']).zfill(2)}"

        if target_room and speaker in positions:
            positions[speaker] = target_room

        event_entry = {
            "time": time_str,
            "turn": chrono["turn"],
            "type": event_type.upper(),
            "speaker": speaker,
            "message": message,
            "target_room": target_room
        }
        chat_events.insert(0, event_entry)

        log_entry = {
            "time": time_str,
            "type": event_type.upper() if event_type.upper() in ["SECURITY", "MEDICAL", "TECH", "LOGISTICS", "COSECHA", "UPGRADE"] else "EVENT",
            "text": f"[{speaker}] {message}" + (f" -> Traslado a {target_room}" if target_room else "")
        }
        logs.insert(0, log_entry)

        data["chrono"] = chrono
        data["positions"] = positions
        data["chat_events"] = chat_events
        data["logs"] = logs

        cls._save_domain_data(data)

        return {
            "success": True,
            "event": event_entry,
            "chrono": chrono,
            "positions": positions,
            "message": f"Evento de chat sincronizado con éxito. Movimiento aplicado a {speaker}."
        }

    @classmethod
    def get_rho9_status(cls) -> Dict[str, Any]:
        return {
            "domain_id": "DOMAIN-RHO9-001",
            "nombre": "Medicae Station Rho-9",
            "ubicacion": "Caídas de Polvo / Dust Falls, Necromunda",
            "integridad_estructural": 88,
            "nivel_seguridad": 75,
            "calidad_sanitaria": 70,
            "estabilidad_electrica": 80,
            "recursos": {
                "raciones_totales": "48 (24 comunes, 10 militares, 9 médicas, 5 alta nutrición)",
                "agua_purificada": "16 Botellas (1L)",
                "prometio_generador": "80% de carga",
                "camaras_frio_farmacia": "100% Operativo"
            },
            "mando_seguridad": {
                "titular": "Severan Holt",
                "autoridad": "Seguridad perimetral, cerraduras, guardias y fortificación",
                "cap_gasto": "200 Créditos / semana",
                "asistente": "Jarek Venn"
            }
        }

    @classmethod
    def get_rho9_blueprint(cls, floor: int = 0) -> Dict[str, Any]:
        if floor == -1:
            return cls._get_sublevel_blueprint()
        return cls._get_floor0_blueprint()

    @classmethod
    def _get_floor0_blueprint(cls) -> Dict[str, Any]:
        data = cls._load_domain_data()
        upg = data["upgrades"]

        # Calcular métricas dinámicas
        gate_lvl = upg.get("GATE-01", 1)
        e01_lvl = upg.get("E-01", 0)
        q01_lvl = upg.get("Q-01", 1)
        c03_lvl = upg.get("C-03", 2)

        defensa = 75 + (gate_lvl - 1) * 8
        sanidad = 65 + e01_lvl * 10 + (q01_lvl - 1) * 5 + (c03_lvl - 1) * 3

        occupants_map = {
            "GATE-01": ["Jarek Venn (Guardia)", "Severan Holt (Rondas)"],
            "ADM-01": ["Syra Kol (16 años)"],
            "Q-01": ["Alexander (Cirujano)", "Halven Rusk (Asistente)"],
            "C-01": ["Tertius Holt (8/11 · Despierto)"],
            "C-02": ["Libre (En espera de urgencias)"],
            "C-03": ["Quartus Holt (4/11 · Desintubación Activa)"],
            "F-02": ["Syra Kol (Control)", "Alexander (Acceso exclusivo)"],
            "E-01": ["Khepra-9 (Adaptación)"],
            "T-01": ["Khepra-9 (Tecnosacerdote)"],
            "HAB-01": ["Alexander"],
            "HAB-02": ["Severan Holt", "Jarek Venn"],
            "HAB-03": ["Syra Kol", "Khepra-9"],
            "HAB-04": ["Mara Veyl", "Sael Veyl", "Ilyra Venn"] if upg.get("HAB-04", 0) > 0 else ["Cajas y escombros"],
            "COMM-01": ["Punto de reunión del séquito"],
            "SUB-01": ["Ninguno (Presencia desconocida)"]
        }

        sectors = []
        for room_id, defn in ROOM_DEFINITIONS.items():
            lvl = upg.get(room_id, 0 if room_id in ["E-01", "HAB-04", "SUB-01"] else 1)
            tier_info = defn["tiers"].get(lvl, defn["tiers"][min(defn["tiers"].keys())])
            
            sector_obj = {
                "id": room_id,
                "code": defn["code"],
                "name": defn["name"],
                "type": defn["type"],
                "is_vital": defn["is_vital"],
                "max_level": defn["max_level"],
                "level": lvl,
                "level_title": tier_info["title"],
                "status": tier_info["status"],
                "status_color": tier_info["color"],
                "occupants": occupants_map.get(room_id, []),
                "equipment": tier_info["equipment"],
                "bonus": tier_info["bonus"],
                "next_upgrade": tier_info.get("next")
            }
            sectors.append(sector_obj)

        return {
            "floor": 0,
            "floor_name": "Planta 0 // Medicae Station Rho-9 (Clínica Clandestina)",
            "global_metrics": {
                "defensa_perimetral": min(defensa, 100),
                "calidad_sanitaria": min(sanidad, 100),
                "red_electrica": 80,
                "camas_ocupadas": 2,
                "camas_totales": 3,
                "habitaciones_ocupadas": 3,
                "habitaciones_totales": 4
            },
            "sectors": sectors
        }

    @classmethod
    def _get_sublevel_blueprint(cls) -> Dict[str, Any]:
        data = cls._load_domain_data()
        rev = data["sublevel"]

        return {
            "floor": -1,
            "floor_name": "Subnivel -1 // Criptas & Red Subterránea Inexplorada",
            "global_metrics": {
                "sectores_revelados": sum(1 for v in rev.values() if v),
                "sectores_totales": 4,
                "amenaza_ambiental": "Media (Gases tóxicos / Oscuridad total)",
                "estabilidad_tuneles": "70%"
            },
            "sectors": [
                {
                    "id": "SUB-GEN",
                    "code": "SUB-02",
                    "name": "Bóveda de Generador Sumergido",
                    "type": "tech",
                    "is_revealed": rev.get("SUB-GEN", False),
                    "level": 1 if rev.get("SUB-GEN", False) else 0,
                    "level_title": "Generador Antiguo Descubierto" if rev.get("SUB-GEN", False) else "Señal Térmica No Confirmada",
                    "status": "REVELADO" if rev.get("SUB-GEN", False) else "NIEBLA_DE_GUERRA",
                    "status_color": "green" if rev.get("SUB-GEN", False) else "cyan",
                    "occupants": ["Khepra-9 (Asignable)"] if rev.get("SUB-GEN", False) else ["Desconocido"],
                    "equipment": ["Turbina geotérmica arcaica", "Depósito de refrigerante"] if rev.get("SUB-GEN", False) else ["Auspex detecta masa metálica pesada"],
                    "bonus": "Energía ilimitada para toda la clínica si se reactiva" if rev.get("SUB-GEN", False) else "Desconocido",
                    "exploration_cost": "1 Turno de Exploración + Tirada de Percepción"
                },
                {
                    "id": "SUB-TUNNEL",
                    "code": "SUB-03",
                    "name": "Conducto de Escape a Dust Falls",
                    "type": "security",
                    "is_revealed": rev.get("SUB-TUNNEL", False),
                    "level": 1 if rev.get("SUB-TUNNEL", False) else 0,
                    "level_title": "Ruta de Evacuación Segura" if rev.get("SUB-TUNNEL", False) else "Corriente de Aire Frío",
                    "status": "REVELADO" if rev.get("SUB-TUNNEL", False) else "NIEBLA_DE_GUERRA",
                    "status_color": "green" if rev.get("SUB-TUNNEL", False) else "cyan",
                    "occupants": ["Severan Holt (Vigilancia)"] if rev.get("SUB-TUNNEL", False) else ["Desconocido"],
                    "equipment": ["Compuerta de alcantarillado", "Escalera de gato"] if rev.get("SUB-TUNNEL", False) else ["Corriente de aire hacia el exterior"],
                    "bonus": "Ruta de escape indetectable ante un asedio a la clínica" if rev.get("SUB-TUNNEL", False) else "Desconocido",
                    "exploration_cost": "1 Turno de Exploración + Tirada de Sigilo"
                },
                {
                    "id": "SUB-STASIS",
                    "code": "SUB-04",
                    "name": "Cámara de Estasis Pre-Imperial",
                    "type": "medical",
                    "is_revealed": rev.get("SUB-STASIS", False),
                    "level": 1 if rev.get("SUB-STASIS", False) else 0,
                    "level_title": "Sarcófagos de Preservación" if rev.get("SUB-STASIS", False) else "Eco Psíquico / Campo Estático",
                    "status": "REVELADO" if rev.get("SUB-STASIS", False) else "NIEBLA_DE_GUERRA",
                    "status_color": "green" if rev.get("SUB-STASIS", False) else "cyan",
                    "occupants": ["3 Cápsulas selladas (Contenido arcaico)"] if rev.get("SUB-STASIS", False) else ["Presencia biológica latente"],
                    "equipment": ["3 Cápsulas criogénicas funcionales", "Sellos de aislamiento"] if rev.get("SUB-STASIS", False) else ["Interferencia en el auspex"],
                    "bonus": "Capacidad de suspensión a largo plazo para biobanco o sujetos de estudio" if rev.get("SUB-STASIS", False) else "Desconocido",
                    "exploration_cost": "1 Turno de Exploración + Tirada de Voluntad/Psicología"
                },
                {
                    "id": "SUB-CHEM",
                    "code": "SUB-05",
                    "name": "Depósito Químico Olvidado (Escher)",
                    "type": "storage",
                    "is_revealed": rev.get("SUB-CHEM", False),
                    "level": 1 if rev.get("SUB-CHEM", False) else 0,
                    "level_title": "Almacén Clandestino de Narcóticos" if rev.get("SUB-CHEM", False) else "Vapores Dulzones en Tuberías",
                    "status": "REVELADO" if rev.get("SUB-CHEM", False) else "NIEBLA_DE_GUERRA",
                    "status_color": "green" if rev.get("SUB-CHEM", False) else "cyan",
                    "occupants": ["Sin custodios"] if rev.get("SUB-CHEM", False) else ["Posibles alimañas del submundo"],
                    "equipment": ["Contenedores de estimulantes químicos", "Reactores de vidrio"] if rev.get("SUB-CHEM", False) else ["Olor penetrante a químicos volátiles"],
                    "bonus": "+50 Dosis de estimulantes y reactivos para el sintetizador de Alexander" if rev.get("SUB-CHEM", False) else "Desconocido",
                    "exploration_cost": "1 Turno de Exploración + Tirada de Resistencia"
                }
            ]
        }

    @classmethod
    def execute_room_upgrade(cls, room_id: str, available_credits: int) -> Dict[str, Any]:
        data = cls._load_domain_data()
        upgrades = data["upgrades"]
        sublevel = data["sublevel"]
        logs = data["logs"]

        blueprint = cls._get_floor0_blueprint()
        sector = next((s for s in blueprint["sectors"] if s["id"] == room_id), None)
        
        if not sector:
            return {"success": False, "error": f"Sala con ID '{room_id}' no encontrada."}
        
        upgrade = sector.get("next_upgrade")
        if not upgrade:
            max_lvl = sector.get("max_level", 3)
            return {"success": False, "error": f"La sala '{sector['name']}' ya está en su nivel máximo (Nivel {max_lvl})."}
        
        cost = upgrade.get("cost_credits", 0)
        if available_credits < cost:
            return {"success": False, "error": f"Créditos insuficientes ({available_credits} ¤ disponibles, requiere {cost} ¤)."}
        
        current_lvl = upgrades.get(room_id, 0 if room_id in ["E-01", "HAB-04", "SUB-01"] else 1)
        new_lvl = current_lvl + 1
        upgrades[room_id] = new_lvl
        new_credits = available_credits - cost

        log_entry = {
            "time": "Día 04 · Noche",
            "type": "UPGRADE",
            "text": f"¡PROYECTO DE MEJORA EJECUTADO! '{sector['name']}' elevada a Nivel {new_lvl} (Máx: {sector['max_level']}). Coste: -{cost} ¤. Efecto: {upgrade.get('effect')}"
        }
        logs.insert(0, log_entry)

        data["upgrades"] = upgrades
        data["logs"] = logs
        cls._save_domain_data(data)

        return {
            "success": True,
            "room_id": room_id,
            "room_name": sector["name"],
            "new_level": new_lvl,
            "max_level": sector["max_level"],
            "spent_credits": cost,
            "remaining_credits": new_credits,
            "applied_effect": upgrade.get("effect"),
            "log": log_entry,
            "message": f"Mejora completada con éxito: {sector['name']} ahora es Nivel {new_lvl} (de {sector['max_level']})."
        }

    @classmethod
    def explore_sublevel_sector(cls, sector_id: str, actor: str = "Alexander") -> Dict[str, Any]:
        data = cls._load_domain_data()
        upgrades = data["upgrades"]
        sublevel = data["sublevel"]
        logs = data["logs"]

        if sector_id not in sublevel:
            return {"success": False, "error": f"Sector '{sector_id}' no existe en el Subnivel -1."}
        
        sublevel[sector_id] = True

        bp = cls._get_sublevel_blueprint()
        sector = next((s for s in bp["sectors"] if s["id"] == sector_id), None)

        log_entry = {
            "time": "Día 04 · Noche",
            "type": "EXPLORATION",
            "text": f"{actor} exploró los subniveles y despejó la niebla de guerra en '{sector['name']}'. ¡Bono desbloqueado: {sector['bonus']}!"
        }
        logs.insert(0, log_entry)

        data["sublevel"] = sublevel
        data["logs"] = logs
        cls._save_domain_data(data)

        return {
            "success": True,
            "sector_id": sector_id,
            "sector_name": sector["name"],
            "is_revealed": True,
            "bonus": sector["bonus"],
            "log": log_entry,
            "message": f"¡Sector '{sector['name']}' asegurado y despejado de la niebla de guerra!"
        }

    @classmethod
    def assign_staff_task(cls, npc_name: str, task: str) -> Dict[str, Any]:
        data = cls._load_domain_data()
        logs = data["logs"]

        log_entry = {
            "time": "Día 04 · Noche",
            "type": "SECURITY",
            "text": f"ASIGNACIÓN TÁCTICA: {npc_name} reasignado a '{task}'."
        }
        logs.insert(0, log_entry)
        data["logs"] = logs
        cls._save_domain_data(data)

        return {
            "success": True,
            "npc_name": npc_name,
            "task": task,
            "message": f"Orden transmitida: {npc_name} ha asumido el puesto '{task}'."
        }

    @staticmethod
    def collect_weekly_revenue(current_credits: int) -> Dict[str, Any]:
        return {
            "revenue": 0,
            "new_total": current_credits,
            "message": "Rho-9 sigue en cuarentena y cerrada al público; no hay ingresos comerciales externos."
        }
