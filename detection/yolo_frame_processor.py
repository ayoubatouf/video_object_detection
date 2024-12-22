from processing.frame_processor import FrameProcessor
import cv2
import numpy as np


class YOLOFrameProcessor(FrameProcessor):
    def __init__(
        self,
        model,
        class_names,
        confidence_threshold=0.5,
        high_confidence_threshold=0.9,
    ):
        self.model = model
        self.class_names = class_names
        self.confidence_threshold = confidence_threshold
        self.high_confidence_threshold = high_confidence_threshold

    def process(self, frame):
        results = self.model.predict(frame, device="cuda", verbose=False)
        result = results[0]

        bboxes = np.array(result.boxes.xyxy.cpu(), dtype="int")
        classes = np.array(result.boxes.cls.cpu(), dtype="int")
        confidences = np.array(result.boxes.conf.cpu(), dtype="float")

        object_classes = set()
        confident_detections = 0
        high_confidence_classes = {}

        for cls, bbox, conf in zip(classes, bboxes, confidences):
            if conf < self.confidence_threshold:
                continue

            object_classes.add(self.class_names[cls])
            if conf > 0.5:
                confident_detections += 1

            if conf > self.high_confidence_threshold:
                object_name = self.class_names[cls]
                if object_name in high_confidence_classes:
                    high_confidence_classes[object_name] += 1
                else:
                    high_confidence_classes[object_name] = 1

            (x, y, x2, y2) = bbox
            object_name = self.class_names[cls]
            box_color = self._get_box_color(conf)
            cv2.rectangle(frame, (x, y), (x2, y2), box_color, 2)
            cv2.putText(
                frame,
                f"{object_name}: {conf:.2f}",
                (x, y - 5),
                cv2.FONT_HERSHEY_PLAIN,
                2,
                box_color,
                2,
            )

        return frame, len(bboxes), high_confidence_classes, confident_detections

    def _get_box_color(self, conf):
        if conf > 0.6:
            return (37, 245, 75)
        elif 0.3 < conf <= 0.6:
            return (66, 224, 245)
        else:
            return (78, 66, 245)
