import sys
import os
import json

# Discover root and subdirectories
base_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(base_dir)

for p in [
    base_dir,
    root_dir,
    os.path.join(root_dir, "engine"),
    os.path.join(root_dir, "engine", "subengines"),
    os.path.join(root_dir, "api")
]:
    if os.path.exists(p) and p not in sys.path:
        sys.path.insert(0, p)

from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from mechanics_engine import MechanicsEngine
from state_manager import StateManager
from command_parser import CommandParser
from universal_engine_master import UniversalEngineMaster

from subengines.npc_generator import NPCGenerator
from subengines.warp_engine import WarpEngine
from subengines.bioware_engine import BiowareEngine
from subengines.pact_ledger import PactLedgerEngine
from subengines.base_engine import BaseDefenseEngine
from subengines.psychology_engine import PsychologyEngine
from subengines.weapon_traits import WeaponTraitsEngine
from subengines.corruption_engine import CorruptionEngine
from subengines.miracles_engine import MiraclesEngine
from subengines.favors_ledger import FavorsLedgerEngine
from subengines.map_exploration_engine import MapExplorationEngine
from subengines.loot_engine import LootEngine
from subengines.economy_engine import EconomyEngine
from subengines.lore_encyclopedia_engine import LoreEncyclopediaEngine
from subengines.tactical_map_engine import TacticalMapEngine
from subengines.alchemy_engine import AlchemyEngine
from subengines.domain_management_engine import DomainManagementEngine
from subengines.world_context_engine import WorldContextEngine
from subengines.beast_taming_engine import BeastTamingEngine
from subengines.anomalous_research_engine import AnomalousResearchEngine
from subengines.duel_engine import DuelEngine
from subengines.oath_ledger_engine import OathLedgerEngine
from subengines.naval_combat_engine import NavalCombatEngine
from subengines.enemy_reinforcement_engine import EnemyReinforcementEngine
from subengines.combat_progression_engine import CombatProgressionEngine

state_mgr = StateManager()
API_KEY_SECRET = os.getenv("API_KEY_SECRET", "wh40k_secret_key_12345")

def verify_api_key(x_api_key: Optional[str] = Header(None)):
    if x_api_key != API_KEY_SECRET:
        raise HTTPException(status_code=401, detail="X-API-Key inválida o no proporcionada.")
    return x_api_key

app = FastAPI(
    title="WH40K Narrative Mechanics Engine API - Modern Production",
    description="API REST determinista con Estructura Limpia y Documentos Dinámicos",
    version="16.5.0",
    servers=[{"url": "https://wh-40k.vercel.app", "description": "Servidor de Producción Vercel"}]
)

class ActionRequest(BaseModel):
    user_input: str
    campaign_id: Optional[str] = "CAMPAIGN.ALEXANDER.NECROMUNDA"
    actor: Optional[str] = "Alexander"
    atributo_base: Optional[int] = 47
    modificadores: Optional[List[int]] = []
    base_logro: Optional[str] = "Cumplir objetivo planteado"
    base_fallo: Optional[str] = "Insuficiencia o peligro activado"
    riesgo_techo: Optional[int] = 3
    weapon_used: Optional[str] = None
    weapon_key: Optional[str] = "PISTOLA_BOLTER"
    weapon_status: Optional[str] = "LIMPIA"
    ability_used: Optional[str] = None
    combat_action: Optional[str] = None
    force_psy_power: Optional[bool] = False

