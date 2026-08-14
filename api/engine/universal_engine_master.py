"""
WH40K Universal Engine Master (universal_engine_master.py)
Consolidador Maestro Único con los 24 Subsistemas Universales de Warhammer 40,000.
"""

from typing import Dict, List, Any
import random

class UniversalEngineMaster:

    # 1. CORE D100 & CONTRATO DE APUESTAS
    @staticmethod
    def resolve_d100(valor_base: int, modificadores: List[int], d100_override: int = None) -> Dict[str, Any]:
        mod_total = sum(modificadores)
        umbral_bruto = valor_base + mod_total
        umbral_final = max(5, min(95, umbral_bruto))
        
        d100 = d100_override if d100_override is not None else random.randint(1, 100)
        exito = (d100 <= umbral_final)
        distancia = abs(umbral_final - d100)
        grados = distancia // 10

        resultado_str = "ÉXITO" if exito else "FALLO"
        return {
            "d100_val": d100,
            "umbral_final": umbral_final,
            "resultado_base": resultado_str,
            "grados_num": grados,
            "distancia": distancia,
            "public_roll_text": f"[REGISTRO PÚBLICO CORE.ROLL.001] Resultado: {resultado_str} | Dado: {d100} vs Umbral: {umbral_final}% (Grados: {grados})"
        }

    # 2. COMBATE NAVAL ESPACIAL & ESCUDOS VACÍOS
    @staticmethod
    def resolve_naval_salvo(void_shields: int, hull: int) -> Dict[str, Any]:
        if void_shields > 0:
            return {"new_void_shields": void_shields - 1, "new_hull": hull, "msg": "Impacto absorbido por Escudo Vacío."}
        damage = 5
        new_hull = max(0, hull - damage)
        return {"new_void_shields": 0, "new_hull": new_hull, "msg": f"Impacto directo en Casco (-{damage}). Casco restante: {new_hull}."}

    # 3. REFUERZOS FINITOS ENEMIGOS
    @staticmethod
    def spawn_reinforcements(requested: int, current_pool: int) -> Dict[str, Any]:
        if current_pool <= 0:
            return {"spawned": 0, "remaining_pool": 0, "msg": "¡Sin más refuerzos enemigos! Reserva agotada."}
        spawned = min(requested, current_pool)
        new_pool = current_pool - spawned
        return {"spawned": spawned, "remaining_pool": new_pool, "msg": f"Refuerzos ingresados: {spawned}. Reserva restante: {new_pool}."}

    # 4. BARRA DE DOMINANCIA (0-100%)
    @staticmethod
    def update_combat_progression(current_pct: int, delta: int) -> Dict[str, Any]:
        new_pct = max(0, min(100, current_pct + delta))
        status = "EN_PROGRESO"
        if new_pct >= 100: status = "VICTORIA_ABSOLUTA / OBJETIVO_CUMPLIDO"
        elif new_pct >= 50: status = "PUNTO_DE_INFLEXIÓN / MORAL_ROTA"
        
        bar = "█" * (new_pct // 5) + "░" * (20 - (new_pct // 5))
        return {"new_percentage": new_pct, "status": status, "progress_bar": f"[{bar}] {new_pct}%"}

    # 5. DUELOS & RÉPLICAS
    @staticmethod
    def resolve_duel(defender_stance: str, attacker_failed_by_20: bool) -> Dict[str, Any]:
        counter = (defender_stance.upper() == "RÉPLICA" and attacker_failed_by_20)
        return {"stance": defender_stance, "counter_triggered": counter, "msg": "¡Contraataque de Réplica Desatado!" if counter else "Guardia Mantenida."}

    # 6. JURAMENTOS DE HONOR
    @staticmethod
    def swear_oath(actor: str, title: str) -> Dict[str, Any]:
        return {"actor": actor, "title": title, "status": "JURADO", "msg": f"Juramento '{title}' prestado con honor por {actor}."}

    # 7. CORRUPCIÓN (0-100)
    @staticmethod
    def add_corruption(current: int, added: int) -> Dict[str, Any]:
        new_val = min(100, current + added)
        return {"new_corruption": new_val, "msg": f"Corrupción incrementada a {new_val}/100."}

    # 8. MILAGROS IMPERIALES
    @staticmethod
    def invoke_miracle(faith_pts: int) -> Dict[str, Any]:
        if faith_pts < 1: return {"success": False, "msg": "Fe insuficiente."}
        return {"success": True, "remaining_faith": faith_pts - 1, "msg": "¡Escudo del Emperador Invocado!"}
