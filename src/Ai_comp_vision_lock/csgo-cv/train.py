import cv2 as cv
from os import listdir
from os.path import isfile, join
import subprocess

target_name = "head"

# https://docs.opencv.org/4.5.4/dc/d88/tutorial_traincascade.html

def get_folder_files(folder):
    return [join(folder, f) for f in listdir(folder) if isfile(join(folder, f))]


print("Getting files...")
background_files = get_folder_files("./background")
positive_files = get_folder_files("./heads")

print("Generating pos and neg files")
# Generate negatives
f = open('neg.txt', 'w')
lines = []
for index, p in enumerate(background_files):
    end = '' if index == len(background_files) - 1 else '\n'
    lines.append(f"{p}{end}")
f.writelines(lines)
f.close()

# Generate positives
f = open('pos.txt', 'w')
lines = []
for index, p in enumerate(positive_files):
    h, w, _ = cv.imread(p).shape
    end = '' if index == len(positive_files) - 1 else '\n'
    line = f"{p} 1 0 0 {w} {h}{end}"
    lines.append(line)
f.writelines(lines)
f.close()

print("Creating samples...")
proc = subprocess.run(["opencv_createsamples",
                       "-info", "pos.txt",
                       "-w", "20",  # Detection window
                       "-h", "20",
                       "-num", str(len(positive_files) * 10),
                       "-vec", "pos.vec"
                       ])
if proc.returncode != 0:
    print("Error generating samples")
    raise RuntimeError()
print("Samples generated!")

print("Training Cascade")
proc = subprocess.run(["opencv_traincascade.exe",
                       "-data", "./" + target_name,
                       "-vec", "pos.vec",
                       "-bg", "neg.txt",
                       "-w", "20",  # Detection window
                       "-h", "20",
                       "-numPos", str(int(len(positive_files) - len(positive_files) * 0.2)), # Use 80% of positives
                       "-numNeg", str(len(background_files)),
                       "-numStages", "8",
                       # "-minHitRate", "0.995",
                       "-maxFalseAlarmRate", "0.3",
                       "-precalcValBufSize", "3000",
                       "-precalcIdxBufSize", "3000"
                       ])
if proc.returncode != 0:
    print("Error training model")
    raise RuntimeError()
print("Training complete!")
