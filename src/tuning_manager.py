from typing import List
from parameters import FixedParameter, TunableParameter
from spsa import Spsa
from fastchess_manager import FastChessManager
from plotter import Plotter
from history import History

class TuningManager:
    def __init__(self, configs, fixed_parameters : List[FixedParameter], tunable_parameters : List[TunableParameter]):
        self.configs = configs
        self.fixed_parameters = fixed_parameters
        self.tunable_parameters = tunable_parameters
        self.spsa = Spsa(self.tunable_parameters, self.configs.iterations)
        self.history = History()
        self.plotter = Plotter(self.history)

        # Load history
        if self.configs.load_path is not None:
            self.history.load(self.configs.load_path)
            self.spsa.iteration = self.history.get_iteration() + 1
            for param in self.tunable_parameters:
                param.current_value = self.history.get_last_value(param.name)
        else:
            for param in self.tunable_parameters:
                self.history.add_parameter_value_to_history(param.name, param.current_value)

    def run_iteration(self):
        self.spsa.generate_perturbation()
        self.spsa.print_state()

        fsm = FastChessManager(
            self.configs,
            self.fixed_parameters,
            self.spsa.get_perturbed_parameters(1),
            self.spsa.get_perturbed_parameters(-1)
        )
        fsm.run()

        wins, losses, draws = fsm.get_wld()
        print(f"Wins: {wins}, Draws: {draws}, Losses: {losses}")

        score = (wins - losses) / (wins + losses + draws)
        self.spsa.update(score)

        for param in self.spsa.get_parameters():
            self.history.add_parameter_value_to_history(param.name, param.current_value)

        if self.configs.plot_name:
            self.plotter.plot_parameter_history(self.configs.plot_name + "_values.png")
            self.plotter.plot_parameter_change(self.configs.plot_name + "_changes.png")

        if self.configs.save_path:
            self.history.save(self.configs.save_path)

    def run(self):
        for _ in range(self.configs.iterations):
            self.run_iteration()