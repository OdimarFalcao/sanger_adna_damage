# 🧬 Complete Sanger aDNA Pipeline Execution Guide

Follow these steps to run the pipeline end-to-end on a fresh workstation.

## 📋 Prerequisites

1. Clone the repository and enter it:

   ```bash
   git clone https://github.com/allyssonallan/sanger_adna_damage.git
   cd sanger_adna_damage
   ```

2. Create/activate a Python environment, then install the project dependencies:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install -e .
   ```

3. Prepare inputs:

   - Place AB1 chromatograms in an ``input/`` directory.
   - Ensure ``ref/rCRS.fasta`` and ``config/default_config.yaml`` are available (they ship with the repo).

## 🚀 Standard workflow (CLI entry point)

1. **Run the pipeline**

   ```bash
   sanger-pipeline run \
       --input-dir ./input \
       --output-dir ./output_q30 \
       --min-quality 30 \
       --config config/default_config.yaml
   ```

   The command converts AB1 files, applies quality filters, builds consensus sequences, and prepares final FASTA files.

2. **Generate the QC report**

   ```bash
   sanger-pipeline generate-report --output-dir ./output_q30 --open-browser
   ```

   HTML reports are written to ``output_q30/reports/``.

3. **Convert consensus to HSD for HaploGrep**

   ```bash
   sanger-pipeline hsd bwa \
       --consensus-dir ./output_q30/consensus \
       --output ./output_q30/haplogroups_bwa.hsd
   ```

   The BWA-MEM backed converter is the recommended approach for both modern and ancient DNA samples.

## 🐍 Alternative invocation (module form)

If the package is not installed or you want to run from source without ``pip install -e .``, prefix commands with ``python -m src``:

```bash
python -m src.sanger_pipeline.cli.main run --input-dir ./input --output-dir ./output_q30
python -m src.sanger_pipeline.cli.main generate-report --output-dir ./output_q30 --open-browser
```

## 🧾 Automation snippet

For repeated analyses, wrap the workflow in a shell script (store it outside the repo if it logs sensitive paths):

```bash
#!/usr/bin/env bash
set -euo pipefail

sanger-pipeline run --input-dir "$1" --output-dir "$2" --min-quality "${3:-30}" --config config/default_config.yaml
sanger-pipeline generate-report --output-dir "$2"
sanger-pipeline hsd bwa --consensus-dir "$2/consensus" --output "$2/haplogroups_bwa.hsd"

echo "Pipeline complete. Report folder: $2/reports"
```

Call it with ``./run_all.sh input output_q30 30``.

## 📁 Expected output layout

```text
output_q30/
├── consensus/            # HVS consensus FASTA files
├── damage_analysis/      # JSON summaries and plots
├── fasta/                # Raw conversions
├── filtered/             # Quality-filtered sequences
├── final/                # Merged per-sample results
├── plots/                # Quality plots
└── reports/              # HTML QC report(s)
```

Optional extras (alignment results, HSD files) appear alongside the structure above.

## 🔧 Useful commands

```bash
# Inspect what's in the input directory and derived outputs
sanger-pipeline status --input-dir ./input

# Convert a single AB1 file with quality trimming and a diagnostic plot
sanger-pipeline convert-ab1 sample.ab1 sample.fasta --min-quality 25 --generate-plot

# Enhanced AB1 conversion with primer removal in aDNA mode
sanger-pipeline convert-ab1-enhanced sample.ab1 sample.fasta --primer-config config/primers.yaml --generate-plot

# Validate a customised primer configuration
sanger-pipeline validate-primers --primer-config my_primers.yaml --show-details

# Stand-alone damage analysis for one FASTA sequence
sanger-pipeline analyze-damage --input-file output_q30/final/sample.fasta --reference ref/rCRS.fasta --output-dir single_damage

# Summarise multiple damage result JSON files
sanger-pipeline damage-summary --results-dir output_q30/damage_analysis
```

## 🚨 Troubleshooting

| Problem | Suggested fix |
| ------- | -------------- |
| ``command not found`` | Activate the virtual environment or reinstall with ``pip install -e .`` |
| MAFFT/BWA missing | Install the tools via your package manager and ensure they are on ``PATH`` (``mafft --version``). |
| Report fails to open | Re-run with ``--open-browser`` or manually open ``output_q30/reports/qc_report_<timestamp>.html``. |
| Permission denied for scripts | If you copied helper scripts elsewhere, grant execute permissions (``chmod +x``). |
| Unexpected config values | Copy ``config/default_config.yaml`` to a new file, edit, and pass with ``--config``. |

## ✅ Next steps

1. Review the HTML QC report for each run.
2. Upload the generated ``.hsd`` file to `https://haplogrep.i-med.ac.at/` for haplogroup classification.
3. Archive or relocate run outputs if they contain sensitive sample identifiers.

The pipeline is ready for production use with these streamlined commands and defaults.
