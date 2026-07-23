<div align="center">

# 2D MMO Launcher Catalog

Catálogo oficial de jogos, manifests e assets consumidos pelo 2D MMO Launcher.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Catalog validation](https://github.com/nkaique21/2D-MMO-Launcher-Catalog/actions/workflows/validate.yml/badge.svg)](https://github.com/nkaique21/2D-MMO-Launcher-Catalog/actions/workflows/validate.yml)
[![JSON](https://img.shields.io/badge/format-JSON-000000?logo=json)](catalog.json)

[Launcher](https://github.com/nkaique21/2D-MMO-Launcher) · [Catálogo bruto](https://raw.githubusercontent.com/nkaique21/2D-MMO-Launcher-Catalog/main/catalog.json) · [Reportar problema](https://github.com/nkaique21/2D-MMO-Launcher-Catalog/issues)

</div>

## O que é este repositório?

Este repositório mantém os dados remotos utilizados pelo **2D MMO Launcher** para descobrir jogos e definir como eles devem ser instalados, localizados, executados, atualizados e verificados.

Separar catálogo e aplicativo permite corrigir URLs, assets e manifests sem publicar uma nova versão do launcher a cada alteração.

> Este catálogo não hospeda clientes proprietários de jogos. Downloads devem apontar preferencialmente para fontes oficiais. O projeto não é afiliado aos desenvolvedores ou publicadores dos jogos listados.

## Estrutura

```text
.
├── catalog.json
├── manifests/
│   └── <game-id>.json
├── assets/games/
│   └── <game-id>/
├── schemas/
│   ├── catalog.schema.json
│   └── game-manifest.schema.json
├── scripts/
│   └── validate_catalog.py
└── .github/workflows/
    └── validate.yml
```

- `catalog.json`: índice e versão do catálogo;
- `manifests/`: configuração individual dos jogos;
- `assets/games/`: banners e ícones usados pelo launcher;
- `schemas/`: contratos JSON suportados;
- `scripts/validate_catalog.py`: validação local e usada pelo CI.

## Adicionando um jogo

1. Escolha um `id` estável, minúsculo e sem espaços.
2. Crie `manifests/<id>.json` seguindo o schema atual.
3. Adicione o jogo em `catalog.json`.
4. Adicione banner e ícone em `assets/games/<id>/`.
5. Use URLs HTTPS e, sempre que possível, downloads oficiais e estáveis.
6. Valide localmente.
7. Abra um pull request explicando como instalação, execução e encerramento foram testados.

Exemplo mínimo de entrada no catálogo:

```json
{
  "id": "example-game",
  "manifest": "manifests/example-game.json",
  "enabled": true
}
```

## Validando localmente

O script usa Python 3:

```bash
python scripts/validate_catalog.py
```

A validação confere, entre outros pontos:

- schema do índice e dos manifests;
- IDs ausentes ou duplicados;
- referências entre catálogo e manifests;
- caminhos inseguros;
- URLs incompatíveis;
- assets ausentes;
- manifests não referenciados.

O mesmo processo é executado pelo GitHub Actions em pushes e pull requests.

## Regras para URLs e downloads

- Não publique cookies, tokens, headers de autenticação ou `cf_clearance`.
- Não use URLs temporárias com assinatura e expiração.
- Não aponte para mirrors não oficiais quando existir uma fonte oficial estável.
- Não envie executáveis ou clientes proprietários para este repositório.
- Downloads protegidos por login, captcha ou Cloudflare devem usar um fluxo assistido pelo navegador quando o launcher oferecer suporte.
- Mudanças em executáveis, argumentos ou runners devem receber revisão cuidadosa.

## Assets e direitos autorais

O código, os schemas e os scripts deste repositório são disponibilizados sob a licença MIT. Isso **não transforma automaticamente artes e marcas de terceiros em conteúdo MIT**.

Ao contribuir com um banner ou ícone:

- prefira material oficialmente disponibilizado para divulgação;
- registre a origem na descrição do pull request;
- remova o arquivo caso o detentor dos direitos solicite;
- não implique parceria ou endosso oficial.

Formatos normalmente recomendados:

```text
ícone: PNG ou WebP, preferencialmente quadrado
banner: WebP, PNG ou JPEG
```

## Compatibilidade de schema

O campo `schemaVersion` indica o contrato esperado pelo launcher. Não aumente essa versão apenas por editar conteúdo. Uma nova versão de schema deve ser coordenada com uma versão do launcher capaz de interpretá-la.

O launcher preserva um cache local válido e pode recorrer ao catálogo embutido quando a atualização remota falha.

## Contribuindo

Pull requests devem informar:

- jogo afetado;
- sistema e runner testados;
- origem das URLs e dos assets;
- passos usados na validação;
- comportamento de instalação, execução, atualização e encerramento.

Mudanças que exigem código novo devem ser abertas primeiro no repositório principal do [2D MMO Launcher](https://github.com/nkaique21/2D-MMO-Launcher).

## Licença

Schemas, scripts e conteúdo original do catálogo são distribuídos sob a [licença MIT](LICENSE). Marcas, nomes, imagens e clientes dos jogos permanecem sob os direitos de seus respectivos proprietários.
