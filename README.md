# Sparc - Simultaneous Perturbation Stochastic Approximation for Arcanum

Sparc is a parameter tuner for chess engines using the [SPSA][spsa-wikipedia] algorithm. While it was created with the intention to tune the [Arcanum][Arcanum-github] chess engine, there is nothing prohibiting it from tuning other engines as well.

## Requirements
* Python
    * Matplotlib
* [Fastchess][Fastchess-github]

The required python libraries can be installed using
```
pip install -r requirements.txt
```
Sparc also requires the engine to support setting the parameters throught `setoption` UCI command. Note that floating point options will always be rounded to an int when the option is passed to the engine.

## Arguments
Sparc takes the following arguments
```
python ./src/main.py config_path [-l LOAD] [--verbose]
```
The `config_path` is the path to a .json file containing all the configurations for the tuner. A template containing all the fields are available in [sparc_config.json](sparc_config.json). The configuration is divided into three tables: configs, fixed_params and tuning_params.

The `LOAD` argument is path to a .json file containing the state of a previous run. Providing this argument will resume the tuning run.

### Configs:

|Name             |Description   |
|-----------------|--------------|
|engine_path      |Path to the chess engine executable|
|fastchess_path   |Path to the fastchess executable|
|iterations       |Number of SPSA iterations|
|matches          |Number of matches per iteration. A match consists of two games with the same opening where the colors are swapped|
|concurrency      |Number of games to play concurrently|
|openings_path    |Path to an .epd or .pgn file to use for openings. The openings will be selected randomly.              |
|save_path        |Path to a .json file to store the state of the run. Can be used to resume the run at a later point using the `[-l LOAD]` argument|
|plot_name        |Name prefix of the plot files. No plots are generated if left as an empty string.|
|nodes            |Number of nodes to search in each position. Not used if left as 0.|
|depth            |Number of plies to search each position. Not used if left as 0.|
|movetime         |Number of seconds to search each position. Not used if left as 0. Supports floating numbers.|
|time             |Number of seconds to play each game. Not used if left as 0. Supports floating numbers.|
|increment        |Nunber of seconds to increment per move. Not used if left as 0. Supports floating numbers.|
|pgn_path         |Path to the output PGN file. No PGN file is created if left as an empty string.|
|tb_path          |Path to a Syzygy tablebase, used to adjudicate games.|

### Tunable parameters

Tunable parameters are given as a list of objects with name, default, value, min, max, ck and ak.

The `name` has is the name of the uci option and `default` is used as the initial value when tuning.

Inspired by [Zamar's spsa tuner][SPSA-zamar]: `ck` is the perturbation used in the last iteration of the tuning process. This should be a value still expected to cause some performance difference. `rk` is the relative apply factor for the last iteration used to update the current value of the parameter.

The `ck` and `rk` relates to the `a` and `c` parameters in SPSA as follows:
```
a = ck * ck * rk * pow(iterations * 1.1, alpha)
c = ck * pow(iterations, gamma)
```
Where gamma = 0.101 and alpha = 0.602.

### Fixed parameters

Fixed parameters are given as a list of objects with a name and value. These are passed directly to the engine.

[SPSA-wikipedia]: https://en.wikipedia.org/wiki/Simultaneous_perturbation_stochastic_approximation
[Arcanum-github]: https://github.com/LarsAur/Arcanum
[Fastchess-github]: https://github.com/Disservin/fastchess
[SPSA-zamar]: https://github.com/zamar/spsa