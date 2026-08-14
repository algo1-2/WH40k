"""
WH40K Domain & Base Management Engine v2.0 (domain_management_engine.py)
Gestión avanzada de refugios, árbol de mejoras interactivo, exploración del Subnivel -1 y asignación de personal.
"""

from typing import Dict, List, Any, Optional

class DomainManagementEngine:

    _logs: List[Dict[str, str]] = [
        {"time": "Día 04 · 23:40", "type": "SECURITY", "text": "Severan Holt completó la ronda perimetral en la compuerta principal. Acceso asegurado."},
        {"time": "Día 04 · 23:15", "type": "MEDICAL", "text": "Tertius Holt estabilizado tras drenaje torácico. Parámetros vitales: 8/11."},
        {"time": "Día 04 · 22:50", "type": "COSECHA", "text": "Halven Rusk ejecutó a los 4 cautivos en la cámara de triaje. +4 Almas transferidas a Alexander."},
        {"time": "Día 04 · 21:30", "type": "LOGISTICS", "text": "Syra Kol registró el botín del depósito: 11 armas de fuego y 1.000+ proyectiles clasificados."},
        {"time": "Día 04 · 20:10", "type": "TECH", "text": "Khepra-9 instaló el banco de trabajo mecatrónico en el Taller T-01."}
    ]

    _active_upgrades: Dict[str, int] = {
        "GATE-01": 1,
        "ADM-01": 1,
        "Q-01": 1,
        "C-01": 1,
        "C-02": 1,
        "C-03": 1,
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

    _sublevel_revealed: Dict[str, bool] = {
        "SUB-GEN": False,
        "SUB-TUNNEL": False,
        "SUB-STASIS": False,
        "SUB-CHEM": False
    }

    @staticmethod
    def get_rho9_status() -> Dict[str, Any]:
        return {
            "domain_id": "DOMAIN-RHO9-001",
            "nombre": "Medicae Station Rho-9",
            "ubicacion": "Caídas de Polvo / Dust Falls, Necromunda",
            "integridad_estructural": 88,
            "nivel_seguridad": 75,
            "calidad_sanitaria": 65,
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
        """
        Devuelve el plano arquitectónico según el piso seleccionado (0: Clínica, -1: Subnivel).
        """
        if floor == -1:
            return cls._get_sublevel_blueprint()
        return cls._get_floor0_blueprint()

    @classmethod
    def _get_floor0_blueprint(cls) -> Dict[str, Any]:
        # Calcular métricas dinámicas según niveles
        e01_lvl = cls._active_upgrades.get("E-01", 0)
        gate_lvl = cls._active_upgrades.get("GATE-01", 1)
        q01_lvl = cls._active_upgrades.get("Q-01", 1)

        defensa = 75 + (gate_lvl - 1) * 15
        sanidad = 65 + e01_lvl * 20 + (q01_lvl - 1) * 10

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
            "sectors": [
                {
                    "id": "GATE-01",
                    "code": "ACCESO-01",
                    "name": "Compuerta Principal & Barricadas",
                    "type": "security",
                    "level": gate_lvl,
                    "level_title": "Barricada Reforzada Simple" if gate_lvl == 1 else "Blindaje de Acero & Alarma Vox",
                    "status": "OPERATIVA",
                    "status_color": "green",
                    "occupants": ["Jarek Venn (Guardia)", "Severan Holt (Rondas)"],
                    "equipment": ["Cerradura codificada", "Troneras de tiro", "Barricadas de chapa pesada"],
                    "bonus": "+15% defensa contra asaltos menores" if gate_lvl == 1 else "+30% resistencia y alarma anticipada de 2 turnos",
                    "next_upgrade": {
                        "title": "Nivel 2: Blindaje de Acero & Alarma Vox Perimetral",
                        "cost_credits": 120,
                        "cost_materials": "2 Placas de aleación + 1 Carrete de cable",
                        "effect": "+25% resistencia estructural y aviso anticipado de 2 turnos ante incursiones"
                    } if gate_lvl == 1 else None
                },
                {
                    "id": "ADM-01",
                    "code": "ADM-01",
                    "name": "Recepción & Registro Logístico",
                    "type": "logistics",
                    "level": cls._active_upgrades.get("ADM-01", 1),
                    "level_title": "Puesto Contable Manual",
                    "status": "OPERATIVA",
                    "status_color": "green",
                    "occupants": ["Syra Kol (16 años)"],
                    "equipment": ["Cogitador de registro", "Caja fuerte de créditos", "Fichas de suministros"],
                    "bonus": "Registro exacto de consumibles y contabilidad auditada sin fugas",
                    "next_upgrade": {
                        "title": "Nivel 2: Terminal Vox Interceptora de Red",
                        "cost_credits": 80,
                        "cost_materials": "1 Tester + 12 Conectores electrónicos",
                        "effect": "Monitoreo pasivo de frecuencias Enforcer y rumores del mercado de Dust Falls"
                    }
                },
                {
                    "id": "Q-01",
                    "code": "Q-01",
                    "name": "Quirófano Central de Trauma",
                    "type": "medical",
                    "level": q01_lvl,
                    "level_title": "Quirófano Parcial Integrado" if q01_lvl == 1 else "Quirófano Aséptico Avanzado",
                    "status": "OPERATIVO",
                    "status_color": "green",
                    "occupants": ["Alexander (Cirujano)", "Halven Rusk (Asistente)"],
                    "equipment": ["Diagnostor de espectro (+15% diagnóstico)", "Mesa quirúrgica hidráulica", "Monitores vitales", "Cauterio"],
                    "bonus": "+10% ambiental a procedimientos médicos; +15% a diagnóstico dirigido" if q01_lvl == 1 else "+20% ambiental a cirugías y tiempo operatorio reducido a la mitad",
                    "next_upgrade": {
                        "title": "Nivel 2: Circuito de Agua Estéril & Lámparas Articuladas",
                        "cost_credits": 200,
                        "cost_materials": "20m Tubería clínica + 2 Filtros clínicos",
                        "effect": "Eleva el bono ambiental a cirugías a +20% y reduce tiempo operatorio a la mitad"
                    } if q01_lvl == 1 else None
                },
                {
                    "id": "C-01",
                    "code": "C-01",
                    "name": "Cama Clínica 01 (Postoperatorio)",
                    "type": "recovery",
                    "level": 1,
                    "level_title": "Cama Monitoreada",
                    "status": "OCUPADA",
                    "status_color": "amber",
                    "occupants": ["Tertius Holt (8/11 · Despierto)"],
                    "equipment": ["Drenaje torácico funcional", "Soporte de fluidos IV", "Monitor de pulso"],
                    "bonus": "Estabilización garantizada; recuperación pasiva de 1 PV cada 24h",
                    "next_upgrade": {
                        "title": "Nivel 2: Módulo de Oxigenoterapia Regulada",
                        "cost_credits": 60,
                        "cost_materials": "1 Cilindro de oxígeno + 1 Regulador",
                        "effect": "Acelera recuperación de heridas pulmonares y torácicas (+2 PV/24h)"
                    }
                },
                {
                    "id": "C-02",
                    "code": "C-02",
                    "name": "Cama Clínica 02 (Triaje / Emergencia)",
                    "type": "recovery",
                    "level": 1,
                    "level_title": "Cama Libre para Triaje",
                    "status": "DISPONIBLE",
                    "status_color": "green",
                    "occupants": ["Libre"],
                    "equipment": ["Líneas IV en espera", "Bandeja de sutura rápida"],
                    "bonus": "Capacidad de recepción inmediata de 1 paciente de trauma sin preparación",
                    "next_upgrade": {
                        "title": "Nivel 2: Carro de Reanimación Avanzada",
                        "cost_credits": 100,
                        "cost_materials": "1 Desfibrilador + 1 Kit trauma mayor",
                        "effect": "+20% a tiradas de estabilización de urgencia en los primeros 2 turnos"
                    }
                },
                {
                    "id": "C-03",
                    "code": "C-03",
                    "name": "Cama Clínica 03 (Cuidados Críticos)",
                    "type": "recovery",
                    "level": 1,
                    "level_title": "Soporte Vital Crítico",
                    "status": "CRÍTICO_ESTABLE",
                    "status_color": "crimson",
                    "occupants": ["Quartus Holt (4/11 · Inconsciente/Intubado)"],
                    "equipment": ["Respirador asistido", "Bomba de infusión continua", "Monitor multiseñal"],
                    "bonus": "Mantiene con vida a pacientes con herida letal a quemarropa en coma farmacológico",
                    "next_upgrade": {
                        "title": "Nivel 2: Sistema de Perfusión Tisular Continua",
                        "cost_credits": 150,
                        "cost_materials": "1 Bomba infusión portátil + 2 Líneas IV",
                        "effect": "Permite iniciar la desintubación segura y despertar progresivo de Quartus"
                    }
                },
                {
                    "id": "F-02",
                    "code": "F-02",
                    "name": "Farmacia & Depósito Químico",
                    "type": "storage",
                    "level": 1,
                    "level_title": "Armario Refrigerado Operativo",
                    "status": "OPERATIVA",
                    "status_color": "green",
                    "occupants": ["Syra Kol (Control)", "Alexander (Acceso exclusivo)"],
                    "equipment": ["Armario refrigerado", "Depósito separado para 9 frascos E-12", "Stock 200+ fármacos"],
                    "bonus": "Cero degradación de medicamentos biológicos y antibióticos",
                    "next_upgrade": {
                        "title": "Nivel 2: Cámara Acorazada de Toxinas & Alquimia",
                        "cost_credits": 90,
                        "cost_materials": "4 Placas de polímero + 2 Sellos",
                        "effect": "Habilita síntesis de antídotos complejos y previene contaminación cruzada"
                    }
                },
                {
                    "id": "E-01",
                    "code": "E-01",
                    "name": "Sala de Esterilización & Filtros",
                    "type": "medical",
                    "level": e01_lvl,
                    "level_title": "Autoclave Parcial / Sin Circuito Limpio" if e01_lvl == 0 else "Circuito Aséptico Completo",
                    "status": "REQUIERE_MEJORA" if e01_lvl == 0 else "OPERATIVA",
                    "status_color": "amber" if e01_lvl == 0 else "green",
                    "occupants": ["Khepra-9 (Adaptación)"],
                    "equipment": ["Autoclave de cámara", "Filtros industriales adaptados" if e01_lvl > 0 else "Filtros sin adaptar"],
                    "bonus": "Esterilización de campo limitada" if e01_lvl == 0 else "Elimina al 100% el riesgo de infecciones postoperatorias en toda la clínica",
                    "next_upgrade": {
                        "title": "Nivel 1: Circuito Completo Limpio/Sucio & Autoclave Térmico",
                        "cost_credits": 80,
                        "cost_materials": "Trabajo de Khepra-9 + 2 Válvulas",
                        "effect": "Elimina al 100% el riesgo de infecciones postoperatorias en toda la clínica"
                    } if e01_lvl == 0 else None
                },
                {
                    "id": "T-01",
                    "code": "T-01",
                    "name": "Taller Mecatrónico & Armería",
                    "type": "tech",
                    "level": cls._active_upgrades.get("T-01", 1),
                    "level_title": "Taller en Instalación",
                    "status": "OPERATIVO",
                    "status_color": "green",
                    "occupants": ["Khepra-9 (Tecnosacerdote)"],
                    "equipment": ["Banco de trabajo", "Microsoldador", "Cortador", "Arsenal de 11 armas guardado"],
                    "bonus": "Reparación, limpieza y desatranco inmediato de armas de fuego",
                    "next_upgrade": {
                        "title": "Nivel 2: Banco de Calibración Protésica & Biónica",
                        "cost_credits": 100,
                        "cost_materials": "Microservos + Actuadores + 1 Plantilla alineación",
                        "effect": "Habilita la fabricación y acople de la prótesis para el brazo del 2º deudor"
                    }
                },
                {
                    "id": "HAB-01",
                    "code": "HAB-01",
                    "name": "Habitación de Personal 1 (Guardia)",
                    "type": "dorm",
                    "level": 1,
                    "level_title": "Dormitorio de Seguridad",
                    "status": "OCUPADA",
                    "status_color": "green",
                    "occupants": ["Severan Holt", "Jarek Venn"],
                    "equipment": ["2 Catres metálicos", "Cofre de munición básica"],
                    "bonus": "Tiempo de respuesta táctica de 1 turno ante alertas en la compuerta",
                    "next_upgrade": {
                        "title": "Nivel 2: Armero de Respuesta Rápida",
                        "cost_credits": 40,
                        "cost_materials": "1 Cofre industrial",
                        "effect": "Despliegue armado instantáneo de Severan y Jarek con equipo completo"
                    }
                },
                {
                    "id": "HAB-02",
                    "code": "HAB-02",
                    "name": "Habitación de Personal 2 (Convalecencia)",
                    "type": "dorm",
                    "level": 1,
                    "level_title": "Dormitorio de Recuperación",
                    "status": "OCUPADA",
                    "status_color": "green",
                    "occupants": ["Mara Veyl (10/10)", "Sael Veyl (10/10)"],
                    "equipment": ["2 Catres simples", "Botiquín menor"],
                    "bonus": "Descanso estable para colaboradores",
                    "next_upgrade": {
                        "title": "Nivel 2: Aislamiento Térmico & Ventilación",
                        "cost_credits": 50,
                        "cost_materials": "Láminas de polímero",
                        "effect": "Acelera recuperación de fatiga a 0 en 4 horas de reposo"
                    }
                },
                {
                    "id": "HAB-03",
                    "code": "HAB-03",
                    "name": "Habitación de Personal 3 (Refugio)",
                    "type": "dorm",
                    "level": 1,
                    "level_title": "Dormitorio Auxiliar",
                    "status": "OCUPADA",
                    "status_color": "green",
                    "occupants": ["Ilyra Venn (9/10)", "Hadrix Vale", "Demer Vhal (Aislada)"],
                    "equipment": ["Catres y mantas térmicas"],
                    "bonus": "Espacio seguro para el séquito extendido",
                    "next_upgrade": {
                        "title": "Nivel 2: Módulo de Aislamiento Anómalo",
                        "cost_credits": 75,
                        "cost_materials": "2 Placas aleación + Sellos",
                        "effect": "Contención perfecta para Demer Vhal sin riesgo de interferencias"
                    }
                },
                {
                    "id": "HAB-04",
                    "code": "HAB-04",
                    "name": "Habitación de Personal 4 (Reserva)",
                    "type": "dorm",
                    "level": cls._active_upgrades.get("HAB-04", 0),
                    "level_title": "Habitación Vacía / Sin Mobiliario" if cls._active_upgrades.get("HAB-04", 0) == 0 else "Dormitorio Acondicionado",
                    "status": "DISPONIBLE",
                    "status_color": "text-dim" if cls._active_upgrades.get("HAB-04", 0) == 0 else "green",
                    "occupants": ["Vacía"],
                    "equipment": ["Estructura básica limpia"],
                    "bonus": "Capacidad para alojar hasta 2 nuevos colaboradores o refugiados",
                    "next_upgrade": {
                        "title": "Nivel 1: Acondicionamiento de Catres & Iluminación",
                        "cost_credits": 30,
                        "cost_materials": "Mobiliario simple",
                        "effect": "Habilita 2 plazas adicionales de descanso para el séquito"
                    } if cls._active_upgrades.get("HAB-04", 0) == 0 else None
                },
                {
                    "id": "COMM-01",
                    "code": "COMM-01",
                    "name": "Sala Común & Almacén de Víveres",
                    "type": "living",
                    "level": 1,
                    "level_title": "Comedor & Despensa Básica",
                    "status": "OPERATIVA",
                    "status_color": "green",
                    "occupants": ["Punto de reunión del séquito"],
                    "equipment": ["Mesa de metal", "Despensa con 48 raciones", "16 botellas de agua 1L"],
                    "bonus": "Suministros garantizados para 12 personas durante 4 días",
                    "next_upgrade": {
                        "title": "Nivel 2: Purificador Hidropónico & Cocina de Campo",
                        "cost_credits": 110,
                        "cost_materials": "Filtros + Tubería",
                        "effect": "Generación pasiva de 4 raciones frescas y 4L de agua purificada al día"
                    }
                },
                {
                    "id": "SUB-01",
                    "code": "SUB-01",
                    "name": "Puerta Posterior & Escaleras a Subniveles",
                    "type": "fog",
                    "level": 0,
                    "level_title": "Sector Inexplorado / Niebla de Guerra",
                    "status": "BLOQUEADO_POR_EXPLORAR",
                    "status_color": "cyan",
                    "occupants": ["Ninguno (Presencia desconocida)"],
                    "equipment": ["Puerta metálica reforzada", "Escaleras descendentes a la oscuridad"],
                    "bonus": "Acceso al Subnivel -1 y zonas ocultas de Rho-9",
                    "next_upgrade": {
                        "title": "Misión: Cambiar al Subnivel -1 para Iniciar Exploración",
                        "cost_credits": 0,
                        "cost_materials": "Orden de Alexander + Lámparas",
                        "effect": "Permite acceder al mapa táctico de las criptas subterráneas"
                    }
                }
            ]
        }

    @classmethod
    def _get_sublevel_blueprint(cls) -> Dict[str, Any]:
        return {
            "floor": -1,
            "floor_name": "Subnivel -1 // Criptas & Red Subterránea Inexplorada",
            "global_metrics": {
                "sectores_revelados": sum(1 for v in cls._sublevel_revealed.values() if v),
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
                    "is_revealed": cls._sublevel_revealed["SUB-GEN"],
                    "level": 1 if cls._sublevel_revealed["SUB-GEN"] else 0,
                    "level_title": "Generador Antiguo Descubierto" if cls._sublevel_revealed["SUB-GEN"] else "Señal Térmica No Confirmada",
                    "status": "REVELADO" if cls._sublevel_revealed["SUB-GEN"] else "NIEBLA_DE_GUERRA",
                    "status_color": "green" if cls._sublevel_revealed["SUB-GEN"] else "cyan",
                    "occupants": ["Khepra-9 (Asignable)"] if cls._sublevel_revealed["SUB-GEN"] else ["Desconocido"],
                    "equipment": ["Turbina geotérmica arcaica", "Depósito de refrigerante"] if cls._sublevel_revealed["SUB-GEN"] else ["Auspex detecta masa metálica pesada"],
                    "bonus": "Energía ilimitada para toda la clínica si se reactiva" if cls._sublevel_revealed["SUB-GEN"] else "Desconocido",
                    "exploration_cost": "1 Turno de Exploración + Tirada de Percepción"
                },
                {
                    "id": "SUB-TUNNEL",
                    "code": "SUB-03",
                    "name": "Conducto de Escape a Dust Falls",
                    "type": "security",
                    "is_revealed": cls._sublevel_revealed["SUB-TUNNEL"],
                    "level": 1 if cls._sublevel_revealed["SUB-TUNNEL"] else 0,
                    "level_title": "Ruta de Evacuación Segura" if cls._sublevel_revealed["SUB-TUNNEL"] else "Corriente de Aire Frío",
                    "status": "REVELADO" if cls._sublevel_revealed["SUB-TUNNEL"] else "NIEBLA_DE_GUERRA",
                    "status_color": "green" if cls._sublevel_revealed["SUB-TUNNEL"] else "cyan",
                    "occupants": ["Severan Holt (Vigilancia)"] if cls._sublevel_revealed["SUB-TUNNEL"] else ["Desconocido"],
                    "equipment": ["Compuerta de alcantarillado", "Escalera de gato"] if cls._sublevel_revealed["SUB-TUNNEL"] else ["Corriente de aire hacia el exterior"],
                    "bonus": "Ruta de escape indetectable ante un asedio a la clínica" if cls._sublevel_revealed["SUB-TUNNEL"] else "Desconocido",
                    "exploration_cost": "1 Turno de Exploración + Tirada de Sigilo"
                },
                {
                    "id": "SUB-STASIS",
                    "code": "SUB-04",
                    "name": "Cámara de Estasis Pre-Imperial",
                    "type": "medical",
                    "is_revealed": cls._sublevel_revealed["SUB-STASIS"],
                    "level": 1 if cls._sublevel_revealed["SUB-STASIS"] else 0,
                    "level_title": "Sarcófagos de Preservación" if cls._sublevel_revealed["SUB-STASIS"] else "Eco Psíquico / Campo Estático",
                    "status": "REVELADO" if cls._sublevel_revealed["SUB-STASIS"] else "NIEBLA_DE_GUERRA",
                    "status_color": "green" if cls._sublevel_revealed["SUB-STASIS"] else "cyan",
                    "occupants": ["3 Cápsulas selladas (Contenido arcaico)"] if cls._sublevel_revealed["SUB-STASIS"] else ["Presencia biológica latente"],
                    "equipment": ["3 Cápsulas criogénicas funcionales", "Sellos de aislamiento"] if cls._sublevel_revealed["SUB-STASIS"] else ["Interferencia en el auspex"],
                    "bonus": "Capacidad de suspensión a largo plazo para biobanco o sujetos de estudio" if cls._sublevel_revealed["SUB-STASIS"] else "Desconocido",
                    "exploration_cost": "1 Turno de Exploración + Tirada de Voluntad/Psicología"
                },
                {
                    "id": "SUB-CHEM",
                    "code": "SUB-05",
                    "name": "Depósito Químico Olvidado (Escher)",
                    "type": "storage",
                    "is_revealed": cls._sublevel_revealed["SUB-CHEM"],
                    "level": 1 if cls._sublevel_revealed["SUB-CHEM"] else 0,
                    "level_title": "Almacén Clandestino de Narcóticos" if cls._sublevel_revealed["SUB-CHEM"] else "Vapores Dulzones en Tuberías",
                    "status": "REVELADO" if cls._sublevel_revealed["SUB-CHEM"] else "NIEBLA_DE_GUERRA",
                    "status_color": "green" if cls._sublevel_revealed["SUB-CHEM"] else "cyan",
                    "occupants": ["Sin custodios"] if cls._sublevel_revealed["SUB-CHEM"] else ["Posibles alimañas del submundo"],
                    "equipment": ["Contenedores de estimulantes químicos", "Reactores de vidrio"] if cls._sublevel_revealed["SUB-CHEM"] else ["Olor penetrante a químicos volátiles"],
                    "bonus": "+50 Dosis de estimulantes y reactivos para el sintetizador de Alexander" if cls._sublevel_revealed["SUB-CHEM"] else "Desconocido",
                    "exploration_cost": "1 Turno de Exploración + Tirada de Resistencia"
                }
            ]
        }

    @classmethod
    def execute_room_upgrade(cls, room_id: str, available_credits: int) -> Dict[str, Any]:
        """
        Ejecuta el proyecto de mejora para una sala, descontando créditos y elevando su nivel.
        """
        blueprint = cls._get_floor0_blueprint()
        sector = next((s for s in blueprint["sectors"] if s["id"] == room_id), None)
        
        if not sector:
            return {"success": False, "error": f"Sala con ID '{room_id}' no encontrada."}
        
        upgrade = sector.get("next_upgrade")
        if not upgrade:
            return {"success": False, "error": f"La sala '{sector['name']}' ya está en su nivel máximo."}
        
        cost = upgrade.get("cost_credits", 0)
        if available_credits < cost:
            return {"success": False, "error": f"Créditos insuficientes ({available_credits} ¤ disponibles, requiere {cost} ¤)."}
        
        # Aplicar mejora
        current_lvl = cls._active_upgrades.get(room_id, 1)
        cls._active_upgrades[room_id] = current_lvl + 1
        new_credits = available_credits - cost

        log_entry = {
            "time": "Día 04 · Noche (Ahora)",
            "type": "UPGRADE",
            "text": f"¡PROYECTO DE MEJORA EJECUTADO! '{sector['name']}' elevada a Nivel {current_lvl + 1}. Coste: -{cost} ¤. Efecto: {upgrade.get('effect')}"
        }
        cls._logs.insert(0, log_entry)

        return {
            "success": True,
            "room_id": room_id,
            "room_name": sector["name"],
            "new_level": current_lvl + 1,
            "spent_credits": cost,
            "remaining_credits": new_credits,
            "applied_effect": upgrade.get("effect"),
            "log": log_entry,
            "message": f"Mejora completada con éxito: {sector['name']} ahora es Nivel {current_lvl + 1}."
        }

    @classmethod
    def explore_sublevel_sector(cls, sector_id: str, actor: str = "Alexander") -> Dict[str, Any]:
        """
        Revela una sala oculta del Subnivel -1 y genera la narrativa de exploración.
        """
        if sector_id not in cls._sublevel_revealed:
            return {"success": False, "error": f"Sector '{sector_id}' no existe en el Subnivel -1."}
        
        cls._sublevel_revealed[sector_id] = True
        bp = cls._get_sublevel_blueprint()
        sector = next((s for s in bp["sectors"] if s["id"] == sector_id), None)

        log_entry = {
            "time": "Día 04 · Noche (Exploración)",
            "type": "EXPLORATION",
            "text": f"{actor} exploró los subniveles y despejó la niebla de guerra en '{sector['name']}'. ¡Bono desbloqueado: {sector['bonus']}!"
        }
        cls._logs.insert(0, log_entry)

        return {
            "success": True,
            "sector_id": sector_id,
            "sector_name": sector["name"],
            "bonus_unlocked": sector["bonus"],
            "log": log_entry,
            "message": f"Sector '{sector['name']}' explorado y asegurado con éxito."
        }

    @classmethod
    def get_logs(cls) -> List[Dict[str, str]]:
        return cls._logs
