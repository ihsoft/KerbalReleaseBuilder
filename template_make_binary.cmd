REM This is a template for a script to build mod's binary(-ies).
REM Adjust path to the compiler and name of the mod.
REM Ensure mod's project has release configuration setup.
REM Verify the output path of the Release configuration, it must mact hthe release project setup.

@echo off
REM Until new major version of C# is released the build number in the path will keep counting.
C:\Windows\Microsoft.NET\Framework\v4.0.30319\MSBuild ..\Source\DefaultModName.csproj /t:Rebuild /p:Configuration=Release
