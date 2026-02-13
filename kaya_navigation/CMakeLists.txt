cmake_minimum_required(VERSION 3.8)
project(kaya_navigation)

find_package(ament_cmake REQUIRED)

# install launch files
install(DIRECTORY launch/
  DESTINATION share/${PROJECT_NAME}/launch
)

# install maps
install(DIRECTORY maps/
  DESTINATION share/${PROJECT_NAME}/maps
)

# install nav2 config
install(DIRECTORY config/
  DESTINATION share/${PROJECT_NAME}/config
)

ament_package()

