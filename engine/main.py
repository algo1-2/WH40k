import sys
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
sub_dir = os.path.join(base_dir, "subengines")

if base_dir not in sys.path:
    sys.path.insert(0, base_dir)
if sub_dir not in sys.path:
    sys.path.insert(0, sub_dir)
# Asegurar que el directorio actual y subengines estén en sys.path para Vercel
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "subengines"))

from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.responses import HTMLResponse, FileResponse
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
from subengines.character_dossier_engine import CharacterDossierEngine
from subengines.entity_registry_engine import EntityRegistryEngine
from dashboard_template import get_dashboard_html

app = FastAPI(
    title="WH40K Narrative Mechanics Engine API - Clean Architecture v17.0",
    description="API REST determinista con Estructura Limpia y Tactical Command Dashboard",
    version="17.0.0",
    servers=[
        {
            "url": "https://wh-40k.vercel.app",
            "description": "Servidor de Producción Vercel"
        }
    ]
)

@app.get("/", response_class=HTMLResponse)
def get_dashboard():
    """Sirve el Dashboard de Comando Táctico interactivo de Warhammer 40k"""
    return get_dashboard_html()

API_KEY_SECRET = os.getenv("API_KEY_SECRET", "wh40k_secret_key_12345")
state_mgr = StateManager()

def verify_api_key(x_api_key: Optional[str] = Header(None)):
    if x_api_key != API_KEY_SECRET:
        raise HTTPException(status_code=401, detail="X-API-Key inválida o no proporcionada.")
    return x_api_key

# Modelos de solicitud
class ProgressionUpdateRequest(BaseModel):
    current_percentage: int
    delta: int
    cause: str

class ReinforcementSpawnRequest(BaseModel):
    enemy_type: str
    requested_count: int
    current_reinforcement_pool: int

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
    weapon_key: Optional[str] = None
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

class RoomUpgradeRequest(BaseModel):
    room_id: str
    available_credits: int = 1196

class ExploreSectorRequest(BaseModel):
    sector_id: str
    actor: str = "Alexander"

class SurgeryRequest(BaseModel):
    patient_name: str = "Tertius Holt"
    procedure: str = "TORACICA"
    medic_skill: int = 65
    use_diagnostor: bool = True
    use_blood: bool = False

class AlchemyRequest(BaseModel):
    compound_key: str = "STIMM_COMBATE"
    medic_skill: int = 65
    available_credits: int = 1196

class ClaimFavorRequest(BaseModel):
    faction_key: str
    perk_id: str

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

class LootRequest(BaseModel):
    table_key: str = "RHO9_SUBNIVELES"

class BuyRequest(BaseModel):
    item_key: str
    current_credits: int = 450

class AddCreditsRequest(BaseModel):
    amount: int
    source: str

class MiracleRequest(BaseModel):
    miracle_key: str

class CorruptionAddRequest(BaseModel):
    added_points: int
    cause: str

class FavorRegisterRequest(BaseModel):
    faction_name: str
    favor_value: str
    origin: str

class FavorClaimRequest(BaseModel):
    favor_id: str
    faction_name: str

class UnjamRequest(BaseModel):
    weapon_name: str

class ChatSyncRequest(BaseModel):
    event_type: str = "NARRATIVE"
    speaker: str = "Alexander"
    message: str = "Acción descrita en el chat"
    target_room: Optional[str] = None
    advance_turns: Optional[int] = 0
    advance_minutes: Optional[int] = 0

class CraftCyberneticRequest(BaseModel):
    implant_key: str = "BRAZO_BIONICO_MECANICO"
    available_credits: int = 1046
    tech_skill: int = 65

class CompleteContractRequest(BaseModel):
    contract_id: str
    current_credits: int = 1046

class BuyMarketItemRequest(BaseModel):
    item_id: str
    current_credits: int = 1046

class NarrativeParseRequest(BaseModel):
    narrative_text: str

class DeltaRequest(BaseModel):
    campaign_id: Optional[str] = "CAMPAIGN.ALEXANDER.NECROMUNDA"
    expected_revision: Any = 11
    deltas: List[Dict[str, Any]]

