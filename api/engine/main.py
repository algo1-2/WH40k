import sys
import os

# Robust path discovery
base_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(base_dir) if os.path.basename(base_dir) in ['engine', 'api'] else base_dir

for p in [
    base_dir,
    os.path.join(base_dir, "subengines"),
    root_dir,
    os.path.join(root_dir, "engine"),
    os.path.join(root_dir, "engine", "subengines"),
    os.path.join(root_dir, "api"),
    os.path.join(root_dir, "api", "engine"),
    os.path.join(root_dir, "api", "engine", "subengines")
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
    title="WH40K Narrative Mechanics Engine API - Clean Architecture v16.0",
    description="API REST determinista con Estructura Limpia y Documentos Dinámicos",
    version="16.0.0",
    servers=[{"url": "https://wh-40k.vercel.app", "description": "Servidor de Producción Vercel"}]
)

class NavalSalvoRequest(BaseModel):
    attacker_ship: str
    defender_ship: str
    defender_void_shields: int
    defender_hull: int

class BoardingActionRequest(BaseModel):
    target_ship_point: str

class OathRequest(BaseModel):
    actor_name: str
    oath_title: str
    objective: str

class FulfillOathRequest(BaseModel):
    oath_id: str
    actor_name: str

class DuelRequest(BaseModel):
    attacker_name: str
    defender_name: str
    defender_stance: str = "DEFENSIVA"

class CampaignSwitchRequest(BaseModel):
    campaign_id: str = "CAMPAIGN.ALEXANDER.NECROMUNDA"

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

class TamingRequest(BaseModel):
    creature_name: str
    actor_taming_skill: int = 52
    creature_ferocity: int = 40

class AnomalousRequest(BaseModel):
    subject_id: str
    stability_level: int = 80

class AssignTaskRequest(BaseModel):
    npc_name: str
    task: str

class LocationQueryRequest(BaseModel):
    location_key: str = "DUST_FALLS"

class TacticalEvalRequest(BaseModel):
    attacker_zone: str = "ZONA_A_QUIRÓFANO"
    target_zone: str = "ZONA_C_ELEVADA"
    target_cover: str = "PESADA"
    attacker_elevated: bool = False
    target_flanked: bool = False

class AlchemySynthesizeRequest(BaseModel):
    compound_key: str = "STIMM_COMBATE"
    medic_skill: int = 75
    available_credits: int = 450

class LoreQueryRequest(BaseModel):
    subfaction_key: str

class LoreSearchRequest(BaseModel):
    keyword: str

class ExploreRequest(BaseModel):
    sublevel_index: int = 1

class LootGenRequest(BaseModel):
    zone_threat_level: int = 3
    scavenger_luck: int = 45

class BuyItemRequest(BaseModel):
    item_key: str
    item_cost: int
    actor_credits: int

class AddCreditsRequest(BaseModel):
    amount: int
    actor_credits: int

class UnjamWeaponRequest(BaseModel):
    weapon_name: str
    ballistics_skill: int = 45

class CorruptionAddRequest(BaseModel):
    amount: int

class MiracleRequest(BaseModel):
    miracle_name: str
    faith_available: int = 10

class RegisterFavorRequest(BaseModel):
    giver: str
    receiver: str
    terms: str
    level: str = "MODERADO"

class ClaimFavorRequest(BaseModel):
    favor_id: str

class DeltaRequest(BaseModel):
    hp_change: Optional[int] = 0
    fatigue_change: Optional[int] = 0
    fate_change: Optional[int] = 0
    soul_change: Optional[int] = 0
    corruption_change: Optional[int] = 0
    ammo_used: Optional[int] = 0
    notes: Optional[str] = "Delta manual"

class ProgressionRequest(BaseModel):
    damage_dealt: int = 0
    tactical_advantage: int = 0
    enemy_count: int = 5

class SpawnReinforcementRequest(BaseModel):
    wave_number: int = 1
    escalation_factor: int = 1

