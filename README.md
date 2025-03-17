# Traffic Spike Magnitude Estimator

## Overview

This tool provides an empirical, quantitative research-based model for estimating the magnitude of traffic spikes based on mean daily traffic. It visualizes the relationship between regular traffic levels and potential traffic spikes, helping system architects and engineers plan for capacity requirements.

The model is based on empirical data collected from various web services, platforms, and peer reviewed studies that, when aggregated, demonstrate that as mean daily traffic increases, the relative magnitude of traffic spikes tends to decrease following a power law relationship.

## Research Basis

The tool implements three models:

1. **Upper Bound (Worst-Case)**: Represents the maximum observed spike magnitudes (593.61 × T^-0.2974)
2. **Median Estimate**: Represents the typical spike magnitude (430.3 × T^-0.3857)
3. **Lower Bound (Minimum)**: Represents the minimum expected spike magnitude (344.27 × T^-0.412)

Where T is the mean daily traffic in users per day.

The model demonstrates that while smaller services might need to handle spikes of 20-35x their normal traffic, large-scale services with millions of daily users typically only experience spikes of 1.5-4x their normal traffic levels.

## Usage

### Basic Usage

Run the script to see the default visualization:

```bash
python plot.py
```

This displays the three trend lines (upper bound, median estimate, and lower bound) along with reference data points used in developing the model.

### Analyzing Specific Traffic Levels

To analyze a specific known daily average traffic level, use the `--traffic` parameter:

```bash
python plot.py --traffic 50000
```

This will:
- Display the standard graph with all trend lines
- Add a vertical line at your specified traffic level (50,000 users/day in this example)
- Mark the intersection points where this line crosses each of the three curves
- Add the calculated spike magnitudes to the legend
- Automatically adjust the scale for optimal visualization

### Interpreting Results

The output shows:
- The expected spike multipliers for your traffic level
- How your traffic level compares to the overall trend
- Visual indicators of where your service falls on the spectrum

Use these results to plan capacity that can handle the expected spike magnitude for your service's scale.

## Example Applications

- **Capacity Planning**: Determine how much extra capacity to provision
- **Load Testing**: Set realistic targets for load testing based on your traffic level
- **Risk Assessment**: Understand the potential magnitude of traffic spikes for your service
- **Cost Optimization**: Avoid over-provisioning by using empirically-based estimates

## Notes

The model is based on observed data and follows general trends. Your specific service characteristics may result in different spike patterns. 

Consider using the upper bound for critical services where downtime is unacceptable.

## License

MIT License

Copyright (c) 2023

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.