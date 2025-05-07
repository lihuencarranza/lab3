

set(US_ServiceComponent_LIBRARIES usServiceComponent)
set(US_ServiceComponent_RUNTIME_LIBRARY_DIRS "/home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib/bin")

if(NOT TARGET usServiceComponent)
  include("${CMAKE_CURRENT_LIST_DIR}/usServiceComponentTargets.cmake")
endif()
