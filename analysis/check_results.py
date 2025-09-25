import os
import re
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple, Set, Dict, Optional
import pandas as pd


@dataclass
class ExperimentConfig:
    """Configuration for a single experiment run."""

    model: str
    task: str
    pace_type: str
    study_condition: str
    profile_source: str
    user_idx: int
    gt_coordinates: bool = False

    def __str__(self) -> str:
        gt_suffix = "_gt_coords" if self.gt_coordinates else ""
        return f"{self.model}{gt_suffix}/{self.task}/{self.pace_type}/{self.study_condition}/{self.profile_source}/u{self.user_idx}"

    def get_file_ids(self) -> str:
        """Get the file_ids parameter for this experiment."""
        if self.task == "al":
            return (
                "al_0_0 al_1_0 al_2_0 al_3_0 al_4_0 al_5_0 al_6_0 al_7_0 al_8_0 al_9_0"
            )
        return self.task

    def get_command(self) -> str:
        """Generate the command to run this experiment."""
        # Determine model type based on model name
        if self.model.startswith("gpt"):
            model_type = "gpt"
        elif self.model.startswith("claude"):
            model_type = "anthropic"
        else:
            model_type = "hf"

        cmd = (
            f"python3 main.py --model_type {model_type} --model_name {self.model} "
            f"--download_dir /local/data/mt/vllm_cache --task {self.pace_type} "
            f"--file_ids {self.get_file_ids()} --study_condition {self.study_condition} "
            f"--user_idx {self.user_idx}"
        )

        if self.profile_source == "image":
            cmd += " --profile_source image"

        if self.gt_coordinates:
            cmd += " --gt_coordinates"

        return f'"{cmd}"'


