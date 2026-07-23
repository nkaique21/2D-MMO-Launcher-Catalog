# 2D MMO Launcher Catalog

Catálogo oficial de jogos para o [2D MMO Launcher](https://github.com/nkaique21/2D-MMO-Launcher).

O launcher consulta por padrão:

```text
https://raw.githubusercontent.com/nkaique21/2D-MMO-Launcher-Catalog/main/catalog.json
```

Assim que este repositório público for criado com esse nome e receber o primeiro push na branch `main`, o launcher poderá atualizar manifestos sem precisar publicar uma nova versão do aplicativo.

## Estrutura

```text
catalog.json
manifests/
assets/games/<game_id>/
schemas/
scripts/validate_catalog.py
.github/workflows/validate.yml
```

- `catalog.json`: índice e versão do catálogo.
- `manifests/*.json`: instalação, execução, update e verificação de cada jogo.
- `assets/`: banners e ícones servidos pelo próprio repositório.
- `schemas/`: contrato JSON do catálogo e dos manifestos.
- `scripts/validate_catalog.py`: valida schema, IDs, paths, URLs e assets.

## Criar o repositório no GitHub

Crie um repositório público chamado exatamente:

```text
2D-MMO-Launcher-Catalog
```

Depois, dentro desta pasta:

```fish
git init
git add .
git commit -m "feat: cria catálogo oficial inicial"
git branch -M main
git remote add origin git@github.com:nkaique21/2D-MMO-Launcher-Catalog.git
git push -u origin main
```

Se preferir HTTPS:

```fish
git remote add origin https://github.com/nkaique21/2D-MMO-Launcher-Catalog.git
```

## Validar localmente

```fish
python -m venv .venv
source .venv/bin/activate.fish
python -m pip install jsonschema==4.23.0
python scripts/validate_catalog.py
```

O GitHub Actions executa a mesma validação em push e pull request.

## Adicionar um jogo

1. Crie `manifests/<game_id>.json`.
2. Adicione banner e ícone em `assets/games/<game_id>/`.
3. Inclua a entrada em `catalog.json`.
4. Incremente `catalogVersion`.
5. Atualize `generatedAt` em UTC.
6. Rode o validador.
7. Faça commit e push.

O `game_id` deve usar apenas letras minúsculas, números, hífen e underscore.

## Assets iniciais

Os SVGs incluídos são placeholders funcionais. Podem ser substituídos por PNG, WebP ou SVG definitivos, desde que os caminhos dos manifestos e os arquivos continuem válidos.

## Compatibilidade e segurança

- `schemaVersion` atual: `1`.
- URLs de download e update devem usar HTTPS.
- Paths absolutos e travessia com `..` são rejeitados.
- IDs duplicados são rejeitados.
- O launcher baixa o catálogo para staging e só ativa o conjunto completo depois de validar todos os manifestos.
- Em falha de rede ou validação, o launcher mantém o último cache válido.
- Sem cache remoto válido, o launcher usa os manifestos embutidos na aplicação.

O catálogo oficial é uma fonte confiável de comandos de instalação e execução. Pull requests precisam ser revisados com atenção especial a URLs, executáveis, argumentos e variáveis de ambiente.
# 2D-MMO-Launcher-Catalog
