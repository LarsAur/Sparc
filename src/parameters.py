from typing import List, Tuple

class TunableParameter:
    def __init__(self, name, default, min_val, max_val, c_k, r_k):
        self.name : str = name
        self.default : float = default
        self.min_val : float = min_val
        self.max_val : float = max_val
        self.c_k : float = c_k
        self.r_k : float = r_k
        self.current_value : float = default
        self.c : float = -1
        self.a : float = -1

class FixedParameter:
    def __init__(self, name, value):
        self.name : str = name
        self.value : str = value

# class ParameterParser:
#     def _parse_line(line, tunable_parameters : List[TunableParameter], fixed_parameters: List[FixedParameter]) -> None:
#         parts = line.strip().split(',')
#         parts = [part.strip() for part in parts]

#         print(f"Parsing line: {line.strip()} with parts: {parts}, length: {len(parts)}")

#         if len(parts) == 6:
#             param_name, default_value, min_val, max_val, c_k, r_k = parts
#             tunable_parameters.append(TunableParameter(
#                 name=param_name,
#                 default=float(default_value),
#                 min_val=float(min_val),
#                 max_val=float(max_val),
#                 c_k=float(c_k),
#                 r_k=float(r_k)
#             ))
#             print(f"Loaded parameter: {param_name} with default={default_value}, min={min_val}, max={max_val}, c_k={c_k}, r_k={r_k}")
#         elif len(parts) == 2:
#             param_name, value = parts
#             fixed_parameters.append(FixedParameter(
#                 name=param_name,
#                 value=value
#             ))
#             print(f"Loaded fixed parameter: {param_name} with value={value}")
#         else:
#             raise ValueError(f"Invalid line in config file: {line}")

#     # Line is parsed as CSV with the columns: parameter_name, default_value, min, max, c_k, r_k
#     # Where c_k and r_k are the final values of the pertubation and relative apply factor
#     # Lines starting with # are consdered as comments and are ignored
#     # The Line can also be parsed as a fixed parameter with the columns: parameter_name, value
#     def get_parameters_from_file(parameter_path) -> Tuple[List[TunableParameter], List[FixedParameter]]:
#         print(f"Parsing config file: {parameter_path}")

#         tunable_parameters : List[TunableParameter] = []
#         fixed_parameters : List[FixedParameter] = []

#         with open(parameter_path, 'r') as f:
#             for line in f:
#                 if line.strip() and not line.startswith('#'):
#                     ParameterParser._parse_line(line, tunable_parameters, fixed_parameters)

#         return tunable_parameters, fixed_parameters


