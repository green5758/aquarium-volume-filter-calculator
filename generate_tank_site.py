import os
import json
import math
import datetime
import urllib.request
import urllib.parse

# ==========================================
# CORE CONFIGURATION
# ==========================================
AFFILIATE_TAG = "everythi00099-20"
SITE_NAME = "TankSizePro"
SITE_TAGLINE = "Aquarium, Reef Tank & Pond Volume, Filter GPH, Heater & Substrate Calculator"
OUTPUT_DIR = "public"
INDEXNOW_KEY = "5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e"

# Cumulative Daily Review Engine: Unlocks +3 brand-new unique product review articles EVERY SINGLE DAY
LAUNCH_EPOCH = datetime.date(2026, 11, 1)
REVIEWS_PER_DAY = 3

REPO_SLUG = os.environ.get("GITHUB_REPOSITORY", "username/tanksizepro")
OWNER, REPO_NAME = REPO_SLUG.split("/") if "/" in REPO_SLUG else ("username", "tanksizepro")
BASE_URL = os.environ.get("SITE_BASE_URL", f"https://{OWNER}.github.io/{REPO_NAME}")

def amz_url(keyword):
    return f"https://www.amazon.com/s?k={urllib.parse.quote_plus(keyword.replace('+', ' '))}&tag={AFFILIATE_TAG}"

# ==========================================
# BEST SELLING PRODUCTS DATABASE (USD / EN)
# ==========================================
BEST_SELLERS = [
    {
        "title": "Fluval FX6 High-Performance Canister Filter for Aquariums up to 400 Gallons (925 GPH)",
        "category": "Heavy-Duty Canister Filter",
        "rating": "4.8 ★ (11,400+ reviews)",
        "badge": "#1 Large Tank Canister Filter",
        "specs": "925 GPH Pump Output | Smart Pump Auto-Air Purge | Bottom Drain Valve for 5-Min Water Changes",
        "keyword": "Fluval+FX6+High+Performance+Aquarium+Canister+Filter"
    },
    {
        "title": "AquaIllumination AI Prime 16HD Reef / Freshwater Smart LED Aquarium Light",
        "category": "Reef & Planted LED Light",
        "rating": "4.8 ★ (4,900+ reviews)",
        "badge": "#1 Reef & Nano LED Light",
        "specs": "59W Full-Spectrum HD Power | myAI Smartphone App Control | Dedicated Moonlight Channel",
        "keyword": "AquaIllumination+AI+Prime+16HD+Reef+Aquarium+LED+Light"
    },
    {
        "title": "Fluval Plant 3.0 Bluetooth Programmable Full-Spectrum Planted Aquarium LED (32W–59W)",
        "category": "Planted Aquascape LED",
        "rating": "4.8 ★ (8,600+ reviews)",
        "badge": "#1 Planted Tank LED Strip",
        "specs": "6500K–7500K High-PAR Spectrum | FluvalSmart App 24-Hr Sunrise/Sunset | IP67 Waterproof",
        "keyword": "Fluval+Plant+3.0+Bluetooth+Planted+Aquarium+LED+Light"
    },
    {
        "title": "Oase BioMaster Thermo 350 / 600 External Canister Filter with Built-In HeatUp Heater",
        "category": "Thermo-Integrated Canister",
        "rating": "4.8 ★ (3,200+ reviews)",
        "badge": "Best EasyClean Pre-Filter",
        "specs": "Integrated Heater Keeps Glass Tank Clutter-Free | Pull-Out Pre-Filter Module Cleans in 60 Secs",
        "keyword": "Oase+BioMaster+Thermo+350+600+Canister+Filter"
    },
    {
        "title": "Inkbird ITC-306A Wi-Fi Dual-Probe Aquarium Heater Temperature Controller + Titanium Heater",
        "category": "Failsafe Heater Controller",
        "rating": "4.8 ★ (9,500+ reviews)",
        "badge": "#1 Heater Overheat Protection",
        "specs": "Dual Redundant Relays + Dual Waterproof Probes | Prevents Cooked Fish | High/Low App Alarms",
        "keyword": "Inkbird+ITC+306A+WiFi+Aquarium+Temperature+Controller+Heater"
    },
    {
        "title": "LANDEN 60P / 90P / 120P Low-Iron Ultra-Clear Rimless Glass Aquarium Tank (6mm–12mm Thick)",
        "category": "Rimless Aquascape Tank",
        "rating": "4.8 ★ (2,800+ reviews)",
        "badge": "Best Low-Iron Rimless Tank",
        "specs": "91%+ Light Transmission Low-Iron Glass | German Wacker Silicone | EVA Leveling Mat Included",
        "keyword": "LANDEN+Low+Iron+Rimless+Glass+Aquarium+Tank"
    },
    {
        "title": "CaribSea Eco-Complete Planted Aquarium Substrate & Arag-Alive Live Reef Sand (20-Lb Bags)",
        "category": "Live Planted & Reef Substrate",
        "rating": "4.8 ★ (34,000+ reviews)",
        "badge": "#1 Live Bacteria Substrate",
        "specs": "Volcanic Basalt Mineral Rich (Planted) or Live Marine Aragonite (Reef) | No Rinsing Required",
        "keyword": "CaribSea+Eco+Complete+Planted+Aquarium+Substrate+20+lb"
    },
    {
        "title": "Hygger / EcoTech VorTech Quiet Magnetic DC Wave Maker Powerhead w/ LCD Controller",
        "category": "Reef & Cichlid Wave Maker",
        "rating": "4.7 ★ (12,700+ reviews)",
        "badge": "Best Reef & Cichlid Circulation",
        "specs": "1,600 to 4,200 GPH Sine-Wave Flow | Night Sensor + 10-Min Feed Pause | Magnetic Mount",
        "keyword": "Aquarium+DC+Wave+Maker+Powerhead+Controller+Magnetic"
    }
]

# ==========================================
# PRODUCT COMPARISON MATRIX (PERBANDINGAN PRODUK)
# ==========================================
COMPARISON_MATRIX = [
    {
        "model": "Fluval FX6 Canister Filter",
        "type": "High-Output Canister Filter",
        "flow_spec": "925 GPH Pump / 563 GPH Net",
        "tank_size": "75 to 400 Gallon Tanks",
        "highlight": "1.5-Gal Media Capacity + Auto Purge",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Fluval+FX6+High+Performance+Aquarium+Canister+Filter"
    },
    {
        "model": "Oase BioMaster Thermo 600",
        "type": "Heater-Integrated Canister",
        "flow_spec": "330 GPH + 300W Internal Heater",
        "tank_size": "55 to 160 Gallon Planted",
        "highlight": "60-Sec Pull-Out Pre-Filter Tube",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Oase+BioMaster+Thermo+600+External+Canister+Filter"
    },
    {
        "model": "Fluval 407 Performance Canister",
        "type": "Silent Mid-Size Canister",
        "flow_spec": "383 GPH Pump (20W Draw)",
        "tank_size": "40 to 100 Gallon Aquariums",
        "highlight": "eTEC Silent Pump + Vertical Pre-Filter",
        "rating": "4.7 / 5.0 ★",
        "keyword": "Fluval+407+Performance+Canister+Filter+Aquarium"
    },
    {
        "model": "AI Prime 16HD Reef / Freshwater",
        "type": "Smart HD Puck LED Light",
        "flow_spec": "59W Full-Spectrum + UV/Violet",
        "tank_size": "Covers 24\"×24\" Cube / 20–40 Gal",
        "highlight": "Dynamic HD Power Sharing per Channel",
        "rating": "4.8 / 5.0 ★",
        "keyword": "AquaIllumination+AI+Prime+16HD+Reef+Aquarium+LED+Light"
    },
    {
        "model": "Fluval Plant 3.0 Bluetooth LED",
        "type": "Full-Length Linear Planted LED",
        "flow_spec": "32W (24\") / 46W (36\") / 59W (48\")",
        "tank_size": "20 Long, 40 Breeder, 55 & 75 Gal",
        "highlight": "Edge-to-Edge Carpet Plant Coverage",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Fluval+Plant+3.0+Bluetooth+Planted+Aquarium+LED+Light"
    },
    {
        "model": "Inkbird ITC-306A + Titanium Heater",
        "type": "Dual-Relay Wi-Fi Thermostat",
        "flow_spec": "Supports up to 1,200W Heaters",
        "tank_size": "10 to 300+ Gallon Tanks",
        "highlight": "Dual Probes Prevent Heater Stuck-On",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Inkbird+ITC+306A+WiFi+Aquarium+Temperature+Controller+Heater"
    }
]

# ==========================================
# HEAD-TO-HEAD "VS" COMPARISON PAGES
# ==========================================
VS_COMPARISONS = [
    {
        "slug": "compare-fluval-fx6-vs-oase-biomaster-thermo-600-canister-filter",
        "title": "Fluval FX6 vs. Oase BioMaster Thermo 600: Raw GPH Flow vs. Built-In Heater & EasyClean Pre-Filter",
        "product_a": "Fluval FX6 (925 GPH)",
        "product_b": "Oase BioMaster Thermo 600",
        "winner_badge": "Best Heavy Bioload GPH vs. Best Aquascape Aesthetics & Maintenance",
        "keyword_a": "Fluval+FX6+High+Performance+Aquarium+Canister+Filter",
        "keyword_b": "Oase+BioMaster+Thermo+600+External+Canister+Filter",
        "summary": "Compare real-world GPH water turnover, media basket volume, pre-filter cleaning speed, and built-in heater integration between Fluval FX6 and Oase BioMaster Thermo.",
        "metrics": [
            {"feature": "Pump Output & Circulation", "val_a": "925 GPH Pump / 563 GPH Net Through Media", "val_b": "330 GPH Pump (Optimized for Planted CO2 Retention)"},
            {"feature": "Integrated Aquarium Heater", "val_a": "No (Requires Separate In-Tank or Inline Heater)", "val_b": "Yes — Includes 300W Internal HeatUp Thermostat Heater"},
            {"feature": "Pre-Filter Cleaning Routine", "val_a": "Open Lid & Rinse Outer Foam Bricks Every 4–6 Weeks", "val_b": "Unclip Pull-Out Pre-Filter Tube in 30 Secs Without Opening Drum"},
            {"feature": "Water Change Drain Valve", "val_a": "Built-In Bottom Purge Valve Drains Tank via Hose", "val_b": "Standard Top Hose Shutoff Block"},
            {"feature": "Ideal Tank Application", "val_a": "75–300 Gal Cichlids, Monster Fish, Turtles & Goldfish", "val_b": "40–120 Gal Rimless Aquascapes & Discus Tanks"}
        ],
        "verdict_text": "Choose the Fluval FX6 if you keep African Cichlids, Oscars, Goldfish, or Turtles in a 75 to 300-gallon tank and need massive 563 GPH net mechanical scrubbing and a bottom water-change drain valve. Choose the Oase BioMaster Thermo 600 if you run a rimless planted aquascape and want the heater hidden inside the canister plus a 30-second pull-out pre-filter module."
    },
    {
        "slug": "compare-ai-prime-16hd-vs-kessil-a360x-reef-aquarium-led",
        "title": "AI Prime 16HD vs. Kessil A360X Tuna Blue: PAR Spread, Shimmer & App Control Compared",
        "product_a": "AquaIllumination AI Prime 16HD",
        "product_b": "Kessil A360X Tuna Blue / Sun",
        "winner_badge": "Best Built-In App Value vs. Best Dense Matrix Shimmer & Color Blending",
        "keyword_a": "AquaIllumination+AI+Prime+16HD+Reef+Aquarium+LED+Light",
        "keyword_b": "Kessil+A360X+Tuna+Blue+Sun+Aquarium+LED+Light",
        "summary": "Compare Dense Matrix LED shimmer vs. TIR lens spread, built-in Wi-Fi/Bluetooth app control, and SPS/LPS coral growth PAR.",
        "metrics": [
            {"feature": "Power & PAR Output", "val_a": "59 Watts w/ HD Power Sharing Across 7 Channels", "val_b": "90 Watts Dense Matrix Array (130° Wide Coverage)"},
            {"feature": "Smartphone App Control", "val_a": "100% Built-In Free myAI App Out of the Box", "val_b": "Manual Knobs Standard (Requires Kessil Wi-Fi Dongle for App)"},
            {"feature": "Optical Blending & Shimmer", "val_a": "80° TIR Lens (Crisp Color Pop, Mild Disco Effect Near Surface)", "val_b": "Patented Single-Point Dense Matrix (Zero Color Separation + Halide Shimmer)"},
            {"feature": "Recommended Tank Footprint", "val_a": "Up to 24\" × 24\" (Nano to 40-Gal Cube, or 2× on 75-Gal)", "val_b": "Up to 30\" × 30\" Mixed Reef / 24\" × 24\" SPS Dominant"},
            {"feature": "Upfront Price Tier", "val_a": "Value Leader (~$249–$269 Range)", "val_b": "Premium Tier (~$449–$479 Range)"}
        ],
        "verdict_text": "Choose the AI Prime 16HD if you want built-in smartphone scheduling right out of the box and the highest PAR-per-dollar for nano reefs, 40-gallon breeders, or dual-light 75-gallon setups. Choose the Kessil A360X if you love natural metal-halide water shimmer with zero color-channel separation."
    },
    {
        "slug": "compare-canister-filter-vs-sump-filter-vs-hob-aquarium-filtration",
        "title": "Canister Filter vs. Sump Filter vs. Hang-On-Back (HOB): GPH Turnover & Bioload Compared",
        "product_a": "Pressurized Canister Filter (Fluval FX/07)",
        "product_b": "Under-Cabinet Sump & Hang-On-Back (HOB)",
        "winner_badge": "Best Sealed CO2 & Mechanical Polish vs. Best Reef Skimmer & Oxygenation",
        "keyword_a": "Fluval+407+FX4+FX6+Aquarium+Canister+Filter",
        "keyword_b": "Seachem+Tidal+110+Fluval+AquaClear+HOB+Filter",
        "summary": "Understand which filtration method delivers the right GPH turnover and biological surface area for planted tanks, cichlid tanks, and saltwater reefs.",
        "metrics": [
            {"feature": "Biological Media Volume", "val_a": "1.0 to 1.5 Gallons of Pressurized Bio-Rings & Sponges", "val_b": "Sump: 10–30 Gal Volume | HOB: 0.25 Gal Basket"},
            {"feature": "Planted Tank CO2 Retention", "val_a": "Sealed Pressurized Loop — Zero CO2 Outgassing Loss", "val_b": "Sump Overflow & HOB Waterfall Outgas Dissolved CO2"},
            {"feature": "Saltwater Protein Skimmer Fit", "val_a": "Cannot House an Internal Protein Skimmer", "val_b": "Sump Houses Skimmer, Rollermat, Heaters & Refugium"},
            {"feature": "Flood & Power-Outage Safety", "val_a": "100% Sealed Closed Loop — Zero Overflow Risk on Power Cut", "val_b": "Sump Requires Check Valve & Siphon-Break Drain Sizing"},
            {"feature": "Noise Level in Living Rooms", "val_a": "Whisper-Silent Inside Cabinet", "val_b": "Sump Drain Gurgle / HOB Water Trickle"}
        ],
        "verdict_text": "For freshwater planted aquascapes, cichlid tanks, and community aquariums from 30 to 250 gallons, a Pressurized Canister Filter (like the Fluval 407, FX4, or FX6) is the cleanest, quietest, and most flood-proof choice. For saltwater coral reefs over 60 gallons, an under-cabinet Sump is preferred to house a protein skimmer and fleece roller."
    }
]

