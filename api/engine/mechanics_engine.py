"""
WH40K Mechanics Engine v2.0 - Core Deterministic Engine
Protocolo Normativo MECÁNICAS UNIVERSALES (WH40K)

Módulos:
1. Clasificación de Ruta (CORE.ACTIVATE.001)
2. Asignación de Posibilidad (CORE.POSSIBILITY.001)
3. Congelación de Contrato de Apuestas (CORE.STAKES.001)
4. Resolución d100 (CORE.ROLL.001)
5. Oposición y Competencia (CORE.OPPOSE.001)
6. Motor de Combate (COMBAT.ENGINE.001) - Entrada, Salida, Iniciativa, PA/Reacciones
7. Motor de Armas y Equipo (WEAPON.ENGINE.001) - Munición, Estado, AP, Alcance
8. Registro de Habilidades Especiales (ABILITY.ENGINE.001) - Paso Sombrío, Pacto Oscuro, etc.
"""

import math
from typing import Dict, List, Any, Optional

class MechanicsEngine:
    
    # ----------------------------------------------------
    # 1. CLASIFICACIÓN DE RUTA (CORE.ACTIVATE.001)
    # ----------------------------------------------------
    @staticmethod
    def classify_route(question: str, method: str, actor: str, objective: str, desired_result: str) -> Dict[str, Any]:
        """
        Determina si una acción es IMPOSIBLE, AUTOMÁTICA o requiere PRUEBA_D100.
        """
        lower_q = question.lower()
        
        # Criterios de Imposibilidad Absoluta (física, disforme o contextual)
        impossibility_keywords = ["resucitar muerto de dias", "destruir planeta a puñetazos", "detener explosion nuclear con las manos"]
        if any(kw in lower_q for kw in impossibility_keywords):
            return {
                "route": "IMPOSIBLE",
                "activation_id": "ACT_IMPOSSIBLE_001",
                "reason": "La acción excede las leyes físicas, biológicas o psíquicas del entorno sin un artefacto o capacidad legendaria."
            }

        # Criterios de Acción Automática (rutina sin oposición ni peligro)
        routine_keywords = ["caminar", "observar sala", "respirar", "guardar objeto", "hablar", "examinar herida sin prisa"]
        if any(kw in lower_q for kw in routine_keywords) and "combat" not in lower_q and "disparo" not in lower_q:
            return {
                "route": "AUTOMÁTICA",
                "activation_id": "ACT_AUTO_001",
                "reason": "Acción de rutina dentro de las capacidades del personaje sin oposición ni urgencia."
            }

        return {
            "route": "PRUEBA_D100",
            "activation_id": f"ACT_{hash(question) % 100000:05d}",
            "reason": "Existe incertidumbre real, presión de tiempo u oposición activa."
        }

    # ----------------------------------------------------
    # 2. RESOLUCIÓN D100 (CORE.ROLL.001)
    # ----------------------------------------------------
    @staticmethod
    def resolve_d100(contract_id: str, actor: str, valor_base: int, modificadores: List[int], d100_override: Optional[int] = None) -> Dict[str, Any]:
        """
        Resuelve una tirada d100 recortada obligatoriamente al rango 5%-95%.
        """
        import random

        mod_total = sum(modificadores)
        umbral_bruto = valor_base + mod_total
        
        # Umbral recortado a 5% mínimo y 95% máximo segun regla estricta
        umbral_final = max(5, min(95, umbral_bruto))

        d100_val = d100_override if d100_override is not None else random.randint(1, 100)

        es_exito = d100_val <= umbral_final
        resultado_base = "ÉXITO" if es_exito else "FALLO"

        distancia = abs(umbral_final - d100_val)
        grados = distancia // 10

        if es_exito:
            if grados == 0:
                grado_str = "ÉXITO_1 (Menor)"
            elif grados == 1:
                grado_str = "ÉXITO_2 (Sólido)"
            elif grados == 2:
                grado_str = "ÉXITO_3 (Limpio)"
            elif grados >= 3:
                grado_str = f"ÉXITO_{grados + 1} (Magistral)"
        else:
            if grados == 0:
                grado_str = "FALLO_1 (Menor)"
            elif grados == 1:
                grado_str = "FALLO_2 (Serio)"
            elif grados == 2:
                grado_str = "FALLO_3 (Grave)"
            elif grados >= 3:
                grado_str = f"FALLO_{grados + 1} (Crítico)"

        # Críticos
        critico = "NINGUNO"
        if d100_val <= 5:
            critico = "ÉXITO_CRÍTICO_EXTRAORDINARIO"
        elif d100_val >= 96:
            critico = "FALLO_CRÍTICO_DESASTROSO"

        public_text = (
            f"[REGISTRO PÚBLICO CORE.ROLL.001]\n"
            f"Actor: {actor} | Valor Base: {valor_base} | Modificadores: {mod_total:+d} | Umbral Bruto: {umbral_bruto} | Umbral Final: {umbral_final}%\n"
            f"Dado: {d100_val} | Resultado: {grado_str} | Distancia: {distancia} | Crítico: {critico}"
        )

        return {
            "contract_id": contract_id,
            "actor": actor,
            "valor_base": valor_base,
            "modificadores": modificadores,
            "mod_total": mod_total,
            "umbral_final": umbral_final,
            "d100_val": d100_val,
            "resultado_base": resultado_base,
            "grado_str": grado_str,
            "grados_num": grados,
            "distancia": distancia,
            "critico": critico,
            "public_roll_text": public_text
        }

    # ----------------------------------------------------
    # 3. MOTOR DE COMBATE (COMBAT.ENGINE.001)
    # ----------------------------------------------------
    @staticmethod
    def process_combat_state(combat_state: Dict[str, Any], action_type: str) -> Dict[str, Any]:
        """
        Gestiona la entrada, turnos y salida de combate.
        """
        if action_type == "INITIATE_COMBAT":
            return {
                "active": True,
                "round": 1,
                "turn_in_round": 1,
                "pa_available": 2,
                "reactions_available": 1,
                "status_message": "¡COMBATE INICIADO! Se asignan 2 PA y 1 Reacción por ronda."
            }
        elif action_type == "END_COMBAT":
            return {
                "active": False,
                "round": 0,
                "turn_in_round": 0,
                "pa_available": 2,
                "reactions_available": 1,
                "status_message": "Combate finalizado. Se vuelve a modo exploratorio / narrativo."
            }
        elif action_type == "NEXT_ROUND":
            current_round = combat_state.get("round", 1) + 1
            return {
                "active": True,
                "round": current_round,
                "turn_in_round": 1,
                "pa_available": 2,
                "reactions_available": 1,
                "status_message": f"Inicio de Ronda {current_round}. Restablecidos 2 PA y 1 Reacción."
            }
        return combat_state

    # ----------------------------------------------------
    # 4. MOTOR DE ARMAS Y EQUIPO (WEAPON.ENGINE.001)
    # ----------------------------------------------------
    @staticmethod
    def resolve_attack(weapon: Dict[str, Any], roll_result: Dict[str, Any], target_resilience: int = 3, target_cover: int = 0) -> Dict[str, Any]:
        """
        Resuelve el daño de un ataque identificando el estado del arma, penetración (AP) y munición.
        """
        if roll_result["resultado_base"] == "FALLO":
            return {
                "attack_hit": False,
                "damage_dealt": 0,
                "weapon_status": weapon.get("estado", "Limpia"),
                "summary": "El ataque falló. No se causa daño."
            }

        # Verificar munición si usa proyectiles
        ammo_current = weapon.get("municion_actual", None)
        if ammo_current is not None:
            if ammo_current <= 0:
                return {
                    "attack_hit": False,
                    "damage_dealt": 0,
                    "weapon_status": "Sin Munición",
                    "summary": f"¡CLICK! El arma {weapon.get('nombre', 'arma')} no tiene munición disponible."
                }
            weapon["municion_actual"] = ammo_current - 1

        # Cálculo de daño
        base_damage = weapon.get("dano_base", 5)
        ap = weapon.get("penetracion_ap", 2)
        grados_exito = roll_result.get("grados_num", 0)

        # Daño final = Base + Grados de Éxito - (Resiliencia - AP)
        effective_armor = max(0, target_resilience + target_cover - ap)
        damage_dealt = max(1, (base_damage + grados_exito) - effective_armor)

        return {
            "attack_hit": True,
            "damage_dealt": damage_dealt,
            "weapon_name": weapon.get("nombre", "Arma"),
            "ammo_remaining": weapon.get("municion_actual"),
            "weapon_status": weapon.get("estado", "Limpia"),
            "summary": f"¡Impacto de {weapon.get('nombre')}! Daño infligido: {damage_dealt} (AP {ap} redujo armadura/cobertura a {effective_armor})."
        }

    # ----------------------------------------------------
    # 5. REGISTRO DE HABILIDADES ESPECIALES (ABILITY.ENGINE.001)
    # ----------------------------------------------------
    @staticmethod
    def resolve_ability(ability_id: str, actor_sheet: Dict[str, Any], target: Optional[str] = None) -> Dict[str, Any]:
        """
        Resuelve la ejecución directa de habilidades especiales particulares.
        """
        if "SHADOWSTEP" in ability_id:
            return {
                "ability": "Paso Sombrío Rango II",
                "cost_pa": 1,
                "effect": "Desplazamiento automático de hasta 25m a través del Umbral Negro. Materialización Parcial Protegida activa hasta el final del turno.",
                "souls_cost": 0,
                "status": "EJECUTADA"
            }
        elif "DARKVISION" in ability_id:
            return {
                "ability": "Visión de Oscuridad Rango I",
                "cost_pa": 0,
                "effect": "Detección tridimensional pasiva de 15m esféricos. Concede Medicina 75 y detección tridimensional de constantes vitales y sombras.",
                "souls_cost": 0,
                "status": "PASIVA_ACTIVA"
            }
        elif "MEDICALMASTERY" in ability_id:
            return {
                "ability": "Maestría Médica Rango I",
                "cost_pa": 2,
                "effect": "Estabilización de emergencia o cirugía. 'Aún no está muerto' disponible como interrupción de reacción si el paciente agoniza.",
                "souls_cost": 0,
                "status": "DISPONIBLE"
            }
        elif "DARKPACT" in ability_id:
            return {
                "ability": "Pacto Oscuro Rango I",
                "cost_pa": 0,
                "effect": "Vínculo umbral automático ante acuerdo verbal o físico. Reclamación por etapas 1-4 en caso de incumplimiento.",
                "souls_cost": 0,
                "status": "LISTO_PARA_VINCULAR"
            }
        elif "UMBRALGRIP" in ability_id:
            return {
                "ability": "Agarre Umbral Rango II",
                "cost_pa": 1,
                "effect": "Manifestación de extremidades umbrales desde sombras lejanas para golpear, manipular o extraer objetos.",
                "souls_cost": 0,
                "status": "EJECUTADA"
            }
        elif "INFINITE_SHADOW" in ability_id:
            souls = actor_sheet.get("reserva_umbral_almas", 10)
            return {
                "ability": "Sombra Infinita Rango I",
                "cost_pa": 0,
                "effect": f"Acceso a la Reserva Umbral personal. Almas actuales disponibles: {souls}.",
                "souls_available": souls,
                "status": "CONSULTADA"
            }
        return {
            "ability": ability_id,
            "status": "HABILIDAD_DESCONOCIDA"
        }

    # ----------------------------------------------------
    # 6. ASIGNACIÓN DE POSIBILIDAD Y APUESTAS
    # ----------------------------------------------------
    @staticmethod
    def freeze_stakes(activation_id: str, actor: str, desired_result: str, base_logro: str, base_fallo: str, risks: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {
            "contract_id": f"CON_{hash(activation_id) % 100000:05d}",
            "activation_id": activation_id,
            "actor": actor,
            "base_logro": base_logro,
            "base_fallo": base_fallo,
            "risks_frozen": risks
        }
