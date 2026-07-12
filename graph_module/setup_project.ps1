# ============================================
# LegalKnowledgeGraph Project Setup
# ============================================

$ProjectName = "LegalKnowledgeGraph"

Write-Host ""
Write-Host "Creating project: $ProjectName"
Write-Host ""

# Root
New-Item -ItemType Directory -Force -Path $ProjectName | Out-Null
Set-Location $ProjectName

# -----------------------------
# app
# -----------------------------
$app = @(
    "app",
    "app\__pycache__"
)

foreach ($folder in $app) {
    New-Item -ItemType Directory -Force -Path $folder | Out-Null
}

$appFiles = @(
    "app\__init__.py",
    "app\engine.py",
    "app\config.py",
    "app\logger.py",
    "app\parser.py",
    "app\extractor.py",
    "app\dependency.py",
    "app\graph_builder.py",
    "app\visualizer.py",
    "app\exporter.py",
    "app\llm.py",
    "app\ontology.py",
    "app\models.py",
    "app\utils.py",
    "app\exceptions.py"
)

foreach ($file in $appFiles) {
    New-Item -ItemType File -Force -Path $file | Out-Null
}

# -----------------------------
# prompts
# -----------------------------

New-Item -ItemType Directory -Force -Path "prompts" | Out-Null

$promptFiles = @(
    "prompts\entity_prompt.md",
    "prompts\relation_prompt.md",
    "prompts\dependency_prompt.md"
)

foreach ($file in $promptFiles) {
    New-Item -ItemType File -Force -Path $file | Out-Null
}

# -----------------------------
# input
# -----------------------------

New-Item -ItemType Directory -Force -Path "input" | Out-Null

New-Item -ItemType File -Force -Path "input\sample_document.json" | Out-Null

# -----------------------------
# output
# -----------------------------

$outputFolders = @(
    "output",
    "output\graphs",
    "output\json",
    "output\html"
)

foreach ($folder in $outputFolders) {
    New-Item -ItemType Directory -Force -Path $folder | Out-Null
}

# -----------------------------
# logs
# -----------------------------

New-Item -ItemType Directory -Force -Path "logs" | Out-Null

New-Item -ItemType File -Force -Path "logs\application.log" | Out-Null

# -----------------------------
# tests
# -----------------------------

New-Item -ItemType Directory -Force -Path "tests" | Out-Null

$testFiles = @(
    "tests\test_parser.py",
    "tests\test_extractor.py",
    "tests\test_dependency.py",
    "tests\test_graph.py",
    "tests\test_engine.py"
)

foreach ($file in $testFiles) {
    New-Item -ItemType File -Force -Path $file | Out-Null
}

# -----------------------------
# Root files
# -----------------------------

$rootFiles = @(
    ".env",
    ".env.example",
    ".gitignore",
    "Dockerfile",
    "docker-compose.yml",
    "requirements.txt",
    "README.md",
    "LICENSE",
    "main.py"
)

foreach ($file in $rootFiles) {
    New-Item -ItemType File -Force -Path $file | Out-Null
}

Write-Host ""
Write-Host "========================================"
Write-Host "Project created successfully!"
Write-Host "========================================"
Write-Host ""

tree /F