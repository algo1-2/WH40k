"""
WH40K AUTOSYNC â€” Motor de SincronizaciÃ³n AutomÃ¡tica Permanente
==============================================================
Ejecuta automÃ¡ticamente vÃ­a Windows Task Scheduler.

QuÃ© hace:
  1. Lee los 6 archivos .docx maestros desde Desktop/WH40K (fuente de verdad)
  2. Los convierte a .txt puro UTF-8
  3. Los renombra sin espacios (BASES_Y_DOMINIOS.txt, etc.)
  4. Los copia al repositorio local (WH40K-API)
  5. Hace git add + commit + push a GitHub
  6. Vercel detecta el push y redeploya automÃ¡ticamente
  7. Registra todo en un log de auditorÃ­a

NO requiere intervenciÃ³n del usuario.
"""

import os
import sys
import json
import hashlib
import zipfile
import logging
import datetime
import subprocess
import xml.etree.ElementTree as ET

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# CONFIGURACIÃ“N â€” Ajustar solo si cambias rutas en tu PC
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

GIT_EXE = r"C:\Users\UsuarioCompuElite\AppData\Local\GitHubDesktop\app-3.6.4\resources\app\git\cmd\git.exe"
REPO_PATH = r"C:\Users\UsuarioCompuElite\Documents\GitHub\WH40K-API"
DESKTOP_WH40K = r"C:\Users\UsuarioCompuElite\Desktop\WH40K"
SCRATCH_WATCHER = r"C:\Users\UsuarioCompuElite\.gemini\antigravity\scratch\wh40k_engine"
LOG_PATH = r"C:\Users\UsuarioCompuElite\.gemini\antigravity\scratch\wh40k_autosync.log"
HASH_CACHE_PATH = r"C:\Users\UsuarioCompuElite\.gemini\antigravity\scratch\wh40k_file_hashes.json"
VERCEL_TOKEN_PATH = r"C:\Users\UsuarioCompuElite\.gemini\antigravity\scratch\vercel_token.txt"
VERCEL_PROJECT_ID = "prj_WZ0kzEi5YeTJO3j7hWDrYI378TQx"

# Mapa de archivos fuente -> destino en el repo (sin espacios)
DOCUMENT_MAP = {
    "BASES Y DOMINIOS.docx":         "BASES_Y_DOMINIOS",
    "FICHA DEL PERSONAJE.docx":      "FICHA_DEL_PERSONAJE",
    "HISTORIA DEL PERSONAJE.docx":   "HISTORIA_DEL_PERSONAJE",
    "PERSONAJES.docx":               "PERSONAJES",
    "REPUTACION DE FACCIONES.docx":  "REPUTACION_DE_FACCIONES",
    "SEQUITO.docx":                  "SEQUITO",
}

