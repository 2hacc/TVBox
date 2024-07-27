dnl init
dnl AC_REVISION($Revision: 1.30 $)
AC_PREREQ([2.60])
AC_INIT([chan_quectel],[1.1],[https://github.com/bg111/asterisk-chan-quectel/issues],[chan_quectel],[https://github.com/bg111/asterisk-chan-quectel/])
PACKAGE_REVISION="43gh=47cg"
AC_CANONICAL_TARGET
AM_INIT_AUTOMAKE
AC_CONFIG_HEADERS([config.h])
AC_CONFIG_SRCDIR([chan_quectel.c])
AC_CONFIG_FILES([stamp-h], [echo timestamp > stamp-h])
AC_CANONICAL_SYSTEM
AC_CANONICAL_HOST

dnl AM_INIT_AUTOMAKE

CPPFLAGS="$CPPFLAGS -D_GNU_SOURCE"

dnl Checks for user settings.
dnl  Set asterisk headers patch
AC_ARG_WITH(
	[asterisk],
	AS_HELP_STRING([--with-asterisk=path], [set asterisk headers location]),
	[ if test "x$with_asterisk" = "xyes" -o "x$with_asterisk" = "xno" ; then  AC_MSG_ERROR([Invalid --with-asterisk=path value]); fi ],
	[ with_asterisk="../include /usr/include /usr/local/include /opt/local/include" ]
)
dnl  Set iconv headers patch
AC_ARG_WITH(
	[iconv],
	AS_HELP_STRING([--with-iconv=path], [set iconv headers location]),
	[ if test "x$with_iconv" = "xyes" -o "x$with_iconv" = "xno" ; then  AC_MSG_ERROR([Invalid --with-iconv=path value]); fi ],
	[ with_iconv="../include /usr/include /usr/local/include /opt/local/include" ]
)

dnl  Required: asterisk version
AC_ARG_WITH(
	[astversion],
	AS_HELP_STRING([--with-astversion=M.m.u], [set asterisk version; for example: 14 or 13.13.1]),
	[ if echo "$with_astversion" | grep -qE '^[[0-9]][[0-9]]?(\.[[0-9]][[0-9]]?){0,2}$'
          then with_astversion=$(echo $with_astversion | sed -e 's/.*/&.0.0/' | tr . '\n' |
				 head -n3 | sed -e 's/^.$/0&/' | tr -d '\n' | sed -e 's/^0*//')
	  else AC_MSG_ERROR([Invalid --with-astversion=M.m.u value]); fi ],
	[ AC_MSG_ERROR([Please set --with-astversion=M.m.u (major.minor.micro)]) ]
)
AC_DEFINE_UNQUOTED([ASTERISK_VERSION_NUM], [$with_astversion],
		   [The Asterisk version as configured --with-astversion.])

AC_ARG_ENABLE(
	[debug], 
	AS_HELP_STRING([--enable-debug], [enable code debugging]),
	[ if test "x$enable_debug" != "xyes" ; then enable_debug="no" ; fi],
	[ enable_debug="no"]
)

dnl  Optionally disable manager.
AC_ARG_ENABLE(
	[manager],
	AS_HELP_STRING([--enable-manager], [enable manager code]),
	[ if test "x$enable_manager" != "xyes" ; then enable_manager="no" ; fi ],
	[ enable_manager="yes" ]
)

dnl  Optionally disable applications
AC_ARG_ENABLE(
	[apps],
	AS_HELP_STRING([--enable-apps], [enable applications code]),
	[ if test "x$enable_apps" != "xyes" ; then enable_apps="no" ; fi],
	[ enable_apps="yes" ]
)

dnl Checks for programs.
AC_PROG_CC([gcc cl cc])
AC_PROG_CPP
AC_PROG_INSTALL

AC_CHECK_PROG(STRIP,strip,strip)
if test -z "$STRIP" ; then
    AC_MSG_ERROR([Can't find strip])
fi
AC_CHECK_PROG(RM,rm,rm)
if test -z "$RM" ; then
    AC_MSG_ERROR([Can't find rm])
fi

dnl Checks for libraries.
dnl AC_CHECK_LIB([pthread], [pthread_create])  # should use ast_pthread_join everywhere?
AC_SEARCH_LIBS([iconv], [c iconv],,AC_MSG_ERROR([iconv library missing]))
AC_CHECK_LIB([sqlite3], [sqlite3_open],,AC_MSG_ERROR([sqlite3 library missing]))

dnl Checks for header files.
AC_CHECK_HEADERS([fcntl.h stdlib.h string.h sys/time.h termios.h])
AC_DEFUN([AC_HEADER_FIND], [
    file=$1
    found=no
    for path in $2 ; do
	AC_MSG_CHECKING([whether $file in $path])
	if test -f $path/$file ; then
	    found="yes"
	    CPPFLAGS="$CPPFLAGS -I${path}"
	    AC_MSG_RESULT([yes])
	    AC_CHECK_HEADER([$file])
	    break;
	fi
	AC_MSG_RESULT([no])
    done
    if test "$found" = "no"; then
	AC_MSG_ERROR([Can't find "$file"])
    fi
    ]
)

AC_HEADER_FIND([asterisk.h], $with_asterisk)
AC_HEADER_FIND([iconv.h], $with_iconv)
AC_CHECK_HEADER([sqlite3.h],,AC_MSG_ERROR([sqlite3.h header file missing]))

AC_DEFINE([ICONV_CONST],[], [Define to const if you has iconv() const declaration of input buffer])
AC_MSG_CHECKING([for iconv use const inbuf])
AC_EGREP_HEADER([^extern.+iconv[[:space:]]*\(.+const], [iconv.h], 
    [
    AC_DEFINE([ICONV_CONST],[const])
    AC_MSG_RESULT([yes])
    ],
    [AC_MSG_RESULT([no])]
)

AC_MSG_CHECKING([for iconv_t in iconv.h])
AC_EGREP_HEADER([iconv_t], [iconv.h], 
    [
    AC_DEFINE([ICONV_T], [iconv_t], , [Define to iconv_t if you has iconv_t in iconv.h])
    AC_MSG_RESULT(yes)
    ],
    [

    AC_DEFINE([ICONV_T], [int], [Define to iconv_t if you has iconv_t in iconv.h])
    AC_MSG_RESULT(no)
    ])

AC_MSG_CHECKING([for AST_CONTROL_SRCCHANGE in asterisk/frame.h])
AC_EGREP_HEADER([AST_CONTROL_SRCCHANGE], [asterisk/frame.h], 
    [
    AC_DEFINE([HAVE_AST_CONTROL_SRCCHANGE], [], [Define to 1 if you have HAVE_AST_CONTROL_SRCCHANGE in asterisk/frame.h])
    AC_MSG_RESULT([yes])
    ],
    [AC_MSG_RESULT([no])]
)


dnl Checking for library options

dnl Checks for typedefs, structures, and compiler characteristics.
AC_C_CONST
AC_C_INLINE
AC_TYPE_SIZE_T
AC_TYPE_SSIZE_T
AC_TYPE_UINT64_T
dnl AC_CHECK_TYPE(size_t, unsigned long)
dnl AC_CHECK_TYPE(ssize_t, long)
dnl AC_CHECK_TYPE(uint64_t, unsigned long long)

dnl checking compiler options
AC_DEFUN([AC_CC_OPT], [
    my_save_cflags="$CFLAGS"
    CFLAGS="$1"
    AC_MSG_CHECKING([whether CC supports $1])
    AC_COMPILE_IFELSE([AC_LANG_PROGRAM([])],
    [AC_MSG_RESULT([yes])]
    [AC_CFLAGS="$AC_CFLAGS $2"],
    [AC_MSG_RESULT([no])]
    )
    CFLAGS="$my_save_cflags"]
    )

AC_CFLAGS=

my_save_cflags="$CFLAGS"
CFLAGS=-fvisibility=hidden
AC_MSG_CHECKING([whether CC supports -fvisibility=hidden])
AC_COMPILE_IFELSE([AC_LANG_PROGRAM([])],
    [AC_MSG_RESULT([yes])]
    [TARGET="chan_quectel.so"]
    [AC_CFLAGS="$AC_CFLAGS -fvisibility=hidden"],
    [AC_MSG_RESULT([no])]
    [TARGET="chan_quectels.so"]
    )
CFLAGS="$my_save_cflags"
AC_SUBST([TARGET])

AC_CC_OPT([-fPIC],[-fPIC])
AC_CC_OPT([-Wall],[-Wall])
AC_CC_OPT([-Wextra],[-Wextra])
AC_CC_OPT([-MD -MT conftest.o -MF /dev/null -MP],[-MD -MT \$@ -MF .\$(subst /,_,\$@).d -MP])

AC_DEFUN([AC_CHECK_DESTDIR], [
    if test -z "$DESTDIR" ; then
	found=no
	for path in $1 ; do
	    AC_MSG_CHECKING([whether DESTDIR is $path])
	    if test -f $path/pbx_config.so ; then
		AC_MSG_RESULT([yes])
		found="yes"
		DESTDIR=$path
		break;
	    fi
	    AC_MSG_RESULT([no])
	done
	if test "$found" = "no"; then
	    AC_MSG_ERROR([DESTDIR is unknown, please be explicit: ./configure DESTDIR=/usr/lib/asterisk/modules])
	fi
    fi
    ])

dnl This detection is kind of flaky. Don't rely on it. The module
dnl directory could be lib64 or x86_64-linux-gnu or even somewhere
dnl completely custom.
AC_CHECK_DESTDIR([ \
    /usr/lib/asterisk/modules /usr/lib64/asterisk/modules \
    /usr/local/lib/asterisk/modules /opt/local/lib/asterisk/modules])

dnl Checks for library functions.
AC_FUNC_MEMCMP
AC_CHECK_FUNCS([memchr memmove memset memmem strcasecmp strchr strncasecmp strtol realpath])


dnl Apply options to defines
if test "x$enable_debug" = "xyes" ; then
  CFLAGS="$CFLAGS -O0 -g"
  AC_DEFINE([__DEBUG__], [1], [Build with debugging])
else
  CFLAGS="$CFLAGS -O6"
fi

dnl Asterisk header files use lots of old style declarations, ignore those.
dnl > warning: ‘inline’ is not at beginning of declaration [-Wold-style-declaration]
dnl >   static void force_inline _ast_assert(...)
CFLAGS="$CFLAGS -Wno-old-style-declaration"

if test "x$enable_manager" = "xyes" ; then
  AC_DEFINE([BUILD_MANAGER],[1], [Build Manager extensions])
fi

if test "x$enable_apps" = "xyes" ; then
  AC_DEFINE([BUILD_APPLICATIONS],[1],[Build Application extensions])
fi

case "$target_os" in
    linux*)
	SOLINK="-shared -Xlinker -x"
	DC_LDFLAGS=""
	;;
    freebsd*)
	SOLINK="-shared -Xlinker -x"
	DC_LDFLAGS="-L/usr/local/lib"
	;;
    openbsd*)
	SOLINK="-shared -Xlinker -x"
	DC_LDFLAGS="-L/usr/local/lib -pthread"
	AC_CFLAGS="$AC_CFLAGS -pthread"
	;;
    darwin*)
	SOLINK="-dynamic -bundle -Xlinker -macosx_version_min -Xlinker 10.4 -Xlinker -undefined -Xlinker dynamic_lookup -force_flat_namespace"
	DC_LDFLAGS="-L/opt/local/lib"
	[ `/usr/bin/sw_vers -productVersion | cut -c1-4` == "10.6" ] && SOLINK="$SOLINK /usr/lib/bundle1.o"
esac

LDFLAGS="$LDFLAGS $DC_LDFLAGS"

dnl AC_DEFINE_UNQUOTED([MODULE_], "$PACKAGE_", [])
dnl AC_DEFINE_UNQUOTED([MODULE_], "$PACKAGE_", [])
AC_DEFINE_UNQUOTED([MODULE_BUGREPORT], "$PACKAGE_BUGREPORT", [Define to the address where bug reports for this package should be sent])
AC_DEFINE_UNQUOTED([MODULE_URL], "$PACKAGE_URL", [Define to the home page for this package])
AC_DEFINE_UNQUOTED([MODULE_VERSION], "$PACKAGE_VERSION", [Define to the version of this package])
AC_DEFINE_UNQUOTED([AST_MODULE],"$PACKAGE_NAME",[name of asterisk module])
AC_DEFINE_UNQUOTED([PACKAGE_REVISION], "$PACKAGE_REVISION",[Revision of package])

AC_SUBST([SOLINK])
AC_SUBST([PACKAGE_TARNAME])
AC_SUBST([PACKAGE_REVISION])
AC_SUBST([PACKAGE_VERSION])
AC_SUBST([DESTDIR])
AC_SUBST([AC_CFLAGS])
AC_CONFIG_FILES([Makefile])
AC_OUTPUT
