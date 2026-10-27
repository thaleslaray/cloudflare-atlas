# cloudflare-atlas

Skill do Claude Code com conhecimento atualizado da Cloudflare. Ela ajuda o agente a escolher os produtos certos, a montar um sistema inteiro dentro da Cloudflare e a **não inventar** preço, limite ou configuração.

## Para que serve

- Escolher o produto certo para cada necessidade (Workers, D1, R2, KV, Queues, Durable Objects e outros 90 e poucos).
- Consultar um arquivo por produto (`references/products/`) e os endpoints exatos da API (`references/api/`).
- Revisar código de Workers e arquivos `wrangler` (`references/code-review/`).
- Regra principal: **a documentação ao vivo da Cloudflare vence** o que está salvo aqui. Os arquivos são uma foto, e a skill manda conferir a página atual antes de citar qualquer número.

## Como instalar

No macOS ou no Linux:

```bash
git clone https://github.com/thaleslaray/cloudflare-atlas ~/.claude/skills/cloudflare-atlas
```

No Windows (PowerShell):

```powershell
git clone https://github.com/thaleslaray/cloudflare-atlas "$env:USERPROFILE\.claude\skills\cloudflare-atlas"
```

Se preferir, peça ao próprio Claude Code: *"clone https://github.com/thaleslaray/cloudflare-atlas dentro da pasta ~/.claude/skills"*.

Depois, feche e abra o Claude Code e rode `/skills`. O `cloudflare-atlas` deve aparecer na lista.

## Como usar

O agente chama a atlas sozinho quando a conversa envolve Cloudflare. Você também pode chamar de propósito digitando `/cloudflare-atlas` ou pedindo "use a cloudflare-atlas para...".

## Como atualizar

```bash
git -C ~/.claude/skills/cloudflare-atlas pull
```

## Créditos e licenças

O conteúdo foi construído a partir de materiais abertos da Cloudflare (Apache 2.0, CC BY 4.0 e MIT). Os créditos e as mudanças feitas estão em [ATTRIBUTION.md](ATTRIBUTION.md). Esta skill é independente e **não é afiliada nem endossada pela Cloudflare**.

## Para quem mantém a skill

- `scripts/check-repo`: confere a higiene do repositório. Rode antes de publicar.
- `scripts/check-pointers`: confere os ponteiros entre os arquivos de produto.
- `scripts/update-check`: compara a lista de produtos da skill com a da Cloudflare ao vivo.
- `CHANGELOG.md`: registro de cada passada de curadoria.
