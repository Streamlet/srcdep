:: This file can be redistributed to your source code root,
:: to help those who don't set srcdep to PATH variables.

@Echo Off

MkDir "%~dp0.srcdep"
If Not Exist "%~dp0.srcdep\repo" (
    git clone https://github.com/Streamlet/srcdep.git "%~dp0.srcdep\repo"
)

Call "%~dp0.srcdep\repo\srcdep.bat"
