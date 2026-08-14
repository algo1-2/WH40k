"""
StateManager: Administrador de Estado Multicampaña (Alexander Necromunda & Ser Caelan Veyr-Hawkshroud)
"""

import json
import os
from typing import Dict, Any, List, Tuple

class StateManager:

    def __init__(self, campaign_id: str = "CAMPAIGN.ALEXANDER.NECROMUNDA"):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.campaign_id = campaign_id

    def get_filepath(self, campaign_id: str = None) -> str:
        cid = campaign_id or self.campaign_id
        
        # Determine campaign folder and filename
        project_root = os.path.dirname(self.base_dir)
        if "CAELAN" in cid.upper():
            local_path = os.path.join(project_root, "campaigns", "caelan", "campaign_state.json")
            filename = "caelan_campaign_state.json" # for tmp
        else:
            local_path = os.path.join(project_root, "campaigns", "alexander", "campaign_state.json")
            filename = "campaign_state.json" # for tmp

        # Priorizar /tmp en Vercel Serverless
        tmp_path = os.path.join("/tmp", filename)
        if os.path.exists(tmp_path):
            return tmp_path

        return local_path

    def load_state(self, campaign_id: str = None) -> Dict[str, Any]:
        filepath = self.get_filepath(campaign_id)
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error cargando estado desde {filepath}: {e}")
        
        # Fallback por defecto si no existe
        return {
            "campaign_id": campaign_id or self.campaign_id,
            "state_revision": 11,
            "character_sheet": {"nombre": "Desconocido", "salud_actual": 12, "salud_maxima": 12}
        }

    def save_state(self, state: Dict[str, Any], campaign_id: str = None) -> bool:
        cid = campaign_id or state.get("campaign_id", self.campaign_id)
        project_root = os.path.dirname(self.base_dir)
        
        if "CAELAN" in cid.upper():
            local_path = os.path.join(project_root, "campaigns", "caelan", "campaign_state.json")
            tmp_filename = "caelan_campaign_state.json"
        else:
            local_path = os.path.join(project_root, "campaigns", "alexander", "campaign_state.json")
            tmp_filename = "campaign_state.json"
        
        target_paths = [
            local_path,
            os.path.join("/tmp", tmp_filename)
        ]

        success = False
        for path in target_paths:
            try:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(state, f, indent=2, ensure_ascii=False)
                success = True
            except Exception as e:
                pass

        return success

    def apply_deltas(self, expected_revision: Any, deltas: List[Dict[str, Any]], campaign_id: str = None) -> Tuple[bool, str, Dict[str, Any]]:
        state = self.load_state(campaign_id)
        curr_rev = state.get("state_revision", 11)

        # Aplicar deltas
        for d in deltas:
            field_path = d.get("field", "")
            op = d.get("operation", "SET")
            val = d.get("value")

            keys = field_path.split("/")
            curr = state
            for k in keys[:-1]:
                if k not in curr or not isinstance(curr[k], dict):
                    curr[k] = {}
                curr = curr[k]

            target_key = keys[-1]
            if op == "SET":
                curr[target_key] = val
            elif op == "INCREMENT":
                curr[target_key] = curr.get(target_key, 0) + val
            elif op == "DECREMENT":
                curr[target_key] = curr.get(target_key, 0) - val

        # Incrementar revisión
        if isinstance(curr_rev, int):
            state["state_revision"] = curr_rev + 1
        elif isinstance(curr_rev, str) and ".R" in curr_rev:
            parts = curr_rev.split(".R")
            try:
                r_num = int(parts[1]) + 1
                state["state_revision"] = f"{parts[0]}.R{r_num}"
            except Exception:
                state["state_revision"] = f"{curr_rev}_UPDATED"
        else:
            state["state_revision"] = 12

        self.save_state(state, campaign_id)
        return True, "Delta aplicada con éxito", state

    def generate_checkpoint(self, campaign_id: str = None) -> Dict[str, Any]:
        state = self.load_state(campaign_id)
        cid = state.get("campaign_id", "CAMPAIGN.ALEXANDER.NECROMUNDA")
        sheet = state.get("character_sheet", {})

        if "CAELAN" in cid.upper():
            chk_text = (
                f"--- [STATE CHECKPOINT | REVISION {state.get('state_revision', 'CAELAN.R2')}] ---\n"
                f"Campaña: {cid} | Turno: {state.get('turn', 929)}\n"
                f"Ubicación: {state.get('location', 'Krastellan (Corredores Interiores)')} | Tiempo: {state.get('time_band', 'Tarde Avanzada')}\n"
                f"Personaje: {sheet.get('nombre', 'Ser Caelan Veyr-Hawkshroud')} ({sheet.get('clase', 'Piloto de Caballero Imperial')})\n"
                f"Salud: {sheet.get('salud_actual', 47)}/{sheet.get('salud_maxima', 47)} | Destino: {sheet.get('puntos_destino', 3)} | Fatiga: {sheet.get('fatiga_actual', 0)}/{sheet.get('fatiga_maxima', 6)}\n"
                f"Fondos: {sheet.get('trons_imperiales', 24000)} Tronos Imperiales\n"
                f"Última Pausa Confirmada: {state.get('persisted_pause_id', 'PAUSE.CAELAN.T928.KRASTELLAN-CORRIDORS')}\n"
            )
        else:
            chk_text = (
                f"--- [STATE CHECKPOINT | REVISION {state.get('state_revision', 11)}] ---\n"
                f"Campaña: {cid} | Turno: {state.get('turn', 916)}\n"
                f"Ubicación: {state.get('location', 'Clínica Clandestina Rho-9 (Dust Falls, Necromunda)')} | Tiempo: {state.get('time_band', 'Día 04, Noche (Post-Incursión)')}\n"
                f"Personaje: {sheet.get('nombre', 'Alexander')} ({sheet.get('clase', 'Operador Umbral / Médico Clandestino')})\n"
                f"Salud: {sheet.get('salud_actual', 12)}/{sheet.get('salud_maxima', 12)} | Destino: {sheet.get('puntos_destino', 3)} | Fatiga: {sheet.get('fatiga_actual', 0)}/{sheet.get('fatiga_maxima', 7)}\n"
                f"Reserva de Almas (Pacto Umbral): {sheet.get('reserva_umbral_almas', 10)} almas completas\n"
                f"Última Pausa Confirmada: {state.get('persisted_pause_id', 'PAUSA-DIA04-NOCHE-2026-08-13-RHO9-POST-INCURSION')}\n"
            )

        return {
            "campaign_id": cid,
            "checkpoint_text": chk_text,
            "state_revision": state.get("state_revision")
        }
