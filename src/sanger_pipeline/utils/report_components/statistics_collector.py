"""
Statistics collection for Sanger Pipeline QC reports.

This module handles all data collection and analysis for generating
comprehensive QC reports, including pipeline statistics, damage analysis,
and sample-level metrics.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml
import pandas as pd

logger = logging.getLogger(__name__)


class StatisticsCollector:
    """Collects and analyzes pipeline statistics for QC reporting."""

    def __init__(self, output_dir: Path, damage_plotter=None):
        """
        Initialize statistics collector.

        Args:
            output_dir: Pipeline output directory
            damage_plotter: Optional damage plot generator instance
        """
        self.output_dir = Path(output_dir)
        self.damage_plotter = damage_plotter

    def collect_pipeline_statistics(self) -> Dict[str, Any]:
        """
        Collect comprehensive pipeline statistics.

        Returns:
            Dictionary containing all collected statistics
        """
        logger.info("Collecting pipeline statistics...")

        stats: Dict[str, Any] = {
            "report_generated": datetime.now().isoformat(),
            "pipeline_version": "2.0.0",
            "output_directory": str(self.output_dir),
        }

        # Load run metadata if available (captures effective configuration and overrides)
        run_metadata = self._try_read_json(self.output_dir / "run_metadata.json")
        if run_metadata:
            stats["run_metadata"] = run_metadata
            stats["quality_settings"] = run_metadata.get("quality", {})
            stats["cli_overrides"] = run_metadata.get("cli_overrides", {})

        # Analyze pipeline directories (stored both collectively and for backward compatibility)
        directories_to_analyze = {
            "output": self.output_dir / "output",
            "fasta": self.output_dir / "fasta",
            "filtered": self.output_dir / "filtered",
            "consensus": self.output_dir / "consensus",
            "final": self.output_dir / "final",
            "aligned": self.output_dir / "aligned",
            "damage_analysis": self.output_dir / "damage_analysis",
            "plots": self.output_dir / "plots",
            "reports": self.output_dir / "reports",
        }

        directories_stats: Dict[str, Any] = {}
        for key, path in directories_to_analyze.items():
            directories_stats[key] = self._analyze_directory(path)

        stats["directories"] = directories_stats

        # Maintain legacy keys referenced elsewhere in the codebase
        for legacy_key in ["input", "output", "consensus", "final"]:
            if legacy_key in directories_stats:
                stats[legacy_key] = directories_stats[legacy_key]

        # Capture configuration parameters used for the run (prefer effective metadata)
        config_parameters = (
            run_metadata.get("config_parameters", {}) if run_metadata else {}
        )
        config_source: Optional[Path] = None

        if config_parameters:
            config_source = self.output_dir / "run_metadata.json"
        else:
            config_parameters, config_source = self._load_config_parameters()

        stats["config_parameters"] = config_parameters
        if config_source:
            stats["config_source"] = str(config_source)

        # Analyze damage analysis results
        if (self.output_dir / "damage_analysis").exists():
            damage_analysis = self._analyze_damage_results()
            stats["damage_analysis"] = damage_analysis
            stats["damage_data"] = damage_analysis.copy()
        else:
            empty_damage = {
                "files_analyzed": 0,
                "summary": {},
                "individual_results": [],
            }
            stats["damage_analysis"] = empty_damage.copy()
            stats["damage_data"] = empty_damage

        # Analyze HVS combinations
        if (self.output_dir / "final").exists():
            stats["hvs_combinations"] = self._analyze_hvs_combinations()

        # Collect sample-level statistics
        stats["samples"] = self._collect_sample_statistics()

        # Generate damage-related data if damage plotter is available
        if self.damage_plotter:
            try:
                # Generate comprehensive dashboard data
                stats["dashboard_data"] = self.damage_plotter.get_dashboard_data(
                    str(self.output_dir)
                )

                # Generate damage data summary
                dashboard_data = stats["dashboard_data"]
                damage_data_summary = stats.get(
                    "damage_data",
                    {"files_analyzed": 0, "summary": {}, "individual_results": []},
                )

                if dashboard_data.get("has_data"):
                    samples = dashboard_data.get("samples", [])
                    damage_data_summary["files_analyzed"] = len(samples)
                    damage_data_summary["summary"].update(
                        dashboard_data.get("summary", {})
                    )
                else:
                    damage_data_summary.setdefault("files_analyzed", 0)
                    damage_data_summary.setdefault("summary", {})

                stats["damage_data"] = damage_data_summary

                # Generate damage plots for embedding in report
                stats["damage_plots"] = (
                    self.damage_plotter.generate_comprehensive_damage_plots()
                )

                # Generate individual sample plots
                stats["individual_sample_plots"] = (
                    self.damage_plotter.generate_individual_sample_plots(
                        str(self.output_dir)
                    )
                )
            except Exception as e:
                logger.warning(f"Error generating damage statistics: {e}")
                stats["damage_data"] = {
                    "files_analyzed": 0,
                    "summary": {},
                    "individual_results": [],
                }
                stats["damage_plots"] = {}
                stats["individual_sample_plots"] = {}
        else:
            stats.setdefault(
                "damage_data",
                {"files_analyzed": 0, "summary": {}, "individual_results": []},
            )
            stats["damage_plots"] = {}
            stats["individual_sample_plots"] = {}

        # Ensure damage data entries exist for downstream rendering
        stats.setdefault(
            "damage_data",
            {"files_analyzed": 0, "summary": {}, "individual_results": []},
        )

        return stats

    def _analyze_directory(self, dir_path: Path) -> Dict[str, Any]:
        """
        Analyze contents of a directory.

        Args:
            dir_path: Path to directory to analyze

        Returns:
            Dictionary with directory analysis results
        """
        if not dir_path.exists():
            return {"exists": False}

        files = list(dir_path.glob("*"))
        file_types = {}
        total_size = 0

        for file_path in files:
            if file_path.is_file():
                suffix = file_path.suffix.lower()
                file_types[suffix] = file_types.get(suffix, 0) + 1
                total_size += file_path.stat().st_size

        return {
            "exists": True,
            "file_count": len([f for f in files if f.is_file()]),
            "file_types": file_types,
            "total_size_mb": round(total_size / 1024 / 1024, 2),
            "files": [f.name for f in files if f.is_file()][:20],  # Limit for display
        }

    def _analyze_damage_results(self) -> Dict[str, Any]:
        """
        Analyze aDNA damage analysis results.

        Returns:
            Dictionary with damage analysis summary
        """
        damage_dir = self.output_dir / "damage_analysis"
        json_files = list(damage_dir.glob("*.json"))

        if not json_files:
            return {
                "files_analyzed": 0,
                "summary": {},
                "individual_results": [],
            }

        damage_data: List[Dict[str, Any]] = []
        for json_file in json_files:
            try:
                with open(json_file, "r") as f:
                    data = json.load(f)
                    damage_patterns = data.get("damage_patterns", {})

                    # Extract key metrics
                    sample_name = json_file.stem.replace("_damage_results", "")
                    damage_data.append(
                        {
                            "sample": sample_name,
                            "damage_5_prime": damage_patterns.get("damage_5_prime", 0),
                            "damage_3_prime": damage_patterns.get("damage_3_prime", 0),
                            "overall_damage_rate": damage_patterns.get(
                                "overall_damage_rate", 0
                            ),
                            "valid_percentage": damage_patterns.get(
                                "sequence_quality", {}
                            ).get("valid_percentage", 0),
                            "n_percentage": damage_patterns.get(
                                "sequence_quality", {}
                            ).get("n_percentage", 0),
                            "n_content": damage_patterns.get("n_content", 0),
                            "valid_bases": damage_patterns.get("valid_bases", 0),
                            "total_bases": damage_patterns.get("total_bases", 0),
                            "ambiguous_content": damage_patterns.get(
                                "ambiguous_content", 0
                            ),
                        }
                    )
            except Exception as e:
                logger.warning(f"Could not parse damage file {json_file}: {e}")

        # Calculate summary statistics
        if damage_data:
            df = pd.DataFrame(damage_data)
            summary = {
                "total_n_bases": float(df["n_content"].sum()),
                "average_n_percentage": float(df["n_percentage"].mean()),
                "median_n_percentage": float(df["n_percentage"].median()),
                "max_n_percentage": float(df["n_percentage"].max()),
                "total_valid_bases": float(df["valid_bases"].sum()),
                "average_valid_percentage": float(df["valid_percentage"].mean()),
                "mean_overall_damage": float(df["overall_damage_rate"].mean()),
            }
        else:
            summary = {}

        return {
            "files_analyzed": len(json_files),
            "summary": summary,
            "individual_results": damage_data[:50],
        }

    def _analyze_hvs_combinations(self) -> Dict[str, Any]:
        """
        Analyze HVS region combinations in final merged files.

        Returns:
            Dictionary with HVS combination analysis
        """
        final_dir = self.output_dir / "final"
        final_files = list(final_dir.glob("*.fasta"))

        combinations = {}
        for file_path in final_files:
            # Extract HVS combination from filename
            name = file_path.stem
            if "_merged" in name:
                # Extract HVS regions from filename
                hvs_regions = []
                if "HVS1" in name:
                    hvs_regions.append("HVS1")
                if "HVS2" in name:
                    hvs_regions.append("HVS2")
                if "HVS3" in name:
                    hvs_regions.append("HVS3")

                combo_key = "_".join(sorted(hvs_regions)) if hvs_regions else "Unknown"
                combinations[combo_key] = combinations.get(combo_key, 0) + 1

        return {
            "total_merged_files": len(final_files),
            "combinations": combinations,
            "files": [f.name for f in final_files],
        }

    def _collect_sample_statistics(self) -> Dict[str, Any]:
        """
        Collect per-sample processing statistics.

        Returns:
            Dictionary with sample-level statistics
        """
        samples = {}

        # Get all samples from consensus directory
        consensus_dir = self.output_dir / "consensus"
        if consensus_dir.exists():
            for consensus_file in consensus_dir.glob("*_consensus.fasta"):
                try:
                    sample_base = consensus_file.stem.replace("_consensus", "")
                    # Remove HVS region suffix if present
                    for hvs in ["_HVS1", "_HVS2", "_HVS3"]:
                        if sample_base.endswith(hvs):
                            sample_base = sample_base[: -len(hvs)]
                            break

                    if sample_base not in samples:
                        samples[sample_base] = {
                            "consensus_files": [],
                            "final_files": [],
                            "damage_files": [],
                            "hvs_regions": set(),
                        }

                    samples[sample_base]["consensus_files"].append(consensus_file.name)

                    # Determine HVS region
                    for hvs in ["HVS1", "HVS2", "HVS3"]:
                        if hvs in consensus_file.name:
                            samples[sample_base]["hvs_regions"].add(hvs)
                            break

                except Exception as e:
                    logger.warning(
                        f"Error processing consensus file {consensus_file}: {e}"
                    )

        # Check for final merged files
        final_dir = self.output_dir / "final"
        if final_dir.exists():
            for final_file in final_dir.glob("*.fasta"):
                # Extract base sample name
                sample_base = final_file.stem.split("_HVS")[0].replace("_merged", "")
                if sample_base in samples:
                    samples[sample_base]["final_files"].append(final_file.name)

        # Check for damage analysis files
        damage_dir = self.output_dir / "damage_analysis"
        if damage_dir.exists():
            for damage_file in damage_dir.glob("*.json"):
                sample_base = damage_file.stem.split("_HVS")[0].replace(
                    "_damage_results", ""
                )
                if sample_base in samples:
                    samples[sample_base]["damage_files"].append(damage_file.name)

        # Convert sets to lists for JSON serialization
        for sample_data in samples.values():
            sample_data["hvs_regions"] = list(sample_data["hvs_regions"])

        return samples

    def _load_config_parameters(self) -> Tuple[Dict[str, Any], Optional[Path]]:
        """Locate and load pipeline configuration parameters for display."""

        candidate_paths = [
            self.output_dir / "config.yaml",
            self.output_dir / "config.yml",
            self.output_dir / "pipeline_config.yaml",
            self.output_dir / "pipeline_config.yml",
        ]

        output_config_dir = self.output_dir / "config"
        if output_config_dir.exists():
            candidate_paths.extend(
                output_config_dir / name
                for name in [
                    "config.yaml",
                    "config.yml",
                    "pipeline_config.yaml",
                    "pipeline_config.yml",
                    "default_config.yaml",
                ]
            )

        for candidate in candidate_paths:
            data = self._try_read_yaml(candidate)
            if data is not None:
                return data, candidate

        # Fallback to repository default configuration
        try:
            repo_config_path = (
                Path(__file__).resolve().parents[4] / "config" / "default_config.yaml"
            )
        except IndexError:
            repo_config_path = None

        if repo_config_path and repo_config_path.exists():
            data = self._try_read_yaml(repo_config_path)
            if data is not None:
                return data, repo_config_path

        return {}, None

    def _try_read_yaml(self, path: Path) -> Optional[Dict[str, Any]]:
        """Attempt to load YAML content from the provided path."""

        try:
            with open(path, "r", encoding="utf-8") as handle:
                loaded = yaml.safe_load(handle)
            if isinstance(loaded, dict):
                return loaded
        except FileNotFoundError:
            return None
        except Exception as exc:
            logger.warning(f"Could not load configuration from {path}: {exc}")
        return None

    def _try_read_json(self, path: Path) -> Optional[Dict[str, Any]]:
        """Attempt to load JSON content from the provided path."""

        try:
            with open(path, "r", encoding="utf-8") as handle:
                loaded = json.load(handle)
            if isinstance(loaded, dict):
                return loaded
        except FileNotFoundError:
            return None
        except Exception as exc:
            logger.warning(f"Could not load JSON metadata from {path}: {exc}")
        return None
