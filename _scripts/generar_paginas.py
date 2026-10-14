"""Páginas internas del Estudio Jurídico Galíndez: el-estudio.html + las 4 áreas.
Toma del index el <head>, el header/menú y el footer (como generar_extras.py) y arma cada página
con su contenido como datos. Idempotente: volver a correrlo cuando cambia el index.
Uso: python _scripts/generar_paginas.py
Textos: los de la web actual (estudiojuridicodariogalindez.com.ar), reescritos en voseo."""
import re
from pathlib import Path

D = Path(__file__).resolve().parent.parent
idx = (D / "index.html").read_text(encoding="utf8")

head_tpl = idx[:idx.index("<title>")]
links_head = idx[idx.index('<link rel="preconnect"'):idx.index("</head>")]
links_head = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', "", links_head, flags=re.S)
links_head = re.sub(r'<meta property="og:.*?>\n|<meta name="twitter:.*?>\n', "", links_head)
top = idx[idx.index("<!-- ============ HEADER ============ -->"):idx.index("<main>")]
f0 = idx.index("<!-- ============ FOOTER ============ -->")
foot = idx[f0:idx.index('<a class="wa-float', f0)]
cola_modal = idx[idx.index('<a class="wa-float', f0):idx.index('<script src="./main.js"')]
cola = re.sub(r'<div class="modal".*?</div>\s*</div>\s*', "", cola_modal, flags=re.S)  # páginas sin formulario: sin modal

def interna(s):
    s = re.sub(r'href="#(?!")', 'href="./index.html#', s)
    return s.replace('href="./index.html#inicio"', 'href="./index.html"')
top, foot = interna(top), interna(foot)

AREAS = {
    "derecho-laboral": {
        "n": "01", "nombre": "Derecho Laboral", "foto": "justicia-practica.jpg",
        "title": "Derecho Laboral en CABA | Estudio Jurídico Galíndez",
        "desc": "Accidentes de trabajo, reclamos ante la ART e indemnizaciones por despido. Asistencia a trabajadores en CABA y Provincia de Buenos Aires.",
        "intro": "Asistencia jurídica para trabajadores frente a accidentes, enfermedades laborales y la ruptura del vínculo de trabajo.",
        "items": [("Accidentes de trabajo y ART", "Analizamos el accidente o la enfermedad profesional, hacemos el seguimiento del trámite y reclamamos las prestaciones e indemnizaciones que correspondan."),
                  ("Indemnizaciones por despido", "Revisamos la liquidación y el intercambio telegráfico, y reclamamos por despidos con o sin causa, registración deficiente y diferencias salariales.")],
        "wa": "Hola, quisiera hacer una consulta de derecho laboral."},
    "derecho-civil-familia": {
        "n": "02", "nombre": "Civil y Familia", "foto": "justicia-consulta.jpg",
        "title": "Derecho Civil y Familia en CABA | Estudio Jurídico Galíndez",
        "desc": "Accidentes de tránsito, sucesiones, divorcios, alimentos y régimen de comunicación. Acompañamiento claro y reservado en CABA y Provincia de Buenos Aires.",
        "intro": "Acompañamiento claro y reservado para resolver conflictos patrimoniales, accidentes y asuntos familiares sensibles.",
        "items": [("Accidentes de tránsito", "Reclamos por daños materiales, lesiones y las consecuencias derivadas de siniestros viales."),
                  ("Sucesiones", "Inicio y seguimiento de procesos sucesorios, declaratorias de herederos y organización patrimonial."),
                  ("Divorcios y alimentos", "Divorcio, convenios, cuota alimentaria y cumplimiento de las obligaciones familiares."),
                  ("Cuidado y comunicación", "Régimen de comunicación, cuidado personal y medidas ante situaciones de violencia familiar.")],
        "wa": "Hola, quisiera hacer una consulta de derecho civil y familia."},
    "derecho-societario": {
        "n": "03", "nombre": "Derecho Societario", "foto": "justicia-institucional.jpg",
        "title": "Derecho Societario y Empresas | Estudio Jurídico Galíndez",
        "desc": "Constitución de S.A. y S.R.L. y asesoramiento legal para empresas, profesionales y emprendimientos en CABA y Provincia de Buenos Aires.",
        "intro": "Estructuras jurídicas sólidas y asesoramiento preventivo para empresas, profesionales y nuevos emprendimientos.",
        "items": [("Constitución de sociedades", "Planificación y constitución de Sociedades Anónimas (S.A.) y Sociedades de Responsabilidad Limitada (S.R.L.)."),
                  ("Asesoramiento empresarial", "Acompañamiento legal cotidiano: contratos, decisiones societarias y prevención de conflictos para empresas y emprendimientos.")],
        "wa": "Hola, quisiera hacer una consulta de derecho societario."},
    "derecho-penal": {
        "n": "04", "nombre": "Derecho Penal", "foto": "justicia-hero.jpg",
        "title": "Derecho Penal en CABA | Estudio Jurídico Galíndez",
        "desc": "Defensas penales, excarcelaciones, acuerdos y ejecución de la pena. Defensa técnica y acompañamiento reservado en CABA y Provincia de Buenos Aires.",
        "intro": "Defensa técnica inmediata, evaluación estratégica del expediente y acompañamiento reservado durante todo el proceso.",
        "items": [("Defensas penales", "Asistencia desde las primeras actuaciones, diseño de la estrategia y representación durante el proceso penal."),
                  ("Excarcelaciones", "Presentación y seguimiento de pedidos de excarcelación y de morigeración de medidas restrictivas."),
                  ("Acuerdos y alternativas", "Evaluación de acuerdos con la fiscalía y el juez, según las circunstancias y los objetivos de cada caso."),
                  ("Ejecución de la pena", "Solicitudes de salidas transitorias, prisión domiciliaria y otros institutos aplicables.")],
        "wa": "Hola, quisiera hacer una consulta de derecho penal."},
}

