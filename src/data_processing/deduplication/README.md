# Deduplication Pipeline

## Description

The Deduplication Pipeline is designed to remove duplicated entries from the Huggingface datasets. By using the techniques similar to this [paper](https://arxiv.org/abs/2107.06499), the pipeline uses the N-Gram MinHash approach in combination with LSH (Locality-Sensitive Hashing) to identify and eliminate duplicate content.

![deduplication_diagram](deduplication_diagram.png)

## Preparation
wget https://raw.githubusercontent.com/PyThaiNLP/pythainlp/dev/pythainlp/corpus/words_th.txt -P src/data_processing/deduplication

## How to use
For details, see [How to use guide](../../../src/scripts/deduplication/README.md).