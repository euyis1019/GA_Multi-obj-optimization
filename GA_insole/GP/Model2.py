#!/usr/bin/env python
# coding: utf-8

import time
import cv2
import torch
from skvideo.io import vreader, FFmpegWriter
from ais_bench.infer.interface import InferSession

from det_utils import letterbox, scale_coords, nms


def preprocess_image(image, cfg, bgr2rgb=True):
    img, scale_ratio, pad_size = letterbox(image, new_shape=cfg['input_shape'])
    if bgr2rgb:
        img = img[:, :, ::-1]
    img = img.transpose(2, 0, 1)  # HWC2CHW
    return img, scale_ratio, pad_size


def draw_bbox(bbox, img0, color, wt, names):
    det_result_str = ''
    for idx, class_id in enumerate(bbox[:, 5]):
        if float(bbox[idx][4] < float(0.05)):
            continue
        img0 = cv2.rectangle(img0, (int(bbox[idx][0]), int(bbox[idx][1])), (int(bbox[idx][2]), int(bbox[idx][3])),
                             color, wt)
        img0 = cv2.putText(img0, str(idx) + ' ' + names[int(class_id)], (int(bbox[idx][0]), int(bbox[idx][1] + 16)),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        img0 = cv2.putText(img0, '{:.4f}'.format(bbox[idx][4]), (int(bbox[idx][0]), int(bbox[idx][1] + 32)),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        det_result_str += '{} {} {} {} {} {}\n'.format(
            names[bbox[idx][5]], str(bbox[idx][4]), bbox[idx][0], bbox[idx][1], bbox[idx][2], bbox[idx][3])
    return img0


def get_labels_from_txt(path):
    labels_dict = dict()
    with open(path) as f:
        for cat_id, label in enumerate(f.readlines()):
            labels_dict[cat_id] = label.strip()
    return labels_dict


def draw_prediction(pred, image, labels):
    img_dw = draw_bbox(pred, image, (0, 255, 0), 2, labels)
    cv2.imshow('result', img_dw)


def infer_image(img_path, model, class_names, cfg):
    image = cv2.imread(img_path)
    img, scale_ratio, pad_size = preprocess_image(image, cfg)
    output = model.infer([img])[0]

    output = torch.tensor(output)
    boxout = nms(output, conf_thres=cfg["conf_thres"], iou_thres=cfg["iou_thres"])
    pred_all = boxout[0].numpy()
    scale_coords(cfg['input_shape'], pred_all[:, :4], image.shape, ratio_pad=(scale_ratio, pad_size))
    draw_prediction(pred_all, image, class_names)


def infer_frame_with_vis(image, model, labels_dict, cfg, bgr2rgb=True):
    img, scale_ratio, pad_size = preprocess_image(image, cfg, bgr2rgb)
    output = model.infer([img])[0]

    output = torch.tensor(output)
    boxout = nms(output, conf_thres=cfg["conf_thres"], iou_thres=cfg["iou_thres"])
    pred_all = boxout[0].numpy()
    scale_coords(cfg['input_shape'], pred_all[:, :4], image.shape, ratio_pad=(scale_ratio, pad_size))
    img_vis = draw_bbox(pred_all, image, (0, 255, 0), 2, labels_dict)
    return img_vis


def img2bytes(image):
    return bytes(cv2.imencode('.jpg', image)[1])


def infer_video(video_path, model, labels_dict, cfg, output_path='output.mp4'):
    cap = vreader(video_path)
    video_writer = None
    for img_frame in cap:
        image_pred = infer_frame_with_vis(img_frame, model, labels_dict, cfg, bgr2rgb=False)
        cv2.imshow('result', image_pred)

        if video_writer is None:
            video_writer = FFmpegWriter(output_path)
        video_writer.writeFrame(image_pred)
    video_writer.close()


def infer_camera(model, labels_dict, cfg):
    cap = cv2.VideoCapture(0)
    while True:
        _, img_frame = cap.read()
        infer_start = time.time()
        image_pred = infer_frame_with_vis(img_frame, model, labels_dict, cfg)
        infer_time = time.time() - infer_start
        print(1 / infer_time)
        cv2.imshow('result', image_pred)
        cv2.waitKey(1)


cfg = {
    'conf_thres': 0.4,
    'iou_thres': 0.5,
    'input_shape': [640, 640],
}

model_path = 'om模型文件路径'
label_path = '标签文件路径'
model = InferSession(0, model_path)
labels_dict = get_labels_from_txt(label_path)


infer_mode = 'camera'

if infer_mode == 'image':
    img_path = 'world_cup.jpg'
    infer_image(img_path, model, labels_dict, cfg)
elif infer_mode == 'camera':
    infer_camera(model, labels_dict, cfg)
elif infer_mode == 'video':
    video_path = 'world_cup.mp4'
    infer_video(video_path, model, labels_dict, cfg, output_path='output.mp4')
