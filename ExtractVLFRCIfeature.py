"""
=============================================================
Web Screenshot Feature Benchmark
=============================================================

Purpose:
    Extract representative visual features used in previous
    website/UI screenshot research and compare them against
    the proposed VLF + RCI features.

Feature families
----------------
1. Color statistics
2. HSV statistics
3. Spatial color grid
4. HOG
5. LBP
6. SIFT
7. ORB
8. Edge / gradient structural features
9. Grid spatial features
10. OCR layout features (optional)
11. Deep CNN embedding (ResNet50, optional)
12. Proposed VLF
13. Proposed RCI

Output:
    One flat feature dictionary suitable for:
        - CSV
        - pandas DataFrame
        - ML models
        - ablation studies
        - statistical comparison
=============================================================
"""

import os
import cv2
import numpy as np

from PIL import Image

from skimage.feature import hog, local_binary_pattern
from skimage.color import rgb2gray
from skimage.transform import resize

from skimage.metrics import structural_similarity as ssim


# ============================================================
# OPTIONAL LIBRARIES
# ============================================================

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False


try:
    import torch
    import torchvision
    from torchvision.models import resnet50, ResNet50_Weights

    TORCH_AVAILABLE = True

except ImportError:
    TORCH_AVAILABLE = False


# ============================================================
# BASIC IMAGE LOADING
# ============================================================

def load_image(image_path):

    img = cv2.imread(image_path)

    if img is None:
        raise ValueError(
            f"Cannot load image: {image_path}"
        )

    return img


# ============================================================
# 1. COLOR FEATURES
# ============================================================

def extract_color_features(img):

    rgb = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2RGB
    )

    hsv = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2HSV
    )

    features = {}

    # --------------------------------------------------------
    # RGB statistics
    # --------------------------------------------------------

    channels = {
        "R": rgb[:, :, 0],
        "G": rgb[:, :, 1],
        "B": rgb[:, :, 2]
    }

    for name, channel in channels.items():

        features[f"color_mean_{name}"] = float(
            np.mean(channel) / 255.0
        )

        features[f"color_std_{name}"] = float(
            np.std(channel) / 255.0
        )

    # --------------------------------------------------------
    # HSV statistics
    # --------------------------------------------------------

    H = hsv[:, :, 0] / 179.0
    S = hsv[:, :, 1] / 255.0
    V = hsv[:, :, 2] / 255.0

    features["hue_mean"] = float(np.mean(H))
    features["hue_std"] = float(np.std(H))

    features["saturation_mean"] = float(np.mean(S))
    features["saturation_std"] = float(np.std(S))

    features["value_mean"] = float(np.mean(V))
    features["value_std"] = float(np.std(V))

    # --------------------------------------------------------
    # Bright / dark pixel ratio
    # --------------------------------------------------------

    features["bright_ratio"] = float(
        np.mean(V > 0.85)
    )

    features["dark_ratio"] = float(
        np.mean(V < 0.20)
    )

    return features


# ============================================================
# 2. COLOR HISTOGRAM
# ============================================================

def extract_color_histogram(
        img,
        bins=16):

    rgb = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2RGB
    )

    features = {}

    for c, name in enumerate(
        ["R", "G", "B"]
    ):

        hist = cv2.calcHist(
            [rgb],
            [c],
            None,
            [bins],
            [0, 256]
        )

        hist = cv2.normalize(
            hist,
            hist
        ).flatten()

        for i, value in enumerate(hist):

            features[
                f"rgb_hist_{name}_{i}"
            ] = float(value)

    return features


# ============================================================
# 3. SPATIAL COLOR GRID
# ============================================================

def extract_spatial_color_features(
        img,
        grid_size=4):

    rgb = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2RGB
    )

    h, w = rgb.shape[:2]

    features = {}

    cell_h = h // grid_size
    cell_w = w // grid_size

    index = 0

    for row in range(grid_size):

        for col in range(grid_size):

            y1 = row * cell_h
            y2 = (
                (row + 1) * cell_h
                if row < grid_size - 1
                else h
            )

            x1 = col * cell_w
            x2 = (
                (col + 1) * cell_w
                if col < grid_size - 1
                else w
            )

            region = rgb[
                y1:y2,
                x1:x2
            ]

            for c, name in enumerate(
                ["R", "G", "B"]
            ):

                features[
                    f"grid_{index}_{name}_mean"
                ] = float(
                    np.mean(region[:, :, c])
                    / 255.0
                )

                features[
                    f"grid_{index}_{name}_std"
                ] = float(
                    np.std(region[:, :, c])
                    / 255.0
                )

            index += 1

    return features


