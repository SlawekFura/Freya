# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.15

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/local/bin/cmake

# The command to remove a file.
RM = /usr/local/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/slawek/workspace/CppWorkspace/ToolpathGenerator

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/slawek/workspace/CppWorkspace/ToolpathGenerator

# Include any dependencies generated for this target.
include CMakeFiles/ToolpathGenerator.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/ToolpathGenerator.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/ToolpathGenerator.dir/flags.make

CMakeFiles/ToolpathGenerator.dir/main.cpp.o: CMakeFiles/ToolpathGenerator.dir/flags.make
CMakeFiles/ToolpathGenerator.dir/main.cpp.o: main.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/slawek/workspace/CppWorkspace/ToolpathGenerator/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/ToolpathGenerator.dir/main.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/ToolpathGenerator.dir/main.cpp.o -c /home/slawek/workspace/CppWorkspace/ToolpathGenerator/main.cpp

CMakeFiles/ToolpathGenerator.dir/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/ToolpathGenerator.dir/main.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/slawek/workspace/CppWorkspace/ToolpathGenerator/main.cpp > CMakeFiles/ToolpathGenerator.dir/main.cpp.i

CMakeFiles/ToolpathGenerator.dir/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/ToolpathGenerator.dir/main.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/slawek/workspace/CppWorkspace/ToolpathGenerator/main.cpp -o CMakeFiles/ToolpathGenerator.dir/main.cpp.s

# Object files for target ToolpathGenerator
ToolpathGenerator_OBJECTS = \
"CMakeFiles/ToolpathGenerator.dir/main.cpp.o"

# External object files for target ToolpathGenerator
ToolpathGenerator_EXTERNAL_OBJECTS =

ToolpathGenerator: CMakeFiles/ToolpathGenerator.dir/main.cpp.o
ToolpathGenerator: CMakeFiles/ToolpathGenerator.dir/build.make
ToolpathGenerator: /usr/lib/x86_64-linux-gnu/libmpfr.so
ToolpathGenerator: /usr/lib/x86_64-linux-gnu/libgmp.so
ToolpathGenerator: /usr/lib/x86_64-linux-gnu/libCGAL.so.11.0.1
ToolpathGenerator: /usr/lib/x86_64-linux-gnu/libboost_thread.so
ToolpathGenerator: /usr/lib/x86_64-linux-gnu/libboost_system.so
ToolpathGenerator: /usr/lib/x86_64-linux-gnu/libpthread.so
ToolpathGenerator: /usr/lib/x86_64-linux-gnu/libCGAL_Core.so.11.0.1
ToolpathGenerator: /usr/lib/x86_64-linux-gnu/libCGAL.so.11.0.1
ToolpathGenerator: /usr/lib/x86_64-linux-gnu/libgmp.so
ToolpathGenerator: /usr/lib/x86_64-linux-gnu/libgmpxx.so
ToolpathGenerator: /usr/lib/x86_64-linux-gnu/libmpfr.so
ToolpathGenerator: /usr/lib/x86_64-linux-gnu/libboost_thread.so
ToolpathGenerator: /usr/lib/x86_64-linux-gnu/libboost_system.so
ToolpathGenerator: /usr/lib/x86_64-linux-gnu/libpthread.so
ToolpathGenerator: CMakeFiles/ToolpathGenerator.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/slawek/workspace/CppWorkspace/ToolpathGenerator/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable ToolpathGenerator"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/ToolpathGenerator.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/ToolpathGenerator.dir/build: ToolpathGenerator

.PHONY : CMakeFiles/ToolpathGenerator.dir/build

CMakeFiles/ToolpathGenerator.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/ToolpathGenerator.dir/cmake_clean.cmake
.PHONY : CMakeFiles/ToolpathGenerator.dir/clean

CMakeFiles/ToolpathGenerator.dir/depend:
	cd /home/slawek/workspace/CppWorkspace/ToolpathGenerator && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/slawek/workspace/CppWorkspace/ToolpathGenerator /home/slawek/workspace/CppWorkspace/ToolpathGenerator /home/slawek/workspace/CppWorkspace/ToolpathGenerator /home/slawek/workspace/CppWorkspace/ToolpathGenerator /home/slawek/workspace/CppWorkspace/ToolpathGenerator/CMakeFiles/ToolpathGenerator.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/ToolpathGenerator.dir/depend
