# Studio Corpo em Movimento · Otimização de SEO

Auditoria e otimização de SEO de um site de fisioterapia, pilates e massagem em Catanduva - SP. O projeto parte de um site inicial sem nenhum cuidado de SEO (**v0**) e entrega uma versão otimizada (**v1**), comparando as duas com os mesmos testes.

- **v1 (otimizado):** https://corpoemmovimento-catanduva.netlify.app/
- **v0 (inicial, sem SEO):** https://corpo-em-movimento-v0.netlify.app/

## Estrutura

```
corpo-em-movimento/
├── README.md
├── v0/                  # site inicial, sem SEO
│   ├── index.html, sobre.html, contato.html, faq.html, ...
│   ├── Servicos/
│   ├── css/
│   └── imagens/
├── v1/                  # site otimizado
│   ├── index.html
│   ├── servicos/
│   ├── fisioterapia-esportiva-catanduva/
│   ├── pilates-catanduva/
│   ├── massagem-relaxante-catanduva/
│   ├── sobre/  depoimentos/  perguntas-frequentes/
│   ├── contato/  agendar/  obrigado/
│   ├── 404.html  robots.txt  sitemap.xml  _redirects  favicon.svg
│   ├── css/
│   └── imagens/
└── ferramentas/         # scripts que geram a v1 e medem v0 e v1
    ├── build_v1.py
    └── audit.py
```

## O que foi feito

| Tema | Implementação |
|---|---|
| **Indexação e robots.txt** | `robots.txt` sem bloqueio de CSS, JS ou imagens, bloqueando apenas parâmetros de campanha (`utm_`, `fbclid`, `gclid`) e indicando o sitemap. Páginas `/obrigado/` e `404` com `meta robots noindex`. |
| **Sitemap** | `sitemap.xml` com as 10 URLs canônicas e indexáveis, com `lastmod`, enviado ao Google Search Console. |
| **HTML semântico** | `header`, `nav`, `main`, `article`, `section` e `footer`; um único `h1` por página; hierarquia de títulos sem pular nível; `lang="pt-BR"`; links com texto descritivo. |
| **Meta tags** | `title` e `description` únicos em todas as páginas, `canonical` absoluto, `viewport`, `charset` e Open Graph. |
| **Imagens** | WebP em 3 larguras (480, 800 e 1200 px) com `srcset`, nomes descritivos, `alt` em todas, `width` e `height` definidos e `loading="lazy"` fora da primeira dobra. |
| **Arquitetura** | 12 páginas, todas a 1 clique da home, menu coerente com a hierarquia, breadcrumbs, links internos entre serviços e nenhuma página órfã. |
| **URLs e 301** | URLs curtas, em minúsculas, com hífens, sem acentos e com a cidade nos serviços. 10 redirecionamentos 301 das URLs antigas (`_redirects`). |
| **Dados estruturados** | JSON-LD de `Physiotherapy` (negócio local), `Service`, `FAQPage` e `BreadcrumbList`. |
| **SEO local** | Nome, endereço e telefone idênticos em todas as páginas, mapa incorporado, horário de funcionamento, texto de localização e simulação do perfil no Google Meu Negócio. |
| **Palavras-chave e off-page** | 25 termos classificados por intenção de busca e ligados a uma única página cada, e plano de 5 ações de link building com `sponsored`, `ugc` e `nofollow`. |
| **Mídia paga (simulada)** | 10 palavras-chave com tipo de correspondência e 2 anúncios de texto. |

## Resultados: v0 x v1

| Métrica | v0 | v1 |
|---|---|---|
| Lighthouse: SEO (mobile) | 73 | 100 |
| Lighthouse: SEO (desktop) | 73 | 100 |
| Lighthouse: desempenho (mobile) | 83 | 100 |
| Erros / avisos no validador W3C | 15 / 20 | 0 / 0 |
| Erros nos dados estruturados | nenhum item detectado | 0 |
| Páginas com `title` único | 5 de 10 | 12 de 12 |
| Páginas com `description` única | 0 de 10 | 12 de 12 |
| Imagens sem `alt` | 5 | 0 |
| Imagens carregadas na home (desktop) | 724 KB | 21 KB |
| Páginas órfãs | 5 | 0 |
| Páginas a mais de 3 cliques da home | 5 | 0 |
| Formatos diferentes de endereço | 3 | 1 |
| `robots.txt` e `sitemap.xml` | não existem | existem |

## Como executar localmente

```bash
python3 -m http.server 8000 --directory v1
```

Acesse http://localhost:8000

## Como publicar

Publicação no Netlify (ou Cloudflare Pages):

1. Crie um site com **Publish directory** `v1`.
2. Para a versão inicial, crie um segundo site com **Publish directory** `v0`.
3. O arquivo `v1/_redirects` deve ficar na raiz da pasta publicada.

## Como gerar a v1

```bash
pip install pillow
cd ferramentas
python3 build_v1.py
```

Defina a variável `BASE` no início de `build_v1.py` com a URL pública do site antes de executar.

## Como medir v0 e v1

```bash
pip install beautifulsoup4 lxml
cd ferramentas
python3 audit.py
```

O `audit.py` compara as duas pastas: títulos e descrições únicos, imagens (alt, dimensões, srcset e peso), cliques a partir da home, páginas órfãs, links genéricos, endereço e telefone, JSON-LD, `robots.txt` e sitemap.

| Verificação | Ferramenta |
|---|---|
| Validação de HTML | [Nu Html Checker](https://validator.w3.org/nu/): `java -jar vnu.jar --skip-non-html v1` |
| SEO e desempenho | Lighthouse |
| Dados estruturados | [Teste de Resultados Enriquecidos](https://search.google.com/test/rich-results) e [Validator Schema.org](https://validator.schema.org/) |
| Rastreamento e sitemap | Google Search Console |
