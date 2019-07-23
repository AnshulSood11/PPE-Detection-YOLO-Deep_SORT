# Helmet Detection and alert system using yolo3 and DeepSORT

##Installation

Using conda environment is recommended. Follow these steps to get the code running:

1. First, clone the repository or download zip.

2. Go to the preject directory and run the following command to create a conda environmnet:
```bash
 conda env create -f environment.yml
```
3. Run:
```bash
conda activate helmet-detection
```
4. To run the code with gui :
```bash
python predict_with_tracker_multicam_gui.py -c config.json -n <number of cameras>
```
  Note that the gui supports only upto 2 cameras.

  Or, to run the code without gui :
```bash
python predict_with_tracker_multicam.py -c config.json -n <number of cameras>
```
  Here you can enter any number of cameras you want to use.