# ============================================================
# 4. HOG FEATURES
# ============================================================

def extract_hog_features(
        img,
        orientations=9,
        pixels_per_cell=(16, 16),
        cells_per_block=(2, 2)):

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    gray = resize(
        gray,
        (512, 512)
    )

    descriptor = hog(
        gray,
        orientations=orientations,
        pixels_per_cell=pixels_per_cell,
        cells_per_block=cells_per_block,
        block_norm="L2-Hys"
    )

    return {
        f"hog_{i}": float(v)
        for i, v in enumerate(descriptor)
    }


# ============================================================
# 5. LBP TEXTURE
# ============================================================

def extract_lbp_features(
        img,
        radius=2,
        points=16):

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    lbp = local_binary_pattern(
        gray,
        points,
        radius,
        method="uniform"
    )

    n_bins = points + 2

    histogram, _ = np.histogram(
        lbp.ravel(),
        bins=n_bins,
        range=(0, n_bins)
    )

    histogram = (
        histogram.astype(np.float32)
        / histogram.sum()
    )

    return {
        f"lbp_{i}": float(v)
        for i, v in enumerate(histogram)
    }


# ============================================================
# 6. SIFT KEYPOINT FEATURES
# ============================================================

def extract_sift_features(
        img,
        max_features=200):

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    try:

        sift = cv2.SIFT_create(
            nfeatures=max_features
        )

    except Exception:

        return {
            "sift_num_keypoints": 0.0,
            "sift_mean_response": 0.0,
            "sift_mean_size": 0.0,
            "sift_mean_angle": 0.0
        }

    keypoints, descriptors = \
        sift.detectAndCompute(
            gray,
            None
        )

    if keypoints is None:

        return {
            "sift_num_keypoints": 0.0,
            "sift_mean_response": 0.0,
            "sift_mean_size": 0.0,
            "sift_mean_angle": 0.0
        }

    responses = [
        kp.response
        for kp in keypoints
    ]

    sizes = [
        kp.size
        for kp in keypoints
    ]

    angles = [
        kp.angle / 360.0
        for kp in keypoints
        if kp.angle >= 0
    ]

    return {

        "sift_num_keypoints":
            float(len(keypoints)),

        "sift_mean_response":
            float(np.mean(responses)),

        "sift_mean_size":
            float(np.mean(sizes)),

        "sift_mean_angle":
            float(
                np.mean(angles)
                if angles
                else 0
            )
    }


# ============================================================
# 7. ORB FEATURES
# ============================================================

def extract_orb_features(
        img,
        max_features=500):

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    orb = cv2.ORB_create(
        nfeatures=max_features
    )

    keypoints, descriptors = \
        orb.detectAndCompute(
            gray,
            None
        )

    if keypoints is None:

        return {
            "orb_num_keypoints": 0.0,
            "orb_mean_response": 0.0,
            "orb_mean_size": 0.0
        }

    return {

        "orb_num_keypoints":
            float(len(keypoints)),

        "orb_mean_response":
            float(
                np.mean([
                    kp.response
                    for kp in keypoints
                ])
            ),

        "orb_mean_size":
            float(
                np.mean([
                    kp.size
                    for kp in keypoints
                ])
            )
    }


# ============================================================
# 8. STRUCTURAL / EDGE FEATURES
# ============================================================

