"""
===========================================================================
  SortBot - Member 2: The Messenger
  FastAPI REST server bridging Unity <-> AI Object Detection
===========================================================================

This server exposes a POST /detect endpoint that:
  1. Accepts an image file uploaded from Unity.
  2. Runs it through a YOLOv11n waste detection model.
  3. Returns a clean JSON response with class, confidence & center coords.

Model: YOLOv11n trained on waste classes (Cardboard, Other, Metal, Plastic)
===========================================================================
"""

import io
import logging
from typing import Optional

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image
from ultralytics import YOLO

# ---------------------------------------------------------------------------
#  Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(message)s",
)
logger = logging.getLogger("sortbot")

# ---------------------------------------------------------------------------
#  FastAPI App
# ---------------------------------------------------------------------------
app = FastAPI(
    title="SortBot - Waste Detection API",
    description=(
        "A REST bridge between the Unity simulation and the AI object-detection "
        "model. Uses a YOLOv11n model to classify waste into Cardboard, Other, Metal, and Plastic."
    ),
    version="1.0.0",
)

# Allow any origin so Unity WebGL / editor / tests can reach us.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
#  Configuration
# ---------------------------------------------------------------------------
model = YOLO("Yolo11nBest.pt")
# Waste classes returned by the YOLOv11n model
WASTE_CLASSES = {0: "Cardboard", 1: "Other", 2: "Metal", 3: "Plastic"}

# ---------------------------------------------------------------------------
#  Response Models (Pydantic)
# ---------------------------------------------------------------------------

class CenterCoordinates(BaseModel):
    """(x, y) pixel position of the detected object's center."""
    x: int
    y: int


class DetectionResult(BaseModel):
    """Single object detection result."""
    waste_class: str            # e.g. "plastic bottle" or "Unknown"
    confidence: float           # 0.0 - 1.0
    center_coordinates: CenterCoordinates


class DetectionResponse(BaseModel):
    """Top-level JSON envelope returned by POST /detect."""
    success: bool
    detection: Optional[DetectionResult] = None
    message: Optional[str] = None


# ---------------------------------------------------------------------------
#  YOLOv11n Waste Detection
# ---------------------------------------------------------------------------
CONFIDENCE_THRESHOLD = 0.25
def detect_objects(image: Image.Image) -> Optional[dict]:
    """
    Runs the real YOLO model on the uploaded image and returns the highest confidence detection.
    """
    results = model.predict(image, conf=CONFIDENCE_THRESHOLD)
    
    if not results or len(results[0].boxes) == 0:
        return None

    english_classes = {0: 'Cardboard', 1: 'Other', 2: 'Metal', 3: 'Plastic'}

    best_box = None
    max_conf = -1.0
    
    for box in results[0].boxes:
        c = float(box.conf[0])
        if c > max_conf:
            max_conf = c
            best_box = box

    if best_box is None:
        return None

    x_min, y_min, x_max, y_max = best_box.xyxy[0]
    center_x = float((x_min + x_max) / 2)
    center_y = float((y_min + y_max) / 2)
    
    class_id = int(best_box.cls[0])
    waste_class = english_classes.get(class_id, "Unknown")

    return {
        "class": waste_class,
        "confidence": max_conf,
        "x": int(center_x),
        "y": int(center_y)
    }


# ---------------------------------------------------------------------------
#  Helpers
# ---------------------------------------------------------------------------

def validate_image(file_bytes: bytes) -> Image.Image:
    """
    Attempt to open and verify the uploaded bytes as a valid image.

    Raises
    ------
    HTTPException(400) if the bytes are not a valid image.
    """
    try:
        # First pass - verify structural integrity
        img_check = Image.open(io.BytesIO(file_bytes))
        img_check.verify()  # raises if corrupt

        # Re-open because .verify() can leave the object unusable
        img = Image.open(io.BytesIO(file_bytes))
        img.load()  # force full decode
        return img
    except Exception as exc:
        logger.warning("Image validation failed: %s", exc)
        raise HTTPException(
            status_code=400,
            detail=f"Uploaded file is not a valid image or is corrupt: {exc}",
        )


# ---------------------------------------------------------------------------
#  Endpoints
# ---------------------------------------------------------------------------

@app.get("/", tags=["Health"])
async def health_check():
    """Simple health-check / welcome endpoint."""
    return {
        "status": "online",
        "service": "SortBot Waste Detection API",
        "version": "1.0.0",
        "hint": "POST an image to /detect to get waste classification results.",
    }


@app.post(
    "/detect",
    response_model=DetectionResponse,
    summary="Detect waste objects in an uploaded image",
    tags=["Detection"],
)
async def detect(file: UploadFile = File(..., description="Image file (JPEG / PNG)")):
    """
    Accept an image upload, run it through the AI detector, and return
    the classification result as JSON.

    **Response fields:**
    - `success` - always `true` on 2xx
    - `detection` - object with `waste_class`, `confidence`,
      `center_coordinates` (or `null` if nothing detected)
    - `message` - human-readable note when detection is null
    """

    # --- 1. Read uploaded bytes -----------------------------------------
    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    logger.info(
        "Received file: name=%s  size=%d bytes  content_type=%s",
        file.filename, len(contents), file.content_type,
    )

    # --- 2. Validate image ----------------------------------------------
    image = validate_image(contents)

    # --- 3. Run detection -----------------------------------------------
    result = detect_objects(image)

    # --- 4. Handle "no detection" case ----------------------------------
    if result is None:
        return DetectionResponse(
            success=True,
            detection=None,
            message="No object detected in the image.",
        )

    # --- 5. Apply confidence threshold ----------------------------------
    waste_class = result["class"]
    confidence  = result["confidence"]

    if confidence < CONFIDENCE_THRESHOLD:
        logger.info(
            "Confidence %.2f is below threshold %.2f -> class set to 'Unknown'.",
            confidence, CONFIDENCE_THRESHOLD,
        )
        waste_class = "Unknown"

    # --- 6. Build & return response -------------------------------------
    detection = DetectionResult(
        waste_class=waste_class,
        confidence=confidence,
        center_coordinates=CenterCoordinates(x=result["x"], y=result["y"]),
    )

    return DetectionResponse(success=True, detection=detection)


# ---------------------------------------------------------------------------
#  Run with:  python main.py   (or:  uvicorn main:app --reload)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    logger.info("Starting SortBot server on http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)