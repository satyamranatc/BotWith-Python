"""
Vision MCP Server — Jarvis-Vision
Uses YOLOv11 + webcam to detect objects in front of the camera.

The YOLO model and webcam are loaded lazily (only when detect_objects is first called),
so MCP startup is instant and doesn't block.
"""

import cv2
import time
from ultralytics import YOLO
from mcp.server.fastmcp import FastMCP

# ── Server ────────────────────────────────────────────────────────────────────
mcp = FastMCP("Jarvis-Vision")

# Lazy globals — set on first tool call, not at import time
_model = None
_cam   = None


def _load_resources():
    """Load YOLO model and open webcam the first time detect_objects is called."""
    global _model, _cam
    if _model is None:
        _model = YOLO("yolo11n.pt")
    if _cam is None or not _cam.isOpened():
        _cam = cv2.VideoCapture(0)


# ── Tool ──────────────────────────────────────────────────────────────────────
@mcp.tool()
def detect_objects() -> list[str]:
    """
    Look through the webcam for 3 seconds and return a list of
    every unique object detected (e.g. ["person", "laptop", "cup"]).
    """
    _load_resources()  # ensure model + cam are ready

    detected = set()
    deadline = time.time() + 3  # scan for 3 seconds

    while time.time() < deadline:
        ok, frame = _cam.read()
        if not ok:
            break

        results = _model(frame, verbose=False)

        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                detected.add(_model.names[class_id])

        # Show live feed with bounding boxes (press Q to quit early)
        cv2.imshow("Jarvis Vision — Object Detection", results[0].plot())
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()
    return sorted(detected)  # sorted so output is predictable


# ── Entry point (required for MCP subprocess launch) ─────────────────────────
if __name__ == "__main__":
    detect_objects()
    # mcp.run()
