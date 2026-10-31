# LORE walk simulation: Gateway of India to CSMT (simulated walk)

> **SIMULATED DATA.** GNSS, compass, gyro and step signals are synthetic (seeded noise, a 7 deg compass bias, magnetic disturbance zones on busy roads). Narration uses the offline deterministic template path from verified City Pack fact cards. Regenerate with `npm run sim`.

Persona: **local-friend**, seed 42. Route 2.32 km, 31.8 min including stops.

## Metrics

| Metric | Value |
|---|---|
| Narrations | 16 (6.9 per km) |
| Facts spoken | 39 |
| Fact repeat rate | 0.0 % |
| POI repeat rate (proximity triggers) | 0.0 % |
| Share of time speaking | 19 % |
| Quiet-moment compliance (no story starts while crossing/talking) | 100.0 % (0 violations, 228 s of quiet moments) |
| Ongoing speech overlapping a quiet moment (device ducks audio) | 1 s |
| Left/right/ahead/behind accuracy vs ground truth | 94 % |
| Fused heading error | mean 2.8 deg, p95 5.4 deg |
| Silent ticks by reason | speaking: 349, cooldown: 281, nothing-nearby: 1020, crossing-road: 163, user-talking: 81 |

## Transcript

### 00:01 | 0 m | Gateway of India

*proximity, medium tier, ~34 s. Said: **right** + look up (ground truth: right), 33 m away.*

> On your right, that's the Gateway of India. This basalt arch was built to commemorate the landing of King George the Fifth and Queen Mary at Apollo Bunder in December 1911. And here's the fun part: It was designed by the architect George Wittet and completed in 1924. Also, in February 1948, the last British troops to leave independent India marched out through this arch. One more thing: Ferries to the Elephanta Caves, a UNESCO World Heritage Site out in the harbour, leave from the jetties beside it.

Facts: mumbai-gateway-of-india-1, mumbai-gateway-of-india-2, mumbai-gateway-of-india-3, mumbai-gateway-of-india-4. Sources: https://en.wikipedia.org/wiki/Gateway_of_India

### 00:55 | 19 m | Taj Mahal Palace Hotel

*proximity, medium tier, ~32 s. Said: **left** (ground truth: left), 132 m away.*

> Quick one: the Taj Mahal Palace Hotel is on your left. The Taj Mahal Palace opened in 1903. It was commissioned by the industrialist Jamsetji Tata, founder of the Tata Group. And here's the fun part: In November 2008 the hotel was one of the targets of the terrorist attacks on Mumbai. It was restored and reopened. Also, a popular story says Tata built it after being refused entry to a hotel that admitted only Europeans. Historians debate whether this really happened.

Facts: mumbai-taj-mahal-palace-1, mumbai-taj-mahal-palace-3, mumbai-taj-mahal-palace-2. Sources: https://en.wikipedia.org/wiki/Taj_Mahal_Palace_Hotel

### 01:47 | 88 m | Chhatrapati Shivaji Maharaj Statue

*proximity, short tier, ~16 s. Said: **right** (ground truth: right), 20 m away.*

> See Chhatrapati Shivaji Maharaj Statue on your right? This equestrian statue honours Chhatrapati Shivaji Maharaj, the seventeenth-century founder of the Maratha Empire. And here's the fun part: It was unveiled in 1961 and faces the Gateway of India across the square.

Facts: mumbai-shivaji-statue-apollo-bunder-1, mumbai-shivaji-statue-apollo-bunder-2. Sources: https://en.wikipedia.org/wiki/Gateway_of_India

### 05:13 | 355 m | Wellington Fountain

*proximity, short tier, ~19 s. Said: **right** (ground truth: right), 32 m away.*

> Quick one: the Wellington Fountain is on your right. This Victorian fountain at Regal Circle was erected in 1865 in honour of the Duke of Wellington. And here's the fun part: Before he became famous for defeating Napoleon at Waterloo, Wellington had visited Bombay, in 1801 and 1804.

Facts: mumbai-wellington-fountain-1, mumbai-wellington-fountain-2. Sources: https://en.wikipedia.org/wiki/Wellington_Fountain

### 06:34 | 460 m | National Gallery of Modern Art

