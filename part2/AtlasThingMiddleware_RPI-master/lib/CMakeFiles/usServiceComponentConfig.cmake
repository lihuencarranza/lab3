
####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was usBundleConfig.cmake.in                            ########

get_filename_component(PACKAGE_PREFIX_DIR "${CMAKE_CURRENT_LIST_DIR}/../../../" ABSOLUTE)

####################################################################################

set(US_ServiceComponent_LIBRARIES usServiceComponent)
set(US_ServiceComponent_RUNTIME_LIBRARY_DIRS "${PACKAGE_PREFIX_DIR}/bin/")

if(NOT TARGET usServiceComponent)
  include("${CMAKE_CURRENT_LIST_DIR}/usServiceComponentTargets.cmake")
endif()
