Start-Process -FilePath "powershell.exe" -ArgumentList '-NoLogo', '-NoExit', '-Command', 'Clear-Host; python "./orchestrator/orchestrator.py"'
Start-Process -FilePath "./modules/imperative/build/AlgoritmosInteligenciaArtificial-imperative.exe"
Start-Process -FilePath "./modules/structured/build/AlgoritmosInteligenciaArtificial-structured.exe"
Start-Process -FilePath "powershell.exe" -ArgumentList '-NoLogo', '-NoExit', '-Command', 'Clear-Host; npx ts-node "./modules/poo/index.ts"'
Start-Process -FilePath "powershell.exe" -ArgumentList '-NoLogo', '-NoExit', '-Command', 'Clear-Host'
