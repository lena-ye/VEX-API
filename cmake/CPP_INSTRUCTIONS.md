
### Requirements
1. install [[vcpkg]] if haven't already.
2. Install the following libraries in [[Bash]]: `vcpkg install cpr nlohmann-json`
3. Install Visual Studio's Desktop development with C++

### Steps
1. create a folder layout as such:
```
your_cpp_project/
├── CMakeLists.txt
└── main.cpp
```

2. In `CMakeLists.txt`, paste:
```
cmake_minimum_required(VERSION 3.14)
project(RobotEventsAPI)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(cpr CONFIG REQUIRED)
find_package(nlohmann_json CONFIG REQUIRED)

add_executable(RobotEventsAPI main.cpp)
target_link_libraries(RobotEventsAPI PRIVATE cpr::cpr nlohmann_json::nlohmann_json)
```

3. Build with [[CMake]] in [[Bash]]

In `/your_cpp_project` (mine is `/cmake'):
1. `cmake -B build -S . -DCMAKE_TOOLCHAIN_FILE="C:/path/to/vcpkg/scripts/buildsystems/vcpkg.cmake"`
	1. Remember to change the `DMAKE_TOOLCHAIN_FILE` path. It is usually at `C:/path_to_vcpkg_folder/scripts/buildsystems/vcpkg.cmake`
2. `cmake --build build`

In the case where you have to recursively delete the entire `./build` folder to rebuild, type:
- Bash: `rm -rf ./build`
- PowerShell: `Remove-Item -Recurse -Force .\build`

4. Run `RobotEventsAPI.exe` in [[Bash]]
	1. You need to know where the `RobotEventsAPI.exe` file is. You can usually find info based on the output from last command.
	2. In my case, it was at `./build/Debug/`
	3. cd into that directory and run `./RobotEventsAPI.exe`
