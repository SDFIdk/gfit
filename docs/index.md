# Geoide-fit med krydsvalidering

Formålet med dette projekt er, at automatisere nedenstående fremgangsmåde: En gravimetrisk opmålt geoide tilpasses geoide-højden målt i et antal punkter forskellige steder i landet. For hvert punkt bliver lavet en geoide-tilpasning uden dette punkt. Efterfølgende bliver en interpoleret værdi i det udeladte punkts lokation sammenlignet med punktets målte geoide-højde.

**Resultatet er filen med de oprindelige målepunkter beriget med en kolonne ekstra, der indeholder den interpolerede geoide-højde.**

Ved sammenligning med det enkelte punkts egen måling og den interpolerede værdi afgør vi, om punktet kan bruges til det endelige geoide-fit, eller om det bør kasseres som en outlier.

---

Disse sider indeholder følgende:

*   Beskrivelser af de anvendte FORTRAN-programmer `fitgeoid1`, `gbin` og `geoid`.
*   Vejledning i installation og kørsel af automatiseringsprogrammerne `gfit-cv`, `gfit-check`, `gfit-gather` og `gfit-clean`.
*   Beskrivelse af data-materialet, som blev anvendt til udviklingen af denne pakke. Disse er dog ikke en forudsætning for at bruge programmet.
