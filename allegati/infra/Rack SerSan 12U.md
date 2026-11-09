# Rack SerSan 12UVEVOR 4 montanti · profondità 584–1016 mm · Cagliari, ufficio · aggiornato al 5 nov 2026

[x] Rete [x] Corrente [x] Mostra il futuro

## Cosa hai davanti

1. #### Oggi: monti il DL380 adesso
   - Guide nel rack, profondità regolata sul DL380 (\~700 mm) più 10–15 cm dietro per i cavi.
   - Per ora presa a muro e router TIM: Proxmox e iLO prendono un IP 192.168.1.x.
   - BIOS: Automatic Power-On su Restore Last Power State; Power Button Mode su Disabled.
   - Proxmox con vmbr0 "VLAN aware". Niente cluster, niente lavori lunghi senza UPS.
2. #### Arrivano cavi e rete zincata in carrello
   - 2× C13–C14 da 0,5 m (DL380) e 2× da 1,8 m (Sophos, ciabatta).
   - Rete zincata 1 × 5 m: due strisce da 40 cm per chiudere il davanti.
3. #### Arriva il Sophos 9–13 nov
   - Prima accendilo com'è: controlla avvio, BIOS, RAM e SSD.
   - Poi metti i tuoi 2× 8 GB; i 2× 4 GB vanno da parte per il PBS.
   - Proxmox, VM OPNsense, LXC NetBird e AdGuard. Montalo girato in U8.
4. #### Arriva l'UPS in spedizione
   - Carica 8 ore, poi test di autonomia con il DL380 acceso.
   - Collega: P1 Sophos, P2 ciabatta, G1 DL380 ×2. USB al Sophos per NUT.
   - Imposta lo spegnimento a livelli: server giù dopo 3 minuti, rete accesa fino a fine batteria.
5. #### Giorno del cambio
   - ONT → Sophos E0: PPPoE su VLAN 835 (con le credenziali del provider).
   - Router TIM come access point su E4: DHCP spento, IP 10.10.99.2.
   - DL380 su E1 (trunk) ed E2 (iLO), nuovi IP 10.10.x.x. Tieni il router TIM pronto per tornare indietro.
6. #### Più avanti quando c'è budget
   - i5-6500T (29,90 €) e pasta termica.
   - PBS: case e dischi.
   - Nodo 2 (max 1.500 €), sdoppiatore a Y, moduli SFP RJ45 o NIP-51081.

| Bargain | 1.256,04 € |
| --- | --- |
| eBay (server, rack, controller RAID, cavi di rete) | 909,92 € |
| IVA d'importazione + costi UPS (stima) | \~290,00 € |
| Sophos SG 230 Rev.2 | 217,80 € |
| UPS HPE R1500 G5 | 255,10 € |
| Cavi C13–C14 (carrello) | \~20,70 € |
| Rete zincata | 25,90 € |
| Totale | \~2.975,46 € |
| Budget | 3.200,00 € |
| Rimane | \~224,54 € |

L'IVA d'importazione è una stima: con la cifra della ricevuta il totale diventa esatto.

## Multi-sito: Cagliari · Oracle · Terra Noa

### Due zone, non un cluster unico

Il cluster Proxmox (corosync) vuole una rete con pochi millisecondi di latenza e senza interruzioni. Starlink ha 25–60 ms, sbalzi e brevi cadute: un cluster stirato tra Cagliari e Terra Noa perderebbe il quorum spesso, e con l'HA attiva i nodi si riavvierebbero da soli.

Il multi-zona si fa così:

- **Una zona per sito:** cluster "cagliari" in ufficio; a Terra Noa un nodo singolo, che diventa un cluster suo quando ci saranno due macchine.
- **Proxmox Datacenter Manager** sul Sophos le vede e gestisce tutte da un'interfaccia, e sposta le VM da una zona all'altra.
- **PBS** sincronizza ogni notte i backup da Cagliari a Terra Noa: se l'ufficio ha un problema, ripristini lì.
- **NetBird** collega tutto in una rete privata, anche dietro il CGNAT di Starlink.

### Primo nodo di Terra Noa entro marzo 2027

**Lenovo ThinkCentre M920q** con i5-8500T (6 core), riser PCIe e scheda Intel i350-T4 a 4 porte. Usa RAM **DDR4 SO-DIMM**: 2 slot, quindi ci vanno due dei tuoi banchi da 4 GB (8 GB). Consuma 10–15 W a riposo, adatto al solare.

| onboard | MGMT locale (VLAN 10) |
| --- | --- |
| i350 p1 | WAN Starlink |
| i350 p2 | trunk verso switch / AP di campo |
| i350 p3 | VLAN IoT: sensori e irrigazione |
| i350 p4 | VLAN video: telecamere, o WAN 2 4G |

| M920q i5-8500T usato (8 GB, 256 GB NVMe) | \~230 € |
| --- | --- |
| Riser PCIe 01AJ940 | \~18–27 € |
| Intel i350-T4 basso profilo | \~40 € |
| Totale stimato, spedizioni escluse | \~290–300 € |

Se arriva con 8 GB in un solo banco, quel banco lo tieni come scorta o lo rivendi. Da evitare i mini PC con N100/N150: usano DDR5, e le tue SO-DIMM DDR4 non entrano. Alternativa più economica e senza ventola: mini PC N5105 con 4 porte 2,5G (DDR4 SO-DIMM), ma con 4 core lenti.

## Mini rack Terra Noa

| M920q #1 onboard | MGMT locale · VLAN 10 (10.20.10.0/24) |
| --- | --- |
| i350 p1 | ← Starlink · WAN 1 |
| i350 p2 | → switch · trunk VLAN (AP, gateway LoRa, ponti radio, M920q #2) |
| i350 p3 | ← router 4G · WAN 2 di riserva (quando lo prendi) |
| i350 p4 | libera |

Lo switch è l'Omada SG2008P perché entra in un 10"; il TL-SG2210MP è largo 29 cm e non ci sta.

## Simulatore blackout

Minuti senza corrente: 0 Spegnimento server dopo: 3 min Stato batterie [ ] Nodo 2 installato [ ] PBS acceso (backup in corso)

Autonomia dalla tabella HPE per R1500 G5 (109 W → 97 min, 328 W → 23 min, 547 W → 12 min, 1094 W → 5 min), interpolata. Sotto i 109 W è una stima, limitata a 5 ore. I consumi dei dispositivi sono stime.

## Collegamenti

| Tipo | Da | A | Cosa passa | Stato |
| --- | --- | --- | --- | --- |

Stato: in casa in arrivo da comprare futuro da verificare · Nessun router 4G per ora. Il Wi-Fi lo fa il router TIM come access point.