INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_SPP spp)

FIND_PATH(
    SPP_INCLUDE_DIRS
    NAMES spp/api.h
    HINTS $ENV{SPP_DIR}/include
        ${PC_SPP_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    SPP_LIBRARIES
    NAMES gnuradio-spp
    HINTS $ENV{SPP_DIR}/lib
        ${PC_SPP_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(SPP DEFAULT_MSG SPP_LIBRARIES SPP_INCLUDE_DIRS)
MARK_AS_ADVANCED(SPP_LIBRARIES SPP_INCLUDE_DIRS)

