# Lane Line Extractor

A lane line detection pipeline for road images, the kind of perception step used in driver-assistance and self-driving systems. It takes a road image and extracts the left and right lane markings using classic image-processing techniques, then draws them on the original image.

## Pipeline

```
Input image -> Grayscale -> Blur -> Edge detection -> Region of interest
            -> Line detection -> Overlay on original
```

| Step | What it does | Why it is needed |
|---|---|---|
| Grayscale | Converts the colour image to a single intensity channel | Simplifies the image; lane markings stand out by brightness |
| Gaussian blur | Smooths the image | Reduces noise so random specks are not detected as edges |
| Edge detection (Canny) | Finds places where brightness changes sharply | Lane paint is bright against dark road, so it appears as strong edges |
| Region of interest (ROI) | Masks everything except the road area in front of the vehicle | Sky, trees and buildings are ignored |
| Line detection (Hough transform) | Finds straight line segments from the remaining edge pixels | Turns edge pixels into actual lane lines |
| Overlay | Averages the segments into one left and one right lane line and draws them on the original image | Gives a visual result |

## Project Structure

```
lane-line-extractor/
├── lane_extractor.py    # pipeline functions
├── main.py              # runs the pipeline on an image
├── images/              # input road images
├── output/              # saved results
└── README.md
```

## Requirements

- Python 3.8+
- NumPy
- OpenCV (`opencv-python`)

```bash
pip install numpy opencv-python
```

## Usage

```bash
python main.py --input images/road.jpg --output output/road_lanes.jpg
```

The script saves the final image with the detected lane lines drawn on it. Intermediate results (grayscale, edges, ROI mask) can also be saved to the `output/` folder to see what each step does.

## Key Parameters

| Parameter | Meaning | Effect |
|---|---|---|
| Blur kernel size | Size of the smoothing window | Larger means less noise but blurrier edges |
| Canny thresholds | Lower and upper edge-strength limits | Higher values keep fewer, stronger edges |
| ROI polygon | Corner points of the road region (usually a trapezoid) | Must fit the camera view |
| Hough settings | Minimum line length and maximum gap | Controls which line segments are accepted |

## Limitations

- Works best on clear daytime images with visible, high-contrast lane markings.
- Struggles with shadows, worn paint, sharp curves, night and rain.
- The ROI is fixed, so it assumes a particular camera position.

## Possible Improvements

- Colour filtering for white and yellow lane markings
- Polynomial curve fitting for curved lanes
- Video support with smoothing across frames
