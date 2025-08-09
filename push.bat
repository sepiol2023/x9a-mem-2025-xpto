@echo off
setlocal enabledelayedexpansion

REM garante que temos o remoto atualizado
git fetch origin

REM adiciona tudo que mudou
git add -A

REM faz commit só se houver mudanças
git diff --cached --quiet
if %errorlevel% neq 0 (
  git commit -m "auto: %date% %time%"
)

REM rebase em cima do remoto
git pull --rebase origin main
if %errorlevel% neq 0 (
  echo.
  echo *** Rebase falhou. Resolva os conflitos (git status), depois:
  echo     git add <arquivos>
  echo     git rebase --continue
  echo e rode push.bat de novo.
  exit /b 1
)

REM push final
git push origin main
endlocal
echo.
echo OK: push concluido.