def extract_structural_features(img):

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    blur = cv2.GaussianBlur(
        gray,
        (5, 5),
        0
    )

    edges = cv2.Canny(
        blur,
        50,
        150
    )

    h, w = gray.shape

    features = {}

    # --------------------------------------------------------
    # Edge density
    # --------------------------------------------------------

    features["edge_density"] = float(
        np.mean(edges > 0)
    )

    # --------------------------------------------------------
    # Horizontal / vertical edge density
    # --------------------------------------------------------

    horizontal = cv2.Sobel(
        gray,
        cv2.CV_64F,
        1,
        0,
        ksize=3
    )

    vertical = cv2.Sobel(
        gray,
        cv2.CV_64F,
        0,
        1,
        ksize=3
    )

    features["horizontal_gradient"] = float(
        np.mean(np.abs(horizontal))
        / 255.0
    )

    features["vertical_gradient"] = float(
        np.mean(np.abs(vertical))
        / 255.0
    )

    # --------------------------------------------------------
    # Horizontal / vertical projection
    # --------------------------------------------------------

    horizontal_projection = np.mean(
        edges > 0,
        axis=1
    )

    vertical_projection = np.mean(
        edges > 0,
        axis=0
    )

    features["horizontal_projection_mean"] = float(
        np.mean(horizontal_projection)
    )

    features["horizontal_projection_std"] = float(
        np.std(horizontal_projection)
    )

    features["vertical_projection_mean"] = float(
        np.mean(vertical_projection)
    )

    features["vertical_projection_std"] = float(
        np.std(vertical_projection)
    )

    # --------------------------------------------------------
    # 3 horizontal regions
    # --------------------------------------------------------

    top = edges[:h // 3]
    middle = edges[h // 3:2 * h // 3]
    bottom = edges[2 * h // 3:]

    features["edge_top_density"] = float(
        np.mean(top > 0)
    )

    features["edge_middle_density"] = float(
        np.mean(middle > 0)
    )

    features["edge_bottom_density"] = float(
        np.mean(bottom > 0)
    )

    return features


# ============================================================
# 9. GRID STRUCTURAL FEATURES
# ============================================================

def extract_grid_structure(
        img,
        grid_size=4):

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    edges = cv2.Canny(
        gray,
        50,
        150
    )

    h, w = edges.shape

    features = {}

    cell_h = h // grid_size
    cell_w = w // grid_size

    index = 0

    for row in range(grid_size):

        for col in range(grid_size):

            y1 = row * cell_h
            y2 = (
                (row + 1) * cell_h
                if row < grid_size - 1
                else h
            )

            x1 = col * cell_w
            x2 = (
                (col + 1) * cell_w
                if col < grid_size - 1
                else w
            )

            region = edges[
                y1:y2,
                x1:x2
            ]

            features[
                f"struct_grid_{index}_edge_density"
            ] = float(
                np.mean(region > 0)
            )

            index += 1

    return features


# ============================================================
# 10. BLOCK / LAYOUT FEATURES
# ============================================================

def extract_layout_features(img):

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    blur = cv2.GaussianBlur(
        gray,
        (5, 5),
        0
    )

    edges = cv2.Canny(
        blur,
        50,
        150
    )

    contours, _ = cv2.findContours(
        edges,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    h, w = gray.shape

    image_area = h * w

    blocks = []

    for contour in contours:

        x, y, bw, bh = cv2.boundingRect(
            contour
        )

        area = bw * bh

        if area > 500:

            blocks.append(
                (x, y, bw, bh)
            )

    features = {}

    features["layout_num_blocks"] = float(
        len(blocks)
    )

    if blocks:

        areas = [
            bw * bh
            for _, _, bw, bh
            in blocks
        ]

        features["layout_largest_block_ratio"] = float(
            max(areas) / image_area
        )

        features["layout_mean_block_ratio"] = float(
            np.mean(areas) / image_area
        )

        features["layout_block_area_std"] = float(
            np.std(areas) / image_area
        )

        # Average normalized coordinates

        xs = [
            x / w
            for x, _, _, _
            in blocks
        ]

        ys = [
            y / h
            for _, y, _, _
            in blocks
        ]

        features["layout_mean_x"] = float(
            np.mean(xs)
        )

        features["layout_mean_y"] = float(
            np.mean(ys)
        )

    else:

        features["layout_largest_block_ratio"] = 0.0
        features["layout_mean_block_ratio"] = 0.0
        features["layout_block_area_std"] = 0.0
        features["layout_mean_x"] = 0.0
        features["layout_mean_y"] = 0.0

    return features


# ============================================================
# 11. WHITESPACE + SYMMETRY
# ============================================================

def extract_whitespace_symmetry(img):

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    h, w = gray.shape

    features = {}

    features["whitespace_ratio"] = float(
        np.mean(gray > 240)
    )

    # --------------------------------------------------------
    # Symmetry
    # --------------------------------------------------------

    left = gray[:, :w // 2]

    right = gray[:, w // 2:]

    right = cv2.flip(
        right,
        1
    )

    min_width = min(
        left.shape[1],
        right.shape[1]
    )

    left = left[:, :min_width]
    right = right[:, :min_width]

    score, _ = ssim(
        left,
        right,
        full=True
    )

    features["horizontal_symmetry"] = float(
        score
    )

    return features


# ============================================================
# 12. OCR / TEXT LAYOUT
# ============================================================

def extract_ocr_features(img):

    if not TESSERACT_AVAILABLE:

        return {
            "ocr_available": 0.0,
            "ocr_num_text_blocks": 0.0,
            "ocr_text_area_ratio": 0.0,
            "ocr_mean_font_height": 0.0,
            "ocr_mean_x": 0.0,
            "ocr_mean_y": 0.0
        }

    rgb = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2RGB
    )

    try:

        data = pytesseract.image_to_data(
            rgb,
            output_type=pytesseract.Output.DICT
        )

    except Exception:

        return {
            "ocr_available": 0.0,
            "ocr_num_text_blocks": 0.0,
            "ocr_text_area_ratio": 0.0,
            "ocr_mean_font_height": 0.0,
            "ocr_mean_x": 0.0,
            "ocr_mean_y": 0.0
        }

    h, w = img.shape[:2]

    areas = []
    heights = []
    xs = []
    ys = []

    for i in range(
        len(data["text"])
    ):

        text = data["text"][i].strip()

        confidence = float(
            data["conf"][i]
        )

        if (
            text == ""
            or confidence < 30
        ):
            continue

        x = int(data["left"][i])
        y = int(data["top"][i])
        bw = int(data["width"][i])
        bh = int(data["height"][i])

        areas.append(
            bw * bh
        )

        heights.append(bh)

        xs.append(x / w)
        ys.append(y / h)

    if not areas:

        return {
            "ocr_available": 1.0,
            "ocr_num_text_blocks": 0.0,
            "ocr_text_area_ratio": 0.0,
            "ocr_mean_font_height": 0.0,
            "ocr_mean_x": 0.0,
            "ocr_mean_y": 0.0
        }

    return {

        "ocr_available": 1.0,

        "ocr_num_text_blocks":
            float(len(areas)),

        "ocr_text_area_ratio":
            float(
                np.sum(areas)
                / (h * w)
            ),

        "ocr_mean_font_height":
            float(
                np.mean(heights) / h
            ),

        "ocr_mean_x":
            float(np.mean(xs)),

        "ocr_mean_y":
            float(np.mean(ys))
    }


# ============================================================
# 13. DEEP VISUAL EMBEDDING
# ============================================================

class ResNetFeatureExtractor:

    model = None
    transform = None

    @classmethod
    def initialize(cls):

        if not TORCH_AVAILABLE:
            return False

        if cls.model is not None:
            return True

        weights = ResNet50_Weights.DEFAULT

        model = resnet50(
            weights=weights
        )

        # Remove classification layer

        model.fc = torch.nn.Identity()

        model.eval()

        cls.model = model

        cls.transform = \
            weights.transforms()

        return True

    @classmethod
    def extract(cls, img):

        if not cls.initialize():

            return {}

        rgb = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2RGB
        )

        pil_image = Image.fromarray(
            rgb
        )

        tensor = cls.transform(
            pil_image
        ).unsqueeze(0)

        with torch.no_grad():

            embedding = cls.model(
                tensor
            )

        embedding = (
            embedding
            .squeeze()
            .cpu()
            .numpy()
        )

        return {
            f"resnet50_{i}":
                float(value)
            for i, value
            in enumerate(embedding)
        }


# ============================================================
# 14. PROPOSED VLF
# ============================================================

def extract_vlf_features(img):

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    blur = cv2.GaussianBlur(
        gray,
        (5, 5),
        0
    )

    edges = cv2.Canny(
        blur,
        50,
        150
    )

    contours, _ = cv2.findContours(
        edges,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    blocks = []

    for c in contours:

        x, y, w, h = cv2.boundingRect(c)

        if w * h > 500:

            blocks.append(
                (x, y, w, h)
            )

    image_h, image_w = img.shape[:2]

    features = {}

    # Number blocks

    features["VLF_num_blocks"] = float(
        len(blocks)
    )

    # Largest block

    if blocks:

        largest = max(
            [
                w * h
                for _, _, w, h
                in blocks
            ]
        )

        features[
            "VLF_largest_block_ratio"
        ] = float(
            largest
            / (image_h * image_w)
        )

    else:

        features[
            "VLF_largest_block_ratio"
        ] = 0.0

    # Whitespace

    features["VLF_whitespace_ratio"] = float(
        np.mean(gray > 240)
    )

    # Vertical density

    top = edges[:image_h // 3]

    middle = edges[
        image_h // 3:
        2 * image_h // 3
    ]

    bottom = edges[
        2 * image_h // 3:
    ]

    features["VLF_top_density"] = float(
        np.mean(top > 0)
    )

    features["VLF_middle_density"] = float(
        np.mean(middle > 0)
    )

    features["VLF_bottom_density"] = float(
        np.mean(bottom > 0)
    )

    # Symmetry

    left = gray[:, :image_w // 2]

    right = gray[:, image_w // 2:]

    right = cv2.flip(
        right,
        1
    )

    min_width = min(
        left.shape[1],
        right.shape[1]
    )

    left = left[:, :min_width]
    right = right[:, :min_width]

    symmetry, _ = ssim(
        left,
        right,
        full=True
    )

    features["VLF_symmetry_score"] = float(
        symmetry
    )

    # Edge density

    features["VLF_edge_density"] = float(
        np.mean(edges > 0)
    )

    # Logo approximation

    top_limit = int(
        image_h * 0.20
    )

    candidates = [
        b for b in blocks
        if b[1] < top_limit
    ]

    if candidates:

        logo = max(
            candidates,
            key=lambda b:
            b[2] * b[3]
        )

        x, y, bw, bh = logo

        features["VLF_logo_x"] = float(
            x / image_w
        )

        features["VLF_logo_y"] = float(
            y / image_h
        )

        features["VLF_logo_area"] = float(
            (bw * bh)
            / (image_w * image_h)
        )

    else:

        features["VLF_logo_x"] = 0.0
        features["VLF_logo_y"] = 0.0
        features["VLF_logo_area"] = 0.0

    return features


# ============================================================
# 15. PROPOSED RCI
# ============================================================

def extract_rci_features(
        image_path,
        grid_size=4):

    image = Image.open(
        image_path
    ).convert("RGB")

    img = (
        np.asarray(
            image,
            dtype=np.float32
        )
        / 255.0
    )

    R = img[:, :, 0]
    G = img[:, :, 1]
    B = img[:, :, 2]

    max_rgb = np.max(
        img,
        axis=2
    )

    min_rgb = np.min(
        img,
        axis=2
    )

    saturation = np.zeros_like(
        max_rgb
    )

    valid = max_rgb > 1e-8

    saturation[valid] = (
        (
            max_rgb[valid]
            - min_rgb[valid]
        )
        /
        (
            max_rgb[valid]
            + 1e-8
        )
    )

    C1 = np.mean(
        saturation
    )

    C2 = np.std(
        saturation
    )

    mean_R = np.mean(R)
    mean_G = np.mean(G)
    mean_B = np.mean(B)

    rgb_sum = (
        mean_R
        + mean_G
        + mean_B
        + 1e-8
    )

    D_RG = abs(
        mean_R - mean_G
    ) / rgb_sum

    D_GB = abs(
        mean_G - mean_B
    ) / rgb_sum

    D_RB = abs(
        mean_R - mean_B
    ) / rgb_sum

    rgb_imbalance = (
        D_RG
        + D_GB
        + D_RB
    ) / 3.0

    C3 = min(
        rgb_imbalance / (2.0 / 3.0),
        1.0
    )

    h, w = saturation.shape

    cell_h = h // grid_size
    cell_w = w // grid_size

    regional = []

    for row in range(grid_size):

        for col in range(grid_size):

            y1 = row * cell_h

            y2 = (
                (row + 1) * cell_h
                if row < grid_size - 1
                else h
            )

            x1 = col * cell_w

            x2 = (
                (col + 1) * cell_w
                if col < grid_size - 1
                else w
            )

            regional.append(
                np.mean(
                    saturation[
                        y1:y2,
                        x1:x2
                    ]
                )
            )

    matrix = np.array(
        regional
    ).reshape(
        grid_size,
        grid_size
    )

    differences = []

    for row in range(grid_size):

        for col in range(
            grid_size - 1
        ):

            differences.append(
                abs(
                    matrix[row, col]
                    -
                    matrix[row, col + 1]
                )
            )

    for row in range(
        grid_size - 1
    ):

        for col in range(
            grid_size
        ):

            differences.append(
                abs(
                    matrix[row, col]
                    -
                    matrix[row + 1, col]
                )
            )

    C4 = np.mean(
        differences
    )

    RCI = (
        C1
        + C2
        + C3
        + C4
    ) / 4.0

    return {

        "RCI": float(RCI),

        "RCI_C1_mean_saturation":
            float(C1),

        "RCI_C2_saturation_std":
            float(C2),

        "RCI_C3_rgb_imbalance":
            float(C3),

        "RCI_C4_spatial_anomaly":
            float(C4),

        "RCI_mean_R":
            float(mean_R),

        "RCI_mean_G":
            float(mean_G),

        "RCI_mean_B":
            float(mean_B),

        "RCI_D_RG":
            float(D_RG),

        "RCI_D_GB":
            float(D_GB),

        "RCI_D_RB":
            float(D_RB)
    }


# ============================================================
# 16. COMPLETE FEATURE EXTRACTOR
# ============================================================

def extract_all_features(
        image_path,
        use_ocr=True,
        use_deep=False):

    print(
        f"\nProcessing: {image_path}"
    )

    img = load_image(
        image_path
    )

    features = {}

    # --------------------------------------------------------
    # Previous-work baselines
    # --------------------------------------------------------

    print("1/11 Color statistics...")

    features.update(
        extract_color_features(img)
    )

    print("2/11 Color histogram...")

    features.update(
        extract_color_histogram(img)
    )

    print("3/11 Spatial color...")

    features.update(
        extract_spatial_color_features(img)
    )

    print("4/11 HOG...")

    features.update(
        extract_hog_features(img)
    )

    print("5/11 LBP...")

    features.update(
        extract_lbp_features(img)
    )

    print("6/11 SIFT...")

    features.update(
        extract_sift_features(img)
    )

    print("7/11 ORB...")

    features.update(
        extract_orb_features(img)
    )

    print("8/11 Structural...")

    features.update(
        extract_structural_features(img)
    )

    print("9/11 Layout...")

    features.update(
        extract_layout_features(img)
    )

    features.update(
        extract_grid_structure(img)
    )

    features.update(
        extract_whitespace_symmetry(img)
    )

    # --------------------------------------------------------
    # OCR
    # --------------------------------------------------------

    if use_ocr:

        print("10/11 OCR...")

        features.update(
            extract_ocr_features(img)
        )

    # --------------------------------------------------------
    # Deep feature
    # --------------------------------------------------------

    if use_deep:

        print(
            "11/11 ResNet50 embedding..."
        )

        features.update(
            ResNetFeatureExtractor.extract(
                img
            )
        )

    # --------------------------------------------------------
    # Proposed method
    # --------------------------------------------------------

    print("Extracting proposed VLF...")

    features.update(
        extract_vlf_features(img)
    )

    print("Extracting proposed RCI...")

    features.update(
        extract_rci_features(
            image_path
        )
    )

    return features


# ============================================================
# 17. EXTRACT MULTIPLE SCREENSHOTS
# ============================================================

def extract_dataset(
        image_folder,
        output_csv="screenshot_features.csv",
        use_ocr=True,
        use_deep=False):

    import pandas as pd

    records = []

    valid_extensions = (
        ".png",
        ".jpg",
        ".jpeg",
        ".webp",
        ".bmp"
    )

    files = sorted(
        [
            f
            for f in os.listdir(
                image_folder
            )
            if f.lower().endswith(
                valid_extensions
            )
        ]
    )

    print(
        f"Found {len(files)} images."
    )

    for index, filename in enumerate(
        files,
        start=1
    ):

        print(
            f"\n[{index}/{len(files)}]"
        )

        path = os.path.join(
            image_folder,
            filename
        )

        try:

            features = extract_all_features(
                path,
                use_ocr=use_ocr,
                use_deep=use_deep
            )

            features["image_name"] = filename

            records.append(
                features
            )

        except Exception as e:

            print(
                f"ERROR: {filename}: {e}"
            )

    df = pd.DataFrame(
        records
    )

    # Put image_name first

    columns = (
        ["image_name"]
        +
        [
            c for c in df.columns
            if c != "image_name"
        ]
    )

    df = df[columns]

    df.to_csv(
        output_csv,
        index=False
    )

    print(
        "\n================================================"
    )

    print(
        f"Saved: {output_csv}"
    )

    print(
        f"Images: {len(df)}"
    )

    print(
        f"Features: {len(df.columns) - 1}"
    )

    print(
        "================================================"
    )

    return df


# ============================================================
# 18. SINGLE IMAGE EXAMPLE
# ============================================================

if __name__ == "__main__":

    image_path = r"E:\dataofphish\1015\ImagesPath\7953388_1.jpg"

    features = extract_all_features(
        image_path,
        use_ocr=True,
        use_deep=False
    )

    print(
        "\nExtracted features:"
    )

    for name, value in features.items():

        print(
            f"{name}: {value}"
        )

    # --------------------------------------------------------
    # Dataset example
    # --------------------------------------------------------
    #
    # df = extract_dataset(
    #     "screenshots/",
    #     "screenshot_features.csv",
    #     use_ocr=True,
    #     use_deep=False
    # )