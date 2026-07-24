from diagnostic_null_actions.run_experiment import main


def test_smoke(tmp_path):
    cfg = tmp_path / "cfg.json"
    cfg.write_text(
        """{
          "seed": 1, "trials": 1, "diagnostic_steps": 4, "task_steps": 8,
          "dt": 0.1, "wheel_base": 0.42, "process_noise": 0.0, "observation_noise": 0.0,
          "damage_cases": [{"name":"left_gain_loss","left_gain":0.62,"right_gain":1.0,"slip":0.02}],
          "policies": ["null_probe", "random_probe"],
          "output": "%s"
        }"""
        % (tmp_path / "out.csv"),
        encoding="utf-8",
    )
    assert main([str(cfg)]) == 0
    assert (tmp_path / "out.csv").read_text(encoding="utf-8").count("\n") == 3

