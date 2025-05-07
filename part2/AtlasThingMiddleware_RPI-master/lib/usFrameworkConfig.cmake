

set(US_Framework_LIBRARIES CppMicroServices)
set(US_Framework_RUNTIME_LIBRARY_DIRS "/home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib/bin")

if(NOT TARGET CppMicroServices)
  include("${CMAKE_CURRENT_LIST_DIR}/usFrameworkTargets.cmake")
endif()