@app.get("/", response_class=HTMLResponse)
@app.get("/dashboard", response_class=HTMLResponse)
def get_dashboard():
    dashboard_path = None
    for candidate in [
        os.path.join(base_dir, "dashboard.html"),
        os.path.join(root_dir, "api", "dashboard.html"),
        os.path.join(base_dir, "api", "dashboard.html"),
        os.path.join(root_dir, "dashboard.html"),
        "api/dashboard.html",
        "dashboard.html"
    ]:
        if os.path.exists(candidate):
            dashboard_path = candidate
            break
            
    if dashboard_path and os.path.exists(dashboard_path):
        with open(dashboard_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>WH40K Dashboard Operativo</h1>"

@app.post("/api/action", dependencies=[Depends(verify_api_key)])
def resolve_action(req: ActionRequest):
    cid = req.campaign_id or "CAMPAIGN.ALEXANDER.NECROMUNDA"
    state = state_mgr.load_state(cid)
    actor_name = req.actor or "Alexander"
    actor_sheet = state.get("character_sheet", {})

    parsed = CommandParser.parse_command(req.user_input)
    if parsed["is_command"]:
        checkpoint = state_mgr.generate_checkpoint(cid)
        return {
            "type": "COMMAND_PARSED",
            "action_code": parsed["action_code"],
            "checkpoint": checkpoint["checkpoint_text"],
            "state_revision": state.get("state_revision"),
            "message": f"Comando procesado: {parsed['command_body']}"
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
        target_value=req.atributo_base or 47,
        modifiers=req.modificadores or []
    )

    delta = MechanicsEngine.calculate_delta(
        roll_result=roll_result,
        stakes=stakes,
        current_state=state,
        weapon_used=req.weapon_used
    )

    state = MechanicsEngine.apply_delta(state, delta)
    checkpoint = state_mgr.generate_checkpoint(cid)
    state_mgr.save_state(state, cid)

    response_payload = {
        "success": roll_result["es_exito"],
        "d100_roll": roll_result["d100"],
        "target_value": roll_result["umbral_final"],
        "degrees": roll_result["grados"],
        "delta": delta,
        "new_state": state,
        "checkpoint": checkpoint["checkpoint_text"],
        "narrative_hint": "Éxito claro" if roll_result["es_exito"] else "Complicación o fallo con consecuencias",
        "combat_info": combat_info,
        "ability_info": ability_info,
        "warp_info": warp_info
    }

    if req.weapon_key:
        dossier = WeaponTraitsEngine.get_weapon_dossier(req.weapon_key)
        response_payload["weapon_dossier"] = dossier

    return response_payload

@app.post("/api/combat/progression", dependencies=[Depends(verify_api_key)])
def combat_progression(req: ProgressionRequest):
    return CombatProgressionEngine.evaluate_progression(req.damage_dealt, req.tactical_advantage, req.enemy_count)

@app.post("/api/enemy/spawn_reinforcements", dependencies=[Depends(verify_api_key)])
def spawn_reinforcements(req: SpawnReinforcementRequest):
    return EnemyReinforcementEngine.calculate_reinforcements(req.wave_number, req.escalation_factor)

@app.post("/api/naval/salvo", dependencies=[Depends(verify_api_key)])
def naval_salvo(req: NavalSalvoRequest):
    return NavalCombatEngine.fire_salvo(req.attacker_ship, req.defender_ship, req.defender_void_shields, req.defender_hull)

@app.post("/api/naval/boarding", dependencies=[Depends(verify_api_key)])
def naval_boarding(req: BoardingActionRequest):
    return NavalCombatEngine.execute_boarding(req.target_ship_point)

@app.post("/api/duel/resolve", dependencies=[Depends(verify_api_key)])
def resolve_duel(req: DuelRequest):
    return DuelEngine.resolve_duel_round(req.attacker_name, req.defender_name, req.defender_stance)

@app.post("/api/oath/swear", dependencies=[Depends(verify_api_key)])
def swear_oath(req: OathRequest):
    return OathLedgerEngine.register_oath(req.actor_name, req.oath_title, req.objective)

@app.post("/api/oath/fulfill", dependencies=[Depends(verify_api_key)])
def fulfill_oath(req: FulfillOathRequest):
    return OathLedgerEngine.fulfill_oath(req.oath_id, req.actor_name)

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
        os.path.join(root_dir, "api", "data", subfolder, filename),
        os.path.join(base_dir, "api", "data", subfolder, filename),
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

@app.post("/api/state/checkpoint", dependencies=[Depends(verify_api_key)])
def get_checkpoint(req: CampaignSwitchRequest):
    return state_mgr.generate_checkpoint(req.campaign_id)

@app.post("/api/beast/tame", dependencies=[Depends(verify_api_key)])
def tame_beast(req: TamingRequest):
    return BeastTamingEngine.attempt_taming(req.creature_name, req.actor_taming_skill, req.creature_ferocity)

@app.post("/api/anomalous/inspect", dependencies=[Depends(verify_api_key)])
def inspect_anomalous_subject(req: AnomalousRequest):
    return AnomalousResearchEngine.evaluate_subject_stability(req.subject_id, req.stability_level)

@app.get("/api/domain/status", dependencies=[Depends(verify_api_key)])
def get_domain_status():
    return DomainManagementEngine.get_rho9_status()

@app.post("/api/domain/assign", dependencies=[Depends(verify_api_key)])
def assign_staff(req: AssignTaskRequest):
    return DomainManagementEngine.assign_staff_task(req.npc_name, req.task)

@app.post("/api/domain/revenue", dependencies=[Depends(verify_api_key)])
def collect_revenue():
    return DomainManagementEngine.calculate_passive_revenue()

@app.post("/api/world/info", dependencies=[Depends(verify_api_key)])
def get_world_info(req: LocationQueryRequest):
    return WorldContextEngine.get_location_context(req.location_key)

@app.post("/api/tactical/evaluate", dependencies=[Depends(verify_api_key)])
def evaluate_tactics(req: TacticalEvalRequest):
    return TacticalMapEngine.calculate_combat_modifiers(
        attacker_zone=req.attacker_zone,
        target_zone=req.target_zone,
        target_cover=req.target_cover,
        attacker_elevated=req.attacker_elevated,
        target_flanked=req.target_flanked
    )

@app.post("/api/alchemy/synthesize", dependencies=[Depends(verify_api_key)])
def synthesize_compound(req: AlchemySynthesizeRequest):
    return AlchemyEngine.synthesize_compound(req.compound_key, req.medic_skill, req.available_credits)

@app.get("/api/weapon/dossier/{weapon_key}", dependencies=[Depends(verify_api_key)])
def get_weapon_dossier_endpoint(weapon_key: str):
    return WeaponTraitsEngine.get_weapon_dossier(weapon_key)

@app.post("/api/lore/query", dependencies=[Depends(verify_api_key)])
def query_subfaction_lore(req: LoreQueryRequest):
    return LoreEncyclopediaEngine.get_subfaction_data(req.subfaction_key)

@app.post("/api/lore/search", dependencies=[Depends(verify_api_key)])
def search_lore(req: LoreSearchRequest):
    return LoreEncyclopediaEngine.search_encyclopedia(req.keyword)

@app.post("/api/exploration/explore", dependencies=[Depends(verify_api_key)])
def explore_sublevel(req: ExploreRequest):
    return MapExplorationEngine.explore_sublevel(req.sublevel_index)

@app.post("/api/loot/generate", dependencies=[Depends(verify_api_key)])
def generate_loot(req: LootGenRequest):
    return LootEngine.generate_scavenge_loot(req.zone_threat_level, req.scavenger_luck)

@app.post("/api/economy/buy", dependencies=[Depends(verify_api_key)])
def buy_item(req: BuyItemRequest):
    return EconomyEngine.process_purchase(req.item_key, req.item_cost, req.actor_credits)

@app.post("/api/economy/credits/add", dependencies=[Depends(verify_api_key)])
def add_credits(req: AddCreditsRequest):
    return EconomyEngine.add_credits(req.amount, req.actor_credits)

@app.post("/api/weapon/unjam", dependencies=[Depends(verify_api_key)])
def unjam_weapon(req: UnjamWeaponRequest):
    return WeaponTraitsEngine.attempt_unjam(req.weapon_name, req.ballistics_skill)

@app.post("/api/corruption/add", dependencies=[Depends(verify_api_key)])
def add_corruption(req: CorruptionAddRequest):
    return CorruptionEngine.add_corruption_points(req.amount)

@app.post("/api/miracles/invoke", dependencies=[Depends(verify_api_key)])
def invoke_miracle(req: MiracleRequest):
    return MiraclesEngine.trigger_faith_miracle(req.miracle_name, req.faith_available)

@app.post("/api/favors/register", dependencies=[Depends(verify_api_key)])
def register_favor(req: RegisterFavorRequest):
    return FavorsLedgerEngine.register_favor(req.giver, req.receiver, req.terms, req.level)

@app.post("/api/favors/claim", dependencies=[Depends(verify_api_key)])
def claim_favor(req: ClaimFavorRequest):
    return FavorsLedgerEngine.claim_favor(req.favor_id)

@app.post("/api/state/delta", dependencies=[Depends(verify_api_key)])
def apply_manual_delta(req: DeltaRequest, x_campaign_id: Optional[str] = Header(None)):
    cid = x_campaign_id or "CAMPAIGN.ALEXANDER.NECROMUNDA"
    state = state_mgr.load_state(cid)
    sheet = state.setdefault("character_sheet", {})
    sheet["salud_actual"] = max(0, min(sheet.get("salud_maxima", 12), sheet.get("salud_actual", 12) + (req.hp_change or 0)))
    sheet["fatiga_actual"] = max(0, min(sheet.get("fatiga_maxima", 7), sheet.get("fatiga_actual", 0) + (req.fatigue_change or 0)))
    sheet["puntos_destino"] = max(0, sheet.get("puntos_destino", 3) + (req.fate_change or 0))
    sheet["reserva_almas"] = max(0, sheet.get("reserva_almas", 10) + (req.soul_change or 0))
    sheet["corrupcion"] = max(0, sheet.get("corrupcion", 0) + (req.corruption_change or 0))
    state_mgr.save_state(state, cid)
    return {"status": "SUCCESS", "message": "Delta aplicado manualmente.", "new_state": state}
