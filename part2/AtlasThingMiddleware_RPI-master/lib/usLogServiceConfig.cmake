

set(US_LogService_LIBRARIES usLogService)
set(US_LogService_RUNTIME_LIBRARY_DIRS "/home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib/bin")

if(NOT TARGET usLogService)
  include("${CMAKE_CURRENT_LIST_DIR}/usLogServiceTargets.cmake")
endif()
