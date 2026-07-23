# Contribuindo

## Checklist de pull request

- [ ] `catalogVersion` foi incrementado.
- [ ] `generatedAt` foi atualizado em UTC.
- [ ] O manifesto usa o mesmo `id` da entrada do catálogo.
- [ ] URLs são oficiais e usam HTTPS.
- [ ] Executáveis e diretórios são relativos e não usam `..`.
- [ ] Não há valores específicos de um usuário, como `/home/nome`.
- [ ] Assets existem.
- [ ] `python scripts/validate_catalog.py` passou.
- [ ] A instalação/execução foi testada no Tauri quando aplicável.

## Política de alterações

Correções de URL, argumentos, ambiente, checksums e estratégias de update podem ser publicadas pelo catálogo sem release nova do launcher, desde que usem campos já suportados pelo schema atual.

Campos novos exigem primeiro uma versão do launcher capaz de interpretá-los com fallback seguro.
