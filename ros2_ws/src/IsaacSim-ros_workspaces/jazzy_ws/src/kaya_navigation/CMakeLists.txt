cmake_minimum_required(VERSION 3.8)
project(kaya_navigation)

find_package(ament_cmake REQUIRED)

install(DIRECTORY
  launch
  params
  maps
  rviz2
  DESTINATION share/${PROJECT_NAME})

ament_package()
