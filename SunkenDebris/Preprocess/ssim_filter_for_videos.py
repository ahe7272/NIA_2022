import cv2
import copy
from skimage.metrics import structural_similarity as ssim


def getSimilarity(img1, img2):
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    crop1 = gray1[int(gray1.shape[0] * 0.25):int(gray1.shape[0] * 0.75), int(gray1.shape[1] * 0.25):int(gray1.shape[1] * 0.75)]
    crop2 = gray2[int(gray1.shape[0] * 0.25):int(gray1.shape[0] * 0.75), int(gray1.shape[1] * 0.25):int(gray1.shape[1] * 0.75)]

    (score, _) = ssim(crop1, crop2, full=True)
    # (score, _) = ssim(gray1, gray2, full=True)

    return score


class Video:
    def __init__(self, VideoPath):
        self.VideoPath = VideoPath
        self.Threshold = 0.5

    def saveFrame(self):
        cap = cv2.VideoCapture(self.VideoPath)

        nFrame = 1
        Memory = None
        NoteMemory = None
        while True:
            ret, frame = cap.read()
            if not(ret):
                pass
            else:
                if nFrame == 1:
                    Memory = copy.deepcopy(frame)
                    NoteMemory = nFrame
                    cv2.imwrite(filename='Test_' + str(nFrame) + '.jpg', img=Memory)
                    nFrame += 1
                elif nFrame > 1 and nFrame % 10 == 0:
                    newFrame = copy.deepcopy(frame)
                    sim = getSimilarity(Memory, newFrame)
                    print(nFrame, sim, NoteMemory)
                    if sim <= self.Threshold:
                        cv2.imwrite(filename='Test_' + str(nFrame) + '.jpg', img=newFrame)
                        # cv2.imwrite(filename='Test_' + str(nFrame) + '_memory.jpg', img=Memory)
                        Memory = copy.deepcopy(frame)
                        NoteMemory = nFrame
                        nFrame += 1
                    else:
                        nFrame += 1
                        pass
                else:
                    nFrame += 1


def main():
    vid = Video('C:/Users/Administrator/Desktop/Original/GH010092.MP4')
    vid.saveFrame()


if __name__ == '__main__':
    main()