# DASHBOARD WEB VISUAL
@app.get("/", response_class=HTMLResponse)
@app.get("/dashboard", response_class=HTMLResponse)
def get_dashboard():
    from engine.dashboard_template import get_dashboard_html
    return get_dashboard_html()

@app.post("/api/action", dependencies=[Depends(verify_api_key)])
def resolve_action(req: ActionRequest, x_campaign_id: Optional[str] = Header(None)):
    cid = req.campaign_id or x_campaign_id or "CAMPAIGN.ALEXANDER.NECROMUNDA"
    state = state_mgr.load_state(cid)
    actor_sheet = state.get("character_sheet", {})
    actor_name = req.actor or actor_sheet.get("nombre", "Alexander")
    
    parsed = CommandParser.parse_input(req.user_input)

    if parsed["is_ooc"]:
        checkpoint = state_mgr.generate_checkpoint(cid)
        return {
            "type": "SYSTEM_RESPONSE",
            "campaign_id": cid,
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
        valor_base=req.atributo_base,
        modificadores=req.modificadores
    )

    attack_info = {}
    if req.weapon_used or req.weapon_key:
        w_key = req.weapon_key or ("PISTOLA_BOLTER" if "Bólter" in str(req.weapon_used) else str(req.weapon_used))
        curr_ammo = 12 if "BOLTER" in w_key.upper() else 10
        attack_info = WeaponTraitsEngine.process_weapon_attack(w_key, curr_ammo, req.weapon_status or "LIMPIA", roll_result)

    try:
        curr_rev = state.get("state_revision", 11)
        curr_turn = state.get("turn", 916)
        
        deltas = [{
            "field": "turn",
            "operation": "INCREMENT",
            "value": 1
        }]

        success, status_msg, updated_state = state_mgr.apply_deltas(curr_rev, deltas, cid)
        rev_num = updated_state.get("state_revision")
        health_actual = updated_state.get("character_sheet", {}).get("salud_actual", 12)
        health_max = updated_state.get("character_sheet", {}).get("salud_maxima", 12)
        health_str = f"{health_actual}/{health_max}"
    except Exception as e:
        success = False
        rev_num = 11
        health_str = "12/12"

    return {
        "type": "RESOLVED_ACTION",
        "campaign_id": cid,
        "classification": classified,
        "stakes": stakes,
        "roll_result": roll_result,
        "public_roll_text": roll_result["public_roll_text"],
        "combat_info": combat_info,
        "ability_info": ability_info,
        "warp_info": warp_info,
        "attack_info": attack_info,
        "state_applied": success,
        "new_state_revision": rev_num,
        "current_health": health_str
    }

# ENDPOINTS DE LA API (v16.0 CLEAN ARCHITECTURE)
@app.post("/api/combat/progression", dependencies=[Depends(verify_api_key)])
def update_progression(req: ProgressionUpdateRequest):
    return CombatProgressionEngine.update_combat_progression(req.current_percentage, req.delta, req.cause)

@app.post("/api/enemy/spawn_reinforcements", dependencies=[Depends(verify_api_key)])
def spawn_reinforcements(req: ReinforcementSpawnRequest):
    return EnemyReinforcementEngine.spawn_reinforcements(req.enemy_type, req.requested_count, req.current_reinforcement_pool)

@app.post("/api/naval/salvo", dependencies=[Depends(verify_api_key)])
def resolve_naval_salvo(req: NavalSalvoRequest):
    return NavalCombatEngine.resolve_naval_salvo(req.attacker_ship, req.defender_ship, req.defender_void_shields, req.defender_hull)

@app.post("/api/naval/boarding", dependencies=[Depends(verify_api_key)])
def initiate_boarding(req: BoardingActionRequest):
    return NavalCombatEngine.initiate_boarding_action(req.target_ship_point)

@app.post("/api/duel/resolve", dependencies=[Depends(verify_api_key)])
def resolve_duel(req: DuelRequest):
    return DuelEngine.resolve_duel_round(req.attacker_name, req.defender_name, req.defender_stance, {"resultado_base": "FALLO", "distancia": 25})