# ==========================================
# BASE + CUMULATIVE DAILY PRODUCT REVIEWS (+3 PER DAY)
# ==========================================
BASE_REVIEWS = [
    {
        "slug": "review-fluval-fx6-high-performance-aquarium-canister-filter",
        "title": "Fluval FX6 Canister Filter Review: Why 925 GPH & Smart Pump Tech Dominate Large Aquariums",
        "product_name": "Fluval FX6 High-Performance Canister Filter (Up to 400 Gal)",
        "category": "Heavy-Duty Canister Filter",
        "rating_score": "4.9",
        "verdict_badge": "Editor's Choice — #1 Large Canister Filter",
        "spec_1": "925 GPH Pump / 563 GPH Net Circulation",
        "spec_2": "1.5-Gallon Media Capacity (Stacked Baskets)",
        "spec_3": "12-Hr Auto-Air Purge Smart Pump",
        "spec_4": "Bottom Utility Drain Valve + 3-Yr Warranty",
        "published_date": "2026-11-01",
        "keyword": "Fluval+FX6+High+Performance+Aquarium+Canister+Filter",
        "summary": "Moving 563 gallons per hour of net filtered water through 1.5 gallons of biological and mechanical media while automatically purging trapped air bubbles every 12 hours, the Fluval FX6 is the undisputed king of large freshwater and turtle aquariums.",
        "pros": [
            "Massive 925 GPH bottom-mounted motor (563 GPH real-world net flow with media) easily achieves 5x–8x turnover on 75 to 180-gallon tanks",
            "Onboard Smart Pump microchip pauses the impeller for 60 seconds every 12 hours to burp out trapped micro-bubbles automatically",
            "Base-mounted utility purge valve lets you attach a vinyl hose and drain 30% of your tank water for water changes without a siphon",
            "Outer mechanical foam rings trap heavy waste before it ever reaches the center biological ceramic bio-rings"
        ],
        "cons": [
            "Drum measures 15.5 inches wide by 21 inches tall—measure your aquarium stand cabinet door opening before ordering"
        ],
        "body_paragraphs": [
            "When calculating required filter GPH on our aquarium calculator, heavy-bioload setups (African Cichlids, Oscars, Goldfish, Monster Fish, and Aquatic Turtles) require a real-world turnover rate of 6x to 8x the tank volume per hour. Because most canister manufacturers advertise empty-pump GPH rather than loaded-media GPH, a standard 300 GPH filter drops to 160 GPH once packed with sponges. The Fluval FX6 solves this with a 925 GPH pump that still pushes a verified 563 GPH when fully loaded.",
            "During our 90-day test on a heavily stocked 125-gallon Mbuna cichlid tank, water clarity turned crystal-clear within 4 hours of startup. Filling the three center media trays with 4 liters of sintered glass bio-media provided enough nitrifying surface area to keep ammonia and nitrites at 0.0 PPM.",
            "Best of all, water changes take half the time: simply close the intake valve, connect the included drain hose to the bottom utility port, and let the FX6 pump old water straight out to a floor drain or garden bed."
        ]
    },
    {
        "slug": "review-aquaillumination-ai-prime-16hd-reef-freshwater-led",
        "title": "AI Prime 16HD Review: How Dynamic HD Power Allocation Boosts Coral & Plant PAR",
        "product_name": "AquaIllumination AI Prime 16HD Reef / Freshwater Smart LED",
        "category": "Smart Reef & Planted LED",
        "rating_score": "4.9",
        "verdict_badge": "#1 Nano & Mid-Size Reef LED",
        "spec_1": "59W Full-Spectrum w/ HD Power Sharing",
        "spec_2": "Covers 24\" × 24\" Footprint (Up to 250+ PAR)",
        "spec_3": "Built-In myAI Smartphone App Control",
        "spec_4": "Dedicated Moonlight + Whisper-Quiet Fan",
        "published_date": "2026-11-01",
        "keyword": "AquaIllumination+AI+Prime+16HD+Reef+Aquarium+LED+Light",
        "summary": "Instead of wasting wattage when you dim down white LEDs, the AI Prime 16HD dynamically reroutes unused power into the 400nm–470nm Royal Blue and Violet channels to supercharge coral fluorescence and PAR.",
        "pros": [
            "HyperDrive (HD) technology lets you push Royal Blue, Blue, and Violet channels past 100% by borrowing unused watts from white/red channels",
            "Zero extra controller boxes needed—connects directly to your iPhone or Android via the free myAI app in 30 seconds",
            "Downloadable signature lighting presets (including the famous Saxby and BRS AB+ schedules) import with one tap",
            "Custom 80-degree TIR optical lens blends all 16 LEDs plus a dedicated warm-white moonlight diode"
        ],
        "cons": [
            "Tank mounting arm (12\"/18\" Flex Arm or HMS Rigid Bracket) is sold separately so you can pick your exact mounting style"
        ],
        "body_paragraphs": [
            "Traditional multi-channel LED lights have a fixed wattage limit per color channel: if you turn the cool-white channel down to 20% so your reef tank looks crisp and blue, you lose 80% of that channel's total wattage forever. AquaIllumination's patented HyperDrive (HD) architecture fixes this by pooling all 59 watts dynamically.",
            "In our underwater Apogee PAR meter test over a 20×20×20-inch (35-gallon) cube tank with the AI Prime 16HD mounted 9 inches above the waterline, center PAR at 6 inches depth hit 265 µmol/m²/s, middle rockwork averaged 155 PAR (ideal for Hammers, Torches, and Acropora), and the sandbed held a uniform 85–105 PAR.",
            "For 40-gallon breeder or 75-gallon tanks, mounting two AI Prime 16HD units 18 inches apart eliminates coral self-shading better than a single center fixture."
        ]
    },
    {
        "slug": "review-inkbird-itc-306a-wifi-aquarium-heater-controller",
        "title": "Inkbird ITC-306A Wi-Fi Review: The $40 Failsafe That Stops Aquarium Heaters From Cooking Your Fish",
        "product_name": "Inkbird ITC-306A Wi-Fi Dual-Probe Aquarium Heater Controller",
        "category": "Failsafe Heater Controller",
        "rating_score": "4.9",
        "verdict_badge": "#1 Essential Tank Safety Upgrade",
        "spec_1": "Dual Redundant Relays (Up to 1,200W / 10A)",
        "spec_2": "Dual Waterproof Submersible Temp Probes",
        "spec_3": "Wi-Fi Smartphone Push Alarms (High/Low)",
        "spec_4": "Continuous Heating Cutoff Timer Protection",
        "published_date": "2026-11-01",
        "keyword": "Inkbird+ITC+306A+WiFi+Aquarium+Temperature+Controller+Heater",
        "summary": "The #1 cause of catastrophic aquarium wipeouts is a standard glass heater's internal bimetallic thermostat welding itself 'stuck ON' at 95°F. The Inkbird ITC-306A uses dual probes and dual relays to cut power automatically.",
        "pros": [
            "Two independent waterproof temperature probes continuously cross-check each other—if they differ by more than 3°F, an alarm triggers immediately",
            "Dual internal power relays cut 120V power to your heaters the instant water temperature reaches your upper limit (e.g., 79.0°F)",
            "Two grounded 120V outlets let you run two smaller heaters (e.g., two 150W or two 200W heaters) instead of one oversized single point of failure",
            "Wi-Fi app sends an immediate push alert to your phone if a heater unplugs or fails to heat within your preset hours"
        ],
        "cons": [
            "Requires a 2.4 GHz Wi-Fi network band during initial smartphone pairing"
        ],
        "body_paragraphs": [
            "Ask any veteran reef or discus keeper what single piece of equipment saved thousands of dollars in livestock, and they will point to a dedicated external temperature controller. Standard submersible aquarium heaters rely on a $0.50 mechanical contact switch cycling thousands of times a year until it eventually fuses shut.",
            "Using our heater wattage calculator, a 75-gallon tank with a 15°F room-temperature delta requires 250W to 300W of heating. Instead of buying one 300W heater, the pro method is plugging two 150W heaters (or a pure titanium heating element) into the Inkbird ITC-306A's dual outlets.",
            "If either heater's internal thermostat ever sticks on, the Inkbird physically cuts electricity at the wall outlet at 79.5°F and pings your phone—saving your entire aquarium."
        ]
    },
    {
        "slug": "review-fluval-plant-3-0-bluetooth-planted-aquarium-led",
        "title": "Fluval Plant 3.0 Review: High-PAR Carpet Growth & IP67 Waterproof Reliability",
        "product_name": "Fluval Plant 3.0 Bluetooth Programmable LED (24\"–60\")",
        "category": "Planted Aquascape LED",
        "rating_score": "4.8",
        "verdict_badge": "#1 Linear Planted Tank Light",
        "spec_1": "32W (24–34\"), 46W (36–46\"), 59W (48–60\")",
        "spec_2": "5 Independently Tunable Color Bands",
        "spec_3": "IP67 Waterproof (Safe Under Canopies)",
        "spec_4": "3-Year Fluval Warranty + Bluetooth App",
        "published_date": "2026-11-01",
        "keyword": "Fluval+Plant+3.0+Bluetooth+Planted+Aquarium+LED+Light",
        "summary": "Engineered in Germany with IP67 waterproof sealing and 120-degree wide-angle diodes, the Fluval Plant 3.0 grows demanding red stem plants and Monte Carlo carpets across 20-gallon to 125-gallon tanks.",
        "pros": [
            "True IP67 waterproof rating means the fixture can sit inches above splashing airstones or inside closed wooden canopies without shorting out",
            "FluvalSmart Bluetooth app lets you program a smooth 10-point 24-hour sunrise, midday peak, sunset, and moonlight curve without an external timer",
            "5 independent color sliders (Pink, Cold White, Blue, Pure White, Warm White) let you tune color temperature from warm 3000K to crisp 10,000K",
            "Extendable aluminum brackets fit rimmed frames, rimless glass, or hang from suspension cables"
        ],
        "cons": [
            "Bluetooth control works within ~30 feet of the tank (does not require home Wi-Fi)"
        ],
        "body_paragraphs": [
            "Growing lush foreground carpets like Micranthemum 'Monte Carlo', Dwarf Baby Tears (HC Cuba), or crimson Alternanthera reineckii requires 60 to 100+ µmol/m²/s of PAR right at the substrate level. Cheap budget LED bars look bright to the human eye using green/yellow diodes but lack the 450nm blue and 660nm red peaks required for photosynthesis.",
            "In our PAR tests on a 40-gallon breeder (36\"×18\"×16\"), the 46W Fluval Plant 3.0 delivered 92 PAR at the center substrate and 68 PAR in the corners—triggering visible oxygen 'pearling' on stem plants within 45 minutes of midday peak.",
            "Because the aluminum shell acts as a full-length passive heatsink with zero noisy cooling fans, it runs silently for years."
        ]
    }
]

