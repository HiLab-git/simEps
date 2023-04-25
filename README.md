# Semi-Supervised Defect Segmentation with Pairwise Similarity Map Consistency and Ensemble-Based Cross-Pseudo Labels (simEps)
In this study, we propose a novel method based on pairwise similarity map consistency with ensemble-based cross-pseudo labels for semisupervised defect segmentation that uses limited labeled samples while exploiting additional label-free samples. The proposed approach uses three network branches that are regularized by pairwise similarity map consistency, and each of them is supervised by the pseudo labels generated by ensemble of predictions of the other two networks for the unlabeled samples. The proposed method achieved significant performance improvement over the baseline of learning only from the labeled images and the current stateof-the-art semi-supervised methods.
## Python >= 3.6
PyTorch >= 1.1.0
PyYAML, tqdm, tensorboardX
## Data Preparation
Download datasets. There are 3 datasets to download:
*NEU-SEG dataset
*DAGM dataset
*MT (Magnetic Tiles) dataset

Put downloaded data into the following directory structure:
data/
    NEU-Seg/ ... # raw data of NEU-Seg
    DAGM/ ...# raw data of DAGM
    MT/ ...# raw data of MTiles
## Data loading and preparation 