*proximity, short tier, ~18 s. Said: **left** (ground truth: ahead), 60 m away.*

> On your left, that's the National Gallery of Modern Art. The Mumbai branch of the National Gallery of Modern Art occupies the old Sir Cowasji Jehangir Public Hall. And here's the fun part: It opened as a gallery in 1996 and shows modern and contemporary Indian art.

Facts: mumbai-ngma-mumbai-1, mumbai-ngma-mumbai-2. Sources: https://en.wikipedia.org/wiki/National_Gallery_of_Modern_Art,_Mumbai

### 07:12 | 509 m | Chhatrapati Shivaji Maharaj Vastu Sangrahalaya

*proximity, medium tier, ~39 s. Said: **ahead** (ground truth: ahead), 148 m away.*

> Just ahead, that's Chhatrapati Shivaji Maharaj Vastu Sangrahalaya. Mumbai's main museum was founded as the Prince of Wales Museum. The future King George the Fifth laid its foundation stone in 1905. And here's the fun part: George Wittet, who also designed the Gateway of India, built it in the Indo-Saracenic style, with a dome inspired by Islamic architecture of the Deccan. Also, during the First World War the building was used as a military hospital, and the museum only opened to the public in 1922. One more thing: In 1998 it was renamed after Chhatrapati Shivaji Maharaj, founder of the Maratha Empire.

Facts: mumbai-csmvs-museum-1, mumbai-csmvs-museum-2, mumbai-csmvs-museum-3, mumbai-csmvs-museum-4. Sources: https://en.wikipedia.org/wiki/Chhatrapati_Shivaji_Maharaj_Vastu_Sangrahalaya

### 09:00 | 650 m | Jehangir Art Gallery

*proximity, short tier, ~21 s. Said: **left** (ground truth: left), 56 m away.*

> Quick one: Jehangir Art Gallery is on your left. Jehangir Art Gallery was established in 1952 by Sir Cowasji Jehangir and is one of India's best-known venues for contemporary art. And here's the fun part: It is run by a trust and hosts changing exhibitions by Indian artists in several galleries, free to enter.

Facts: mumbai-jehangir-art-gallery-1, mumbai-jehangir-art-gallery-2. Sources: https://en.wikipedia.org/wiki/Jehangir_Art_Gallery

### 09:41 | 703 m | Kala Ghoda

*proximity, short tier, ~24 s. Said: **ahead** (ground truth: ahead), 84 m away.*

> See Kala Ghoda just ahead? Kala Ghoda means black horse. The name comes from a black statue of King Edward the Seventh, as Prince of Wales, on horseback, which stood here from 1879. And here's the fun part: The original statue was a gift to the city from the businessman Sir Albert Sassoon. Say 'tell me more' if you want the rest.

Facts: mumbai-kala-ghoda-1, mumbai-kala-ghoda-3. Sources: https://en.wikipedia.org/wiki/Kala_Ghoda

### 11:56 | 820 m | Kala Ghoda

*tell-me-more, deep tier, ~22 s. Said: **behind** (ground truth: behind), 29 m away.*

> Okay, more on Kala Ghoda. The royal statue was removed in 1965 and moved to the gardens of the Byculla zoo, Jijamata Udyaan. In 2017 a new statue of a riderless black horse was installed here. And here's the fun part: Every February since 1999, the Kala Ghoda Arts Festival fills these streets with art, music and talks.

Facts: mumbai-kala-ghoda-2, mumbai-kala-ghoda-4. Sources: https://en.wikipedia.org/wiki/Kala_Ghoda

### 12:38 | 875 m | David Sassoon Library

*proximity, short tier, ~20 s. Said: **left** (ground truth: left), 54 m away.*

> See the David Sassoon Library on your left? This Gothic library was built between 1867 and 1870 and named after David Sassoon, a Baghdadi Jewish merchant and philanthropist who helped pay for it. And here's the fun part: Behind the building is a garden reading room where members read under the trees.

Facts: mumbai-david-sassoon-library-1, mumbai-david-sassoon-library-2. Sources: https://en.wikipedia.org/wiki/David_Sassoon_Library

### 16:12 | 1153 m | Flora Fountain and Hutatma Chowk

*proximity, short tier, ~29 s. Said: **ahead** + look up (ground truth: ahead), 89 m away.*

