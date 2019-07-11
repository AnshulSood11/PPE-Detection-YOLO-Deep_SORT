#! /usr/bin/env python

import os
import argparse
import json
import cv2
from utils.utils import get_yolo_boxes, makedirs
from utils.bbox import draw_boxes
from tensorflow.keras.models import load_model
from tqdm import tqdm
import numpy as np
from object_tracking.application_util import preprocessing
from object_tracking.deep_sort import nn_matching
from object_tracking.deep_sort.detection import Detection
from object_tracking.deep_sort.tracker import Tracker
from object_tracking.application_util import generate_detections as gdet
from utils.bbox import draw_box_with_id

import warnings
warnings.filterwarnings("ignore")

def _main_(args):
    config_path = args.conf
    num_cam = int(args.count)

    with open(config_path) as config_buffer:
        config = json.load(config_buffer)

    # makedirs(output_path)

    ###############################
    #   Set some parameter
    ###############################
    net_h, net_w = 416, 416  # a multiple of 32, the smaller the faster
    obj_thresh, nms_thresh = 0.5, 0.45

    ###############################
    #   Load the model
    ###############################
    os.environ['CUDA_VISIBLE_DEVICES'] = config['train']['gpus']
    infer_model = load_model(config['train']['saved_weights_name'])

    ###############################
    #   Set up the Tracker
    ###############################

    #   Definition of the parameters
    max_cosine_distance = 0.3
    nn_budget = None
    nms_max_overlap = 1.0

    # deep_sort
    model_filename = 'mars-small128.pb'
    encoder = gdet.create_box_encoder(model_filename, batch_size=1)

    metrics = []
    trackers = []
    for i in range(num_cam):
        metric = nn_matching.NearestNeighborDistanceMetric("cosine", max_cosine_distance, nn_budget)
        tracker = Tracker(metric)
        trackers.append(tracker)



    ###############################
    #   Predict bounding boxes
    ###############################
    # if 'webcam' in input_path:  # do detection on the first webcam
    video_readers = []
    for i in range(num_cam):
        video_reader = cv2.VideoCapture(i)
        video_readers.append(video_reader)

    # the main loop
    batch_size = num_cam
    images = []
    while True:
        for i in range(num_cam):
            ret_val, image = video_readers[i].read()
            if ret_val == True: images += [image]

        if (len(images) == batch_size) or (ret_val == False and len(images) > 0):

            batch_boxes = get_yolo_boxes(infer_model, images, net_h, net_w, config['model']['anchors'], obj_thresh,
                                         nms_thresh)

            for i in range(len(images)):
                boxs = [[box1.xmin,box1.ymin,box1.xmax-box1.xmin, box1.ymax-box1.ymin] for box1 in batch_boxes[i]]
                features = encoder(images[i], boxs)

                # print(features)
                # score to 1.0 here).
                detections = []
                for j in range(len(boxs)):
                    label = batch_boxes[i][j].label
                    detections.append(Detection(boxs[j], batch_boxes[i][j].c, features[j],label))

                # Call the tracker
                trackers[i].predict()
                trackers[i].update(detections)

                n_without_helmet = 0
                n_with_helmet = 0

                for track in trackers[i].tracks:
                    if not track.is_confirmed() or track.time_since_update > 1:
                        continue
                    if track.label == 2:
                        n_without_helmet += 1
                    if track.label == 1:
                        n_with_helmet += 1
                    bbox = track.to_tlbr()
                    # print(track.track_id,"+",track.label)
                    draw_box_with_id(images[i], bbox, track.track_id, track.label, config['model']['labels'])

                # for det in detections:
                #     print(det.label)
                #     bbox = det.to_tlbr()
                #     cv2.rectangle(images[i], (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (255, 0, 0), 2)
                
                print("CAM "+str(i))
                print("Persons without helmet = " + str(n_without_helmet))
                print("Persons with helmet = " + str(n_with_helmet))
                cv2.imshow('Cam'+str(i), images[i])
            images = []
        if cv2.waitKey(1) == 27:
            break  # esc to quit
    cv2.destroyAllWindows()

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Predict with a trained yolo model')
    argparser.add_argument('-c', '--conf', help='path to configuration file')
    argparser.add_argument('-n', '--count', help='number of cameras')

    args = argparser.parse_args()
    _main_(args)
