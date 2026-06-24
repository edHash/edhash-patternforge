# Usage Guide

edHash PatternForge is a terminal-based tool for controlled pattern generation, storage estimation and authorized security lab workflows.

## Running the tool

From the project root, run:

```bash
python main.py
````

If your environment uses `python3`, run:

```bash
python3 main.py
```

## Main workflow

The tool works through an interactive terminal menu.

Typical flow:

1. Start the tool.
2. Select a generation mode.
3. Configure the character set or audit-oriented inputs.
4. Define length, quantity or target size.
5. Review the estimated output.
6. Generate the local file.
7. Review the generated report if available.

## Output

Generated files are local only.

Recommended practice:

* Keep generated files inside `output/`.
* Do not commit generated `.txt` files.
* Use fictional, owned or explicitly authorized data during lab scenarios.

## Common use cases

* Pattern generation for technical exercises.
* Storage estimation before creating large outputs.
* Defensive auditing simulations.
* Classroom demonstrations.
* Controlled security lab documentation.

## Notes

This project does not require network access, external APIs or cloud services.
