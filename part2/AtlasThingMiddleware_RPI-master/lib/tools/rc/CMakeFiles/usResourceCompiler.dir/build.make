# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.25

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib/CppMicroServices-development

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib

# Include any dependencies generated for this target.
include tools/rc/CMakeFiles/usResourceCompiler.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include tools/rc/CMakeFiles/usResourceCompiler.dir/compiler_depend.make

# Include the progress variables for this target.
include tools/rc/CMakeFiles/usResourceCompiler.dir/progress.make

# Include the compile flags for this target's objects.
include tools/rc/CMakeFiles/usResourceCompiler.dir/flags.make

tools/rc/CMakeFiles/usResourceCompiler.dir/ResourceCompiler.cpp.o: tools/rc/CMakeFiles/usResourceCompiler.dir/flags.make
tools/rc/CMakeFiles/usResourceCompiler.dir/ResourceCompiler.cpp.o: /home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib/CppMicroServices-development/tools/rc/ResourceCompiler.cpp
tools/rc/CMakeFiles/usResourceCompiler.dir/ResourceCompiler.cpp.o: tools/rc/CMakeFiles/usResourceCompiler.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object tools/rc/CMakeFiles/usResourceCompiler.dir/ResourceCompiler.cpp.o"
	cd /home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib/tools/rc && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT tools/rc/CMakeFiles/usResourceCompiler.dir/ResourceCompiler.cpp.o -MF CMakeFiles/usResourceCompiler.dir/ResourceCompiler.cpp.o.d -o CMakeFiles/usResourceCompiler.dir/ResourceCompiler.cpp.o -c /home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib/CppMicroServices-development/tools/rc/ResourceCompiler.cpp

tools/rc/CMakeFiles/usResourceCompiler.dir/ResourceCompiler.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/usResourceCompiler.dir/ResourceCompiler.cpp.i"
	cd /home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib/tools/rc && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib/CppMicroServices-development/tools/rc/ResourceCompiler.cpp > CMakeFiles/usResourceCompiler.dir/ResourceCompiler.cpp.i

tools/rc/CMakeFiles/usResourceCompiler.dir/ResourceCompiler.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/usResourceCompiler.dir/ResourceCompiler.cpp.s"
	cd /home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib/tools/rc && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib/CppMicroServices-development/tools/rc/ResourceCompiler.cpp -o CMakeFiles/usResourceCompiler.dir/ResourceCompiler.cpp.s

tools/rc/CMakeFiles/usResourceCompiler.dir/__/__/third_party/miniz.c.o: tools/rc/CMakeFiles/usResourceCompiler.dir/flags.make
tools/rc/CMakeFiles/usResourceCompiler.dir/__/__/third_party/miniz.c.o: /home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib/CppMicroServices-development/third_party/miniz.c
tools/rc/CMakeFiles/usResourceCompiler.dir/__/__/third_party/miniz.c.o: tools/rc/CMakeFiles/usResourceCompiler.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building C object tools/rc/CMakeFiles/usResourceCompiler.dir/__/__/third_party/miniz.c.o"
	cd /home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib/tools/rc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT tools/rc/CMakeFiles/usResourceCompiler.dir/__/__/third_party/miniz.c.o -MF CMakeFiles/usResourceCompiler.dir/__/__/third_party/miniz.c.o.d -o CMakeFiles/usResourceCompiler.dir/__/__/third_party/miniz.c.o -c /home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib/CppMicroServices-development/third_party/miniz.c

tools/rc/CMakeFiles/usResourceCompiler.dir/__/__/third_party/miniz.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/usResourceCompiler.dir/__/__/third_party/miniz.c.i"
	cd /home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib/tools/rc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib/CppMicroServices-development/third_party/miniz.c > CMakeFiles/usResourceCompiler.dir/__/__/third_party/miniz.c.i

tools/rc/CMakeFiles/usResourceCompiler.dir/__/__/third_party/miniz.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/usResourceCompiler.dir/__/__/third_party/miniz.c.s"
	cd /home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib/tools/rc && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib/CppMicroServices-development/third_party/miniz.c -o CMakeFiles/usResourceCompiler.dir/__/__/third_party/miniz.c.s

