# PPE Detection using yolo3 and DeepSORT

## Introduction
In Industry, specially manufacturing industry, Personal Protective Equipment (PPE) like helmet (hard-hat), safety-harness, goggles etc play a very important role in ensuring the safety of workers. However, many accidents still occur, due to the negligence of the workers as well as their supervisors. Supervisors can make mistakes due to the fact that such tasks are monotonous and they may not be able to monitor consistently. This project aims to utilize existing CCTV camera infrastructure to assist supervisors to monitor workers effectively by providing them with real time alerts.

## Functioning
* Input is taken from CCTV cameras
* YOLO is used for detecting persons with proper PPE and those without PPE.
* Deep_SORT allocates unique ids to detected persons and tracks them through consecutive frames of the video.
* An alert is raised if a person is found to be without proper PPE for more than some set duration, say 5 seconds.

![img1](https://github.com/AnshulSood11/PPE-Detection-YOLO-Deep_SORT/blob/master/ppe-demo-images/img1.png)
It detects persons without helmet and displays the number of persons with helmet and
those without helmet. It sends notification in the message box for each camera. There is global
message box, where alerts from all cameras are displayed.

![img2](https://github.com/AnshulSood11/PPE-Detection-YOLO-Deep_SORT/blob/master/ppe-demo-images/img2.png)
It detects that the same person about which it had warned earlier has now worn a
helmet and notifies that also.

![img3](https://github.com/AnshulSood11/PPE-Detection-YOLO-Deep_SORT/blob/master/ppe-demo-images/img3.png)

Please note that this is still a work under progress and new ideas and contributions are welcome.
* Currently, the model is trained to detect helmets (hard-hat) only. I have plans to train the model for other PPEs as well.
* Currently, only usb cameras are supported. Support for other cameras needs to be added.
* The tracker needs to be made robust.
* Integrate service (via mobile app or SMS) to send real-time notifications to supervisors present on the field.

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
## Training the model

### 1. Data preparation

**Data Collection**

The dataset containing images of people wearing helmets and people without helmets were collected mostly from google search. Some images have people applauding, those were collected from Stanford 40 Action Dataset. Download images for training from [train_image_folder](https://drive.google.com/drive/folders/1b5ocFK8Z_plni0JL4gVhs3383V7Q9EYH?usp=sharing).

**Annotations**

Annotaion of each image was done in Pascal VOC format using the awesome lightweight annotation tool [LabelImg](https://github.com/tzutalin/labelImg) for object-detection. Download annotations from [train_annot_folder](https://drive.google.com/drive/folders/1u_s_kxq0x_fqtqgJn9nKC92ikrThMDru?usp=sharing).

**Organize the dataset into 4 folders:**
* train_image_folder <= the folder that contains the train images.
* train_annot_folder <= the folder that contains the train annotations in VOC format.
* valid_image_folder <= the folder that contains the validation images.
* valid_annot_folder <= the folder that contains the validation annotations in VOC format.

There is a one-to-one correspondence by file name between images and annotations. If the validation set is empty, the training set will be automatically splitted into the training set and validation set using the ratio of 0.8.

### 2. Edit the configuration file

The configuration file is a json file, which looks like this:
```
{
  "model" : {
    "min_input_size":       288,
    "max_input_size":       448,
    "anchors":              [33,34, 52,218, 55,67, 92,306, 96,88, 118,158, 153,347, 209,182, 266,359],
    "labels":               ["helmet","person with helmet","person without helmet"]
  },

  "train": {
    "train_image_folder":   "train_image_folder/",
    "train_annot_folder":   "train_annot_folder/",
    "cache_name":           "helmet_train.pkl",

    "train_times":          8,
    "batch_size":           8,
    "learning_rate":        1e-4,
    "nb_epochs":            100,
    "warmup_epochs":        3,
    "ignore_thresh":        0.5,
    "gpus":                 "0,1",

    "grid_scales":          [1,1,1],
    "obj_scale":            5,
    "noobj_scale":          1,
    "xywh_scale":           1,


    "tensorboard_dir":      "logs",
    "saved_weights_name":   "full_yolo3_helmet_and_person.h5",
    "debug":                true
  },

  "valid": {
    "valid_image_folder":   "",
    "valid_annot_folder":   "",
    "cache_name":           "",

    "valid_times":          1
  }
}
```
The model section defines the type of the model to construct as well as other parameters of the model such as the input image size and the list of anchors. The `labels` setting lists the labels to be trained on. Only images, which has labels being listed, are fed to the network. The rest images are simply ignored. By this way, a Dog Detector can easily be trained using VOC or COCO dataset by setting `labels` to `['dog']`.

Download pretrained weights for backend at:
[backend.h5](https://1drv.ms/u/s!ArJHK_Eldk0Cg3nUkkHZcS7btEGb?e=BlFGvM)

**These weights must be put in the root folder of the repository. They are the pretrained weights for the backend only and will be loaded during model creation. The code does not work without these weights.**

### 3. Generate anchors for your dataset (optional)

`python gen_anchors.py -c config.json`

Copy the generated anchors printed on the terminal to the `anchors` setting in `config.json`.

### 4. Start the training process

`python train.py -c config.json`

By the end of this process, the code will write the weights of the best model to file best_weights.h5 (or whatever name specified in the setting "saved_weights_name" in the config.json file). The training process stops when the loss on the validation set is not improved in 3 consecutive epoches.
 
 ### 5. Perform detection using trained weights on live feed from webcam
 
  To run the code with gui :
```bash
python predict_gui.py -c config.json -n <number of cameras>
```
  Note that the gui supports only upto 2 cameras.

  To run the code without gui :
```bash
python predict.py -c config.json -n <number of cameras>
```
  Here you can enter any number of cameras you want to use.

## Acknowledgements

* [rekon/keras-yolo2](https://github.com/rekon/keras-yolo2) for training data.
* [experiencor/keras-yolo3](https://github.com/experiencor/keras-yolo3) for YOLO v3 implementation.
* [nwojke/deep_sort](https://github.com/nwojke/deep_sort) for Deep_SORT implementation.
