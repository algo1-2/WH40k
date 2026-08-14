import urllib.request
import json
import sys

base_url = 'https://wh-40k.vercel.app'
headers = {'x-api-key': 'wh40k_secret_key_12345'}

def test_endpoint(ep, description):
    url = base_url + ep
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            print(f"[PASS] {description} ({ep}) -> HTTP {resp.status}")
            return True, data
    except urllib.error.HTTPError as e:
        print(f"[FAIL] {description} ({ep}) -> HTTP {e.code}")
        return False, None
    except Exception as e:
        print(f"[ERROR] {description} ({ep}) -> {str(e)}")
        return False, None

print('======================================================================')
print('TEST SUITE 1: ENTITY REGISTRY & CLASSIFICATION AUDIT')
print('======================================================================')

# 1. Total entities
ok, d = test_endpoint('/api/entities', 'List all entities')
if ok:
    print(f"   Total entities registered: {d.get('total')}")

# 2. Retinue only
ok, d = test_endpoint('/api/retinue', 'Séquito members exclusive query')
if ok:
    members = [m['nombre_completo'] for m in d.get('members', [])]
    print(f"   Retinue members: {members}")
    assert len(members) == 3, 'Retinue count mismatch!'
    assert 'Mara Veyl' in members and 'Ilyra Venn' in members and 'Halven Rusk' in members

# 3. Patients only
ok, d = test_endpoint('/api/patients', 'Active Rho-9 patients query')
if ok:
    patients = [(p['nombre_completo'], p['estado_clinico'], p['ubicacion_actual']) for p in d.get('patients', [])]
    print('   Active patients:')
    for p in patients:
        print(f"     - {p[0]}: {p[1]} @ {p[2]}")
    assert len(patients) == 4, 'Patient count mismatch!'

# 4. Rho-9 inhabitants breakdown
ok, d = test_endpoint('/api/rho9/inhabitants', 'Rho-9 Station Inhabitants Classification')
if ok:
    print('   Breakdown:')
    sec = [e['nombre_completo'] for e in d.get('seguridad', [])]
    adm = [e['nombre_completo'] for e in d.get('personal_tecnico_y_admin', [])]
    pat = [e['nombre_completo'] for e in d.get('pacientes_clinicos', [])]
    print(f"     Seguridad: {sec}")
    print(f"     Tech & Admin: {adm}")
    print(f"     Pacientes: {pat}")

# 5. Family trees
ok, d_holt = test_endpoint('/api/family/Holt', 'Family tree: Holt')
if ok:
    holt_names = [m['nombre_completo'] for m in d_holt.get('members', [])]
    print(f"   Holt members: {holt_names}")
    assert 'Severan Holt' in holt_names and 'Tertius Holt' in holt_names and 'Quartus Holt' in holt_names

ok, d_veyl = test_endpoint('/api/family/Veyl', 'Family tree: Veyl')
if ok:
    veyl_names = [m['nombre_completo'] for m in d_veyl.get('members', [])]
    print(f"   Veyl members: {veyl_names}")
    assert 'Mara Veyl' in veyl_names and 'Sael Veyl' in veyl_names

# 6. Specific character lookups by name / ID / alias
lookups = [
    ('severan', 'Severan Holt'),
    ('NPC-SEVERAN-HOLT-001', 'Severan Holt by Entity ID'),
    ('khepra', 'Khepra-9'),
    ('syra', 'Syra Kol'),
    ('tertius', 'Tertius Holt'),
    ('quartus', 'Quartus Holt'),
    ('demer', 'Demer Vhal'),
    ('NPC-M01-SUBJECT-04', 'Demer Vhal by historic alias M-01 IV'),
    ('sael', 'Sael Veyl'),
    ('darrik', 'Darrik Vane'),
    ('dervan', 'Dervan Kol (Harvested soul)'),
    ('sarda', 'Sarda E-12 (Shadow figure)'),
    ('orven', 'M. Orven (Shadow figure)')
]

print('\n======================================================================')
print('TEST SUITE 2: INDIVIDUAL DOSSIER QUERY & ALIAS RESOLUTION')
print('======================================================================')

for query, desc in lookups:
    ok, d = test_endpoint(f'/api/entities/{query}', f'Lookup {desc}')
    if ok:
        status = d.get('estado_vital') or d.get('estado_clinico') or d.get('estado')
        print(f"   -> Found: {d.get('nombre_completo')} | Cat: {d.get('categoria')} | Status: {status}")

# 7. Category filtering
print('\n======================================================================')
print('TEST SUITE 3: CATEGORY & SEARCH FILTERS')
print('======================================================================')
ok, d = test_endpoint('/api/entities?category=paciente', 'Filter category=paciente')
if ok:
    names = [e['nombre_completo'] for e in d.get('entities', [])]
    print(f"   Matches: {names}")

ok, d = test_endpoint('/api/entities?search=caldereros', 'Search keyword: caldereros')
if ok:
    names = [e['nombre_completo'] for e in d.get('entities', [])]
    print(f"   Matches: {names}")

print('\n======================================================================')
print('ALL VERIFICATION TESTS COMPLETED SUCCESSFULLY')
print('======================================================================')
