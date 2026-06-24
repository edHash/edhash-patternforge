# Security Notes

edHash PatternForge is designed as a local-first security lab utility.

It does not connect to external systems, does not use APIs and does not send generated data anywhere.

## Local execution

The tool runs locally from the terminal.

Generated output remains on the user machine unless manually shared.

## Generated files

Generated `.txt` files, reports and temporary outputs should not be committed to the repository.

The `.gitignore` file is configured to exclude common generated outputs.

## Data handling

Recommended data sources:

- Fictional data.
- Owned datasets.
- Training data.
- Explicitly authorized lab inputs.

Avoid placing private, real or sensitive data inside generated public examples.

## Repository hygiene

Before publishing updates, review:

git status --short

git diff --cached --check

Also verify that generated files, temporary files, archives and local configuration files are not staged.

## Operational mindset

> Controlled input.
> Local output.
> Documented behavior.
> Authorized lab.
