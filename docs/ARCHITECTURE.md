# Architecture

edHash PatternForge follows a modular terminal-based structure.

The project separates the interface, generation logic, estimation logic, audit-oriented workflows, reporting and branding into independent Python modules.

## High-level structure

edhash-patternforge/
├── main.py
├── app.py
├── auditoria.py
├── generador.py
├── analizador.py
├── reporte.py
├── ui.py
├── banner.py
├── branding.py
├── docs/
├── examples/
└── output/

## Module overview

### main.py

Main entry point of the tool.

### app.py

Application flow and menu orchestration.

### generador.py

Pattern generation logic.

### analizador.py

Storage estimation, quantity calculations and output analysis.

### auditoria.py

Audit-oriented pattern workflow for authorized lab scenarios.

### reporte.py

Local report generation.

### ui.py

Terminal interaction utilities.

### banner.py

Terminal banner and visual identity.

### branding.py

Project metadata and edHash identity values.

## Design principles

- Local execution.
- No external services.
- No network dependency.
- Modular code organization.
- Terminal-first workflow.
- Documentation-first publication.
- Controlled output generation.
