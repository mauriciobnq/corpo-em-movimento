import os, re, json, glob, collections
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
GENERIC = {"clique aqui","aqui","saiba mais","veja mais","leia mais","ver mais"}

def audit(root, home="index.html"):
    files = sorted(glob.glob(root+"/**/*.html", recursive=True))
    pages = {}
    for f in files:
        rel = os.path.relpath(f, root)
        soup = BeautifulSoup(open(f,encoding="utf-8").read(), "lxml")
        pages[rel] = soup
    def norm(rel_from, href):
        if not href or href.startswith(("http","mailto:","tel:","#")): return None
        href = href.split("#")[0].split("?")[0]
        base = os.path.dirname(rel_from)
        p = os.path.normpath(os.path.join(base, href)) if not href.startswith("/") else href.lstrip("/")
        if href.endswith("/") or p in ("", "."): p = os.path.join(p, "index.html")
        elif os.path.isdir(os.path.join(root,p)): p = os.path.join(p,"index.html")
        return p
    # grafo
    graph = {r: set() for r in pages}
    generic = []
    broken = []
    for r,s in pages.items():
        for a in s.find_all("a", href=True):
            t = norm(r, a["href"])
            if t is None: continue
            if t in pages: graph[r].add(t)
            else: broken.append((r,a["href"]))
            if a.get_text(strip=True).lower() in GENERIC: generic.append((r,a.get_text(strip=True)))
    # profundidade
    depth = {home:0}; q=collections.deque([home])
    while q:
        c=q.popleft()
        for n in graph[c]:
            if n not in depth: depth[n]=depth[c]+1; q.append(n)
    inbound = collections.Counter(t for r in graph for t in graph[r] if t!=r)
    orphans = [r for r in pages if r!=home and inbound[r]==0]
    unreachable = [r for r in pages if r not in depth]
    deeper = [r for r in pages if r in depth and depth[r]>3]
    # meta
    titles = {r:(s.title.get_text(strip=True) if s.title else "") for r,s in pages.items()}
    descs = {r:((s.find("meta",attrs={"name":"description"}) or {}).get("content","") or "") for r,s in pages.items()}
    tc = collections.Counter(titles.values()); dc = collections.Counter(descs.values())
    uniq_t = sum(1 for r in pages if titles[r] and tc[titles[r]]==1)
    uniq_d = sum(1 for r in pages if descs[r] and dc[descs[r]]==1)
    # imagens
    img_total=img_noalt=img_nowh=img_lazy=img_srcset=0; used=set(); served_per_page={}
    for r,s in pages.items():
        served=0
        for im in s.find_all("img"):
            img_total+=1
            if not im.get("alt","").strip(): img_noalt+=1
            if not (im.get("width") and im.get("height")): img_nowh+=1
            if im.get("loading")=="lazy": img_lazy+=1
            if im.get("srcset"): img_srcset+=1
            src = im.get("src",""); path=None
            if im.get("srcset"):
                cands=[(int(m.group(2)), m.group(1)) for m in re.finditer(r"(\S+)\s+(\d+)w", im["srcset"])]
                slot = 520 if "520px" in im.get("sizes","") else 330
                ok=[c for c in sorted(cands) if c[0]>=slot]; path=(ok[0] if ok else sorted(cands)[-1])[1]
            else: path=src
            p = norm(r, path) if not path.startswith("/") else path.lstrip("/")
            if p and os.path.exists(os.path.join(root,p)): used.add(p); served+=os.path.getsize(os.path.join(root,p))
        served_per_page[r]=served
    folder = os.path.join(root,"imagens")
    folder_bytes = sum(os.path.getsize(f) for f in glob.glob(folder+"/*"))
    used_bytes = sum(os.path.getsize(os.path.join(root,p)) for p in used)
    # estrutura
    h1_bad=skip=0; sem_count={"header":0,"nav":0,"main":0,"footer":0}; lang=0; canon=0; viewport=0; og=0
    for r,s in pages.items():
        if len(s.find_all("h1"))!=1: h1_bad+=1
        lv=[int(h.name[1]) for h in s.find_all(re.compile("^h[1-6]$"))]
        if any(b-a>1 for a,b in zip(lv,lv[1:])) or (lv and lv[0]!=1): skip+=1
        for k in sem_count:
            if s.find(k): sem_count[k]+=1
        if s.html and s.html.get("lang"): lang+=1
        if s.find("link",rel="canonical"): canon+=1
        if s.find("meta",attrs={"name":"viewport"}): viewport+=1
        if s.find("meta",property="og:title"): og+=1
    # json-ld
    ld_ok=ld_bad=0; types=collections.Counter()
    for s in pages.values():
        for sc in s.find_all("script",type="application/ld+json"):
            try:
                d=json.loads(sc.string); ld_ok+=1
                for t in ([d.get("@type")] if isinstance(d.get("@type"),str) else d.get("@type",[])): types[t]+=1
            except Exception: ld_bad+=1
    # NAP
    phones=collections.Counter(); addr=collections.Counter()
    for s in pages.values():
        txt=s.get_text(" ")
        for m in re.findall(r"\(?\d{2}\)?\s?\d{4,5}-\d{4}", txt): phones[m]+=1
        for m in re.findall(r"(?:Rua|R\.|Av\.)\s+Pernambuco,?\s*450", txt): addr[m]+=1
    robots = open(root+"/robots.txt").read() if os.path.exists(root+"/robots.txt") else None
    return dict(paginas=len(pages), titulo_unico=uniq_t, desc_unica=uniq_d, titulo_max=max(len(t) for t in titles.values()),
        desc_max=max(len(d) for d in descs.values()), titulos_vazios_ou_genericos=sum(1 for t in titles.values() if t in("","Serviço","Início")),
        imgs=img_total, imgs_sem_alt=img_noalt, imgs_sem_wh=img_nowh, imgs_lazy=img_lazy, imgs_srcset=img_srcset,
        peso_pasta_imagens_kb=round(folder_bytes/1024), peso_imagens_usadas_kb=round(used_bytes/1024),
        peso_home_imagens_kb=round(served_per_page[home]/1024), 
        paginas_acima_3_cliques=len(deeper), paginas_inalcancaveis=len(unreachable), orfas=sorted(orphans),
        profundidade={r:depth.get(r,None) for r in sorted(pages)}, links_genericos=generic, links_quebrados=broken,
        h1_incorreto=h1_bad, hierarquia_pulada=skip, semantica=sem_count, lang=lang, canonical=canon, viewport=viewport, og=og,
        jsonld_validos=ld_ok, jsonld_invalidos=ld_bad, jsonld_tipos=dict(types), telefones=dict(phones), enderecos=dict(addr),
        robots=bool(robots), sitemap=os.path.exists(root+"/sitemap.xml"),
        titles=titles, descs=descs)
if __name__=="__main__":
    res={"v0":audit("../v0"),"v1":audit("../v1")}
    json.dump(res,open("audit.json","w"),ensure_ascii=False,indent=1)
    for v,r in res.items():
        print("=====",v)
        for k,x in r.items():
            if k not in("titles","descs","profundidade"): print(f" {k}: {x}")
    print(res["v0"]["profundidade"]); print(res["v1"]["profundidade"])
