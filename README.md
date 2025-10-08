# Sanger aDNA Damage Pipeline

Process Sanger chromatograms, apply sequence-quality filtering, and review an interactive QC report focused on ancient-DNA damage signatures.

## Requirements

- Python 3.8 or newer
- [MAFFT](https://mafft.cbrc.jp/alignment/software/) in your `PATH` for consensus building
- A Unix-like shell (Linux, macOS, or Windows via WSL2)

## Installation

```bash
git clone https://github.com/allyssonallan/sanger_adna_damage.git
cd sanger_adna_damage
python3 -m venv venv
source venv/bin/activate    # On Windows (WSL2): source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

Create an `input/` folder and place your `.ab1` files inside. The default settings live in `config/default_config.yaml`.

## Run the pipeline

```bash
python -m src.sanger_pipeline.cli.main run \
  --input-dir input \
  --output-dir output_q30 \
  --min-quality 30 \
  --config config/default_config.yaml
```

Use a fresh output directory for each quality threshold:

```bash
# Q10
python -m src.sanger_pipeline.cli.main run --input-dir input --output-dir output_q10 --min-quality 10 --config config/default_config.yaml

# Q20
python -m src.sanger_pipeline.cli.main run --input-dir input --output-dir output_q20 --min-quality 20 --config config/default_config.yaml

# Q30
python -m src.sanger_pipeline.cli.main run --input-dir input --output-dir output_q30 --min-quality 30 --config config/default_config.yaml
```

## Generate the QC report

```bash
python -m src.sanger_pipeline.cli.main generate-report --output-dir output_q30 --open-browser
```

Reports are written to `<output>/reports/` and can be reopened later with any web browser.

## Helpful CLI commands

```bash
# Inspect what has already been processed
python -m src.sanger_pipeline.cli.main status --input-dir input

# Convert a single AB1 chromatogram to FASTA
python -m src.sanger_pipeline.cli.main convert-ab1 sample.ab1 sample.fasta

# Run standalone damage analysis when a reference FASTA is available
python -m src.sanger_pipeline.cli.main analyze-damage \
  --input-file output_q30/final/sample.fasta \
  --reference ref/rCRS.fasta \
  --output-dir damage_single
```

## Documentation

The Sphinx documentation (installation, configuration, troubleshooting, and API details) is published at **[https://allysson.dev.br/sanger_adna_damage/](https://allysson.dev.br/sanger_adna_damage/)**.

## Notes on responsible use

- The pipeline helps triage and prioritise samples; it does **not** authenticate ancient DNA on its own.
- Store run outputs outside the repository if they contain sensitive data.
- Review configuration files before sharing reports to avoid leaking local paths or metadata.

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for full terms.