@app.get("/", response_class=HTMLResponse)
@app.get("/dashboard", response_class=HTMLResponse)
def get_dashboard():
    dashboard_path = None
    for candidate in [
        os.path.join(base_dir, "dashboard.html"),
        os.path.join(root_dir, "api", "dashboard.html"),
        os.path.join(root_dir, "dashboard.html")
    ]:
        if os.path.exists(candidate):
            dashboard_path = candidate
            break
            
    if dashboard_path and os.path.exists(dashboard_path):
        with open(dashboard_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>WH40K Dashboard Operativo - Vercel Serverless</h1>"

@app.get("/api/state", dependencies=[Depends(verify_api_key)])
def get_state(x_campaign_id: Optional[str] = Header(None)):
    cid = x_campaign_id or "CAMPAIGN.ALEXANDER.NECROMUNDA"
    return state_mgr.load_state(cid)

@app.get("/api/documents/{filename}", dependencies=[Depends(verify_api_key)])
def get_document(filename: str, x_campaign_id: Optional[str] = Header(None)):
    cid = x_campaign_id or "CAMPAIGN.ALEXANDER.NECROMUNDA"
    subfolder = "caelan" if "CAELAN" in cid.upper() else "alexander"
    
    doc_path = None
    for candidate in [
        os.path.join(root_dir, "data", subfolder, filename),
        os.path.join(base_dir, "data", subfolder, filename),
        os.path.join("data", subfolder, filename),
        filename
    ]:
        if os.path.exists(candidate):
            doc_path = candidate
            break
            
    if doc_path and os.path.exists(doc_path):
        with open(doc_path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"filename": filename, "content": content}
    raise HTTPException(status_code=404, detail=f"Document {filename} not found")

@app.post("/api/action", dependencies=[Depends(verify_api_key)])
def resolve_action(req: ActionRequest):
    cid = req.campaign_id or "CAMPAIGN.ALEXANDER.NECROMUNDA"
    state = state_mgr.load_state(cid)
    actor_name = req.actor or "Alexander"
    actor_sheet = state.setdefault("character_sheet", {})

    parsed = CommandParser.parse_command(req.user_input)
    if parsed.get("is_command"):
        checkpoint = state_mgr.generate_checkpoint(cid)
        return {
            "type": "COMMAND_PARSED",
            "action_code": parsed.get("action_code"),
            "checkpoint": checkpoint.get("checkpoint_text"),
            "state_revision": state.get("state_revision"),
            "message": f"Comando procesado: {parsed.get('command_body')}"
        }

    combat_info = {}
    if req.combat_action:
        curr_combat = state.get("combat_state", {"active": False})
        new_combat = MechanicsEngine.process_combat_state(curr_combat, req.combat_action)
        state["combat_state"] = new_combat
        combat_info = new_combat

    ability_info = {}
    warp_info = {}
    if req.ability_used:
        ability_info = MechanicsEngine.resolve_ability(req.ability_used, actor_sheet)
        if "PSY" in req.ability_used:
            warp_info = WarpEngine.check_warp_phenomena(power_forced=req.force_psy_power)

    classified = MechanicsEngine.classify_route(
        question=req.user_input,
        method="Acción declarada",
        actor=actor_name,
        objective="Objetivo en escena",
        desired_result=req.base_logro
    )

    stakes = MechanicsEngine.freeze_stakes(
        activation_id=classified["activation_id"],
        actor=actor_name,
        desired_result=req.base_logro,
        base_logro=req.base_logro,
        base_fallo=req.base_fallo,
        risks=[{"nivel_base": 1, "techo": req.riesgo_techo, "activador": "CUALQUIER_FALLO"}]
    )

    roll_result = MechanicsEngine.resolve_d100(
        contract_id=stakes["contract_id"],
        actor=actor_name,
        valor_base=req.atributo_base or 47,
        modificadores=req.modificadores or []
    )

    attack_info = {}
    if req.weapon_key:
        weapon_dossier = WeaponTraitsEngine.get_weapon_dossier(req.weapon_key)
        attack_info = WeaponTraitsEngine.resolve_attack_with_traits(req.weapon_key, roll_result.get("es_exito", True), 3)

    state["state_revision"] = state.get("state_revision", 12) + 1
    checkpoint = state_mgr.generate_checkpoint(cid)
    state_mgr.save_state(state, cid)

    response_payload = {
        "success": roll_result.get("es_exito", True),
        "d100_roll": roll_result.get("d100_val", 50),
        "target_value": roll_result.get("umbral_final", 50),
        "degrees": roll_result.get("grados_num", 0),
        "public_roll_text": roll_result.get("public_roll_text", ""),
        "new_state_revision": state.get("state_revision"),
        "current_health": f"{actor_sheet.get('salud_actual', 12)}/{actor_sheet.get('salud_maxima', 12)}",
        "narrative_hint": "Éxito claro" if roll_result.get("es_exito") else "Complicación o fallo con consecuencias",
        "combat_info": combat_info,
        "ability_info": ability_info,
        "warp_info": warp_info,
        "attack_info": attack_info,
        "checkpoint": checkpoint.get("checkpoint_text", "")
    }

    if req.weapon_key:
        response_payload["weapon_dossier"] = WeaponTraitsEngine.get_weapon_dossier(req.weapon_key)

    return response_payload
