import argparse

class Config:
    def __init__(self, config, args : argparse.Namespace):
        self.engine_path         = config['engine_path']
        self.fastchess_path      = config['fastchess_path']
        self.iterations          = config['iterations']
        self.matches             = config['matches']
        self.concurrency         = config['concurrency']
        self.openings_path       = config['openings_path']
        self.save_path           = config['save_path']
        self.plot_name           = config['plot_name']
        self.nodes               = config['nodes']
        self.depth               = config['depth']
        self.time                = config['time']
        self.increment           = config['increment']
        self.movetime            = config['movetime']
        self.pgn_path            = config['pgn_path']
        self.tb_path             = config['tb_path']
        self.draw_adjudication   = config['draw_adjudication']
        self.resign_adjudication = config['resign_adjudication']

        self.verbose = args.verbose
        self.load_path = args.load
