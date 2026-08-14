import re
from typing import Dict, Any

class CommandParser:
    """
    Parser del CATÁLOGO DE COMANDOS DEL JUGADOR (WH40K).
    Diferencia entre:
    - [comando]: Consulta o instrucción fuera de rol / Sistema.
    - (acción): Acción o movimiento físico del personaje activo.
    - texto plano: Diálogo u orden pronunciada por el personaje activo.
    """

    @staticmethod
    def parse_input(raw_input: str) -> Dict[str, Any]:
        text = raw_input.strip()

        # Detectar comandos de sistema [comando]
        bracket_match = re.search(r'\[(.*?)\]', text)
        paren_match = re.search(r'\((.*?)\)', text)

        command_type = "DIALOGUE"
        command_body = text
        is_ooc = False

        if bracket_match:
            command_type = "SYSTEM_COMMAND"
            command_body = bracket_match.group(1).strip().lower()
            is_ooc = True
        elif paren_match:
            command_type = "PHYSICAL_ACTION"
            command_body = paren_match.group(1).strip()
        
        # Mapear comandos específicos del catálogo
        action_code = "CUSTOM_ACTION"
        if is_ooc:
            if "pausa" in command_body:
                action_code = "SESSION_PAUSE"
            elif "confirmar pausa" in command_body:
                action_code = "SESSION_PAUSE_CONFIRM"
            elif "reanudar" in command_body:
                action_code = "SESSION_RESUME"
            elif "ficha" in command_body or "estado completo" in command_body:
                action_code = "QUERY_STATE"
            elif "salud" in command_body or "fatiga" in command_body:
                action_code = "QUERY_HEALTH"
            elif "inventario" in command_body:
                action_code = "QUERY_INVENTORY"
            elif "explicar la prueba" in command_body:
                action_code = "EXPLAIN_TEST"
            elif "no decidas acciones" in command_body:
                action_code = "ENFORCE_AGENCY"

        return {
            "raw_input": raw_input,
            "command_type": command_type,
            "command_body": command_body,
            "is_ooc": is_ooc,
            "action_code": action_code
        }
