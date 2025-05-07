

set(US_WebConsole_LIBRARIES usWebConsole)
set(US_WebConsole_RUNTIME_LIBRARY_DIRS "/home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib/bin")

if(NOT TARGET usWebConsole)
  include("${CMAKE_CURRENT_LIST_DIR}/usWebConsoleTargets.cmake")
endif()
