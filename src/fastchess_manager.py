from parameters import FixedParameter, TunableParameter
from typing import List
from pathlib import Path
from subprocess import Popen, PIPE
import re

class FastChessManager:
    def __init__(self, configs, fixed_parameters : List[FixedParameter], params0 : List[FixedParameter], params1 : List[FixedParameter]):
        self.configs = configs
        self.fixed_parameters = fixed_parameters
        self.params0 = params0
        self.params1 = params1
        self.results = None

    def option_string_from_param(self, param : FixedParameter):
        if isinstance(param.value, float):
            return f"option.{param.name}={int(round(param.value))}"
        else:
            return f"option.{param.name}={param.value}"

    def get_run_command(self):
        engine_name = Path(self.configs.engine_path).name

        cmd = ""
        cmd += f"{self.configs.fastchess_path} "

        # Engine 0
        cmd += f"-engine cmd={self.configs.engine_path} name={engine_name}-0 "
        cmd += " ".join([self.option_string_from_param(param) for param in self.params0]) + " "
        # Engine 1
        cmd += f"-engine cmd={self.configs.engine_path} name={engine_name}-1 "
        cmd += " ".join([self.option_string_from_param(param) for param in self.params1]) + " "

        # Each
        cmd += f"-each "
        cmd += "proto=uci "
        cmd += " ".join([self.option_string_from_param(param) for param in self.fixed_parameters]) + " "

        # Depth
        if self.configs.depth != 0:
            cmd += f"depth={self.configs.depth} "

        # Nodes
        if self.configs.nodes != 0:
            cmd += f"nodes={self.configs.nodes} "

        # Movetime
        if self.configs.movetime != 0:
            cmd += f"movetime={self.configs.movetime} "

        # Time control
        if self.configs.time != 0:
            if self.configs.increment != 0:
                cmd += f"tc={self.configs.time}+{self.configs.increment} "
            else:
                cmd += f"tc={self.configs.time} "

        cmd += f"-rounds {self.configs.matches} "
        cmd += f"-concurrency {self.configs.concurrency} "

        # Opening book
        if self.configs.openings_path:
            # The format is already checked in main.py
            book_format = "pgn" if self.configs.openings_path.endswith('.pgn') else "epd"
            cmd += f"-openings file={self.configs.openings_path} format={book_format} order=random "

        if self.configs.pgn_path:
            cmd += f"-pgnout file={self.configs.pgn_path} notation=san -site Sparc -event Sparc_tuning_{engine_name} "

        if self.configs.draw_adjudication["enabled"]:
            cmd += f"-draw movenumber={self.configs.draw_adjudication['movenumber']} "
            cmd += f"movecount={self.configs.draw_adjudication['movecount']} "
            cmd += f"score={self.configs.draw_adjudication['threshold']} "

        if self.configs.resign_adjudication["enabled"]:
            cmd += f"-resign movecount={self.configs.resign_adjudication['movecount']} "
            cmd += f"score={self.configs.resign_adjudication['threshold']} "
            if(self.configs.resign_adjudication['twosided']):
                cmd += "twosided=true "

        if self.configs.tb_path:
            cmd += f"-tb {self.configs.tb_path} -tbadjudicate BOTH "

        # Disable printing printing of the rating at intervals
        # This makes it easier to parse the output at the end
        cmd += "-ratinginterval 0 "

        # Disable autosaving of the tournament state to avoid cluttering the output directory
        # Saving the state is not that useful since we are usually running very short tournaments
        cmd += "-autosaveinterval 0"

        return cmd

    def run(self):
        cmd = self.get_run_command()

        if self.configs.verbose:
            print(f"Running command: {cmd}")

        fastchess = Popen(cmd.split(), stdout=PIPE, stderr=PIPE)

        while True:
            output = fastchess.stdout.readline().strip().decode('ascii')

            if not output:
                break

            if "does not exist" in output:
                fastchess.terminate()
                raise FileNotFoundError(output)

            if output.startswith("Warning"):
                print(f"{output}")
            elif self.configs.verbose:
                print(f"{output}")

            if output.startswith("Games:"):
                # Find the 2, 3, 4 number in the results output
                # The format is: "Games: X, Wins: X, Losses: X, Draws: X, ..."
                self.results = [int(num) for num in re.findall(f"\d+", output)[1:4]]

        fastchess.wait()

    def get_wld(self):
        return self.results