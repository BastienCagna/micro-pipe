from micropype.commandline import override_config_with_args, parse_args, run_function_from_commandline
from micropype.config import Config


class DBConfig(Config):
    path: str

class NamedDBConfig(DBConfig):
    name: str = "unknown"

class ExConfig(Config):
    db: NamedDBConfig
    param1: float = 1.0
    step1: bool = False
    step2: bool = False
    step3: bool = False


testing_args = [
    "--param1", "1.2",
    "--step3",
    "--db.path", "/path/to/a/file.txz"
]

def test_parse_args():
    params = parse_args(testing_args)

    assert("param1" in params)
    assert("step3" in params)
    assert("db.path" in params)
    assert(params["param1"] == float(testing_args[1]))
    assert(params["db.path"] == testing_args[4])

def test_override_config_with_args():
    cfg = ExConfig()
    cfg2 = override_config_with_args(
        cfg,
        testing_args
    )

    assert(cfg2.db.name == "unknown")
    assert(cfg2.db.path == testing_args[4])
    assert(cfg.step1 == cfg2.step1)
    assert(cfg.step2 == cfg2.step2)
    assert(type(cfg2.step3) == bool)
    assert(cfg2.step3 == True)


def test_run_with_only_positionnals():
    print(run_function_from_commandline("numpy.e"))

test_run_with_only_positionnals()