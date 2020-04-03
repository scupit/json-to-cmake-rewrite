
TOGGLING_LIBRARY_CREATOR = """function( createLibraryWithTypeToggle libName libType libSources )
  if( libType STREQUAL STATIC )
    set( oppositeLibType SHARED )
  elseif( libType STREQUAL SHARED )
    set( oppositeLibType STATIC )
  endif()

  if( NOT ${libName}_LIB_TYPE )
    set( ${libName}_LIB_TYPE ${libType} CACHE STRING "${libName} library type" FORCE )
  endif()

  set_property( CACHE ${libName}_LIB_TYPE PROPERTY STRINGS "${libType}" "${oppositeLibType}" )

  if( ${libName}_LIB_TYPE STREQUAL ${libType} )
    add_library( ${libName} ${libType} ${libSources} )
  elseif( ${libName}_LIB_TYPE STREQUAL ${oppositeLibType} )
    add_library( ${libName} ${oppositeLibType} ${libSources} )
  endif()
endFunction()
"""