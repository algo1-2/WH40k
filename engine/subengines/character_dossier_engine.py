"""
WH40K Character Dossier Engine (character_dossier_engine.py)
Provides structured, rich authoritative data for:
- Abilities & Powers (Visión de Oscuridad, Sombra Infinita, Reserva Umbral, etc.)
- Weapons & Ballistics (Profiles, Damage, Range, Penetration, Ammo, Traits)
- Inventory & Equipment (Categorized & Real-time)
"""

from typing import Dict, List, Any

ABILITIES_CATALOG = [
    {
        "id": "VISION_OSCURIDAD",
        "name": "Visión de Oscuridad",
        "type": "Percepción / Umbral Pasiva-Activa",
        "attribute": "Percepción (Base 72%)",
        "standard_modifier": "+15%",
        "description": "Permite ver nítidamente a través de penumbra, humo y oscuridad absoluta sin penalizadores ambientales. Revela contraste biológico, seguimiento de respiración, perfusión tisular, calor corporal y siluetas anatómicas a distancia sin necesidad de contacto físico ni iluminación.",
        "combat_effect": "Anula cualquier penalizador por oscuridad/cobertura de humo al disparar u observar."
    },
    {
        "id": "SOMBRA_INFINITA",
        "name": "Sombra Infinita",
        "type": "Dimensión de Bolsillo / Almacén Umbral",
        "attribute": "Voluntad (Base 80%)",
        "standard_modifier": "Automático",
        "description": "Pliegue espacial de la No-Existencia ligado indisolublemente a Alexander. Permite guardar, almacenar y extraer equipo inerte, armas, cadáveres, reactivos y suministros de forma instantánea sin generar peso, volumen ni rastro exterior.",
        "combat_effect": "Extracción o guardado de un objeto como Acción Gratuita (Free Action) en combate."
    },
    {
        "id": "RESERVA_UMBRAL",
        "name": "Reserva Umbral & Cosecha Álmica",
        "type": "Energía Espiritual / Pactos",
        "attribute": "Voluntad",
        "standard_modifier": "Automático",
        "description": "Contenedor metafísico de almas purificadas (Capacidad: 10/10 Almas). Se alimenta de la cosecha de cautivos o moribundos. Se utiliza para sellar o alimentar Hilos Álmicos y potenciar intervenciones milagrosas.",
        "current_souls": 10,
        "max_souls": 10
    },
    {
        "id": "SUTURA_CLANDESTINA",
        "name": "Cirugía Clandestina de Trauma",
        "type": "Medicae Especializado",
        "attribute": "Medicae (Base 65%)",
        "standard_modifier": "+10% con Kit Quirúrgico / +15% en Quirófano Q-01",
        "description": "Capacidad médica avanzada para detener hemorragias letales, drenar neumotórax/hemotórax a tensión, reconstruir vísceras perforadas e implantar prótesis biónicas sin rechazo tisular agudo.",
        "combat_effect": "Estabilización de shock y recuperación de PV según nivel de procedimiento."
    },
    {
        "id": "TOQUE_VACIO",
        "name": "Toque del Vacío",
        "type": "Manipulación Umbral",
        "attribute": "Voluntad (Base 80%)",
        "standard_modifier": "+0%",
        "description": "Permite proyectar filamentos de sombra para manipular palancas, cerrar compuertas a distancia, desarmar enemigos o silenciar sensores auspex."
    }
]

