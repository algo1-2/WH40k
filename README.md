# WH40K Engine - Ecosistema Universal

Este workspace contiene el motor, base de datos, y campañas de simulación para el Ecosistema Universal de Warhammer 40k.

## Estructura del Proyecto

El proyecto ha sido organizado en las siguientes áreas principales:

* **`engine/`**: Código fuente de Python. Contiene el motor principal (`main.py`, `mechanics_engine.py`, etc.) y la carpeta `subengines/` con 26 módulos especializados.
* **`api/`**: Configuraciones de despliegue web y API (Vercel, OpenAPI, Dashboard HTML).
* **`lore/`**: Enciclopedias maestras, manuales del jugador/DM y borradores de cosmología. Incluye los documentos `.docx` originales en `originales_docx/`.
* **`campaigns/`**: Carpetas aisladas por campaña (Alexander, Caelan, Flota Exploradora). Cada una tiene sus propios registros, plantillas y archivos de estado (JSON).
* **`data/`**: Textos extraídos que utiliza el motor para el análisis rápido, separados por la campaña u origen del que provienen.
* **`_archive/`**: Archivos obsoletos, scripts de un solo uso de versiones previas, bundles antiguos (ZIP) y copias duplicadas, mantenidos como historial pero removidos del foco principal.
