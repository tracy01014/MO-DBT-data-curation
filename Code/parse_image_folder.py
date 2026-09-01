import os
import pandas as pd

def parse_folder_structure(root_path):
    """
    Parse DICOM-like metadata from folder naming convention:
    Patient_{PatientID}/{StudyDate}/Study_{StudyDescription}_{AccessionNumber}/Series_{SeriesNumber}_{SeriesDescription}
    """
    records = []

    for patient_folder in os.listdir(root_path):
        if not patient_folder.startswith("Patient_"):
            continue
        patient_path = os.path.join(root_path, patient_folder)
        if not os.path.isdir(patient_path):
            continue

        patient_id = patient_folder[len("Patient_"):]

        for study_date_folder in os.listdir(patient_path):
            study_date_path = os.path.join(patient_path, study_date_folder)
            if not os.path.isdir(study_date_path):
                continue

            study_date = study_date_folder  # e.g., 20190819

            for study_folder in os.listdir(study_date_path):
                if not study_folder.startswith("Study_"):
                    continue
                study_path = os.path.join(study_date_path, study_folder)
                if not os.path.isdir(study_path):
                    continue

                # "Study_{StudyDescription}_{AccessionNumber}"
                # AccessionNumber is the last underscore-separated numeric token
                study_content = study_folder[len("Study_"):]
                parts = study_content.rsplit("_", 1)
                if len(parts) == 2 and parts[1].isdigit():
                    study_description = parts[0].replace("_", " ")
                    accession_number = parts[1]
                else:
                    study_description = study_content.replace("_", " ")
                    accession_number = None

                for series_folder in os.listdir(study_path):
                    if not series_folder.startswith("Series_"):
                        continue
                    series_path = os.path.join(study_path, series_folder)
                    if not os.path.isdir(series_path):
                        continue

                    # "Series_{SeriesNumber}_{SeriesDescription}"
                    # SeriesNumber is the first token after "Series_"
                    series_content = series_folder[len("Series_"):]
                    series_parts = series_content.split("_", 1)
                    series_number = series_parts[0]
                    series_description = series_parts[1].replace("_", " ") if len(series_parts) > 1 else ""

                    records.append({
                        "PatientID":         patient_id,
                        "StudyDate":         study_date,
                        "StudyDescription":  study_description,
                        "AccessionNumber":   accession_number,
                        "SeriesNumber":      series_number,
                        "SeriesDescription": series_description,
                        "FolderPath":        series_path,
                    })

    df = pd.DataFrame(records)
    df = df.sort_values(by=["PatientID", "StudyDate", "AccessionNumber", "SeriesNumber"],
                        ignore_index=True)
    return df


# Usage
root_path = r"J:\Testing\jlee\MO_DBT\DICOM_data_and_summaries_882GB"
df_folders = parse_folder_structure(root_path)
df_folders.to_excel("P:/Dataset/R01-MO-DBT/MO-DBT-data-curation/R3Data/dicomtocsv_series_20250527.xlsx", index=False)