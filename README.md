# EventNoise: Perception and Encoding of Narrative Events During Speech Listening in Background Noise

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository contains data, analysis, code, and experimental materials for a study which investigating how background noise affects event segmentation, speech intelligibility, and memory for naturalistic spoken narratives.

Panela, R.A., Barnett, A.J., Lamekina, Y., Barense, M.D., & Herrmann, B. (2026). Perception and Encoding of Narrative Events During Continuous Speech Listening in Background Noise. *PsyArXiv*. https://doi.org/10.31234/osf.io/e67qr_v1

## Overview
Event segmentation – the cognitive process of parsing continuous experiences into discrete, meaningful unites – is fundamental to comprehension and memory. This study examines how background noise impacts listeners' ability to segment spoken speech and whether segmentation behaviour predicts subsequent recall performance.

Participants listened to three narratives at varying signal-to-noise ratios (clear, +2 dB SNR, –4 dB SNR) while marking event boundaries, then subsequently performed a free recall task. We assessed speech intelligibility, event segmentation, and recall to understand whether listening challenges affect the perceptual organization and encoding of narratives.

## Repository Structure

```
EventNoise/
├── code/                          # Analysis scripts
│   ├── intelligibility/           # Speech intelligibility analysis
│   │   └── intelligibility.Rmd
│   ├── recall/                    # Memory recall analysis
│   │   └── recall_analysis.Rmd
│   └── segmentation/              # Event segmentation analysis
│       ├── auditory_segmentation.Rmd
│       └── esMethods_agreement.R
│
├── data/                          # Processed data files
│   ├── intelligibility/           # Intelligibility task data
│   │   ├── intelligibility_responses.csv
│   │   └── intelligibility_scores.csv
│   ├── recall/                    # Free recall data
│   │   ├── centrality.csv         # Event centrality ratings
│   │   ├── event_recall.csv       # Scored recall data
│   │   └── transcripts/           # Raw recall transcriptions (N=34)
│   ├── segmentation/              # Event segmentation data
│   │   ├── agreement.csv          # Inter-rater agreement
│   │   ├── auditory_data.csv      # Main segmentation data
│   │   ├── auditory_series.csv    # Time-series data
│   │   └── sliding_*.csv          # Sliding window analyses
│   └── stories/                   # Stimulus information
│       ├── normative_boundaries.csv
│       ├── raw/                   # Story transcripts
│       └── word_times/            # Word-level timing data
│
└── experiment/                    # PsychoPy experiment files
    ├── Auditory.py                # Event segmentation task
    ├── MasterExperiment.py        # Main experiment controller
    ├── SpeechIntelligibility.py   # Intelligibility task
    ├── audio/                     # Audio stimuli (3 stories × 3 SNR levels)
    ├── instructions/              # Task instruction slides
    ├── order/                     # Counterbalancing files
    └── requirements.txt
```

## Data Description

### Segmentation Data (`auditory_data.csv`)
- `subject`: Participant ID
- `trial`: Block
- `story_id`: Story
- `noise_condition`: SNR ondition (clear, +2SNR, -4SNR)
- `times`: Timestamp of button press (seconds)
- `word_number`: Relative word number of button press
- Additional derived measures (agreement index, sliding window)

### Recall Data (`event_recall.csv`)
- `subject`: Participant ID
- `story_id`: Story 
- `noise_condition`: SNR condition (clear, +2SNR, -4SNR)
- `recall_index`: Index position in participant's recall sequence
- `event_number`: Relative event position in narrative
- `recall_events`: Semantic similarity between recall and narrative event
- `random_events`: Baseline similarity (random event comparison)
- `diagonal_score`: Similarity score for sequential event matching
- `reversed_score`: Similarity score for reverse-order matching

### Intelligibility Data (`intelligibility_scores.csv`)
- `subject`: Participant ID
- `noise_condition`: SNR condition (clear, +2SNR, -4SNR)
- `proportion`: Proportion of words correctly transcribed

## Requirements

### For running experiments
```
psychopy=2023.2.3
numpy>=2.4
pandas==3.0.0
```

### For analyses (R)
```r
tidyverse
lme4
lmerTest
lm.beta
emmeans
effectsize
ggplot2
ggdist
ggeffects
```

## Usage

### Running the Experiment
```bash
cd experiment
pip install -r requirements.txt
python MasterExperiment.py
```

### Running Analyses
Open the relevant `.Rmd` files in RStudio:
- `code/segmentation/auditory_segmentation.Rmd` - Event segmentation analyses
- `code/recall/recall_analysis.Rmd` - Recall analyses
- `code/intelligibility/intelligibility.Rmd` - Intelligibility analyses

## Stories

The study used three narratives from Trevor Noah's memoire [Born A Crime](https://trevornoahbooks.com/). The book highlights his experiences growing up during the era of Apartheid in South Africa

| Story | Duration | 
|-------|----------|
| Run! | 585.51 s | 
| Go Hitler! | 545.39 s| 
| My Mother's Life | 667.25 s|

## Contact

For questions about this repository, please open an issue or contact [Ryan Panela](ryan.panela@utoronto.ca).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

MIT License © 2025 Ryan A. Panela
