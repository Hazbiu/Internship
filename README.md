## Kaya Robot Navigation

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

## How to create the map using SLAM?

This step creates the occupancy map that will later be used by Nav2.

1. Open the Kaya scene in Isaac Sim.

2. Open the Occupancy Map tool:

   ```text
   Tools > Robotics > Occupancy Map
   ```

3. In the Occupancy Map extension, set the Origin to:

   ```text
   X: 0.0
   Y: 0.0
   Z: -0.65
   ```

4. Set the Upper Bound Z to:

   ```text
   Z: 0.2
   ```

   This height matches the lidar height of the Kaya robot.

5. Select the `SimpleRoom` prim in the stage.

6. Click:

   ```text
   BOUND SELECTION
   ```

7. Check that the occupancy map bounds cover the complete `SimpleRoom` environment.

8. Delete the `Kaya` prim from the stage before generating the map.

9. Click:

   ```text
   CALCULATE
   ```

10. Click:
   
   ```text
   VISUALIZE IMAGE
   ```

11. In the Visualization window, save the map image in this directory:

   ```bash
   ~/ros2_ws/src/IsaacSim-ros_workspaces/jazzy_ws/src/kaya_navigation/maps
   ```

12. Create a YAML file in the same directory, for example:

   ```text
   KayaMap.yaml
   ```

13. Copy the generated map parameters from the Visualization window into the YAML file.

   Example:

   ```yaml
   image: KayaMap.png
   mode: trinary
   resolution: 0.05
   origin: [0.0, 0.0, 0.0]
   negate: 0
   occupied_thresh: 0.65
   free_thresh: 0.196
   ```

14. Make sure the image name in the YAML file matches the saved map image name.

15. After this, the map is ready to be used with Nav2.


## Limitations of the Project

There are two known limitations in the current navigation setup:

1. **Global Costmap Obstacle Layer Issue**

   If the `obstacle_layer` is included inside the `plugins` list of the `global_costmap` parameters, the implemented areas shown in the RViz map can appear abnormal or incorrect.

   Because of this, the `obstacle_layer` should not be added to the `global_costmap` plugins unless the configuration is carefully adjusted and tested.

2. **First Goal May Be Aborted**

   After running the navigation script startRViz.sh and sending the first navigation goal in RViz, the goal will most likely be aborted.

   After this first aborted goal, the system usually behaves normally, and the following navigation goals can be executed correctly.
