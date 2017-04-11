%{?_javapackages_macros:%_javapackages_macros}
%global namedreltag -rc5
%global namedversion %{version}%{?namedreltag}
Name:          jcsp
Version:       1.1
Release:       0 #0.6.rc5%{?dist}
Summary:       Communicating Sequential Processes for Java (JCSP)
License:       LGPLv2+
URL:           https://github.com/codehaus/jcsp
# sh jcsp-create-tarball.sh < VERSION-TAG >
Source0:       %{name}-%{namedversion}-clean.tar.xz
Source1:       %{name}-create-tarball.sh

BuildRequires: maven-local
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires: mvn(org.apache.felix:org.osgi.core)

BuildArch:     noarch

%description
JCSP (Communication Sequential Processes for Java) is a
library providing a concurrency model that is a combination
of ideas from Hoare's CSP and Milner's pi-calculus.

Communicating Sequential Processes (CSP) is a mathematical
theory for specifying and verifying complex patterns of
behavior arising from interactions between concurrent
objects.

JCSP provides a base range of CSP primitives plus a rich set of
extensions. Also included is a package providing CSP process
wrappers giving a channel interface to all Java AWT widgets
and graphics operations.  It is extensively (java/documented)
and includes much teaching.

JCSP is an alternative concurrency model to the threads and
mechanisms built into Java. It is also compatible with
it since it is implemented on top of it.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{name}-%{namedversion}

%pom_remove_plugin :cobertura-maven-plugin
%pom_remove_plugin :findbugs-maven-plugin
%pom_remove_plugin :jdepend-maven-plugin
%pom_remove_plugin :rat-maven-plugin
%pom_remove_plugin :taglist-maven-plugin

# remove wagon-webdav
%pom_xpath_remove "pom:project/pom:build/pom:extensions"
# fix resouce directory and filter these ones
%pom_xpath_inject "pom:project/pom:build" "
<resources>
  <resource>
    <directory>src</directory>
    <excludes>
      <exclude>**/*.java</exclude>
      <exclude>**/doc-files/**</exclude>
      <exclude>**/win32/*Services.txt</exclude>
      <exclude>**/package.html</exclude>
    </excludes>
  </resource>
</resources>"

%pom_xpath_remove "pom:project/pom:reporting/pom:plugins/pom:plugin[pom:artifactId='maven-javadoc-plugin']/pom:configuration/pom:excludePackageNames"

%pom_xpath_remove "pom:project/pom:build/pom:plugins/pom:plugin[pom:artifactId='maven-bundle-plugin']/pom:configuration/pom:instructions/pom:Export-Package"
%pom_xpath_inject "pom:project/pom:build/pom:plugins/pom:plugin[pom:artifactId='maven-bundle-plugin']/pom:configuration/pom:instructions" '
<Export-Package>org.jcsp.*;version="${project.version}"</Export-Package>'

sed -i 's|${name}|${project.name}|' pom.xml

sed -i "s|59 Temple Place, Suite 330, Boston, MA 02111-1307 USA|51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA|" pom.xml

for d in LICENCE README ; do
  iconv -f iso8859-1 -t utf-8 $d.txt > $d.txt.conv && mv -f $d.txt.conv $d.txt
  sed -i 's/\r//' $d.txt
done

rm -r src/org/jcsp/win32 \
 src/org/jcsp/net/remote/SpawnerServiceNT.java \
 src/org/jcsp/net/tcpip/TCPIPCNSServerNT.java

%mvn_file : %{name}

%build

%mvn_build -- -Dproject.build.sourceEncoding=UTF-8

%install
%mvn_install

%files -f .mfiles
%doc README.txt
%doc LICENCE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENCE.txt

%changelog
* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-0.6.rc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-0.5.rc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-0.4.rc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Feb 06 2015 gil cattaneo <puntogil@libero.it> 1.1-0.3.rc5
- introduce license macro

* Fri Oct 31 2014 gil cattaneo <puntogil@libero.it> 1.1-0.2.rc5
- remove win32 java stuff
- fix description

* Tue Sep 04 2012 gil cattaneo <puntogil@libero.it> 1.1-0.1.rc5
- initial rpm
