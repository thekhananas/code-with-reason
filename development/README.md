# Run the Project

This directory contains the application and experiment commands. Read the
[dissertation](https://github.com/thekhananas/msc-dissertation-report-writing-ak7025) for the research methods and findings.

## Start the Demo

Install Git and Pixi 0.63 or later. The environment supports Apple Silicon macOS and Linux x86-64.
Pixi installs Python, Node.js and the project dependencies. Start from the repository root:

```sh
cd development
pixi install --locked
pixi run install-web
pixi run dev
```

Open **http://127.0.0.1:5173/**. Installation needs internet access. The tutor and recorded experiments then work
without credentials or a `.env` file. The demo estimate is not a validated measure of student learning.

Run all remaining commands from `development/`. Stop the application with Ctrl+C before restarting it.

## Enable Live Model Calls

Use your own Cerebras API key and Modal account. Create a local settings file:

```sh
cp -n .env.example .env
```

This preserves an existing `.env`. Open it and uncomment or add these settings, replacing the key placeholder:

```dotenv
SOCRATIC_LIVE_EVALUATION_ENABLED=true
SOCRATIC_LIVE_EVALUATION_CASE_ID=dev-aliasing-001
SOCRATIC_CEREBRAS_API_KEY=your-actual-key
```

Authenticate with Modal, then start the application:

```sh
pixi run modal setup
pixi run dev
```

Select **Experiment > Live illustration**. Start a run, inspect its predictions, then select **Reveal live result**.
A complete run makes up to three Cerebras requests to `gpt-oss-120b` and two Modal executions. These may incur charges.
This runs a demonstration case. Reproducing the dissertation studies requires the inputs described below.

Keep `.env` private. To disable live calls, set `SOCRATIC_LIVE_EVALUATION_ENABLED=false` and restart the application.

## Run Checks

| Command | Purpose |
|---|---|
| `pixi run build-web` | Production web build |
| `pixi run check` | Complete checks |

Install Chromium before running browser tests:

```sh
pixi run pnpm --dir apps/web exec playwright install chromium
```

On Linux, add `--with-deps` before `chromium` if system libraries are missing. This may require administrator access.
The complete checks also require D2 0.7.1. CI installs these dependencies.

## Analysis Entry Points

The repository includes demo records and study configurations. Full reproduction also needs saved experiment files or
the learner dataset. These are excluded from Git. Contact the author listed in the [project README](../README.md#project-details)
to arrange access to experiment records that can be shared.

| Study | Command to inspect available options | Required inputs |
|---|---|---|
| External model benchmark | `pixi run python scripts/benchmark_cli.py --help` | Saved responses, ratings and execution records |
| Probe selection simulation | `pixi run python scripts/acquisition_study_canonical.py --help` | Study plans, calibration records and the saved experiment settings |
| Probe selection analysis | `pixi run python scripts/acquisition_study_canonical_analysis.py --help` | Saved simulation observations and the original environment |
| Learner records | `pixi run python scripts/csedm_study_reproduce.py --help` | CSEDM dataset archive |

The original probe selection analysis requires revision `5d6e76b099f8904d5a70aca5909b49d6fa0d86af` and its lockfile.
Use a separate checkout with the retained experiment inputs. The required hashes and paths are in
[`v1-canonical-primary-analysis.yaml`](configs/acquisition-study/v1-canonical-primary-analysis.yaml).
The current lockfile differs, so running that analysis directly from the current checkout will fail validation.

Obtain CSEDM from [DataShop dataset 2865](https://doi.org/10.60710/DATASET-2865), following its access conditions.
The expected archive is `data/CSEDM_DataChallenge v1.1.zip`. Its checksum and required contents are in
[`v1-inventory.yaml`](configs/csedm-study/v1-inventory.yaml). Then run:

```sh
pixi run csedm-reproduce
```

Results go to `artifacts/csedm-study/reproduction-<revision>/`. Preserve the generated `pipeline_manifest.json`.
For another run, select an unused output directory:

```sh
pixi run python scripts/csedm_study_reproduce.py --output-root artifacts/csedm-study/reproduction-review-001
```

## Troubleshooting and Local Files

- **Port in use:** stop the previous demo. The web interface uses port 5173 and the API uses port 8000.
- **Live call fails:** check your Cerebras key and Modal authentication. Use recorded replay if the provider is unavailable.
- **Missing experiment input:** restore the required records before running the analysis.
- **Output already exists:** preserve the previous result and choose another output directory when the command permits it.

Demo conversations are saved in `.local/`. Experiment outputs are saved in `artifacts/`. Both remain local.
Keep credentials, learner archives and reviewer information out of commits.
