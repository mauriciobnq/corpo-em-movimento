# -*- coding: utf-8 -*-
import os, json, shutil, html
from urllib.parse import urlparse
from PIL import Image

# ====== CONFIGURAÇÃO (troque BASE pela URL pública real do deploy) ======
BASE = "https://corpoemmovimento-catanduva.netlify.app"
LASTMOD = "2026-11-20"
SRC = "../v0"
OUT = "../v1"
ROOT = urlparse(BASE).path.rstrip("/")          # "" em Netlify; "/repo" em GitHub Pages de projeto
NOME = "Studio Corpo em Movimento"
FONE = "(17) 3522-1100"; FONE_TEL = "+551735221100"
ZAP = "(17) 99877-2200"; ZAP_TEL = "+5517998772200"
RUA = "Rua Pernambuco, 450"; BAIRRO = "Centro"; CIDADE = "Catanduva"; UF = "SP"; CEP = "15800-000"
HORARIO = [("Segunda a sexta", "07:00 às 20:00"), ("Sábado", "08:00 às 12:00"), ("Domingo e feriados", "Fechado")]
LAT, LON = -21.1378, -48.9728

if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(OUT + "/imagens"); os.makedirs(OUT + "/css")
shutil.copy(SRC + "/css/estilo.css", OUT + "/css/estilo.css")

# ---------- imagens: WebP em 3 larguras, nomes descritivos ----------
IMG = {
 "fachada":  ("fachada.jpg",  "fachada-studio-corpo-em-movimento-catanduva", "Fachada do Studio Corpo em Movimento, com porta azul e janelas com floreiras, em Catanduva"),
 "espaco":   ("DSC_7788.jpg", "sala-pilates-faixas-elasticas-bola-catanduva", "Sala de atendimento com faixas elásticas coloridas e bola de pilates no chão de madeira"),
 "fisio":    ("IMG_2201.jpg", "acessorios-fisioterapia-esportiva-catanduva", "Colchonete, rolos, anéis e faixas usados nos exercícios de fisioterapia esportiva"),
 "pilates":  ("IMG_2202.jpg", "aparelho-pilates-reformer-catanduva", "Aparelho de pilates com bola ao lado, em sala iluminada do studio"),
 "massagem": ("IMG_2203.jpg", "massagem-relaxante-pedras-vela-catanduva", "Pedras empilhadas, vela acesa e toalhas dobradas na sala de massagem relaxante"),
 "bola":     ("IMG_2204.jpg", "bola-pilates-rosa-faixas-studio-catanduva", "Bola de pilates rosa e faixas elásticas ao lado de uma planta no studio"),
}
WIDTHS = [480, 800, 1200]
def img_tag(key, sizes, eager=False, cls=""):
    f, base, alt = IMG[key]
    srcset = ", ".join(f"{ROOT}/imagens/{base}-{w}.webp {w}w" for w in WIDTHS)
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="{ROOT}/imagens/{base}-800.webp" srcset="{srcset}" sizes="{sizes}" '
            f'width="1200" height="800" alt="{html.escape(alt)}" {load}>')
for key,(f,base,alt) in IMG.items():
    im = Image.open(f"{SRC}/imagens/{f}").convert("RGB")
    for w in WIDTHS:
        im.resize((w, round(w*2/3)), Image.LANCZOS).save(f"{OUT}/imagens/{base}-{w}.webp", "WEBP", quality=78, method=6)
# imagem Open Graph 1200x630 (JPEG por compatibilidade com redes sociais)
im = Image.open(f"{SRC}/imagens/fachada.jpg").convert("RGB").crop((0,285,1800,1230)).resize((1200,630), Image.LANCZOS)
im.save(OUT + "/imagens/og-studio-corpo-em-movimento.jpg", "JPEG", quality=78, optimize=True)
open(OUT + "/favicon.svg","w").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="16" fill="#1b5e8c"/><text x="32" y="45" font-size="38" text-anchor="middle" fill="#fff" font-family="Georgia,serif" font-weight="bold">S</text></svg>')

# ---------- páginas ----------
def u(slug): return f"{ROOT}/{slug}/" if slug else f"{ROOT}/"
def abs_(slug): return f"{BASE}/{slug}/" if slug else f"{BASE}/"
PAGES = {}   # slug -> dict
ORDER = []
def add(slug, **kw): PAGES[slug] = kw; ORDER.append(slug)

