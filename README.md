# Uteklasserommet.no

Prototype av nettsiden for prosjektet **Uteklasserommet** – Friluftsrådenes Landsforbund, støttet av Sparebankstiftelsen DNB.

> **Hovedidé:** Bygg skolens felles uteklasserom. Alle lærere ved skolen jobber i samme kart over nærmiljøet, og henter inspirasjon fra skoler i hele landet. Uteklasserommet.no viser *hvor* læring i friluft kan skje.

## Hva dette er

En **statisk, klikkbar prototype** av nettsiden, holdt bevisst slank (less is more). Selve kartleggingen (registrering av uteskoleopplegg) og kartdataene ligger i **Adaptiv 4**, og nettsiden er koblet til den ekte løsningen:

- Registreringsknapp → `https://friluft.avadaptive.no/survey/uteklasserommet`
- Embedet kart (forside + «Finn skole») → `https://friluft.avadaptive.no/map/.embed/uteklasserommet`. Nye registreringer dukker opp automatisk.

Nettsiden er en *inngangsport*: presentere idéen, embede kartet, og senke terskelen for å komme i gang. Funksjoner som hører hjemme i Adaptiv (egne undervisningskart, fysisk plakat, admin/statistikk) er bevisst utelatt.

## Teknologi

- Ren HTML/CSS/JS – ingen byggesteg, ingen avhengigheter
- Kartet er en `<iframe>`-embed fra Adaptiv 4
- Delt header/footer injiseres via `js/site.js` (vedlikeholdes ett sted)
- Lokale CSS/JS har `?v=N` for cache-busting – øk tallet ved endringer

## Sider (6)

| Fil | Meny | Innhold |
|-----|------|---------|
| `index.html` | (forside) | Hovedbudskap, innganger, embedet kart |
| `finn-skole.html` | Finn skole | Embedet Adaptiv-kart – søk skole / utforsk hele landet |
| `kartlegg.html` | Kartlegg | 4 steg + registreringsknapp + «Slik blir skolen med» |
| `laeringsopplegg.html` | Opplegg | Filtrerbar katalog over 629 læringsopplegg fra Læringsportalen |
| `sjekkliste.html` | Sjekkliste | Digital sjekkliste (taksonomi fra feltspesifikasjonen) |
| `veileder.html` | Veileder | Veileder for lærere/skoler, inkl. elevmedvirkning |
| `planlegg.html` | Ressurser | Eksterne ressurser + samarbeidspartnere |

## Datamodell / kilder

Innholdet bygger på prosjektets kildefiler:
- `Uteklasserommet_survey_feltspesifikasjon.xlsx` (25 felt, 7 seksjoner, verdilister → sjekklistas taksonomi)
- `Uteklasserommet_datamodell.geojson`
- Tegnforklaring (forside + Finn skole), to grupper:
  - **Natur- og landskapstyper** (fargekodet): 🔵 Vann og våtområde · 🟢 Skog · 🟡 Åpent/dyrka mark · ⚫ Fjell · ⚪ Bebygd · 🟣 Annet
  - **Type sted** (uten farge, m/ikon): ⛺ Tilrettelagt friluftsområde · 🍄 Høstingsplass · 🏛️ Kulturminne · 🏠 Bygning · 🏭 Næringsliv
  - (Selve punktfargene/kategoriene på det embedede kartet styres av Adaptiv.)

## Læringsopplegg-katalog

`data/laeringsopplegg.json` (629 opplegg) hentes fra **Friluftsrådenes læringsportal** sitt API (`friluftsrad.no/api/learningactivity/all` + detalj per opplegg). Hvert opplegg er beriket med trinn, fag, **årstid**, **sted** og **arena** (utledet fra sted-teksten), samt en søkeblob som også dekker kompetansemål. Filtre i katalogen: trinn · fag · årstid · **arena** (🌲 Skog, 💧 Vann/fjære/sjø, 🔥 Bålplass/leir, 🏫 Skolegård/nærmiljø, 🌾 Åpent område, 📍 Passer hvor som helst) · fritekstsøk. **Sortering:** Anbefalt · A–Å · «Overrask meg» (tilfeldig, med «Trekk på nytt»). På mobil er filtrene samlet bak en sammenleggbar «Filtre & søk»-knapp. Kortene **lenker til** det fulle opplegget på friluftsrad.no (innholdet speiles ikke).

**Oppdatere katalogen** (henter nye opplegg på nytt, ~1–2 min):
```bash
python verktoy/hent_laeringsopplegg.py
```

## Kjøre lokalt

Åpne `index.html` i en nettleser med nettilgang (kartet og fontene lastes eksternt).

## Sette i drift (GitHub + Vercel)

Repoet (denne `nettside/`-mappen) er ferdig initialisert med git og en første commit.

**1. Opprett GitHub-repo og push:**

Opprett et tomt repo på [github.com/new](https://github.com/new) (f.eks. `uteklasserommet`, uten README/.gitignore), og kjør så fra denne mappen:

```bash
git remote add origin https://github.com/<bruker>/uteklasserommet.git
git push -u origin main
```

**2. Importer i Vercel:**

- Logg inn på [vercel.com](https://vercel.com) → **Add New → Project** → importer GitHub-repoet.
- **Framework Preset:** Other · **Build Command:** (tom) · **Output Directory:** (tom/`.`) — det er en ren statisk side uten byggesteg.
- Deploy. Du får en `*.vercel.app`-adresse umiddelbart.

**3. Koble domenet:**

- I Vercel: **Settings → Domains** → legg til `uteklasserommet.no` og følg DNS-instruksjonene hos domeneleverandøren.

`vercel.json` setter sikkerhets-headere og lang cache på `/img`. `404.html` brukes automatisk som feilside.

## Å gjøre før produksjon

- [x] Koble registreringsknapp til Adaptiv 4-survey
- [x] Embede det ekte Adaptiv-kartet (forside + «Finn skole»)
- [x] Slanke strukturen til 6 sider (fjernet Mine kart, Andre skoler, Fysisk kart, For friluftsråd; foldet inn Elevmedvirkning + Samarbeidspartnere)
- [x] Offisiell FL-logo lagt inn (`img/fl-logo.png`, header + footer)
- [ ] Ekte bilder (skolebarn ute) – største visuelle løft
- [ ] 2–3 konkrete eksempel-opplegg (sted + bilde + hva klassen gjorde)
- [ ] Kort FAQ (hvem kan delta, hva koster det, utstyr)
- [ ] Sette riktig kontakt-e-post i «Bli med» (nå `post@friluftsrad.no`)
