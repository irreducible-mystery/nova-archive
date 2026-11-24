#!/usr/bin/env python3
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os

OUT = os.path.expanduser("~/workspace/your_files/black-swan-essentials-checklist/black-swan-essentials-checklist.docx")
NAVY = RGBColor(0x1F, 0x3A, 0x4D)
SLATE = RGBColor(0x4A, 0x5A, 0x66)
ACCENT = "1F3A4D"

doc = Document()
doc.core_properties.title = "Black Swan Essentials Checklist"
doc.core_properties.subject = "Two weeks at home, one person, Bay Area apartment — plus a 3-day go-bag"
for s in doc.sections:
    s.top_margin = Inches(0.6); s.bottom_margin = Inches(0.6)
    s.left_margin = Inches(0.65); s.right_margin = Inches(0.65)

st = doc.styles["Normal"]
st.font.name = "Calibri"; st.font.size = Pt(10.5)
st.paragraph_format.space_after = Pt(6); st.paragraph_format.line_spacing = 1.07

def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd"); shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), hexcolor); tcPr.append(shd)

def h(text, level=1):
    p = doc.add_heading(text, level=level)
    for r in p.runs: r.font.color.rgb = NAVY
    return p

def para(text, bold_prefix=None, italic=False, size=10.5):
    p = doc.add_paragraph()
    if bold_prefix:
        r = p.add_run(bold_prefix); r.bold = True
    r = p.add_run(text); r.italic = italic; r.font.size = Pt(size)
    return p

def bullet(text, bold_prefix=None):
    p = doc.add_paragraph(style="List Bullet")
    if bold_prefix:
        r = p.add_run(bold_prefix); r.bold = True
    p.add_run(text)
    return p

def checklist_table(rows):
    t = doc.add_table(rows=1, cols=4)
    t.style = "Table Grid"; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    widths = [Inches(3.1), Inches(1.25), Inches(1.85), Inches(1.0)]
    hdr = ["\u2610  Item", "Qty (1 person)", "Notes", "Rough cost"]
    for i, txt in enumerate(hdr):
        c = t.rows[0].cells[i]; c.text = ""
        r = c.paragraphs[0].add_run(txt); r.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF); r.font.size = Pt(9.5)
        shade(c, ACCENT); c.width = widths[i]
    for item, qty, note, cost in rows:
        cells = t.add_row().cells
        for i, txt in enumerate([f"\u2610  {item}", qty, note, cost]):
            cells[i].text = ""
            r = cells[i].paragraphs[0].add_run(txt); r.font.size = Pt(9.5)
            cells[i].width = widths[i]
    doc.add_paragraph()
    return t

# ---------- Title ----------
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Black Swan Essentials Checklist"); r.bold = True; r.font.size = Pt(26); r.font.color.rgb = NAVY
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Two weeks at home \u00b7 one person \u00b7 Bay Area apartment \u2014 plus a 3-day go-bag")
r.font.size = Pt(12); r.font.color.rgb = SLATE
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("The assumption: everything is down \u2014 no electricity, no banks, no gas, no digital communication, no grocery stores. "
              "The same kit also covers an ordinary 3-day PSPS shutoff, a storm, or an accident. Tick items off as you get them; most people already own several.")
r.italic = True; r.font.size = Pt(10); r.font.color.rgb = SLATE

h("Ground rules", 1)
bullet("no open flame or gas indoors, no gasoline stored inside, and no generator in the apartment. Cooking and any flame happen on the balcony only.", bold_prefix="Apartment rules still apply: ")
bullet("14 days at home is the target. A month of water for one person is about 30 gallons / 240 lb, which a one-bedroom cannot sensibly store \u2014 past two weeks, you resupply from outside rather than living off a closet.", bold_prefix="Two weeks, not forever: ")
bullet("it is one item on this list, not the list. In a long outage the binding limits are water, food, cash and communications \u2014 a bigger battery fixes none of those.", bold_prefix="The power station is already in progress: ")
bullet("Only buy food you would actually eat, and rotate it into normal cooking so nothing quietly goes stale.", bold_prefix="Buy what you eat: ")