> Quick one: the Flora Fountain and Hutatma Chowk is just ahead. Look up. Flora Fountain was built in 1864 and is crowned by a statue of Flora, the Roman goddess of flowers. And here's the fun part: The square is now called Hutatma Chowk, Martyrs' Square. Its memorial honours the people killed in the Samyukta Maharashtra movement, which led to the creation of Maharashtra state in 1960. Say 'tell me more' if you want the rest.

Facts: mumbai-flora-fountain-hutatma-chowk-1, mumbai-flora-fountain-hutatma-chowk-3. Sources: https://en.wikipedia.org/wiki/Flora_Fountain, https://en.wikipedia.org/wiki/Hutatma_Chowk

### 19:37 | 1419 m | St. Thomas Cathedral

*proximity, short tier, ~19 s. Said: **ahead** (ground truth: ahead), 70 m away.*

> Just ahead, that's St. Thomas Cathedral. St. Thomas Cathedral opened in 1718 and is the oldest Anglican church in Mumbai. And here's the fun part: Churchgate takes its name from it: the gate in the old fort wall that led to this church was called the Church Gate.

Facts: mumbai-st-thomas-cathedral-1, mumbai-st-thomas-cathedral-2. Sources: https://en.wikipedia.org/wiki/St._Thomas_Cathedral,_Mumbai

### 20:49 | 1460 m | Horniman Circle Gardens

*related, medium tier, ~20 s. Said: **ahead** (ground truth: ahead), 163 m away.*

> Since you liked that, here's a related one: Horniman Circle Gardens, just ahead. This circular garden, ringed by uniform arcaded buildings, was laid out in the 1860s as Elphinstone Circle. And here's the fun part: It was renamed after Benjamin Horniman, a British editor of the Bombay Chronicle who supported Indian independence.

Facts: mumbai-horniman-circle-1, mumbai-horniman-circle-2. Sources: https://en.wikipedia.org/wiki/Horniman_Circle_Gardens

### 23:09 | 1643 m | Mumbai Samachar (Red House)

*proximity, short tier, ~17 s. Said: **ahead** (ground truth: ahead), 39 m away.*

> See Mumbai Samachar (Red House) right in front of you? This is the home of the Mumbai Samachar, a Gujarati newspaper founded in 1822 by Fardunjee Marzban. And here's the fun part: It is widely described as the oldest continuously published newspaper in Asia.

Facts: mumbai-mumbai-samachar-1, mumbai-mumbai-samachar-2. Sources: https://en.wikipedia.org/wiki/Mumbai_Samachar

### 30:35 | 2222 m | Chhatrapati Shivaji Maharaj Terminus

*proximity, medium tier, ~39 s. Said: **ahead** + look up (ground truth: ahead), 131 m away.*

> See Chhatrapati Shivaji Maharaj Terminus just ahead? This railway station was designed by Frederick William Stevens and completed in 1888. It was named Victoria Terminus, for Queen Victoria's Golden Jubilee year of 1887. And here's the fun part: It became a UNESCO World Heritage Site in 2004 as an outstanding blend of Victorian Gothic Revival architecture with traditional Indian features. Look up. Look up at the central dome: it is crowned by a statue of a woman representing Progress. One more thing: India's first passenger train ran from Bori Bunder, right here, to Thane on the 16th of April, 1853.

Facts: mumbai-csmt-1, mumbai-csmt-2, mumbai-csmt-3, mumbai-csmt-4. Sources: https://en.wikipedia.org/wiki/Chhatrapati_Shivaji_Maharaj_Terminus, https://whc.unesco.org/en/list/945

### 31:40 | 2306 m | BMC Headquarters

*proximity, short tier, ~16 s. Said: **left** + look up (ground truth: left), 114 m away.*

> Quick one: the BMC Headquarters is on your left. The headquarters of the Brihanmumbai Municipal Corporation, the city government, was completed in 1893. Look up. Like the station opposite, it was designed by Frederick William Stevens, mixing Gothic with Indo-Saracenic elements.

Facts: mumbai-bmc-headquarters-1, mumbai-bmc-headquarters-2. Sources: https://en.wikipedia.org/wiki/Municipal_Corporation_Building,_Mumbai
