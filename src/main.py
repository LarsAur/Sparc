import argparse
import json
from pathlib import Path
from typing import List
from config import Config
from parameters import FixedParameter, TunableParameter
from tuning_manager import TuningManager
import cProfile

def main():
    parser = argparse.ArgumentParser(description="Sparc Chess Engine Tuner")
    parser.add_argument("config_path",   type=str, help="Path to the file containing tunable and fixed parameters")
    parser.add_argument("-l", "--load", type=str, help="Path to load the SPSA state from")
    parser.add_argument("--verbose", action="store_true", help="Increase output verbosity")

    args = parser.parse_args()

    with open(args.config_path, 'r') as f:
        all_configs = json.load(f)

    # Parse configurations from the JSON file and validate them
    configs = Config(all_configs["configs"], args)

    if (configs.nodes == 0) and (configs.movetime == 0) and (configs.time == 0) and (configs.depth == 0):
        parser.error("At least one of nodes, movetime, time, or depth must be set")

    if configs.concurrency > 2 * configs.matches:
        parser.error("Number of concurrent games cannot exceed the number of games per iteration")

    if (configs.openings_path != "") and (not configs.openings_path.endswith('.pgn') and (not configs.openings_path.endswith('.epd'))):
        parser.error("Opening book is expected to end with .pgn or .epd")

    if (configs.openings_path != "") and (not Path(configs.openings_path).is_file()):
        parser.error("Opening book path does not exist: " + configs.openings_path)

    if not Path(configs.engine_path).is_file():
        parser.error("Engine path does not exist: " + configs.engine_path)

    if not Path(configs.fastchess_path).is_file():
        parser.error("Fastchess path does not exist: " + configs.fastchess_path)

    if (configs.load_path is not None) and (not Path(configs.load_path).is_file()):
        parser.error("Load path does not exist: " + configs.load_path)

    # Parse fixed parameters
    fixed_parameters : List[FixedParameter] = []
    for param in all_configs["fixed_params"]:
        if "name" not in param or "value" not in param:
            parser.error("Each fixed parameter must have a name and a value: " + str(param))
        fixed_parameters.append(FixedParameter(param["name"], param["value"]))

    # Parse tunable parameters
    tunable_parameters : List[TunableParameter] = []
    for param in all_configs["tuning_params"]:
        if "name" not in param or "default" not in param or "min" not in param or "max" not in param or "ck" not in param or "ak" not in param:
            parser.error("Each tunable parameter must have a name, default value, min value, max value, ck and ak: " + str(param))
        tunable_parameters.append(TunableParameter(
            name=param["name"],
            default=float(param["default"]),
            min_val=float(param["min"]),
            max_val=float(param["max"]),
            c_k=float(param["ck"]),
            r_k=float(param["ak"])
        ))

    tuning_manager = TuningManager(configs, fixed_parameters, tunable_parameters)
    tuning_manager.run()

if __name__ == "__main__":
    main()