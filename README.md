## Kaya Robot Navigatiom

https://drive.google.com/file/d/1wbu4CFYYdb1A6QALh3H21Rj_6sesPXBn/view

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


## Limitations of the Project

There are two known limitations in the current navigation setup:

1. **Global Costmap Obstacle Layer Issue**

   If the `obstacle_layer` is included inside the `plugins` list of the `global_costmap` parameters, the implemented areas shown in the RViz map can appear abnormal or incorrect.

   Because of this, the `obstacle_layer` should not be added to the `global_costmap` plugins unless the configuration is carefully adjusted and tested.

2. **First Goal May Be Aborted**

   After running the navigation script startRViz.sh and sending the first navigation goal in RViz, the goal will most likely be aborted.

   After this first aborted goal, the system usually behaves normally, and the following navigation goals can be executed correctly.
