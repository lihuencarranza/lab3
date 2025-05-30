/*
  GlobalConfig.h
  this file is generated. Do not change!
*/

#ifndef CPPMICROSERVICES_GLOBALCONFIG_H
#define CPPMICROSERVICES_GLOBALCONFIG_H

#define US_BUILD_SHARED_LIBS
#define US_ENABLE_THREADING_SUPPORT
#define US_HAVE_VISIBILITY_ATTRIBUTE

//-------------------------------------------------------------------
// Header Availability
//-------------------------------------------------------------------

#define US_HAVE_CXXABI_H

//-------------------------------------------------------------------
// Version information
//-------------------------------------------------------------------

#define CppMicroServices_VERSION_MAJOR 4
#define CppMicroServices_VERSION_MINOR 0
#define CppMicroServices_VERSION_PATCH 0
#define CppMicroServices_VERSION 4.0.0
#define CppMicroServices_VERSION_STR "4.0.0"

#define US_VERSION_MAJOR 4
#define US_VERSION_MINOR 0
#define US_VERSION_PATCH 0
#define US_VERSION 4.0.0
#define US_VERSION_STR "4.0.0"

//-------------------------------------------------------------------
// Platform defines
//-------------------------------------------------------------------

#if defined(__APPLE__)
  #define US_PLATFORM_APPLE
#endif

#if defined(__linux__)
  #define US_PLATFORM_LINUX
#endif

#if defined(_WIN32) || defined(_WIN64)
  #define US_PLATFORM_WINDOWS
#else
  #define US_PLATFORM_POSIX
#endif

/* #undef US_BIG_ENDIAN */
#define US_LITTLE_ENDIAN

#define US_LIB_PREFIX "lib"
#define US_LIB_EXT ".so"
#define US_EXE_EXT ""

#ifdef NDEBUG // Defined by cmake UNLESS Debug build type is chosen
#define US_LIB_POSTFIX ""
#else
#define US_LIB_POSTFIX "d" // Set in top level CMakeList.txt
#endif

///-------------------------------------------------------------------
// Macros for import/export declarations
//-------------------------------------------------------------------

#if defined(US_PLATFORM_WINDOWS)
  #define US_ABI_EXPORT __declspec(dllexport)
  #define US_ABI_IMPORT __declspec(dllimport)
  #define US_ABI_LOCAL
#elif defined(US_HAVE_VISIBILITY_ATTRIBUTE)
  #define US_ABI_EXPORT __attribute__ ((visibility ("default")))
  #define US_ABI_IMPORT __attribute__ ((visibility ("default")))
  #define US_ABI_LOCAL  __attribute__ ((visibility ("hidden")))
#else
  #define US_ABI_EXPORT
  #define US_ABI_IMPORT
  #define US_ABI_LOCAL
#endif

//-------------------------------------------------------------------
// Macros for suppressing warnings
//-------------------------------------------------------------------

#ifdef _MSC_VER
#define US_MSVC_PUSH_DISABLE_WARNING(wn) \
__pragma(warning(push))                  \
__pragma(warning(disable:wn))
#define US_MSVC_POP_WARNING \
__pragma(warning(pop))
#define US_MSVC_DISABLE_WARNING(wn) \
__pragma(warning(disable:wn))
#else
#define US_MSVC_PUSH_DISABLE_WARNING(wn)
#define US_MSVC_POP_WARNING
#define US_MSVC_DISABLE_WARNING(wn)
#endif

#ifdef __GNUC__
#define us_gcc_pragma_expand(x) _Pragma (#x)
#define US_GCC_PUSH_DISABLE_WARNING(wn) \
_Pragma ("GCC diagnostic push") \
us_gcc_pragma_expand(GCC diagnostic ignored "-W" #wn)
#define US_GCC_POP_WARNING \
_Pragma ("GCC diagnostic pop")
#else
#define US_GCC_PUSH_DISABLE_WARNING(wn)
#define US_GCC_POP_WARNING
#endif

#if defined(__GNUC__)
  #define US_DEPRECATED __attribute__((deprecated))
#elif defined(_MSC_VER)
  #define US_DEPRECATED __declspec(deprecated)
#else
  #pragma message("WARNING: You need to implement US_DEPRECATED for your compiler!")
  #define US_DEPRECATED
#endif

// Do not warn about the usage of deprecated unsafe functions
US_MSVC_DISABLE_WARNING(4996)

// Mark a variable or expression result as unused
#define US_UNUSED(x) (void)(x)

//-------------------------------------------------------------------
// C++ Language features
//-------------------------------------------------------------------

#define US_HAVE_THREAD_LOCAL

//-------------------------------------------------------------------
// C++ Library features
//-------------------------------------------------------------------

#define US_HAVE_REGEX

//-------------------------------------------------------------------
// Hash Container
//-------------------------------------------------------------------

#define US_HASH_FUNCTION_BEGIN(type)                         \
namespace std {                                              \
template<>                                                   \
struct hash<type> { \
std::size_t operator()(const type& arg) const {

#define US_HASH_FUNCTION_END } }; }


//-------------------------------------------------------------------
// Utility macros
//-------------------------------------------------------------------

#define US_STR_(x) #x
#define US_STR(x) US_STR_(x)
#define US_CONCAT_(x,y) x ## y
#define US_CONCAT(x,y) US_CONCAT_(x,y)

#define US_GET_CTX_PREFIX _us_get_bundle_context_instance_
#define US_SET_CTX_PREFIX _us_set_bundle_context_instance_
#define US_CTX_INS_PREFIX _us_bundle_context_instance_

#define US_GET_CTX_FUNC(bsn) US_CONCAT(US_GET_CTX_PREFIX, bsn)
#define US_SET_CTX_FUNC(bsn) US_CONCAT(US_SET_CTX_PREFIX, bsn)
#define US_CTX_INS(bsn) US_CONCAT(US_CTX_INS_PREFIX, bsn)

#define US_CREATE_ACTIVATOR_PREFIX _us_create_activator_
#define US_DESTROY_ACTIVATOR_PREFIX _us_destroy_activator_

#define US_CREATE_ACTIVATOR_FUNC(bsn) US_CONCAT(US_CREATE_ACTIVATOR_PREFIX, bsn)
#define US_DESTROY_ACTIVATOR_FUNC(bsn) US_CONCAT(US_DESTROY_ACTIVATOR_PREFIX, bsn)


//-------------------------------------------------------------------
// Backwards compatibility macros
//-------------------------------------------------------------------

#if !defined(__clang__) && __GNUC__ == 4 && __GNUC_MINOR__ < 7
#define US_FUTURE_READY true
#define US_FUTURE_TIMEOUT false
#else
#define US_FUTURE_READY std::future_status::ready
#define US_FUTURE_TIMEOUT std::future_status::timeout
#endif

#endif // CPPMICROSERVICES_GLOBALCONFIG_H
