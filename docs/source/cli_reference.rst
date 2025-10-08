=============
CLI Reference
=============

Command-line interface for the Sanger DNA Damage Pipeline. All commands are exposed through the Click entry point:

.. code-block:: bash

   python -m src.sanger_pipeline.cli.main [COMMAND] [OPTIONS]

Use ``--help`` on any command for the authoritative list of flags.

.. contents::
   :local:
   :depth: 1

run
===

Run the full pipeline from AB1 files to processed outputs.

.. code-block:: bash

   python -m src.sanger_pipeline.cli.main run \
       --input-dir input \
       --output-dir output_q30 \
       --min-quality 30 \
       --config config/default_config.yaml

**Options**

=======================  ==================  =======================================
Option                   Type               Description
=======================  ==================  =======================================
``--input-dir`` ``-i``   Path (required)    Directory containing AB1 chromatograms.
``--output-dir`` ``-o``  Path (required)    Destination for pipeline results.
``--config`` ``-c``      Path               Custom YAML configuration file.
``--min-quality`` ``-q`` Integer            Override minimum Phred score.
``--min-sequence-length`` ``-l`` Integer    Override minimum sequence length.
``--alignment-tool``     Text               Alignment backend (default: ``mafft``).
``--alignment-params``   Text               Arguments passed to the aligner.
``--help``               Flag               Show command help.
=======================  ==================  =======================================

generate-report
===============

Render the interactive HTML QC report for a previous pipeline run.

.. code-block:: bash

   python -m src.sanger_pipeline.cli.main generate-report \
       --output-dir output_q30 \
       --open-browser

**Options**

=======================  ==================  =======================================
Option                   Type               Description
=======================  ==================  =======================================
``--output-dir`` ``-o``  Path (required)    Pipeline output directory.
``--open-browser``       Flag               Launch the report in the default browser.
``--help``               Flag               Show command help.
=======================  ==================  =======================================

status
======

Summarise the current state of an input directory and its derived results.

.. code-block:: bash

   python -m src.sanger_pipeline.cli.main status --input-dir input

**Option**

=======================  ==================  =======================================
Option                   Type               Description
=======================  ==================  =======================================
``--input-dir`` ``-i``   Path (required)    Directory to inspect for AB1/outputs.
``--help``               Flag               Show command help.
=======================  ==================  =======================================

convert-ab1
===========

Convert a single AB1 chromatogram to FASTA, optionally creating plots and filtered sequences.

.. code-block:: bash

   python -m src.sanger_pipeline.cli.main convert-ab1 sample.ab1 sample.fasta \
       --min-quality 25 --generate-plot

**Options**

==============================  ==================  =======================================
Option                          Type               Description
==============================  ==================  =======================================
``ab1_file``                    Path (argument)    Input AB1 chromatogram.
``output_fasta``                Path (argument)    Output FASTA file.
``--min-quality`` ``-q``        Integer            Minimum Phred quality (default: 20).
``--min-sequence-length`` ``-l`` Integer           Minimum length after filtering (default: 30).
``--generate-plot``             Flag               Write a PNG quality plot next to output.
``--help``                      Flag               Show command help.
==============================  ==================  =======================================

convert-ab1-enhanced
====================

Enhanced conversion with primer trimming, ancient-DNA heuristics, and optional plotting.

.. code-block:: bash

   python -m src.sanger_pipeline.cli.main convert-ab1-enhanced sample.ab1 sample.fasta \
       --primer-config config/primers.yaml --generate-plot

**Notable options**

==============================  ==================  ==============================================
Option                          Type               Description
==============================  ==================  ==============================================
``--primer-config``             Path               YAML primer definitions.
``--primer-forward``            Text               Override forward primers (``region:sequence`` pairs).
``--primer-reverse``            Text               Override reverse primers.
``--disable-primer-removal``    Flag               Keep primers in the output sequence.
``--adna-mode/--modern-mode``   Flag               Toggle relaxed matching for ancient DNA (default: on).
``--show-primer-info``          Flag               Print detected primer details.
==============================  ==================  ==============================================

validate-primers
================

Check primer configuration files for consistency.

.. code-block:: bash

   python -m src.sanger_pipeline.cli.main validate-primers --primer-config my_primers.yaml --show-details

**Options**