@app.post("/api/oath/swear", dependencies=[Depends(verify_api_key)])
def swear_oath(req: OathRequest):
    return OathLedgerEngine.swear_oath(req.actor_name, req.oath_title, req.objective)

@app.post("/api/oath/fulfill", dependencies=[Depends(verify_api_key)])
def fulfill_oath(req: FulfillOathRequest):
    return OathLedgerEngine.fulfill_oath(req.oath_id, req.actor_name)

@app.get("/api/state", dependencies=[Depends(verify_api_key)])
def get_state(x_campaign_id: Optional[str] = Header(None)):
    """Devuelve el estado autoritativo completo de la campaña y la ficha activa de Alexander"""
    cid = x_campaign_id or "CAMPAIGN.ALEXANDER.NECROMUNDA"
    return state_mgr.load_state(cid)

@app.get("/api/character/abilities", dependencies=[Depends(verify_api_key)])
def get_character_abilities():
    """Devuelve el catálogo detallado de habilidades pasivas, activas y poderes umbrales de Alexander (Visión de Oscuridad, Sombra Infinita, Reserva Umbral, Cirugía de Trauma) con sus mecánicas, bonos y modificadores exactos"""
    return CharacterDossierEngine.get_abilities()

@app.get("/api/character/weapons", dependencies=[Depends(verify_api_key)])
def get_character_weapons():
    """Devuelve el arsenal y fichas balísticas completas de todas las armas disponibles (daño, penetración, cadencia, alcance, capacidad, munición y rasgos de arma)"""
    return CharacterDossierEngine.get_weapons()

@app.get("/api/character/inventory", dependencies=[Depends(verify_api_key)])
def get_character_inventory():
    """Devuelve el inventario estructurado categorizado en tiempo real (Equipo Activo, Botín Incursión, Municiones, Equipo Médico Avanzado, Fármacos y Consumibles)"""
    return CharacterDossierEngine.get_full_inventory()

@app.get("/api/entities", dependencies=[Depends(verify_api_key)])
def list_entities(category: Optional[str] = None, search: Optional[str] = None):
    """Devuelve el registro estructurado de PNJ, Séquito, Pacientes y Contactos con filtros por categoría o búsqueda"""
    return {
        "total": len(EntityRegistryEngine.get_all_entities(category, search)),
        "entities": EntityRegistryEngine.get_all_entities(category, search)
    }

@app.get("/api/entities/{identifier}", dependencies=[Depends(verify_api_key)])
def get_entity_detail(identifier: str):
    """Devuelve el expediente completo, estado clínico, competencias, lealtad y límites de conocimiento de una entidad específica"""
    ent = EntityRegistryEngine.get_entity_by_id_or_name(identifier)
    if not ent:
        raise HTTPException(status_code=404, detail=f"Entidad '{identifier}' no encontrada en el registro canónico.")
    return ent

@app.get("/api/retinue", dependencies=[Depends(verify_api_key)])
def get_retinue_dossier():
    """Devuelve la ficha oficial del Séquito incorporado (Mara Veyl, Ilyra Venn, Halven Rusk) gobernado por SEQUITO.txt"""
    return EntityRegistryEngine.get_retinue()

@app.get("/api/patients", dependencies=[Depends(verify_api_key)])
def get_patients_status():
    """Devuelve el estado clínico y telemetría de todos los pacientes activos en Medicae Station Rho-9 (Tertius, Quartus, Demer Vhal, Sael Veyl)"""
    return {
        "total_patients": len(EntityRegistryEngine.get_patients_telemetry()),
        "patients": EntityRegistryEngine.get_patients_telemetry()
    }

@app.get("/api/rho9/inhabitants", dependencies=[Depends(verify_api_key)])
def get_rho9_inhabitants_endpoint():
    """Devuelve el desglose clasificado de todos los habitantes y personal presente en Medicae Station Rho-9 (Seguridad, Técnico, Admin, Pacientes)"""
    return EntityRegistryEngine.get_rho9_inhabitants()

