(1) Installation
cd detect-facade-elements
sudo pip3 install -U -r requirements.txt


(2) Usage
python3 detect.py --cfg cfg/yolov3-3classes.cfg --data-cfg data/vgidata.data --weights weights/windorbal/windorbal.pt --images testimg/ --output output --img-size 1024 --conf-thres 0.1

Note:
"--images": path to test images folder
"--output": path to output folder

Credit: Gefei Kong, Wuhan University, China, Detection of Facade Elements (2020)
