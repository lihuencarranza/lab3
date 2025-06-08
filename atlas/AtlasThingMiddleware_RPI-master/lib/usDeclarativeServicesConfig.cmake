

set(US_DeclarativeServices_LIBRARIES DeclarativeServices)
set(US_DeclarativeServices_RUNTIME_LIBRARY_DIRS "/home/lihuen/Documents/lab3/part2/AtlasThingMiddleware_RPI-master/lib/bin")

if(NOT TARGET DeclarativeServices)
  include("${CMAKE_CURRENT_LIST_DIR}/usDeclarativeServicesTargets.cmake")
endif()
