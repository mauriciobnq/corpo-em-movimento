# Trabalho Prático de SEO - Grupo 2 (Studio Corpo em Movimento, Catanduva - SP)

**Site v1 (otimizado):** https://corpoemmovimento-catanduva.netlify.app  <!-- TROCAR pela URL real -->
**Site v0 (kit inicial, sem SEO):** <!-- URL pública da v0 -->

Integrantes: <!-- preencher -->

## Estrutura
| Pasta | Conteúdo |
|---|---|
| `v0/` | Kit inicial, **intacto**, sem nenhum SEO |
| `v1/` | Site otimizado (publicar esta pasta) |
| `ferramentas/` | Scripts que geram a v1 (`build_v1.py`) e medem v0 e v1 (`audit.py`) |

## Como publicar (recomendado: Netlify ou Cloudflare Pages)
1. Publique `v0/` em um site e `v1/` em outro, apontando o "publish directory" para a pasta.
2. O arquivo `v1/_redirects` faz os redirecionamentos 301 (não funciona no GitHub Pages).
3. Se a URL pública for diferente da do topo deste arquivo, edite a variável `BASE` em
   `ferramentas/build_v1.py` e rode `python3 build_v1.py` dentro da pasta `ferramentas/`
   (ela refaz a v1 com canonical, Open Graph, JSON-LD, robots.txt e sitemap.xml corretos).

## Ver localmente
Os links são relativos à raiz do site, então abra por um servidor local:
`python3 -m http.server 8000 --directory v1` e acesse http://localhost:8000

## Medições
`cd ferramentas && python3 audit.py` compara v0 e v1 (title, description, imagens, cliques da home,
órfãs, NAP, JSON-LD). Validador W3C: `java -jar vnu.jar --skip-non-html v1`.
Lighthouse e Teste de Resultados Enriquecidos devem ser rodados no Chrome/Google, nas duas versões, no mesmo dia.

## Dados fictícios
Marca, endereço, telefones, horário, CEP e depoimentos são fictícios (vindos do kit v0 ou definidos pelo grupo).

## Uso de IA
Declarado no relatório (seção 17).
