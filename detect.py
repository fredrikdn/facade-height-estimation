import argparse
import time
from sys import platform
import torch
import time

from models import *
from datasets import *
from myutils import *
from torch_utils import *


def detect(
        cfg='./cfg/yolov3-3classes.cfg',
        data_cfg='./data/vgidata.data',
        weights='./weights/windorbal/windorbal.pt',
        images='testimg/',
        output='output',  # output folder
        img_size=1024,
        conf_thres=0.1,
        nms_thres=0.3,
        save_txt=True,
        save_images=True,
        webcam=False
):
    # device = torch_utils.select_device()
    device = select_device()
    # if os.path.exists(output):
    #     shutil.rmtree(output)  # delete output folder

    if not os.path.exists(output):
        os.makedirs(output)  # make new output folder

    # Initialize model
    model = Darknet(cfg, img_size)

    # Load weights
    if weights.endswith('.pt'):  # pytorch format
        model.load_state_dict(torch.load(weights, map_location=device)['model'])
    else:  # darknet format
        _ = load_darknet_weights(model, weights)

    model.to(device).eval()

    # Set Dataloader
    vid_path, vid_writer = None, None
    if webcam:
        save_images = False
        dataloader = LoadWebcam(img_size=img_size)
    else:
        dataloader = LoadImages(images, img_size=img_size)

    # Get classes and colors
    classes = load_classes(parse_data_cfg(data_cfg)['names'])
    #colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(classes))]
    colors = [[255, 0, 0], [0, 255, 0], [0, 0, 255]]  # red: balcony; green: door; blue: window

    for i, (path, img, im0, vid_cap) in enumerate(dataloader):
        t = time.time()
        save_path = str(Path(output) / Path(path).name)

        # Get detections
        img = torch.from_numpy(img).unsqueeze(0).to(device)
        if ONNX_EXPORT:
            torch.onnx.export(model, img, 'weights/model.onnx', verbose=True)
            return
        pred, _ = model(img)
        detections = non_max_suppression(pred, conf_thres, nms_thres)[0]

        if detections is not None and len(detections) > 0:
            # Rescale boxes from 416 to true image size
            scale_coords(img_size, detections[:, :4], im0.shape).round()

            # Print results to screen
            for c in detections[:, -1].unique():
                n = (detections[:, -1] == c).sum()
                print('%g %ss' % (n, classes[int(c)]), end=', ')

            # COORDS: xy xy class confidence (X:WIDTH, Y:HEIGHT)
            # Draw bounding boxes and labels of detections

            # DIVIDE EACH RUN
            if save_txt:
                with open(save_path + '.txt', 'a') as file:
                    file.truncate(0)
            for *xyxy, conf, cls_conf, cls in detections:
                if save_txt:  # Write to file
                    with open(save_path + '.txt', 'a') as file:
                        file.write(('%g ' * 6 + '\n') % (*xyxy, cls, conf))

# TODO: Fix window in window ... bounding box problem
                # Add bbox to the image
                label = '% s %.2f' % (classes[int(cls)], conf)
                plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=2)

        print('Done. (%.3fs)' % (time.time() - t))

# TODO: Draw bounding box on images
        if webcam:  # Show live webcam?
            cv2.imshow(weights, im0)

        if save_images:  # Save generated image with detections
            if dataloader.mode == 'video':
                if vid_path != save_path:  # new video
                    vid_path = save_path
                    if isinstance(vid_writer, cv2.VideoWriter):
                        vid_writer.release()  # release previous video writer
                    width = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    fps = vid_cap.get(cv2.CAP_PROP_FPS)
                    vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'avc1'), fps, (width, height))
                vid_writer.write(im0)

            else:
                cv2.imwrite(save_path, im0)

    if save_images and platform == 'darwin':  # macos
        os.system('open ' + output + ' ' + save_path)


if __name__ == '__main__':
    start_time = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('--cfg', type=str, default='cfg/yolov3-3classes.cfg', help='cfg file path')
    parser.add_argument('--data-cfg', type=str, default='data/vgidata.data', help='coco.data file path')
    parser.add_argument('--weights', type=str, default='weights/windorbal/windorbal.pt', help='path to weights file')
    parser.add_argument('--images', type=str, default='testimg/', help='path to images')
    parser.add_argument('--output', type=str, default='output/', help='path to output folder')
    parser.add_argument('--img-size', type=int, default=1024, help='size of each image dimension')
    parser.add_argument('--conf-thres', type=float, default=0.1, help='object confidence threshold')
    parser.add_argument('--nms-thres', type=float, default=0.5, help='iou threshold for non-maximum suppression')
    opt = parser.parse_args()
    print(opt)

    with torch.no_grad():
        detect(
            opt.cfg,
            opt.data_cfg,
            opt.weights,
            opt.images,
            img_size=opt.img_size,
            conf_thres=opt.conf_thres,
            nms_thres=opt.nms_thres
        )

    # with torch.no_grad():
    #     detect(images='./testimg',
    #            output='./output')

print("--- %s seconds ---" % (time.time() - start_time))