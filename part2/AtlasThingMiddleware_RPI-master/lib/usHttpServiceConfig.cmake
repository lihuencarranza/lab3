

set(US_HttpService_LIBRARIES usHttpService)
set(US_HttpService_RUNTIME_LIBRARY_DIRS "/home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib/bin")

if(NOT TARGET usHttpService)
  include("${CMAKE_CURRENT_LIST_DIR}/usHttpServiceTargets.cmake")
endif()
