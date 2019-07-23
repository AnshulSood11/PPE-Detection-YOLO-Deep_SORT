# Helmet Detection and alert system using yolo3 and DeepSORT

## Installation

Using conda environment is recommended. Follow these steps to get the code running:

1. First, download the zip file.
2. Download the following files into the project directory:
[mars-small128.pb](https://1drv.ms/u/s!ArJHK_Eldk0Cg3jyt-NR3xPErr_5?e=88vcgg)
[full_yolo3_helmet_and_person.h5](https://1drv.ms/u/s!ArJHK_Eldk0Cg3cTEpkVoZyyxQzl?e=10MXuV)

3. Run the following command to create a conda environmnet:
```bash
 conda env create -f environment.yml
```
4. Activate the conda environment:
```bash
conda activate helmet-detection
```
5. To run the code with gui :
```bash
python predict_gui.py -c config.json -n <number of cameras>
```
  Note that the gui supports only upto 2 cameras.

  To run the code without gui :
```bash
python predict.py -c config.json -n <number of cameras>
```
  Here you can enter any number of cameras you want to use.
