"""
WH40K Domain & Clandestine Network Management Engine (domain_management_engine.py)
Modos de gestión de refugios, plano arquitectónico, asignación de tareas a PNJ y árbol de mejoras.
"""

from typing import Dict, List, Any

class DomainManagementEngine:

    @staticmethod
    def get_rho9_status() -> Dict[str, Any]:
        """
        Devuelve el estado de gestión general de la Clínica Clandestina Rho-9.
        """
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
            },
            "message": "Estado de Gestión de Rho-9: Integridad 88% | Seguridad 75% | Calidad Sanitaria 65% | Cap de Gasto 200 Cr/semana."
        }

    @staticmethod
    def get_rho9_blueprint() -> Dict[str, Any]:
        """
        Devuelve el plano arquitectónico interactivo con el estado de cada sala,
        sus ocupantes, equipamiento instalado, bonos a la campaña y mejoras disponibles.
        """
        return {
            "base_name": "Medicae Station Rho-9",
            "location": "Submundo de Dust Falls, Necromunda",
            "global_metrics": {
                "defensa_perimetral": 75,
                "calidad_sanitaria": 65,
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
                    "level": 1,
                    "level_title": "Barricada Reforzada Simple",
                    "status": "OPERATIVA",
                    "status_color": "green",
                    "occupants": ["Jarek Venn (Guardia)", "Severan Holt (Rondas)"],
                    "equipment": ["Cerradura codificada", "Troneras de tiro", "Barricadas de chapa pesada"],
                    "bonus": "+15% defensa contra asaltos menores sin explosivos",
                    "next_upgrade": {
                        "title": "Nivel 2: Blindaje de Acero & Alarma Vox Perimetral",
                        "cost_credits": 120,
                        "cost_materials": "2 Placas de aleación + 1 Carrete de cable",
                        "effect": "+25% resistencia estructural y aviso anticipado de 2 turnos ante incursiones"
                    }
                },
                {
                    "id": "ADM-01",
                    "code": "ADM-01",
                    "name": "Recepción & Registro Logístico",
                    "type": "logistics",
                    "level": 1,
                    "level_title": "Puesto Contable Manual",
                    "status": "OPERATIVA",
                    "status_color": "green",
                    "occupants": ["Syra Kol (16 años)"],
                    "equipment": ["Cogitador de registro", "Caja fuerte de créditos (1.196 ¤)", "Fichas de suministros"],
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
                    "level": 1,
                    "level_title": "Quirófano Parcial Integrado",
                    "status": "OPERATIVO",
                    "status_color": "green",
                    "occupants": ["Alexander (Cirujano)", "Halven Rusk (Asistente)"],
                    "equipment": ["Diagnostor de espectro (+15% diagnóstico)", "Mesa quirúrgica hidráulica", "Monitores vitales", "Cauterio"],
                    "bonus": "+10% ambiental a procedimientos médicos; +15% a diagnóstico dirigido",
                    "next_upgrade": {
                        "title": "Nivel 2: Circuito de Agua Estéril & Lámparas Articuladas",
                        "cost_credits": 200,
                        "cost_materials": "20m Tubería clínica + 2 Filtros clínicos",
                        "effect": "Eleva el bono ambiental a cirugías a +20% y reduce tiempo operatorio a la mitad"
                    }
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
                    "level": 0,
                    "level_title": "Autoclave Parcial / Sin Circuito Limpio",
                    "status": "REQUIERE_MEJORA",
                    "status_color": "amber",
                    "occupants": ["Khepra-9 (Adaptación)"],
                    "equipment": ["Autoclave de cámara", "Filtros industriales sin adaptar"],
                    "bonus": "Esterilización de instrumental de campo (12 ciclos)",
                    "next_upgrade": {
                        "title": "Nivel 1: Circuito Completo Limpio/Sucio & Autoclave Térmico",
                        "cost_credits": 80,
                        "cost_materials": "Trabajo de Khepra-9 + 2 Válvulas",
                        "effect": "Elimina al 100% el riesgo de infecciones postoperatorias en toda la clínica"
                    }
                },
                {
                    "id": "T-01",
                    "code": "T-01",
                    "name": "Taller Mecatrónico & Armería",
                    "type": "tech",
                    "level": 1,
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
                    "level": 0,
                    "level_title": "Habitación Vacía / Sin Mobiliario",
                    "status": "DISPONIBLE",
                    "status_color": "text-dim",
                    "occupants": ["Vacía"],
                    "equipment": ["Estructura básica limpia"],
                    "bonus": "Capacidad para alojar hasta 2 nuevos colaboradores o refugiados",
                    "next_upgrade": {
                        "title": "Nivel 1: Acondicionamiento de Catres & Iluminación",
                        "cost_credits": 30,
                        "cost_materials": "Mobiliario simple",
                        "effect": "Habilita 2 plazas adicionales de descanso para el séquito"
                    }
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
                    "equipment": ["Puerta metálica reforzada (cierra, sin cerrojo)", "Escaleras descendentes a la oscuridad"],
                    "bonus": "Potencial de expansión masiva, depósitos antiguos o peligros del submundo",
                    "next_upgrade": {
                        "title": "Misión: Expedición Táctica a los Subniveles de Rho-9",
                        "cost_credits": 0,
                        "cost_materials": "Orden de Alexander + Visor multispectral + Lámparas",
                        "effect": "Revela el mapa del Subnivel -1 y desbloquea nuevas salas (Almacén Antiguo, Generador Secundario o Celdas)"
                    }
                }
            ]
        }

    @staticmethod
    def assign_staff_task(npc_name: str, task: str) -> Dict[str, Any]:
        """
        Reasigna la tarea de un PNJ en la base o red clandestina.
        """
        return {
            "npc_name": npc_name,
            "new_task": task,
            "status": "ASIGNACIÓN_ACTUALIZADA",
            "message": f"Se ha asignado a '{npc_name}' la tarea: '{task}' en el protocolo de gestión de Rho-9."
        }

    @staticmethod
    def collect_weekly_revenue(current_credits: int) -> Dict[str, Any]:
        """
        Recauda los ingresos pasivos de la red de informantes y honorarios de la clínica.
        """
        passive_income = 120
        new_total = current_credits + passive_income
        return {
            "passive_income": passive_income,
            "previous_credits": current_credits,
            "new_credits_total": new_total,
            "message": f"¡RECAUDACIÓN SEMANAL DE RED CLANDESTINA!: +{passive_income} Créditos de Necromunda cobrados. Nuevo saldo: {new_total} Créditos."
        }
