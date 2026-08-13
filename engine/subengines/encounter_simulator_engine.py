"""
WH40K Tactical Encounter Simulator Engine (encounter_simulator_engine.py)
Simulador determinista de enfrentamientos tácticos en vivo entre el Personaje Jugador (Alexander)
y escuadras enemigas del Bestiario Maestro.
"""

from typing import Dict, List, Any
import sys
import os

# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mechanics_engine import MechanicsEngine
from subengines.npc_generator import NPCGenerator

class EncounterSimulatorEngine:

    @staticmethod
    def simulate_alexander_vs_enforcers() -> Dict[str, Any]:
        """
        Simula una ronda táctica de combate entre Alexander y 3 Enforcers Palatinos en QTN-3.
        """
        log = []
        log.append("=========================================================================")
        log.append("SIMULACION TACTICA EN VIVO: ALEXANDER VS 3 ENFORCERS PALATINOS")
        log.append("Ubicacion: Medicae Station Rho-9 (Subnivel -1, Dust Falls)")
        log.append("=========================================================================\n")

        # 1. ESTADO INICIAL Y BARRA DE DOMINANCIA (0-100%)
        dominance = 30 # Inicia en 30% por emboscada en penumbra
        enforcers_alive = 3

        log.append("ESTADO INICIAL:")
        log.append("   - Alexander: Salud 12/12 | Fatiga 0/7 | Reserva Umbral: 10 Almas")
        log.append("   - Enemigos: 3 Enforcers Palatinos (Salud 15 c/u, Armadura 5)")
        log.append(f"   - Barra de Dominancia de Combate: {dominance}% (Desventaja inicial por cerco)\n")

        # 2. ACCIÓN 1 DE ALEXANDER: PASO SOMBRÍO (RANGO II) -> INTANGIBILIDAD & POSICIONAMIENTO
        log.append("ACCION 1: PASO SOMBRIO (RANGO II) [1 PA]")
        log.append("   - Tipo: Capacidad Automatica (Infalible, sin tirada d100).")
        log.append("   - Efecto: Alexander se desvanece en la penumbra de la pared norte y reaparece a 12m a la espalda del Sargento.")
        log.append("   - Estado Activado: MATERIALIZACION PARCIAL (Silueta de humo/sombra intangible durante 1 turno completo).")
        log.append("   - Bonificador: Intangible a balas mundanas, +10% a Sigilo.\n")

        # 3. ACCIÓN 2 DE ALEXANDER: GOLPE UMBRAL EN CUELLO DEL SARGENTO [1 PA]
        log.append("ACCION 2: GOLPE UMBRAL (RANGO II) EN CUELLO DEL SARGENTO [1 PA]")
        # Tirada de ataque con Voluntad (43%) + 20% bono disputas de Agarre Umbral = 63%
        roll_attack = MechanicsEngine.resolve_d100("CON_SIM_001", "Alexander", 63, [0], d100_override=18)
        log.append(f"   - Tirada d100 (Umbral 63%): {roll_attack['public_roll_text']}")
        log.append("   - Resultado: EXITO SOLIDO (Grado 2). Una garra de penumbra emerge dentro del cuello del Sargento.")
        log.append("   - Dano Aplicado: 3 Dano Fijo.")
        log.append("   - Efecto de Estado Aplicado: RALENTIZADO 1x (Congelacion vascular parcial en zona de cuello).\n")

        # 4. REACCIÓN DE LOS ENFORCERS & RETALIACIÓN INTANGIBLE
        log.append("TURNO ENEMIGO: LOS ENFORCERS ABREN FUEGO DE DISUASION")
        log.append("   - El Enforcer #2 dispara una rafaga de escopeta directamente al pecho de Alexander.")
        log.append("   - EFECTO DE MATERIALIZACION PARCIAL: Los cartuchos de plomo atraviesan la silueta de humo sombrio de Alexander sin infligir ningun dano. Alexander permanece a 12/12 Salud.\n")

        # 5. AVANCE DE LA BARRA DE DOMINANCIA & VERDICTO
        dominance += 35 # Gana +35% por maniobra de intangibilidad e impacto directo en líder
        log.append("ACTUALIZACION DE BARRA DE DOMINANCIA:")
        log.append(f"   - Dominancia de Combate: {dominance}% / 100%")
        log.append("   - Estado Tactico: PUNTO DE INFLEXION ALCANZADO (>50%). Moral de los Enforcers rota por ver disparos atravesar al objetivo.")
        log.append("   - Devolucion de Control: Alexander mantiene la iniciativa con 1 Enforcer ralentizado y 2 desconcertados.\n")
        log.append("=========================================================================")

        return {
            "simulation_text": "\n".join(log),
            "dominance_bar": dominance,
            "alexander_health": "12/12",
            "enforcers_alive": enforcers_alive
        }

if __name__ == "__main__":
    result = EncounterSimulatorEngine.simulate_alexander_vs_enforcers()
    print(result["simulation_text"])
