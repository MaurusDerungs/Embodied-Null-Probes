# References And Novelty Positioning

This note records the sources used to position the project. The novelty claim remains probabilistic: no reviewed source was found that directly evaluates paired, nominally cancelling robot actions as embodied negative-control interventions while jointly measuring parameter information, maximum task disturbance, and cumulative task disturbance.

## Core Reference Threads

### Damage Recovery Without Explicit Diagnosis

- Cully, Clune, Tarapore, and Mouret, "Robots that can adapt like animals," Nature 2015 / arXiv 2014. URL: https://arxiv.org/abs/1407.3501
- Chatzilygeroudis, Vassiliades, Stulp, Calinon, and Mouret, "Reset-free Trial-and-Error Learning for Robot Damage Recovery," Robotics and Autonomous Systems / arXiv 2016. URL: https://arxiv.org/abs/1610.04213

Relevance: These works show that robots can adapt to damage by searching behavior repertoires or learning during deployment. They usually optimize compensatory behavior after damage, whereas this project asks whether low-disturbance diagnostic interventions can expose hidden embodiment changes before or during recovery.

### Active System Identification

- Memmel, Wagenmaker, Zhu, Yin, Fox, and Gupta, "ASID: Active Exploration for System Identification in Robotic Manipulation," arXiv 2024. URL: https://arxiv.org/abs/2404.12308
- WEIRDLab ASID implementation. URL: https://github.com/WEIRDLabUW/asid

Relevance: ASID motivates active data collection for system identification and sim-to-real transfer. The `constrained_fisher` baseline in this repository is deliberately aligned with this thread as the strongest local challenge to diagnostic null actions.

### Causal And Interventional Robotics Benchmarks

- Ahmed et al., "CausalWorld: A Robotic Manipulation Benchmark for Causal Structure and Transfer Learning," arXiv 2020. URL: https://arxiv.org/abs/2010.04296
- CausalWorld repository. URL: https://github.com/rr-learning/CausalWorld
- "Interventional Boundary Discovery for Reinforcement Learning," arXiv 2026. URL: https://arxiv.org/html/2603.18257

Relevance: These sources motivate interventions and controlled causal variation in robot learning. They do not appear to study paired physical null interventions as diagnostic negative controls for hidden embodiment changes.

### Failure Discovery And Safe Exploration

- "RoboFail: Analyzing Failures in Robot Learning Policies," arXiv 2024. URL: https://arxiv.org/html/2412.02818v1
- Garcia and Fernandez, "A Comprehensive Survey on Safe Reinforcement Learning," JMLR 2015. URL: https://www.jmlr.org/papers/volume16/garcia15a/garcia15a.pdf
- Safe exploration overview in robotics, Garcia/Fernandez-adjacent survey thread. URL: https://link.springer.com/chapter/10.1007/978-3-319-13823-7_31

Relevance: These works prioritize avoiding unsafe exploration or discovering failures. Diagnostic null actions are adjacent but ask a narrower measurement question: can a robot collect diagnostic evidence while minimizing accumulated disturbance from the task state?

### Cross-Embodiment Robot Learning

- Open X-Embodiment Collaboration, "Open X-Embodiment: Robotic Learning Datasets and RT-X Models," arXiv 2023. URL: https://arxiv.org/abs/2310.08864
- Project website. URL: https://robotics-transformer-x.github.io/

Relevance: Large robot datasets motivate general embodied policies and adaptation across platforms. This project focuses on small, falsifiable diagnostic probes rather than broader policy scaling.

### Negative Controls In Causal Inference

- Lipsitch, Tchetgen Tchetgen, and Cohen, "Negative Controls: A Tool for Detecting Confounding and Bias in Observational Studies," Epidemiology 2010. URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC3053408/

Relevance: Negative controls are used to reveal bias or hidden confounding by using variables or outcomes that should not be causally affected in the target way. This project transfers the spirit of negative controls into embodied robotics: actions designed to have no nominal net task effect become probes for hidden physical changes.

## Novelty Boundary

The project should not claim novelty for:

- robot damage recovery;
- active probing;
- system identification;
- safe exploration;
- causal intervention in robot learning;
- negative controls as a statistical concept.

The defensible novelty claim is narrower:

Within the reviewed sources, no direct precedent was located for an evaluation protocol in which a robot executes paired, nominally cancelling physical action sequences as embodied negative controls, and evaluates them against unpaired-action, random, task-greedy, Fisher-grid, and disturbance-constrained Fisher baselines using parameter error, maximum diagnostic disturbance, and cumulative diagnostic disturbance.

## Search Limitations

- The search was broad but not exhaustive.
- Terminology may differ; related work may describe similar ideas as "reversible probes," "undo actions," "safe excitation," "probing maneuvers," "null-space exploration," or "self-test actions."
- Patent and dissertation coverage was not exhaustive.
- Future or unpublished workshop work may directly overlap.
