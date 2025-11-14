@echo off
setlocal

rem Get the directory of the current script
set "SCRIPT_DIR=%~dp0"
rem Remove trailing backslash if present
if "%SCRIPT_DIR:~-1%"=="\" set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

rem Get the current working directory (project root)
set "PROJECT_ROOT=%CD%"

rem List of files to copy
set FILES_TO_COPY=.pylintrc .clang-format CPPLINT.cfg

for %%f in (%FILES_TO_COPY%) do (
    if exist "%SCRIPT_DIR%\%%f" (
        if not exist "%PROJECT_ROOT%\%%f" (
            copy "%SCRIPT_DIR%\%%f" "%PROJECT_ROOT%\" > nul
            echo Copied %%f to %PROJECT_ROOT%.
        ) else (
            echo %%f already exists in %PROJECT_ROOT%.
        )
    ) else (
        echo %%f does not exist in %SCRIPT_DIR%.
    )
)

echo Setup complete.
pause
