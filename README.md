# ENIGMA-Sleep Deprivation Superdataset (`enigma-sd`)

## Overview

`enigma-sd` is the master DataLad dataset of the ENIGMA-Sleep Working Group short-term sleep loss study. It contains 13 subdatasets belonging to 10 participating sites. Each subdataset has its own README with the full acquisition parameters and the original publication.

The dataset is managed with DataLad (git and git-annex). File contents are stored in the annex and are retrieved on demand.

> **Note on subdataset names:** Some subdatasets were shared and maintained under names that could not be changed afterwards. `melbourne-bids` is the Christchurch sample, and `juelich-somnosafe-bids` and `juelich-petcoffee-bids` belong to the Cologne sample. In the study, samples with several subdatasets (Cologne and Singapore) were treated as single samples, and the table below follows that convention.

## Samples and subdatasets

| Sample | Subdataset(s) | Site | Country | N | Protocol | Images |
|---|---|---|---|---|---|---|
| Bruxelles | `bruxelles-bids` | ULB Neurosciences Institute | Belgium | 21 | SD (22 h) | T1w, dMRI |
| Christchurch | `melbourne-bids` | New Zealand Brain Research Institute | New Zealand | 16 | SR (3 h TIB) | T1w |
| Cologne | `juelich-somnosafe-bids`, `juelich-petcoffee-bids` | German Aerospace Center | Germany | 48 | SD (24 h), SR (5 h TIB) | T1w |
| Juelich | `juelich-sleepless-bids` | Forschungszentrum Juelich | Germany | 39 | SD (24 h) | T1w, dMRI |
| Montreal | `montreal-bids` | Concordia University | Canada | 18 | SD (36 h) | T1w |
| Oslo | `oslo-bids` | Oslo University Hospital | Norway | 36 | SD (32 h) | T1w, dMRI |
| Singapore | `singapore-alfie-bids`, `singapore-cheevul-bids`, `singapore-effo2-bids` | National University of Singapore | Singapore | 66 | SD (24 h) | T1w |
| Stockholm | `stockholm-bids` | Karolinska Institutet | Sweden | 81 | SR (3 h TIB) | T1w |
| Trondheim | `ntnu-bids` | Norwegian University of Science and Technology | Norway | 73 | SR (-3 h TIB) | T1w, dMRI |
| Zurich | `zurich-bids` | University of Zurich | Switzerland | 31 | SD (40 h) | T1w |

SD: total sleep deprivation. SR: sleep restriction. TIB: time in bed.

Four samples (Bruxelles, Juelich, Oslo, Trondheim) include diffusion MRI, which is required for FWI and ALPS. All samples include T1-weighted images, which are used for PVS and ChP segmentation.

## Session labels

Each scanning session is labeled `ses-T<n><code>`, where `T1`, `T2`, `T3`, ... count the single scanning sessions of a participant in chronological order, and `<code>` is the session type. For example, `ses-T1BL` is the first scan, taken at baseline, and `ses-T2SD` is the second scan, taken after sleep deprivation.

| Code | Session type |
|---|---|
| BL | Baseline, habitual |
| SR | Sleep restriction |
| SD | Sleep deprivation |
| RC | Recovery, habitual |
| CL | Control, habitual |

The same labels are used in the `session_id`, `visit`, and `condition` columns of each `sub-<ID>_sessions.tsv` file.

## Repository structure

```
enigma-sd/
├── bruxelles-bids/
├── juelich-petcoffee-bids/
├── juelich-sleepless-bids/
├── juelich-somnosafe-bids/
├── melbourne-bids/
├── montreal-bids/
├── ntnu-bids/
├── oslo-bids/
├── singapore-alfie-bids/
├── singapore-cheevul-bids/
├── singapore-effo2-bids/
├── stockholm-bids/
├── zurich-bids/
├── code/
│   ├── alps/                        ALPS analysis (clone of gbarisano/alps)
│   ├── bids/                        BIDS conversion and session relabeling scripts
│   ├── containers/                  ReproNim containers (fMRIPrep, QSIPrep)
│   ├── deprecated/                  old scripts, kept for reference
│   ├── logs/                        HTCondor logs, organized by dataset
│   ├── preproc/                     BIDS filter files
│   ├── shiva/                       PVS segmentation (clone of pboutinaud/SHiVAi)
│   ├── glymphatic_analyses.ipynb    main analysis pipeline
│   └── statistical_analyses.Rmd     statistical analyses and raw figures
└── outputs/
    ├── <dataset>/                   output datasets for each subdataset
    ├── master dataframe             all data used for statistical analyses
    └── freezes/                     all prior versions of the master dataframe
```

## Analysis workflow

