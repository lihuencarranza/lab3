///-------------------------------------------------------------------
// Macros for import/export declarations
//-------------------------------------------------------------------

#ifndef CPPMICROSERVICES_ServiceComponentEXPORT_H
#define CPPMICROSERVICES_ServiceComponentEXPORT_H

#include "cppmicroservices/GlobalConfig.h"

#ifdef US_BUILD_SHARED_LIBS
  // We are building a shared lib
  #ifdef usServiceComponent_EXPORTS
    #define US_ServiceComponent_EXPORT US_ABI_EXPORT
  #else
    #define US_ServiceComponent_EXPORT US_ABI_IMPORT
  #endif
#else
  // We are building a static lib
  // Don't hide RTTI symbols of definitions in the C++ Micro Services
  // headers that are included in DSOs with hidden visibility
  #define US_ServiceComponent_EXPORT US_ABI_EXPORT
#endif

#endif // CPPMICROSERVICES_ServiceComponentEXPORT_H
