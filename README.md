# Internship

This repository contains the work and documentation related to my internship project.

[Kaya_Navigation_Files](https://drive.google.com/file/d/1wbu4CFYYdb1A6QALh3H21Rj_6sesPXBn/view?usp=sharing)

## Running Kaya Robot Navigation

To navigate the Kaya robot, follow these steps:

1. Make sure the `kaya_navigation` folder is placed inside the ROS 2 workspace source directory:

   ```bash
   ~/ros2_ws/src/IsaacSim-ros_workspaces/jazzy_ws/src
   ```

2. Start **Isaac Sim 5.1.0**.

3. Open the Kaya robot scene:

   ```text
   kaya.usd
   ```

4. Press **Play** in Isaac Sim to start the simulation.

5. Open a terminal and go to the `kaya_navigation` directory using a relative path from the workspace source directory:

   ```bash
   cd ~/ros2_ws/src/IsaacSim-ros_workspaces/jazzy_ws/src/kaya_navigation
   ```

6. Run the RViz launch script:

   ```bash
   ./startRViz.sh
   ```

After this, RViz should open and the Kaya robot navigation setup should start.
