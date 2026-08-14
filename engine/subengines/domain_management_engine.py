"""
WH40K Domain & Base Management Engine v6.0 (domain_management_engine.py)
Includes:
- Standardized 5/3 Room Upgrade Tree (15 Sectors)
- Intelligent Narrative Text Parser (parse_narrative_to_sync) from ChatGPT
- Full Turn Report Generator (generate_full_turn_report)
- Canonical System Instruction Prompt Generator (generate_chatgpt_system_prompt)
- Chat Synchronization Bridge & Real-time Chrono State Tracking
"""

import json
import os
import re
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

# ROOM DEFINITIONS WITH 5/3 STANDARDIZED UPGRADE TREE
ROOM_DEFINITIONS = {
    "Q-01": {
        "is_vital": True, "max_level": 5, "code": "Q-01", "name": "Quirófano Central de Trauma", "type": "medical",
        "tiers": {
            1: {"title": "Quirófano Parcial Integrado (Nivel 1)", "status": "OPERATIVO", "color": "green", "equipment": ["Diagnostor de espectro (+15% diagnóstico)", "Mesa quirúrgica hidráulica", "Monitores vitales"], "bonus": "+10% ambiental a procedimientos médicos; +15% a diagnóstico dirigido", "next": {"title": "Nivel 2: Circuito de Agua Estéril & Lámparas Articuladas", "cost_credits": 200, "cost_mats": "20m Tubería clínica + 2 Filtros clínicos", "effect": "Eleva el bono ambiental a cirugías a +20% y reduce tiempo operatorio a la mitad"}},
            2: {"title": "Quirófano Aséptico Avanzado (Nivel 2)", "status": "OPERATIVO", "color": "green", "equipment": ["Circuito de agua estéril", "Lámparas cenitales articuladas", "Diagnostor multispectral"], "bonus": "+20% ambiental a cirugías; tiempo operatorio reducido a la mitad", "next": {"title": "Nivel 3: Servobrazo Quirúrgico Mecanizado", "cost_credits": 350, "cost_mats": "1 Servobrazo articulado + 4 Cánulas de vacío", "effect": "Eleva el bono a +30% a cirugías; anula penalizadores por fatiga o temblor del cirujano y permite 2 cirugías simultáneas"}},
            3: {"title": "Quirófano Mecatrónico Asistido (Nivel 3)", "status": "OPERATIVO", "color": "green", "equipment": ["Servobrazo quirúrgico mecanizado", "Inyectores automáticos de coagulante", "Cauterio láser doble"], "bonus": "+30% a cirugías; anula fatiga/temblor del cirujano; permite 2 cirugías simultáneas con Halven", "next": {"title": "Nivel 4: Campo de Estasis Focal Intraoperatorio", "cost_credits": 550, "cost_mats": "1 Generador de campo estático + 2 Células energéticas", "effect": "Suspende el desangrado y la muerte clínica durante la operación (0% riesgo de muerte intraoperatoria)"}},
            4: {"title": "Unidad de Trauma con Campo de Estasis (Nivel 4)", "status": "OPERATIVO", "color": "green", "equipment": ["Emisor de campo de estasis focal", "Monitores de ondas cerebrales", "Líneas de soporte extracorpóreo"], "bonus": "+35% a cirugías; suspende la muerte clínica durante la operación (0% riesgo de parada irreversible)", "next": {"title": "Nivel 5: Sanctum de Biotransferencia & Regeneración Tisular Mayor", "cost_credits": 850, "cost_mats": "1 Núcleo de bio-impresión tisular + Aleaciones biológicas", "effect": "+40% a cirugías, regeneración de extremidades amputadas y transplante de órganos genéticos/biónicos sin rechazo"}},
            5: {"title": "Sanctum de Regeneración Tisular Mayor (Nivel 5 · MÁXIMO)", "status": "OPERATIVO", "color": "green", "equipment": ["Matriz de bio-impresión tisular", "Campo de estasis focal", "Servobrazo de micro-cirugía", "Diagnostor arcaico"], "bonus": "+40% a cirugías; regeneración de miembros amputados e injertos biónicos/genéticos con compatibilidad total", "next": None}
        }
    },
    "GATE-01": {
        "is_vital": True, "max_level": 5, "code": "ACCESO-01", "name": "Compuerta Principal & Perímetro Defensivo", "type": "security",
        "tiers": {
            1: {"title": "Compuerta Acorazada Estándar (Nivel 1)", "status": "OPERATIVO", "color": "green", "equipment": ["Chapa de aleación reforzada", "Cerrojos manuales de presión", "Tronera de tiro simple"], "bonus": "+15% defensa perimetral; posición de cobertura pesada (+20% a esquiva)", "next": {"title": "Nivel 2: Sistema de Esclusa Doble & Cerrojo Hidráulico", "cost_credits": 180, "cost_mats": "4 Placas de aleación + 1 Cilindro hidráulico", "effect": "Eleva la defensa a +25% e impide asaltos directos"}},
            2: {"title": "Esclusa Blindada Doble (Nivel 2)", "status": "OPERATIVO", "color": "green", "equipment": ["Esclusa doble de contención", "Cerrojos hidráulicos", "Troneras de fuego cruzado"], "bonus": "+25% defensa perimetral; elimina riesgo de brecha rápida", "next": {"title": "Nivel 3: Aspilleras Fortificadas con Blindaje de Prometio & Focos", "cost_credits": 300, "cost_mats": "2 Reflectores de alta potencia + 6 Chapas de acero", "effect": "Eleva la defensa a +35%; visión nocturna total sobre el callejón de acceso y +10% a balística defensiva"}},
            3: {"title": "Baluarte Fortificado con Iluminación Táctica (Nivel 3)", "status": "OPERATIVO", "color": "green", "equipment": ["Reflectores de haz estrecho", "Aspilleras de titanio", "Intercomunicador blindado"], "bonus": "+35% defensa; anula penalizadores por oscuridad al disparar hacia el exterior", "next": {"title": "Nivel 4: Torretas Automáticas Servocontroladas de Autogun", "cost_credits": 500, "cost_mats": "2 Autoguns montados + 1 Cogitador de puntería", "effect": "Eleva la defensa a +45%; 2 disparos defensivos automáticos por asalto contra intrusos no autorizados"}},
            4: {"title": "Perímetro Automatizado con Torretas Centinela (Nivel 4)", "status": "OPERATIVO", "color": "green", "equipment": ["2 Torretas autogun servoguiadas", "Cámaras con sensor térmico", "Parrilla de electrificación exterior"], "bonus": "+45% defensa; fuego reactivo automático y descarga eléctrica disuasoria", "next": {"title": "Nivel 5: Bastión Acorazado con Escudo de Vacío de Grado Refugio", "cost_credits": 800, "cost_mats": "1 Generador de escudo de vacío + Bobinas de plasma", "effect": "+60% defensa perimetral; inmunidad a explosivos pesados y asedios prolongados"}},
            5: {"title": "Bastión de Vacío Acorazado (Nivel 5 · MÁXIMO)", "status": "OPERATIVO", "color": "green", "equipment": ["Escudo de vacío perimetral", "Torretas dobles pesadas", "Sistema de esclusa de triple cámara"], "bonus": "+60% defensa perimetral; soporte vital aislado y defensa impenetrable en Dust Falls", "next": None}
        }
    },
    "F-02": {
        "is_vital": True, "max_level": 5, "code": "F-02", "name": "Biobanco Celular & Farmacia Clandestina", "type": "storage",
        "tiers": {
            1: {"title": "Almacén Refrigerado de Fármacos (Nivel 1)", "status": "OPERATIVO", "color": "green", "equipment": ["Nevera química", "Armario ignífugo de reactivos", "Centrifugadora manual"], "bonus": "+5% calidad sanitaria; capacidad para almacenar 50 dosis de stimms/fármacos", "next": {"title": "Nivel 2: Tanques Criogénicos de Órganos & Tejido", "cost_credits": 190, "cost_mats": "1 Tanque criogénico + 2 Líneas de nitrógeno", "effect": "Permite conservar órganos y muestras tisulares sin degradación durante 30 días"}},
            2: {"title": "Biobanco Criogénico de Preservación (Nivel 2)", "status": "OPERATIVO", "color": "green", "equipment": ["Tanques criogénicos de nitrógeno", "Filtros antibacterianos", "Refrigerador de sangre"], "bonus": "+10% calidad sanitaria; conservación indefinida de 10 muestras de órganos y 20 unidades de sangre", "next": {"title": "Nivel 3: Sintetizador Químico Automatizado de Fármacos", "cost_credits": 320, "cost_mats": "1 Alambique de condensación + 2 Sensores de pureza", "effect": "Reduce el coste en créditos de todas las recetas alquímicas en un 20% y añade +10% a síntesis"}},
            3: {"title": "Laboratorio Bio-Químico Automatizado (Nivel 3)", "status": "OPERATIVO", "color": "green", "equipment": ["Sintetizador automático", "Columnas de cromatografía", "Destilador de pureza"], "bonus": "+15% calidad sanitaria; -20% coste de recetas químicas y +10% éxito en síntesis", "next": {"title": "Nivel 4: Incubadora de Cultivos Genéticos & Células Madre", "cost_credits": 520, "cost_mats": "1 Matriz de cultivo celular + Calefactores de precisión", "effect": "Genera 1 unidad de tejido regenerativo o muestra de sangre purificada cada 48 horas de forma pasiva"}},
            4: {"title": "Bio-Incubadora de Clonación Tisular (Nivel 4)", "status": "OPERATIVO", "color": "green", "equipment": ["Incubadora de tejidos vivos", "Tanques de nutrientes orgánicos", "Banco de plasma sellado"], "bonus": "+20% calidad sanitaria; producción pasiva de injertos tisulares y +15% éxito en cirugías", "next": {"title": "Nivel 5: Arca Biológica Ancestral de Purificación Celular", "cost_credits": 780, "cost_mats": "1 Replicador celular arqueotecnológico", "effect": "+30% calidad sanitaria; producción pasiva de fármacos raros e inmunidad absoluta a mutaciones/toxinas"}},
            5: {"title": "Arca Biológica Ancestral (Nivel 5 · MÁXIMO)", "status": "OPERATIVO", "color": "green", "equipment": ["Matriz arqueotecnológica de réplica celular", "Depósito hermético de bio-plasma"], "bonus": "+30% calidad sanitaria; sintetiza compuestos únicos sin coste de reactivos", "next": None}
        }
    },
    "T-01": {
        "is_vital": True, "max_level": 5, "code": "T-01", "name": "Taller Mecatrónico de Khepra-9", "type": "tech",
        "tiers": {
            1: {"title": "Banco de Trabajo Mecatrónico (Nivel 1)", "status": "OPERATIVO", "color": "green", "equipment": ["Torno manual de precisión", "Soldador de plasma de arco", "Herramientas de relojero"], "bonus": "Permite reparar armas dañadas, ensamblar prótesis básicas y mantener la red de plasma", "next": {"title": "Nivel 2: Torno Mecánico & Estación de Soldadura de Precisión", "cost_credits": 175, "cost_mats": "1 Motor de torno + 2 Bobinas de estaño", "effect": "+10% a tiradas de tecnología y permite fabricar munición especializada (+1 daño)"}},
            2: {"title": "Taller Mecánico de Precisión (Nivel 2)", "status": "OPERATIVO", "color": "green", "equipment": ["Torno industrial", "Soldador láser", "Analizador de circuitos ópticos"], "bonus": "+10% a tiradas técnicas de Khepra-9; permite fabricar munición reforzada", "next": {"title": "Nivel 3: Fragua de Aleaciones Pesadas & Banco de Calibración de Biónicos", "cost_credits": 310, "cost_mats": "1 Crisol de inducción + 4 Placas de aleación pesada", "effect": "+20% a tiradas técnicas; permite forjar implantes biónicos avanzados (Ojo auspex, extremidades reforzadas)"}},
            3: {"title": "Fragua Cibernética de Precisión (Nivel 3)", "status": "OPERATIVO", "color": "green", "equipment": ["Crisol de inducción magnética", "Banco de calibración neural", "Impresora de piezas de titanio"], "bonus": "+20% a tecnología; desbloquea prótesis biónicas de combate e implantes auspex", "next": {"title": "Nivel 4: Servotaller Automatizado del Adeptus Mechanicus", "cost_credits": 490, "cost_mats": "1 Unidad lógica mecatrónica + 2 Servobrazos de ensamblaje", "effect": "+30% a tecnología; reduce a la mitad el tiempo de fabricación y mejora armaduras con +1 PA"}},
            4: {"title": "Servofactoría del Dios Máquina (Nivel 4)", "status": "OPERATIVO", "color": "green", "equipment": ["Servobrazos de montaje automatizado", "Bancos de prueba de plasma", "Cámara de blindaje térmico"], "bonus": "+30% a tecnología; blindaje de armaduras (+1 PA permanente) y mantenimiento autónomo", "next": {"title": "Nivel 5: Forja Sacra Omnissiah de Alta Complejidad", "cost_credits": 750, "cost_mats": "1 Núcleo de cogitador sagrado + Bobinas de energía pura", "effect": "+40% a tecnología; capacidad para fabricar armas de plasma, implantes cibernéticos maestros y servo-armaduras ligeras"}},
            5: {"title": "Forja Sacra Omnissiah (Nivel 5 · MÁXIMO)", "status": "OPERATIVO", "color": "green", "equipment": ["Matriz de forja sacra", "Ensamblador cuántico de biónicos", "Reactor de calibración neural"], "bonus": "+40% a tecnología; forja de arqueotecnología y cibernética de grado maestro", "next": None}
        }
    },
    "C-03": {
        "is_vital": True, "max_level": 5, "code": "CAMA-03", "name": "Cama de Cuidados Críticos (Quartus Holt)", "type": "recovery",
        "tiers": {
            1: {"title": "Cama de Monitoreo Básico (Nivel 1)", "status": "OPERATIVO", "color": "green", "equipment": ["Monitor cardíaco simple", "Gotero IV", "Soporte de oxígeno"], "bonus": "+1 PV/día a pacientes ingresados", "next": {"title": "Nivel 2: Sistema de Soporte Vital & Perfusión Tisular Continua", "cost_credits": 150, "cost_mats": "1 Bomba de perfusión + 1 Tubo endotraqueal", "effect": "Mantiene con vida a pacientes en coma profundo e incrementa recuperación a +2 PV/día"}},
            2: {"title": "Cama con Soporte Vital & Perfusión Tisular (Nivel 2 · ACTUAL)", "status": "OPERATIVO", "color": "green", "equipment": ["Bomba de perfusión continua", "Respirador asistido", "Monitor de presión intracraneal", "Línea de suero balanceada"], "bonus": "Mantiene con vida a Quartus Holt (4/11 PV) sin riesgo de muerte por asfixia; +2 PV/día en recuperación", "next": {"title": "Nivel 3: Cápsula de Bio-Regeneración Acelerada con Nutrientes Químicos", "cost_credits": 260, "cost_mats": "1 Cúpula de estanqueidad + 2 Válvulas dosificadoras", "effect": "Acelera el despertar de pacientes en coma a la mitad del tiempo (+3 PV/día)"}},
            3: {"title": "Cápsula de Bio-Regeneración Acelerada (Nivel 3)", "status": "OPERATIVO", "color": "green", "equipment": ["Cúpula hermética transparente", "Dosificador neuroquímico", "Calefactor térmico tisular"], "bonus": "+3 PV/día; reduce el tiempo de coma a la mitad y acelera la recuperación de Quartus", "next": {"title": "Nivel 4: Tanque de Inmersión Médica de Lento Estasis", "cost_credits": 420, "cost_mats": "1 Tanque de inmersión en gel + Filtros de perfusión", "effect": "Curación completa de daños orgánicos severos en 48 horas (+4 PV/día)"}},
            4: {"title": "Tanque de Inmersión en Gel Médico (Nivel 4)", "status": "OPERATIVO", "color": "green", "equipment": ["Tanque de gel con oxígeno disuelto", "Monitores neuronales profundos"], "bonus": "+4 PV/día; reparación celular total y regeneración sin cicatrices", "next": {"title": "Nivel 5: Sarcófago Biogénico de Restauración Total", "cost_credits": 680, "cost_mats": "1 Sarcófago de curación arqueotecnológico", "effect": "Restaura la salud completa y anula todas las secuelas de traumas críticos en 24 horas"}},
            5: {"title": "Sarcófago Biogénico de Restauración (Nivel 5 · MÁXIMO)", "status": "OPERATIVO", "color": "green", "equipment": ["Sarcófago de biotransferencia", "Matriz neural de regeneración"], "bonus": "Restaura salud total y elimina secuelas críticas en 24 horas", "next": None}
        }
    },
    # === SALAS ESTÁNDAR (3 NIVELES MÁXIMO) ===
    "E-01": {
        "is_vital": False, "max_level": 3, "code": "E-01", "name": "Cámara de Esterilización & Filtros Asépticos", "type": "medical",
        "tiers": {
            0: {"title": "Inoperativa / Sin Filtros (Nivel 0)", "status": "PENDIENTE", "color": "text-dim", "equipment": ["Autoclave desconectado", "Filtros colmatados"], "bonus": "Riesgo de infección en cirugías mayores (10%)", "next": {"title": "Nivel 1: Autoclave Químico Operativo & Lámpara UV", "cost_credits": 120, "cost_mats": "1 Lámpara UV + 2 Válvulas de presión", "effect": "+15% calidad sanitaria de la clínica y elimina riesgo de sepsis postoperatoria"}},
            1: {"title": "Autoclave Químico & Lámpara UV (Nivel 1)", "status": "OPERATIVO", "color": "green", "equipment": ["Autoclave de calor seco", "Lámpara UV germicida", "Lavabo aséptico"], "bonus": "+15% calidad sanitaria; reduce riesgo de infección al 0%", "next": {"title": "Nivel 2: Sistema de Desinfección por Vapor & Filtros HEPA", "cost_credits": 220, "cost_mats": "2 Filtros HEPA de flujo laminar + Bomba de vapor", "effect": "+25% calidad sanitaria y otorga +5% pasivo a todas las operaciones en Q-01"}},
            2: {"title": "Cámara Aséptica con Filtros HEPA (Nivel 2)", "status": "OPERATIVO", "color": "green", "equipment": ["Filtros HEPA", "Ducha de descontaminación química", "Esterilizador ultrasónico"], "bonus": "+25% calidad sanitaria; +5% pasivo a cirugías en Q-01", "next": {"title": "Nivel 3: Esclusa de Descontaminación de Grado Laboratorio Spire", "cost_credits": 350, "cost_mats": "1 Esclusa presurizada + Sensores biológicos", "effect": "+35% calidad sanitaria e inmunidad total de la base a patógenos aéreos del sumidero"}},
            3: {"title": "Esclusa Aséptica Grado Spire (Nivel 3 · MÁXIMO)", "status": "OPERATIVO", "color": "green", "equipment": ["Esclusa presurizada", "Esterilización molecular", "Filtros de carbono activo"], "bonus": "+35% calidad sanitaria; purificación total del aire de Rho-9", "next": None}
        }
    },
    "ADM-01": {
        "is_vital": False, "max_level": 3, "code": "ADM-01", "name": "Recepción & Cogitador Logístico (Syra Kol)", "type": "logistics",
        "tiers": {
            1: {"title": "Terminal Cogitador Básico (Nivel 1)", "status": "OPERATIVO", "color": "green", "equipment": ["Terminal de pantalla de fósforo verde", "Archivo de placas de datos", "Archivador blindado"], "bonus": "Control del inventario de Sombra Infinita y contabilidad", "next": {"title": "Nivel 2: Matriz Vox de Intercepción & Banco de Datos Encriptor", "cost_credits": 140, "cost_mats": "1 Antena receptora + 2 Cintas de datos magnéticas", "effect": "Permite interceptar transmisiones de Enforcers y bandas rivales con 1 hora de anticipación"}},
            2: {"title": "Centro Vox de Intercepción & Criptografía (Nivel 2)", "status": "OPERATIVO", "color": "green", "equipment": ["Matriz vox omnidireccional", "Descifrador lógico", "Banco de identidades"], "bonus": "Alerta temprana de redadas o movimientos hostiles", "next": {"title": "Nivel 3: Cogitador Táctico Maestro con Vínculo a la Red del Spire", "cost_credits": 280, "cost_mats": "1 Núcleo de cogitador de cobre + Vínculo óptico", "effect": "Acceso a registros de deudas del submundo, precios de mercado en tiempo real y +10% a favores ganados"}},
            3: {"title": "Cogitador Táctico de Red Maestro (Nivel 3 · MÁXIMO)", "status": "OPERATIVO", "color": "green", "equipment": ["Cogitador de cobre integrado", "Banco de holoproyector", "Transmisor seguro"], "bonus": "Inteligencia completa del submundo de Dust Falls y +10% beneficios económicos", "next": None}
        }
    },
    "COMM-01": {
        "is_vital": False, "max_level": 3, "code": "COMM-01", "name": "Sala Común, Cocina & Distribución de Raciones", "type": "living",
        "tiers": {
            1: {"title": "Cocina Rústica de Campaña (Nivel 1)", "status": "OPERATIVO", "color": "green", "equipment": ["Hornillo de prometio", "Mesa metálica", "Despensa con 24 raciones comunes"], "bonus": "Sustento básico para 6 personas del séquito", "next": {"title": "Nivel 2: Purificador de Agua de Condensación & Almacén Seguro", "cost_credits": 130, "cost_mats": "1 Filtro de agua + 1 Depósito hermético", "effect": "Genera +4 botellas de agua potable al día y reduce consumo de raciones un 25%"}},
            2: {"title": "Comedor Equipado con Purificador de Agua (Nivel 2)", "status": "OPERATIVO", "color": "green", "equipment": ["Purificador de agua de condensación", "Despensa sellada", "Mesa de recreo"], "bonus": "+4L agua purificada/día; -25% gasto de raciones; mejora moral del séquito", "next": {"title": "Nivel 3: Reconstituidor Nutricional Automatizado de Alta Calidad", "cost_credits": 250, "cost_mats": "1 Reconstituidor de almidón + Dispensador de calor", "effect": "Produce raciones médicas de alta energía (+1 PV diario pasivo al séquito que descanse)"}},
            3: {"title": "Cantina Reconstituidora de Alta Nutrición (Nivel 3 · MÁXIMO)", "status": "OPERATIVO", "color": "green", "equipment": ["Reconstituidor nutricional", "Purificador industrial", "Mobiliario confortable"], "bonus": "+1 PV pasivo/día al séquito descansando; autosuficiencia hídrica y alimentaria", "next": None}
        }
    },
    "HAB-01": {
        "is_vital": False, "max_level": 3, "code": "HAB-01", "name": "Sanctum Privado de Alexander", "type": "living",
        "tiers": {
            1: {"title": "Dormitorio de Operador (Nivel 1)", "status": "OPERATIVO", "color": "green", "equipment": ["Catrecillo", "Cofre con candado biométrico", "Lámpara de aceite"], "bonus": "Descanso y recuperación normal de fatiga para Alexander", "next": {"title": "Nivel 2: Cámara de Meditación Umbral con Velas de Sebo & Relicario", "cost_credits": 160, "cost_mats": "1 Relicario de latón + Velas santificadas", "effect": "Restaura +1 punto de Reserva Umbral por descanso nocturno completo"}},
            2: {"title": "Cámara de Meditación Umbral (Nivel 2)", "status": "OPERATIVO", "color": "green", "equipment": ["Altar de meditación umbral", "Cofre sellado", "Inciensario"], "bonus": "+1 Alma restaurada a Reserva Umbral tras descanso nocturno completo", "next": {"title": "Nivel 3: Sanctum Hermético con Foco de Resonancia Psíquica", "cost_credits": 300, "cost_mats": "1 Espejo de cristal negro + Círculo de sal purificada", "effect": "Permite almacenar hasta 15 Almas (en vez de 10) y otorga +10 a Voluntad en tiradas umbrales"}},
            3: {"title": "Sanctum Hermético Resonante (Nivel 3 · MÁXIMO)", "status": "OPERATIVO", "color": "green", "equipment": ["Círculo de resonancia umbral", "Armario de grimorios", "Cama con dosel aislante"], "bonus": "Límite de Reserva Umbral aumentado a 15 Almas; +10 a tiradas psíquicas/umbrales", "next": None}
        }
    },
    "HAB-02": {
        "is_vital": False, "max_level": 3, "code": "HAB-02", "name": "Dormitorio de Guardia & Armero (Severan Holt)", "type": "living",
        "tiers": {
            1: {"title": "Barracón Básico con Armero (Nivel 1)", "status": "OPERATIVO", "color": "green", "equipment": ["2 Literas metálicas", "Armero de pared", "Caja de munición"], "bonus": "Alojamiento para Severan Holt y Jarek Venn", "next": {"title": "Nivel 2: Armero Reforzado con Cerrojo Temporal & Banco de Limpieza", "cost_credits": 140, "cost_mats": "1 Armero de chapa + 1 Kit de mantenimiento de armas", "effect": "Todas las armas del séquito ganan la regla Fiable (+0 encasquillamiento) y +5m de alcance"}},
            2: {"title": "Armero Reforzado & Taller Balístico (Nivel 2)", "status": "OPERATIVO", "color": "green", "equipment": ["Armero con clave", "Banco de engrase", "Esteras acolchadas"], "bonus": "Armas del séquito ganan regla Fiable; moral de combate elevada", "next": {"title": "Nivel 3: Puesto de Mando Táctico & Monitores de Vigilancia", "cost_credits": 260, "cost_mats": "2 Pantallas CRT + Cable coaxial de seguridad", "effect": "Severan reacciona al instante a cualquier ataque (+20 a Iniciativa de guardia)"}},
            3: {"title": "Puesto de Mando Táctico Integrado (Nivel 3 · MÁXIMO)", "status": "OPERATIVO", "color": "green", "equipment": ["Consola de vigilancia perimetral", "Armero reforzado de titanio", "Literas militares"], "bonus": "+20 a Iniciativa defensiva; tiempo de respuesta armada inmediato", "next": None}
        }
    },
    "HAB-03": {
        "is_vital": False, "max_level": 3, "code": "HAB-03", "name": "Dormitorio de Técnicos (Syra Kol & Khepra-9)", "type": "living",
        "tiers": {
            1: {"title": "Aposento Doble Mixto (Nivel 1)", "status": "OPERATIVO", "color": "green", "equipment": ["Litera doble", "Toma de recarga de plasma", "Escritorio de lectura"], "bonus": "Alojamiento y recarga para Khepra y Syra", "next": {"title": "Nivel 2: Estación de Recarga Galvánica & Escritorio Iluminado", "cost_credits": 130, "cost_mats": "1 Acumulador galvánico + 1 Foco articulado", "effect": "Khepra trabaja un 30% más rápido en reparaciones y Syra duplica su velocidad de archivo"}},
            2: {"title": "Estación Galvánica & Archivo Técnico (Nivel 2)", "status": "OPERATIVO", "color": "green", "equipment": ["Conector galvánico directo", "Archivador metálico", "Cama cómoda"], "bonus": "+30% velocidad de trabajo para Khepra y Syra", "next": {"title": "Nivel 3: Sanctum Tecnológico con Enlace de Datos & Aislamiento Acústico", "cost_credits": 240, "cost_mats": "1 Terminal de sub-red + Paneles de insonorización", "effect": "+10% pasivo a todas las tiradas de tecnología y logística de la base"}},
            3: {"title": "Sanctum Tecnológico Insonorizado (Nivel 3 · MÁXIMO)", "status": "OPERATIVO", "color": "green", "equipment": ["Enlace neural mecatrónico", "Mobiliario ergonómico"], "bonus": "+10% a todas las tiradas técnicas y de abastecimiento de la base", "next": None}
        }
    },
    "HAB-04": {
        "is_vital": False, "max_level": 3, "code": "HAB-04", "name": "Refugio Clandestino / Celda de Contención Oculta", "type": "living",
        "tiers": {
            0: {"title": "Cámara en Desuso (Nivel 0)", "status": "PENDIENTE", "color": "text-dim", "equipment": ["Escombros", "Puerta desvencijada"], "bonus": "Sin uso activo", "next": {"title": "Nivel 1: Cámara de Aislamiento con Paredes Insonorizadas", "cost_credits": 110, "cost_mats": "Placas de aislamiento acústico + Cerrojo exterior", "effect": "Permite alojar a 2 fugitivos de alto valor o interrogar prisioneros sin ruido exterior"}},
            1: {"title": "Celda Insonorizada de Seguridad (Nivel 1)", "status": "OPERATIVO", "color": "green", "equipment": ["Paredes insonorizadas", "Argollas de sujeción", "Puerta blindada"], "bonus": "Contención segura de 2 prisioneros o refugio para VIPs", "next": {"title": "Nivel 2: Sistema de Extracción de Aire Filtrado & Rejas Electrificadas", "cost_credits": 200, "cost_mats": "1 Reja electrificada + 1 Filtro de escape", "effect": "0% probabilidad de fuga e inmunidad a rastreo por perros o auspex exterior"}},
            2: {"title": "Celda de Contención de Alta Seguridad (Nivel 2)", "status": "OPERATIVO", "color": "green", "equipment": ["Rejas electrificadas", "Conductos con trampa de gas", "Monitores ocultos"], "bonus": "Imposible de rastrear desde el exterior; 0% fugas", "next": {"title": "Nivel 3: Búnker de Máxima Seguridad con Trampilla de Escape Secreta", "cost_credits": 320, "cost_mats": "1 Trampilla oculta con contrapeso + Blindaje plomado", "effect": "Sirve como refugio final indetectable en caso de redada total de los Enforcers"}},
            3: {"title": "Búnker de Escape Hermético (Nivel 3 · MÁXIMO)", "status": "OPERATIVO", "color": "green", "equipment": ["Trampilla de escape a subnivel", "Blindaje plomado anti-auspex"], "bonus": "Refugio indetectable para todo el séquito en caso de asedio", "next": None}
        }
    },
    "C-01": {
        "is_vital": False, "max_level": 3, "code": "CAMA-01", "name": "Cama de Recuperación Post-Operatoria (Tertius Holt)", "type": "recovery",
        "tiers": {
            1: {"title": "Cama Clínica Estándar (Nivel 1)", "status": "OPERATIVO", "color": "green", "equipment": ["Colchón sanitario", "Soporte de drenaje pleural", "Mesa auxiliar"], "bonus": "+1 PV/día a pacientes ingresados (Tertius en 8/11 PV)", "next": {"title": "Nivel 2: Cama Articulada con Monitor de Signos Vitales & Sedación", "cost_credits": 120, "cost_mats": "1 Monitor multiparamétrico + 1 Regulador IV", "effect": "Aumenta la recuperación a +2 PV/día y previene crisis de dolor"}},
            2: {"title": "Cama Articulada con Monitorización Continua (Nivel 2)", "status": "OPERATIVO", "color": "green", "equipment": ["Monitor multiparamétrico", "Bomba de infusión analgésica"], "bonus": "+2 PV/día; estabilización rápida de pacientes traumatizados", "next": {"title": "Nivel 3: Unidad de Recuperación Acelerada con Lámparas de Calor Bio-Térmico", "cost_credits": 220, "cost_mats": "1 Lámpara bio-térmica infrarroja + Colchón anti-escaras", "effect": "Aumenta la curación a +3 PV/día y cicatriza heridas torácicas en tiempo récord"}},
            3: {"title": "Unidad de Recuperación Bio-Térmica (Nivel 3 · MÁXIMO)", "status": "OPERATIVO", "color": "green", "equipment": ["Lámpara infrarroja", "Colchón de presión variable"], "bonus": "+3 PV/día; cicatriza heridas graves en 48 horas", "next": None}
        }
    },
    "C-02": {
        "is_vital": False, "max_level": 3, "code": "CAMA-02", "name": "Cama de Triaje & Urgencias Nocturnas", "type": "recovery",
        "tiers": {
            1: {"title": "Camilla de Triaje Inmediato (Nivel 1)", "status": "OPERATIVO", "color": "green", "equipment": ["Camilla metálica de ruedas", "Bandeja de suturas rápidas", "Torniquetes"], "bonus": "Permite estabilizar de inmediato a heridos recién llegados de la compuerta", "next": {"title": "Nivel 2: Puesto de Estabilización con Suero & Aspirador de Fluidos", "cost_credits": 110, "cost_mats": "1 Bomba de succión manual + 2 Bolsas de salina", "effect": "Anula el riesgo de muerte por shock en los primeros 10 minutos de ingreso"}},
            2: {"title": "Puesto de Reanimación Rápida (Nivel 2)", "status": "OPERATIVO", "color": "green", "equipment": ["Aspirador de fluidos", "Desfibrilador galvánico manual", "Línea IV"], "bonus": "Anula shock inicial y reduce penalizadores de urgencia", "next": {"title": "Nivel 3: Módulo de Trauma Autónomo con Inyectores de Emergencia", "cost_credits": 210, "cost_mats": "1 Inyector neumático de adrenalina + Monitor portátil", "effect": "+20% de éxito en cualquier intervención realizada en los primeros 5 minutos"}},
            3: {"title": "Módulo de Trauma Inmediato (Nivel 3 · MÁXIMO)", "status": "OPERATIVO", "color": "green", "equipment": ["Inyector neumático", "Monitor de telemetría portátil"], "bonus": "+20% a tiradas médicas de urgencia inmediata", "next": None}
        }
    },
    "SUB-01": {
        "is_vital": False, "max_level": 3, "code": "SUB-01", "name": "Acceso a Subniveles & Bóvedas Inexploradas", "type": "fog",
        "tiers": {
            0: {"title": "Escotilla Sellada con Soldadura (Nivel 0)", "status": "PENDIENTE", "color": "text-dim", "equipment": ["Escotilla de hierro corroída", "Candado pesado oxidado"], "bonus": "Acceso bloqueado a las criptas inferiores", "next": {"title": "Nivel 1: Desbloqueo de Escotilla con Cabestrante & Escalera de Acero", "cost_credits": 130, "cost_mats": "1 Cabestrante manual + 15m Cable de acero", "effect": "Permite descender al Subnivel -1 y comenzar la exploración de las 4 bóvedas"}},
            1: {"title": "Escotilla Desbloqueada con Escalera Mecánica (Nivel 1)", "status": "OPERATIVO", "color": "green", "equipment": ["Escalera de acero fija", "Polea de carga", "Farol de carburo"], "bonus": "Permite expediciones al Subnivel -1", "next": {"title": "Nivel 2: Montacargas Mecanizado de Carga & Línea Eléctrica", "cost_credits": 230, "cost_mats": "1 Motor de elevación + 30m Cable eléctrico", "effect": "Permite subir maquinaria pesada y chatarra desde los subniveles con 0 riesgo"}},
            2: {"title": "Montacargas Industrial a Subnivel (Nivel 2)", "status": "OPERATIVO", "color": "green", "equipment": ["Montacargas con motor eléctrico", "Iluminación de pozo", "Sensor de gas"], "bonus": "Extracción rápida de botín y maquinaria del subnivel", "next": {"title": "Nivel 3: Sistema de Túneles Reforzados con Compuerta Blindada Inferior", "cost_credits": 340, "cost_mats": "4 Vigas de sostenimiento + Compuerta neumática", "effect": "Asegura el subnivel de intrusiones de mutantes del sumidero y conecta con túneles de escape"}},
            3: {"title": "Complejo Subterráneo Fortificado (Nivel 3 · MÁXIMO)", "status": "OPERATIVO", "color": "green", "equipment": ["Compuerta neumática inferior", "Vigas de refuerzo", "Sensor auspex de vibración"], "bonus": "Defensa perimetral inferior impenetrable y ruta de escape segura", "next": None}
        }
    }
}

