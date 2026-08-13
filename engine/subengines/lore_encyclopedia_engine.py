"""
WH40K Sub-Faction Lore Encyclopedia Engine (lore_encyclopedia_engine.py)
Motor de consulta y búsqueda omni-enciclopédica por ENTRY_ID, facción o palabras clave.
"""

import os
from typing import Dict, List, Any

class LoreEncyclopediaEngine:

    @staticmethod
    def get_omni_file_path() -> str:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_dir, "manuales_originales_y_lore", "OMNI_ENCICLOPEDIA_WARHAMMER_40K_MAGNUM_OPUS.md")

    @staticmethod
    def search_lore(keyword: str, entry_id_filter: str = None) -> Dict[str, Any]:
        """
        Busca cualquier término, ENTRY_ID o subfacción en la Omni-Enciclopedia Magnum Opus (2M+ caracteres).
        """
        file_path = LoreEncyclopediaEngine.get_omni_file_path()
        if not os.path.exists(file_path):
            return {
                "keyword": keyword,
                "matches_found": 0,
                "results": [],
                "message": "Archivo de la Omni-Enciclopedia no encontrado."
            }

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        target_query = (entry_id_filter or keyword).upper()
        lines = content.split("\n")
        results = []

        for idx, l in enumerate(lines):
            if target_query in l.upper():
                context_snippet = "\n".join(lines[max(0, idx - 3): min(len(lines), idx + 5)])
                results.append({
                    "line_number": idx + 1,
                    "snippet": context_snippet[:500]
                })
                if len(results) >= 5:
                    break

        return {
            "query": target_query,
            "matches_found": len(results),
            "results": results,
            "message": f"Búsqueda ultra-refinada finalizada para '{target_query}'. Se encontraron {len(results)} extractos en la Omni-Enciclopedia."
        }

    @staticmethod
    def query_subfaction(subfaction_key: str) -> Dict[str, Any]:
        return LoreEncyclopediaEngine.search_lore(subfaction_key)

    @staticmethod
    def query_by_entry_id(entry_id: str) -> Dict[str, Any]:
        return LoreEncyclopediaEngine.search_lore(entry_id, entry_id_filter=entry_id)