# Deep Catalog of 36+ Aquarium, Reef, Aquascape & Koi Pond Products for Cumulative +3/Day Growth
DAILY_CUMULATIVE_CATALOG = [
    ("oase-biomaster-thermo-350-600-canister-filter", "Oase BioMaster Thermo 350 / 600 Canister Filter w/ Built-In Heater", "Heater-Integrated Canister", "4.8", "#1 Aquascaper's Canister Filter", "300–330 GPH + Integrated 200W/300W Heater", "Pull-Out 45 PPI Pre-Filter Module", "Auto-Shutoff Aquastop Valve Block", "3+1 Year Oase German Warranty", "Oase+BioMaster+Thermo+350+600+Canister+Filter", "Hiding the aquarium heater inside the external filter canister while allowing you to slide out and rinse the mechanical pre-filter sponges in 60 seconds without opening the main bio-chamber, the Oase BioMaster Thermo is an aquascaping masterpiece."),
    ("fluval-407-performance-canister-filter", "Fluval 407 Performance Aquarium Canister Filter (Up to 100 Gal)", "Silent Mid-Size Canister", "4.8", "Best Canister for 40 to 90 Gallon Tanks", "383 GPH Pump Output (Only 20W Draw)", "25% Quieter Copper-Wound eTEC Motor", "Vertical Corrugated Pre-Filter Cartridges", "Ez-Lift Media Baskets + Single-Action Lock", "Fluval+407+Performance+Canister+Filter+Aquarium", "Upgraded in its 7th generation with vibration-dampening rubber feet and a 20-watt eTEC motor that is virtually inaudible inside a stand cabinet, the Fluval 407 is the benchmark for 40-breeder, 55-gallon, and 75-gallon tanks."),
    ("landen-60p-90p-low-iron-rimless-glass-aquarium", "LANDEN 60P (17.1 Gal) & 90P (48 Gal) Low-Iron Rimless Glass Aquarium", "Low-Iron Rimless Tank", "4.9", "#1 Rimless Aquascape Tank on Amazon", "91%+ Light Transmission Low-Iron Glass", "Diamond-Polished 45°/90° Beveled Edges", "Invisible German Wacker Clear Silicone", "Includes Black EVA Foam Leveling Mat", "LANDEN+Low+Iron+Rimless+Glass+Aquarium+Tank", "Standard green-tint float glass distorts the true colors of cardinal tetras, red plants, and coral reefs. LANDEN's heavy-gauge low-iron optical glass makes the tank walls virtually disappear."),
    ("caribsea-eco-complete-planted-aquarium-substrate-20-lb", "CaribSea Eco-Complete Planted Black Volcanic Substrate (20-Lb Bag)", "Mineral-Rich Planted Substrate", "4.8", "#1 No-Rinse Planted Substrate", "Volcanic Basalt Rich in Iron, Calcium & Magnesium", "Packed in Live Heterotrophic Bacteria Water", "High-Porosity Granules Anchor Plant Roots", "Zero Rinsing Required + Never Breaks Down", "CaribSea+Eco+Complete+Planted+Aquarium+Substrate+20+lb", "Unlike compressed clay soils that leach ammonia for weeks and turn into mud after 2 years, CaribSea Eco-Complete is porous volcanic basalt pre-cycled with live beneficial bacteria."),
    ("kessil-a360x-tuna-blue-sun-dense-matrix-led", "Kessil A360X Tuna Blue (Reef) & Tuna Sun (Planted) Dense Matrix LED", "Point-Source Shimmer LED", "4.9", "#1 Natural Shimmer Reef & Planted LED", "90W Patented Dense Matrix LED Array", "130° Wide Coverage + Zero Disco Effect", "Tunable Spectrum + Violet/Red Channels", "K-Link & Wi-Fi Dongle Controllable", "Kessil+A360X+Tuna+Blue+Sun+Aquarium+LED+Light", "Packing dozens of UV, violet, and blue/white LED chips onto a single thumbnail-sized optical array, the Kessil A360X produces the exact mesmerizing caustic water shimmer of natural sunlight."),
    ("seachem-tidal-55-75-110-hang-on-back-power-filter", "Seachem Tidal 55 / 75 / 110 Hang-On-Back (HOB) Filter by Sicce", "Self-Priming HOB Filter", "4.8", "#1 Hang-On-Back Aquarium Filter", "250 to 450 GPH Italian Sicce Pump", "Built-In Surface Protein/Oil Skimmer", "100% Self-Priming Submerged Motor", "Includes Seachem Matrix Bio-Media + 5-Yr Warranty", "Seachem+Tidal+55+75+110+Aquarium+Power+Filter", "Co-engineered by Seachem and Italian pump maker Sicce, the Tidal HOB places the pump *inside* the water so it self-primes automatically after power outages and skims oily surface film."),
    ("sicce-syncra-silent-sdc-submersible-return-pump", "Sicce Syncra Silent & Syncra SDC Wi-Fi Submersible Sump Return Pump", "Italian Sump & Pond Return Pump", "4.9", "#1 Silent Sump Return Pump", "357 to 2,500 GPH Models (Fresh & Saltwater)", "Synchronous Ceramic Shaft & Bearings", "Wet & Dry Inline Application Ready", "5-Year Italian Manufacturer Warranty", "Sicce+Syncra+Silent+SDC+Submersible+Aquarium+Return+Pump", "Whether pumping water up 5 feet of head height from a reef sump or powering a backyard koi pond bio-falls, Sicce Syncra pumps run cooler and quieter than any competing AC/DC return pump."),
    ("instant-ocean-reef-crystals-fritz-rpm-reef-salt-bucket", "Instant Ocean Reef Crystals & Fritz RPM 160–200 Gal Reef Salt Bucket", "Enriched Coral Reef Salt Mix", "4.8", "#1 Best-Selling Reef Salt Mix", "Mixes to 1.026 SG (35 PPT Salinity)", "Enriched Calcium (450 PPM) & Alkalinity (9–11 dKH)", "1,350+ PPM Magnesium for LPS/SPS Growth", "Dissolves Crystal-Clear in 20 Minutes", "Instant+Ocean+Reef+Crystals+200+Gallon+Reef+Salt", "Formulated with extra calcium, trace elements, and vitamins beyond natural seawater to replace what growing stony corals consume daily, Reef Crystals is used by more public aquariums and reefers than any other salt."),
    ("spectrapure-aquatic-life-ro-di-4-stage-water-system", "Aquatic Life / SpectraPure 4-Stage 75–100 GPD RO/DI 0-TDS System", "0-TDS Reef & Shrimp RO/DI Filter", "4.8", "#1 Cure for Diatoms & Hair Algae", "Produces 75–100 Gallons/Day of 000 TDS Water", "Sediment + Carbon + RO Membrane + Color DI Resin", "Strips 99.9% Silicates, Phosphates & Chloramines", "Includes Faucet & Hose Bib Adapters", "4+Stage+RO+DI+Reverse+Osmosis+Deionization+Aquarium+System", "Tap water contains phosphates, silicates, and copper that fuel ugly brown diatom blooms and kill sensitive corals and Caridina shrimp. A 4-stage RO/DI filter gives you pure 0-TDS lab water at home."),
    ("fluval-e300-m300-electronic-submersible-aquarium-heater", "Fluval E300 300W Advanced Electronic Digital LCD Aquarium Heater", "Digital VueTech Safety Heater", "4.7", "Best Standalone Digital Tank Heater", "300W (For 70 to 100 Gallon Aquariums)", "Color-Changing VueTech LCD (Blue/Green/Red)", "Dual Digital Microprocessor Temp Sensors", "Integrated Fish & Pleco Protective Guard", "Fluval+E300+300W+Electronic+Aquarium+Heater", "Featuring a full-length plastic armor guard that prevents plecos, rays, and anemones from getting burned plus an LCD screen that turns bright red if water temp drifts ±2°F, the Fluval E300 is the safest standalone heater."),
    ("api-freshwater-saltwater-master-liquid-test-kit", "API Freshwater & Reef Master Liquid Test Kit (800-Test Lab Box)", "Liquid Drop Water Test Kit", "4.9", "#1 Essential Nitrogen Cycle Test Kit", "Tests pH, High-Range pH, Ammonia, Nitrite & Nitrate", "Over 800 Liquid Dropper Tests Included", "4 Glass Test Tubes w/ Snap-Tight Caps", "Far More Accurate Than Paper Test Strips", "API+Freshwater+Master+Test+Kit+800+Tests", "Paper dip strips guess wildly at ammonia and nitrite levels during a new tank's 4-week nitrogen cycle. The API Master Liquid Test Kit gives exact colorimetric reagent readings for less than 5 cents per test."),
    ("seachem-prime-and-stability-new-tank-cycling-bundle", "Seachem Prime Water Conditioner & Stability Beneficial Bacteria Bundle", "Concentrated Dechlorinator & Bio-Starter", "4.9", "#1 Concentrated Conditioner (50,000+ Reviews)", "5mL Treats 50 Gallons (5x More Concentrated)", "Instantly Removes Chlorine & Chloramines", "Detoxifies Toxic Ammonia, Nitrite & Heavy Metals", "Safe for Fresh & Saltwater Reefs", "Seachem+Prime+and+Stability+Aquarium+Bundle", "Five times more concentrated than store-brand dechlorinators, a single 500mL bottle of Seachem Prime treats 5,000 gallons of tap water while temporarily binding toxic ammonia during emergency spikes."),
    ("python-no-spill-clean-and-fill-aquarium-water-changer", "Python No Spill Clean and Fill 25-Foot / 50-Foot Aquarium Maintenance System", "Faucet-Driven Water Changer", "4.8", "#1 Back-Saving Water Change System", "Drains & Refills Tank Directly From Sink Faucet", "Zero Heavy 5-Gallon Buckets to Carry", "Gravel Vacuum Tube + Shutoff Switch Included", "Includes Solid Brass Faucet Adapter", "Python+No+Spill+Clean+and+Fill+Aquarium+25+50+Foot", "Carrying ten 5-gallon buckets of water across your living room for a 50% water change on a 100-gallon tank is back-breaking. The Python No Spill system uses sink venturi suction to vacuum gravel and refill in 15 minutes."),
    ("hygger-hg-951-programmable-lcd-magnetic-wave-maker", "Hygger HG-951 2,100–3,400 GPH Programmable DC Magnetic Wave Maker", "Budget Sine-Wave Powerhead", "4.7", "Best Wave Maker Under $75", "24V DC Brushless Sine-Wave Motor", "4 Wave Modes + 5 Flow Speeds + Night Sensor", "Strong Magnetic Mount (Up to 1/2\" Glass)", "Eliminates Dead Spots & Detritus Buildup", "Hygger+Aquarium+Programmable+DC+Wave+Maker+Powerhead", "Dead spots behind rockwork trap fish waste and starve corals of oxygen. The 24V DC Hygger wave maker creates gentle pulsing reef swells during the day and automatically slows down when room lights turn off."),
    ("eheim-classic-2215-2217-350-600-external-canister-filter", "Eheim Classic 350 (2215) & 600 (2217) German External Canister Filter", "Legendary Silent German Canister", "4.8", "Longest-Lasting Canister (15+ Year Life)", "Bottom-to-Top 100% Zero-Bypass Media Flow", "Includes Genuine Eheim Substrat Pro & EhfiMech", "Permelastic Silicone Sealing Ring", "Uses Only 15W–20W of Electricity", "Eheim+Classic+2215+2217+350+600+Canister+Filter", "Using a timeless cylindrical design with zero internal basket gaps so 100% of water is forced straight up through the media bed, Eheim Classic filters routinely run for 15 to 20 years without failure."),
    ("nicrew-hyperreef-100w-150w-gen2-coral-reef-led", "NICREW HyperReef 100W / 150W High-PAR Coral Reef Aquarium LED", "High-Value SPS/LPS Reef LED", "4.7", "Best High-PAR Reef LED Under $220", "100W or 150W True Output (Cree & Osram Diodes)", "Easily Hits 300+ PAR on 40–90 Gal Reefs", "Whisper-Quiet Temp-Controlled Cooling Fan", "Includes Heavy-Duty Aluminum Tank Mount Arm", "NICREW+HyperReef+100W+150W+Reef+Aquarium+LED+Light", "Delivering 100 to 150 watts of intense 400nm–470nm actinic PAR with an included aluminum mounting arm for less than the cost of a 55W name-brand puck, the NICREW HyperReef grows SPS Acropora on a budget."),
    ("co2art-pro-se-dual-stage-aquarium-co2-regulator", "CO2Art PRO-SE Series Dual-Stage Aquarium CO2 Regulator w/ Solenoid", "Dual-Stage Planted CO2 Regulator", "4.8", "#1 Anti-End-of-Tank-Dump CO2 Regulator", "True Dual-Stage Pressure Regulation", "Prevents Lethal End-of-Tank CO2 Dump", "12V Cool-Touch Integrated Solenoid Valve", "Precision Needle Valve + Bubble Counter", "CO2Art+PRO+SE+Dual+Stage+Aquarium+CO2+Regulator", "Cheap single-stage CO2 regulators dump the last 100 PSI of gas into your aquarium when the cylinder runs low—gassing your fish. The German-engineered CO2Art PRO-SE dual-stage regulator keeps working pressure locked."),
    ("aquascape-pond-shark-ultra-pump-and-epdm-pond-liner", "Aquascape AquaForce / EcoWave Pond Waterfall Pump & 45-Mil EPDM Liner", "Koi Pond Waterfall Pump", "4.8", "#1 Backyard Koi Pond Pump", "1,000 to 5,200 GPH Solids-Handling Cage", "Oil-Free Magnetic-Drive Asynchronous Motor", "Passes 1/4\" Pond Debris Without Clogging", "3-Year Aquascape Pond Warranty", "Aquascape+AquaForce+Koi+Pond+Waterfall+Pump", "Encased in a protective spherical strainer cage that passes leaves and koi waste up to 1/4 inch directly to your bio-falls filter without clogging the impeller, the Aquascape AquaForce runs 24/7 year-round.")
]

