from conans import ConanFile, CMake
from os import environ


class SECP256K1Conan(ConanFile):
    name = "SECP256K1"
    version = "0.1"
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of SECP256K1 here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "cmake"
    exports_sources = "*"
    requires = "autoconf/2.71", "automake/1.16.3", "libtool/2.4.6"

    def set_version(self):
        if "CIRCLE_TAG" in environ:
            self.version = environ.get("CIRCLE_TAG")[1:]

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def build(self):
        self.run("./autogen.sh")
        self.run("./configure --disable-debug --disable-dependency-tracking --disable-silent-rules --prefix=$(pwd)")
        self.run("make install")

    def package(self):
        self.copy("*.h", dst="include", src="include")

        if self.options.shared == False:
            self.copy("*.a", dst="lib", keep_path=False)
            self.copy("*.lib", dst="lib", keep_path=False)
        else:
            self.copy("*.lib", dst="lib", keep_path=False)
            self.copy("*.dll", dst="bin", keep_path=False)
            self.copy("*.dylib*", dst="lib", keep_path=False)
            self.copy("*.so", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["secp256k1"]
