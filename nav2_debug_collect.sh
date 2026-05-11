#!/usr/bin/env bash

OUT="nav2_debug_$(date +%Y%m%d_%H%M%S).log"

run_cmd() {
  echo "" | tee -a "$OUT"
  echo "============================================================" | tee -a "$OUT"
  echo "CMD: $*" | tee -a "$OUT"
  echo "============================================================" | tee -a "$OUT"
  timeout 8 bash -lc "$*" 2>&1 | tee -a "$OUT"
}

echo "NAV2 / TF / COSTMAP DEBUG LOG" | tee "$OUT"
echo "Created: $(date)" | tee -a "$OUT"
echo "PWD: $(pwd)" | tee -a "$OUT"
echo "ROS_DOMAIN_ID: ${ROS_DOMAIN_ID:-not_set}" | tee -a "$OUT"
echo "RMW_IMPLEMENTATION: ${RMW_IMPLEMENTATION:-not_set}" | tee -a "$OUT"

run_cmd "ros2 node list"
run_cmd "ros2 topic list"

# Important map/costmap topics
run_cmd "ros2 topic info /map --verbose"
run_cmd "ros2 topic info /scan --verbose"
run_cmd "ros2 topic info /global_costmap/costmap --verbose"
run_cmd "ros2 topic info /global_costmap/static_layer --verbose"
run_cmd "ros2 topic info /global_costmap/obstacle_layer --verbose"
run_cmd "ros2 topic info /local_costmap/costmap --verbose"
run_cmd "ros2 topic info /local_costmap/lidar_layer --verbose"
run_cmd "ros2 topic info /downsampled_costmap --verbose"

# One message from important topics
run_cmd "ros2 topic echo /map --once --qos-durability transient_local"
run_cmd "ros2 topic echo /scan --once"
run_cmd "ros2 topic echo /global_costmap/costmap --once --qos-durability transient_local"
run_cmd "ros2 topic echo /global_costmap/static_layer --once --qos-durability transient_local"
run_cmd "ros2 topic echo /global_costmap/obstacle_layer --once --qos-durability transient_local"
run_cmd "ros2 topic echo /local_costmap/costmap --once --qos-durability transient_local"
run_cmd "ros2 topic echo /local_costmap/lidar_layer --once --qos-durability transient_local"

# TF checks
run_cmd "ros2 run tf2_ros tf2_echo map odom"
run_cmd "ros2 run tf2_ros tf2_echo odom base_link"
run_cmd "ros2 run tf2_ros tf2_echo map base_link"

# Get scan frame automatically and check TF from base_link to scan frame
SCAN_FRAME=$(timeout 8 ros2 topic echo /scan --once 2>/dev/null | awk '/frame_id:/ {print $2; exit}' | tr -d '"')
echo "" | tee -a "$OUT"
echo "Detected scan frame: ${SCAN_FRAME:-not_found}" | tee -a "$OUT"

if [ -n "$SCAN_FRAME" ]; then
  run_cmd "ros2 run tf2_ros tf2_echo base_link $SCAN_FRAME"
  run_cmd "ros2 run tf2_ros tf2_echo map $SCAN_FRAME"
fi

# Nav2 lifecycle states
run_cmd "ros2 lifecycle get /map_server"
run_cmd "ros2 lifecycle get /amcl"
run_cmd "ros2 lifecycle get /global_costmap/global_costmap"
run_cmd "ros2 lifecycle get /local_costmap/local_costmap"
run_cmd "ros2 lifecycle get /planner_server"
run_cmd "ros2 lifecycle get /controller_server"
run_cmd "ros2 lifecycle get /bt_navigator"

# Important Nav2 params
run_cmd "ros2 param get /amcl use_sim_time"
run_cmd "ros2 param get /amcl global_frame_id"
run_cmd "ros2 param get /amcl odom_frame_id"
run_cmd "ros2 param get /amcl base_frame_id"
run_cmd "ros2 param get /amcl scan_topic"

run_cmd "ros2 param get /global_costmap/global_costmap global_frame"
run_cmd "ros2 param get /global_costmap/global_costmap robot_base_frame"
run_cmd "ros2 param get /global_costmap/global_costmap rolling_window"
run_cmd "ros2 param get /global_costmap/global_costmap plugins"
run_cmd "ros2 param get /global_costmap/global_costmap static_layer.map_topic"
run_cmd "ros2 param get /global_costmap/global_costmap static_layer.map_subscribe_transient_local"
run_cmd "ros2 param get /global_costmap/global_costmap obstacle_layer.observation_sources"
run_cmd "ros2 param get /global_costmap/global_costmap obstacle_layer.scan.topic"

run_cmd "ros2 param get /local_costmap/local_costmap global_frame"
run_cmd "ros2 param get /local_costmap/local_costmap robot_base_frame"
run_cmd "ros2 param get /local_costmap/local_costmap rolling_window"
run_cmd "ros2 param get /local_costmap/local_costmap plugins"
run_cmd "ros2 param get /local_costmap/local_costmap lidar_layer.observation_sources"
run_cmd "ros2 param get /local_costmap/local_costmap lidar_layer.scan.topic"

# Show TF tree if available
run_cmd "ros2 run tf2_tools view_frames"

echo "" | tee -a "$OUT"
echo "============================================================" | tee -a "$OUT"
echo "DONE" | tee -a "$OUT"
echo "Log file created:" | tee -a "$OUT"
echo "$OUT" | tee -a "$OUT"
echo "============================================================" | tee -a "$OUT"