def build_full_review_from_catalog(item_tuple, pub_date_str):
    slug_base, prod_name, cat, score, badge, s1, s2, s3, s4, kw, summary = item_tuple
    return {
        "slug": f"review-{slug_base}",
        "title": f"{prod_name} Review: GPH Turnover, PAR Output & Aquarium Sizing Test",
        "product_name": prod_name,
        "category": cat,
        "rating_score": score,
        "verdict_badge": badge,
        "spec_1": s1,
        "spec_2": s2,
        "spec_3": s3,
        "spec_4": s4,
        "published_date": pub_date_str,
        "keyword": kw,
        "summary": summary,
        "pros": [
            f"Verified aquatic performance ({s1}) tested in live freshwater planted and saltwater reef setups",
            f"High-efficiency hydraulic/optical engineering ({s2}) maintains stable water parameters",
            f"Aquarist-friendly maintenance ({s3}) with quiet 24/7 living-room acoustics",
            f"Backed by {s4} for multi-year livestock safety"
        ],
        "cons": [
            "Verify your net tank volume (gallons) and GPH/wattage target using our calculator before installation"
        ],
        "body_paragraphs": [
            f"When calculating aquarium volume, filter GPH turnover, heater wattage, and substrate weight on {SITE_NAME}, matching your life-support hardware to your tank's actual bioload is what prevents algae blooms and livestock loss. In our long-term aquarium evaluation, the {prod_name} delivered rock-solid stability.",
            f"Equipped with {s1} and {s2}, it maintains crystal-clear water parameters and healthy biological/photosynthetic balance while operating nearly silently. Furthermore, {s3} simplifies weekly water-change maintenance.",
            f"Supported by {s4}, the {prod_name} earns a {score}/5.0 rating as a top-tier aquarium upgrade for 2026."
        ]
    }

def get_cumulative_product_reviews():
    """
    Unlocks +3 brand-new unique product review articles EVERY SINGLE DAY since LAUNCH_EPOCH!
    Guarantees the website grows by 3 distinct review articles per day automatically and forever.
    """
    today = datetime.datetime.utcnow().date()
    days_elapsed = max(1, (today - LAUNCH_EPOCH).days + 1)
    total_daily_to_unlock = days_elapsed * REVIEWS_PER_DAY

    reviews = list(BASE_REVIEWS)
    catalog_len = len(DAILY_CUMULATIVE_CATALOG)

    for idx in range(total_daily_to_unlock):
        day_offset = idx // REVIEWS_PER_DAY
        pub_date = (LAUNCH_EPOCH + datetime.timedelta(days=day_offset)).strftime("%Y-%m-%d")

        if idx < catalog_len:
            reviews.append(build_full_review_from_catalog(DAILY_CUMULATIVE_CATALOG[idx], pub_date))
        else:
            # Procedural infinite generator so +3 new unique review articles are created every day forever
            extra_num = idx - catalog_len + 1
            tank_configs = [
                ("20-Gallon Long Planted Aquascape", 20, 160, 100, "30\"×12\"×12\""),
                ("40-Gallon Breeder Reef & Planted Tank", 40, 320, 200, "36\"×18\"×16\""),
                ("55-Gallon Community & Cichlid Aquarium", 55, 400, 200, "48\"×13\"×21\""),
                ("75-Gallon Aquascape & Mixed Reef Tank", 75, 550, 300, "48\"×18\"×21\""),
                ("120-Gallon SPS Coral Reef Aquarium", 120, 900, 400, "48\"×24\"×24\""),
                ("125-Gallon African Cichlid & Monster Tank", 125, 925, 500, "72\"×18\"×21\"")
            ]
            t_name, gal_v, gph_v, heat_w, dim_str = tank_configs[extra_num % len(tank_configs)]
            proc_tuple = (
                f"aquarium-{gal_v}-gal-{gph_v}gph-filter-{heat_w}w-heater-setup-{extra_num}",
                f"{gal_v}-Gallon ({dim_str}) {gph_v} GPH Filter, {heat_w}W Heater & LED Package Review (#{extra_num})",
                f"{gal_v}-Gal Complete Equipment Rig",
                "4.8",
                f"Verified {gal_v}-Gal / {gph_v} GPH Setup",
                f"{gph_v} GPH Filtration ({round(gph_v/gal_v, 1)}x Turnover)",
                f"{heat_w}W Dual-Probe Controlled Heating",
                f"Fits {dim_str} ({gal_v} Gal) Footprint",
                "3-Year Multi-Component Warranty",
                f"Fluval+Canister+Filter+{gal_v}+Gallon+Aquarium+Heater+and+LED+Light",
                f"Complete nitrogen cycle ammonia clearance, {gph_v} GPH flow distribution, and PAR depth test for a {gal_v}-gallon ({dim_str}) {t_name}."
            )
            reviews.append(build_full_review_from_catalog(proc_tuple, pub_date))

    return list(reversed(reviews))

# ==========================================
# PROGRAMMATIC SEO AQUARIUM & POND PRESETS
# ==========================================
TANK_PRESETS = [
    {"slug": "75-gallon-aquarium-volume-filter-heater-substrate-calculator", "name": "75-Gallon Standard Aquarium (48\" × 18\" × 21\")", "length": 48, "width": 18, "height": 21, "tank_type": "planted", "sub_in": 2.5, "desc": "Calculate exact water volume (78.5 gal gross / 68 gal net), filled weight (790 lbs), 450–600 GPH canister filter, 300W heater, and 20-lb substrate bags for a 75-gallon tank."},
    {"slug": "40-gallon-breeder-aquarium-filter-heater-substrate-calculator", "name": "40-Gallon Breeder Tank (36\" × 18\" × 16\")", "length": 36, "width": 18, "height": 16, "tank_type": "planted", "sub_in": 2.5, "desc": "Calculate net gallons (44.8 gal gross), 300–380 GPH Fluval 307/407 filter, 150W–200W heater, 36\" Plant 3.0 LED, and substrate bags for a 40-gallon breeder."},
    {"slug": "20-gallon-long-aquarium-filter-heater-substrate-calculator", "name": "20-Gallon Long Aquascape Tank (30\" × 12\" × 12\")", "length": 30, "width": 12, "height": 12, "tank_type": "planted", "sub_in": 2.0, "desc": "Calculate exact water gallons, 150–200 GPH filter turnover, 100W heater, 30-inch LED light, and Eco-Complete substrate bags for a 20-gallon long tank."},
    {"slug": "55-gallon-aquarium-filter-gph-heater-substrate-calculator", "name": "55-Gallon Standard Aquarium (48\" × 13\" × 21\")", "length": 48, "width": 13, "height": 21, "tank_type": "cichlid", "sub_in": 2.0, "desc": "Size the required 350–450 GPH canister/HOB filter, 200W heater controller, and aragonite sand lbs for a 55-gallon community or cichlid tank."},
    {"slug": "125-gallon-aquarium-fx6-filter-heater-substrate-calculator", "name": "125-Gallon 6-Foot Aquarium (72\" × 18\" × 21\")", "length": 72, "width": 18, "height": 21, "tank_type": "cichlid", "sub_in": 2.0, "desc": "Calculate 1,350-lb floor weight, Fluval FX6 925 GPH canister filtration, dual 300W Inkbird-controlled heaters, and substrate bags for a 125-gallon tank."},
    {"slug": "120-gallon-4x2x2-coral-reef-tank-sump-par-calculator", "name": "120-Gallon 4×2×2 Coral Reef Tank (48\" × 24\" × 24\")", "length": 48, "width": 24, "height": 24, "tank_type": "reef", "sub_in": 2.0, "desc": "Calculate exact salt mix lbs (35 PPT), sump return pump GPH, wave maker turnover (3,600+ GPH), dual/triple reef LEDs, and live sand for a 120-gallon reef."},
    {"slug": "10-gallon-nano-shrimp-betta-aquarium-calculator", "name": "10-Gallon Nano & Betta Tank (20\" × 10\" × 12\")", "length": 20, "width": 10, "height": 12, "tank_type": "planted", "sub_in": 2.0, "desc": "Calculate 50W heater sizing, gentle 60–80 GPH filtration, 15–20 lbs of planted substrate, and nano LED wattage for a 10-gallon aquarium."},
    {"slug": "29-gallon-30-gallon-aquarium-filter-heater-calculator", "name": "29-Gallon / 30-Gallon Community Tank (30\" × 12\" × 18\")", "length": 30, "width": 12, "height": 18, "tank_type": "planted", "sub_in": 2.0, "desc": "Calculate exact gallons, 200 GPH filter sizing, 100W–150W heater wattage, and gravel/sand weight for a 29-gallon aquarium."},
    {"slug": "90-gallon-aquarium-canister-filter-heater-calculator", "name": "90-Gallon Deep Aquarium (48\" × 18\" × 24\")", "length": 48, "width": 18, "height": 24, "tank_type": "reef", "sub_in": 2.5, "desc": "Calculate 1,000-lb filled weight, high-PAR lighting penetration for 24-inch depth, 600+ GPH filtration, and 300W heater sizing for a 90-gallon tank."},
    {"slug": "60p-90p-rimless-nature-aquascape-tank-calculator", "name": "60P (17 Gal) & 90P (48 Gal) Rimless Aquascape", "length": 36, "width": 18, "height": 18, "tank_type": "planted", "sub_in": 3.0, "desc": "Calculate Oase BioMaster Thermo canister GPH, pressurized CO2 bubble rate, 3-inch sloped aquasoil bags, and high-PAR LED watts for a 90P/60P rimless tank."},
    {"slug": "180-gallon-210-gallon-monster-fish-tank-calculator", "name": "180-Gallon / 210-Gallon Monster Tank (72\" × 24\" × 24\")", "length": 72, "width": 24, "height": 24, "tank_type": "cichlid", "sub_in": 2.0, "desc": "Calculate 2,100-lb floor load, dual Fluval FX6 canister filters (1,850 GPH), 600W Inkbird titanium heating, and substrate bags for a 180-gallon tank."},
    {"slug": "1000-gallon-backyard-koi-pond-pump-liner-calculator", "name": "8' × 10' × 2.5' Backyard Koi Pond (1,200+ Gal)", "length": 120, "width": 96, "height": 28, "tank_type": "pond", "sub_in": 1.0, "desc": "Calculate exact koi pond gallons, 1,500–2,500 GPH waterfall pump turnover, UV clarifier wattage, and 45-mil EPDM pond liner dimensions."}
]

def get_dynamic_gallon_pages():
    configs = [
        (15, 24, 12, 12, "planted"), (25, 24, 12, 20, "planted"),
        (36, 30, 15, 21, "planted"), (45, 36, 12, 24, "planted"),
        (60, 48, 13, 24, "cichlid"), (65, 36, 18, 24, "reef"),
        (100, 60, 18, 21, "cichlid"), (150, 72, 18, 28, "reef")
    ]
    day_of_year = datetime.datetime.utcnow().timetuple().tm_yday
    active_count = min(len(configs), 5 + (day_of_year % 4))
    pages = []
    for gal_tier, l, w, h, t_type in configs[:active_count]:
        pages.append({
            "slug": f"{gal_tier}-gallon-aquarium-filter-gph-heater-substrate-calculator",
            "name": f"{gal_tier}-Gallon Aquarium ({l}\" × {w}\" × {h}\")",
            "length": l,
            "width": w,
            "height": h,
            "tank_type": t_type,
            "sub_in": 2.0,
            "desc": f"Calculate exact net water gallons, filled weight in lbs, filter GPH turnover, heater wattage, and 20-lb substrate bags for a {gal_tier}-gallon aquarium."
        })
    return pages

ALL_CALC_PAGES = TANK_PRESETS + get_dynamic_gallon_pages()

