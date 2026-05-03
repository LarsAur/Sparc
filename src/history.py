import json

class History:
    def __init__(self):
        self.parameter_histories = {}

    def load(self, filename):
        print("Loading history from file:", filename)
        with open(filename, 'r') as f:
            self.parameter_histories = json.load(f)

    def save(self, filename):
        print("Saving history to file:", filename)
        with open(filename, 'w') as f:
            json.dump(self.parameter_histories, f)

    def add_parameter_value_to_history(self, name, value):
        if name not in self.parameter_histories:
            self.parameter_histories[name] = []
        self.parameter_histories[name].append(value)

    def get_parameter_names(self):
        return list(self.parameter_histories.keys())

    def get_parameter_history(self, name):
        return self.parameter_histories[name]

    def get_last_value(self, name):
        if not name in self.parameter_histories.keys():
            raise ValueError(f"No history for parameter {name}")
        return self.parameter_histories[name][-1]

    def get_iteration(self):
        key = list(self.parameter_histories.keys())[0]
        return len(self.parameter_histories[key])