# Carpetas donde buscar los .docx (en orden de prioridad)
SOURCE_DIRS = [
    DESKTOP_WH40K,  # 1. Escritorio (fuente principal)
    SCRATCH_WATCHER,  # 2. Carpeta watcher (si el usuario deja un ZIP aquÃ­)
]

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# LOGGING
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
log = logging.getLogger("wh40k_autosync")

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# UTILIDADES
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def load_hash_cache() -> dict:
    if os.path.exists(HASH_CACHE_PATH):
        try:
            with open(HASH_CACHE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_hash_cache(cache: dict):
    with open(HASH_CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)

def extract_docx_text(path: str) -> str:
    """Extrae texto plano de un archivo .docx."""
    with zipfile.ZipFile(path) as z:
        xml_content = z.read("word/document.xml")
        tree = ET.fromstring(xml_content)
        paragraphs = []
        ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
        for p in tree.iter(f"{ns}p"):
            texts = [node.text for node in p.iter(f"{ns}t") if node.text]
            if texts:
                paragraphs.append("".join(texts))
        return "\n".join(paragraphs)

def run_git(*args) -> tuple:
    result = subprocess.run(
        [GIT_EXE, "-C", REPO_PATH] + list(args),
        capture_output=True, text=True, encoding="utf-8", errors="ignore"
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()

def get_github_token() -> str:
    """Lee el token de GitHub desde Windows Credential Manager."""
    try:
        import ctypes
        import ctypes.wintypes

        class CREDENTIAL(ctypes.Structure):
            _fields_ = [
                ("Flags", ctypes.wintypes.DWORD),
                ("Type", ctypes.wintypes.DWORD),
                ("TargetName", ctypes.c_wchar_p),
                ("Comment", ctypes.c_wchar_p),
                ("LastWritten", ctypes.c_ulonglong),
                ("CredentialBlobSize", ctypes.wintypes.DWORD),
                ("CredentialBlob", ctypes.POINTER(ctypes.c_ubyte)),
                ("Persist", ctypes.wintypes.DWORD),
                ("AttributeCount", ctypes.wintypes.DWORD),
                ("Attributes", ctypes.c_void_p),
                ("TargetAlias", ctypes.c_wchar_p),
                ("UserName", ctypes.c_wchar_p),
            ]

        advapi32 = ctypes.windll.Advapi32
        cred_ptr = ctypes.POINTER(CREDENTIAL)()
        target = "GitHub - https://api.github.com/algo1-2"
        if advapi32.CredReadW(target, 1, 0, ctypes.byref(cred_ptr)):
            cred = cred_ptr.contents
            blob = bytes(cred.CredentialBlob[i] for i in range(cred.CredentialBlobSize))
            advapi32.CredFree(cred_ptr)
            return blob.decode("utf-8")
    except Exception as e:
        log.error(f"No se pudo leer token de GitHub: {e}")
    return ""

def find_docx_in_zip(watch_dir: str) -> dict:
    """Busca archivos .docx dentro de ZIPs en el directorio de observaciÃ³n."""
    found = {}
    for f in os.listdir(watch_dir):
        if f.lower().endswith(".zip"):
            zip_path = os.path.join(watch_dir, f)
            try:
                with zipfile.ZipFile(zip_path) as z:
                    for name in z.namelist():
                        basename = os.path.basename(name)
                        if basename in DOCUMENT_MAP:
                            tmp_path = os.path.join(watch_dir, "_extracted_" + basename)
                            with open(tmp_path, "wb") as out:
                                out.write(z.read(name))
                            found[basename] = tmp_path
                            log.info(f"  ZIP: ExtraÃ­do {basename} desde {f}")
            except Exception as e:
                log.warning(f"  No se pudo leer ZIP {f}: {e}")
    return found

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# SINCRONIZACIÃ“N PRINCIPAL
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def sync():
    log.info("=" * 60)
    log.info("WH40K AUTOSYNC â€” Iniciando sincronizaciÃ³n")
    log.info("=" * 60)

    hash_cache = load_hash_cache()
    changes = []
    tmp_files = []

    # Destino en el repo
    dest_dir = os.path.join(REPO_PATH, "data", "alexander")
    os.makedirs(dest_dir, exist_ok=True)

    # â”€â”€â”€ Buscar archivos fuente â”€â”€â”€
    sources = {}

    # Paso 1: Buscar en carpetas fuente directas
    for src_dir in SOURCE_DIRS:
        if not os.path.isdir(src_dir):
            continue
        for docx_name in DOCUMENT_MAP:
            if docx_name not in sources:
                candidate = os.path.join(src_dir, docx_name)
                if os.path.exists(candidate):
                    sources[docx_name] = candidate
                    log.info(f"  Fuente: {docx_name} <- {src_dir}")

    # Paso 2: Buscar dentro de ZIPs en el watcher
    zip_extracted = find_docx_in_zip(SCRATCH_WATCHER)
    for docx_name, path in zip_extracted.items():
        if docx_name not in sources:
            sources[docx_name] = path
            tmp_files.append(path)

    if not sources:
        log.warning("No se encontraron archivos .docx fuente. Abortando.")
        return False

    # â”€â”€â”€ Convertir y copiar â”€â”€â”€
    for docx_name, src_path in sources.items():
        base_key = DOCUMENT_MAP[docx_name]
        txt_name = base_key + ".txt"
        dest_txt = os.path.join(dest_dir, txt_name)
        dest_docx = os.path.join(dest_dir, base_key + ".docx")

        try:
            # Verificar si cambiÃ³ (por hash)
            current_hash = sha256_file(src_path)
            cached_hash = hash_cache.get(docx_name, "")

            if current_hash == cached_hash and os.path.exists(dest_txt):
                log.info(f"  SIN CAMBIOS: {docx_name} (hash idÃ©ntico, omitiendo)")
                continue

            # Convertir
            text = extract_docx_text(src_path)
            with open(dest_txt, "w", encoding="utf-8") as f:
                f.write(text)

            # Copiar .docx original tambiÃ©n
            import shutil
            shutil.copy2(src_path, dest_docx)

            hash_cache[docx_name] = current_hash
            changes.append(txt_name)
            log.info(f"  ACTUALIZADO: {docx_name} -> {txt_name} ({len(text):,} chars)")

        except Exception as e:
            log.error(f"  ERROR convirtiendo {docx_name}: {e}")

    # â”€â”€â”€ Limpiar temporales de ZIP â”€â”€â”€
    for tmp in tmp_files:
        try:
            os.remove(tmp)
        except Exception:
            pass

    if not changes:
        log.info("Sin cambios detectados. No se hace push.")
        save_hash_cache(hash_cache)
        return True

    # â”€â”€â”€ Git add + commit + push â”€â”€â”€
    log.info(f"\nCambios detectados: {len(changes)} archivos. Haciendo commit...")

    token = get_github_token()
    if not token:
        log.error("No se pudo obtener el token de GitHub. Push abortado.")
        return False

    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    commit_msg = f"AutoSync {ts}: {', '.join(changes)}"

    run_git("add", "-A")
    code, out, err = run_git("commit", "-m", commit_msg)

    if code != 0 and "nothing to commit" in (out + err):
        log.info("Git: nothing to commit (archivos ya sincronizados).")
        save_hash_cache(hash_cache)
        return True

    if code != 0:
        log.error(f"Git commit fallÃ³: {err}")
        return False

    log.info(f"Git commit OK: {commit_msg}")

    for remote_url in [
        f"https://algo1-2:{token}@github.com/algo1-2/WH40K-API.git",
        f"https://algo1-2:{token}@github.com/algo1-2/WH40k.git",
    ]:
        code, out, err = run_git("push", remote_url, "main:main", "--force-with-lease")
        if code == 0:
            log.info(f"  Push OK -> {remote_url.split('@')[1]}")
        else:
            log.warning(f"  Push WARN -> {err}")

    save_hash_cache(hash_cache)
    log.info("AutoSync completado con Ã©xito.\n")
    return True


def get_vercel_token() -> str:
    """Lee el token de Vercel desde el archivo guardado."""
    try:
        if os.path.exists(VERCEL_TOKEN_PATH):
            with open(VERCEL_TOKEN_PATH, "r", encoding="utf-8-sig") as f:
                return f.read().strip().replace("\ufeff", "")
    except Exception as e:
        log.warning(f"No se pudo leer token Vercel: {e}")
    return ""


def vercel_health_check():
    """
    Verifica y auto-corrige la configuracion del proyecto en Vercel:
    1. Asegura que rootDirectory sea None (repo root)
    2. Verifica estado del ultimo deployment
    """
    import urllib.request

    vtoken = get_vercel_token()
    if not vtoken:
        log.info("Vercel health check: sin token, omitiendo.")
        return

    log.info("=== Vercel Health Check ===")

    # Verificar rootDirectory
    try:
        req = urllib.request.Request(
            "https://api.vercel.com/v9/projects/" + VERCEL_PROJECT_ID,
            headers={"Authorization": "Bearer " + vtoken}
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            proj = json.loads(r.read())
        root_dir = proj.get("rootDirectory")
        if root_dir is not None:
            log.warning(f"  rootDirectory = '{root_dir}' (incorrecto). Corrigiendo...")
            patch = json.dumps({"rootDirectory": None}).encode("utf-8")
            req2 = urllib.request.Request(
                "https://api.vercel.com/v9/projects/" + VERCEL_PROJECT_ID,
                data=patch,
                headers={"Authorization": "Bearer " + vtoken, "Content-Type": "application/json"},
                method="PATCH"
            )
            urllib.request.urlopen(req2, timeout=10).close()
            log.info("  rootDirectory corregido a None (repo root).")
        else:
            log.info("  rootDirectory: OK (None = repo root)")
    except Exception as e:
        log.warning(f"  Error verificando rootDirectory: {e}")

    # Verificar ultimo deployment
    try:
        req = urllib.request.Request(
            "https://api.vercel.com/v6/deployments?projectId=" + VERCEL_PROJECT_ID + "&limit=1",
            headers={"Authorization": "Bearer " + vtoken}
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        deploys = data.get("deployments", [])
        if deploys:
            state = deploys[0].get("state", "?")
            url = deploys[0].get("url", "?")
            err = deploys[0].get("errorMessage", "")
            if state == "READY":
                log.info(f"  Ultimo deployment: READY ({url})")
            else:
                log.warning(f"  Ultimo deployment: {state} | {err[:80] if err else 'sin detalle'}")
    except Exception as e:
        log.warning(f"  Error verificando deployments: {e}")

    log.info("==========================")


if __name__ == "__main__":
    try:
        vercel_health_check()
        sync()
    except Exception as e:
        log.exception(f"Error critico en AutoSync: {e}")
        sys.exit(1)