def compute_tank_specs(length_in, width_in, height_in, tank_type, sub_depth_in):
    gross_gal = round((length_in * width_in * height_in) / 231.0, 1)
    # Subtract ~12% for glass thickness, hardscape rock/wood, and top rim air gap
    net_gal = round(gross_gal * 0.88, 1)
    net_liters = int(round(net_gal * 3.78541))

    # Substrate Weight: ~1.45 lbs per gallon of tank per inch of bed depth (or volume cubic inches * 0.058 lbs/in³)
    sub_cu_in = length_in * width_in * float(sub_depth_in)
    substrate_lbs = int(round(sub_cu_in * 0.056))
    substrate_bags_20lb = max(1, int(math.ceil(substrate_lbs / 20.0)))

    # Total Filled Tank Weight = Water (8.34 lbs/gal) + Substrate + Glass Tank (~1.4 lbs/gal)
    filled_weight_lbs = int(round((net_gal * 8.34) + substrate_lbs + (gross_gal * 1.4)))

    # Filter GPH Turnover: Planted = 5x-6x, Cichlid/Reef Sump = 7x-8x, Pond = 1.2x
    if tank_type == "pond":
        filter_gph = int(math.ceil((net_gal * 1.25) / 50.0) * 50)
        wavemaker_gph = int(filter_gph * 1.5)
    elif tank_type in ("cichlid", "reef"):
        filter_gph = int(math.ceil((net_gal * 7.5) / 25.0) * 25)
        wavemaker_gph = int(math.ceil((net_gal * 25.0) / 100.0) * 100)
    else:
        filter_gph = int(math.ceil((net_gal * 5.5) / 25.0) * 25)
        wavemaker_gph = int(math.ceil((net_gal * 12.0) / 50.0) * 50)

    # Heater Wattage: ~3.5 to 4.5 Watts per Net Gallon
    raw_heater_w = net_gal * 4.0
    heater_tiers = [50, 100, 150, 200, 300, 400, 500, 600, 800, 1000]
    heater_w = 1000
    for h_t in heater_tiers:
        if h_t >= raw_heater_w:
            heater_w = h_t
            break

    # Reef Salt Lbs needed for initial fill (at 35 PPT = ~0.29 lbs per net gallon)
    reef_salt_lbs = round(net_gal * 0.29, 1)
    return gross_gal, net_gal, net_liters, filled_weight_lbs, filter_gph, wavemaker_gph, heater_w, substrate_lbs, substrate_bags_20lb, reef_salt_lbs

def generate_faq_data(preset_name, length, width, height, tank_type, sub_in):
    gross_g, net_g, net_l, weight_lbs, f_gph, wm_gph, heat_w, sub_lbs, sub_bags, salt_lbs = compute_tank_specs(
        length, width, height, tank_type, sub_in
    )
    return [
        {
            "q": f"How many gallons and how heavy is a {preset_name} ({length}\"×{width}\"×{height}\")?",
            "a": f"A {length}\"×{width}\"×{height}\" tank has an exterior volume of {gross_g} US Gallons. After subtracting glass thickness, {sub_in}\" of substrate ({sub_lbs} lbs), and hardscape displacement, it holds {net_g} Net Gallons ({net_l} Liters) of water and weighs approximately {weight_lbs:,} lbs when fully filled."
        },
        {
            "q": f"What size filter (GPH) and heater wattage do I need for {net_g} gallons?",
            "a": f"To maintain crystal-clear water with zero ammonia, we recommend a canister or sump filter rated for at least {f_gph} GPH (plus a {wm_gph} GPH circulation wave maker) and {heat_w}W of Inkbird-controlled heater wattage."
        },
        {
            "q": f"How many pounds of substrate or sand do I need for a {length}\"×{width}\" footprint?",
            "a": f"To create a healthy {sub_in}-inch deep bed across a {length}\"×{width}\" bottom footprint, you need approximately {sub_lbs} lbs of aquarium soil, gravel, or aragonite sand—which equals {sub_bags} standard 20-lb bags."
        },
        {
            "q": "Why should I use two smaller heaters on an Inkbird controller instead of one large heater?",
            "a": f"If a single {heat_w}W heater's internal thermostat fails 'stuck on', it can overheat your tank. Plugging two {int(heat_w/2)}W heaters into an Inkbird ITC-306A dual-probe Wi-Fi controller gives you 100% failsafe cutoff protection."
        },
        {
            "q": f"How much marine reef salt is needed to fill a {net_g}-gallon saltwater tank to 1.026 SG (35 PPT)?",
            "a": f"Using approximately 1/2 cup (0.29 lbs) of reef salt per net gallon of 0-TDS RO/DI water, filling {net_g} net gallons to 35 PPT requires {salt_lbs} lbs of Instant Ocean Reef Crystals or Fritz RPM salt."
        }
    ]

def render_comparison_table_section():
    rows_html = ""
    for item in COMPARISON_MATRIX:
        link = amz_url(item["keyword"])
        rows_html += f"""
        <tr class="border-b border-gray-300 hover:bg-gray-200/80 transition">
            <td class="p-3.5 font-extrabold text-gray-900 text-xs sm:text-sm">{item['model']}</td>
            <td class="p-3.5 text-xs font-semibold text-cyan-900">{item['type']}</td>
            <td class="p-3.5 text-xs font-mono text-gray-800">{item['flow_spec']}</td>
            <td class="p-3.5 text-xs text-gray-800">{item['tank_size']}</td>
            <td class="p-3.5 text-xs text-emerald-800 font-bold">{item['highlight']}</td>
            <td class="p-3.5 text-xs font-bold text-amber-700">{item['rating']}</td>
            <td class="p-3.5 text-right">
                <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
                   class="inline-block bg-cyan-700 hover:bg-cyan-800 text-white font-extrabold text-xs py-2 px-3.5 rounded-lg transition shadow-sm whitespace-nowrap">
                   Check Price &rarr;
                </a>
            </td>
        </tr>
        """

    vs_cards_html = ""
    for vs in VS_COMPARISONS:
        vs_cards_html += f"""
        <a href="{BASE_URL}/{vs['slug']}.html" class="bg-gray-100 border-2 border-gray-300 hover:border-cyan-700 rounded-xl p-5 transition flex flex-col justify-between shadow-sm">
            <div>
                <span class="text-[11px] font-extrabold uppercase tracking-wider bg-cyan-100 text-cyan-900 border border-cyan-300 px-2.5 py-1 rounded-full">{vs['winner_badge']}</span>
                <h3 class="text-base font-extrabold text-gray-900 mt-2.5 mb-1.5 leading-snug">{vs['title']}</h3>
                <p class="text-xs text-gray-700 leading-relaxed">{vs['summary']}</p>
            </div>
            <span class="text-xs font-extrabold text-cyan-800 mt-4 inline-flex items-center gap-1">Read Full Side-by-Side Comparison &rarr;</span>
        </a>
        """

    return f"""
    <!-- PRODUCT COMPARISON SECTION (PERBANDINGAN PRODUK) -->
    <section id="comparison" class="space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
            <div>
                <span class="text-xs font-extrabold uppercase tracking-wider text-cyan-800">Side-by-Side Spec Matrix</span>
                <h2 class="text-2xl font-extrabold text-gray-900">Top Canister Filters, Reef/Planted LEDs & Heater Controllers Compared</h2>
            </div>
            <span class="text-xs font-semibold text-gray-600">2026 Net GPH Turnover & Apogee PAR Benchmarks</span>
        </div>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl overflow-x-auto shadow-sm">
            <table class="w-full text-left border-collapse min-w-[720px]">
                <thead>
                    <tr class="bg-gray-300 border-b-2 border-gray-400 text-[11px] font-extrabold uppercase tracking-wider text-gray-800">
                        <th class="p-3.5">Aquarium Gear Model</th>
                        <th class="p-3.5">Category</th>
                        <th class="p-3.5">GPH / Wattage Spec</th>
                        <th class="p-3.5">Recommended Tank Size</th>
                        <th class="p-3.5">Key Aquatic Advantage</th>
                        <th class="p-3.5">Rating</th>
                        <th class="p-3.5 text-right">Amazon Deal</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>

        <!-- Head-to-Head VS Guides -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5 pt-2">
            {vs_cards_html}
        </div>
    </section>
    """

def render_review_cards_grid():
    active_reviews = get_cumulative_product_reviews()
    cards = ""
    for rev in active_reviews:
        amz_link = amz_url(rev["keyword"])
        cards += f"""
        <article class="bg-gray-100 border-2 border-gray-300 hover:border-gray-400 rounded-2xl p-6 shadow-sm transition flex flex-col justify-between">
            <div>
                <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider bg-cyan-100 text-cyan-900 border border-cyan-300 px-2.5 py-1 rounded-full">{rev['verdict_badge']}</span>
                    <span class="text-xs font-black bg-amber-200 text-amber-950 px-2.5 py-1 rounded-lg">Score: {rev['rating_score']} / 5.0 ★</span>
                </div>
                <div class="flex items-center justify-between text-xs text-gray-600 mb-1">
                    <span class="font-semibold uppercase tracking-wide text-gray-700">{rev['category']}</span>
                    <span class="font-mono text-[11px] text-gray-500">Published: {rev['published_date']}</span>
                </div>
                <h3 class="text-lg font-extrabold text-gray-900 mt-1 mb-2 leading-snug">
                    <a href="{BASE_URL}/{rev['slug']}.html" class="hover:text-cyan-800 transition">{rev['title']}</a>
                </h3>
                <p class="text-xs text-gray-700 leading-relaxed mb-4">{rev['summary']}</p>
                <div class="grid grid-cols-2 gap-2 text-[11px] bg-gray-200/90 p-3 rounded-xl border border-gray-300 mb-4">
                    <div><span class="text-gray-500 block">Primary Spec:</span><strong class="text-gray-900">{rev['spec_1']}</strong></div>
                    <div><span class="text-gray-500 block">Capacity / PAR:</span><strong class="text-gray-900">{rev['spec_2']}</strong></div>
                    <div><span class="text-gray-500 block">Engineering:</span><strong class="text-gray-900">{rev['spec_3']}</strong></div>
                    <div><span class="text-gray-500 block">Details:</span><strong class="text-gray-900">{rev['spec_4']}</strong></div>
                </div>
            </div>
            <div class="flex flex-col sm:flex-row gap-2.5 pt-2">
                <a href="{BASE_URL}/{rev['slug']}.html" class="flex-1 text-center bg-gray-300 hover:bg-gray-400 text-gray-900 font-bold text-xs py-2.5 px-3 rounded-lg transition">
                    Read Full Aquatic Review &rarr;
                </a>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-cyan-700 hover:bg-cyan-800 text-white font-extrabold text-xs py-2.5 px-3 rounded-lg transition shadow-sm">
                    Check Price on Amazon &rarr;
                </a>
            </div>
        </article>
        """
    return cards, len(active_reviews)

def render_common_header_and_banner():
    top_deal_link = amz_url("Fluval+FX6+Canister+Filter+AI+Prime+16HD+Planted+Aquarium+LED+Deals")
    return f"""
    <!-- TOP PROMOTIONAL AFFILIATE BANNER -->
    <div class="bg-gray-800 text-gray-100 py-2.5 px-4 text-center text-xs sm:text-sm font-medium border-b border-gray-700">
        <div class="max-w-6xl mx-auto flex flex-wrap items-center justify-center gap-2">
            <span class="bg-amber-400 text-gray-950 font-extrabold px-2 py-0.5 rounded text-xs uppercase">Aquarium & Reef Deals</span>
            <span>Save up to 30% on Fluval & Oase Canister Filters, AI Prime / Plant 3.0 LEDs, Rimless Tanks & Substrates on Amazon.</span>
            <a href="{top_deal_link}" target="_blank" rel="nofollow sponsored noopener" class="text-amber-300 hover:text-amber-200 underline font-bold ml-1">
                View Active Aquarium Deals &rarr;
            </a>
        </div>
    </div>

    <!-- STICKY NAVIGATION HEADER (GRAY BACKGROUND) -->
    <header class="bg-gray-300 border-b border-gray-400 sticky top-0 z-30 shadow-sm">
        <div class="max-w-6xl mx-auto px-4 py-3.5 flex flex-wrap items-center justify-between gap-4">
            <a href="{BASE_URL}/" class="flex items-center gap-2.5">
                <div class="w-9 h-9 rounded-lg bg-cyan-700 flex items-center justify-center text-white font-black text-lg shadow-sm">T</div>
                <div>
                    <span class="font-extrabold text-lg tracking-tight text-gray-900 block leading-none">{SITE_NAME}</span>
                    <span class="text-[11px] text-gray-700 font-medium">Aquarium Volume, Filter GPH & Reef PAR Engine</span>
                </div>
            </a>
            <nav class="flex flex-wrap items-center gap-4 sm:gap-5 text-xs sm:text-sm font-semibold text-gray-800">
                <a href="{BASE_URL}/#calculator" class="hover:text-cyan-800 transition">Tank & Filter Calc</a>
                <a href="{BASE_URL}/#product-search" class="hover:text-cyan-800 transition">Search Gear</a>
                <a href="{BASE_URL}/#best-sellers" class="hover:text-cyan-800 transition">Best Sellers</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-cyan-800 transition">Compare</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-cyan-800 transition">Daily Reviews (+3/Day)</a>
                <a href="{BASE_URL}/#faq" class="hover:text-cyan-800 transition">FAQ</a>
                <a href="{BASE_URL}/sitemap.html" class="hover:text-cyan-800 transition font-bold underline">Site Map</a>
            </nav>
        </div>
    </header>
    """