def cabecera(foto, ruta, n, h1, intro):
    num = f'<span class="ph-n">{n}</span>' if n else ""
    return f'''
<!-- ============ CABECERA DE PÁGINA (foto B/N + ruta) ============ -->
<section class="ph">
  <div class="ph-bg" style="background-image:url(img/{foto})" aria-hidden="true"></div>
  <div class="wrap ph-in">
    <nav class="ruta rise" aria-label="Ruta"><a href="./index.html">Inicio</a><i class="ti ti-chevron-right" aria-hidden="true"></i><span>{ruta}</span></nav>
    {num}<h1 class="ph-h1 rise d1">{h1}</h1>
    <p class="ph-lead rise d2">{intro}</p>
  </div>
</section>'''

def cta(wa):
    return f'''
<!-- ============ CTA (franja amarilla: contrasta con el footer oscuro) ============ -->
<section class="cta-y">
  <div class="wrap cta-y-in reveal">
    <div>
      <p class="cta-y-eye">Evaluación profesional</p>
      <h2>Conversemos<br>sobre tu caso.</h2>
    </div>
    <div class="cta-y-btns">
      <a class="btn btn-ink js-wa" href="#" data-msg="{wa}">Consultar por WhatsApp</a>
      <a class="btn btn-ink-line" href="./index.html#contacto">Completar el formulario</a>
    </div>
  </div>
</section>'''

# foto de fondo de «Otras áreas»: distinta a la de la cabecera de cada página
FONDO_OTRAS = {"derecho-laboral": "justicia-institucional.jpg", "derecho-civil-familia": "justicia-hero.jpg",
               "derecho-societario": "justicia-practica.jpg", "derecho-penal": "justicia-consulta.jpg", None: "justicia-practica.jpg"}

def otras(actual):
    cards = "".join(f'''
      <a class="otra reveal" href="./{k}.html"><span>{a["n"]}</span><b>{a["nombre"]}</b><i class="ti ti-arrow-right" aria-hidden="true"></i></a>'''
                    for k, a in AREAS.items() if k != actual)
    titulo = "Otras áreas <em>del estudio.</em>" if actual else "Áreas <em>de práctica.</em>"
    return f'''
<!-- ============ OTRAS ÁREAS ============ -->
<section class="sec sec-foto otras-sec">
  <div class="foto-bg" style="background-image:url(img/{FONDO_OTRAS[actual]})" aria-hidden="true"></div>
  <div class="wrap">
    <div class="sec-head reveal"><h2 class="h2">{titulo}</h2></div>
    <div class="otras{' otras-4' if not actual else ''}">{cards}
    </div>
  </div>
</section>'''