=======================  ==================  =======================================
Option                   Type               Description
=======================  ==================  =======================================
``--primer-config``      Path               YAML file to validate (defaults to built-in if omitted).
``--show-details``       Flag               Print loaded primers and matching parameters.
``--help``               Flag               Show command help.
=======================  ==================  =======================================

generate-primer-config
======================

Write a starter primer configuration file.

.. code-block:: bash

   python -m src.sanger_pipeline.cli.main generate-primer-config primers.yaml --template-type comprehensive

**Options**

=======================  ==================  =======================================
Option                   Type               Description
=======================  ==================  =======================================
``output_file``          Path (argument)    Destination file.
``--template-type``      Choice             ``basic`` (default) or ``comprehensive`` sample set.
``--help``               Flag               Show command help.
=======================  ==================  =======================================

convert-to-hsd
==============

Convert consensus FASTA files to the HaploGrep HSD format using BWA-MEM alignment.

.. code-block:: bash

   python -m src.sanger_pipeline.cli.main convert-to-hsd \
       --consensus-dir output_q30/consensus \
       --output haplogroups.hsd

**Options**

=======================  ==================  =======================================
Option                   Type               Description
=======================  ==================  =======================================
``--consensus-dir`` ``-i`` Path (required)  Directory containing consensus FASTA files.
``--output`` ``-o``        Path (required)  Output HSD file.
``--reference`` ``-r``     Path             Reference FASTA (default: ``ref/rCRS.fasta``).
``--help``                 Flag             Show command help.
=======================  ==================  =======================================

analyze-damage
==============

Assess damage patterns for a single FASTA sequence against a reference.

.. code-block:: bash

   python -m src.sanger_pipeline.cli.main analyze-damage \
       --input-file output_q30/final/sample.fasta \
       --reference ref/rCRS.fasta \
       --output-dir damage_single

**Options**

=======================  ==================  =======================================
Option                   Type               Description
=======================  ==================  =======================================
``--input-file`` ``-i``  Path (required)    FASTA file to analyse.
``--reference`` ``-r``   Path (required)    Reference FASTA file.
``--output-dir`` ``-o``  Path (required)    Directory for JSON/plot outputs.
``--sample-name`` ``-s`` Text               Override sample label in outputs.
``--help``               Flag               Show command help.
=======================  ==================  =======================================

damage-summary
==============

Summarise multiple damage-analysis JSON files.

.. code-block:: bash

   python -m src.sanger_pipeline.cli.main damage-summary --results-dir output_q30/damage_analysis

**Option**

=======================  ==================  =======================================
Option                   Type               Description
=======================  ==================  =======================================
``--results-dir`` ``-d`` Path (required)    Folder containing ``*_damage_results.json`` files.
``--help``               Flag               Show command help.
=======================  ==================  =======================================

hsd command group
=================

Utility group for additional HSD converters. Invoke subcommands as ``hsd <name>``.

.. code-block:: bash

   python -m src.sanger_pipeline.cli.main hsd enhanced --consensus-dir output_q30/consensus --output haplogroups.hsd

Subcommands

``enhanced``
   Alignment-backed conversion (recommended). Accepts ``--consensus-dir``, ``--output``, ``--method`` (``aligned`` or ``direct``).

``bwa``
   Shortcut to the BWA-MEM converter with ``--consensus-dir`` and ``--output`` options.

``pipeline``
   Convert full pipeline outputs to HSD via ``scripts/convert_pipeline_to_hsd.py``. Requires ``--input-dir`` and ``--output``; accepts ``--reference``.

Global options
==============

``-v`` / ``--verbose``
   Enable debug logging before command execution.

``--help``
   Display command usage.
     - FLAG
     - Show help for command
   * - ``--verbose``
     - FLAG
     - Enable verbose output
   * - ``--quiet``
     - FLAG
     - Suppress non-error output
   * - ``--log-file``
     - PATH
     - Write logs to file
   * - ``--config-help``
     - FLAG
     - Show configuration help

**Examples**:

.. code-block:: bash

   # Check version
   python -m src.sanger_pipeline.cli.main --version

   # Get help for any command
   python -m src.sanger_pipeline.cli.main run-pipeline --help

   # Verbose logging to file
   python -m src.sanger_pipeline.cli.main run-pipeline \
       --verbose \
       --log-file ./pipeline.log \
       --input-dir ./input \
       --output-dir ./output