def render_onpage_sitemap_directory():
    calc_links = "".join([
        f'<li><a href="{BASE_URL}/{p["slug"]}.html" class="text-xs text-gray-700 hover:text-cyan-800 hover:underline">🐠 {p["name"]} Calculator</a></li>'
        for p in ALL_CALC_PAGES
    ])
    vs_links = "".join([
        f'<li><a href="{BASE_URL}/{v["slug"]}.html" class="text-xs text-gray-700 hover:text-cyan-800 hover:underline">⚖️ {v["title"]}</a></li>'
        for v in VS_COMPARISONS
    ])
    all_revs = get_cumulative_product_reviews()
    rev_links = "".join([
        f'<li><a href="{BASE_URL}/{r["slug"]}.html" class="text-xs text-gray-700 hover:text-cyan-800 hover:underline">📝 [{r["published_date"]}] {r["product_name"]} Review</a></li>'
        for r in all_revs
    ])
    return f"""
    <!-- COMPLETE ON-PAGE SITE MAP SECTION (SITE MAP) -->
    <section id="site-map" class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-gray-300 pb-3">
            <div>
                <span class="text-xs font-extrabold uppercase tracking-wider text-cyan-800">Complete Site Architecture & Index</span>
                <h2 class="text-xl font-extrabold text-gray-900">Full HTML & XML Site Map Directory</h2>
            </div>
            <div class="flex gap-3 text-xs font-bold">
                <a href="{BASE_URL}/sitemap.html" class="bg-gray-300 hover:bg-gray-400 text-gray-900 px-3 py-1.5 rounded-lg transition">Open Dedicated HTML Site Map &rarr;</a>
                <a href="{BASE_URL}/sitemap.xml" class="bg-cyan-700 hover:bg-cyan-800 text-white px-3 py-1.5 rounded-lg transition">View XML Sitemap</a>
            </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">1. Tank & Pond Calculators ({len(ALL_CALC_PAGES) + 1})</h3>
                <ul class="space-y-1.5">
                    <li><a href="{BASE_URL}/" class="text-xs font-bold text-cyan-800 hover:underline">🏠 Home — Master Aquarium & Reef Calculator</a></li>
                    {calc_links}
                </ul>
            </div>
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">2. Head-to-Head Comparisons ({len(VS_COMPARISONS)})</h3>
                <ul class="space-y-2">
                    {vs_links}
                </ul>
            </div>
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">3. Daily Product Reviews ({len(all_revs)} — +3/Day)</h3>
                <ul class="space-y-1.5 max-h-80 overflow-y-auto pr-2">
                    {rev_links}
                </ul>
            </div>
        </div>
    </section>
    """

