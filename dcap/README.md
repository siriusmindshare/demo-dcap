# DCAP repository configuration labs
A local, runnable training scaffold following the requested dcap structure. Only the monthly-enrollment demonstration is implemented. It uses fictional records, configurable input checks, reusable functions and CSV reports. Star-rating files are explicit placeholders, not rating calculations. Dataset inventory and owners are worksheets awaiting confirmation.

## Owners and scope
Workstream owner, QA reviewer, publication owner and GitHub reviewers: assign before operational use. CODEOWNERS entries are commented examples. They do not request reviewers or enforce approvals. Confirm GitHub organization rules separately.

## Setup in Windows VS Code
1. Extract the archive and open the `dcap` folder with File > Open Folder. Do not open only `scripts`.
2. Open Terminal > New Terminal. Install/select an approved Python 3.10+ installation and the Python extension if available under your organization's process.
3. Run at the dcap root:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Use Ctrl+Shift+P > Python: Select Interpreter > `.venv`. Commands below can use `python` after activation, or use `.\.venv\Scripts\python.exe` directly as shown. This avoids changing the PowerShell execution policy.

## Lab 1 (30-40 minutes): set up, validate and run
```powershell
.\.venv\Scripts\python.exe scripts/setup_demo.py
.\.venv\Scripts\python.exe scripts/run_monthly_enrollment.py --month 2026-09
.\.venv\Scripts\python.exe scripts/run_monthly_enrollment.py --month 2026-10
```

Open config/paths.local.yaml, config/datasets.yaml and config/validation_rules.yaml. Trace the CLI runner into read_inputs, validate_inputs, prepare and reports. Paths resolve from the repository root. Relative paths and absolute local paths work. Approved shared-drive locations can be configured on a system that has access; this demo does not mount or connect a shared drive. Operational data and local path settings stay out of Git.

Expected state totals: September CA=100, NY=200, TX=0. October CA=115, NY=210, TX=10. The script validates all 8 input rows, then sums enrollment_count for the selected month. It does not count records as enrollment.

1. Change output_dir in paths.local.yaml to `_local/review_output` and run October again. Observe the new output location, then restore `_local/output`.
2. In `_local/input/enrollment.csv`, change one count to -1. Run the job and expect a nonnegative-integer error and exit 1. Restore the value.
3. Duplicate a complete input row and rerun. Expect a duplicate-key error. Remove the extra row.
4. Rerun both months and confirm the expected totals. A failed run does not delete a previously generated output, so do not mistake an older file for a fresh successful result.

setup_demo.py never overwrites an existing config or input. To reset the training data, copy tests/fixtures/enrollment.csv back to _local/input/enrollment.csv after confirming it is only demo data.

## Lab 2 (20-25 minutes): review month changes
```powershell
.\.venv\Scripts\python.exe scripts/run_validation.py --prior-month 2026-09 --current-month 2026-10
```

Open `_local/output/change_2026-10.csv`. CA: +15, 15.00%, REVIEW. NY: +10, 5.00%, OK. TX: +10, percentage blank, ZERO BASELINE. In validation_rules.yaml change comparison.change_threshold_pct from 10 to 4 and rerun; NY becomes REVIEW. Restore 10. A threshold equal to the change is OK because the rule uses strict greater-than, not greater-than-or-equal. Flags use the unrounded percentage; only the display is rounded.

## Tests
```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```
Tests cover monthly totals, duplicate keys, invalid months, negative values, missing columns, rounding, threshold boundaries, missing states and zero baselines.

## Local Git and GitHub handoff
For an existing authorized repository: clone its approved URL, create a working branch and copy these files into the agreed location. Do not initialize a nested repository. For a new local training repository, run at dcap root:

```powershell
git init -b main
git status --short
git add .
git diff --cached --stat
git diff --cached
git commit -m "Add configuration and enrollment training demo"
```
Review staged content first. Confirm _local, .venv and paths.local.yaml are excluded. Blank directories survive via .gitkeep. Assign real CODEOWNERS users/teams before relying on review routing. An owner assignment alone does not enforce approval rules.

After a repository owner provides an approved empty GitHub repository and URL, add its remote and push a working branch. Replace the example below before execution:

```powershell
git switch -c training/config-demo
git remote add origin <APPROVED_REPOSITORY_URL>
git push -u origin training/config-demo
```
Open a pull request using the organization's normal process. No repository is created or pushed by this package.

## What remains for real migration
Confirm the 10-11 actual datasets, SAS inventory, contractor interfaces, approved year-specific settings, business keys, validation tolerances, review ownership and publication process. Add validated SAS logic incrementally. Preserve the existing validated process and fallback until signoff.
