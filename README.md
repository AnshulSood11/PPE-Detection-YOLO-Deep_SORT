# Helmet Detection and alert system using yolo3 and DeepSORT

## Introduction
In Industry, specially manufacturing industry, Personal Protective Equipment (hereon abbreviated as
PPE) like helmet (hard-hat), safety-harness, goggles etc play a very important role in ensuring the
safety of workers. However, many accidents still occur, due to the negligence of the workers as well
as their supervisors. Supervisors can make mistakes due to the fact that such tasks are monotonous
and they may not be able to monitor consistently. This project aims to assist the supervisors to monitor
effectively by providing them with real time alerts.
### Infrastructure required:
1. The project utilizes existing CCTV camera infrastructure and no modification in
cameras is required.
2. Powerful enough computer(preferable with GPU) to process camera feed at good frame rate.
### Functioning
* Input is taken from CCTV cameras
* YOLO3 is used for detecting persons with proper PPE and those without PPE.
* Deep_SORT allocates unique ids to detected persons and tracks the persons through consecutive frames of the video.
* An alert is raised if a person is found to be without proper PPE for more than some set
duration, say 5 seconds.
![img1](https://drive.google.com/uc?export=view&id=1-uozV5f_CqtF0wnEZnIBfZsOoqbSfQyN)
It detects persons without helmet and displays the number of persons with helmet and
those without helmet. It sends notification in the message box for each camera. There is global
message box, where alerts from all cameras are displayed.
![img2](https://drive.google.com/uc?export=view&id=1L0aQLGMMzMG3j2dVw0LV3bjkd4bGTeOp)
It detects that the same person about which it had warned earlier has now worn a
helmet and notifies that also.
![img3](https://drive.google.com/uc?export=view&id=1l8VUS9GjKMmOsOTzQv-FZ2rm7_Ho9gM4)
### Further Plans
Please note that this is still a work under progress and new ideas and contributions are welcome.
1. Currently, the model has been trained to detect helmets (hard-hat) only. There are plans to train the model for other PPEs as well.
2. Integrate service (via mobile app or SMS) to send real-time notifications to supervisors present on the field.
3. The tracker needs to be made robust.

## Quick Start
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
