================
Quick Start Guide
================

This guide takes you from raw AB1 chromatograms to an interactive QC report with the smallest set of commands.

.. warning::
   **Scope Reminder**

   The pipeline prioritises haplogroup screening and damage inspection. Definitive ancient-DNA authentication still requires NGS-based workflows with full contamination controls.

Prerequisites
-------------

* Python 3.8 or newer
* MAFFT available on ``$PATH`` (see :doc:`installation`)
* ``input/`` directory containing your AB1 chromatograms

Step 1 – install the project
----------------------------

.. code-block:: bash

   git clone "https://github.com/allyssonallan/sanger_adna_damage.git"
   cd sanger_adna_damage
   python3 -m venv venv
   source venv/bin/activate  # Windows via WSL2: source venv/bin/activate
   pip install -r requirements.txt
   pip install -e .

Step 2 – prepare your input
---------------------------

.. code-block:: bash

   mkdir -p input
   cp /path/to/*.ab1 input/

Step 3 – run the pipeline
-------------------------

Use a unique output directory for each quality threshold you evaluate.

.. code-block:: bash

   # Example Q30 run
   python -m src.sanger_pipeline.cli.main run \
       --input-dir input \
       --output-dir output_q30 \
       --min-quality 30 \
       --config config/default_config.yaml

Additional thresholds (optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
-------------------------------

.. code-block:: bash

   python -m src.sanger_pipeline.cli.main generate-report \
       --output-dir output_q30 \
       --open-browser

Reports are written to ``<output>/reports/``. Open the HTML file in any modern browser.

Optional helper commands
------------------------

.. code-block:: bash

   # Inspect the current state of the input directory
   python -m src.sanger_pipeline.cli.main status --input-dir input

   # Convert a single AB1 file to FASTA
   python -m src.sanger_pipeline.cli.main convert-ab1 sample.ab1 sample.fasta

   # Run standalone damage analysis with a reference
   python -m src.sanger_pipeline.cli.main analyze-damage \
       --input-file output_q30/final/sample.fasta \
       --reference ref/rCRS.fasta \
       --output-dir damage_single

Output overview
---------------

.. code-block:: text

   output_q30/
   ├── fasta/              # Raw FASTA conversions from AB1
   ├── filtered/           # Quality-filtered sequences
   ├── consensus/          # HVS-region consensus sequences
   ├── final/              # Final merged sequences
   ├── damage_analysis/    # JSON summaries of damage metrics
   ├── plots/              # Quality score visualisations
   └── reports/            # Interactive HTML QC report(s)

Key result files
----------------

``final/``
   Final sequences ready for HSD conversion or other downstream analysis.

``damage_analysis/``
   Per-sample JSON files with bootstrap metrics and transition profiles.

``reports/``
   Interactive HTML reports that summarise processing outcomes, quality, and damage signals.

Interpreting the QC report
--------------------------

* **Overview tab** – Run summary, QC throughput, quick warnings.
* **Damage tab** – Bootstrap-derived damage metrics and transition plots.
* **Quality tab** – Phred score distributions and length profiles.
* **Samples tab** – Per-sample metrics and links to underlying files.

Troubleshooting
---------------

``Command not found``
   Ensure the virtual environment is activated and installation succeeded (``pip install -e .``).

``MAFFT executable missing``
   Install MAFFT and confirm ``mafft --version`` works in your shell; update ``PATH`` if required.

``No AB1 files detected``
   Confirm the ``input/`` folder exists and files use the ``.ab1`` extension.

``Report doesn't open``
   Use ``--open-browser`` or open ``<output>/reports/qc_report_TIMESTAMP.html`` manually.

Next steps
----------

* Tailor the pipeline via :doc:`configuration`.
* Review :doc:`tutorials/index` for end-to-end walkthroughs.
* Explore :doc:`troubleshooting` for more detailed diagnostics.
