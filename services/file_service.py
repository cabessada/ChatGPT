from fastapi import APIRouter, HTTPException
from pathlib import Path
import os
from utils.cache import cache_get, cache_set, cache_clear

router = APIRouter()
BASE_DIR = Path(os.environ.get("REPO_PATH", "."))

@router.get("/")
def listar_arquivos_e_pastas():
    resultado = []
    for path in BASE_DIR.rglob("*"):
        resultado.append(str(path.relative_to(BASE_DIR)))
    return resultado

@router.post("/criar_arquivo")
def criar_arquivo(nome: str, conteudo: str = ""):
    caminho = BASE_DIR / nome
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(conteudo)
    cache_clear(nome)
    return {"status": "arquivo criado", "ficheiro": nome}

@router.post("/criar_pasta")
def criar_pasta(nome: str):
    caminho = BASE_DIR / nome
    caminho.mkdir(parents=True, exist_ok=True)
    return {"status": "pasta criada", "pasta": nome}

@router.put("/editar_arquivo")
def editar_arquivo(nome: str, conteudo: str):
    caminho = BASE_DIR / nome
    if not caminho.exists():
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    caminho.write_text(conteudo)
    cache_clear(nome)
    return {"status": "arquivo editado", "ficheiro": nome}

@router.delete("/remover")
def remover(nome: str):
    caminho = BASE_DIR / nome
    if caminho.exists():
        if caminho.is_dir():
            for f in caminho.rglob("*"):
                if f.is_file():
                    f.unlink()
            caminho.rmdir()
            return {"status": "pasta removida"}
        else:
            caminho.unlink()
            return {"status": "arquivo removido"}
    raise HTTPException(status_code=404, detail="Arquivo ou pasta não encontrada")

@router.get("/ler")
def ler_arquivo(nome: str):
    cached = cache_get(nome)
    if cached:
        return {"cached": True, "conteudo": cached}
    caminho = BASE_DIR / nome
    if not caminho.exists():
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    conteudo = caminho.read_text()
    cache_set(nome, conteudo)
    return {"cached": False, "conteudo": conteudo}
