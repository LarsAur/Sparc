import random
from parameters import TunableParameter, FixedParameter
from typing import List
from pathlib import Path

class Spsa:

    GAMMA = 0.101
    ALPHA = 0.602
    A_FACTOR = 1.1

    def __init__ (self, parameters: List[TunableParameter], iterations: int):
        self.parameters : List[TunableParameter] = parameters.copy()
        self.perturbations : List[int] = [0] * len(parameters)
        self.iteration = 1
        self.target_iterations = iterations

        # Calculate the a and c values for each parameter
        # based on the end values for c_k and r_k and the number of iterations
        for param in self.parameters:
            a_end = param.c_k * param.c_k * param.r_k
            param.c = param.c_k * pow(self.target_iterations, Spsa.GAMMA)
            param.a = a_end * pow(self.target_iterations * Spsa.A_FACTOR, Spsa.ALPHA)

    def _clamp(value, min_val, max_val):
        return max(min_val, min(max_val, value))

    def generate_perturbation(self):
        for i in range(len(self.perturbations)):
            self.perturbations[i] = random.choice([-1, 1])

    def get_perturbed_parameters(self, sign) -> List[FixedParameter]:
        perturbated_parameters : List[FixedParameter] = []

        # Calculate the perturbated value and clip it to the min and max values
        for i, param in enumerate(self.parameters):
            c_i = param.c / pow(self.iteration, Spsa.GAMMA)
            value = param.current_value + sign * c_i * self.perturbations[i]
            value = Spsa._clamp(value, param.min_val, param.max_val)
            perturbated_parameters.append(FixedParameter(
                name=param.name,
                value=value
            ))
        return perturbated_parameters

    def update(self, score):
        for i, param in enumerate(self.parameters):
            a_i = param.a / pow(self.iteration * Spsa.A_FACTOR, Spsa.ALPHA)
            c_i = param.c / pow(self.iteration, Spsa.GAMMA)

            param0 = Spsa._clamp(param.current_value + c_i * self.perturbations[i], param.min_val, param.max_val)
            param1 = Spsa._clamp(param.current_value - c_i * self.perturbations[i], param.min_val, param.max_val)
            clamped_perturbation = param0 - param1

            g_i = a_i * score / clamped_perturbation

            self.parameters[i].current_value += g_i

            # Clamp the value to the min and max values
            self.parameters[i].current_value = Spsa._clamp(
                self.parameters[i].current_value,
                self.parameters[i].min_val,
                self.parameters[i].max_val
            )

        self.iteration += 1

    def print_state(self):
        print(f"Iteration: {self.iteration}")

        pos_params = self.get_perturbed_parameters(1)
        neg_params = self.get_perturbed_parameters(-1)

        print("Parameter, Current Value, (Perturbation0, Perturbation1)")
        for i, param in enumerate(self.parameters):
            print(f"{param.name}: {param.current_value:.2f}, ({int(round(pos_params[i].value))}, {int(round(neg_params[i].value))})")

    def get_parameters(self) -> List[TunableParameter]:
        return self.parameters