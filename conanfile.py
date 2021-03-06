#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools ,CMake
from conans.errors import ConanException
import os
import shutil


class KirigamiConan(ConanFile):
    name = "Kirigami"
    version = "5.80.0"
    description = "Kirigami is a set of QtQuick components at the moment targeted for mobile use (in the future desktop as well) targeting both Plasma Mobile and Android"
    url = "https://github.com/Tereius/conan-kirigami"
    homepage = "https://invent.kde.org/frameworks/kirigami"
    license = "GNU LGPL-2.0"
    settings = ("os", "compiler", "arch", "build_type")
    requires = "Qt/[^5.14]@tereius/stable"
    generators = "cmake"
    default_options = (
        "Qt:shared=True",
        "Qt:GUI=True",
        "Qt:widgets=True",
        "Qt:openssl=True",
        "Qt:qtbase=True",
        "Qt:qtsvg=True",
        "Qt:qtdeclarative=True",
        "Qt:qttools=True",
        "Qt:qttranslations=True",
        "Qt:qtgraphicaleffects=True",
        "Qt:qtquickcontrols2=True")

    def build_requirements(self):
        self.build_requires("extra-cmake-modules/5.80.0@tereius/stable", force_host_context=True)

    def configure(self):
        if self.settings.os == 'Android':
            self.options["Qt"].qtandroidextras = True

    def source(self):
        source_url = "https://invent.kde.org/frameworks/kirigami/-/archive/v{0}/kirigami-v{0}.zip".format(self.version)
        tools.get(source_url)
        tools.replace_in_file(os.path.join("kirigami-v%s" % self.version, "CMakeLists.txt"), "################# Disallow in-source build #################",
                              'if (EXISTS "${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")\n \
                               include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")\n \
                               conan_basic_setup(KEEP_RPATHS)\n \
                               endif ()')
        
    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="kirigami-v%s" % self.version)
        cmake.build()
        cmake.install()

    def package_info(self):
        self.env_info.QML_IMPORT_PATH.append(os.path.join(self.package_folder, "lib", "qml"))
