# MotorCycleGraph
A Python implementation of MotorCycle Graph algorithm for Quad-Mesh partitioning

This project is a Python project for patotioning a Quad-Mesh using MotorCycleGraph algorithm published by Eppstein et al (2008). You can find the orgignal paper in the following link:

https://disneyanimation.com/publications/motorcycle-graphs-canonical-quad-mesh-partitioning

## Dependencies

Before running the project, ensure you have the following dependencies installed:

- Python 3.8+
- NumPy
- Matplotlib
- pyvista

You can install these dependencies using `pip`:

```bash
pip install numpy matplotlib pyvista
```
## How to use
To use the code, you need to run "Motor.py" following by the path to a quad-mesh you wish to partition it:
```bash
python Motor.py <path to your quad mesh>
```
The code will process the mesh and show the inout mesh and the result of MotorCycleGraph algorithm side-by-side

## Usage example
Here is an example of code to partitioning a quad mesh:

```bash
python Motor.py ./models/6_rem_p0_0_quadrangulation_smooth.obj
```

And below is a screenshot of the output. The left image is the inital quad-mesh and the righ image the partitioned quad-mesh by MotorCycleGraph.

![An example of MotorCycleGraph output](Models/example1.PNG)

