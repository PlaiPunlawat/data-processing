from data_processing.anonymization import (
    anonymize,
)

import hydra


@hydra.main(version_base=None, config_path="./config", config_name="blind_pdpa")
def main(cfg):
    anonymize(cfg.train_dataset, cfg.blind_config)


if __name__ == "__main__":
    main()  # type: ignore