NAV = [("", "Início"), ("servicos", "Serviços"), ("sobre", "Sobre"), ("depoimentos", "Depoimentos"), ("perguntas-frequentes", "Perguntas"), ("contato", "Contato")]
SERV = [("fisioterapia-esportiva-catanduva","Fisioterapia esportiva"),("pilates-catanduva","Pilates"),("massagem-relaxante-catanduva","Massagem relaxante")]
BC_NAMES = {"servicos":"Serviços","sobre":"Sobre","depoimentos":"Depoimentos","perguntas-frequentes":"Perguntas frequentes","contato":"Contato","agendar":"Agendar sessão", **{s:n for s,n in SERV}}

def ld_negocio():
    return {"@context":"https://schema.org","@type":"Physiotherapy","@id":BASE+"/#negocio","name":NOME,
      "description":"Fisioterapia esportiva, pilates e massagem relaxante em Catanduva (SP), com avaliação individual e hora marcada.",
      "url":BASE+"/","telephone":"+55-17-3522-1100","image":BASE+"/imagens/og-studio-corpo-em-movimento.jpg","priceRange":"$$",
      "address":{"@type":"PostalAddress","streetAddress":RUA,"addressLocality":CIDADE,"addressRegion":UF,"postalCode":CEP,"addressCountry":"BR"},
      "geo":{"@type":"GeoCoordinates","latitude":LAT,"longitude":LON},
      "hasMap":f"https://www.openstreetmap.org/?mlat={LAT}&mlon={LON}#map=17/{LAT}/{LON}",
      "openingHoursSpecification":[
        {"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"07:00","closes":"20:00"},
        {"@type":"OpeningHoursSpecification","dayOfWeek":"Saturday","opens":"08:00","closes":"12:00"}],
      "areaServed":[{"@type":"City","name":c} for c in ["Catanduva","Pindorama","Elisiário","Palmares Paulista","Catiguá"]],
      "knowsAbout":["Fisioterapia esportiva","Pilates","Massagem relaxante"]}
def ld_bc(slug):
    items=[("Início","")]
    if slug in dict(SERV): items.append(("Serviços","servicos"))
    items.append((BC_NAMES[slug],slug))
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":abs_(s)} for i,(n,s) in enumerate(items)]}
def ld_service(slug, nome, tipo, desc):
    return {"@context":"https://schema.org","@type":"Service","name":f"{nome} em Catanduva","serviceType":tipo,"description":desc,
            "url":abs_(slug),"provider":{"@id":BASE+"/#negocio"},"areaServed":{"@type":"City","name":"Catanduva"}}

def layout(slug, p):
    robots = p.get("robots")
    canon = abs_(slug) if slug != "404" else None
    head = ['<meta charset="utf-8">','<meta name="viewport" content="width=device-width, initial-scale=1">',
            f'<title>{html.escape(p["title"])}</title>', f'<meta name="description" content="{html.escape(p["desc"])}">']
    if robots: head.append(f'<meta name="robots" content="{robots}">')
    if canon: head.append(f'<link rel="canonical" href="{canon}">')
    head += [f'<link rel="icon" href="{ROOT}/favicon.svg" type="image/svg+xml">', f'<link rel="stylesheet" href="{ROOT}/css/estilo.css">']
    if canon:
        head += ['<meta property="og:type" content="website">','<meta property="og:locale" content="pt_BR">',f'<meta property="og:site_name" content="{NOME}">',
                 f'<meta property="og:title" content="{html.escape(p["title"])}">',f'<meta property="og:description" content="{html.escape(p["desc"])}">',
                 f'<meta property="og:url" content="{canon}">',f'<meta property="og:image" content="{BASE}/imagens/og-studio-corpo-em-movimento.jpg">',
                 '<meta property="og:image:width" content="1200">','<meta property="og:image:height" content="630">',
                 '<meta property="og:image:alt" content="Fachada do Studio Corpo em Movimento em Catanduva">','<meta name="twitter:card" content="summary_large_image">']
    for ld in p.get("ld", []):
        head.append('<script type="application/ld+json">'+json.dumps(ld, ensure_ascii=False)+'</script>')
    nav = "".join(f'<a href="{u(s)}"' + (' aria-current="page"' if s==slug or (s=="servicos" and slug in dict(SERV)) else '') + f'>{n}</a>' for s,n in NAV)
    bc = ""
    if slug not in ("", "404", "obrigado"):
        parts = [f'<a href="{u("")}">Início</a>']
        if slug in dict(SERV): parts.append(f'<a href="{u("servicos")}">Serviços</a>')
        parts.append(f'<span aria-current="page">{BC_NAMES[slug]}</span>')
        bc = '<nav class="breadcrumb" aria-label="Você está aqui">' + " &rsaquo; ".join(parts) + '</nav>'
    foot_serv = "".join(f'<li><a href="{u(s)}">{n}</a></li>' for s,n in SERV)
    footer = f'''<footer class="rodape"><div class="rodape-in">
<div><strong>{NOME}</strong><address>{RUA} - {BAIRRO}<br>{CIDADE} - {UF}, {CEP}<br>Telefone: <a href="tel:{FONE_TEL}">{FONE}</a><br>WhatsApp: <a href="https://wa.me/{ZAP_TEL.strip("+")}">{ZAP}</a></address></div>
<div><strong>Serviços</strong><ul>{foot_serv}</ul></div>
<div><strong>Mais</strong><ul><li><a href="{u("agendar")}">Agendar sessão</a></li><li><a href="{u("perguntas-frequentes")}">Perguntas frequentes</a></li><li><a href="{u("contato")}">Como chegar</a></li></ul></div>
</div><p class="rodape-fim">{NOME} - Fisioterapia, pilates e massagem em Catanduva - SP</p></footer>'''
    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
{chr(10).join(head)}
</head>
<body>
<a class="pular" href="#principal">Ir para o conteúdo</a>
<header class="topo"><div class="topo-in">
<a class="logo" href="{u("")}"><span class="logo-sel" aria-hidden="true">S</span>{NOME}</a>
<nav class="menu" aria-label="Menu principal">{nav}</nav>
</div></header>
<main class="conteudo" id="principal">
{bc}
{p["body"]}
</main>
{footer}
</body>
</html>
'''
def cta(): return f'<p><a class="botao" href="{u("agendar")}">Agendar uma sessão</a></p>'
def relacionados(slug):
    li = "".join(f'<div class="caixa chamada"><p><a href="{u(s)}">{n} em Catanduva</a></p></div>' for s,n in SERV if s!=slug)
    return f'<section><h2>Conheça também</h2><div class="grade dois">{li}</div></section>'
def local_bloco(extra=""):
    return (f'<section><h2>Onde atendemos</h2><p>O {NOME} fica na {RUA}, no {BAIRRO} de {CIDADE}, interior de São Paulo. '
            f'Atendemos com hora marcada: ligue para <a href="tel:{FONE_TEL}">{FONE}</a> ou veja o <a href="{u("contato")}">mapa e os horários de funcionamento</a>. {extra}</p></section>')

# ---- Home
add("", title="Fisioterapia e Pilates em Catanduva | Corpo em Movimento",
    desc="Fisioterapia esportiva, pilates e massagem relaxante em Catanduva (SP). Avaliação individual, turmas pequenas e atendimento com hora marcada.",
    ld=[ld_negocio()],
    body=f'''<section class="hero">
<div>
<h1>Fisioterapia e pilates em Catanduva</h1>
<p>No {NOME} você encontra fisioterapia esportiva, pilates e massagem relaxante, com atendimento com hora marcada no centro de Catanduva.</p>
<div class="selos"><span class="selo">Avaliação individual</span><span class="selo">Turmas pequenas</span><span class="selo">Hora marcada</span></div>
<p class="topo-cta"><a class="botao" href="{u("agendar")}">Agendar uma sessão</a></p>
</div>
{img_tag("fachada","(max-width: 780px) 100vw, 520px",eager=True)}
</section>
<section><h2>Nossos serviços</h2>
<div class="grade">
<div class="caixa card">{img_tag("fisio","(max-width: 780px) 100vw, 330px")}<h3>Fisioterapia esportiva</h3><p>Volta segura ao esporte depois de uma lesão, com avaliação e exercícios individuais.</p><a href="{u("fisioterapia-esportiva-catanduva")}">Ver fisioterapia esportiva em Catanduva</a></div>
<div class="caixa card">{img_tag("pilates","(max-width: 780px) 100vw, 330px")}<h3>Pilates</h3><p>Aulas em solo e em aparelhos, em turmas pequenas, para postura, força e flexibilidade.</p><a href="{u("pilates-catanduva")}">Ver aulas de pilates em Catanduva</a></div>
<div class="caixa card">{img_tag("massagem","(max-width: 780px) 100vw, 330px")}<h3>Massagem relaxante</h3><p>Sessões de 50 minutos para aliviar as tensões do dia a dia, com profissional formado.</p><a href="{u("massagem-relaxante-catanduva")}">Ver massagem relaxante em Catanduva</a></div>
</div></section>
<section><h2>Por que escolher o studio</h2>
<div class="grade dois">
<div class="caixa chamada"><p>Equipe de fisioterapeutas e instrutores de pilates com mais de dez anos de experiência. <a href="{u("sobre")}">Conheça o studio</a>.</p></div>
<div class="caixa chamada"><p>Veja o que os clientes contam sobre o atendimento nos <a href="{u("depoimentos")}">depoimentos</a>, ou tire dúvidas nas <a href="{u("perguntas-frequentes")}">perguntas frequentes</a>.</p></div>
</div></section>
<section><h2>Estamos no centro de Catanduva</h2>
<p>Ficamos na {RUA}, {BAIRRO}. Atendemos moradores de Catanduva e de cidades próximas, como Pindorama, Elisiário e Palmares Paulista. Veja o <a href="{u("contato")}">endereço, o mapa e o horário de funcionamento</a> ou ligue para <a href="tel:{FONE_TEL}">{FONE}</a>.</p></section>''')

# ---- Hub de serviços
add("servicos", title="Serviços de Fisioterapia e Pilates em Catanduva | Studio",
    desc="Conheça os serviços do Studio Corpo em Movimento em Catanduva: fisioterapia esportiva, aulas de pilates e massagem relaxante, com hora marcada.",
    ld=[ld_bc("servicos")],
    body=f'''<h1>Serviços de fisioterapia e pilates em Catanduva</h1>
<p>Todos os atendimentos do {NOME} são feitos com hora marcada, na {RUA}, em {CIDADE}. Escolha o serviço para ver como funciona.</p>
<div class="grade">
<div class="caixa card">{img_tag("fisio","(max-width: 780px) 100vw, 330px")}<h2>Fisioterapia esportiva</h2><p>Para quem pratica esporte e quer voltar com segurança depois de uma lesão.</p><a href="{u("fisioterapia-esportiva-catanduva")}">Fisioterapia esportiva em Catanduva</a></div>
<div class="caixa card">{img_tag("pilates","(max-width: 780px) 100vw, 330px")}<h2>Pilates</h2><p>Aulas em solo e em aparelhos, em turmas pequenas.</p><a href="{u("pilates-catanduva")}">Aulas de pilates em Catanduva</a></div>
<div class="caixa card">{img_tag("massagem","(max-width: 780px) 100vw, 330px")}<h2>Massagem relaxante</h2><p>Sessões de 50 minutos para aliviar tensões.</p><a href="{u("massagem-relaxante-catanduva")}">Massagem relaxante em Catanduva</a></div>
</div>
{cta()}''')

# ---- Serviços
def servico(slug, nome, tipo, title, desc, key, intro, quem, como, itens):
    lis = "".join(f"<li>{i}</li>" for i in itens)
    passos = "".join(f"<li>{i}</li>" for i in como)
    body = f'''<article>
<div class="prod">
{img_tag(key,"(max-width: 780px) 100vw, 520px",eager=True)}
<div><h1>{nome} em Catanduva</h1>
<p>{intro}</p>
<p>Telefone: <a href="tel:{FONE_TEL}">{FONE}</a></p>
{cta()}</div>
</div>
<section><h2>Para quem é</h2><p>{quem}</p></section>
<section><h2>Como funciona</h2><ol>{passos}</ol></section>
<section><h2>O que você encontra</h2><ul>{lis}</ul></section>
{local_bloco()}
<section><h2>Dúvidas?</h2><p>Veja as <a href="{u("perguntas-frequentes")}">perguntas frequentes sobre os atendimentos</a>, como a necessidade de pedido médico.</p></section>
{relacionados(slug)}
</article>'''
    add(slug, title=title, desc=desc, ld=[ld_service(slug,nome,tipo,desc), ld_bc(slug)], body=body)
servico("fisioterapia-esportiva-catanduva","Fisioterapia esportiva","Fisioterapia esportiva",
  "Fisioterapia Esportiva em Catanduva | Corpo em Movimento",
  "Fisioterapia esportiva em Catanduva para voltar ao esporte com segurança após uma lesão. Avaliação individual e atendimento com hora marcada.",
  "fisio","Atendimento para quem pratica esporte e quer voltar com segurança depois de uma lesão. Em Catanduva, o studio oferece avaliação individual, exercícios e orientação, sempre com hora marcada.",
  "Corredores, praticantes de musculação, futebol, vôlei e ciclismo, e qualquer pessoa que precise retomar a atividade física depois de uma lesão, como entorses, dores no joelho ou no ombro e tendinites. Também atendemos quem quer treinar melhor e evitar novos problemas.",
  ["<strong>Avaliação:</strong> conversamos sobre o seu histórico, o esporte que você pratica e avaliamos seus movimentos. Se tiver pedido médico ou exames, traga.","<strong>Plano individual:</strong> montamos um conjunto de exercícios e orientações para o seu objetivo.","<strong>Acompanhamento:</strong> a evolução é reavaliada ao longo das sessões, e o retorno ao treino acontece de forma gradual."],
  ["Avaliação individual com a fisioterapeuta","Exercícios de fortalecimento, mobilidade e equilíbrio","Orientação para o retorno gradual ao treino","Atendimento com hora marcada, sem filas"])
servico("pilates-catanduva","Pilates","Pilates",
  "Aulas de Pilates em Catanduva | Studio Corpo em Movimento",
  "Aulas de pilates em Catanduva, em solo e em aparelhos, com turmas pequenas para melhorar postura, força e flexibilidade. Agende sua aula.",
  "pilates","Aulas de pilates em solo e em aparelhos, em turmas pequenas, para melhorar a postura, a força e a flexibilidade. O studio fica no centro de Catanduva e as aulas são com hora marcada.",
  "Pessoas de diferentes idades e níveis de condicionamento, de quem nunca fez pilates a quem já pratica. É uma boa opção para quem passa muitas horas sentado, sente o corpo travado ou quer um exercício com atenção ao movimento correto.",
  ["<strong>Primeiro contato:</strong> você conversa com a equipe sobre seus objetivos e possíveis limitações.","<strong>Aulas em turma pequena:</strong> o instrutor acompanha a execução dos exercícios, no solo e nos aparelhos.","<strong>Continuidade:</strong> os exercícios evoluem conforme o seu ritmo, com ajustes quando necessário."],
  ["Aulas em solo e em aparelhos","Turmas pequenas, com acompanhamento do instrutor","Foco em postura, força e flexibilidade","Instrutores com experiência e atendimento com hora marcada"])
servico("massagem-relaxante-catanduva","Massagem relaxante","Massagem relaxante",
  "Massagem Relaxante em Catanduva | Corpo em Movimento",
  "Massagem relaxante em Catanduva, com sessões de 50 minutos feitas por profissional formado para aliviar as tensões do dia a dia. Agende.",
  "massagem","Sessões de massagem relaxante de 50 minutos para aliviar as tensões do dia a dia, feitas por profissional formado, em ambiente tranquilo no centro de Catanduva.",
  "Quem sente o corpo pesado ou tenso por causa da rotina de trabalho, do estresse ou de muitas horas na mesma posição, e quer um momento de descanso com atendimento cuidadoso.",
  ["<strong>Conversa inicial:</strong> você conta onde sente mais tensão e se há algum cuidado especial.","<strong>Sessão de 50 minutos:</strong> a massagem é feita em sala reservada, com o ritmo e a pressão adequados para você.","<strong>Depois da sessão:</strong> você recebe orientações simples para manter o relaxamento nos dias seguintes."],
  ["Sessões de 50 minutos","Profissional formado","Sala reservada e ambiente tranquilo","Atendimento com hora marcada"])

# ---- Sobre
add("sobre", title="Sobre o Studio Corpo em Movimento | Catanduva",
    desc="Conheça a equipe de fisioterapeutas e instrutores de pilates do Studio Corpo em Movimento, com mais de dez anos de experiência em Catanduva.",
    ld=[ld_bc("sobre")],
    body=f'''<article><div class="duas">{img_tag("espaco","(max-width: 780px) 100vw, 520px",eager=True)}
<div><h1>Sobre o studio</h1>
<p>Somos uma equipe de fisioterapeutas e instrutores de pilates com mais de dez anos de experiência. Atendemos na {RUA}, no {BAIRRO} de {CIDADE}.</p></div></div>
<section><h2>Nosso jeito de atender</h2><p>Cada pessoa começa com uma avaliação individual. As turmas de pilates são pequenas e todos os atendimentos têm hora marcada, para que a equipe tenha tempo de olhar com atenção para o seu movimento.</p></section>
<section><h2>O que fazemos</h2><p>Trabalhamos com <a href="{u("fisioterapia-esportiva-catanduva")}">fisioterapia esportiva</a>, <a href="{u("pilates-catanduva")}">aulas de pilates</a> e <a href="{u("massagem-relaxante-catanduva")}">massagem relaxante</a>. Veja o que os clientes dizem nos <a href="{u("depoimentos")}">depoimentos</a>.</p></section>
{local_bloco()}
{cta()}</article>''')

# ---- Depoimentos
add("depoimentos", title="Depoimentos de Clientes | Studio Corpo em Movimento",
    desc="Veja o que os clientes do Studio Corpo em Movimento, em Catanduva, contam sobre a fisioterapia e o pilates. Relatos de quem já passou pelo studio.",
    ld=[ld_bc("depoimentos")],
    body=f'''<article><h1>Depoimentos de clientes</h1>
<p>Relatos de quem já frequentou o studio em Catanduva. Os resultados variam de pessoa para pessoa.</p>
<div class="grade dois">
<blockquote class="caixa citacao"><p>Ótimo atendimento, voltei a correr.</p><footer>Marcos</footer></blockquote>
<blockquote class="caixa citacao"><p>Minhas costas agradecem o pilates.</p><footer>Luciana</footer></blockquote>
</div>
<section><h2>Quer conhecer melhor o atendimento?</h2>
<p>Veja as <a href="{u("perguntas-frequentes")}">perguntas frequentes</a>, conheça a <a href="{u("fisioterapia-esportiva-catanduva")}">fisioterapia esportiva</a> e o <a href="{u("pilates-catanduva")}">pilates</a> ou <a href="{u("agendar")}">agende sua sessão</a>.</p></section></article>''')

# ---- FAQ
FAQ = [
 ("Preciso de pedido médico para fazer fisioterapia?", "Para a fisioterapia, recomendamos trazer o pedido médico e os exames, se você tiver. Eles ajudam na avaliação, mas você pode conversar com a equipe sobre o seu caso."),
 ("Qual é o telefone do studio?", f"Ligue para {FONE}. Também atendemos pelo WhatsApp {ZAP}."),
 ("Onde fica o studio em Catanduva?", f"Ficamos na {RUA}, {BAIRRO}, {CIDADE} - {UF}."),
 ("Qual é o horário de funcionamento?", "Atendemos de segunda a sexta, das 7h às 20h, e aos sábados, das 8h às 12h, sempre com hora marcada."),
 ("As aulas de pilates são em turmas grandes?", "Não. As turmas são pequenas, para que o instrutor acompanhe cada aluno."),
 ("Quanto tempo dura a sessão de massagem relaxante?", "A sessão de massagem relaxante dura 50 minutos."),
]
ld_faq = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]}
add("perguntas-frequentes", title="Perguntas Frequentes | Studio Corpo em Movimento",
    desc="Tire dúvidas sobre fisioterapia, pilates e massagem no Studio Corpo em Movimento, em Catanduva: pedido médico, horários, endereço e telefone.",
    ld=[ld_faq, ld_bc("perguntas-frequentes")],
    body=f'''<article><h1>Perguntas frequentes</h1>
{"".join(f'<div class="caixa"><h2 class="pergunta">{q}</h2><p>{a}</p></div>' for q,a in FAQ)}
<p>Não achou sua dúvida? Veja a página de <a href="{u("contato")}">contato</a> ou <a href="{u("agendar")}">agende uma sessão</a>.</p></article>''')

# ---- Contato
horas = "".join(f"<tr><th scope='row'>{d}</th><td>{h}</td></tr>" for d,h in HORARIO)
bb = f"{LON-0.004},{LAT-0.003},{LON+0.004},{LAT+0.003}"
add("contato", title="Contato e Endereço em Catanduva | Corpo em Movimento",
    desc="Endereço, telefone, horário de funcionamento e mapa do Studio Corpo em Movimento, na Rua Pernambuco, 450, Centro de Catanduva (SP).",
    ld=[ld_negocio(), ld_bc("contato")],
    body=f'''<article><h1>Contato e como chegar em Catanduva</h1>
<div class="grade dois">
<section class="caixa"><h2>Fale com a gente</h2>
<address class="nap"><strong>{NOME}</strong><br>{RUA} - {BAIRRO}<br>{CIDADE} - {UF}, {CEP}<br>Telefone: <a href="tel:{FONE_TEL}">{FONE}</a><br>WhatsApp: <a href="https://wa.me/{ZAP_TEL.strip("+")}">{ZAP}</a></address>
<p><a class="botao" href="{u("agendar")}">Agendar uma sessão</a></p></section>
<section class="caixa"><h2>Horário de funcionamento</h2><table class="horario"><tbody>{horas}</tbody></table><p>Atendimento com hora marcada.</p></section>
</div>
<section><h2>Mapa</h2>
<iframe class="mapa" title="Mapa com a localização do Studio Corpo em Movimento, na Rua Pernambuco, 450, em Catanduva" loading="lazy" width="1000" height="380" src="https://www.openstreetmap.org/export/embed.html?bbox={bb}&amp;layer=mapnik&amp;marker={LAT},{LON}"></iframe>
<p><a href="https://www.openstreetmap.org/?mlat={LAT}&amp;mlon={LON}#map=17/{LAT}/{LON}">Abrir o mapa em tela cheia</a></p></section>
<section><h2>Como chegar</h2><p>O studio fica no {BAIRRO} de {CIDADE}, interior de São Paulo, na {RUA}. Atendemos moradores da cidade e de municípios próximos, como Pindorama, Elisiário, Palmares Paulista e Catiguá. Conheça os <a href="{u("servicos")}">serviços</a> antes de vir.</p></section></article>''')

# ---- Agendar (formulário Netlify Forms)
add("agendar", title="Agendar Sessão de Fisioterapia ou Pilates em Catanduva",
    desc="Agende sua sessão de fisioterapia, pilates ou massagem no Studio Corpo em Movimento, em Catanduva. Preencha o formulário e retornamos o contato.",
    ld=[ld_bc("agendar")],
    body=f'''<article><h1>Agende sua sessão em Catanduva</h1>
<p>Preencha o formulário e a equipe retorna o contato para combinar o melhor horário. Se preferir, ligue para <a href="tel:{FONE_TEL}">{FONE}</a>.</p>
<form class="caixa form" name="agendamento" method="POST" action="{u("obrigado")}" data-netlify="true">
<input type="hidden" name="form-name" value="agendamento">
<p><label for="nome">Nome</label><input id="nome" name="nome" type="text" autocomplete="name" required></p>
<p><label for="telefone">Telefone ou WhatsApp</label><input id="telefone" name="telefone" type="tel" autocomplete="tel" required></p>
<p><label for="servico">Serviço</label><select id="servico" name="servico"><option>Fisioterapia esportiva</option><option>Pilates</option><option>Massagem relaxante</option></select></p>
<p><label for="mensagem">Mensagem (opcional)</label><textarea id="mensagem" name="mensagem" rows="4"></textarea></p>
<p><button class="botao" type="submit">Enviar pedido de agendamento</button></p>
</form>
<p>Conheça os <a href="{u("servicos")}">serviços do studio</a> ou veja as <a href="{u("perguntas-frequentes")}">perguntas frequentes</a>.</p></article>''')

# ---- Obrigado e 404 (noindex)
add("obrigado", title="Pedido enviado | Studio Corpo em Movimento", desc="Recebemos o seu pedido de agendamento no Studio Corpo em Movimento, em Catanduva. Retornaremos o contato.", robots="noindex, follow",
    body=f'<div class="caixa vazio"><h1>Obrigado pelo contato!</h1><p>Recebemos o seu pedido e vamos retornar em breve.</p><p><a href="{u("")}">Voltar para o início</a></p></div>')
add("404", title="Página não encontrada | Studio Corpo em Movimento", desc="A página que você procurou não foi encontrada. Volte ao início do Studio Corpo em Movimento, em Catanduva.", robots="noindex, follow",
    body=f'<div class="caixa vazio"><h1>Página não encontrada</h1><p>Confira o endereço ou volte para o <a href="{u("")}">início</a> ou para os <a href="{u("servicos")}">serviços</a>.</p></div>')

for slug in ORDER:
    page = layout(slug, PAGES[slug])
    path = f"{OUT}/404.html" if slug=="404" else (f"{OUT}/index.html" if slug=="" else f"{OUT}/{slug}/index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True); open(path,"w",encoding="utf-8").write(page)

# ---- CSS: apenas acréscimos (visual da v0 preservado)
with open(OUT + "/css/estilo.css","a",encoding="utf-8") as f: f.write('''
/* 7. ACRESCIMOS DA V1 (SEO, acessibilidade e novos blocos) ------------ */
.pular{position:absolute;left:-999px;top:0;background:#fff;color:var(--escuro);padding:8px 14px;z-index:20}
.pular:focus{left:8px;top:8px}
a.logo{text-decoration:none}
.menu a[aria-current="page"]{background:var(--suave);color:var(--escuro)}
.hero h1{font-size:46px}
.hero .topo-cta{margin-top:22px}
.breadcrumb{font-size:15px;margin-bottom:18px;color:#4a5560}
.conteudo h2{font-size:28px}
.conteudo h3{font-size:22px}
.hero h1{font-size:46px}
.conteudo .caixa h2,.conteudo .card h2,.conteudo h2.pergunta{font-size:21px;margin-bottom:8px}
.conteudo section{margin-bottom:12px}
.conteudo ul,.conteudo ol{margin:0 0 14px;padding-left:24px}
.card h3,.card h2{margin-bottom:8px}
blockquote.caixa{margin:0}
blockquote.caixa footer{font-weight:700;color:var(--escuro)}
.mapa{width:100%;height:380px;border:1px solid var(--borda);border-radius:16px}
.horario{border-collapse:collapse;width:100%}.horario th,.horario td{text-align:left;padding:6px 0;border-bottom:1px solid var(--borda)}
.nap{font-style:normal}
.form label{display:block;font-weight:700;margin-bottom:4px}
.form input,.form select,.form textarea{width:100%;font:inherit;padding:10px 12px;border:1px solid #b7c2ca;border-radius:10px}
.form button{border:0;cursor:pointer;font:inherit}
.rodape{text-align:left}
.rodape-in{max-width:1080px;margin:0 auto;display:grid;grid-template-columns:2fr 1fr 1fr;gap:28px}
.rodape a{color:#fff}.rodape ul{list-style:none;margin:6px 0 0;padding:0}.rodape li{margin-bottom:6px}
.rodape address{font-style:normal;margin-top:6px}
.rodape-fim{max-width:1080px;margin:24px auto 0;padding-top:16px;border-top:1px solid #2c5a78;text-align:center}
@media(max-width:780px){.rodape-in{grid-template-columns:1fr}.hero h1{font-size:32px}.conteudo h2{font-size:24px}}
''')

# ---- robots, sitemap, redirects, README
indexaveis = [s for s in ORDER if s not in ("obrigado","404")]
open(OUT+"/robots.txt","w").write(f"""User-agent: *
Allow: /
# Parametros de rastreamento geram URLs duplicadas das mesmas paginas
Disallow: /*?utm_
Disallow: /*?fbclid=
Disallow: /*?gclid=

# CSS, JS e imagens NAO sao bloqueados, para o Google renderizar a pagina.
# /obrigado/ e a 404 usam meta robots noindex (nao bloquear aqui, ou o Google nao leria o noindex).

Sitemap: {BASE}/sitemap.xml
""")
sm = ['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for s in indexaveis: sm.append(f"  <url><loc>{abs_(s)}</loc><lastmod>{LASTMOD}</lastmod></url>")
sm.append("</urlset>"); open(OUT+"/sitemap.xml","w").write("\n".join(sm)+"\n")
REDIR = [("/index.html","/"),("/sobre.html","/sobre/"),("/contato.html","/contato/"),("/depoimentos.html","/depoimentos/"),("/faq.html","/perguntas-frequentes/"),
         ("/agendar.html","/agendar/"),("/obrigado.html","/obrigado/"),("/Servicos/Fisioterapia_Esportiva.html","/fisioterapia-esportiva-catanduva/"),
         ("/Servicos/Pilates.html","/pilates-catanduva/"),("/Servicos/Massagem_Relaxante.html","/massagem-relaxante-catanduva/")]
open(OUT+"/_redirects","w").write("# Redirecionamentos 301 (v0 -> v1). Funciona no Netlify e no Cloudflare Pages.\n"+"\n".join(f"{a}  {b}  301" for a,b in REDIR)+"\n")
json.dump({"BASE":BASE,"REDIR":REDIR,"ORDER":ORDER,"INDEX":indexaveis}, open("meta.json","w"), ensure_ascii=False)
print("ok", len(ORDER), "páginas")