class DomainManagementEngine:

    _memory_cache = None

    @classmethod
    def _get_storage_path(cls) -> str:
        primary = os.path.join(os.path.dirname(__file__), "..", "..", "campaigns", "alexander", "domain_state.json")
        try:
            test_dir = os.path.dirname(primary)
            os.makedirs(test_dir, exist_ok=True)
            test_file = os.path.join(test_dir, ".write_test")
            with open(test_file, "w") as f:
                f.write("ok")
            os.remove(test_file)
            return primary
        except Exception:
            return os.path.join("/tmp", "domain_state.json")

    @classmethod
    def _load_domain_data(cls) -> Dict[str, Any]:
        if cls._memory_cache is not None:
            return dict(cls._memory_cache)
        path = cls._get_storage_path()
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    cls._memory_cache = json.load(f)
                    return dict(cls._memory_cache)
            except Exception:
                pass
        default_data = {
            "upgrades": dict(DEFAULT_UPGRADES),
            "sublevel": dict(DEFAULT_SUBLEVEL_REVEALED),
            "positions": dict(DEFAULT_POSITIONS),
            "chrono": dict(DEFAULT_CHRONO),
            "logs": list(DEFAULT_LOGS),
            "chat_events": []
        }
        cls._memory_cache = default_data
        return dict(default_data)

    @classmethod
    def _save_domain_data(cls, data: Dict[str, Any]):
        cls._memory_cache = dict(data)
        try:
            path = cls._get_storage_path()
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    @classmethod
    def sync_chat_event(cls, event_type: str, speaker: str, message: str, target_room: Optional[str] = None, advance_turns: int = 0, advance_minutes: int = 0) -> Dict[str, Any]:
        data = cls._load_domain_data()
        chrono = data.get("chrono", DEFAULT_CHRONO)
        positions = data.get("positions", DEFAULT_POSITIONS)
        chat_events = data.get("chat_events", [])
        logs = data.get("logs", DEFAULT_LOGS)

        if advance_turns > 0:
            chrono["turn"] = chrono.get("turn", 918) + advance_turns
            chrono["minute"] = (chrono.get("minute", 54) + (advance_turns * 5)) % 60
            if chrono["minute"] < (advance_turns * 5):
                chrono["hour"] = (chrono.get("hour", 23) + 1) % 24
                if chrono["hour"] == 0:
                    chrono["day"] = chrono.get("day", 4) + 1
        elif advance_minutes > 0:
            chrono["minute"] = (chrono.get("minute", 54) + advance_minutes) % 60
            if chrono["minute"] < advance_minutes:
                chrono["hour"] = (chrono.get("hour", 23) + 1) % 24
                if chrono["hour"] == 0:
                    chrono["day"] = chrono.get("day", 4) + 1

        chrono["phase"] = "CICLO DIURNO" if (6 <= chrono.get("hour", 23) < 18) else "VIGILIA NOCTURNA"

        if target_room and speaker in positions:
            positions[speaker] = target_room
        elif target_room and speaker:
            positions[speaker] = target_room

        timestamp_str = f"Día {chrono.get('day', 4):02d} · {chrono.get('hour', 23):02d}:{chrono.get('minute', 54):02d}"

        event_item = {
            "time": timestamp_str,
            "turn": chrono.get("turn", 918),
            "type": event_type,
            "speaker": speaker,
            "message": message,
            "target_room": target_room
        }
        chat_events.insert(0, event_item)
        if len(chat_events) > 50:
            chat_events = chat_events[:50]

        log_item = {
            "time": timestamp_str,
            "type": "SECURITY" if event_type in ["MOVEMENT", "ALERT"] else "MEDICAL",
            "text": f"[{speaker}] {message}"
        }
        logs.insert(0, log_item)
        if len(logs) > 50:
            logs = logs[:50]

        data["chrono"] = chrono
        data["positions"] = positions
        data["chat_events"] = chat_events
        data["logs"] = logs
        cls._save_domain_data(data)

        return {
            "success": True,
            "event": event_item,
            "chrono": chrono,
            "positions": positions,
            "message": f"Evento sincronizado: [{speaker}] {message}"
        }

    @classmethod
    def get_live_events(cls) -> Dict[str, Any]:
        data = cls._load_domain_data()
        return {
            "chrono": data.get("chrono", DEFAULT_CHRONO),
            "positions": data.get("positions", DEFAULT_POSITIONS),
            "chat_events": data.get("chat_events", []),
            "logs": data.get("logs", DEFAULT_LOGS)
        }

    @classmethod
    def parse_narrative_to_sync(cls, raw_text: str) -> Dict[str, Any]:
        """
        Interpreta un fragmento de texto narrativo del rol en ChatGPT,
        extrayendo personajes, salas de destino, diálogos y avances de turno.
        """
        text_lower = raw_text.lower()
        events_found = []
        
        # Character map
        char_names = {
            "alexander": "Alexander",
            "severan": "Severan Holt",
            "khepra": "Khepra-9",
            "syra": "Syra Kol",
            "halven": "Halven Rusk",
            "jarek": "Jarek Venn",
            "tertius": "Tertius Holt",
            "quartus": "Quartus Holt"
        }

        # Room map
        room_keywords = {
            "compuerta": "GATE-01",
            "puerta": "GATE-01",
            "perímetro": "GATE-01",
            "quirófano": "Q-01",
            "cirugía": "Q-01",
            "trauma": "Q-01",
            "taller": "T-01",
            "forja": "T-01",
            "biónico": "T-01",
            "farmacia": "F-02",
            "biobanco": "F-02",
            "almacén": "F-02",
            "esterilización": "E-01",
            "filtro": "E-01",
            "autoclave": "E-01",
            "recepción": "ADM-01",
            "administración": "ADM-01",
            "vox": "ADM-01",
            "comedor": "COMM-01",
            "sala común": "COMM-01",
            "sanctum": "HAB-01",
            "dormitorio de alexander": "HAB-01",
            "cama tertius": "C-01",
            "cama triaje": "C-02",
            "cama quartus": "C-03",
            "subnivel": "SUB-01",
            "criptas": "SUB-01"
        }

        detected_speaker = "Alexander"
        detected_room = None
        for key, full_name in char_names.items():
            if key in text_lower:
                detected_speaker = full_name
                break

        for rk, r_id in room_keywords.items():
            if rk in text_lower:
                detected_room = r_id
                break

        # Dialogue quote search
        dialogue_match = re.search(r'["«]([^"»]+)["»]', raw_text)
        extracted_dialogue = dialogue_match.group(1) if dialogue_match else raw_text[:120]

        sync_result = cls.sync_chat_event(
            event_type="NARRATIVE_IMPORT",
            speaker=detected_speaker,
            message=extracted_dialogue,
            target_room=detected_room,
            advance_turns=1
        )

        return {
            "success": True,
            "detected_speaker": detected_speaker,
            "detected_room": detected_room,
            "extracted_dialogue": extracted_dialogue,
            "sync_details": sync_result,
            "message": f"Texto del chat procesado: [{detected_speaker}] -> {detected_room or 'Ubicación actual'}."
        }

    @classmethod
    def generate_full_turn_report(cls, credits_available: int = 1046) -> str:
        """
        Genera un reporte de estado canónico completo para pegar en ChatGPT.
        """
        data = cls._load_domain_data()
        chrono = data.get("chrono", DEFAULT_CHRONO)
        positions = data.get("positions", DEFAULT_POSITIONS)
        upgrades = data.get("upgrades", DEFAULT_UPGRADES)
        
        pos_lines = "\n".join([f"  • {k}: Sector {v}" for k, v in positions.items()])

        return (
            f"═══════════════════════════════════════════════════════════════════\n"
            f"📡 [REPORTE DE ESTADO // MEDICAE STATION RHO-9 // DUST FALLS]\n"
            f"⏱️ CRONÓMETRO: Día {chrono.get('day', 4):02d} · {chrono.get('phase', 'VIGILIA NOCTURNA')} ({chrono.get('hour', 23):02d}:{chrono.get('minute', 54):02d}) · Turno {chrono.get('turn', 918)}\n"
            f"💰 RECURSOS: {credits_available} Créditos | 10 Almas (Reserva Umbral) | 3 Puntos de Destino\n"
            f"🛡️ MÉTRICAS BASE: Fortaleza Perimetral 75% | Calidad Sanitaria 70% | Red Eléctrica 80%\n"
            f"👥 DESPLIEGUE DEL SÉQUITO:\n{pos_lines}\n"
            f"🩺 ESTADO DE PACIENTES:\n"
            f"  • Quartus Holt: Cama C-03 (4/11 PV · Soporte de Perfusión Tisular Nvl 2 Activo)\n"
            f"  • Tertius Holt: Cama C-01 (8/11 PV · Drenaje Pleural Operativo)\n"
            f"═══════════════════════════════════════════════════════════════════"
        )

    @classmethod
    def get_blueprint(cls, floor: int = 0) -> Dict[str, Any]:
        data = cls._load_domain_data()
        upgrades = data["upgrades"]
        positions = data["positions"]

        if floor == -1:
            return cls._get_sublevel_blueprint()

        sectors = []
        for room_id, defn in ROOM_DEFINITIONS.items():
            lvl = upgrades.get(room_id, 0 if room_id in ["E-01", "HAB-04", "SUB-01"] else 1)
            tier_info = defn["tiers"].get(lvl, defn["tiers"].get(1))
            
            occupants = [name for name, pos in positions.items() if pos == room_id]

            sectors.append({
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
                "equipment": tier_info["equipment"],
                "bonus": tier_info["bonus"],
                "next_upgrade": tier_info["next"],
                "occupants": occupants
            })

        return {
            "floor": 0,
            "floor_title": "Planta 0: Clínica Medicae Station Rho-9",
            "global_metrics": {
                "defensa_perimetral": 75,
                "calidad_sanitaria": 70,
                "capacidad_camas": "2 / 3 Camas Ocupadas",
                "capacidad_habitaciones": "3 / 4 Cuartos Ocupados"
            },
            "sectors": sectors
        }

    @classmethod
    def _get_sublevel_blueprint(cls) -> Dict[str, Any]:
        data = cls._load_domain_data()
        sublevel = data["sublevel"]

        return {
            "floor": -1,
            "floor_title": "Subnivel -1: Criptas & Bóvedas Inexploradas",
            "sectors": [
                {
                    "id": "SUB-GEN",
                    "code": "BÓVEDA-GEN",
                    "name": "Bóveda del Generador de Respaldo",
                    "status": "OPERATIVO" if sublevel.get("SUB-GEN") else "NIEBLA_DE_GUERRA",
                    "status_color": "green" if sublevel.get("SUB-GEN") else "text-dim",
                    "type": "fog" if not sublevel.get("SUB-GEN") else "tech",
                    "level": 1 if sublevel.get("SUB-GEN") else 0,
                    "level_title": "Generador Auxiliar Pre-Imperial" if sublevel.get("SUB-GEN") else "Sector Oculto",
                    "bonus": "+25% de energía a la red de plasma y autonomía total de 30 días" if sublevel.get("SUB-GEN") else "Desconocido",
                    "exploration_cost": "Requiere 1 Turno + Auspex",
                    "occupants": []
                },
                {
                    "id": "SUB-TUNNEL",
                    "code": "TÚNEL-02",
                    "name": "Túnel de Escape del Sumidero",
                    "status": "OPERATIVO" if sublevel.get("SUB-TUNNEL") else "NIEBLA_DE_GUERRA",
                    "status_color": "green" if sublevel.get("SUB-TUNNEL") else "text-dim",
                    "type": "fog" if not sublevel.get("SUB-TUNNEL") else "security",
                    "level": 1 if sublevel.get("SUB-TUNNEL") else 0,
                    "level_title": "Ruta de Evacuación Segura" if sublevel.get("SUB-TUNNEL") else "Sector Oculto",
                    "bonus": "Permite evacuación inmediata de la clínica sin pasar por la compuerta" if sublevel.get("SUB-TUNNEL") else "Desconocido",
                    "exploration_cost": "Requiere 1 Turno + Linterna",
                    "occupants": []
                },
                {
                    "id": "SUB-STASIS",
                    "code": "CRIPTAS-03",
                    "name": "Sarcófagos de Estasis Antiguos",
                    "status": "OPERATIVO" if sublevel.get("SUB-STASIS") else "NIEBLA_DE_GUERRA",
                    "status_color": "green" if sublevel.get("SUB-STASIS") else "text-dim",
                    "type": "fog" if not sublevel.get("SUB-STASIS") else "medical",
                    "level": 1 if sublevel.get("SUB-STASIS") else 0,
                    "level_title": "Cámaras de Estasis Arqueotecnológicas" if sublevel.get("SUB-STASIS") else "Sector Oculto",
                    "bonus": "Permite suspender a 2 pacientes en estasis temporal indefinida sin gasto de recursos" if sublevel.get("SUB-STASIS") else "Desconocido",
                    "exploration_cost": "Requiere 2 Turnos + Conocimiento Tecnológico",
                    "occupants": []
                },
                {
                    "id": "SUB-CHEM",
                    "code": "DEPÓSITO-04",
                    "name": "Depósito Químico Abandonado de Casa Escher",
                    "status": "OPERATIVO" if sublevel.get("SUB-CHEM") else "NIEBLA_DE_GUERRA",
                    "status_color": "green" if sublevel.get("SUB-CHEM") else "text-dim",
                    "type": "fog" if not sublevel.get("SUB-CHEM") else "storage",
                    "level": 1 if sublevel.get("SUB-CHEM") else 0,
                    "level_title": "Alijo Químico Escher" if sublevel.get("SUB-CHEM") else "Sector Oculto",
                    "bonus": "+10 Reactivos químicos raros y +15 Dosis de antídotos" if sublevel.get("SUB-CHEM") else "Desconocido",
                    "exploration_cost": "Requiere 1 Turno + Traje de Protección",
                    "occupants": []
                }
            ]
        }

    @classmethod
    def upgrade_room_sector(cls, room_id: str, available_credits: int) -> Dict[str, Any]:
        data = cls._load_domain_data()
        upgrades = data["upgrades"]
        logs = data["logs"]

        bp = cls.get_blueprint(floor=0)
        sector = next((s for s in bp["sectors"] if s["id"] == room_id), None)
        if not sector:
            return {"success": False, "error": f"Sector '{room_id}' no encontrado."}

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
