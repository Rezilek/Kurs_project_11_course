# Тестирование API в PowerShell

Write-Host "ТСТ API" -ForegroundColor Green
Write-Host "================" -ForegroundColor Green

$baseUrl = "http://localhost:8000"

# 1. олучение токена
Write-Host "`n1. олучение JWT токена..." -ForegroundColor Yellow

$loginData = @{
    email = "test@example.com"
    password = "testpass123"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/users/token/" `
        -Method POST `
        -Headers @{"Content-Type" = "application/json; charset=utf-8"} `
        -Body $loginData `
        -ErrorAction Stop
    
    $accessToken = $response.access
    Write-Host "   ✓ Токен получен" -ForegroundColor Green
    Write-Host "   Token: $($accessToken.Substring(0, 30))..." -ForegroundColor Cyan
    
} catch {
    Write-Host "   ✗ шибка получения токена:" -ForegroundColor Red
    Write-Host "   $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}


# 2. олучение профиля
Write-Host "`n2. олучение профиля пользователя..." -ForegroundColor Yellow

$headers = @{
    "Authorization" = "Bearer $accessToken"
    "Content-Type" = "application/json; charset=utf-8"
    "Accept" = "application/json; charset=utf-8"
}

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/users/me/" `
        -Method GET `
        -Headers $headers `
        -ErrorAction Stop
    
    Write-Host "   ✓ рофиль получен" -ForegroundColor Green
    
    # ыведем результат
    Write-Host "`n   анные профиля:" -ForegroundColor Cyan
    $response | ConvertTo-Json -Depth 10 | Write-Host
    
    # роверка русских символов
    if ($response.city) {
        Write-Host "`n   ород: '$($response.city)'" -ForegroundColor Magenta
        Write-Host "   мя: '$($response.first_name)'" -ForegroundColor Magenta
    }
    
} catch {
    Write-Host "   ✗ шибка получения профиля:" -ForegroundColor Red
    Write-Host "   $($_.Exception.Message)" -ForegroundColor Red
}

# 3. бновление профиля
Write-Host "`n3. бновление профиля с русскими символами..." -ForegroundColor Yellow

$updateData = @{
    first_name = "лександр"
    last_name = "ванов"
    city = "осква"
    phone = "+7 (999) 123-45-67"
} | ConvertTo-Json

Write-Host "   тправляемые данные:" -ForegroundColor Gray
Write-Host "   $updateData" -ForegroundColor Gray

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/users/me/" `
        -Method PATCH `
        -Headers $headers `
        -Body $updateData `
        -ErrorAction Stop
    
    Write-Host "   ✓ рофиль обновлен" -ForegroundColor Green
    
    Write-Host "`n   бновленные данные:" -ForegroundColor Cyan
    $response | ConvertTo-Json -Depth 10 | Write-Host
    
    # роверка
    if ($response.city -eq "осква") {
        Write-Host "`n   ✓ усские символы работают корректно!" -ForegroundColor Green
    } else {
        Write-Host "`n   ✗ роблема: город '$($response.city)' вместо 'осква'" -ForegroundColor Red
    }
    
} catch {
    Write-Host "   ✗ шибка обновления:" -ForegroundColor Red
    Write-Host "   $($_.Exception.Message)" -ForegroundColor Red
}
