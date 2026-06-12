Start-Process -FilePath "python.exe" -ArgumentList "./orchestrator/orchestrator.py"
Start-Process -FilePath "./modules/imperative/build/AlgoritmosInteligenciaArtificial-imperative.exe"
Start-Process -FilePath "./modules/structured/build/AlgoritmosInteligenciaArtificial-structured.exe"