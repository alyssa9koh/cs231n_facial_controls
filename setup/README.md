This is a Windows-specific guide for setting up our project.

# Setting up OpenFace with ZeroMQ

Credits: This setup process was developed by NumesSanguis as part of [FACSvatar](https://github.com/NumesSanguis/FACSvatar). It has been modified for our project. See [this issue](https://github.com/TadasBaltrusaitis/OpenFace/issues/375) for more information.

1. Download OpenFace 2.1.0 source code from [the OpenFace repo](https://github.com/TadasBaltrusaitis/OpenFace/releases). Follow the installation instructions given in [the wiki](https://github.com/TadasBaltrusaitis/OpenFace/wiki/Windows-Installation). To run `download_models.ps1`, open Terminal as Administrator and run `powershell -ExecutionPolicy Bypass -File .\download_models.ps1` in the root directory (`OpenFace-OpenFace_2.1.0`).
2. Install Visual Studio 2015.
3. Overwrite `MainWindow.xaml.cs` in `OpenFace-OpenFace_2.1.0\gui\OpenFaceOffline` with `MainWindow.xaml.cs` given in this setup folder. 
    1. Note that `pubSocket.Connect` from the FACSvatar repo was replaced with `pubSocket.Bind`. This is important or else the ZeroMQ messages will not work!
4. Open `OpenFace-OpenFace_2.1.0/OpenFace.sln` with Visual Studio 2015.
5. In "Solution Explorer", right click on "OpenFaceOffline" > "Manage NuGet Packages".
    1. Browse and search for `netmq`. Install NetMQ by NetMQ with version v4.0.0.1.
    2. Make sure that AsyncIO is version v0.1.26.
    3. Search for `json`; Install Newtonsoft.Json by James Newton-King v12.0.1.
6. In Visual Studio 2015: Select OpenFaceOffline > Release, x64, OpenFaceOffline > Build.
7. In Visual Studio 2015: Select OpenFaceOffline > Release, x64, OpenFaceOffline > Rebuild. (Yes do this again)
8. Copy `config.xml` given in this setup folder and put it at `OpenFace-OpenFace_2.1.0\x64\Release\config.xml`. This is important, otherwise OpenFaceOffline will crash at startup.
9. When you run OpenFaceOffline in `OpenFace-OpenFace_2.1.0\x64\Release\`, it will automatically start ZeroMQ / NetMQ in the background and publish in the format `[topic, timestamp, data_json]`.

Debugging OpenFace with ZeroMQ: Use Wireshark to look at traffic on localhost (`127.0.0.1`). Be sure to use the display filter `tcp.port == 5570`.
