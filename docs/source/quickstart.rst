================
Quick Start Guide
================

This guide gets you from raw AB1 chromatograms to an interactive QC report in a few minutes.

.. warning::
   **Scope Reminder**

   The pipeline prioritises haplogroup screening and damage inspection. Definitive ancient-DNA authentication still requires NGS-based workflows with full contamination controls.

Prerequisites
-------------

* Python 3.8 or newer
* MAFFT available on ``$PATH`` (see :doc:`installation`)
* Your AB1 files collected in an ``input/`` directory

Step 1 – install the project
----------------------------

.. code-block:: bash

   git clone "https://github.com/allyssonallan/sanger_adna_damage.git"
   cd sanger_adna_damage
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -e .

Step 2 – (optional) organise working folders
--------------------------------------------

.. code-block:: bash

   mkdir -p input
   cp /path/to/*.ab1 input/

Step 3 – run the pipeline
-------------------------

The CLI command is named ``run``. Use unique output folders for each quality threshold.

.. code-block:: bash

   # Example Q30 run
   python -m src.sanger_pipeline.cli.main run \
       --input-dir input \
       --output-dir output_q30 \
       --min-quality 30 \
       --config config/default_config.yaml

Additional quality thresholds
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Q10
   python -m src.sanger_pipeline.cli.main run \
       --input-dir input \
       --output-dir output_q10 \
       --min-quality 10 \
       --config config/default_config.yaml

   # Q20
   python -m src.sanger_pipeline.cli.main run \
       --input-dir input \
       --output-dir output_q20 \
       --min-quality 20 \
       --config config/default_config.yaml

Step 4 – generate the QC report
--------------------------------

.. code-block:: bash

   python -m src.sanger_pipeline.cli.main generate-report \
       --output-dir output_q20  # swap for output_q10/output_q30 as needed
       --open-browser

The report lives in ``<output>/reports/``. Open the HTML file in any modern browser.

Optional helper commands
------------------------

.. code-block:: bash

   # Inspect the current state of your input folder
   python -m src.sanger_pipeline.cli.main status --input-dir input

   # Convert a single AB1 file to FASTA
   python -m src.sanger_pipeline.cli.main convert-ab1 sample.ab1 sample.fasta

Directory layout reference
--------------------------

Typical output after a run:

.. code-block:: text

   output/
   ├── fasta/              # Raw FASTA conversions from AB1
   │   ├── sample1_F.fasta
   │   ├── sample1_R.fasta
   │   └── ...
   ├── filtered/           # Quality-filtered sequences
   │   ├── sample1_F_filtered.fasta
   │   ├── sample1_R_filtered.fasta
   │   └── ...
   ├── consensus/          # Consensus sequences by HVS region
   │   ├── sample1_HVS1_consensus.fasta
   │   ├── sample1_HVS2_consensus.fasta
   │   ├── sample1_HVS3_consensus.fasta
   │   └── ...
   ├── final/              # Final merged sequences
   │   ├── sample1_final.fasta
   │   └── ...
   ├── damage_analysis/    # Ancient DNA damage analysis
   │   ├── sample1_damage_analysis.json
   │   └── ...
   ├── plots/              # Quality score visualizations
   │   ├── sample1_F_quality.png
   │   └── ...
   └── reports/            # Interactive HTML reports
       └── qc_report_TIMESTAMP.html

Key Result Files
----------------

**Final Sequences (final/ directory)**
   Your processed, consensus sequences ready for downstream analysis

**Damage Analysis (damage_analysis/ directory)**
   JSON files containing ancient DNA damage assessments and statistics

**QC Reports (reports/ directory)**
   Interactive HTML reports with comprehensive analysis summaries

📈 Interpreting the QC Report
=============================

The interactive QC report includes several key sections:

Overview Tab
------------
* **Processing Summary**: Files processed, success rates, errors
* **Quality Metrics**: Average quality scores, sequence lengths
* **HVS Region Coverage**: Which hypervariable regions were successfully processed

Damage Analysis Tab
------------------
* **Damage Assessment**: Overall damage score and interpretation
* **Statistical Significance**: Bootstrap analysis results (p-values)
* **Damage Patterns**: Visual representation of C→T and G→A transitions
* **Quality Indicators**: Confidence metrics for damage assessment

Quality Control Tab
-------------------
* **Sequence Quality**: Distribution of Phred quality scores
* **Length Distribution**: Sequence length statistics
* **Processing Efficiency**: Success rates by processing stage

Sample Details Tab
------------------
* **Individual Results**: Per-sample breakdown of all metrics
* **HVS Region Analysis**: Detailed results for each hypervariable region
* **File Processing**: Status and results for each input file

🔍 Common Scenarios
==================

Scenario 1: Basic Analysis
--------------------------

.. code-block:: bash

   python -m src.sanger_pipeline.cli.main run \
      --input-dir ./my_ab1_files \
      --output-dir ./results

Scenario 2: Custom Quality Threshold
------------------------------------

.. code-block:: bash

   cp config/default_config.yaml my_config.yaml
   # edit my_config.yaml as needed
   python -m src.sanger_pipeline.cli.main run \
      --input-dir ./my_ab1_files \
      --output-dir ./results \
      --config ./my_config.yaml

Scenario 3: Ancient DNA Assessment
----------------------------------

.. code-block:: bash

   python -m src.sanger_pipeline.cli.main run \
      --input-dir ./ancient_samples \
      --output-dir ./ancient_results

   python -m src.sanger_pipeline.cli.main analyze-damage \
      --input-dir ./ancient_results/final \
      --output-dir ./ancient_results/damage_analysis

🛠️ Command Line Interface
=========================

Key Commands
------------

**run-pipeline**: Complete analysis pipeline

.. code-block:: bash

   python -m src.sanger_pipeline.cli.main run-pipeline [OPTIONS]

**generate-report**: Create QC reports

.. code-block:: bash

   python -m src.sanger_pipeline.cli.main generate-report [OPTIONS]

**analyze-damage**: Damage analysis only

.. code-block:: bash

   python -m src.sanger_pipeline.cli.main analyze-damage [OPTIONS]

**status**: Check pipeline status

.. code-block:: bash

   python -m src.sanger_pipeline.cli.main status [OPTIONS]

Common Options
--------------

* ``--input-dir``: Directory containing AB1 files
* ``--output-dir``: Directory for results
* ``--config``: Configuration file path
* ``--quality-threshold``: Override quality threshold
* ``--open-browser``: Open report in browser automatically
* ``--help``: Show help for any command

🔧 Configuration Basics
=======================

The configuration file controls pipeline behavior. Key settings:

Quality Control
---------------

.. code-block:: yaml

   quality_threshold: 20        # Minimum Phred quality score
   min_sequence_length: 50      # Minimum sequence length

Damage Analysis
---------------

.. code-block:: yaml

   damage_threshold: 0.05       # Significance threshold for damage
   bootstrap_iterations: 10000  # Bootstrap analysis iterations

HVS Regions
-----------

.. code-block:: yaml

   hvs_regions:
     HVS1:
       start: 16024
       end: 16365
     HVS2:
       start: 57
       end: 372
     HVS3:
       start: 438
       end: 574

⚡ Performance Tips
==================

For Large Datasets
------------------

1. **Use Quality Pre-filtering**: Set appropriate quality thresholds to reduce processing time
2. **Monitor Memory Usage**: Large datasets may require more RAM
3. **Batch Processing**: Process samples in batches if memory is limited

For Ancient DNA
---------------

1. **Use Conservative Settings**: Lower quality thresholds may be appropriate
2. **Focus on Damage Analysis**: Use the damage analysis tools extensively
3. **Multiple Replicates**: Analyze multiple extractions when possible

🆘 Quick Troubleshooting
========================

Pipeline Fails to Start
-----------------------

.. code-block:: bash

   # Check installation
   python -c "from src.sanger_pipeline.core.pipeline import SangerPipeline"
   
   # Check external dependencies
   mafft --version

No AB1 Files Found
------------------

.. code-block:: bash

   # Check file extensions and directory
   ls -la input/
   
   # Ensure files have .ab1 extension

Quality Issues
--------------

.. code-block:: bash

   # Lower quality threshold temporarily
   python -m src.sanger_pipeline.cli.main run-pipeline \\
       --input-dir ./input \\
       --output-dir ./output \\
       --quality-threshold 15

Memory Errors
-------------

.. code-block:: bash

   # Process smaller batches
   # Split AB1 files into smaller groups
   
   # Monitor memory usage
   top  # or htop on Linux

🎯 Next Steps
=============

Now that you've run your first analysis:

1. **Explore Configuration**: :doc:`configuration` - Customize pipeline behavior
2. **Learn Advanced Features**: :doc:`tutorials/index` - Detailed tutorials
3. **Understand Damage Analysis**: :doc:`understanding_damage_analysis` - Deep dive into aDNA analysis
4. **API Reference**: :doc:`api/index` - For programmatic usage
5. **Troubleshooting**: :doc:`troubleshooting` - Solve common issues

🤝 Getting Help
===============

* **Documentation**: Browse these docs for detailed information
* **GitHub Issues**: Report bugs or request features
* **Community**: Join discussions and get help from other users

Congratulations! You've successfully run the Sanger DNA Damage Analysis Pipeline. The interactive QC report provides a comprehensive overview of your results, and you're ready to dive deeper into ancient DNA analysis.