WEAPONS_CATALOG = [
    {
        "key": "AUTOPISTOLA_VOSS",
        "name": "Autopistola de Malrec Voss",
        "category": "Pistola Automática",
        "damage": "1d10+4 Impacto",
        "penetration": 0,
        "rate_of_fire": "S/3/-",
        "range_m": 30,
        "capacity": 18,
        "current_ammo": 18,
        "status": "LIMPIA",
        "traits": ["Fiable (+0 encasquillamiento)", "Munición Sólida"],
        "description": "Arma personal balanceada entregada por Malrec Voss. Ráfagas cortas de alta precisión."
    },
    {
        "key": "CARABINA_CAPTURA",
        "name": "Carabina de Captura",
        "category": "Arma Larga No Letal",
        "damage": "0 (Shock / Parálisis)",
        "penetration": 0,
        "rate_of_fire": "S/-/-",
        "range_m": 45,
        "capacity": 24,
        "current_ammo": 24,
        "status": "LIMPIA",
        "traits": ["Shock(2)", "No Letal", "Aturdidor Neural"],
        "description": "Dispara proyectiles electrificados no letales diseñados para incapacitar cautivos vivos para la cosecha."
    },
    {
        "key": "DAGA_VENENOSA",
        "name": "Daga Venenosa",
        "category": "Arma Cuerpo a Cuerpo",
        "damage": "1d10 Rasgante",
        "penetration": 0,
        "rate_of_fire": "Melee",
        "range_m": 1,
        "capacity": 1,
        "current_ammo": 1,
        "status": "LIMPIA",
        "traits": ["Tóxico(1) (Requiere tirada de Resistencia o daño adicional)"],
        "description": "Hoja curva impregnada con toxina química paralizante."
    },
    {
        "key": "PISTOLA_SERVICIO",
        "name": "Pistola Sólida de Servicio Mk II",
        "category": "Pistola Sólida",
        "damage": "1d10+3 Impacto",
        "penetration": 0,
        "rate_of_fire": "S/2/-",
        "range_m": 30,
        "capacity": 12,
        "current_ammo": 12,
        "status": "LIMPIA",
        "traits": ["Fiable", "Munición Sólida"],
        "description": "Pistola estándar de patrulla de los Enforcers. Robusta, fácil de mantener y con recambios abundantes."
    },
    {
        "key": "RIFLE_PRECISION_MANUFACTORUM",
        "name": "Rifle Sólido de Precisión Manufactorum",
        "category": "Rifle de Precisión",
        "damage": "1d10+5 Impacto",
        "penetration": 1,
        "rate_of_fire": "S/-/-",
        "range_m": 120,
        "capacity": 10,
        "current_ammo": 10,
        "status": "LIMPIA",
        "traits": ["Precisión (+10 a impactar si se apunta)", "Penetrante(1)", "Óptica Telescópica"],
        "description": "Rifle largo manufactorum capturado en el depósito. Munición pesada capaz de perforar blindajes ligeros."
    },
    {
        "key": "AUTOGUN_RETH",
        "name": "Autogun Patrón Reth",
        "category": "Rifle Automático",
        "damage": "1d10+3 Impacto",
        "penetration": 0,
        "rate_of_fire": "S/3/10",
        "range_m": 90,
        "capacity": 30,
        "current_ammo": 30,
        "status": "LIMPIA",
        "traits": ["Fuego Automático", "Supresivo"],
        "description": "Fusil de asalto estándar del submundo. Excelente cadencia de tiro para defensa perimetral."
    },
    {
        "key": "PISTOLA_BRAKK",
        "name": "Pistola Pesada Brakk",
        "category": "Pistola Pesada",
        "damage": "1d10+5 Impacto",
        "penetration": 1,
        "rate_of_fire": "S/-/-",
        "range_m": 20,
        "capacity": 8,
        "current_ammo": 8,
        "status": "LIMPIA",
        "traits": ["Contundente", "Parada Difícil"],
        "description": "Pistola de gran calibre que dispara munición masiva a corta distancia."
    },
    {
        "key": "CARABINA_KORD",
        "name": "Carabina Kord-24",
        "category": "Carabina Sólida",
        "damage": "1d10+3 Impacto",
        "penetration": 0,
        "rate_of_fire": "S/3/-",
        "range_m": 60,
        "capacity": 24,
        "current_ammo": 24,
        "status": "LIMPIA",
        "traits": ["Compacta", "Fiable"],
        "description": "Carabina de servicio militar recortada. Ideal para combate en pasillos estrechos de la colmena."
    },
    {
        "key": "ESCOPETA_COMPACTA",
        "name": "Escopeta Compacta de Corredera",
        "category": "Escopeta",
        "damage": "1d10+4 Impacto",
        "penetration": 0,
        "rate_of_fire": "S/-/-",
        "range_m": 15,
        "capacity": 6,
        "current_ammo": 6,
        "status": "LIMPIA",
        "traits": ["Dispersión (+20 a corta distancia)", "Derribo"],
        "description": "Escopeta corta de asalto. Destructiva en las esquinas y puertas de la clínica."
    }
]

