#----------------------------------------------------------------
# Generated CMake target import file for configuration "Debug".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "DeclarativeServices" for configuration "Debug"
set_property(TARGET DeclarativeServices APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(DeclarativeServices PROPERTIES
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/lib/libDeclarativeServicesd.so.1.0.0"
  IMPORTED_SONAME_DEBUG "libDeclarativeServicesd.so.1.0.0"
  )

list(APPEND _cmake_import_check_targets DeclarativeServices )
list(APPEND _cmake_import_check_files_for_DeclarativeServices "${_IMPORT_PREFIX}/lib/libDeclarativeServicesd.so.1.0.0" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