def page(name, title, desc, body, schema="", modal=False):
    html = (head_tpl + f'<title>{title}</title>\n<meta name="description" content="{desc}">\n'
            + '<meta name="theme-color" content="#0E0E0D">\n<link rel="icon" type="image/png" href="./favicon.png">\n<link rel="apple-touch-icon" href="./favicon.png">\n'
            + links_head + schema + "</head>\n<body>\n\n" + top + "<main>\n" + body + "\n\n</main>\n\n" + foot
            + (cola_modal if modal else cola) + '<script src="./main.js"></script>\n</body>\n</html>\n')
    (D / name).write_text(html, encoding="utf8", newline="\n"); print("ok", name)

# ---------- áreas
for k, a in AREAS.items():
    items = "".join(f'''
      <li class="serv reveal"><span class="serv-n">{i:02d}</span><div><h3>{t}</h3><p>{d}</p></div></li>''' for i, (t, d) in enumerate(a["items"], 1))
    body = cabecera(a["foto"], a["nombre"], a["n"] + " · Área de práctica", a["nombre"], a["intro"]) + f'''

<!-- ============ QUÉ INCLUYE ============ -->
<section class="sec servs-sec">
  <div class="wrap servs-grid">
    <div class="servs-head reveal">
      <p class="eyebrow">Cómo te ayudamos</p>
      <h2 class="h2">Asistencia <em>en cada etapa.</em></h2>
      <p class="lead">Analizamos tu situación, te explicamos las alternativas con claridad y definimos juntos la estrategia.</p>
    </div>
    <ol class="servs{' servs-2' if len(a['items']) == 2 else ''}">{items}
    </ol>
  </div>
</section>
''' + otras(k) + cta(a["wa"])
    schema = f'''<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Service","name":"{a['nombre']}","serviceType":"{a['nombre']}","provider":{{"@type":"LegalService","name":"Estudio Jurídico Galíndez","telephone":"+54 11 4054-1945","address":{{"@type":"PostalAddress","streetAddress":"Av. Corrientes 1441","addressLocality":"Ciudad Autónoma de Buenos Aires","addressCountry":"AR"}}}},"areaServed":["Ciudad Autónoma de Buenos Aires","Provincia de Buenos Aires"]}}
</script>
'''
    page(f"{k}.html", a["title"], a["desc"], body, schema)

# ---------- preguntas frecuentes (las del index + las de cada área; solo datos de la web actual)
FAQ = [
    ("La primera consulta", [
        ("¿Cómo coordino una consulta?", "Por WhatsApp, por teléfono al 011 4054-1945, por email o completando el formulario. La atención en el estudio es con cita previa, así que coordinamos día y horario antes del encuentro."),
        ("¿Qué conviene contar en el primer mensaje?", "Una descripción breve de lo que pasó y en qué etapa está tu caso. No hace falta incluir información sensible: los detalles se analizan después, en la consulta."),
        ("¿Lo que cuento en la consulta es confidencial?", "Siempre. La reserva profesional acompaña todo el proceso, desde el primer mensaje hasta la resolución del caso."),
        ("¿Quién lleva mi caso?", "Cada asunto lo dirige personalmente el Dr. Darío Galíndez, titular del estudio, con comunicación directa durante todo el proceso."),
        ("¿Atienden casos en Provincia de Buenos Aires?", "Sí. El estudio está en Av. Corrientes 1441, CABA, y asiste a particulares y empresas tanto en la Ciudad como en la Provincia de Buenos Aires."),
    ]),
    ("Según el área", [
        ("Tuve un accidente laboral, ¿me ayudan con la ART?", "Sí. Analizamos el accidente o la enfermedad profesional, hacemos el seguimiento del trámite y reclamamos las prestaciones e indemnizaciones que correspondan."),
        ("Me despidieron, ¿qué revisan?", "La liquidación final y el intercambio telegráfico. Reclamamos por despidos con o sin causa, registración deficiente y diferencias salariales."),
        ("¿Llevan sucesiones y divorcios?", "Sí: inicio y seguimiento de sucesiones y declaratorias de herederos, divorcios, convenios, cuota alimentaria y régimen de comunicación."),
        ("Detuvieron a un familiar, ¿desde cuándo pueden intervenir?", "La defensa puede asumirse desde las primeras actuaciones: diseño de la estrategia, pedidos de excarcelación y representación durante todo el proceso penal."),
        ("¿También asesoran a empresas y emprendimientos?", "Sí. Constituimos S.A. y S.R.L. y acompañamos a empresas y emprendimientos con contratos, decisiones societarias y prevención de conflictos."),
    ]),
]
grupos = ""
for g, (titulo, qs) in enumerate(FAQ, 1):
    dets = "".join(f'\n      <details><summary>{q}</summary><div class="faq-a"><p>{a}</p></div></details>' for q, a in qs)
    grupos += (f'\n    <div class="faq-grupo">\n      <h2 class="faq-grupo-t reveal"><span>{g:02d}</span>{titulo}</h2>'
               f'\n      <div class="faq reveal">{dets}\n      </div>\n    </div>')