h("What it costs, roughly", 1)
para("Rough US retail ranges, estimated for planning in November 2026 \u2014 not live-checked prices. Buying only what you do not already own will usually land well below the top of the range.")
t = doc.add_table(rows=1, cols=2); t.style = "Table Grid"; t.autofit = False
for i, txt in enumerate(["Category", "Rough cost"]):
    c = t.rows[0].cells[i]; c.text = ""
    r = c.paragraphs[0].add_run(txt); r.bold = True; r.font.color.rgb = RGBColor(0xFF,0xFF,0xFF); r.font.size = Pt(9.5)
    shade(c, ACCENT)
for a, b in [
    ("Water", "$80\u2013135"), ("Food (14 days, incl. stove and fuel)", "$155\u2013260"),
    ("Power and light (excluding the power station)", "$110\u2013170"), ("Warmth", "$70\u2013135"),
    ("Comms, money and papers (excluding cash itself)", "$15\u201325"),
    ("Health and sanitation", "$70\u2013115"), ("Getting around", "$55\u201395"),
    ("Tools and knowledge", "$55\u201395"), ("Go-bag extras", "$20\u201340"),
    ("TOTAL \u2014 essentials, if bought new", "about $650\u20131,100"),
]:
    cells = t.add_row().cells
    for i, txt in enumerate([a, b]):
        cells[i].text = ""
        r = cells[i].paragraphs[0].add_run(txt); r.font.size = Pt(9.5)
        if "TOTAL" in a: r.bold = True
    cells[0].width = Inches(5.2); cells[1].width = Inches(2.0)
doc.add_paragraph()
para("Separate from that total: set aside about $300 in cash in small bills (money held, not money spent), any extra prescription medicines (cost varies), and the power station and solar panels, which are being chosen separately.", italic=True, size=10)

h("Water \u2014 the binding constraint", 1)
para("One gallon per person per day covers drinking and basic sanitation. Stored water runs out, so the kit pairs storage with a way to make more.")
checklist_table([
    ("Stored drinking water", "14 gal", "In sturdy containers; rotate every 6 months", "$30\u201360"),
    ("Squeeze / gravity water filter (Sawyer-style)", "1", "For rain, creek or a neighbour's supply \u2014 filter first, always", "$25\u201335"),
    ("Water purification tablets", "1 pack", "Backup to the filter, not a replacement for it", "$10\u201315"),
    ("Collapsible water containers", "2", "Water is 8 lb a gallon \u2014 do not plan to haul it far in a bucket", "$15\u201325"),
])

h("Food \u2014 nothing that needs a fridge", 1)
para("About 2,000 calories a day for 14 days. Tier 1 needs no refrigeration, no water and no cooking. Tier 2 needs only hot water.")
checklist_table([
    ("Canned tuna / chicken", "14 cans", "Tier 1 \u2014 ready to eat", "incl. below"),
    ("Nut butter", "2 jars", "Tier 1 \u2014 dense calories, keeps well", "incl. below"),
    ("Crackers", "2\u20133 boxes", "Tier 1", "incl. below"),
    ("Dried fruit and nuts", "4\u20135 lb total", "Tier 1", "incl. below"),
    ("Granola / protein bars", "28 bars", "Tier 1 \u2014 about 2 a day", "incl. below"),
    ("Shelf-stable milk", "6\u20138 cartons", "Tier 1", "incl. below"),
    ("Rice, oats, dried beans / lentils, instant soup", "About 7 days' worth", "Tier 2 \u2014 hot water only; foods you already cook", "incl. below"),
    ("All food above, combined", "14 days", "Rotate into normal cooking before it ages out", "$120\u2013200"),
    ("Manual can opener", "1", "The item everyone forgets", "incl. above"),
    ("Single-burner butane camp stove + fuel canisters", "1 stove, 4 canisters", "BALCONY ONLY, never indoors", "$35\u201360"),
])