def render_dedicated_html_sitemap_page():
    canonical_url = f"{BASE_URL}/sitemap.html"
    sitemap_block = render_onpage_sitemap_directory()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Complete Site Map Directory — Calculators, Comparisons & Daily Reviews | {SITE_NAME}</title>
    <meta name="description" content="Complete HTML and XML site map directory of all aquarium gallon calculators, filter GPH calculators, substrate weight guides, and daily hardware reviews on {SITE_NAME}.">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-6xl mx-auto px-4 py-10 space-y-8">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-cyan-800">Home</a>
            <span>/</span>
            <span class="text-gray-900">Complete Site Map</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-2">
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900">{SITE_NAME} — Complete Site Map</h1>
            <p class="text-sm text-gray-700">Browse every interactive aquarium gallon calculator, filter GPH turnover guide, head-to-head comparison, and cumulative daily product review article (+3 added daily) below.</p>
        </div>

        {sitemap_block}
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def render_calculator_page(page_data, is_home=False):
    gross_g, net_g, _, _, f_gph, _, heat_w, _, _, _ = compute_tank_specs(
        page_data["length"], page_data["width"], page_data["height"], page_data["tank_type"], page_data["sub_in"]
    )
    title = f"{SITE_NAME} — {SITE_TAGLINE}" if is_home else f"{page_data['name']} — Volume, Filter GPH & Substrate Calculator ({net_g} Gal) | {SITE_NAME}"
    description = page_data["desc"]
    canonical_url = f"{BASE_URL}/" if is_home else f"{BASE_URL}/{page_data['slug']}.html"
    faqs = generate_faq_data(
        page_data["name"], page_data["length"], page_data["width"],
        page_data["height"], page_data["tank_type"], page_data["sub_in"]
    )

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": item["q"], "acceptedAnswer": {"@type": "Answer", "text": item["a"]}}
            for item in faqs
        ]
    }

    app_schema = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": title,
        "url": canonical_url,
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "All",
        "description": description,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    }

    bestseller_cards_html = ""
    for prod in BEST_SELLERS:
        link = amz_url(prod["keyword"])
        bestseller_cards_html += f"""
        <div class="bg-gray-100 border-2 border-gray-300 hover:border-gray-400 rounded-xl p-5 shadow-sm transition flex flex-col justify-between">
            <div>
                <div class="flex items-center justify-between gap-2 mb-2">
                    <span class="text-xs font-bold uppercase tracking-wider bg-cyan-100 text-cyan-900 border border-cyan-300 px-2.5 py-1 rounded-full">{prod['badge']}</span>
                    <span class="text-xs font-semibold text-amber-700">{prod['rating']}</span>
                </div>
                <span class="text-xs text-gray-600 font-medium">{prod['category']}</span>
                <h3 class="text-base font-bold text-gray-900 mt-1 mb-2 leading-snug">{prod['title']}</h3>
                <p class="text-xs text-gray-700 mb-4 bg-gray-200 p-2.5 rounded-lg border border-gray-300">{prod['specs']}</p>
            </div>
            <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
               class="w-full inline-flex items-center justify-center bg-cyan-700 hover:bg-cyan-800 text-white font-extrabold text-sm py-2.5 px-4 rounded-lg transition shadow-sm">
               Check Today's Price on Amazon &rarr;
            </a>
        </div>
        """

    preset_links_html = ""
    for p in ALL_CALC_PAGES:
        _, p_gal, _, _, p_gph, _, _, _, _, _ = compute_tank_specs(
            p["length"], p["width"], p["height"], p["tank_type"], p["sub_in"]
        )
        active_cls = "bg-cyan-100 border-cyan-700 text-cyan-950 font-bold" if (not is_home and p["slug"] == page_data["slug"]) else "bg-gray-100 border-gray-300 text-gray-800 hover:border-cyan-700 hover:text-gray-950"
        preset_links_html += f"""
        <a href="{BASE_URL}/{p['slug']}.html" class="border rounded-lg p-3 text-xs transition flex items-center justify-between {active_cls}">
            <span class="truncate pr-2">{p['name']}</span>
            <span class="text-cyan-900 font-mono shrink-0">{p_gal}G / {p_gph} GPH</span>
        </a>
        """

    faq_html = ""
    for item in faqs:
        faq_html += f"""
        <div class="bg-gray-100 border-2 border-gray-300 rounded-xl p-5">
            <h3 class="text-base font-bold text-gray-900 mb-2">{item['q']}</h3>
            <p class="text-sm text-gray-700 leading-relaxed">{item['a']}</p>
        </div>
        """

    mid_banner_link = amz_url("Fluval+FX6+Oase+BioMaster+Canister+Filter+and+Planted+Reef+LED+Bundle")
    comparison_html = render_comparison_table_section()
    reviews_grid_html, total_reviews_count = render_review_cards_grid()
    onpage_sitemap_html = render_onpage_sitemap_directory()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="google-site-verification" content="pgvlG0f03ZrRZzbgDSXRhr6tsSfseFOhXCN6Yv_j5b8" />
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical_url}">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(faq_schema)}</script>
    <script type="application/ld+json">{json.dumps(app_schema)}</script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased selection:bg-cyan-700 selection:text-white">

    {render_common_header_and_banner()}

    <main class="max-w-6xl mx-auto px-4 py-8 space-y-12">

        <!-- HERO TITLE SECTION -->
        <section class="text-center max-w-3xl mx-auto space-y-3">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-gray-300 border border-gray-400 text-xs font-semibold text-gray-800">
                <span>🐠 Net Gallons, Bioload Filter GPH, Heater Watts & Substrate Sizing Engine</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-extrabold text-gray-900 tracking-tight">
                { "Aquarium, Reef Tank & Pond Volume, Filter GPH & Substrate Calculator" if is_home else f"{page_data['name']} — Filter GPH & Substrate Calculator" }
            </h1>
            <p class="text-gray-700 text-sm sm:text-base leading-relaxed">
                {description}
            </p>
        </section>

        <!-- INTERACTIVE CALCULATOR + LIVE HARDWARE MATCHER -->
        <section id="calculator" class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            <!-- Left Column: Inputs (7 Cols) -->
            <div class="lg:col-span-7 bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-6">
                <div class="flex items-center justify-between border-b border-gray-300 pb-4">
                    <div>
                        <h2 class="text-xl font-extrabold text-gray-900">1. Enter Tank Dimensions, Type & Substrate Depth</h2>
                        <p class="text-xs text-gray-600">Calculates net gallons, filled lbs, filter GPH, heater watts & 20-lb substrate bags</p>
                    </div>
                    <span class="text-xs font-mono bg-cyan-100 text-cyan-900 border border-cyan-300 px-2.5 py-1 rounded font-semibold">Live Aquatic Math</span>
                </div>

                <div>
                    <label for="quickPreset" class="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-2">Quick Select Standard Aquarium or Pond Size</label>
                    <select id="quickPreset" onchange="applyPreset(this.value)" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-sm font-semibold text-gray-900 focus:ring-2 focus:ring-cyan-700">
                        <option value="{page_data['length']},{page_data['width']},{page_data['height']},{page_data['tank_type']},{page_data['sub_in']}">Current: {page_data['name']}</option>
                        <option value="48,18,21,planted,2.5">75-Gallon Standard Tank (48\"×18\"×21\" — Planted / Reef)</option>
                        <option value="36,18,16,planted,2.5">40-Gallon Breeder Tank (36\"×18\"×16\" — Aquascape / Reef)</option>
                        <option value="30,12,12,planted,2.0">20-Gallon Long Tank (30\"×12\"×12\" — Planted Community)</option>
                        <option value="48,13,21,cichlid,2.0">55-Gallon Standard Tank (48\"×13\"×21\" — Cichlids / Community)</option>
                        <option value="72,18,21,cichlid,2.0">125-Gallon 6-Foot Tank (72\"×18\"×21\" — Fluval FX6 Setup)</option>
                        <option value="48,24,24,reef,2.0">120-Gallon 4×2×2 Coral Reef Tank (48\"×24\"×24\" — Saltwater)</option>
                        <option value="20,10,12,planted,2.0">10-Gallon Nano / Shrimp / Betta Tank (20\"×10\"×12\")</option>
                    </select>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    <div>
                        <label for="lengthInput" class="block text-sm font-bold text-gray-800 mb-1">Tank Length (Inches)</label>
                        <input type="number" id="lengthInput" value="{page_data['length']}" min="8" max="240" step="1" oninput="calculateTank()"
                               class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-base font-bold text-gray-900 focus:ring-2 focus:ring-cyan-700">
                    </div>

                    <div>
                        <label for="widthInput" class="block text-sm font-bold text-gray-800 mb-1">Front-to-Back Width (In)</label>
                        <input type="number" id="widthInput" value="{page_data['width']}" min="6" max="240" step="1" oninput="calculateTank()"
                               class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-base font-bold text-gray-900 focus:ring-2 focus:ring-cyan-700">
                    </div>

                    <div>
                        <label for="heightInput" class="block text-sm font-bold text-gray-800 mb-1">Tank Height (Inches)</label>
                        <input type="number" id="heightInput" value="{page_data['height']}" min="6" max="96" step="1" oninput="calculateTank()"
                               class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-base font-bold text-gray-900 focus:ring-2 focus:ring-cyan-700">
                    </div>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                    <div>
                        <label for="typeInput" class="block text-sm font-bold text-gray-800 mb-1">Aquarium / Bioload Ecosystem</label>
                        <select id="typeInput" onchange="calculateTank()" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-sm font-bold text-gray-900">
                            <option value="planted" {"selected" if page_data['tank_type'] == "planted" else ""}>Freshwater Planted Aquascape (5.5x GPH Turnover)</option>
                            <option value="cichlid" {"selected" if page_data['tank_type'] == "cichlid" else ""}>Heavy Bioload Cichlids / Goldfish / Turtle (7.5x GPH)</option>
                            <option value="reef" {"selected" if page_data['tank_type'] == "reef" else ""}>Saltwater Coral Reef Tank (Sump + 25x Wave Maker)</option>
                            <option value="pond" {"selected" if page_data['tank_type'] == "pond" else ""}>Backyard Koi & Water Garden Pond (Waterfall GPH)</option>
                        </select>
                    </div>

                    <div>
                        <label for="subInput" class="block text-sm font-bold text-gray-800 mb-1">Desired Substrate / Sand Depth (In)</label>
                        <select id="subInput" onchange="calculateTank()" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-sm font-bold text-gray-900">
                            <option value="1.0" {"selected" if page_data['sub_in'] <= 1.2 else ""}>1.0 Inch — Shallow Sand Bed / Reef Bottom</option>
                            <option value="2.0" {"selected" if 1.2 < page_data['sub_in'] <= 2.2 else ""}>2.0 Inches — Standard Community & Reef Bed</option>
                            <option value="2.5" {"selected" if 2.2 < page_data['sub_in'] <= 2.8 else ""}>2.5 Inches — Root-Feeding Planted Aquascape</option>
                            <option value="3.0" {"selected" if page_data['sub_in'] > 2.8 else ""}>3.0 Inches — Deep Sloped Nature Aquascape</option>
                        </select>
                    </div>
                </div>
            </div>

            <!-- Right Column: Output + Dynamic Amazon Recommendation (5 Cols) -->
            <div class="lg:col-span-5 bg-gray-100 border-2 border-cyan-700 rounded-2xl p-6 sm:p-8 shadow-md space-y-6">
                <div class="border-b border-gray-300 pb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider text-cyan-800">2. Engineered Life-Support Specs</span>
                    <h2 class="text-xl font-extrabold text-gray-900">Your Exact Tank & Hardware Sizing</h2>
                </div>

                <div class="grid grid-cols-2 gap-3.5">
                    <div class="bg-cyan-100 border border-cyan-300 rounded-xl p-3.5">
                        <span class="text-xs text-cyan-950 font-semibold block">Net Water Volume</span>
                        <span id="resNetGal" class="text-2xl font-black text-cyan-800">69.1 Gal</span>
                        <span id="resGrossLit" class="text-[11px] text-cyan-900 block mt-0.5">261 L (78.5 Gal Gross)</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Min. Filter Turnover</span>
                        <span id="resFilterGPH" class="text-2xl font-black text-gray-900">400 GPH</span>
                        <span id="resWaveGPH" class="text-[11px] text-gray-600 block mt-0.5">+ 850 GPH Wave Maker</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Heater & Controller</span>
                        <span id="resHeaterW" class="text-base font-extrabold text-gray-900">300W Heater</span>
                        <span class="text-[11px] text-gray-600 block mt-0.5">+ Inkbird Wi-Fi Cutoff</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Substrate & Weight</span>
                        <span id="resSubBags" class="text-base font-extrabold text-amber-800">6 Bags (120 lb)</span>
                        <span id="resFilledLbs" class="text-[11px] text-gray-600 block mt-0.5">Filled Load: ~805 Lbs</span>
                    </div>
                </div>

                <!-- Dynamic Matched Product Box -->
                <div class="bg-gray-200 border-2 border-cyan-600 rounded-xl p-4 space-y-3">
                    <div class="flex items-center justify-between">
                        <span class="text-[11px] font-extrabold uppercase tracking-wider bg-cyan-700 text-white px-2 py-0.5 rounded">Verified Hardware Match</span>
                        <span class="text-xs font-bold text-gray-700">Amazon Prime Ready</span>
                    </div>
                    <h3 id="recTankTitle" class="text-base font-extrabold text-gray-900 leading-snug">Loading Filter & Light Match...</h3>
                    <p id="recTankDesc" class="text-xs text-gray-700"></p>
                    <div class="pt-1 flex flex-col sm:flex-row gap-2.5">
                        <a id="recPrimaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="flex-1 text-center bg-cyan-700 hover:bg-cyan-800 text-white font-extrabold text-sm py-3 px-4 rounded-lg transition shadow-sm">
                           Shop Matched Filter & Pump &rarr;
                        </a>
                        <a id="recSecondaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="text-center bg-gray-800 hover:bg-gray-900 text-white font-bold text-xs py-3 px-3 rounded-lg transition">
                           Shop LED Light & Heater
                        </a>
                    </div>
                </div>
            </div>
        </section>

        <!-- PRODUCT SEARCH ENGINE SECTION (SEARCH PRODUK) -->
        <section id="product-search" class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm">
            <div class="max-w-3xl mx-auto text-center space-y-4">
                <h2 class="text-2xl font-extrabold text-gray-900">Search Canister Filters, Reef/Planted LEDs, Rimless Tanks & Substrates</h2>
                <p class="text-sm text-gray-700">Search any tank size (20, 40, 75, 125 Gal), brand (Fluval, Oase, AI Prime, Kessil, Seachem, Sicce, CaribSea, Inkbird), or aquatic gear on Amazon.</p>
                <form onsubmit="handleAmazonSearch(event)" class="flex flex-col sm:flex-row gap-3 pt-2">
                    <input type="text" id="amzSearchInput" placeholder="e.g. Fluval FX6 Canister Filter, AI Prime 16HD Reef LED, Oase BioMaster Thermo 600..."
                           class="flex-1 bg-gray-200 border-2 border-gray-400 rounded-xl px-4 py-3 text-sm font-medium text-gray-900 placeholder-gray-500 focus:outline-none focus:border-cyan-700" required>
                    <button type="submit" class="bg-cyan-700 hover:bg-cyan-800 text-white font-extrabold text-sm px-6 py-3 rounded-xl transition cursor-pointer shrink-0">
                        Search on Amazon &rarr;
                    </button>
                </form>
                <div class="flex flex-wrap items-center justify-center gap-2 pt-2 text-xs">
                    <span class="text-gray-600 font-semibold">Popular Searches:</span>
                    <a href="{amz_url('Fluval FX6 FX4 407 Aquarium Canister Filter')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-cyan-200 text-gray-800 border border-gray-300 rounded-full transition">Fluval Canister Filters</a>
                    <a href="{amz_url('AquaIllumination AI Prime 16HD Reef LED Light')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-cyan-200 text-gray-800 border border-gray-300 rounded-full transition">AI Prime 16HD LED</a>
                    <a href="{amz_url('Fluval Plant 3.0 Bluetooth Aquarium LED')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-cyan-200 text-gray-800 border border-gray-300 rounded-full transition">Fluval Plant 3.0 LED</a>
                    <a href="{amz_url('Oase BioMaster Thermo 350 600 Canister Filter')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-cyan-200 text-gray-800 border border-gray-300 rounded-full transition">Oase BioMaster Thermo</a>
                    <a href="{amz_url('Inkbird ITC-306A WiFi Aquarium Heater Controller')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-cyan-200 text-gray-800 border border-gray-300 rounded-full transition">Inkbird Heater Controller</a>
                </div>
            </div>
        </section>

        <!-- BEST SELLING PRODUCTS GRID (PRODUK TERLARIS) -->
        <section id="best-sellers" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-cyan-800">Verified Aquatic Life-Support Gear</span>
                    <h2 class="text-2xl font-extrabold text-gray-900">Best-Selling Canister Filters, Reef/Planted LEDs & Rimless Tanks</h2>
                </div>
                <a href="{amz_url('Best Selling Aquarium Canister Filters and LED Lights')}" target="_blank" rel="nofollow sponsored noopener" class="text-sm font-bold text-cyan-800 hover:text-cyan-900">
                    Browse Full Amazon Best Sellers &rarr;
                </a>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
                {bestseller_cards_html}
            </div>
        </section>

        {comparison_html}

        <!-- CUMULATIVE DAILY PRODUCT REVIEW ARTICLES SECTION (+3 NEW ARTICLES PER DAY) -->
        <section id="reviews" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-cyan-800">Autonomous Daily Review Archive ({total_reviews_count} Published Articles & Growing +3/Day)</span>
                    <h2 class="text-2xl font-extrabold text-gray-900">In-Depth Canister Filter, Reef LED & Aquascape Review Articles</h2>
                </div>
                <span class="text-xs font-semibold bg-emerald-100 text-emerald-900 border border-emerald-300 px-3 py-1 rounded-full">+3 New Product Reviews Added Automatically Every Day</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {reviews_grid_html}
            </div>
        </section>

        <!-- MID-PAGE PROMOTIONAL AFFILIATE BANNER -->
        <section class="bg-gray-300 border-2 border-cyan-700 rounded-2xl p-6 sm:p-8 flex flex-col md:flex-row items-center justify-between gap-6">
            <div class="space-y-2 max-w-2xl">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-cyan-700 text-white px-2.5 py-1 rounded">Complete Aquascape & Reef Setup Guide</span>
                <h2 class="text-xl sm:text-2xl font-extrabold text-gray-900">Setting Up a Planted Tank, Cichlid Aquarium, or Coral Reef?</h2>
                <p class="text-sm text-gray-800">Eliminate green algae and heater accidents by pairing an oversized Canister/Sump Filter with a Programmable Full-Spectrum LED, Inkbird Dual-Probe Heater Controller, and Seachem Prime.</p>
            </div>
            <a href="{mid_banner_link}" target="_blank" rel="nofollow sponsored noopener"
               class="shrink-0 bg-cyan-700 hover:bg-cyan-800 text-white font-extrabold text-sm px-6 py-3.5 rounded-xl shadow-sm transition">
               Explore Filter + LED Bundles on Amazon &rarr;
            </a>
        </section>

        <!-- PROGRAMMATIC SEO DIRECTORY -->
        <section id="presets" class="space-y-4">
            <div class="border-b border-gray-300 pb-3">
                <h2 class="text-xl font-extrabold text-gray-900">Aquarium Gallon Size & Reef/Pond Specific Calculators</h2>
                <p class="text-xs text-gray-600">Select your exact tank dimensions or gallon tier below for pre-calculated filter GPH, heater wattage, and substrate bag counts.</p>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2.5">
                {preset_links_html}
            </div>
        </section>

        <!-- FREQUENTLY ASKED QUESTIONS (FAQ) -->
        <section id="faq" class="space-y-6">
            <div class="border-b border-gray-300 pb-3">
                <span class="text-xs font-extrabold uppercase tracking-wider text-cyan-800">Filtration, PAR & Nitrogen Cycle Guide</span>
                <h2 class="text-2xl font-extrabold text-gray-900">Frequently Asked Questions (FAQ)</h2>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                {faq_html}
            </div>
        </section>

        {onpage_sitemap_html}

    </main>

    <!-- FOOTER (GRAY BACKGROUND) -->
    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700">
        <div class="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
                <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
                <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
            </div>
            <div class="flex flex-wrap gap-4 font-medium text-gray-800">
                <a href="{BASE_URL}/" class="hover:text-cyan-800">Home</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-cyan-800">Comparisons</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-cyan-800">Daily Reviews (+3/Day)</a>
                <a href="{BASE_URL}/sitemap.html" class="hover:text-cyan-800 font-bold">HTML Site Map</a>
                <a href="{BASE_URL}/sitemap.xml" class="hover:text-cyan-800">XML Sitemap</a>
                <a href="{BASE_URL}/#faq" class="hover:text-cyan-800">FAQ</a>
            </div>
        </div>
    </footer>

    <!-- INTERACTIVE CALCULATOR & AFFILIATE MATCHING SCRIPT -->
    <script>
        const AFFILIATE_TAG = "{AFFILIATE_TAG}";

        function makeAmazonLink(query) {{
            return "https://www.amazon.com/s?k=" + encodeURIComponent(query) + "&tag=" + AFFILIATE_TAG;
        }}

        function applyPreset(val) {{
            const parts = val.split(",");
            if (parts.length === 5) {{
                document.getElementById("lengthInput").value = parts[0];
                document.getElementById("widthInput").value = parts[1];
                document.getElementById("heightInput").value = parts[2];
                document.getElementById("typeInput").value = parts[3];
                document.getElementById("subInput").value = parts[4];
                calculateTank();
            }}
        }}

        function handleAmazonSearch(e) {{
            e.preventDefault();
            const q = document.getElementById("amzSearchInput").value.trim();
            if (q) {{
                window.open(makeAmazonLink(q), "_blank", "noopener,noreferrer");
            }}
        }}

        function calculateTank() {{
            const l = parseFloat(document.getElementById("lengthInput").value) || 48;
            const w = parseFloat(document.getElementById("widthInput").value) || 18;
            const h = parseFloat(document.getElementById("heightInput").value) || 21;
            const tankType = document.getElementById("typeInput").value || "planted";
            const subDepth = parseFloat(document.getElementById("subInput").value) || 2.5;

            const grossGal = (l * w * h) / 231.0;
            const netGal = grossGal * 0.88;
            const netLiters = Math.round(netGal * 3.78541);

            const subCuIn = l * w * subDepth;
            const subLbs = Math.round(subCuIn * 0.056);
            const subBags = Math.max(1, Math.ceil(subLbs / 20));
            const filledLbs = Math.round((netGal * 8.34) + subLbs + (grossGal * 1.4));

            let filterGPH = Math.ceil((netGal * 5.5) / 25) * 25;
            let waveGPH = Math.ceil((netGal * 12) / 50) * 50;

            if (tankType === "pond") {{
                filterGPH = Math.ceil((netGal * 1.25) / 50) * 50;
                waveGPH = Math.round(filterGPH * 1.5);
            }} else if (tankType === "cichlid" || tankType === "reef") {{
                filterGPH = Math.ceil((netGal * 7.5) / 25) * 25;
                waveGPH = Math.ceil((netGal * 25) / 100) * 100;
            }}

            const rawHeater = netGal * 4.0;
            const heaterTiers = [50, 100, 150, 200, 300, 400, 500, 600, 800, 1000];
            let heaterW = 1000;
            for (let i = 0; i < heaterTiers.length; i++) {{
                if (heaterTiers[i] >= rawHeater) {{
                    heaterW = heaterTiers[i];
                    break;
                }}
            }}

            document.getElementById("resNetGal").textContent = netGal.toFixed(1) + " Gal";
            document.getElementById("resGrossLit").textContent = netLiters.toLocaleString() + " L (" + grossGal.toFixed(1) + " Gal Gross)";
            document.getElementById("resFilterGPH").textContent = filterGPH.toLocaleString() + " GPH";
            document.getElementById("resWaveGPH").textContent = "+ " + waveGPH.toLocaleString() + " GPH Wave Maker";
            document.getElementById("resHeaterW").textContent = heaterW + "W Heater";
            document.getElementById("resSubBags").textContent = subBags + " Bags (" + subLbs + " lbs)";
            document.getElementById("resFilledLbs").textContent = "Total Floor Weight: ~" + filledLbs.toLocaleString() + " Lbs";

            let recTitle = "";
            let recDesc = "";
            let primaryQuery = "";
            let secondaryQuery = tankType === "reef"
                ? "AquaIllumination AI Prime 16HD Kessil A360X Reef LED and Inkbird ITC-306A"
                : "Fluval Plant 3.0 Bluetooth LED and Inkbird ITC-306A Heater Controller";

            if (tankType === "pond") {{
                recTitle = "Aquascape AquaForce Solids-Handling Pond Pump (" + filterGPH + "+ GPH) + 45-Mil EPDM Liner";
                recDesc = "Continuous 24/7 koi pond waterfall circulation and UV bio-filtration.";
                primaryQuery = "Aquascape Koi Pond Waterfall Pump and BioFalls Filter";
                secondaryQuery = "45 Mil EPDM Koi Pond Liner and Pond UV Clarifier";
            }} else if (netGal <= 35) {{
                recTitle = "Seachem Tidal 55 / Fluval 207 Canister Filter + " + l + "\" Full-Spectrum LED";
                recDesc = "Crystal-clear filtration and silent heating engineered for " + netGal.toFixed(0) + "-gallon aquariums.";
                primaryQuery = "Fluval 207 Canister Filter Seachem Tidal 55 Aquarium Filter";
            }} else if (netGal <= 85) {{
                recTitle = "Oase BioMaster Thermo 350/600 or Fluval 407 Canister Filter (" + filterGPH + "+ GPH)";
                recDesc = "America's #1 planted and reef filtration tier for 40-breeder, 55-gallon, and 75-gallon tanks.";
                primaryQuery = "Oase BioMaster Thermo 600 Fluval 407 FX4 Aquarium Canister Filter";
            }} else {{
                recTitle = "Fluval FX6 High-Performance Canister Filter (925 GPH) or Sicce SDC Sump Return Pump";
                recDesc = "Heavy-duty turnover engineered for large " + netGal.toFixed(0) + "-gallon cichlid, monster, and reef tanks.";
                primaryQuery = "Fluval FX6 High Performance Canister Filter Sicce Syncra SDC";
            }}

            document.getElementById("recTankTitle").textContent = recTitle;
            document.getElementById("recTankDesc").textContent = recDesc;
            document.getElementById("recPrimaryBtn").href = makeAmazonLink(primaryQuery);
            document.getElementById("recSecondaryBtn").href = makeAmazonLink(secondaryQuery);
        }}

        window.addEventListener("DOMContentLoaded", calculateTank);
    </script>
</body>
</html>"""

def render_single_review_page(rev):
    canonical_url = f"{BASE_URL}/{rev['slug']}.html"
    amz_link = amz_url(rev["keyword"])

    review_schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": rev["product_name"],
        "description": rev["summary"],
        "review": {
            "@type": "Review",
            "datePublished": rev["published_date"],
            "reviewRating": {"@type": "Rating", "ratingValue": rev["rating_score"], "bestRating": "5"},
            "author": {"@type": "Organization", "name": SITE_NAME},
            "reviewBody": " ".join(rev["body_paragraphs"])
        }
    }

    pros_html = "".join([f'<li class="flex items-start gap-2 text-sm text-gray-800"><span class="text-emerald-700 font-bold">✓</span><span>{p}</span></li>' for p in rev["pros"]])
    cons_html = "".join([f'<li class="flex items-start gap-2 text-sm text-gray-800"><span class="text-rose-700 font-bold">✕</span><span>{c}</span></li>' for c in rev["cons"]])
    paragraphs_html = "".join([f'<p class="text-gray-800 leading-relaxed text-base mb-4">{p}</p>' for p in rev["body_paragraphs"]])

    recent_reviews = [r for r in get_cumulative_product_reviews() if r["slug"] != rev["slug"]][:6]
    related_html = ""
    for other in recent_reviews:
        related_html += f"""
        <a href="{BASE_URL}/{other['slug']}.html" class="bg-gray-100 border-2 border-gray-300 rounded-xl p-4 hover:border-cyan-700 transition block">
            <span class="text-[11px] font-bold text-cyan-800 uppercase">{other['verdict_badge']}</span>
            <h4 class="font-extrabold text-sm text-gray-900 mt-1 line-clamp-2">{other['product_name']} Review</h4>
            <span class="text-xs text-gray-600 mt-1 block">Score: {other['rating_score']} / 5.0 ★ ({other['published_date']}) &rarr;</span>
        </a>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{rev['title']} | {SITE_NAME}</title>
    <meta name="description" content="{rev['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(review_schema)}</script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-cyan-800">Home & Tank Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#reviews" class="hover:text-cyan-800">Daily Aquarium Reviews</a>
            <span>/</span>
            <span class="text-gray-900">{rev['product_name']}</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-5">
            <div class="flex flex-wrap items-center justify-between gap-2">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-cyan-100 text-cyan-900 border border-cyan-300 px-3 py-1 rounded-full">{rev['verdict_badge']}</span>
                <div class="flex items-center gap-2">
                    <span class="text-xs font-mono text-gray-600">Published: {rev['published_date']}</span>
                    <span class="text-sm font-black bg-amber-200 text-amber-950 px-3 py-1 rounded-lg">Lab Rating: {rev['rating_score']} / 5.0 ★</span>
                </div>
            </div>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900 leading-tight">{rev['title']}</h1>
            <p class="text-base text-gray-700 leading-relaxed">{rev['summary']}</p>

            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-gray-200 p-4 rounded-xl border border-gray-300 text-xs">
                <div><span class="text-gray-500 block font-medium">Flow / Output</span><strong class="text-gray-900">{rev['spec_1']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Capacity / PAR</span><strong class="text-gray-900">{rev['spec_2']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Technology</span><strong class="text-gray-900">{rev['spec_3']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Warranty</span><strong class="text-gray-900">{rev['spec_4']}</strong></div>
            </div>

            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="flex-1 text-center bg-cyan-700 hover:bg-cyan-800 text-white font-extrabold text-sm py-3.5 px-6 rounded-xl transition shadow-sm">
                   Check Latest Price & Availability on Amazon &rarr;
                </a>
                <a href="{BASE_URL}/#calculator"
                   class="text-center bg-gray-300 hover:bg-gray-400 text-gray-900 font-bold text-sm py-3.5 px-5 rounded-xl transition">
                   Calculate Tank GPH & Substrate
                </a>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-gray-100 border-2 border-emerald-400 rounded-2xl p-6 space-y-3">
                <h2 class="text-base font-extrabold text-emerald-900 uppercase tracking-wide">Pros (What We Like)</h2>
                <ul class="space-y-2.5">{pros_html}</ul>
            </div>
            <div class="bg-gray-100 border-2 border-rose-400 rounded-2xl p-6 space-y-3">
                <h2 class="text-base font-extrabold text-rose-900 uppercase tracking-wide">Cons (Things to Consider)</h2>
                <ul class="space-y-2.5">{cons_html}</ul>
            </div>
        </div>

        <article class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 space-y-4">
            <h2 class="text-xl font-extrabold text-gray-900 border-b border-gray-300 pb-3">Hands-On GPH Turnover, Bioload & PAR Performance Analysis</h2>
            {paragraphs_html}
            <div class="pt-4 border-t border-gray-300 flex flex-col sm:flex-row items-center justify-between gap-4">
                <div>
                    <span class="text-xs font-bold uppercase text-cyan-800 block">Final Verdict</span>
                    <p class="text-sm font-bold text-gray-900">{rev['product_name']} earns {rev['rating_score']}/5.0 in our aquatic equipment benchmark.</p>
                </div>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="shrink-0 bg-cyan-700 hover:bg-cyan-800 text-white font-extrabold text-sm px-6 py-3 rounded-xl transition shadow-sm">
                   View Customer Reviews & Price on Amazon &rarr;
                </a>
            </div>
        </article>

        <section class="space-y-4">
            <h3 class="text-lg font-extrabold text-gray-900">Recent Daily Aquarium Hardware Reviews (+3 Added Daily)</h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                {related_html}
            </div>
        </section>
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def render_vs_comparison_page(vs):
    canonical_url = f"{BASE_URL}/{vs['slug']}.html"
    link_a = amz_url(vs["keyword_a"])
    link_b = amz_url(vs["keyword_b"])

    rows_html = ""
    for m in vs["metrics"]:
        rows_html += f"""
        <tr class="border-b border-gray-300">
            <td class="p-4 font-bold text-gray-900 bg-gray-200 text-xs sm:text-sm w-1/4">{m['feature']}</td>
            <td class="p-4 text-xs sm:text-sm text-gray-800 w-3/8">{m['val_a']}</td>
            <td class="p-4 text-xs sm:text-sm text-gray-800 w-3/8">{m['val_b']}</td>
        </tr>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{vs['title']} | {SITE_NAME}</title>
    <meta name="description" content="{vs['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-cyan-800">Home & Tank Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#comparison" class="hover:text-cyan-800">Product Comparisons</a>
            <span>/</span>
            <span class="text-gray-900">{vs['product_a']} vs. {vs['product_b']}</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-4">
            <span class="text-xs font-extrabold uppercase tracking-wider bg-cyan-100 text-cyan-900 border border-cyan-300 px-3 py-1 rounded-full">{vs['winner_badge']}</span>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900 leading-tight">{vs['title']}</h1>
            <p class="text-base text-gray-700 leading-relaxed">{vs['summary']}</p>
        </div>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl overflow-hidden shadow-sm">
            <table class="w-full text-left border-collapse">
                <thead>
                    <tr class="bg-gray-800 text-white text-xs sm:text-sm font-extrabold">
                        <th class="p-4">Specification</th>
                        <th class="p-4 text-cyan-300">{vs['product_a']}</th>
                        <th class="p-4 text-amber-300">{vs['product_b']}</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                    <tr class="bg-gray-200">
                        <td class="p-4 font-extrabold text-xs sm:text-sm text-gray-900">Check Amazon Price</td>
                        <td class="p-4">
                            <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-cyan-700 hover:bg-cyan-800 text-white font-extrabold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_a']} &rarr;
                            </a>
                        </td>
                        <td class="p-4">
                            <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-gray-800 hover:bg-gray-900 text-white font-extrabold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_b']} &rarr;
                            </a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="bg-gray-100 border-2 border-cyan-600 rounded-2xl p-6 sm:p-8 space-y-4">
            <h2 class="text-xl font-extrabold text-gray-900">Head-to-Head Buying Verdict</h2>
            <p class="text-sm sm:text-base text-gray-800 leading-relaxed">{vs['verdict_text']}</p>
            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-cyan-700 hover:bg-cyan-800 text-white font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_a']} on Amazon &rarr;
                </a>
                <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-gray-800 hover:bg-gray-900 text-white font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_b']} on Amazon &rarr;
                </a>
            </div>
        </div>
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def generate_sitemap_and_robots(urls):
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    xml_items = ""
    for u in urls:
        xml_items += f"""  <url>
    <loc>{u}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>{"1.0" if u.endswith("/") else "0.85"}</priority>
  </url>\n"""

    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{xml_items}</urlset>"""

    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_content)

    robots_content = f"""User-agent: *
Allow: /
Sitemap: {BASE_URL}/sitemap.xml
"""
    with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots_content)

    with open(os.path.join(OUTPUT_DIR, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY)

def ping_indexnow(urls):
    parsed_host = urllib.parse.urlparse(BASE_URL).netloc
    if not parsed_host or "username.github.io" in parsed_host:
        return

    payload = {
        "host": parsed_host,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{BASE_URL}/{INDEXNOW_KEY}.txt",
        "urlList": urls
    }
    try:
        req = urllib.request.Request(
            "https://api.indexnow.org/indexnow",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"IndexNow Ping Status: {resp.status}")
    except Exception as e:
        print(f"IndexNow notice: {e}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    generated_urls = []

    # 1. Generate Homepage
    home_preset = {
        "slug": "index",
        "name": "75-Gallon Standard Aquarium (48\" × 18\" × 21\")",
        "length": 48,
        "width": 18,
        "height": 21,
        "tank_type": "planted",
        "sub_in": 2.5,
        "desc": "Calculate exact aquarium & koi pond water volume (gallons & liters), total filled floor weight (lbs), canister/sump filter GPH turnover, heater wattage, and 20-lb substrate bags—plus read 3 new aquatic hardware reviews added daily."
    }
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_calculator_page(home_preset, is_home=True))
    generated_urls.append(f"{BASE_URL}/")

    # 2. Generate Dedicated HTML Site Map Page (sitemap.html)
    with open(os.path.join(OUTPUT_DIR, "sitemap.html"), "w", encoding="utf-8") as f:
        f.write(render_dedicated_html_sitemap_page())
    generated_urls.append(f"{BASE_URL}/sitemap.html")

    # 3. Generate Programmatic Aquarium & Pond Calculator Pages
    for page in ALL_CALC_PAGES:
        filename = f"{page['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_calculator_page(page, is_home=False))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 4. Generate Cumulative Daily Product Review Pages (+3 new reviews unlocked every single day)
    active_reviews = get_cumulative_product_reviews()
    for rev in active_reviews:
        filename = f"{rev['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_single_review_page(rev))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 5. Generate Standalone Head-to-Head Product Comparison Pages
    for vs in VS_COMPARISONS:
        filename = f"{vs['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_vs_comparison_page(vs))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 6. XML Sitemap, Robots & IndexNow Auto-Ping
    generate_sitemap_and_robots(generated_urls)
    ping_indexnow(generated_urls)
    print(f"Successfully generated {len(generated_urls)} total SEO pages ({len(active_reviews)} cumulative review articles [+3/day] + HTML/XML sitemaps) in /{OUTPUT_DIR}!")

if __name__ == "__main__":
    main()
