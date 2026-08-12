# ACL Recovery Analytics

An end-to-end analytics project that transforms surface electromyography (sEMG) recordings into interpretable bilateral muscle activation metrics for exploratory ACL rehabilitation analysis.

The project combines signal processing, quality control, feature engineering, statistical analysis, participant-level screening, and an interactive Streamlit dashboard.

> **Note:** This project is an exploratory analytics prototype. It is not a clinical diagnostic tool and should not be used for rehabilitation or return-to-sport decisions.

---

## Project Overview

ACL rehabilitation is commonly evaluated using functional tests and clinician assessment, but recovery can vary substantially between individuals.

This project explores whether bilateral sEMG activation patterns can provide an additional quantitative view of muscle activation asymmetry.

The analysis focuses on three questions:

1. How symmetric is muscle activation between the involved and uninvolved sides?
2. How does an individual's asymmetry compare with a healthy reference group?
3. Can signal quality control and participant-level analytics identify recordings or participants that require additional review?

The final workflow converts raw sEMG recordings into an interactive analytics dashboard for cohort-level and participant-level exploration.

---

## Analytics Pipeline

```text
Raw sEMG recordings
        ↓
Data inspection and signal validation
        ↓
Signal preprocessing
        ↓
Contraction detection
        ↓
Quality control
        ↓
Active RMS feature extraction
        ↓
Bilateral activation metrics
        ↓
Healthy reference comparison
        ↓
Cohort and participant-level analysis
        ↓
Interactive Streamlit dashboard
```

---

## Dataset

The analysis includes ACL patient recordings and healthy-control recordings with measurements from involved and uninvolved sides.

After signal-level quality control, the primary analytical sample contains:

- **11 ACL patients**
- **8 healthy controls**

Participants or recordings that failed predefined analytical QC criteria are retained for transparency but excluded from the primary analysis.

Raw data files are not included in this repository. The processed feature dataset used by the dashboard is available in:

```text
data/processed/bilateral_semg_features.csv
```

---

## Signal Processing and Quality Control

Raw sEMG recordings were inspected before participant-level comparisons were performed.

The workflow includes:

- signal structure and sampling inspection
- baseline estimation
- threshold-based active-region detection
- contraction segmentation
- valid-contraction counting
- active-signal RMS calculation
- recording-level quality control

QC guardrails prevent unreliable recordings from automatically receiving a full participant-level interpretation.

Examples include recordings with insufficient valid contractions or unusual signal amplitude.

---

## Feature Engineering

The main participant-level features include:

### Active RMS

Mean RMS amplitude calculated from detected active contraction regions.

### RMS Ratio

```text
RMS Ratio = Involved Active RMS / Uninvolved Active RMS
```

A value close to **1.0** indicates similar bilateral activation.

Values below 1 indicate lower involved-side activation, while values above 1 indicate higher involved-side activation.

### Symmetry Deviation

To measure distance from perfect bilateral symmetry:

```text
Symmetry Deviation = |log(RMS Ratio)|
```

This treats proportional deviations above and below 1 symmetrically.

### Activation Difference

The magnitude of bilateral activation difference is also expressed as a percentage to improve interpretability.

---

## Healthy Reference Comparison

A healthy-control reference distribution is used to contextualize participant-level asymmetry.

Participants are compared with the healthy median using a robust deviation score based on the median absolute deviation (MAD).

This supports exploratory analytical categories such as:

- Routine review
- Moderate review priority
- High review priority

These categories represent analytical distance from the healthy reference distribution and are **not clinical risk classifications**.

---

## Key Findings

At the cohort level, mean bilateral symmetry deviation was nearly identical:

| Cohort | Mean Symmetry Deviation |
|---|---:|
| ACL Patients | 0.277 |
| Healthy Controls | 0.278 |

The similarity of the group averages masks substantial participant-level variation.

Within the ACL cohort:

