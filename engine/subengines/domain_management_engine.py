"""
WH40K Domain & Base Management Engine v3.0 (domain_management_engine.py)
Gestión avanzada y PERSISTENTE de refugios, árbol de mejoras interactivo,
exploración del Subnivel -1 y asignación de personal para Necromunda.
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

DEFAULT_SUBLEVEL_REVEALED = {
    "SUB-GEN": False,
    "SUB-TUNNEL": False,
    "SUB-STASIS": False,
    "SUB-CHEM": False
}

DEFAULT_LOGS = [
    {"time": "Día 04 · 23:40", "type": "SECURITY", "text": "Severan Holt completó la ronda perimetral en la compuerta principal. Acceso asegurado."},
    {"time": "Día 04 · 23:15", "type": "MEDICAL", "text": "Tertius Holt estabilizado tras drenaje torácico. Parámetros vitales: 8/11."},
    {"time": "Día 04 · 22:50", "type": "COSECHA", "text": "Halven Rusk ejecutó a los 4 cautivos en la cámara de triaje. +4 Almas transferidas a Alexander."},
    {"time": "Día 04 · 21:30", "type": "LOGISTICS", "text": "Syra Kol registró el botín del depósito: 11 armas de fuego y 1.000+ proyectiles clasificados."},
    {"time": "Día 04 · 20:10", "type": "TECH", "text": "Khepra-9 instaló el banco de trabajo mecatrónico en el Taller T-01."}
]

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
                    
                    merged_upgrades = dict(DEFAULT_UPGRADES)
                    merged_upgrades.update(upgrades)
                    
                    merged_sublevel = dict(DEFAULT_SUBLEVEL_REVEALED)
                    merged_sublevel.update(sublevel)
                    
                    merged_logs = logs if logs else list(DEFAULT_LOGS)
                    return {
                        "upgrades": merged_upgrades,
                        "sublevel": merged_sublevel,
                        "logs": merged_logs
                    }
            except Exception as e:
                print(f"Error cargando domain_data: {e}")
        return {
            "upgrades": dict(DEFAULT_UPGRADES),
            "sublevel": dict(DEFAULT_SUBLEVEL_REVEALED),
            "logs": list(DEFAULT_LOGS)
        }

    @classmethod
    def _save_domain_data(cls, upgrades: Dict[str, int], sublevel: Dict[str, bool], logs: List[Dict[str, str]]):
        filepath = cls._get_state_file()
        state = {}
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    state = json.load(f)
            except Exception:
                pass
        
        state["domain_state"] = {
            "upgrades": upgrades,
            "sublevel_revealed": sublevel,
            "logs": logs[:30] # conservar últimos 30 logs
        }

        # Guardar en tmp si está en Vercel
        try:
            with open("/tmp/campaign_state.json", "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

        # Guardar local si es accesible
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
    def get_rho9_status(cls) -> Dict[str, Any]:
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
        if floor == -1:
            return cls._get_sublevel_blueprint()
        return cls._get_floor0_blueprint()

    @classmethod
    def _get_floor0_blueprint(cls) -> Dict[str, Any]:
        data = cls._load_domain_data()
        upg = data["upgrades"]

        gate_lvl = upg.get("GATE-01", 1)
        adm_lvl = upg.get("ADM-01", 1)
        q01_lvl = upg.get("Q-01", 1)
        c01_lvl = upg.get("C-01", 1)
        c02_lvl = upg.get("C-02", 1)
        c03_lvl = upg.get("C-03", 1)
        f02_lvl = upg.get("F-02", 1)
        e01_lvl = upg.get("E-01", 0)
        t01_lvl = upg.get("T-01", 1)
        hab01_lvl = upg.get("HAB-01", 1)
        hab02_lvl = upg.get("HAB-02", 1)
        hab03_lvl = upg.get("HAB-03", 1)
        hab04_lvl = upg.get("HAB-04", 0)
        comm_lvl = upg.get("COMM-01", 1)
        sub01_lvl = upg.get("SUB-01", 0)

        defensa = 75 + (gate_lvl - 1) * 15
        sanidad = 65 + e01_lvl * 20 + (q01_lvl - 1) * 10 + (c03_lvl - 1) * 5

        sectors = [
            {
                "id": "GATE-01",
                "code": "ACCESO-01",
                "name": "Compuerta Principal & Barricadas",
                "type": "security",
                "level": gate_lvl,
                "level_title": "Barricada Reforzada Simple" if gate_lvl == 1 else "Blindaje de Acero & Alarma Vox (Nivel 2)",
                "status": "OPERATIVA",
                "status_color": "green",
                "occupants": ["Jarek Venn (Guardia)", "Severan Holt (Rondas)"],
                "equipment": ["Cerradura codificada", "Troneras de tiro", "Barricadas de chapa pesada"],
                "bonus": "+15% defensa contra asaltos menores" if gate_lvl == 1 else "+30% resistencia y sensor vox perimetral (2 turnos de aviso)",
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
                "level": adm_lvl,
                "level_title": "Puesto Contable Manual" if adm_lvl == 1 else "Terminal Vox Interceptora (Nivel 2)",
                "status": "OPERATIVA",
                "status_color": "green",
                "occupants": ["Syra Kol (16 años)"],
                "equipment": ["Cogitador de registro", "Caja fuerte de créditos", "Fichas de suministros"],
                "bonus": "Registro exacto de consumibles y contabilidad auditada sin fugas" if adm_lvl == 1 else "Monitoreo de frecuencias policiales y alerta temprana de bandas",
                "next_upgrade": {
                    "title": "Nivel 2: Terminal Vox Interceptora de Red",
                    "cost_credits": 80,
                    "cost_materials": "1 Tester + 12 Conectores electrónicos",
                    "effect": "Monitoreo pasivo de frecuencias Enforcer y rumores del mercado de Dust Falls"
                } if adm_lvl == 1 else None
            },
            {
                "id": "Q-01",
                "code": "Q-01",
                "name": "Quirófano Central de Trauma",
                "type": "medical",
                "level": q01_lvl,
                "level_title": "Quirófano Parcial Integrado" if q01_lvl == 1 else "Quirófano Aséptico Avanzado (Nivel 2)",
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
                "level": c01_lvl,
                "level_title": "Cama Monitoreada" if c01_lvl == 1 else "Oxigenoterapia Regulada (Nivel 2)",
                "status": "OCUPADA",
                "status_color": "amber",
                "occupants": ["Tertius Holt (8/11 · Despierto)"],
                "equipment": ["Drenaje torácico funcional", "Soporte de fluidos IV", "Monitor de pulso"],
                "bonus": "Estabilización garantizada; recuperación pasiva de 1 PV cada 24h" if c01_lvl == 1 else "Recuperación acelerada de heridas pulmonares (+2 PV cada 24h)",
                "next_upgrade": {
                    "title": "Nivel 2: Módulo de Oxigenoterapia Regulada",
                    "cost_credits": 60,
                    "cost_materials": "1 Cilindro de oxígeno + 1 Regulador",
                    "effect": "Acelera recuperación de heridas pulmonares y torácicas (+2 PV/24h)"
                } if c01_lvl == 1 else None
            },
            {
                "id": "C-02",
                "code": "C-02",
                "name": "Cama Clínica 02 (Triaje / Emergencia)",
                "type": "recovery",
                "level": c02_lvl,
                "level_title": "Cama Libre para Triaje" if c02_lvl == 1 else "Carro de Reanimación Avanzada (Nivel 2)",
                "status": "DISPONIBLE",
                "status_color": "green",
                "occupants": ["Libre (En espera de urgencias)"],
                "equipment": ["Líneas IV en espera", "Bandeja de sutura rápida"],
                "bonus": "Capacidad de recepción inmediata de 1 paciente de trauma sin preparación" if c02_lvl == 1 else "+20% a tiradas de estabilización de urgencia en primeros 2 turnos",
                "next_upgrade": {
                    "title": "Nivel 2: Carro de Reanimación Avanzada",
                    "cost_credits": 100,
                    "cost_materials": "1 Desfibrilador + 1 Kit trauma mayor",
                    "effect": "+20% a tiradas de estabilización de urgencia en los primeros 2 turnos"
                } if c02_lvl == 1 else None
            },
            {
                "id": "C-03",
                "code": "C-03",
                "name": "Cama Clínica 03 (Cuidados Críticos)",
                "type": "recovery",
                "level": c03_lvl,
                "level_title": "Soporte Vital Crítico (Nivel 1)" if c03_lvl == 1 else "Perfusión Tisular & Desintubación Segura (Nivel 2)",
                "status": "CRÍTICO_ESTABLE" if c03_lvl == 1 else "RECUPERACIÓN_ACTIVA",
                "status_color": "crimson" if c03_lvl == 1 else "amber",
                "occupants": ["Quartus Holt (4/11 · Intubado)"] if c03_lvl == 1 else ["Quartus Holt (4/11 · Desintubación Iniciada)"],
                "equipment": ["Respirador asistido", "Bomba de infusión continua", "Monitor multiseñal"],
                "bonus": "Mantiene con vida a pacientes con herida letal a quemarropa en coma farmacológico" if c03_lvl == 1 else "Perfusión activa: Habilita desintubación segura sin colapso pulmonar y recuperación consciente",
                "next_upgrade": {
                    "title": "Nivel 2: Sistema de Perfusión Tisular Continua",
                    "cost_credits": 150,
                    "cost_materials": "1 Bomba infusión portátil + 2 Líneas IV",
                    "effect": "Permite iniciar la desintubación segura y despertar progresivo de Quartus"
                } if c03_lvl == 1 else None
            },
            {
                "id": "F-02",
                "code": "F-02",
                "name": "Farmacia & Depósito Químico",
                "type": "storage",
                "level": f02_lvl,
                "level_title": "Armario Refrigerado Operativo" if f02_lvl == 1 else "Cámara Acorazada de Toxinas & Alquimia (Nivel 2)",
                "status": "OPERATIVA",
                "status_color": "green",
                "occupants": ["Syra Kol (Control)", "Alexander (Acceso exclusivo)"],
                "equipment": ["Armario refrigerado", "Depósito separado para 9 frascos E-12", "Stock 200+ fármacos"],
                "bonus": "Cero degradación de medicamentos biológicos y antibióticos" if f02_lvl == 1 else "Habilita síntesis de antídotos complejos y previene contaminación cruzada",
                "next_upgrade": {
                    "title": "Nivel 2: Cámara Acorazada de Toxinas & Alquimia",
                    "cost_credits": 90,
                    "cost_materials": "4 Placas de polímero + 2 Sellos",
                    "effect": "Habilita síntesis de antídotos complejos y previene contaminación cruzada"
                } if f02_lvl == 1 else None
            },
            {
                "id": "E-01",
                "code": "E-01",
                "name": "Sala de Esterilización & Filtros",
                "type": "medical",
                "level": e01_lvl,
                "level_title": "Autoclave Parcial / Sin Circuito Limpio" if e01_lvl == 0 else "Circuito Aséptico Completo (Nivel 1)",
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
                "level": t01_lvl,
                "level_title": "Taller en Instalación" if t01_lvl == 1 else "Banco Protésico & Armería Avanzada (Nivel 2)",
                "status": "OPERATIVO",
                "status_color": "green",
                "occupants": ["Khepra-9 (Tecnosacerdote)"],
                "equipment": ["Banco de soldadura de arco", "Herramientas de precisión", "Analizador lógico"],
                "bonus": "Mantenimiento y reparación de armas sólidas y láser" if t01_lvl == 1 else "Desbloquea fabricación de prótesis biónicas para el 2º deudor de Sombra",
                "next_upgrade": {
                    "title": "Nivel 2: Banco de Prótesis Biónicas & Fabricación",
                    "cost_credits": 140,
                    "cost_materials": "1 Servo-articulador + 4 Circuitos de control",
                    "effect": "Desbloquea la fabricación de la prótesis mecánica para el brazo del 2º deudor de Sombra"
                } if t01_lvl == 1 else None
            },
            {
                "id": "HAB-01",
                "code": "HAB-01",
                "name": "Dormitorio de Alexander & Sanctum",
                "type": "living",
                "level": hab01_lvl,
                "level_title": "Habitación Privada Segura",
                "status": "OPERATIVA",
                "status_color": "green",
                "occupants": ["Alexander"],
                "equipment": ["Catre reforzado", "Cerradura de llave maestra", "Escritorio táctico"],
                "bonus": "Privacidad absoluta; meditación umbral protegida de miradas ajenas",
                "next_upgrade": {
                    "title": "Nivel 2: Aislamiento Psico-Acústico & Caja Oculta",
                    "cost_credits": 70,
                    "cost_materials": "Paneles de plomo y espuma acústica",
                    "effect": "Oculta emanaciones psíquicas menores durante el descanso y agrega alijo secreto"
                } if hab01_lvl == 1 else None
            },
            {
                "id": "HAB-02",
                "code": "HAB-02",
                "name": "Dormitorio de Guardia (Severan & Jarek)",
                "type": "living",
                "level": hab02_lvl,
                "level_title": "Cuartel de Seguridad",
                "status": "OPERATIVA",
                "status_color": "green",
                "occupants": ["Severan Holt", "Jarek Venn"],
                "equipment": ["2 Catres de campaña", "Armero de pared cerrado", "Intercomunicador"],
                "bonus": "Tiempo de respuesta de guardias ante intrusiones: Inmediato (1 turno)",
                "next_upgrade": {
                    "title": "Nivel 2: Acondicionador Térmico & Taquillas Reforzadas",
                    "cost_credits": 50,
                    "cost_materials": "1 Calefactor de chimenea",
                    "effect": "Permite recuperar toda la fatiga del personal de guardia en 4h de reposo"
                } if hab02_lvl == 1 else None
            },
            {
                "id": "HAB-03",
                "code": "HAB-03",
                "name": "Dormitorio de Personal (Syra & Khepra)",
                "type": "living",
                "level": hab03_lvl,
                "level_title": "Habitación de Apoyo",
                "status": "OPERATIVA",
                "status_color": "green",
                "occupants": ["Syra Kol", "Khepra-9 (Nicho de recarga)"],
                "equipment": ["1 Catre estándar", "Estación de recarga de bio-baterías"],
                "bonus": "Descanso y mantenimiento técnico garantizados para la logística de la base",
                "next_upgrade": {
                    "title": "Nivel 2: Terminal de Consulta y Archivo Clandestino",
                    "cost_credits": 40,
                    "cost_materials": "1 Pantalla fosfórica + cables",
                    "effect": "+10% de velocidad en inventarios y clasificaciones logísticas"
                } if hab03_lvl == 1 else None
            },
            {
                "id": "HAB-04",
                "code": "HAB-04",
                "name": "Dormitorio Clandestino / Colaboradores",
                "type": "living",
                "level": hab04_lvl,
                "level_title": "Cuarto de Desahogo Sin Acondicionar" if hab04_lvl == 0 else "Dormitorio de Pasajeros Clandestinos",
                "status": "REQUIERE_LIMPIEZA" if hab04_lvl == 0 else "OPERATIVA",
                "status_color": "amber" if hab04_lvl == 0 else "green",
                "occupants": ["Mara Veyl", "Sael Veyl", "Ilyra Venn"] if hab04_lvl > 0 else ["Cajas y escombros"],
                "equipment": ["Catres improvisados"] if hab04_lvl > 0 else ["Sin mobiliario"],
                "bonus": "Capacidad de alojamiento seguro para 3 personas adicionales sin ocupar camas de trauma" if hab04_lvl > 0 else "Sin uso",
                "next_upgrade": {
                    "title": "Nivel 1: Acondicionamiento de Catres & Iluminación",
                    "cost_credits": 30,
                    "cost_materials": "Mobiliario simple",
                    "effect": "Habilita 2 plazas adicionales de descanso para el séquito"
                } if hab04_lvl == 0 else None
            },
            {
                "id": "COMM-01",
                "code": "COMM-01",
                "name": "Sala Común & Almacén de Víveres",
                "type": "living",
                "level": comm_lvl,
                "level_title": "Comedor & Despensa Básica" if comm_lvl == 1 else "Purificador Hidropónico (Nivel 2)",
                "status": "OPERATIVA",
                "status_color": "green",
                "occupants": ["Punto de reunión del séquito"],
                "equipment": ["Mesa de metal", "Despensa con 48 raciones", "16 botellas de agua 1L"],
                "bonus": "Suministros garantizados para 12 personas durante 4 días" if comm_lvl == 1 else "Generación pasiva de 4 raciones y 4L de agua purificada al día",
                "next_upgrade": {
                    "title": "Nivel 2: Purificador Hidropónico & Cocina de Campo",
                    "cost_credits": 110,
                    "cost_materials": "Filtros + Tubería",
                    "effect": "Generación pasiva de 4 raciones frescas y 4L de agua purificada al día"
                } if comm_lvl == 1 else None
            },
            {
                "id": "SUB-01",
                "code": "SUB-01",
                "name": "Puerta Posterior & Escaleras a Subniveles",
                "type": "fog",
                "level": sub01_lvl,
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
            return {"success": False, "error": f"La sala '{sector['name']}' ya está en su nivel máximo."}
        
        cost = upgrade.get("cost_credits", 0)
        if available_credits < cost:
            return {"success": False, "error": f"Créditos insuficientes ({available_credits} ¤ disponibles, requiere {cost} ¤)."}
        
        current_lvl = upgrades.get(room_id, 1)
        new_lvl = current_lvl + 1
        upgrades[room_id] = new_lvl
        new_credits = available_credits - cost

        log_entry = {
            "time": "Día 04 · Noche",
            "type": "UPGRADE",
            "text": f"¡PROYECTO DE MEJORA EJECUTADO! '{sector['name']}' elevada a Nivel {new_lvl}. Coste: -{cost} ¤. Efecto: {upgrade.get('effect')}"
        }
        logs.insert(0, log_entry)

        cls._save_domain_data(upgrades, sublevel, logs)

        return {
            "success": True,
            "room_id": room_id,
            "room_name": sector["name"],
            "new_level": new_lvl,
            "spent_credits": cost,
            "remaining_credits": new_credits,
            "applied_effect": upgrade.get("effect"),
            "log": log_entry,
            "message": f"Mejora completada con éxito: {sector['name']} ahora es Nivel {new_lvl}."
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
        cls._save_domain_data(upgrades, sublevel, logs)

        bp = cls._get_sublevel_blueprint()
        sector = next((s for s in bp["sectors"] if s["id"] == sector_id), None)

        log_entry = {
            "time": "Día 04 · Noche",
            "type": "EXPLORATION",
            "text": f"{actor} exploró los subniveles y despejó la niebla de guerra en '{sector['name']}'. ¡Bono desbloqueado: {sector['bonus']}!"
        }
        logs.insert(0, log_entry)
        cls._save_domain_data(upgrades, sublevel, logs)

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
        upgrades = data["upgrades"]
        sublevel = data["sublevel"]
        logs = data["logs"]

        log_entry = {
            "time": "Día 04 · Noche",
            "type": "SECURITY",
            "text": f"ASIGNACIÓN TÁCTICA: {npc_name} reasignado a '{task}'."
        }
        logs.insert(0, log_entry)
        cls._save_domain_data(upgrades, sublevel, logs)

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