@app.get("/api/family/{family_name}", dependencies=[Depends(verify_api_key)])
def get_family_members(family_name: str):
    """Devuelve los miembros conocidos de una familia o linaje (ej. Holt: Severan, Tertius, Quartus, Kerrin; Veyl: Mara, Sael)"""
    return {
        "family": family_name,
        "members": EntityRegistryEngine.get_family_tree(family_name)
    }

@app.get("/api/documents", dependencies=[Depends(verify_api_key)])
def list_available_documents():
    """Devuelve la lista de todos los manuales de reglas, instructivos y expedientes disponibles en el sistema"""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    docs = []
    search_dirs = [
        os.path.join(project_root, "lore"),
        os.path.join(project_root, "data", "alexander"),
        os.path.join(project_root, "scripts")
    ]
    for d in search_dirs:
        if os.path.isdir(d):
            for entry in os.listdir(d):
                if entry.endswith((".txt", ".md")):
                    docs.append({"name": entry, "category": os.path.basename(d)})
    return {"total_documents": len(docs), "documents": docs}

@app.get("/api/documents/{filename}", dependencies=[Depends(verify_api_key)])
def get_document(filename: str, x_campaign_id: Optional[str] = Header(None)):
    """Busca y sirve el texto de cualquier documento, manual de DM o ficha de lore"""
    cid = x_campaign_id or "CAMPAIGN.ALEXANDER.NECROMUNDA"
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    search_dirs = [
        os.path.join(project_root, "lore"),
        os.path.join(project_root, "data", "caelan" if "CAELAN" in cid.upper() else "alexander"),
        os.path.join(project_root, "scripts")
    ]
    
    clean_name = filename.strip()
    norm_name = clean_name.replace(" ", "_")
    candidates = [
        clean_name,
        clean_name + ".txt",
        clean_name + ".md",
        norm_name,
        norm_name + ".txt",
        norm_name + ".md"
    ]
    
    for s_dir in search_dirs:
        if not os.path.isdir(s_dir):
            continue
        for cand in candidates:
            cand_path = os.path.join(s_dir, cand)
            if os.path.isfile(cand_path):
                with open(cand_path, "r", encoding="utf-8", errors="ignore") as f:
                    return {"filename": cand, "directory": os.path.basename(s_dir), "content": f.read()}
        
        # Case-insensitive / fuzzy match
        lookup = norm_name.lower().replace(".txt", "").replace(".md", "")
        for entry in os.listdir(s_dir):
            base_entry = entry.lower().replace(".txt", "").replace(".md", "")
            if base_entry == lookup:
                with open(os.path.join(s_dir, entry), "r", encoding="utf-8", errors="ignore") as f:
                    return {"filename": entry, "directory": os.path.basename(s_dir), "content": f.read()}
                    
    raise HTTPException(status_code=404, detail=f"Document '{filename}' not found in server repositories.")

@app.get("/api/inventory", dependencies=[Depends(verify_api_key)])
def get_inventory_legacy(x_campaign_id: Optional[str] = Header(None)):
    cid = x_campaign_id or "CAMPAIGN.ALEXANDER.NECROMUNDA"
    current_state = state_mgr.load_state(cid)
    sheet = current_state.get("character_sheet", {})
    return {
        "campaign_id": cid,
        "character_name": sheet.get("nombre", "Alexander"),
        "location": current_state.get("location"),
        "inventario_activo": sheet.get("inventario_activo", []),
        "inventario_sombra_infinita": sheet.get("inventario_sombra_infinita", {}),
        "recursos_economicos": sheet.get("recursos_economicos", {}),
        "reserva_almas": sheet.get("reserva_almas", 10),
        "puntos_destino": sheet.get("puntos_destino", 3),
        "salud": f"{sheet.get('salud_actual', 12)}/{sheet.get('salud_maxima', 12)}",
        "fatiga": f"{sheet.get('fatiga_actual', 0)}/{sheet.get('fatiga_maxima', 7)}"
    }

@app.post("/api/state/checkpoint", dependencies=[Depends(verify_api_key)])
def get_checkpoint(req: CampaignSwitchRequest):
    return state_mgr.generate_checkpoint(req.campaign_id)