📝 Configuration via CLI
========================

Many configuration parameters can be overridden via command line:

**Quality Control Overrides**:

.. code-block:: bash

   python -m src.sanger_pipeline.cli.main run-pipeline \
       --quality-threshold 25 \
       --min-length 75 \
       --input-dir ./input \
       --output-dir ./output

**Damage Analysis Overrides**:

.. code-block:: bash

   python -m src.sanger_pipeline.cli.main analyze-damage \
       --threshold 0.01 \
       --iterations 50000 \
       --input-dir ./sequences \
       --output-dir ./damage

🔄 Chaining Commands
===================

Commands can be chained for custom workflows:

.. code-block:: bash

   # Step-by-step processing
   
   # 1. Convert AB1 to FASTA
   python -m src.sanger_pipeline.cli.main convert \
       --input-dir ./ab1_files \
       --output-dir ./fasta_files
   
   # 2. Run full pipeline on converted files
   python -m src.sanger_pipeline.cli.main run-pipeline \
       --input-dir ./ab1_files \
       --output-dir ./results
   
   # 3. Generate report
   python -m src.sanger_pipeline.cli.main generate-report \
       --output-dir ./results \
       --open-browser
   
   # 4. Check status
   python -m src.sanger_pipeline.cli.main status \
       --output-dir ./results

📊 Exit Codes
=============

All commands return standard exit codes:

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Code
     - Meaning
   * - ``0``
     - Success - command completed without errors
   * - ``1``
     - General error - something went wrong during execution
   * - ``2``
     - Invalid arguments - check command syntax and options
   * - ``3``
     - Input error - files not found or invalid input data
   * - ``4``
     - Configuration error - invalid or missing configuration
   * - ``5``
     - Dependency error - external tools not found or not working
   * - ``6``
     - Output error - cannot write to output directory

**Using exit codes in scripts**:

.. code-block:: bash

   #!/bin/bash
   
   python -m src.sanger_pipeline.cli.main run-pipeline \
       --input-dir ./input \
       --output-dir ./output
   
   if [ $? -eq 0 ]; then
       echo "Pipeline completed successfully"
       python -m src.sanger_pipeline.cli.main generate-report \
           --output-dir ./output \
           --open-browser
   else
       echo "Pipeline failed with exit code $?"
       exit 1
   fi

🌍 Environment Variables
=======================

The CLI respects several environment variables:

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Variable
     - Description
   * - ``SANGER_CONFIG``
     - Default configuration file path
   * - ``SANGER_OUTPUT_DIR``
     - Default output directory
   * - ``SANGER_QUALITY_THRESHOLD``
     - Default quality threshold
   * - ``TMPDIR``
     - Temporary directory for processing
   * - ``MAFFT_BINDIR``
     - MAFFT installation directory

**Using environment variables**:

.. code-block:: bash

   # Set default configuration
   export SANGER_CONFIG=/path/to/my/config.yaml
   
   # Set default output location
   export SANGER_OUTPUT_DIR=/data/sanger_results
   
   # Run with environment defaults
   python -m src.sanger_pipeline.cli.main run-pipeline \
       --input-dir ./input

🔍 Debugging and Troubleshooting
================================

**Enable verbose output**:

.. code-block:: bash

   python -m src.sanger_pipeline.cli.main run-pipeline \
       --verbose \
       --input-dir ./input \
       --output-dir ./output

**Save logs to file**:

.. code-block:: bash

   python -m src.sanger_pipeline.cli.main run-pipeline \
       --log-file ./debug.log \
       --input-dir ./input \
       --output-dir ./output

**Dry run to check inputs**:

.. code-block:: bash

   python -m src.sanger_pipeline.cli.main run-pipeline \
       --dry-run \
       --input-dir ./input \
       --output-dir ./output

**Validate before running**:

.. code-block:: bash

   # Check configuration
   python -m src.sanger_pipeline.cli.main validate \
       --config ./my_config.yaml \
       --check-deps \
       --check-input ./input

📝 Scripting Examples
====================

**Bash script for automated processing**:

.. code-block:: bash

   #!/bin/bash
   # automated_analysis.sh
   
   INPUT_DIR="$1"
   OUTPUT_DIR="$2"
   CONFIG_FILE="${3:-config/default_config.yaml}"
   
   # Validate inputs
   python -m src.sanger_pipeline.cli.main validate \
       --config "$CONFIG_FILE" \
       --check-input "$INPUT_DIR"
   
   if [ $? -ne 0 ]; then
       echo "Validation failed"
       exit 1
   fi
   
   # Run pipeline
   python -m src.sanger_pipeline.cli.main run-pipeline \
       --input-dir "$INPUT_DIR" \
       --output-dir "$OUTPUT_DIR" \
       --config "$CONFIG_FILE" \
       --verbose
   
   # Generate report if pipeline succeeded
   if [ $? -eq 0 ]; then
       python -m src.sanger_pipeline.cli.main generate-report \
           --output-dir "$OUTPUT_DIR" \
           --open-browser
       
       # Show final status
       python -m src.sanger_pipeline.cli.main status \
           --output-dir "$OUTPUT_DIR" \
           --detailed
   fi

**Python script for batch processing**:

.. code-block:: python

   #!/usr/bin/env python3
   # batch_process.py
   
   import subprocess
   import sys
   from pathlib import Path
   
   def run_pipeline(input_dir, output_dir, config_file):
       """Run pipeline with error handling"""
       cmd = [
           sys.executable, "-m", "src.sanger_pipeline.cli.main", 
           "run-pipeline",
           "--input-dir", str(input_dir),
           "--output-dir", str(output_dir),
           "--config", str(config_file)
       ]
       
       result = subprocess.run(cmd, capture_output=True, text=True)
       
       if result.returncode == 0:
           print(f"✓ Successfully processed {input_dir}")
           return True
       else:
           print(f"✗ Failed to process {input_dir}: {result.stderr}")
           return False
   
   # Process multiple directories
   base_dir = Path("./samples")
   output_base = Path("./results")
   config = Path("./config/default_config.yaml")
   
   for sample_dir in base_dir.iterdir():
       if sample_dir.is_dir():
           output_dir = output_base / sample_dir.name
           run_pipeline(sample_dir, output_dir, config)

🆕 Enhanced Quality Control Tools
=================================

.. versionadded:: 2.0

The enhanced quality control tools provide advanced processing for ancient DNA samples.

enhanced_hsd_converter.py
-------------------------

Applies comprehensive quality control to pipeline outputs.

**Syntax**:

.. code-block:: bash

   python enhanced_hsd_converter.py

**Description**:

This tool automatically applies enhanced quality control to the most recent pipeline output:

1. **Combines consensus sequences** from the pipeline output directory
2. **Cleans sequences** using aDNA-specific algorithms
3. **Converts to HSD format** with quality filtering
4. **Performs diversity analysis** with comprehensive reporting

**Output Files**:

* ``{output}_final_cleaned.fasta``: Cleaned consensus sequences
* ``{output}_final_high_quality.hsd``: High-quality HSD file
* Console output with diversity analysis report

**Quality Control Features**:

* **Artifact Removal**: Eliminates common aDNA artifacts
* **Quality Filtering**: 70% quality threshold by default
* **Diversity Analysis**: Comprehensive genetic diversity assessment
* **Sample Prioritization**: Identifies highest-quality samples

Manual Quality Control Tools
----------------------------

For advanced users who want to run quality control steps individually:

aDNA Sequence Cleaner
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from sanger_pipeline.utils.adna_sequence_cleaner import aDNASequenceCleaner
   
   cleaner = aDNASequenceCleaner(min_length=50, min_quality=0.6)
   cleaned_sequences = cleaner.clean_fasta_file("input.fasta", "cleaned.fasta")

Improved HSD Converter
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from sanger_pipeline.utils.improved_fasta_to_hsd_converter import ImprovedFastaToHSDConverter
   
   converter = ImprovedFastaToHSDConverter(min_quality_threshold=0.7)
   converter.convert_fasta_to_hsd("cleaned.fasta", "output.hsd")

HSD Diversity Analyzer
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from sanger_pipeline.utils.hsd_diversity_analyzer import HSDDiversityAnalyzer
   
   analyzer = HSDDiversityAnalyzer()
   samples = analyzer.parse_hsd_file("output.hsd")
   diversity_report = analyzer.analyze_diversity(samples)

This comprehensive CLI reference covers all available commands and options for the Sanger DNA Damage Analysis Pipeline, including the new enhanced quality control features. Use it as a quick reference while working with the pipeline, or for developing automated workflows and scripts.
