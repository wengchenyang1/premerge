@echo off
setlocal

rem Get the directory of the current script
set "SCRIPT_DIR=%~dp0"
rem Remove trailing backslash if present
if "%SCRIPT_DIR:~-1%"=="\" set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

rem Get the parent directory
for %%i in ("%SCRIPT_DIR%") do set "PARENT_DIR=%%~dpi"
rem Remove trailing backslash if present
if "%PARENT_DIR:~-1%"=="\" set "PARENT_DIR=%PARENT_DIR:~0,-1%"

rem List of files to copy
set FILES_TO_COPY=.pylintrc .clang-format CPPLINT.cfg

for %%f in (%FILES_TO_COPY%) do (
    if exist "%SCRIPT_DIR%\%%f" (
        if not exist "%PARENT_DIR%\%%f" (
            copy "%SCRIPT_DIR%\%%f" "%PARENT_DIR%\" > nul
            echo Copied %%f to %PARENT_DIR%.
        ) else (
            echo %%f already exists in %PARENT_DIR%.
        )
    ) else (
        echo %%f does not exist in %SCRIPT_DIR%.
    )
)

echo Setup complete.
pause
