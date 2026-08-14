"""
WH40K AUTOSYNC — Instalador de Tarea en Windows Task Scheduler
==============================================================
Ejecutar UNA SOLA VEZ como administrador para instalar la tarea.
Después de esto, el autosync corre solo: al iniciar Windows y cada 6 horas.
"""
import subprocess
import os
import sys

PYTHON = sys.executable
SCRIPT = r"C:\Users\UsuarioCompuElite\Documents\GitHub\WH40K-API\scripts\wh40k_autosync.py"
TASK_NAME = "WH40K_AutoSync"
LOG = r"C:\Users\UsuarioCompuElite\.gemini\antigravity\scratch\wh40k_autosync.log"

def install_task():
    print(f"Instalando tarea '{TASK_NAME}' en Windows Task Scheduler...")

    # XML de definición de la tarea
    xml = f"""<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <Triggers>
    <TimeTrigger>
      <Repetition>
        <Interval>PT6H</Interval>
        <StopAtDurationEnd>false</StopAtDurationEnd>
      </Repetition>
      <StartBoundary>2026-01-01T00:00:00</StartBoundary>
      <Enabled>true</Enabled>
    </TimeTrigger>
    <LogonTrigger>
      <Enabled>true</Enabled>
    </LogonTrigger>
  </Triggers>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <ExecutionTimeLimit>PT30M</ExecutionTimeLimit>
    <Enabled>true</Enabled>
    <Hidden>true</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <IdleSettings>
      <StopOnIdleEnd>false</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
  </Settings>
  <Actions>
    <Exec>
      <Command>{PYTHON}</Command>
      <Arguments>"{SCRIPT}"</Arguments>
      <WorkingDirectory>C:\\Users\\UsuarioCompuElite\\Documents\\GitHub\\WH40K-API</WorkingDirectory>
    </Exec>
  </Actions>
</Task>"""

    xml_path = r"C:\Users\UsuarioCompuElite\.gemini\antigravity\scratch\wh40k_task.xml"
    with open(xml_path, "w", encoding="utf-16") as f:
        f.write(xml)

    # Eliminar tarea anterior si existe
    subprocess.run(["schtasks", "/Delete", "/TN", TASK_NAME, "/F"],
                   capture_output=True)

    # Crear la nueva tarea
    result = subprocess.run(
        ["schtasks", "/Create", "/TN", TASK_NAME, "/XML", xml_path, "/F"],
        capture_output=True, text=True
    )

    if result.returncode == 0:
        print(f"[OK] Tarea '{TASK_NAME}' instalada correctamente.")
        print("   - Se ejecuta al iniciar Windows")
        print("   - Se ejecuta cada 6 horas automáticamente")
        print(f"   - Log en: {LOG}")

        # Correr inmediatamente para verificar
        print("\nEjecutando primera sincronización...")
        run_result = subprocess.run(
            ["schtasks", "/Run", "/TN", TASK_NAME],
            capture_output=True, text=True
        )
        if run_result.returncode == 0:
            print("[OK] Primera ejecucion lanzada.")
        else:
            print(f"   INFO: {run_result.stderr}")
    else:
        print(f"[ERROR] Error al instalar tarea: {result.stderr}")
        print("   Intenta ejecutar este script como Administrador.")
        # Fallback: correr directamente
        print("\nCorriendo sync directamente como fallback...")
        subprocess.run([PYTHON, SCRIPT])

if __name__ == "__main__":
    install_task()