@app.post("/api/beast/tame", dependencies=[Depends(verify_api_key)])
def tame_beast(req: TamingRequest):
    return BeastTamingEngine.attempt_taming(req.creature_name, req.actor_taming_skill, req.creature_ferocity)

@app.post("/api/anomalous/inspect", dependencies=[Depends(verify_api_key)])
def inspect_anomalous(req: AnomalousRequest):
    return AnomalousResearchEngine.inspect_containment_subject(req.subject_id, req.stability_level)

@app.get("/api/domain/status", dependencies=[Depends(verify_api_key)])
def get_domain_status():
    return DomainManagementEngine.get_rho9_status()

@app.get("/api/domain/blueprint", dependencies=[Depends(verify_api_key)])
def get_domain_blueprint(floor: int = 0):
    """Devuelve el plano arquitectónico interactivo y estado de mejoras de Rho-9 por piso (0 o -1)"""
    return DomainManagementEngine.get_rho9_blueprint(floor)

@app.post("/api/domain/upgrade", dependencies=[Depends(verify_api_key)])
def upgrade_room_endpoint(req: RoomUpgradeRequest, x_campaign_id: Optional[str] = Header(None)):
    """Ejecuta un proyecto de mejora para una sala descontando créditos de la base"""
    cid = x_campaign_id or "CAMPAIGN.ALEXANDER.NECROMUNDA"
    res = DomainManagementEngine.execute_room_upgrade(req.room_id, req.available_credits)
    if res.get("success"):
        current_state = state_mgr.load_state(cid)
        recursos = current_state.get("recursos_economicos", {})
        recursos["creditos_disponibles"] = res.get("remaining_credits", req.available_credits)
        current_state["recursos_economicos"] = recursos
        state_mgr.save_state(current_state, cid)
    return res

@app.post("/api/domain/explore_step", dependencies=[Depends(verify_api_key)])
def explore_sublevel_endpoint(req: ExploreSectorRequest):
    """Revela un sector del Subnivel -1 y genera registro de telemetría"""
    return DomainManagementEngine.explore_sublevel_sector(req.sector_id, req.actor)

@app.get("/api/domain/logs", dependencies=[Depends(verify_api_key)])
def get_domain_logs_endpoint():
    """Devuelve los registros de actividad y telemetría de Rho-9"""
    return {"logs": DomainManagementEngine.get_logs()}

@app.post("/api/medicae/operate", dependencies=[Depends(verify_api_key)])
def perform_surgery_endpoint(req: SurgeryRequest):
    """Ejecuta un procedimiento quirúrgico con instrumental y cálculo determinista"""
    return BiowareEngine.perform_surgery(req.patient_name, req.procedure, req.medic_skill, req.use_diagnostor, req.use_blood)

@app.post("/api/medicae/synthesize", dependencies=[Depends(verify_api_key)])
def synthesize_alchemy_endpoint(req: AlchemyRequest, x_campaign_id: Optional[str] = Header(None)):
    """Sintetiza un compuesto químico/farmacológico en el laboratorio de Rho-9 y lo añade a Sombra"""
    cid = x_campaign_id or "CAMPAIGN.ALEXANDER.NECROMUNDA"
    res = AlchemyEngine.synthesize_compound(req.compound_key, req.medic_skill, req.available_credits)
    if res.get("success"):
        current_state = state_mgr.load_state(cid)
        sheet = current_state.get("character_sheet", {})
        sombra = sheet.get("inventario_sombra_infinita", {})
        farmacos = sombra.get("farmacos_y_consumibles", [])
        
        farmacos.append({
            "item": res.get("compound_name"),
            "efecto": res.get("effect"),
            "categoria": "Farmacología Sintetizada en Rho-9"
        })
        sombra["farmacos_y_consumibles"] = farmacos
        sheet["inventario_sombra_infinita"] = sombra
        
        recursos = current_state.get("recursos_economicos", {})
        recursos["creditos_disponibles"] = res.get("remaining_credits", req.available_credits)
        current_state["recursos_economicos"] = recursos
        current_state["character_sheet"] = sheet
        state_mgr.save_state(current_state, cid)
    return res

