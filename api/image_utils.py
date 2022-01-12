import cv2
import numpy as np

def clean_image(img, alpha=2.2, beta=-160, quality=60):
    raw_image = cv2.imdecode(np.fromstring(img.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    cleaned_image = np.clip(alpha * raw_image + beta, 0, 255).astype(np.uint8)

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    _, image_buffer = cv2.imencode(".jpg", cleaned_image, encode_param)

    processed_image = SimpleUploadedFile(
        str(datetime.now()) + ".jpg", BytesIO(image_buffer).getvalue()
    )

    return processed_image