- **3 participants** were assigned high analytical review priority
- **2 participants** were assigned moderate review priority
- **6 participants** were within the routine review range

Several ACL participants demonstrated substantially lower involved-side activation relative to their uninvolved side.

For example, one participant showed an RMS ratio of approximately **0.61**, corresponding to approximately **39% lower involved-side activation**.

This illustrates an important analytical insight:

> **Group-level averages can obscure meaningful participant-level heterogeneity.**

Rather than relying only on cohort averages, participant-level screening provides a way to identify individual activation patterns that may warrant additional analytical review.

---

## Statistical Analysis

The project also evaluates whether the ACL and healthy-control groups differ in overall symmetry deviation.

The primary comparison did not show evidence of a cohort-level difference in this exploratory sample.

Because the sample size is small, the analysis includes multiple approaches:

- Welch's t-test
- Mann–Whitney U test
- permutation testing
- bootstrap confidence intervals
- standardized effect sizes
- sensitivity analysis

The statistical results are interpreted cautiously and are not used to make clinical claims.

---

## Interactive Dashboard

A Streamlit dashboard translates the analytical workflow into an interactive prototype.

### Cohort Overview

The cohort dashboard provides:

- primary-analysis sample counts
- ACL vs. healthy asymmetry comparison
- participant-level distribution visualization
- review-priority summary
- activation-direction summary
- participant-level asymmetry plots
- flagged-participant table
- quick participant lookup

### Participant Explorer

The participant-level view provides:

- bilateral RMS ratio
- activation difference
- robust asymmetry score
- healthy-reference category
- valid contraction counts
- automated analytical interpretation
- bilateral activation visualization
- healthy-reference comparison

A QC guardrail prevents excluded recordings from receiving a full analytical assessment.

---

## Repository Structure

```text
acl-rehab-analytics/
│
├── app/
│   └── app.py
│
├── data/
│   └── processed/
│       └── bilateral_semg_features.csv
│
├── notebooks/
│   ├── 01_semg_signal_processing.ipynb
│   └── 02_recovery_analytics.ipynb
│
├── src/
│
├── .gitignore
├── README.md
└── requirements.txt
```

### Notebooks

**01_semg_signal_processing.ipynb**

Signal inspection, preprocessing, contraction detection, feature extraction, and quality-control workflow.

**02_recovery_analytics.ipynb**

Bilateral feature construction, healthy-reference comparison, statistical analysis, participant screening, and analytical reporting.

---

## Running the Dashboard

Clone the repository:

```bash
git clone <repository-url>
cd acl-rehab-analytics
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
streamlit run app/app.py
```

---

## Technology Stack

- Python
- Pandas
- NumPy
- SciPy
- Matplotlib
- scikit-learn
- Streamlit
- Jupyter Notebook
- Git / GitHub

---

## Limitations

This project has several important limitations.

The analytical sample is small, particularly the healthy reference group. The reference distribution therefore should not be interpreted as a population-level clinical benchmark.

sEMG amplitude can also be influenced by factors such as electrode placement, recording conditions, normalization procedures, and signal quality.

The current analysis focuses primarily on bilateral activation magnitude and does not model the full temporal or biomechanical complexity of ACL recovery.

For these reasons, the dashboard is intended as an exploratory analytics prototype rather than a clinical decision-support system.

---

## Future Development

Potential extensions include:

- larger healthy reference datasets
- longitudinal recovery tracking
- normalized EMG measures
- contraction-level temporal features
- additional biomechanical variables
- recovery trajectory visualization
- predictive modeling with larger validated datasets
- improved automated signal-quality assessment

---

## Project Goal

The broader goal of this project is to demonstrate how noisy physiological sensor data can be transformed into a reproducible analytics workflow and an interpretable decision-support prototype.

The project emphasizes not only statistical analysis, but also data quality, feature engineering, uncertainty, individual heterogeneity, and communication of analytical results.