body = cabecera("justicia-institucional.jpg", "Preguntas frecuentes", "", "Antes de <em>consultar.</em>",
                "Lo que más nos preguntan al dar el primer paso, sobre la consulta y sobre cada área.") + f'''

<!-- ============ PREGUNTAS ============ -->
<section class="sec faq-pag">
  <div class="wrap faq-pag-grid">
    <div class="faq-pag-list">{grupos}
    </div>
    <aside class="faq-pag-aside reveal">
      <div class="faq-card">
        <div><h3>¿Tenés otra duda?</h3>
        <p>Escribinos y te respondemos personalmente.</p></div>
        <div class="faq-card-btns">
          <a class="btn btn-dark js-wa" href="#" data-msg="Hola, tengo una consulta.">Consultar por WhatsApp</a>
          <a class="btn btn-accent" href="./index.html#contacto">Enviar un email</a>
        </div>
      </div>
    </aside>
  </div>
</section>
''' + otras(None) + cta("Hola, quisiera hacer una consulta.")
faq_schema = ('<script type="application/ld+json">\n{"@context":"https://schema.org","@type":"FAQPage","mainEntity":['
              + ",".join('{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}' % (q, a) for _, qs in FAQ for q, a in qs)
              + ']}\n</script>\n')
page("preguntas-frecuentes.html", "Preguntas frecuentes | Estudio Jurídico Galíndez",
     "Cómo coordinar una consulta, confidencialidad, accidentes de trabajo, despidos, sucesiones, defensas penales y empresas. Estudio Jurídico Galíndez, CABA.", body, faq_schema)

# ---------- el estudio
body = cabecera("justicia-consulta.jpg", "El estudio", "", "Dirección personal, criterio estratégico <em>y compromiso.</em>",
                "Asesoramiento a particulares, empresas y emprendimientos en la Ciudad y la Provincia de Buenos Aires.") + '''

<!-- ============ PERFIL ============ -->
<section class="sec sec-3 perfil">
  <div class="wrap perfil-grid">
    <figure class="tri-foto perfil-foto reveal">
      <div class="vitral">
        <div class="vitral-marco" aria-hidden="true"></div>
        <div class="vitral-img">
          <!-- foto tomada de la web actual: confirmar con el cliente que sea un retrato real -->
          <img src="./img/dr-dario-galindez.jpg" alt="Retrato del Dr. Darío Galíndez" width="928" height="1152" loading="lazy">
        </div>
      </div>
      <figcaption><b>Dr. Darío Galíndez</b><span>Titular del estudio</span></figcaption>
    </figure>
    <div class="perfil-txt reveal">
      <p class="eyebrow">Perfil profesional</p>
      <h2 class="h2">Seriedad, análisis riguroso <em>y comunicación directa.</em></h2>
      <p>El estudio brinda asesoramiento a particulares, empresas y emprendimientos con una práctica fundada en la seriedad, el análisis riguroso y la comunicación directa.</p>
      <p>Cada asunto recibe una evaluación responsable de sus alternativas, sus tiempos y sus riesgos. La prioridad es construir una estrategia clara, comprensible y adecuada a tus intereses.</p>
      <p>La confidencialidad y el trato respetuoso acompañan todo el proceso, desde la primera consulta hasta la resolución del caso.</p>
    </div>
  </div>
</section>
''' + otras(None) + cta("Hola, quisiera hacer una consulta.")
page("el-estudio.html", "El estudio y el Dr. Darío Galíndez | Estudio Jurídico Galíndez",
     "Perfil del Estudio Jurídico Galíndez: dirección personal del Dr. Darío Galíndez, análisis riguroso y absoluta reserva. Av. Corrientes 1441, CABA.", body)