tools/rc/CMakeFiles/usResourceCompiler.dir/__/__/third_party/jsoncpp.cpp.o: tools/rc/CMakeFiles/usResourceCompiler.dir/flags.make
tools/rc/CMakeFiles/usResourceCompiler.dir/__/__/third_party/jsoncpp.cpp.o: /home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib/CppMicroServices-development/third_party/jsoncpp.cpp
tools/rc/CMakeFiles/usResourceCompiler.dir/__/__/third_party/jsoncpp.cpp.o: tools/rc/CMakeFiles/usResourceCompiler.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building CXX object tools/rc/CMakeFiles/usResourceCompiler.dir/__/__/third_party/jsoncpp.cpp.o"
	cd /home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib/tools/rc && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT tools/rc/CMakeFiles/usResourceCompiler.dir/__/__/third_party/jsoncpp.cpp.o -MF CMakeFiles/usResourceCompiler.dir/__/__/third_party/jsoncpp.cpp.o.d -o CMakeFiles/usResourceCompiler.dir/__/__/third_party/jsoncpp.cpp.o -c /home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib/CppMicroServices-development/third_party/jsoncpp.cpp

tools/rc/CMakeFiles/usResourceCompiler.dir/__/__/third_party/jsoncpp.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/usResourceCompiler.dir/__/__/third_party/jsoncpp.cpp.i"
	cd /home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib/tools/rc && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib/CppMicroServices-development/third_party/jsoncpp.cpp > CMakeFiles/usResourceCompiler.dir/__/__/third_party/jsoncpp.cpp.i

tools/rc/CMakeFiles/usResourceCompiler.dir/__/__/third_party/jsoncpp.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/usResourceCompiler.dir/__/__/third_party/jsoncpp.cpp.s"
	cd /home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib/tools/rc && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib/CppMicroServices-development/third_party/jsoncpp.cpp -o CMakeFiles/usResourceCompiler.dir/__/__/third_party/jsoncpp.cpp.s

# Object files for target usResourceCompiler
usResourceCompiler_OBJECTS = \
"CMakeFiles/usResourceCompiler.dir/ResourceCompiler.cpp.o" \
"CMakeFiles/usResourceCompiler.dir/__/__/third_party/miniz.c.o" \
"CMakeFiles/usResourceCompiler.dir/__/__/third_party/jsoncpp.cpp.o"

# External object files for target usResourceCompiler
usResourceCompiler_EXTERNAL_OBJECTS =

bin/usResourceCompiler4: tools/rc/CMakeFiles/usResourceCompiler.dir/ResourceCompiler.cpp.o
bin/usResourceCompiler4: tools/rc/CMakeFiles/usResourceCompiler.dir/__/__/third_party/miniz.c.o
bin/usResourceCompiler4: tools/rc/CMakeFiles/usResourceCompiler.dir/__/__/third_party/jsoncpp.cpp.o
bin/usResourceCompiler4: tools/rc/CMakeFiles/usResourceCompiler.dir/build.make
bin/usResourceCompiler4: tools/rc/CMakeFiles/usResourceCompiler.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Linking CXX executable ../../bin/usResourceCompiler4"
	cd /home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib/tools/rc && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/usResourceCompiler.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
tools/rc/CMakeFiles/usResourceCompiler.dir/build: bin/usResourceCompiler4
.PHONY : tools/rc/CMakeFiles/usResourceCompiler.dir/build

tools/rc/CMakeFiles/usResourceCompiler.dir/clean:
	cd /home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib/tools/rc && $(CMAKE_COMMAND) -P CMakeFiles/usResourceCompiler.dir/cmake_clean.cmake
.PHONY : tools/rc/CMakeFiles/usResourceCompiler.dir/clean

tools/rc/CMakeFiles/usResourceCompiler.dir/depend:
	cd /home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib/CppMicroServices-development /home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib/CppMicroServices-development/tools/rc /home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib /home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib/tools/rc /home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib/tools/rc/CMakeFiles/usResourceCompiler.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : tools/rc/CMakeFiles/usResourceCompiler.dir/depend

