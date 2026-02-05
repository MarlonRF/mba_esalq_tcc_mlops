Essa API foi criada para ser um projeto independente. Pode ser testada localmente na máquina do usuário.

# Comandos
Para rodar a API localmente, utilize os comandos:

Criação da Imagem Docker:
```powershell
docker build -t conforto-api-local .
```

Criação do Container Docker, baseado na imagem:
```powershell
docker run -d --name conforto-api -p 8080:8080 conforto-api-local
```

Para acessar, digite no navegador
```powershell
http://localhost:8080/
```

ou para acessar via Swagger (interface visual)
```powershell
http://localhost:8080/docs
```

Testar via linha de comando:
```powershell
$corpo_requisicao_json = @{
  idade_anos = 30
  peso_kg = 70.0
  altura_cm = 175
  sexo_biologico = "m"
  temperatura_media_c = 25.0
  umidade_relativa_percent = 60.0
  radiacao_solar_media_wm2 = 400.0
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8080/predict -Method POST -ContentType "application/json" -Body $corpo_requisicao_json
```