@app.get("/api/medicae/patient_anatomy", dependencies=[Depends(verify_api_key)])
def get_patient_anatomy_endpoint(patient_name: str = "Quartus Holt"):
    """Devuelve el estado anatómico zonal y cuadro clínico del paciente"""
    return BiowareEngine.get_anatomical_status(patient_name)

@app.post("/api/medicae/craft_cybernetic", dependencies=[Depends(verify_api_key)])
def craft_cybernetic_endpoint(req: CraftCyberneticRequest, x_campaign_id: Optional[str] = Header(None)):
    """Fabricación de implantes cibernéticos y prótesis mecatrónicas en el taller de Khepra-9"""
    cid = x_campaign_id or "CAMPAIGN.ALEXANDER.NECROMUNDA"
    res = BiowareEngine.craft_cybernetic(req.implant_key, req.available_credits, req.tech_skill)
    if res.get("success"):
        current_state = state_mgr.load_state(cid)
        sheet = current_state.get("character_sheet", {})
        sombra = sheet.get("inventario_sombra_infinita", {})
        artefactos = sombra.get("artefactos_arcanos_y_xenotecnologia", [])
        artefactos.append({
            "nombre": res.get("name"),
            "bono": res.get("bonus"),
            "destinatario": res.get("recipient")
        })
        sombra["artefactos_arcanos_y_xenotecnologia"] = artefactos
        sheet["inventario_sombra_infinita"] = sombra
        
        recursos = current_state.get("recursos_economicos", {})
        recursos["creditos_disponibles"] = res.get("remaining_credits", req.available_credits)
        current_state["recursos_economicos"] = recursos
        current_state["character_sheet"] = sheet
        state_mgr.save_state(current_state, cid)
    return res

@app.get("/api/factions/contracts", dependencies=[Depends(verify_api_key)])
def get_faction_contracts_endpoint():
    """Devuelve la lista de contratos clandestinos disponibles de las facciones"""
    return {"contracts": FavorsLedgerEngine.get_contracts()}

@app.post("/api/factions/complete_contract", dependencies=[Depends(verify_api_key)])
def complete_faction_contract_endpoint(req: CompleteContractRequest, x_campaign_id: Optional[str] = Header(None)):
    """Completa un contrato clandestino y abona créditos y favores al estado"""
    cid = x_campaign_id or "CAMPAIGN.ALEXANDER.NECROMUNDA"
    res = FavorsLedgerEngine.complete_contract(req.contract_id, req.current_credits)
    if res.get("success"):
        current_state = state_mgr.load_state(cid)
        sheet = current_state.get("character_sheet", {})
        recursos = current_state.get("recursos_economicos", {})
        recursos["creditos_disponibles"] = res.get("new_credits", req.current_credits)
        current_state["recursos_economicos"] = recursos
        current_state["character_sheet"] = sheet
        state_mgr.save_state(current_state, cid)
    return res

@app.get("/api/market/items", dependencies=[Depends(verify_api_key)])
def get_market_items_endpoint():
    """Devuelve el catálogo de materiales de mejora y reactivos del Mercado Negro de Dust Falls"""
    return {"items": FavorsLedgerEngine.get_market_items()}

@app.post("/api/market/buy", dependencies=[Depends(verify_api_key)])
def buy_market_item_endpoint(req: BuyMarketItemRequest, x_campaign_id: Optional[str] = Header(None)):
    """Compra materiales de mejora en el mercado negro descontando créditos"""
    cid = x_campaign_id or "CAMPAIGN.ALEXANDER.NECROMUNDA"
    res = FavorsLedgerEngine.buy_market_item(req.item_id, req.current_credits)
    if res.get("success"):
        current_state = state_mgr.load_state(cid)
        sheet = current_state.get("character_sheet", {})
        recursos = current_state.get("recursos_economicos", {})
        recursos["creditos_disponibles"] = res.get("remaining_credits", req.current_credits)
        current_state["recursos_economicos"] = recursos
        current_state["character_sheet"] = sheet
        state_mgr.save_state(current_state, cid)
    return res

@app.get("/api/factions/status", dependencies=[Depends(verify_api_key)])
def get_factions_status_endpoint():
    """Devuelve la matriz de reputación y favores de las facciones de Dust Falls"""
    return {"factions": FavorsLedgerEngine.get_factions_status()}

