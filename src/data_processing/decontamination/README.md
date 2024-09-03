# Decontamination Pipeline

## Description

The Decontamination Pieline is designed to combat leaking of training dataset into evaluation process. The goal of this pipeline is to identify and remove potentially duplicated documents used in evlaution process from pretraining dataset.
This contamination check is based on N-Gram MinHash and LSH (Locality-Sensitive Hashing) techniques inspired by the methods presented in this .

![deduplication_diagram](decontaminate_diagram.png)

## How to use
For details, see [How to use guide](src/scripts/decontamination/README.md).