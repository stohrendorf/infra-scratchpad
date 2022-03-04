$ErrorActionPreference = "Stop"

$VENV = ( & poetry env info -p)

Get-ChildItem -Path . -Recurse -File -Filter *.py |
        Where-Object { !$_.FullName.StartsWith($VENV) } |
        Where-Object { ( ( Get-Content $_.FullName | Where-Object { $_.Contains("__main__") }).Length -gt 0) } |
        ForEach-Object {
            $ModuleName = ( Resolve-Path -Path $_.FullName -Relative).Substring(2).Replace(".py", "").Replace("\", ".")
            echo ">>> $ModuleName"
            ( poetry run python -m $ModuleName )
        }