h("Power and light", 1)
para("The power station and panels are in progress separately. These are the small, cheap items that make dark evenings workable \u2014 light matters more than people expect when it is dark at 5 p.m.")
checklist_table([
    ("Power station + solar panels", "1 set", "In progress \u2014 see separate comparison; keep it cool indoors, around 50\u201360% charge if stored for outages", "Separate"),
    ("Headlamp", "1", "Hands-free light for stairs, cooking and repairs", "$20\u201330"),
    ("Lantern", "1", "Room light for evenings", "$20\u201335"),
    ("Spare batteries (for headlamp, lantern, radio)", "1 set", "Check and replace yearly", "$15"),
    ("USB battery bank", "1 (10,000\u201320,000 mAh)", "Keeps a phone alive between station charges", "$25\u201340"),
    ("Hand-crank / battery NOAA weather radio", "1", "Your news source when phone and internet are down", "$30\u201350"),
])

h("Warmth \u2014 layers beat gadgets", 1)
para("With no power or gas there is no indoor heating. A Bay Area apartment will not freeze, but it will be cold and damp.")
checklist_table([
    ("Sleeping bag, rated to about 20\u00b0F", "1", "Plenty for Bay Area nights", "$60\u2013120"),
    ("Extra blankets", "2", "Layer over the sleeping bag or bed", "Often owned"),
    ("Warm layers and wool socks", "2\u20133 sets", "Base layers count more than one heavy coat", "Often owned"),
    ("Hand warmers", "10 pairs", "Small comfort, long shelf life", "$10\u201315"),
])

h("Comms, money and papers \u2014 the no-digital part", 1)
para("No banks means no cards and no ATMs. No phone or internet means paper is the backup for everything digital normally holds.")
checklist_table([
    ("Cash in small bills, in a waterproof bag", "About $300", "Money set aside, not spent \u2014 small bills only", "$300 held"),
    ("Paper copies: ID, insurance, prescriptions", "1 set", "Keep with the cash, in the waterproof bag", "Printing"),
    ("Written list of phone numbers and addresses", "1", "Numbers you no longer have memorised", "\u2014"),
    ("Printed local map", "1", "For getting around without a phone", "\u2014"),
    ("Whistle", "1", "Signalling without shouting or power", "$5"),
    ("Waterproof document pouch", "1", "Holds cash and paper copies together", "$10\u201320"),
])

h("Health and sanitation", 1)
para("Medicines are the real bottleneck for most people \u2014 food and water are easy to store, a prescription is not.")
checklist_table([
    ("First aid kit", "1", "Bandages, antiseptic, tweezers, basic supplies", "$25\u201340"),
    ("Extra supply of medicines you take", "14 days extra", "Plus painkillers; talk to your pharmacist about how to hold a buffer", "Varies"),
    ("Toilet paper", "12+ rolls", "Stores flat-ish, never wasted", "incl. below"),
    ("Soap and hand sanitiser", "2\u20133 bottles each", "Hygiene is what stops a bad week becoming an illness", "incl. below"),
    ("Trash bags", "1 box", "Waste has nowhere to go if collection stops", "incl. below"),
    ("Bucket + heavy bags (backup toilet)", "1 bucket, 1 pack bags", "For if water is out and the toilet will not flush", "incl. below"),
    ("Sanitation supplies above, combined", "\u2014", "", "$30\u201350"),
    ("N95 masks", "10\u201320", "Doubles for wildfire smoke \u2014 a Bay Area item anyway", "$15\u201325"),
])

