# Celestial Knowledge Base — Source Intake 005

Назначение: научное ядро астрономических расчётов для Future Lab с отдельным, строго изолированным слоем исторических/астрологических интерпретаций.

## 1. Научный слой

### JPL Horizons
Официальная система JPL для построения точных эфемерид объектов Солнечной системы. Используется для вычисления положения, движения и наблюдаемости объектов во времени.

Reference: https://ssd.jpl.nasa.gov/horizons/manual.html

Ключевые возможности для Future Lab:
- координаты и скорости;
- RA/Dec;
- azimuth/elevation;
- угловые скорости;
- observer-centric geometry;
- major bodies, asteroids, comets, satellites, spacecraft;
- reference frames;
- long-term ephemerides based on DE441.

### NASA NAIF SPICE
Профессиональный toolkit для геометрии космических миссий и работы с ephemeris kernels.

Reference: https://naif.jpl.nasa.gov/naif/toolkit.html

Future Lab usage:
- SPK ephemerides;
- reference frames;
- transformations;
- observer/target geometry;
- reproducible local calculations;
- mission-grade geometry tooling.

### Swiss Ephemeris
Высокоточная ephemeris library, используемая многими астрологическими приложениями. По официальной документации с мая 2026 опирается на JPL DE441.

Reference: https://www.astro.com/swisseph/swephinfo_e.htm

Future Lab usage:
- compatibility layer for traditional astrology calculations;
- local ephemeris engine;
- comparison with JPL/DE441 calculations.

## 2. Scientific data model

```text
CELESTIAL_OBJECT
├── object_id
├── name
├── object_type
├── parent_body
├── source_catalog
└── physical_metadata

EPHEMERIS_SAMPLE
├── object_id
├── epoch
├── time_scale
├── reference_frame
├── observer
├── position
├── velocity
├── distance
├── ra_dec
├── az_el
├── uncertainty
└── source/version

CELESTIAL_EVENT
├── event_type
├── objects[]
├── start_time
├── peak_time
├── end_time
├── observer/location
├── geometry
└── source/version
```

## 3. Core scientific topics

- Time systems: UTC, UT1, TT, TDB, Julian Date
- Reference frames: ICRF, ecliptic, equatorial, Earth-fixed
- Orbital elements
- State vectors
- Precession / nutation
- Earth orientation parameters
- Topocentric vs geocentric coordinates
- Solar/Lunar phases
- Rise / set / transit
- Conjunction / opposition / angular separation
- Retrograde apparent motion
- Eclipses
- Occultations
- Asteroids / comets
- Barycenters / Lagrange points
- Uncertainty of ephemerides

## 4. Cultural / astrology layer

This layer is explicitly NON_SCIENTIFIC as a predictive evidence class.

It may consume the same scientific ephemeris engine, but must never change the scientific status of the interpretation.

Planned systems:
- Western tropical astrology
- Sidereal astrology / Jyotish
- Hellenistic
- Medieval / Renaissance
- Chinese astrology
- Natal
- Transit
- Synastry
- Horary
- Electional
- Mundane astrology

## 5. Architectural separation

```text
JPL / SPICE / Swiss Ephemeris
        ↓
CELESTIAL ENGINE
        ↓
NORMALIZED EPHEMERIS
        ↓
┌─────────────────────┬──────────────────────┐
│ SCIENTIFIC ANALYSIS │ CULTURAL INTERPRET. │
│ SCIENTIFIC_A        │ NON_SCIENTIFIC      │
└─────────────────────┴──────────────────────┘
```

## 6. Qualification

Scientific calculations:
- authoritative source/version;
- reproducible parameters;
- reference frame/time scale;
- numeric validation against reference ephemeris;
- tolerance;
- tests.

Astrological rule systems:
- historically documented rule source;
- deterministic/reproducible implementation;
- blind/backtest where a predictive claim exists;
- evidence class always kept separate from astronomy.
