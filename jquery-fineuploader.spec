%define		plugin	fineuploader
Summary:	Multiple file upload plugin with progress-bar, drag-and-drop
Name:		jquery-%{plugin}
Version:	3.7.1
Release:	1
License:	GPL v3
Group:		Applications/WWW
Source0:	https://github.com/Widen/fine-uploader/archive/%{version}.tar.gz?/%{plugin}-%{version}.tgz
# Source0-md5:	a0d7c906c1cc4f1894659f43898f4347
URL:		http://fineuploader.com/
BuildRequires:	closure-compiler
BuildRequires:	js
BuildRequires:	unzip
BuildRequires:	yuicompressor
Requires:	jquery >= 1.5
#Obsoletes:	js-ajax-upload
#Obsoletes:	js-fileuploader
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir	%{_datadir}/jquery/%{plugin}

%description
This project attempts to achieve a user-friendly file-uploading
experience over the web. It's built as a Javascript plugin for
developers looking to incorporate file-uploading into their website.

This plugin uses an XMLHttpRequest (AJAX) for uploading multiple files
with a progress-bar in FF3.6+, Safari4+, Chrome and falls back to
hidden-iframe-based upload in other browsers (namely IE), providing
good user experience everywhere.

It does not use Flash, jQuery, or any external libraries.

%package demo
Summary:	Demo for %{plugin}
Summary(pl.UTF-8):	Pliki demonstracyjne dla pakietu %{plugin}
Group:		Development
Requires:	%{name} = %{version}-%{release}

%description demo
Demonstrations and samples for %{plugin}.

%prep
%setup -q -n fine-uploader-%{version}

%build
install -d build

# pack .css
for css in client/*.css; do
	out=build/${css#*/}
%if 0%{!?debug:1}
	yuicompressor --charset UTF-8 $css -o $out
%else
	cp -p $css $out
%endif
done

# combine .js, based on Gruntfile.coffee
coreFiles=client/js/{util,version,features,promise,button,paste,upload-data,uploader.basic,dnd,uploader,ajax.requester,deletefile.ajax.requester,window.receive.message,handler.{base,form,xhr},ui.handler.{events,click.drc,edit.filename,click.filename,focusin.filenameinput,focus.filenameinput}}.js
jQueryPluginFiles=client/js/jquery-{plugin,dnd}.js

cat $coreFiles > build/%{plugin}.js
cat $coreFiles $jQueryPluginFiles > build/jquery.%{plugin}.js

# compress .js
for js in build/*.js; do
	fn=${js#*/}
	out=build/${fn%*.js}.min.js
	%if 0%{!?debug:1}
	closure-compiler --js $js --charset UTF-8 --js_output_file $out
	js -C -f $out
	%else
	cp -p $js $out
	%endif
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_examplesdir}/%{name}-%{version}}
cp -p build/jquery.%{plugin}.min.js $RPM_BUILD_ROOT%{_appdir}/%{plugin}-%{version}.min.js
cp -p build/jquery.%{plugin}.js $RPM_BUILD_ROOT%{_appdir}/%{plugin}-%{version}.js
ln -s %{plugin}-%{version}.min.js $RPM_BUILD_ROOT%{_appdir}/%{plugin}.js

# package plain js version too
cp -p build/%{plugin}.min.js $RPM_BUILD_ROOT%{_appdir}/js.%{plugin}-%{version}.min.js
cp -p build/%{plugin}.js $RPM_BUILD_ROOT%{_appdir}/js.%{plugin}-%{version}.js
ln -s js.%{plugin}-%{version}.min.js $RPM_BUILD_ROOT%{_appdir}/js.%{plugin}.js

cp -p client/%{plugin}.css $RPM_BUILD_ROOT%{_appdir}/%{plugin}-%{version}.css
cp -p build/%{plugin}.css $RPM_BUILD_ROOT%{_appdir}/%{plugin}-%{version}.min.css
ln -s %{plugin}-%{version}.min.css $RPM_BUILD_ROOT%{_appdir}/%{plugin}.css

cp -p client/loading.gif  $RPM_BUILD_ROOT%{_appdir}

cp -a test/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_appdir}

%files demo
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