h("Getting around", 1)
para("The elevator will not work, so stairs are the plan \u2014 worth knowing your stair route now, not discovering it in the dark. In a long outage the e-bike is your car, and the solar panels are its gas station.")
checklist_table([
    ("E-bike, kept charged", "1", "Already ordered; charge from the station / panels in an outage", "Already owned"),
    ("Walking shoes", "1 pair", "Broken in, not new", "Often owned"),
    ("Backpack", "1", "Carries water, food and the go-bag contents", "$40\u201370"),
    ("Bike lock", "1", "", "Often owned"),
    ("Bike tire repair kit + pump", "1 kit", "A flat tire ends the e-bike plan", "$15\u201325"),
])

h("Tools and knowledge \u2014 the actual 1800s part", 1)
checklist_table([
    ("Multi-tool", "1", "", "$25\u201350"),
    ("Duct tape", "1 roll", "", "incl. below"),
    ("Wrench (to shut off utilities)", "1", "Learn where your shut-offs are before you need them", "incl. below"),
    ("Rope / cord", "About 50 ft", "", "incl. below"),
    ("Work gloves", "1 pair", "", "incl. below"),
    ("Lighter + waterproof matches", "1 + 1 pack", "For the balcony stove only", "incl. below"),
    ("Small tools and consumables above, combined", "\u2014", "", "$30\u201345"),
    ("Printed instructions, on paper", "1 folder", "How to purify water, basic first aid, how to use the stove and the power station \u2014 because you cannot look it up when it is down", "Printing"),
])

h("The 3-day go-bag \u2014 if you have to leave", 1)
para("This is a subset of the home kit packed to grab, not a second stockpile. Pack it once, keep it by the door or in a closet, and check it when you rotate the water.")
checklist_table([
    ("Water", "1 gal + filter", "Plus purification tablets from the home kit", "From kit"),
    ("Food bars / ready-to-eat food", "3 days", "No cooking, no water needed", "From kit"),
    ("Change of warm clothes + wool socks", "1 set", "Sealed in a dry bag", "From kit"),
    ("Headlamp + spare batteries", "1 set", "", "From kit"),
    ("Cash in small bills + paper ID copies", "Part of the $300", "Split between home pouch and go-bag if you prefer", "From kit"),
    ("Medicines", "3 days", "Rotate with your regular supply so they never expire in the bag", "From kit"),
    ("Phone battery bank + cable", "1", "", "From kit"),
    ("N95 masks, whistle, multi-tool", "2 / 1 / 1", "", "From kit"),
    ("Sturdy backpack or duffel for the bag itself", "1", "Only a new cost if you do not already own one", "$20\u201340"),
])

h("Rotation and upkeep \u2014 the kit only works if it is fresh", 1)
t = doc.add_table(rows=1, cols=2); t.style = "Table Grid"; t.autofit = False
for i, txt in enumerate(["When", "Do this"]):
    c = t.rows[0].cells[i]; c.text = ""
    r = c.paragraphs[0].add_run(txt); r.bold = True; r.font.color.rgb = RGBColor(0xFF,0xFF,0xFF); r.font.size = Pt(9.5)
    shade(c, ACCENT)
for a, b in [
    ("Every 6 months", "Replace stored water. Check go-bag medicines and swap in fresh ones."),
    ("Ongoing", "Eat the stored food in normal cooking and replace it, oldest first."),
    ("Once a year", "Check batteries, hand warmers, masks and fuel canisters; top up the cash if you dipped into it."),
    ("A few times a year", "If the power station is stored for outages, check its charge and top it up; store it cool, around 50\u201360%."),
    ("After any real outage", "Restock what you used while you still remember what ran short."),
]:
    cells = t.add_row().cells
    for i, txt in enumerate([a, b]):
        cells[i].text = ""
        r = cells[i].paragraphs[0].add_run(txt); r.font.size = Pt(9.5)
    cells[0].width = Inches(1.6); cells[1].width = Inches(5.6)
doc.add_paragraph()
para("Storage: everything above except the water containers fits in a closet and a balcony corner. Keep the go-bag, headlamp, radio and paper copies somewhere you can reach in the dark.", italic=True, size=10)

doc.save(OUT)
print("saved", OUT)
