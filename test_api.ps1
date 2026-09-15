Write-Host "Testing GET /tasks"
curl.exe -i http://localhost:8000/tasks

Write-Host "`nTesting POST /tasks"
curl.exe -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{"title":"API Test"}'

Write-Host "`nTesting GET /health"
curl.exe -i http://localhost:8000/health