# Abdominal Trauma Classification from CT Slices

This repository contains a research prototype for multi-label abdominal trauma classification using a 3D convolutional neural network in PyTorch. It was developed from the [RSNA 2023 Abdominal Trauma Detection](https://www.kaggle.com/competitions/rsna-2023-abdominal-trauma-detection/data) competition dataset.

## Dataset and scope

The exploratory notebook inventories:

- 1,500,653 CT image slices
- 4,711 CT series
- 3,147 patients

The notebooks in this repository expect **preconverted PNG slices** plus the competition CSV metadata. They do not read raw DICOM files, connect to PACS, or perform DICOM de-identification. Patient and series identifiers are the de-identified identifiers supplied with the competition data.

This project is an educational research prototype. It has not been externally validated, integrated into a clinical workflow, or approved for diagnosis or patient care.

## What the project demonstrates

- Exploratory analysis and validation of image- and patient-level metadata
- Grouping of 2D CT slices by series and patient
- Conversion of image stacks into standardized 3D PyTorch tensors
- Patient-level train, validation, and test splitting
- Training of a multi-label 3D CNN
- Evaluation with per-label ROC AUC, average precision, sensitivity, specificity, precision, recall, F1 score, and accuracy

## Repository structure

The notebooks are intended to be run in order:

1. `1. Data entry and EDA.ipynb` - inspect the metadata and image inventory.
2. `2. Images-to-3d-tensors.ipynb` - group PNG slices and create series- and patient-level tensors.
3. `3. Check 3d object.ipynb` - visually inspect an example 3D tensor.
4. `4. PyTorch_CNN.ipynb` - split patients, train the model, and evaluate the held-out test set.

Shared paths are defined in `project_config.py`.

## Reproducible setup

### 1. Clone the repository

```bash
git clone https://github.com/Babak-Davani/CtScan-CNN.git
cd CtScan-CNN
```

### 2. Create the environment

```bash
conda env create -f environment.yml
conda activate ctscan-cnn
```

### 3. Prepare the data

Place the competition CSV files and preconverted PNG slices under `data/`:

```text
data/
├── train.csv
├── train_series_meta.csv
├── image_level_labels.csv
├── images.csv
└── train_images/
    ├── <patient_id>_<series_id>_<instance>.png
    └── ...
```

The competition data are not committed to this repository. Follow the competition terms when downloading or transforming the data.

### 4. Optional path configuration

The default directories are inside the repository. Override them with environment variables when data or artifacts are stored elsewhere:

```bash
export CTSCAN_DATA_DIR=/path/to/data
export CTSCAN_ARTIFACT_DIR=/path/to/artifacts
```

On PowerShell:

```powershell
$env:CTSCAN_DATA_DIR = "C:\path\to\data"
$env:CTSCAN_ARTIFACT_DIR = "C:\path\to\artifacts"
```

### 5. Start Jupyter

```bash
jupyter lab
```

Run the notebooks from the repository root in the order shown above. Intermediate tensors and model outputs are written beneath `artifacts/` by default.

## Leakage prevention

The modelling table contains one row per patient. The split is performed on this patient-level table before `Dataset` and `DataLoader` objects are constructed. Assertions verify that:

- `patient_id` is unique in the modelling table; and
- no patient identifier occurs in more than one of the train, validation, or test partitions.

Consequently, multiple series or slices belonging to one patient cannot be distributed across different partitions. A fixed random seed makes the split reproducible. Class balancing is applied only to the training loader; validation and test loaders remain unmodified.

## Evaluation

The network produces logits and is trained with `BCEWithLogitsLoss`. A default logit threshold of `0.0` is used for binary predictions, which is equivalent to a probability threshold of `0.5` after the sigmoid function.

The evaluation notebook reports per-label metrics rather than relying on a single overall accuracy. This is important because abdominal injury labels are imbalanced and accuracy alone can obscure poor detection of uncommon positive cases. Threshold selection and model calibration would require separate validation before any applied use.

## Limitations

- The workflow expects preconverted PNG slices and therefore does not preserve or use the complete DICOM metadata and intensity-processing pipeline.
- The model and preprocessing choices are experimental and have not been clinically validated.
- Reported notebook results depend on the local data transformation, split, and runtime configuration.
- No claim of diagnostic performance or clinical readiness should be inferred from this repository.

## Next steps

- Add a documented DICOM-to-array preprocessing stage with appropriate intensity handling.
- Compare the prototype with established medical-imaging architectures.
- Use repeated or cross-site validation and confidence intervals.
- Evaluate calibration and clinically relevant operating thresholds.
- Add automated tests for metadata validation and preprocessing.