1. **BIDS conversion and session relabeling** (`code/bids`). Raw data from each site are converted to BIDS and session labels are harmonized across samples.
2. **Preprocessing and glymphatic indices** (`code/glymphatic_analyses.ipynb`). This notebook is the main analysis pipeline. It runs preprocessing (fMRIPrep and QSIPrep from `code/containers`, restricted with the filter files in `code/preproc`) and computes the glymphatic indices: choroid plexus volume (ChPV), perivascular space volume (PVSV), free water index (FWI), and ALPS. PVS segmentation uses `code/shiva` and ALPS uses `code/alps`. Its output is the master dataframe in `outputs/`.
3. **Statistical analyses** (`code/statistical_analyses.Rmd`). This R Markdown file reads the master dataframe, performs the statistical analyses, and generates the raw figures.

## Code

### `code/glymphatic_analyses.ipynb`

The main analysis pipeline. It covers preprocessing and the computation of the four glymphatic indices (ChPV, PVSV, FWI, ALPS) for all samples, and writes the master dataframe.

### `code/statistical_analyses.Rmd`

Statistical analyses of the master dataframe and generation of the raw figures.

### `code/alps`

Clone of the ALPS repository by Liu and Barisano ([github.com/gbarisano/alps](https://github.com/gbarisano/alps)). It computes the diffusivity along the perivascular space (ALPS) index from diffusion MRI, a proposed measure of glymphatic function. Used for all ALPS analyses in this project.

- Taoka, T., et al. (2017). Evaluation of glymphatic system activity with the diffusion MR technique: diffusion tensor image analysis along the perivascular space (DTI-ALPS) in Alzheimer's disease cases. *Japanese Journal of Radiology*, 35, 172–178. [https://doi.org/10.1007/s11604-017-0617-z](https://doi.org/10.1007/s11604-017-0617-z)
- Liu, X., Barisano, G., Shao, X., et al. Cross-vendor test-retest validation of diffusion tensor image analysis along the perivascular space (DTI-ALPS) for evaluating glymphatic system function. *Aging and Disease*. [https://doi.org/10.14336/AD.2023.0321-2](https://doi.org/10.14336/AD.2023.0321-2)

### `code/bids`

Scripts for BIDS conversion and for session relabeling. Session labels were harmonized across samples, and each `sub-<ID>_sessions.tsv` file records the session, condition, visit, date, and time.

### `code/containers`

Clone of the ReproNim containers collection ([github.com/ReproNim/containers](https://github.com/ReproNim/containers)), which provides containerized neuroimaging tools as a DataLad dataset. It contains the fully containerized versions of fMRIPrep and QSIPrep used here. Containers are run with `datalad containers-run`, which records the exact container version in the git history.

### `code/deprecated`

Old scripts that are no longer used. They are kept for provenance only and should not be used to reproduce the current results.

### `code/logs`

Logs of HTCondor runs, organized by dataset.

### `code/preproc`

BIDS filter files used to select the images passed to the preprocessing pipelines.

### `code/shiva`

Clone of the SHiVAi repository ([github.com/pboutinaud/SHiVAi](https://github.com/pboutinaud/SHiVAi)), used for PVS segmentation on T1-weighted images. It builds on the SHIVA-PVS model.

- Boutinaud, P., Tsuchida, A., Laurent, A., et al. (2021). 3D segmentation of perivascular spaces on T1-weighted 3 Tesla MR images with a convolutional autoencoder and a U-shaped neural network. *Frontiers in Neuroinformatics*. [https://doi.org/10.3389/fninf.2021.641600](https://doi.org/10.3389/fninf.2021.641600)

## Outputs

The `outputs/` folder holds:

- **Output datasets** for each subdataset.
- **Master dataframe**: the table containing all data used for the statistical analyses, produced by `code/glymphatic_analyses.ipynb`.
- **`freezes/`**: every prior version of the master dataframe, so that earlier analyses can be reproduced exactly.

## Getting the data

```bash
datalad clone <url> enigma-sd
cd enigma-sd
datalad get -n .                      # install all subdatasets without file content
datalad get bruxelles-bids/sub-<ID>   # retrieve content for specific subjects
```

File contents are tracked with git-annex, so a fresh clone contains links only until `datalad get` is run. Access to the file contents depends on read permission for the storage remote.

## Computing environment

- Processing was run on an HTCondor cluster. Job logs are in `code/logs`.
- Preprocessing uses containers from `code/containers`, run through `datalad containers-run` so that each step is recorded in the git history.
- The analysis pipeline is a Jupyter notebook (Python), and the statistical analyses are an R Markdown file (R).

## Contact

- Jorik D. Elberse: [j.elberse@fz-juelich.de](mailto:j.elberse@fz-juelich.de)
- Masoud Tahmasian: [m.tahmasian@fz-juelich.de](mailto:m.tahmasian@fz-juelich.de)

## Acknowledgements

The data were collected and shared by the contributing sites of the ENIGMA-Sleep Working Group. See the subdataset READMEs for the original publication of each sample.
