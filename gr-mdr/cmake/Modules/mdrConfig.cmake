INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_MDR mdr)

FIND_PATH(
    MDR_INCLUDE_DIRS
    NAMES mdr/api.h
    HINTS $ENV{MDR_DIR}/include
        ${PC_MDR_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    MDR_LIBRARIES
    NAMES gnuradio-mdr
    HINTS $ENV{MDR_DIR}/lib
        ${PC_MDR_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/mdrTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(MDR DEFAULT_MSG MDR_LIBRARIES MDR_INCLUDE_DIRS)
MARK_AS_ADVANCED(MDR_LIBRARIES MDR_INCLUDE_DIRS)
