# from data_processing.anonymization import (
#     anonymize,
# )
from data_processing.anonymization.anonymize import anonymize
import hydra


@hydra.main(version_base=None, config_path="D:/NECTEC/Code/Processing_PDF/Check_PDPA_Data/data-processing/scripts/anonymization/config", config_name="D:/NECTEC/Code/Processing_PDF/Check_PDPA_Data/data-processing/scripts/anonymization/config/blind_pdpa.yaml")
def main(cfg):
    anonymize(cfg.train_dataset, cfg.blind_config)


if __name__ == "__main__":
    main()  # type: ignore
