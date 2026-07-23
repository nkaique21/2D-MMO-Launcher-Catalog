# AGENTS.md

## Objetivo

Manter o catálogo oficial remoto do 2D MMO Launcher de forma segura, versionada e compatível com o schema suportado pelo aplicativo.

## Regras

- Responder em pt-BR.
- Não alterar IDs existentes sem plano de migração.
- Não usar caminhos absolutos ou `..`.
- URLs externas devem usar HTTPS.
- Não incluir credenciais, tokens ou dados locais.
- Não introduzir lógica específica no launcher: diferenças entre jogos pertencem aos manifestos.
- Toda alteração funcional deve incrementar `catalogVersion` e atualizar `generatedAt`.
- Todo manifesto habilitado precisa estar listado em `catalog.json`.
- Todo manifesto listado precisa existir e declarar o mesmo `id`.
- Banners e ícones relativos precisam existir no repositório.
- Não mudar `schemaVersion` sem compatibilidade implementada primeiro no launcher.
- Antes do commit, executar `python scripts/validate_catalog.py`.
- Revisar URLs, executáveis, argumentos, ambiente e estratégia de update como superfícies de segurança.
