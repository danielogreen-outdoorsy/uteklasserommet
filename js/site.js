/* Felles header + footer for alle sider på Uteklasserommet.no
   Injiseres med JS slik at navigasjonen bare vedlikeholdes ett sted. */

(function () {
  const ADAPTIV_URL = "https://friluft.avadaptive.no/survey/uteklasserommet"; // Registrering av uteskoleopplegg (Adaptiv 4)

  const NAV = [
    { href: "finn-skole.html",       tekst: "Finn skole" },
    { href: "kartlegg.html",         tekst: "Kartlegg" },
    { href: "laeringsopplegg.html",  tekst: "Læringsopplegg" },
    { href: "sjekkliste.html",       tekst: "Sjekkliste" },
    { href: "veileder.html",         tekst: "Veileder" },
    { href: "planlegg.html",         tekst: "Ressurser" },
  ];

  const aktiv = location.pathname.split("/").pop() || "index.html";

  const logo = `<img class="merke__ikon" src="img/fl-logo.png" alt="Friluftsrådenes Landsforbund">`;

  const navHtml = NAV.map(n =>
    `<a href="${n.href}"${n.href === aktiv ? ' class="aktiv" aria-current="page"' : ""}>${n.tekst}</a>`
  ).join("");

  const header = `
    <a class="hopp" href="#hoved">Hopp til innhold</a>
    <div class="prototype-strip">Prototype – innhold og funksjoner er under utvikling</div>
    <header class="topp">
      <div class="wrap topp__inn">
        <a class="merke" href="index.html">
          ${logo}
          <span>Uteklasserommet</span>
        </a>
        <span class="merke-skille" aria-hidden="true"></span>
        <a class="merke-lif" href="https://www.friluftsrad.no/laring-i-friluft" target="_blank" rel="noopener" aria-label="Læring i friluft">
          <img src="img/lif-logo.svg" alt="Læring i friluft">
        </a>
        <button class="burger" aria-label="Meny" aria-expanded="false">
          <span></span><span></span><span></span>
        </button>
        <nav class="nav" aria-label="Hovedmeny">
          ${navHtml}
          <a class="btn btn--gul nav__cta" href="${ADAPTIV_URL}" target="_blank" rel="noopener">Logg inn / registrer</a>
        </nav>
      </div>
    </header>`;

  const footer = `
    <footer class="bunn">
      <div class="wrap">
        <div class="bunn__grid">
          <div>
            <a class="merke" href="index.html" style="color:#fff">
              <span class="logo-disc">${logo}</span>
              <span style="color:#fff">Uteklasserommet<small style="color:#8fb3a0">Friluftsrådenes Landsforbund</small></span>
            </a>
            <p style="margin-top:1rem;max-width:34ch">Bygg skolens felles uteklasserom. Kartlegg, del og utvikle læringsarenaer i nærmiljøet.</p>
            <div style="margin-top:1.6rem">
              <small style="display:block;color:#8fb3a0;text-transform:uppercase;letter-spacing:.08em;font-size:.72rem;margin-bottom:.55rem">En del av</small>
              <img src="img/lif-logo-hvit.svg" alt="Læring i friluft" style="height:48px;width:auto;display:block">
            </div>
          </div>
          <div>
            <h4>Kom i gang</h4>
            <a href="finn-skole.html">Finn skolen din</a>
            <a href="kartlegg.html">Kartlegg uteklasserom</a>
            <a href="veileder.html">Veileder</a>
          </div>
          <div>
            <h4>Verktøy &amp; ressurser</h4>
            <a href="laeringsopplegg.html">Læringsopplegg</a>
            <a href="sjekkliste.html">Digital sjekkliste</a>
            <a href="planlegg.html">Ressurser og samarbeid</a>
            <a href="https://friluft.avadaptive.no/survey/uteklasserommet" target="_blank" rel="noopener">Registrer i Adaptiv 4</a>
          </div>
        </div>
        <div class="bunn__under">
          <span>© ${new Date().getFullYear()} Friluftsrådenes Landsforbund · Et prosjekt støttet av Sparebankstiftelsen DNB</span>
          <span>Kartdata: Kartverket · Registrering: Adaptiv 4</span>
        </div>
      </div>
    </footer>`;

  const hdr = document.getElementById("site-header");
  const ftr = document.getElementById("site-footer");
  if (hdr) hdr.outerHTML = header;
  if (ftr) ftr.outerHTML = footer;

  // Burger-meny
  const burger = document.querySelector(".burger");
  const nav = document.querySelector(".nav");
  if (burger && nav) {
    burger.addEventListener("click", () => {
      const apen = nav.classList.toggle("apen");
      burger.setAttribute("aria-expanded", String(apen));
    });
  }
})();
