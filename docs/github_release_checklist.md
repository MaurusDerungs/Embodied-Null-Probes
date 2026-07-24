# GitHub Release Checklist

Recommended repository name:

```text
embodied-null-probes
```

Recommended one-line description:

```text
Reproducible study of embodied negative-control probes for low-disturbance robot self-diagnosis.
```

Suggested GitHub topics:

```text
robotics, embodied-ai, robot-learning, system-identification, safe-exploration, causal-inference, negative-controls
```

## Before Publishing

- Replace contributor metadata in `CITATION.cff` with real author names if desired.
- Decide whether to keep generated raw CSV logs in Git or attach them as release assets.
- If keeping CSV logs in Git, note that the repository is evidence-heavy but immediately reproducible.
- Create a first GitHub release after upload and archive it with Zenodo if a DOI is desired.
- Update `CITATION.cff` with `repository-code`, DOI, and final release date after archiving.
- Add a project screenshot or figure preview in the GitHub repository settings if desired.

## Suggested Initial Commit Message

```text
Initial release of embodied null probe study
```

## Suggested Release Title

```text
v0.1.0: First reproducible simulation study
```

## Suggested Release Notes

```text
First public release of Embodied Null Probes.

Includes:
- differential-drive diagnostic simulator;
- paired null-probe and baseline policies;
- budget, robustness, recovery, and correlated-slip sweeps;
- 38,400 raw experiment rows;
- quantified SVG figures with 95% confidence intervals;
- full manuscript draft and novelty audit notes.

The central result is a boundary-condition finding: paired null probes are not superior estimators, but they expose a cumulative-disturbance tradeoff that remains scientifically useful against constrained active probing.
```
