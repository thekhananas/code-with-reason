# Evaluating Code Evidence for AI Programming Tutors

This MSc Computing project asks whether running an additional coding check helps a tutor predict performance on a separate
programming task. It also examines how unreliable evidence affects a prediction and which cases should receive checks when
their number is limited.

The repository contains a working tutoring demo, an experiment pipeline and analysis code. The studies use one language
model, controlled simulations and existing Python learner records. They measure prediction quality. They do not establish
improved student learning.

The [dissertation and its build instructions](https://github.com/thekhananas/msc-dissertation-report-writing-ak7025)
are maintained in a separate repository.

## Project Details

| Field | Details |
|---|---|
| Institution | Imperial College London, Department of Computing |
| Degree | MSc Computing (Individual Project) |
| Author | Anas Khan (ak7025@ic.ac.uk) |
| Supervisor | Dr. Konstantinos Gkoutzis |
| Second Marker | Dr. Thomas Lancaster |
| Academic Year | 2025-2026 |
| Submission Date | September 2026 |

## Run the Demo

Install [Pixi](https://pixi.sh/) and Git. The locked environment supports Apple Silicon macOS and Linux x86-64.
Run these commands in a terminal:

```sh
git clone https://github.com/thekhananas/msc-dissertation-ak7025.git
cd msc-dissertation-ak7025/development
pixi install --locked
pixi run install-web
pixi run dev
```

Open **http://127.0.0.1:5173/**. Initial installation needs internet access. The tutor and recorded experiments then run
without model credentials.

In **Tutor**, choose a Python task and submit an explanation. The interface shows the response check, an updated demo
estimate and the next question. The estimate is a demonstration score, not a validated measure of a learner's knowledge.

In **Experiment**, inspect saved predictions before revealing a separate task result. The recorded example shows how code
can pass tests that miss a requirement. The probe selection view compares two methods using the same saved simulation episode.

An optional live illustration calls Cerebras `gpt-oss-120b` and runs generated code in Modal. It is disabled by default and
requires credentials and network access. See the [development guide](development/README.md) for setup and possible charges.

## Findings

After correcting a scoring fault, additional coding evidence increased correct predictions from 18 to 19 among 23 eligible
authored cases. That small study did not establish a general benefit.

Limiting each Bayesian update reduced average error across the tested adverse simulation settings, with worse results in
some settings. Under an equal probe budget, the proposed selection rule beat random selection but lost to stronger simple
alternatives, including uncertainty selection.

In a separate analysis of existing learner records, uncertainty helped identify prediction errors. No teaching intervention
was tested. The dissertation explains the methods, uncertainty and limitations behind these findings.

## Where to Look

| Location | Contents |
|---|---|
| [Web application](development/apps/web/src/) | Tutoring interface and experiment views |
| [API](development/apps/api/) | Local application endpoints |
| [Python implementation](development/src/socratic_tutor/) | Tutoring logic, model adapters, sandbox execution and analyses |
| [Study configurations](development/configs/) | Experiment settings and analysis plans |
| [Research inputs](development/data/) | Authored tasks, benchmark cases and demo records |
| [Scripts](development/scripts/) | Commands for running and analysing studies |
| [Tests](development/tests/) | Checks of calculations, data boundaries and application behaviour |
| [Original proposal](proposal/) | Historical proposal, which predates the final scope |

## Reproduction and Checks

The checkout includes the inputs needed for the offline demo. Full experiment reproduction also needs the retained response
and execution records. The historical CSEDM archive must be obtained separately. These files are not included in Git.
The [development guide](development/README.md#analysis-entry-points) explains the required inputs and version constraints.

For the complete local checks, run from `development/`:

```sh
pixi run pnpm --dir apps/web exec playwright install chromium
pixi run check
```

The complete check also requires D2 0.7.1. Linux may need Playwright's system dependencies. CI installs both before running
the checks. Focused test and build commands are listed in the development guide.

Keep credentials in `development/.env`. Generated experiment outputs and local demo conversations are excluded from Git.
The package's current licence declaration is recorded in [pyproject.toml](development/pyproject.toml).