@app.post("/api/factions/claim_favor", dependencies=[Depends(verify_api_key)])
def claim_faction_favor_endpoint(req: ClaimFavorRequest):
    """Reclama un favor activo ante una facción para obtener beneficios"""
    return FavorsLedgerEngine.claim_favor(req.faction_key, req.perk_id)

@app.post("/api/events/generate_patient", dependencies=[Depends(verify_api_key)])
def generate_patient_event_endpoint():
    """Genera una llamada de urgencia médica en la compuerta de Rho-9"""
    return NPCGenerator.generate_clandestine_patient()

@app.post("/api/domain/assign", dependencies=[Depends(verify_api_key)])
def assign_staff(req: AssignTaskRequest):
    return DomainManagementEngine.assign_staff_task(req.npc_name, req.task)

@app.post("/api/domain/revenue", dependencies=[Depends(verify_api_key)])
def collect_revenue():
    return DomainManagementEngine.collect_weekly_revenue(450)

@app.post("/api/world/info", dependencies=[Depends(verify_api_key)])
def get_world_info(req: LocationQueryRequest):
    return WorldContextEngine.get_location_info(req.location_key)

@app.post("/api/tactical/evaluate", dependencies=[Depends(verify_api_key)])
def evaluate_tactical(req: TacticalEvalRequest):
    return TacticalMapEngine.evaluate_tactical_shot(req.attacker_zone, req.target_zone, req.target_cover, req.attacker_elevated, req.target_flanked)

@app.post("/api/alchemy/synthesize", dependencies=[Depends(verify_api_key)])
def synthesize_alchemy(req: AlchemySynthesizeRequest, x_campaign_id: Optional[str] = Header(None)):
    cid = x_campaign_id or "CAMPAIGN.ALEXANDER.NECROMUNDA"
    res = AlchemyEngine.synthesize_compound(req.compound_key, req.medic_skill, req.available_credits)
    if res.get("success"):
        current_state = state_mgr.load_state(cid)
        sheet = current_state.get("character_sheet", {})
        sombra = sheet.get("inventario_sombra_infinita", {})
        farmacos = sombra.get("farmacos_y_consumibles", [])
        farmacos.append({
            "nombre": res.get("compound_name"),
            "efecto": res.get("effect"),
            "categoria": res.get("category", "Farmacología")
        })
        sombra["farmacos_y_consumibles"] = farmacos
        sheet["inventario_sombra_infinita"] = sombra
        
        recursos = current_state.get("recursos_economicos", {})
        recursos["creditos_disponibles"] = res.get("remaining_credits", req.available_credits)
        current_state["recursos_economicos"] = recursos
        current_state["character_sheet"] = sheet
        state_mgr.save_state(current_state, cid)
    return res

@app.get("/api/weapon/dossier/{weapon_key}", dependencies=[Depends(verify_api_key)])
def get_weapon_dossier_endpoint(weapon_key: str):
    return WeaponTraitsEngine.get_weapon_dossier(weapon_key)

@app.post("/api/lore/query", dependencies=[Depends(verify_api_key)])
def query_subfaction_lore(req: LoreQueryRequest):
    return LoreEncyclopediaEngine.query_subfaction(req.subfaction_key)

@app.post("/api/lore/search", dependencies=[Depends(verify_api_key)])
def search_subfaction_lore(req: LoreSearchRequest):
    return LoreEncyclopediaEngine.search_lore(req.keyword)

@app.post("/api/exploration/explore", dependencies=[Depends(verify_api_key)])
def explore_sublevel(req: ExploreRequest):
    return MapExplorationEngine.explore_sector(req.sublevel_index)

@app.post("/api/loot/generate", dependencies=[Depends(verify_api_key)])
def generate_loot(req: LootRequest):
    return LootEngine.generate_loot(req.table_key)

@app.post("/api/economy/buy", dependencies=[Depends(verify_api_key)])
def buy_item(req: BuyRequest):
    return EconomyEngine.buy_item(req.item_key, req.current_credits)

