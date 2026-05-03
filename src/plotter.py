from history import History
import matplotlib.pyplot as plt

class Plotter:

    FIGURE_SIZE = (10, 6)
    BBOX_ANCHOR = (0.5, -0.3)
    NCOLS = 4
    MARK_INTERVAL_DIVISOR = 25
    FONT_FAMILY = 'serif'
    LEGEND_LOC = 'lower center'
    COLOR_MAP = 'rainbow'
    AVAILABLE_SYMBOLS = ['o', 's', 'D', '^', 'v', '<', '>', 'p', '*', 'h']

    def __init__(self, history : History):
        self.parameter_plot_configs = {}
        self.histories = history

    def get_color_map(self):
        cmap = plt.get_cmap(self.COLOR_MAP)
        num_colors = len(self.histories.get_parameter_names())
        colors = [cmap(i / num_colors) for i in range(num_colors)]
        return colors

    def get_symbol_map(self):
        num_symbols = len(self.histories.get_parameter_names())
        symbols = [self.AVAILABLE_SYMBOLS[i % len(self.AVAILABLE_SYMBOLS)] for i in range(num_symbols)]
        return symbols

    def get_mark_interval(self, history_length):
        return max(1, history_length // self.MARK_INTERVAL_DIVISOR)

    def plot_parameter_history(self, filename):
        color_index = 0
        colors = self.get_color_map()
        symbols = self.get_symbol_map()

        plt.figure(figsize=self.FIGURE_SIZE)
        for name in self.histories.get_parameter_names():
            history = self.histories.get_parameter_history(name)
            plt.plot(history, label=name, color=colors[color_index], marker=symbols[color_index], markevery=self.get_mark_interval(len(history)))
            color_index += 1

        plt.rcParams.update({
            "font.family": self.FONT_FAMILY,
        })

        plt.xlabel('Iteration')
        plt.ylabel('Parameter Value')
        plt.title('Parameter History')
        plt.figlegend(loc=self.LEGEND_LOC, bbox_to_anchor=self.BBOX_ANCHOR, ncol=self.NCOLS)
        plt.grid()
        plt.savefig(filename, bbox_inches='tight')
        plt.close()

    def plot_parameter_change(self, filename):
        color_index = 0
        colors = self.get_color_map()
        symbols = self.get_symbol_map()

        plt.figure(figsize=self.FIGURE_SIZE)
        for name in self.histories.get_parameter_names():
            history = self.histories.get_parameter_history(name)
            change = [history[i] - history[0] for i in range(0, len(history))]
            plt.plot(change, label=name, color=colors[color_index], marker=symbols[color_index], markevery=self.get_mark_interval(len(change)))
            color_index += 1

        plt.rcParams.update({
            "font.family": self.FONT_FAMILY,
        })

        plt.xlabel('Iteration')
        plt.ylabel('Parameter Change')
        plt.title('Parameter Changes Over Time')
        plt.figlegend(loc=self.LEGEND_LOC, bbox_to_anchor=self.BBOX_ANCHOR, ncol=self.NCOLS)
        plt.grid()
        plt.savefig(filename, bbox_inches='tight')
        plt.close()