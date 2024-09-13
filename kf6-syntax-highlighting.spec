%define major %(echo %{version} |cut -d. -f1-2)
%define stable %([ "$(echo %{version} |cut -d. -f2)" -ge 80 -o "$(echo %{version} |cut -d. -f3)" -ge 80 ] && echo -n un; echo -n stable)

%define libname %mklibname KF6SyntaxHighlighting
%define devname %mklibname KF6SyntaxHighlighting -d
#define git 20240217

Name: kf6-syntax-highlighting
Version: 6.6.0
Release: %{?git:0.%{git}.}1
%if 0%{?git:1}
Source0: https://invent.kde.org/frameworks/syntax-highlighting/-/archive/master/syntax-highlighting-master.tar.bz2#/syntax-highlighting-%{git}.tar.bz2
%else
Source0: https://download.kde.org/%{stable}/frameworks/%{major}/syntax-highlighting-%{version}.tar.xz
%endif
Summary: Syntax highlighting Engine for Structured Text and Code
URL: https://invent.kde.org/frameworks/syntax-highlighting
License: CC0-1.0 LGPL-2.0+ LGPL-2.1 LGPL-3.0
Group: System/Libraries
BuildRequires: cmake
BuildRequires: cmake(ECM)
BuildRequires: python
BuildRequires: cmake(Qt6DBusTools)
BuildRequires: cmake(Qt6DBus)
BuildRequires: cmake(Qt6Network)
BuildRequires: cmake(Qt6Test)
BuildRequires: cmake(Qt6QmlTools)
BuildRequires: cmake(Qt6Qml)
BuildRequires: cmake(Qt6GuiTools)
BuildRequires: cmake(Qt6QuickTest)
BuildRequires: cmake(Qt6DBusTools)
BuildRequires: gettext
BuildRequires: doxygen
BuildRequires: cmake(Qt6ToolsTools)
BuildRequires: cmake(Qt6)
BuildRequires: cmake(Qt6QuickTest)
BuildRequires: cmake(Qt6PrintSupport)
BuildRequires: cmake(Qt6Quick)
BuildRequires: pkgconfig(xerces-c)
Requires: %{libname} = %{EVRD}
Obsoletes: kate-syntax-highlighter < %{EVRD}

%description
Syntax highlighting Engine for Structured Text and Code

%package -n %{libname}
Summary: Syntax highlighting Engine for Structured Text and Code
Group: System/Libraries
Requires: %{name} = %{EVRD}

%description -n %{libname}
Syntax highlighting Engine for Structured Text and Code

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{libname} = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

Syntax highlighting Engine for Structured Text and Code

%prep
%autosetup -p1 -n syntax-highlighting-%{?git:master}%{!?git:%{version}}
%cmake \
	-DBUILD_QCH:BOOL=ON \
	-DBUILD_WITH_QT6:BOOL=ON \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build

# FIXME for some reason, find_lang misidentifies the language
# for locale files as LC_MESSAGES/syntaxhighlighting, so let's
# do it manually for now
for i in %{buildroot}%{_datadir}/locale/*/*/*.qm; do
	echo "%lang($(echo $i |rev |cut -d/ -f3 |rev)) /$(echo $i |rev |cut -d/ -f1-6 |rev)" >>%{name}.lang
done

%files -f %{name}.lang
%{_datadir}/qlogging-categories6/ksyntaxhighlighting.*
%{_bindir}/ksyntaxhighlighter6

%files -n %{devname}
%{_includedir}/KF6/KSyntaxHighlighting
%{_libdir}/cmake/KF6SyntaxHighlighting
%{_qtdir}/doc/KF6SyntaxHighlighting.*

%files -n %{libname}
%{_libdir}/libKF6SyntaxHighlighting.so*
%{_qtdir}/qml/org/kde/syntaxhighlighting
