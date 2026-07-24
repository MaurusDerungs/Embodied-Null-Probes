from __future__ import annotations

import argparse
import os
from copy import deepcopy
from itertools import product
from pathlib import Path

from diagnostic_null_actions.run_experiment import load_config, run_config, write_rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=Path)
    args = parser.parse_args(argv)

    config = load_config(os.fspath(args.config))
    sweep = config.get("sweep", {})
    if not sweep:
        raise ValueError("sweep config must define at least one swept field")

    rows = []
    keys = list(sweep.keys())
    value_lists = [sweep[key] for key in keys]
    for values in product(*value_lists):
        run = deepcopy(config)
        run.pop("sweep", None)
        for key, value in zip(keys, values):
            run[key] = value
        rows.extend(run_config(run))

    write_rows(rows, Path(config["output"]))
    print(config["output"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