class ExperimentChecker:
    """Handles checking for completed experiments and generating missing ones."""

    def __init__(self, results_dir: str = "/local/data/mt/FormGym/results"):
        self.results_dir = Path(results_dir)
        self.models = ["aria", "molmo", "llava", "gpt-5", "claude-sonnet-4-20250514"]
        self.tasks = ["al", "form-nlu", "funsd", "xfund"]
        self.study_conditions = ["ours", "baseline"]
        self.pace_types = ["oneshot", "iterative"]
        self.profile_sources = ["text", "image"]

    def _get_task_config(self, task: str) -> Tuple[List[str], List[int]]:
        """Get profile sources and user indices for a given task."""
        if task in [
            "al",
        ]:
            return ["text", "image"], [0, 1, 2, 3]
        else:
            return ["text"], [0]

    def _has_results(self, config: ExperimentConfig) -> bool:
        """Check if results exist for the given experiment configuration."""
        user_dir = (
            self.results_dir
            / config.model
            / config.task
            / config.pace_type
            / config.study_condition
            / config.profile_source
            / f"u{config.user_idx}"
        )

        if not user_dir.exists():
            return False

        # Look for any results.md file in any date/time subdirectory
        for date_dir in user_dir.iterdir():
            if date_dir.is_dir():
                for time_dir in date_dir.iterdir():
                    if time_dir.is_dir():
                        results_file = time_dir / "results.md"
                        if results_file.exists():
                            # For AL tasks, check if all 10 files are present
                            if config.task in ["al"]:
                                if self._has_all_al_files(results_file):
                                    return True
                            else:
                                return True
        return False

    def _has_all_al_files(self, results_file: Path) -> bool:
        """Check if the results.md file contains all 10 AL files."""
        try:
            with open(results_file, "r") as f:
                content = f.read()

            # Check for all 10 AL files (al_0_0 through al_9_0)
            al_files = {f"al_{i}_0" for i in range(10)}
            found_files = set()

            # Look for AL files in the content
            for al_file in al_files:
                if al_file in content:
                    found_files.add(al_file)

            # Return True if all 10 files are found
            return len(found_files) == 10

        except Exception:
            return False

    def generate_all_configs(self) -> List[ExperimentConfig]:
        """Generate all possible experiment configurations."""
        configs = []

        for model in self.models:
            for task in self.tasks:
                for pace_type in self.pace_types:
                    for study_condition in self.study_conditions:
                        profile_sources, user_indices = self._get_task_config(task)

                        for profile_source in profile_sources:
                            # Skip iterative for certain tasks (only Auto Loans should have iterative)
                            if task == "xfund" and pace_type == "iterative":
                                continue
                            if task == "form-nlu" and pace_type == "iterative":
                                continue
                            if task == "funsd" and pace_type == "iterative":
                                continue

                            # Skip molmo+image combinations
                            if model == "molmo" and profile_source == "image":
                                continue

                            for user_idx in user_indices:
                                configs.append(
                                    ExperimentConfig(
                                        model=model,
                                        task=task,
                                        pace_type=pace_type,
                                        study_condition=study_condition,
                                        profile_source=profile_source,
                                        user_idx=user_idx,
                                    )
                                )
        return configs

    def check_results_completion(
        self,
    ) -> Tuple[List[ExperimentConfig], List[ExperimentConfig]]:
        """Check which experiments are completed and which are missing."""
        all_configs = self.generate_all_configs()
        completed = []
        missing = []

        for config in all_configs:
            if self._has_results(config):
                completed.append(config)
            else:
                missing.append(config)

        # Also check for Claude gt_coordinates experiments (baseline only)
        claude_gt_configs = self._generate_claude_gt_coords_configs()
        for config in claude_gt_configs:
            if self._has_results_gt_coords(
                config.model,
                config.task,
                config.pace_type,
                config.study_condition,
                config.profile_source,
                config.user_idx,
            ):
                completed.append(config)
            else:
                missing.append(config)

        return completed, missing

    def _generate_claude_gt_coords_configs(self) -> List[ExperimentConfig]:
        """Generate Claude gt_coordinates experiment configurations (baseline only)."""
        configs = []
        claude_model = "claude-sonnet-4-20250514"

        for task in self.tasks:
            for pace_type in self.pace_types:
                # Only baseline study condition for gt_coordinates
                study_condition = "baseline"
                profile_sources, user_indices = self._get_task_config(task)

                for profile_source in profile_sources:
                    # Skip molmo+image combinations
                    if claude_model == "molmo" and profile_source == "image":
                        continue

                    # Skip iterative for xfund, form-nlu, funsd
                    if (
                        task in ["xfund", "form-nlu", "funsd"]
                        and pace_type == "iterative"
                    ):
                        continue

                    for user_idx in user_indices:
                        configs.append(
                            ExperimentConfig(
                                model=claude_model,
                                task=task,
                                pace_type=pace_type,
                                study_condition=study_condition,
                                profile_source=profile_source,
                                user_idx=user_idx,
                                gt_coordinates=True,
                            )
                        )
        return configs

    def _extract_accuracy_from_results(
        self, config: ExperimentConfig
    ) -> Optional[float]:
        """Extract average field accuracy from a results file."""
        user_dir = (
            self.results_dir
            / config.model
            / config.task
            / config.pace_type
            / config.study_condition
            / config.profile_source
            / f"u{config.user_idx}"
        )

        if not user_dir.exists():
            return None

        # Look for any results.md file in any date/time subdirectory
        for date_dir in user_dir.iterdir():
            if date_dir.is_dir():
                for time_dir in date_dir.iterdir():
                    if time_dir.is_dir():
                        results_file = time_dir / "results.md"
                        if results_file.exists():
                            try:
                                with open(results_file, "r") as f:
                                    content = f.read()

                                # Extract average field accuracy using regex
                                match = re.search(
                                    r"- Average Field Accuracy: ([\d.]+)", content
                                )
                                if match:
                                    return float(match.group(1))
                            except Exception:
                                continue
        return None

    def _extract_placements_from_results(
        self, config: ExperimentConfig
    ) -> Optional[int]:
        """Extract total placements from a results file."""
        user_dir = (
            self.results_dir
            / config.model
            / config.task
            / config.pace_type
            / config.study_condition
            / config.profile_source
            / f"u{config.user_idx}"
        )

        if not user_dir.exists():
            return None

        # Look for any results.md file in any date/time subdirectory
        for date_dir in user_dir.iterdir():
            if date_dir.is_dir():
                for time_dir in date_dir.iterdir():
                    if time_dir.is_dir():
                        results_file = time_dir / "results.md"
                        if results_file.exists():
                            try:
                                with open(results_file, "r") as f:
                                    content = f.read()

                                # Extract total placements using regex
                                match = re.search(
                                    r"- Total Placements: ([\d]+)", content
                                )
                                if match:
                                    return int(match.group(1))
                            except Exception:
                                continue
        return None

    def _extract_al_accuracy_averaged(
        self, model: str, pace_type: str, study_condition: str, profile_source: str
    ) -> Optional[float]:
        """Extract AL accuracy averaged across all 4 users. Returns None if not all users are present."""
        accuracies = []

        for user_idx in [0, 1, 2, 3]:
            config = ExperimentConfig(
                model=model,
                task="al",
                pace_type=pace_type,
                study_condition=study_condition,
                profile_source=profile_source,
                user_idx=user_idx,
            )
            accuracy = self._extract_accuracy_from_results(config)
            if accuracy is None:
                return None  # Missing any user means missing overall
            accuracies.append(accuracy)

        # At this point we know we have exactly 4 non-None accuracies
        return sum(accuracies) / len(accuracies)

    def _extract_al_placements_averaged(
        self, model: str, pace_type: str, study_condition: str, profile_source: str
    ) -> Optional[float]:
        """Extract AL placements averaged across all 4 users. Returns None if not all users are present."""
        placements = []

        for user_idx in [0, 1, 2, 3]:
            config = ExperimentConfig(
                model=model,
                task="al",
                pace_type=pace_type,
                study_condition=study_condition,
                profile_source=profile_source,
                user_idx=user_idx,
            )
            placement = self._extract_placements_from_results(config)
            if placement is None:
                return None  # Missing any user means missing overall
            placements.append(placement)

        # At this point we know we have exactly 4 non-None placements
        return sum(placements) / len(placements)

    def _extract_accuracy_from_results_gt_coords(
        self,
        model: str,
        task: str,
        pace_type: str,
        study_condition: str,
        profile_source: str,
        user_idx: int,
    ) -> Optional[float]:
        """Extract average field accuracy from a results file with gt_coordinates."""
        # Handle gt_coordinates case - model name gets "_gt_coords" suffix in directory
        model_name = f"{model}_gt_coords"

        user_dir = (
            self.results_dir
            / model_name
            / task
            / pace_type
            / study_condition
            / profile_source
            / f"u{user_idx}"
        )

        if not user_dir.exists():
            return None

        # Look for any results.md file in any date/time subdirectory
        for date_dir in user_dir.iterdir():
            if date_dir.is_dir():
                for time_dir in date_dir.iterdir():
                    if time_dir.is_dir():
                        results_file = time_dir / "results.md"
                        if results_file.exists():
                            try:
                                with open(results_file, "r") as f:
                                    content = f.read()

                                # Extract average field accuracy using regex
                                match = re.search(
                                    r"- Average Field Accuracy: ([\d.]+)", content
                                )
                                if match:
                                    return float(match.group(1))
                            except Exception:
                                continue
        return None

    def _extract_placements_from_results_gt_coords(
        self,
        model: str,
        task: str,
        pace_type: str,
        study_condition: str,
        profile_source: str,
        user_idx: int,
    ) -> Optional[int]:
        """Extract total placements from a results file with gt_coordinates."""
        # Handle gt_coordinates case - model name gets "_gt_coords" suffix in directory
        model_name = f"{model}_gt_coords"

        user_dir = (
            self.results_dir
            / model_name
            / task
            / pace_type
            / study_condition
            / profile_source
            / f"u{user_idx}"
        )

        if not user_dir.exists():
            return None

        # Look for any results.md file in any date/time subdirectory
        for date_dir in user_dir.iterdir():
            if date_dir.is_dir():
                for time_dir in date_dir.iterdir():
                    if time_dir.is_dir():
                        results_file = time_dir / "results.md"
                        if results_file.exists():
                            try:
                                with open(results_file, "r") as f:
                                    content = f.read()

                                # Extract total placements using regex
                                match = re.search(
                                    r"- Total Placements: ([\d]+)", content
                                )
                                if match:
                                    return int(match.group(1))
                            except Exception:
                                continue
        return None

    def _extract_al_accuracy_averaged_gt_coords(
        self, model: str, pace_type: str, study_condition: str, profile_source: str
    ) -> Optional[float]:
        """Extract AL accuracy averaged across all 4 users with gt_coordinates. Returns None if not all users are present."""
        accuracies = []

        for user_idx in [0, 1, 2, 3]:
            accuracy = self._extract_accuracy_from_results_gt_coords(
                model, "al", pace_type, study_condition, profile_source, user_idx
            )
            if accuracy is None:
                return None  # Missing any user means missing overall
            accuracies.append(accuracy)

        # At this point we know we have exactly 4 non-None accuracies
        return sum(accuracies) / len(accuracies)

    def _extract_al_placements_averaged_gt_coords(
        self, model: str, pace_type: str, study_condition: str, profile_source: str
    ) -> Optional[float]:
        """Extract AL placements averaged across all 4 users with gt_coordinates. Returns None if not all users are present."""
        placements = []

        for user_idx in [0, 1, 2, 3]:
            placement = self._extract_placements_from_results_gt_coords(
                model, "al", pace_type, study_condition, profile_source, user_idx
            )
            if placement is None:
                return None  # Missing any user means missing overall
            placements.append(placement)

        # At this point we know we have exactly 4 non-None placements
        return sum(placements) / len(placements)

    def _has_results_gt_coords(
        self,
        model: str,
        task: str,
        pace_type: str,
        study_condition: str,
        profile_source: str,
        user_idx: int,
    ) -> bool:
        """Check if results exist for the given experiment configuration with gt_coordinates."""
        # Handle gt_coordinates case - model name gets "_gt_coords" suffix in directory
        model_name = f"{model}_gt_coords"

        user_dir = (
            self.results_dir
            / model_name
            / task
            / pace_type
            / study_condition
            / profile_source
            / f"u{user_idx}"
        )

        if not user_dir.exists():
            return False

        # Look for any results.md file in any date/time subdirectory
        for date_dir in user_dir.iterdir():
            if date_dir.is_dir():
                for time_dir in date_dir.iterdir():
                    if time_dir.is_dir():
                        results_file = time_dir / "results.md"
                        if results_file.exists():
                            # For AL tasks, check if all 10 files are present
                            if task in ["al"]:
                                if self._has_all_al_files(results_file):
                                    return True
                            else:
                                return True
        return False

    def _get_model_display_name(self, model: str) -> str:
        """Convert model name to display name for CSV."""
        if model == "aria":
            return "Aria 25B"
        elif model == "claude-sonnet-4-20250514":
            return "Claude 4"
        elif model == "gpt-5":
            return "GPT-5"
        elif model == "llava":
            return "Llava 7B"
        elif model == "molmo":
            return "Molmo 7B"
        else:
            return model

    def _get_model_display_name_with_fl(self, model: str) -> str:
        """Convert model name to display name with FL suffix for CSV."""
        base_name = self._get_model_display_name(model)
        return f"{base_name} + FF (ours)"

    def _should_exist(
        self,
        model: str,
        task: str,
        pace_type: str,
        study_condition: str,
        profile_source: str,
    ) -> bool:
        """Check if a combination should exist based on the checking logic."""
        # Skip molmo+image combinations
        if model == "molmo" and profile_source == "image":
            return False

        # Skip iterative for xfund, form-nlu, funsd
        if task in ["xfund", "form-nlu", "funsd"] and pace_type == "iterative":
            return False

        return True

    def generate_accuracy_csv(self, completed: List[ExperimentConfig]) -> str:
        """Generate CSV string with accuracy extraction data using pandas DataFrame."""
        # Initialize data structure
        models = ["aria", "claude-sonnet-4-20250514", "gpt-5", "llava", "molmo"]
        tasks = ["al", "form-nlu", "funsd", "xfund"]

        # Create a dictionary to store accuracy and placements data
        accuracy_data = {}
        placements_data = {}

        # Initialize all combinations
        for model in models:
            accuracy_data[model] = {}
            placements_data[model] = {}
            for task in tasks:
                accuracy_data[model][task] = {
                    "oneshot_baseline_text": None,
                    "oneshot_baseline_image": None,
                    "oneshot_ours_text": None,
                    "oneshot_ours_image": None,
                    "iterative_baseline_text": None,
                    "iterative_baseline_image": None,
                    "iterative_ours_text": None,
                    "iterative_ours_image": None,
                }
                placements_data[model][task] = {
                    "oneshot_baseline_text": None,
                    "oneshot_baseline_image": None,
                    "oneshot_ours_text": None,
                    "oneshot_ours_image": None,
                    "iterative_baseline_text": None,
                    "iterative_baseline_image": None,
                    "iterative_ours_text": None,
                    "iterative_ours_image": None,
                }

        # Extract accuracy and placements data from completed experiments
        # First, handle AL tasks with averaging across users
        for model in models:
            for pace_type in ["oneshot", "iterative"]:
                for study_condition in ["baseline", "ours"]:
                    for profile_source in ["text", "image"]:
                        # Handle AL task
                        if self._should_exist(
                            model, "al", pace_type, study_condition, profile_source
                        ):
                            accuracy = self._extract_al_accuracy_averaged(
                                model, pace_type, study_condition, profile_source
                            )
                            placements = self._extract_al_placements_averaged(
                                model, pace_type, study_condition, profile_source
                            )
                            if accuracy is not None:
                                key = f"{pace_type}_{study_condition}_{profile_source}"
                                accuracy_data[model]["al"][key] = accuracy
                            if placements is not None:
                                key = f"{pace_type}_{study_condition}_{profile_source}"
                                placements_data[model]["al"][key] = placements

        # Then handle other tasks (single user)
        for config in completed:
            if config.task not in ["al"]:
                accuracy = self._extract_accuracy_from_results(config)
                placements = self._extract_placements_from_results(config)
                if accuracy is not None:
                    key = f"{config.pace_type}_{config.study_condition}_{config.profile_source}"
                    accuracy_data[config.model][config.task][key] = accuracy
                if placements is not None:
                    key = f"{config.pace_type}_{config.study_condition}_{config.profile_source}"
                    placements_data[config.model][config.task][key] = placements

        # Create DataFrame
        data = []

        # Add baseline models
        for model in models:
            row = {
                "Model": self._get_model_display_name(model),
                "Auto Loans (Text) - One Shot": self._format_accuracy(
                    accuracy_data[model]["al"]["oneshot_baseline_text"],
                    model,
                    "al",
                    "oneshot",
                    "baseline",
                    "text",
                ),
                "Auto Loans (Text) - Iterative": self._format_accuracy(
                    accuracy_data[model]["al"]["iterative_baseline_text"],
                    model,
                    "al",
                    "iterative",
                    "baseline",
                    "text",
                ),
                "Auto Loans (Doc Transfer) - One Shot": self._format_accuracy(
                    accuracy_data[model]["al"]["oneshot_baseline_image"],
                    model,
                    "al",
                    "oneshot",
                    "baseline",
                    "image",
                ),
                "Auto Loans (Doc Transfer) - Iterative": self._format_accuracy(
                    accuracy_data[model]["al"]["iterative_baseline_image"],
                    model,
                    "al",
                    "iterative",
                    "baseline",
                    "image",
                ),
                "FUNSD - One Shot": self._format_accuracy(
                    accuracy_data[model]["funsd"]["oneshot_baseline_text"],
                    model,
                    "funsd",
                    "oneshot",
                    "baseline",
                    "text",
                ),
                "XFUND - One Shot": self._format_accuracy(
                    accuracy_data[model]["xfund"]["oneshot_baseline_text"],
                    model,
                    "xfund",
                    "oneshot",
                    "baseline",
                    "text",
                ),
                "Form-NLU - One Shot": self._format_accuracy(
                    accuracy_data[model]["form-nlu"]["oneshot_baseline_text"],
                    model,
                    "form-nlu",
                    "oneshot",
                    "baseline",
                    "text",
                ),
                # Total Placements columns
                "Auto Loans (Text) - One Shot (Placements)": self._format_placements(
                    placements_data[model]["al"]["oneshot_baseline_text"],
                    model,
                    "al",
                    "oneshot",
                    "baseline",
                    "text",
                ),
                "Auto Loans (Text) - Iterative (Placements)": self._format_placements(
                    placements_data[model]["al"]["iterative_baseline_text"],
                    model,
                    "al",
                    "iterative",
                    "baseline",
                    "text",
                ),
                "Auto Loans (Doc Transfer) - One Shot (Placements)": self._format_placements(
                    placements_data[model]["al"]["oneshot_baseline_image"],
                    model,
                    "al",
                    "oneshot",
                    "baseline",
                    "image",
                ),
                "Auto Loans (Doc Transfer) - Iterative (Placements)": self._format_placements(
                    placements_data[model]["al"]["iterative_baseline_image"],
                    model,
                    "al",
                    "iterative",
                    "baseline",
                    "image",
                ),
                "FUNSD - One Shot (Placements)": self._format_placements(
                    placements_data[model]["funsd"]["oneshot_baseline_text"],
                    model,
                    "funsd",
                    "oneshot",
                    "baseline",
                    "text",
                ),
                "XFUND - One Shot (Placements)": self._format_placements(
                    placements_data[model]["xfund"]["oneshot_baseline_text"],
                    model,
                    "xfund",
                    "oneshot",
                    "baseline",
                    "text",
                ),
                "Form-NLU - One Shot (Placements)": self._format_placements(
                    placements_data[model]["form-nlu"]["oneshot_baseline_text"],
                    model,
                    "form-nlu",
                    "oneshot",
                    "baseline",
                    "text",
                ),
            }
            data.append(row)

        # Add FL (ours) models
        for model in models:
            row = {
                "Model": self._get_model_display_name_with_fl(model),
                "Auto Loans (Text) - One Shot": self._format_accuracy(
                    accuracy_data[model]["al"]["oneshot_ours_text"],
                    model,
                    "al",
                    "oneshot",
                    "ours",
                    "text",
                ),
                "Auto Loans (Text) - Iterative": self._format_accuracy(
                    accuracy_data[model]["al"]["iterative_ours_text"],
                    model,
                    "al",
                    "iterative",
                    "ours",
                    "text",
                ),
                "Auto Loans (Doc Transfer) - One Shot": self._format_accuracy(
                    accuracy_data[model]["al"]["oneshot_ours_image"],
                    model,
                    "al",
                    "oneshot",
                    "ours",
                    "image",
                ),
                "Auto Loans (Doc Transfer) - Iterative": self._format_accuracy(
                    accuracy_data[model]["al"]["iterative_ours_image"],
                    model,
                    "al",
                    "iterative",
                    "ours",
                    "image",
                ),
                "FUNSD - One Shot": self._format_accuracy(
                    accuracy_data[model]["funsd"]["oneshot_ours_text"],
                    model,
                    "funsd",
                    "oneshot",
                    "ours",
                    "text",
                ),
                "XFUND - One Shot": self._format_accuracy(
                    accuracy_data[model]["xfund"]["oneshot_ours_text"],
                    model,
                    "xfund",
                    "oneshot",
                    "ours",
                    "text",
                ),
                "Form-NLU - One Shot": self._format_accuracy(
                    accuracy_data[model]["form-nlu"]["oneshot_ours_text"],
                    model,
                    "form-nlu",
                    "oneshot",
                    "ours",
                    "text",
                ),
                # Total Placements columns
                "Auto Loans (Text) - One Shot (Placements)": self._format_placements(
                    placements_data[model]["al"]["oneshot_ours_text"],
                    model,
                    "al",
                    "oneshot",
                    "ours",
                    "text",
                ),
                "Auto Loans (Text) - Iterative (Placements)": self._format_placements(
                    placements_data[model]["al"]["iterative_ours_text"],
                    model,
                    "al",
                    "iterative",
                    "ours",
                    "text",
                ),
                "Auto Loans (Doc Transfer) - One Shot (Placements)": self._format_placements(
                    placements_data[model]["al"]["oneshot_ours_image"],
                    model,
                    "al",
                    "oneshot",
                    "ours",
                    "image",
                ),
                "Auto Loans (Doc Transfer) - Iterative (Placements)": self._format_placements(
                    placements_data[model]["al"]["iterative_ours_image"],
                    model,
                    "al",
                    "iterative",
                    "ours",
                    "image",
                ),
                "FUNSD - One Shot (Placements)": self._format_placements(
                    placements_data[model]["funsd"]["oneshot_ours_text"],
                    model,
                    "funsd",
                    "oneshot",
                    "ours",
                    "text",
                ),
                "XFUND - One Shot (Placements)": self._format_placements(
                    placements_data[model]["xfund"]["oneshot_ours_text"],
                    model,
                    "xfund",
                    "oneshot",
                    "ours",
                    "text",
                ),
                "Form-NLU - One Shot (Placements)": self._format_placements(
                    placements_data[model]["form-nlu"]["oneshot_ours_text"],
                    model,
                    "form-nlu",
                    "oneshot",
                    "ours",
                    "text",
                ),
            }
            data.append(row)

        # Add Claude with gt_coordinates (baseline only)
        claude_gt_model = "claude-sonnet-4-20250514"
        claude_gt_row = {
            "Model": "Claude 4 (GT Coords)",
            "Auto Loans (Text) - One Shot": self._format_accuracy(
                self._extract_al_accuracy_averaged_gt_coords(
                    claude_gt_model, "oneshot", "baseline", "text"
                ),
                claude_gt_model,
                "al",
                "oneshot",
                "baseline",
                "text",
            ),
            "Auto Loans (Text) - Iterative": self._format_accuracy(
                self._extract_al_accuracy_averaged_gt_coords(
                    claude_gt_model, "iterative", "baseline", "text"
                ),
                claude_gt_model,
                "al",
                "iterative",
                "baseline",
                "text",
            ),
            "Auto Loans (Doc Transfer) - One Shot": self._format_accuracy(
                self._extract_al_accuracy_averaged_gt_coords(
                    claude_gt_model, "oneshot", "baseline", "image"
                ),
                claude_gt_model,
                "al",
                "oneshot",
                "baseline",
                "image",
            ),
            "Auto Loans (Doc Transfer) - Iterative": self._format_accuracy(
                self._extract_al_accuracy_averaged_gt_coords(
                    claude_gt_model, "iterative", "baseline", "image"
                ),
                claude_gt_model,
                "al",
                "iterative",
                "baseline",
                "image",
            ),
            "FUNSD - One Shot": self._format_accuracy(
                self._extract_accuracy_from_results_gt_coords(
                    claude_gt_model, "funsd", "oneshot", "baseline", "text", 0
                ),
                claude_gt_model,
                "funsd",
                "oneshot",
                "baseline",
                "text",
            ),
            "XFUND - One Shot": self._format_accuracy(
                self._extract_accuracy_from_results_gt_coords(
                    claude_gt_model, "xfund", "oneshot", "baseline", "text", 0
                ),
                claude_gt_model,
                "xfund",
                "oneshot",
                "baseline",
                "text",
            ),
            "Form-NLU - One Shot": self._format_accuracy(
                self._extract_accuracy_from_results_gt_coords(
                    claude_gt_model, "form-nlu", "oneshot", "baseline", "text", 0
                ),
                claude_gt_model,
                "form-nlu",
                "oneshot",
                "baseline",
                "text",
            ),
            # Total Placements columns
            "Auto Loans (Text) - One Shot (Placements)": self._format_placements(
                self._extract_al_placements_averaged_gt_coords(
                    claude_gt_model, "oneshot", "baseline", "text"
                ),
                claude_gt_model,
                "al",
                "oneshot",
                "baseline",
                "text",
            ),
            "Auto Loans (Text) - Iterative (Placements)": self._format_placements(
                self._extract_al_placements_averaged_gt_coords(
                    claude_gt_model, "iterative", "baseline", "text"
                ),
                claude_gt_model,
                "al",
                "iterative",
                "baseline",
                "text",
            ),
            "Auto Loans (Doc Transfer) - One Shot (Placements)": self._format_placements(
                self._extract_al_placements_averaged_gt_coords(
                    claude_gt_model, "oneshot", "baseline", "image"
                ),
                claude_gt_model,
                "al",
                "oneshot",
                "baseline",
                "image",
            ),
            "Auto Loans (Doc Transfer) - Iterative (Placements)": self._format_placements(
                self._extract_al_placements_averaged_gt_coords(
                    claude_gt_model, "iterative", "baseline", "image"
                ),
                claude_gt_model,
                "al",
                "iterative",
                "baseline",
                "image",
            ),
            "FUNSD - One Shot (Placements)": self._format_placements(
                self._extract_placements_from_results_gt_coords(
                    claude_gt_model, "funsd", "oneshot", "baseline", "text", 0
                ),
                claude_gt_model,
                "funsd",
                "oneshot",
                "baseline",
                "text",
            ),
            "XFUND - One Shot (Placements)": self._format_placements(
                self._extract_placements_from_results_gt_coords(
                    claude_gt_model, "xfund", "oneshot", "baseline", "text", 0
                ),
                claude_gt_model,
                "xfund",
                "oneshot",
                "baseline",
                "text",
            ),
            "Form-NLU - One Shot (Placements)": self._format_placements(
                self._extract_placements_from_results_gt_coords(
                    claude_gt_model, "form-nlu", "oneshot", "baseline", "text", 0
                ),
                claude_gt_model,
                "form-nlu",
                "oneshot",
                "baseline",
                "text",
            ),
        }
        data.append(claude_gt_row)

        # Create DataFrame
        df = pd.DataFrame(data)

        # Print as CSV format
        return df.to_csv(index=False, sep=",")

    def _format_accuracy(
        self,
        accuracy: Optional[float],
        model: str,
        task: str,
        pace_type: str,
        study_condition: str,
        profile_source: str,
    ) -> str:
        """Format accuracy value based on whether it should exist and if it's missing."""
        if not self._should_exist(
            model, task, pace_type, study_condition, profile_source
        ):
            return "-"
        elif accuracy is None:
            return "MISSING"
        else:
            return f"{accuracy:.3f}"

    def _format_placements(
        self,
        placements: Optional[float],
        model: str,
        task: str,
        pace_type: str,
        study_condition: str,
        profile_source: str,
    ) -> str:
        """Format placements value based on whether it should exist and if it's missing."""
        if not self._should_exist(
            model, task, pace_type, study_condition, profile_source
        ):
            return "-"
        elif placements is None:
            return "MISSING"
        else:
            return f"{int(placements)}"

    def print_results(
        self, completed: List[ExperimentConfig], missing: List[ExperimentConfig]
    ):
        # """Print the results in a formatted way."""
        # print("=== COMPLETED RESULTS ===")
        # for config in sorted(completed, key=str):
        #     print(f"✓ {config}")

        # print(f"\n=== MISSING RESULTS ===")
        # for config in sorted(missing, key=str):
        #     print(f"✗ {config}")

        print(f"\n=== PYTHON COMMANDS TO GENERATE MISSING RESULTS ===")
        for config in sorted(missing, key=str):
            # print(f"# {config}")
            print(config.get_command())
            print()

        print(f"\n=== SUMMARY ===")
        print(f"Completed: {len(completed)}")
        print(f"Missing: {len(missing)}")
        print(f"Total expected: {len(completed) + len(missing)}")

        # Generate and print CSV
        print(f"\n=== ACCURACY EXTRACTION CSV ===")
        csv_output = self.generate_accuracy_csv(completed)
        print(csv_output)


def main():
    """Main function to check experiment completion status."""
    checker = ExperimentChecker()
    completed, missing = checker.check_results_completion()
    checker.print_results(completed, missing)


if __name__ == "__main__":
    main()
