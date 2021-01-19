INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_USRP_PACK usrp_pack)

FIND_PATH(
    USRP_PACK_INCLUDE_DIRS
    NAMES usrp_pack/api.h
    HINTS $ENV{USRP_PACK_DIR}/include
        ${PC_USRP_PACK_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    USRP_PACK_LIBRARIES
    NAMES gnuradio-usrp_pack
    HINTS $ENV{USRP_PACK_DIR}/lib
        ${PC_USRP_PACK_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(USRP_PACK DEFAULT_MSG USRP_PACK_LIBRARIES USRP_PACK_INCLUDE_DIRS)
MARK_AS_ADVANCED(USRP_PACK_LIBRARIES USRP_PACK_INCLUDE_DIRS)

