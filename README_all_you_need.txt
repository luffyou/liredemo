HOW TO RUN LIREDEMO
===================
Linux:
$> gradlew runDemo

may need ops:
    Could not find tools.jar. Please check that /usr/lib/jvm/java-8-openjdk-amd64 contains a valid JDK installation.
    sudo apt install openjdk-8-jdk
    chmod +x gradlew
    sudo gradlew runDemo

open in intellij IDEA:
    open as project through build.gradle
        will run gradle wraper
        download apache jar to /root/ or /home/user
    run cp_lib_for_custombuild.xml
    find ant plugin in IDEA
    modify custombuild.xml
        rename jar for wrong version
        rename main class
    run ant build
    find jar and lib in dist

dir path:
    wrong path of index and corespending img may cause exception
    solve this through specify dir or make soft link

Windows:
D:\TEMP\> gradlew.bat runDemo