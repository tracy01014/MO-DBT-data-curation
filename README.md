# MO-DBT Data Curation

This repository contains the pipeline for curating the MO-DBT dataset. The curation process involves several sequential steps as outlined below.

## Pipeline Steps

### (Optional) 0. Image Folder Parsing (`parse_image_folder`)
This script parses the image folder structure and extracts relevant metadata to generate standardized tags.

* **Outputs:**
  *`P:/Dataset/R01-MO-DBT/MO-DBT-data-curation/R3Data/dicomtocsv_series_{date}.xlsx`

### 1. DICOM Tag Processing (`dicom_tag`)
#### (Optional) 1. DICOM Tag Processing (`dicom_tag_v2`): for processing multi-part DICOM series files (construct from image folder directly)
Groups DICOM records and extracts relevant attributes to generate standardized tags.

* **Inputs:**
  * `P:/Dataset/R01-MO-DBT/MO-DBT-data-curation/R3Data/dicomtocsv_series.csv`
  * `P:/Dataset/R01-MO-DBT/MO-DBT-data-curation/R3Data/dicomtocsv_study.csv`
* **Outputs:**
  * `P:/Dataset/R01-MO-DBT/MO-DBT-data-curation/dicom_tag.xlsx`

**Actions:**
* Combines the two input files and groups by `PatientID`.
* Calculates `PatientAge` at the accession visit.
* Renames columns for consistency:
  * `PatientID` $\rightarrow$ `PATIENT_STUDY_ID`
  * `AccessionNumber` $\rightarrow$ `ACCESSION_NUMBER`
  * `PatientBirthDate` $\rightarrow$ `BIRTH_DATE`
* Adds standardized tags:
  * **Study:** `SCRRE`, `DIAG`
  * **Side:** `R`, `L`
  * **Series:** `DBT`, `IN2D`, `C VIEW`, `SECURE`
  * **View:** `MLO`, `CC`

### 2. Parameters Configuration (`parameters`)
* **Actions:** Lists all possible parameters in their respective files.

### 3. Interfile Duplicates Filter (`interfile_duplicates_<EHR>`)
Filters out duplicate records across different files for specific EHR sources.

* **Inputs:**
  * `P:/Dataset/R3Data/Cancer/<EHR>`
  * `P:/Dataset/MO-DBT-data-curation/parameters of interest.xlsx`
* **Outputs:**
  * `P:/Dataset/MO-DBT-data-curation/Cancer/Cleaned/<EHR>`

**Actions:**
* Focuses only on duplicates *between* files, ignoring duplicates *within* a single file.
* Only processes parameters listed in the "parameters of interest".

### 4. Patient Data IE Tagging (`patient_data_ie_tag`)
* **Actions:** Adds standardized tags to the data:
  * **Study:** `SCREEN`, `DIAG`

### 5. Cancer Cohort Extraction (`extract_cancer`)
Extracts the eligible MO cancer cohort based on the curated data.

* **Inputs:**
  * `P:/Dataset/MO-DBT-data-curation/dicom_tag.xlsx`
  * `P:/Dataset/MO-DBT-data-curation/Cancer/Cleaned/enteredit_findings.xlsx`
  * `P:/Dataset/MO-DBT-data-curation/Cancer/Cleaned/pathology.xlsx`
  * `P:/Dataset/MO-DBT-data-curation/Cancer/Cleaned/patient_data_ie_tag.xlsx`
* **Outputs:**
  * `P:/Dataset/MO-DBT-data-curation/Cancer/mo_cancer_cohort.xlsx`
  * `P:/Dataset/MO-DBT-data-curation/Cancer/mo_cancer_cohort_dbt.xlsx`

**Actions:**
* Locates `INDEX` and `INDEX-1` findings.
* Filters to extract the eligible MO cancer cohort.

### 6. MO Cancer Subtyping & Curation (`mo_cancer_subtype`)
Incorporates subtype information and prepares the cohort for final curation.

* **Inputs:**
  * `P:/Dataset/MO-DBT-data-curation/Cancer/mo_cancer_cohort.xlsx`
* **Intermediate Outputs:**
  * `P:/Dataset/MO-DBT-data-curation/Cancer/mo_cancer_cohort_subtype.xlsx`
  * `P:/Dataset/MO-DBT-data-curation/Cancer/mo_cancer_cohort_index_1.xlsx`
  * `P:/Dataset/MO-DBT-data-curation/Cancer/mo_cancer_cohort_index.xlsx`
* **Outputs:**
  * `P:/Dataset/MO-DBT-data-curation/Cancer/mo_cancer_cohort_focus.xlsx`

**Actions:**
* Incorporates cancer subtype information.
* Splits the dataset into `index_1` and `index` files for targeted curation.
  * Incorporates EHR data into the `index_1` file.
* Merges the curated files for `index_1` and `index` into the final dataset.

### 7. File Movement (`move_files`)
Handles the transferring of processed files to target directories.

* **Inputs:**
  * `P:/Dataset/MO-DBT-data-curation/Cancer/mo_cancer_cohort_focus.xlsx` (source path)
* **Outputs:**
  * `P:/Dataset/MO-DBT-data-curation/Cancer/mo_cancer_cohort_focus.xlsx` (target path)

**Actions:**
* Moves files from the source path to the designated target path.