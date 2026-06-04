#!/bin/bash

# Config
WS_DIR="$HOME/ros2_ws/src/IsaacSim-ros_workspaces/jazzy_ws"

# Log setup 
LOG_DIR="$HOME/kaya_logs"
mkdir -p "$LOG_DIR"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
LOG_FILE="$LOG_DIR/nav2_${TIMESTAMP}.log"

exec > >(tee -a "$LOG_FILE") 2>&1


echo " Kaya Nav2 Session — $(date)"
echo " Log file: $LOG_FILE"


# ROS 2 environment
echo ""
echo "Sourcing ROS 2 Jazzy"
source /opt/ros/jazzy/setup.bash

# Workspace
echo ""
echo "Cleaning workspace"
cd "$WS_DIR" || { echo "[ERROR] Workspace not found: $WS_DIR"; exit 1; }
rm -rf "$WS_DIR/build" "$WS_DIR/install" "$WS_DIR/log"
echo "--- Removing stale symlink-install directories ---"
for PKG in custom_message isaac_ros2_messages; do
    STALE="$WS_DIR/build/$PKG/ament_cmake_python/$PKG/$PKG"
    if [ -d "$STALE" ]; then
        echo "  Removing stale dir: $STALE"
        rm -rf "$STALE"
    fi
done

echo ""
echo "Building workspace"
colcon build --symlink-install
BUILD_STATUS=$?

if [ $BUILD_STATUS -ne 0 ]; then
    echo ""
    echo "[ERROR] colcon build failed with exit code $BUILD_STATUS"
    echo "        Check above for the failing package(s)."
    exit $BUILD_STATUS
fi

echo ""
echo "Sourcing workspace"
source "$WS_DIR/install/setup.bash"

# Pre-launch diagnostics
echo ""
echo "Pre-launch diagnostics"

echo "Checking map files"
MAP_DIR="$(ros2 pkg prefix kaya_navigation 2>/dev/null)/share/kaya_navigation/maps"
if [ -d "$MAP_DIR" ]; then
    ls -lh "$MAP_DIR"
else
    echo "[WARN] Map directory not found: $MAP_DIR"
fi

echo "--- Checking /clock topic (Isaac Sim must be running) ---"
timeout 3 ros2 topic hz /clock --window 5 2>&1 | head -5 || echo "[WARN] /clock not publishing — start Isaac Sim first"

echo "--- Checking /scan topic ---"
timeout 3 ros2 topic hz /scan --window 5 2>&1 | head -5 || echo "[WARN] /scan not publishing"

echo "--- Checking /odom topic ---"
timeout 3 ros2 topic hz /odom --window 5 2>&1 | head -5 || echo "[WARN] /odom not publishing"

# Launch Nav2
echo ""
echo "Starting Nav2 for Kaya"
echo "--- Launch start time: $(date) ---"

ros2 launch kaya_navigation kaya_navigation.launch.py use_sim_time:=True
LAUNCH_STATUS=$?

# Post-exit summary
echo ""
echo " Session ended — $(date)"
echo " Exit code: $LAUNCH_STATUS"
echo " Full log: $LOG_FILE"

echo ""
echo "Error/Warn summary"
grep -E "\[ERROR\]|\[WARN\]" "$LOG_FILE" | tail -50