INVENTORY_STRUCTURED = {
    "equipo_activo": [
        {"item": "Autopistola de Malrec Voss", "estado": "18/18 · LIMPIA", "ubicacion": "Funda de cintura"},
        {"item": "Carabina de Captura", "estado": "24/24 · Shock(2) · LIMPIA", "ubicacion": "Bandolera dorsal"},
        {"item": "Daga Venenosa", "estado": "1 dosis activa · LIMPIA", "ubicacion": "Bota derecha"},
        {"item": "Pistola Sólida de Servicio Mk II", "estado": "12/12 · LIMPIA", "ubicacion": "Funda táctica"},
        {"item": "Gabardina Reforzada", "estado": "Perforada en torso (+1 PA)", "ubicacion": "Equipada"},
        {"item": "Medikit Personal de Trauma", "estado": "12 recargas completas disponibles", "ubicacion": "Cinturón médico"},
        {"item": "Kit Quirúrgico Clandestino", "estado": "Operativo y esterilizado", "ubicacion": "Estuche médico"},
        {"item": "Inyector de Stimms Alquímicos", "estado": "3 dosis preparadas", "ubicacion": "Bolsillo interior"}
    ],
    "botin_incursion_nocturna": {
        "pistolas": [
            "1x Autopistola Hesh-9 (Cap. 8)",
            "2x Pistola Sólida de Servicio Mk II (Cap. 12)",
            "1x Autopistola Vex (Cap. 18)",
            "1x Pistola Pesada Brakk (Cap. 8)",
            "1x Pistola compacta de cautivo"
        ],
        "armas_largas": [
            "2x Carabina Kord-24 (Cap. 24)",
            "1x Escopeta Compacta (Cap. 6)",
            "1x Autogun Patrón Reth (Cap. 30)",
            "1x Rifle Sólido de Precisión Manufactorum (Cap. 10)"
        ],
        "explosivos": [
            "3x Granadas de Fragmentación (Frag)",
            "2x Granadas de Humo Tácticas",
            "1x Granada Antitanque Krak"
        ]
    },
    "municion_y_cargadores": {
        "calibre_kord_24": "312 proyectiles sueltos + 144 en cargadores",
        "calibre_pistola_servicio": "240 proyectiles sueltos + 36 en cargadores",
        "calibre_vex": "108 proyectiles sueltos + 36 en cargadores",
        "calibre_brakk": "40 proyectiles pesados sueltos + 16 en cargadores",
        "calibre_autogun_reth": "240 proyectiles sueltos + 120 en cargadores",
        "calibre_rifle_precision": "60 cartuchos manufactorum + 20 en cargadores",
        "cartuchos_escopeta": "120 cartuchos de posta + 8 cartuchos incendiarios",
        "reserva_adicional": "22 proyectiles Mk IV + 4 cartuchos desconocidos sellados"
    },
    "equipo_medico_avanzado": [
        "2x Bio-Auspex de diagnóstico espectral",
        "1x Módulo de imagen anatómica profunda",
        "1x Analizador hemático portátil",
        "1x Analizador farmacológico/químico",
        "1x Óptica de microcirugía con aumentos",
        "2x Monitores vitales de cabecera",
        "1x Respirador portátil asistido con filtros",
        "2x Bombas de infusión intravenosa continua",
        "1x Aspirador de fluidos quirúrgico",
        "1x Electrocauterio galvánico",
        "1x Esterilizador de campo (12 ciclos disponibles)",
        "3x Bandejas de instrumental quirúrgico mayor",
        "2x Kits de trauma mayor y microcirugía vascular"
    ],
    "farmacos_y_fluidos": {
        "antibioticos_amplio_espectro": 36,
        "analgesicos_centrales": 48,
        "sedantes_clinicos": 30,
        "anestesicos_generales": 18,
        "anestesicos_locales": 24,
        "coagulantes_hemostaticos": 30,
        "vasopresores_antishock": 20,
        "antiinflamatorios_esteroideos": 24,
        "antitoxinas_universales": 10,
        "estimulantes_medicae": 12,
        "suero_electrolitos_iv": 24,
        "salina_expansor_plasma_iv": 32,
        "bolsas_sangre_sintetica_iv": 12,
        "gel_dermico_quemaduras": 16,
        "espumas_hemostaticas": 14,
        "droga_desconocida_cuarentena": 3,
        "frascos_agente_quimico_e12": 9
    },
    "consumibles_clinicos": {
        "apositos_esteriles": 80,
        "vendas_elasticas": 48,
        "gasas_hemostaticas": 24,
        "juegos_sutura_monofilamento": 40,
        "grapadoras_cutaneas": "6 unidades + 12 cargadores",
        "selladores_tisulares_adhesivos": 18,
        "lineas_iv_cateteres": 30,
        "tubos_drenaje_toracico": 8
    }
}

class CharacterDossierEngine:

    @classmethod
    def get_abilities(cls) -> Dict[str, Any]:
        return {
            "character": "Alexander",
            "archetype": "Operador Umbral & Médico de Trauma Clandestino",
            "abilities": ABILITIES_CATALOG
        }

    @classmethod
    def get_weapons(cls) -> Dict[str, Any]:
        return {
            "character": "Alexander",
            "active_weapons_count": len(WEAPONS_CATALOG),
            "weapons": WEAPONS_CATALOG
        }

    @classmethod
    def get_full_inventory(cls) -> Dict[str, Any]:
        return {
            "character": "Alexander",
            "location": "Medicae Station Rho-9 // Dust Falls",
            "credits_available": 1046,
            "souls_in_reserve": 10,
            "inventory": INVENTORY_STRUCTURED
        }