# ---------- index: los links a páginas pendientes ya existen
i_new = idx.replace(" data-soon", "")
if i_new != idx:
    (D / "index.html").write_text(i_new, encoding="utf8", newline="\n"); print("index: data-soon quitados")

# ---------- CSS de las páginas internas (una sola vez)
css_p = D / "styles.css"; c = css_p.read_text(encoding="utf8")
if "/* ---------- preguntas frecuentes (página)" not in c:
    c += '''
/* ---------- preguntas frecuentes (página): los dos grupos lado a lado y la consulta abajo, a todo el ancho ---------- */
.faq-pag-grid{display:grid;gap:4.5rem}
.faq-pag-list{display:grid;grid-template-columns:1fr 1fr;gap:4.5rem;align-items:start}
.faq-pag-grid>*,.faq-pag-list>*{min-width:0}
.faq-grupo-t{flex-wrap:wrap}
.faq-grupo-t{display:flex;align-items:baseline;gap:1rem;margin-bottom:1.4rem;font-size:clamp(1.8rem,3vw,2.4rem)}
.faq-grupo-t span{color:var(--y)}
.faq-pag-aside{width:100%}  /* mismo ancho que los dos grupos de arriba */
.faq-pag-aside .faq-card{display:grid;grid-template-columns:1fr auto;align-items:center;gap:2.5rem;padding:2.2rem 2.6rem;text-align:left}
.faq-pag-aside .faq-card-btns{grid-template-columns:auto auto;margin-top:0}
@media (max-width:1024px){
  .faq-pag-list{grid-template-columns:1fr;gap:3.5rem}
  .faq-pag-aside .faq-card{grid-template-columns:1fr;gap:1.4rem;text-align:center}
  .faq-pag-aside .faq-card-btns{justify-content:center}
}
@media (max-width:768px){
  .faq-grupo-t{justify-content:center;text-align:center}
  .faq-pag-aside .faq-card-btns{grid-template-columns:1fr}
}
'''
    css_p.write_text(c, encoding="utf8"); print("css faq ok")