@app.post("/api/economy/credits/add", dependencies=[Depends(verify_api_key)])
def add_credits(req: AddCreditsRequest):
    return EconomyEngine.add_credits(450, req.amount, req.source)

@app.post("/api/weapon/unjam", dependencies=[Depends(verify_api_key)])
def unjam_weapon(req: UnjamRequest):
    return WeaponTraitsEngine.unjam_weapon(req.weapon_name)

@app.post("/api/corruption/add", dependencies=[Depends(verify_api_key)])
def add_corruption(req: CorruptionAddRequest):
    state = state_mgr.load_state()
    curr_corr = state.get("character_sheet", {}).get("corrupcion", 0)
    result = CorruptionEngine.add_corruption(curr_corr, req.added_points, req.cause)
    state_mgr.apply_deltas(state.get("state_revision", 11), [{
        "field": "character_sheet/corrupcion",
        "operation": "SET",
        "value": result["new_points"]
    }])
    return result

@app.post("/api/miracles/invoke", dependencies=[Depends(verify_api_key)])
def invoke_miracle(req: MiracleRequest):
    state = state_mgr.load_state()
    curr_fe = state.get("character_sheet", {}).get("fe", 10)
    return MiraclesEngine.invoke_miracle(req.miracle_key, curr_fe)

@app.post("/api/favors/register", dependencies=[Depends(verify_api_key)])
def register_favor(req: FavorRegisterRequest):
    return FavorsLedgerEngine.register_favor(req.faction_name, req.favor_value, req.origin)

@app.post("/api/favors/claim", dependencies=[Depends(verify_api_key)])
def claim_favor(req: FavorClaimRequest):
    return FavorsLedgerEngine.claim_favor(req.favor_id, req.faction_name)

@app.post("/api/state/delta", dependencies=[Depends(verify_api_key)])
def apply_custom_delta(req: DeltaRequest):
    cid = req.campaign_id or "CAMPAIGN.ALEXANDER.NECROMUNDA"
    success, msg, new_state = state_mgr.apply_deltas(req.expected_revision, req.deltas, cid)
    if not success:
        raise HTTPException(status_code=409, detail=msg)
    return {
        "status": "APLICADA",
        "campaign_id": cid,
        "new_revision": new_state.get("state_revision"),
        "checkpoint": state_mgr.generate_checkpoint(cid)["checkpoint_text"]
    }

@app.post("/api/chat/sync", dependencies=[Depends(verify_api_key)])
def sync_chat_action(req: ChatSyncRequest):
    return DomainManagementEngine.sync_chat_event(
        event_type=req.event_type,
        speaker=req.speaker,
        message=req.message,
        target_room=req.target_room,
        advance_turns=req.advance_turns or 0,
        advance_minutes=req.advance_minutes or 0
    )

@app.get("/api/chat/live_events", dependencies=[Depends(verify_api_key)])
def get_chat_live_events():
    return DomainManagementEngine.get_live_events()

@app.post("/api/chat/parse_narrative", dependencies=[Depends(verify_api_key)])
def parse_chat_narrative(req: NarrativeParseRequest):
    return DomainManagementEngine.parse_narrative_to_sync(req.narrative_text)

@app.get("/api/chat/turn_report", dependencies=[Depends(verify_api_key)])
def get_turn_report_endpoint():
    state = state_mgr.load_state()
    creds = state.get("character_sheet", {}).get("recursos_economicos", {}).get("creditos_disponibles", 1046)
    return {"turn_report": DomainManagementEngine.generate_full_turn_report(creds)}

@app.get("/api/chat/time_directive", dependencies=[Depends(verify_api_key)])
def get_time_directive_endpoint():
    return {"time_directive": DomainManagementEngine.generate_time_directive_prompt()}

@app.get("/api/chat/hud_standard", dependencies=[Depends(verify_api_key)])
def get_hud_standard_endpoint():
    state = state_mgr.load_state()
    creds = state.get("character_sheet", {}).get("recursos_economicos", {}).get("creditos_disponibles", 1046)
    return {"hud_standard": DomainManagementEngine.generate_hud_standard_prompt(creds)}