if "/* ---------- páginas internas" not in c:
    c += '''
/* ---------- páginas internas (generar_paginas.py) ---------- */
.ph{position:relative;min-height:62vh;display:flex;align-items:flex-end;overflow:hidden;background:var(--bg)}
.ph-bg{position:absolute;inset:0;background-size:cover;background-position:center;filter:grayscale(1)}
.ph-bg::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(14,14,13,.72),rgba(14,14,13,.6) 40%,rgba(14,14,13,.95)),linear-gradient(135deg,rgba(253,215,75,.12),transparent 45%)}
.ph::after{content:"";position:absolute;left:0;right:0;bottom:0;height:1px;background:linear-gradient(90deg,transparent,rgba(253,215,75,.75) 50%,transparent)}
.ph-in{position:relative;z-index:1;padding-top:calc(var(--hdr-top) + 4rem);padding-bottom:4.4rem}
.ruta{display:flex;align-items:center;flex-wrap:wrap;gap:.6rem;margin-bottom:1.6rem;font-size:.74rem;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:var(--muted)}
.ruta a{transition:color .3s}
.ruta a:hover{color:var(--y)}
.ruta i{font-size:.9rem;color:var(--y)}
.ruta span{color:var(--y)}
.ph-n{display:block;margin-bottom:.6rem;font-family:var(--f-head);font-weight:700;font-size:1.3rem;letter-spacing:.12em;text-transform:uppercase;color:var(--y)}
.ph-h1{max-width:52rem;font-size:clamp(2.8rem,5.4vw,4.6rem);line-height:1}
.ph-h1 em{color:var(--y)}
.ph-lead{max-width:40rem;margin-top:1.4rem;font-size:1.12rem;color:var(--text)}
/* qué incluye cada área */
.servs-grid{display:grid;grid-template-columns:.85fr 1.15fr;gap:5rem;align-items:start}
.servs-head{position:sticky;top:calc(var(--hdr) + 2rem)}
.servs-head .lead{margin:1.2rem 0 2rem}
.serv{display:grid;grid-template-columns:auto 1fr;gap:1.8rem;padding:2.2rem 0}
.serv+.serv{border-top:1px solid var(--line)}
.serv-n{font-family:var(--f-head);font-weight:700;font-size:2.6rem;line-height:.9;color:var(--y)}
.serv h3{font-size:1.75rem}
.serv p{margin-top:.6rem;color:var(--muted)}
.servs-2 .serv{padding:3rem 0}
/* otras áreas */
.otras{display:grid;grid-template-columns:repeat(3,1fr);gap:1.2rem}
.otras-4{grid-template-columns:repeat(4,1fr)}
.otra{display:flex;flex-direction:column;gap:.5rem;padding:1.8rem 1.6rem;border:1px solid var(--line);border-top:2px solid var(--y);background:rgba(255,255,255,.025);transition:background .5s,border-color .5s,opacity .9s var(--ease),transform .9s var(--ease)}
.otra:hover{background:rgba(253,215,75,.05);border-color:var(--line-y)}
.otra span{font-family:var(--f-head);font-weight:700;font-size:1.2rem;letter-spacing:.08em;color:var(--y)}
.otra b{font-family:var(--f-head);font-weight:700;font-size:1.6rem;letter-spacing:.01em;text-transform:uppercase;line-height:1.05;color:var(--head)}
.otra i{margin-top:auto;padding-top:1rem;font-size:1.3rem;color:var(--y);transition:transform .3s var(--ease)}
.otra:hover i{transform:translateX(5px)}
/* CTA amarillo */
.cta-y{background:var(--y);color:var(--ink)}
.cta-y-in{display:flex;align-items:center;justify-content:space-between;gap:2.5rem;padding-top:4.4rem;padding-bottom:4.4rem}
.cta-y-eye{font-size:.76rem;font-weight:700;letter-spacing:.28em;text-transform:uppercase}
.cta-y h2{margin-top:.5rem;font-size:clamp(2.2rem,4vw,3.3rem);color:var(--ink)}
.cta-y-btns{display:flex;flex-wrap:wrap;gap:.9rem}
.btn-ink{background:var(--ink);color:var(--y)}
.btn-ink:hover{background:#2a2a28}
.btn-ink-line{border-color:var(--ink);color:var(--ink)}
.btn-ink-line:hover{background:var(--ink);color:var(--y)}
/* perfil */
.perfil-grid{display:grid;grid-template-columns:minmax(0,380px) 1fr;gap:5.5rem;align-items:center}
.perfil-foto{margin:0}
.perfil-txt .h2{margin-bottom:1.6rem}
.perfil-txt>p:not(.eyebrow){color:var(--muted)}
.perfil-txt>p+p{margin-top:1rem}
@media (max-width:1024px){
  .servs-grid,.perfil-grid{grid-template-columns:1fr;gap:3rem}
  .servs-head{position:static}
  .perfil-foto{width:min(100%,340px);margin:0 auto}
  .otras-4{grid-template-columns:repeat(2,1fr)}
  .cta-y-in{flex-direction:column;text-align:center}
  .cta-y-btns{justify-content:center}
}
@media (max-width:768px){
  .ph{min-height:auto}
  .ph-in{padding-top:calc(var(--hdr-top) + 3rem);padding-bottom:3.2rem;text-align:center}
  .ruta{justify-content:center}
  .ph-h1{font-size:clamp(2.2rem,9.6vw,3rem)}
  .ph-lead{margin-left:auto;margin-right:auto;font-size:1rem}
  .servs-head,.perfil-txt{display:flex;flex-direction:column;align-items:center;text-align:center}
  .serv{grid-template-columns:1fr;gap:.6rem;text-align:center;padding:1.8rem 0}
  .servs-2 .serv{padding:2.2rem 0}
  .otras,.otras-4{grid-template-columns:1fr}
  .otra{align-items:center;text-align:center}
      .cta-y-btns{flex-direction:column;align-items:center;width:100%}
  .cta-y-btns .btn{width:100%;max-width:300px}
}
'''
    css_p.write_text(c, encoding="utf8"); print("css ok")
