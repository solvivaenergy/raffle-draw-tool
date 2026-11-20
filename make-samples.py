"""Write two sample files with made-up people, in the exact column layout the Odoo export will use.

    verified-entries-sample.csv   312 rows for a draw
    previous-winners-sample.csv   3 rows: winners of an earlier draw (two of them also appear in the entries file)
"""
import csv
import os
import random

random.seed(20261222)
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample")
os.makedirs(HERE, exist_ok=True)

FIRST = ["Maria", "Jose", "Ana", "Carlo", "Luz", "Ben", "Rosa", "Daniel", "Elena", "Paolo", "Grace", "Marco", "Liza", "Ramon",
         "Jen", "Mark", "Teresa", "Nico", "Bea", "Rico", "Cathy", "Jun", "Mia", "Allan", "Joy", "Edwin", "Karen", "Noel", "Faye", "Dennis"]
LAST = ["Santos", "Dela Cruz", "Villanueva", "Tan", "Garcia", "Pascual", "Lim", "Bautista", "Mercado", "Ocampo", "Ramos", "Aquino",
        "Castillo", "Fernandez", "Torres", "Flores", "Gonzales", "Navarro", "Mendoza", "Domingo", "Salazar", "Cruz", "Rivera", "Diaz"]
CITY = ["Quezon City", "Makati", "Pasig", "Taguig", "Bacoor", "Santa Rosa", "Lipa", "Malolos", "San Fernando", "Antipolo",
        "Paranaque", "Las Pinas", "Cainta", "Cebu City", "Davao City"]
STREET = ["Mabini St", "Rizal Ave", "Sampaguita St", "Narra St", "Acacia Lane", "Molave St", "Ilang-Ilang St", "Maharlika Hwy",
          "Camia St", "Dama de Noche St", "Yakal St", "Lawin St"]

COLUMNS = ["Full Name", "Street", "City", "Email", "Phone/Mobile", "System Size"]


def person(i):
    first, last = random.choice(FIRST), random.choice(LAST)
    name = f"{first} {last}"
    email = f"{first}.{last}{i}@example.com".lower().replace(" ", "")
    phone = f"09{random.randint(10, 99)} {random.randint(100, 999)} {random.randint(1000, 9999)}"
    street = f"{random.randint(1, 250)} {random.choice(STREET)}"
    city = random.choice(CITY)
    big = random.random() < 0.19
    kwp = round(random.uniform(15, 30), 1) if big else round(random.uniform(5, 14.9), 1)
    return [name, street, city, email, phone, f"{kwp} kWp"]


rows = [person(i) for i in range(1, 313)]
# a few rows that the tool should flag
rows[10][5] = "4.5 kWp"           # under 5 kWp: no prize pool
rows[25][5] = ""                  # missing system size
rows[40] = list(rows[39])         # exact duplicate of the row above

with open(os.path.join(HERE, "verified-entries-sample.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(COLUMNS)
    w.writerows(rows)

# earlier winners: two of them are also in tonight's list (same email), so the tool must skip them
prev = [rows[4], rows[17], ["Ramon Ocampo", "12 Narra St", "Lipa", "ramon.ocampo.d1@example.com", "0917 555 0101", "18.2 kWp"]]
with open(os.path.join(HERE, "previous-winners-sample.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(COLUMNS)
    w.writerows(prev)

# The shape Odoo's "Promo Participation" list exports (staging module, Oct 2026). Reference is the entry number,
# Promo Prize decides the pool, and only Status = Joined with Eligible ticked goes into the draw.
PART_COLUMNS = ["Reference", "Full Name", "Street", "City", "Email", "Mobile", "Promo Prize", "Status", "Eligible",
                "Winner Type", "Opportunity/System Size (kWp)"]
part = []
for i, r in enumerate(rows[:60], start=1):
    name, street, city, email, phone, size = r
    kwp = float(size.replace(" kWp", "")) if size else None
    prize = "16 kWh Battery Package" if kwp and kwp >= 15 else "5 kWh Battery Package"
    status, eligible = "Joined", "True"
    if i in (3, 11):
        status = "Invited"           # never submitted the form
    if i in (7,):
        status, eligible = "Joined", "False"   # submitted but failed the eligibility check
    if i == 20:
        status = "Winner"            # won in an earlier draw of the same promo
    if i == 25:
        prize = "16 kWh Battery Package"       # prize set wrongly for a small system
    size_cell = f"{kwp}" if kwp and i % 3 else ""          # some exports will carry the kWp, some will not
    part.append([f"PWRUP-{i:04d}", name, street, city, email, phone, prize, status, eligible, "Priority", size_cell])

with open(os.path.join(HERE, "odoo-participation-export-sample.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(PART_COLUMNS)
    w.writerows(part)

# The exact column layout of the real Odoo export (15 Oct 2026) plus the two fields it must also carry: Promo Prize
# (the pool) and Eligible. Prize names are written the way Odoo shows them, remaining quantity in brackets.
REAL_COLUMNS = ["Reference", "Draw Number", "Draw Date", "Customer", "Last Name", "First Name", "Middle Name", "Mobile",
                "Email", "Street", "City", "Status", "Eligible", "Promo Prize"]
CITIES_ODOO = ["Metro Manila ~ Caloocan", "Metro Manila ~ Makati", "Metro Manila ~ Valenzuela", "Metro Manila ~ Quezon City",
               "Cavite ~ Bacoor", "Laguna ~ Santa Rosa", "Batangas ~ Lipa", "Bulacan ~ Malolos", "Rizal ~ Antipolo"]
real = []
for i, r in enumerate(rows[:40], start=1):
    name, street, _city, email, phone, size = r
    first, last = name.split(" ", 1)
    kwp = float(size.replace(" kWp", "")) if size else 8.0
    prize = "Pylontech 16kwh Battery (1)" if kwp >= 15 else "Pylontech 5kwh Battery (2)"
    draw = "2" if i > 34 else "1"
    status, eligible = "Joined", "True"
    if i in (5, 17):
        status = "Invited"
    if i == 9:
        eligible = "False"
    if i == 22:
        status = "Winner"
    mobile = "+63" + phone.replace(" ", "")[1:]
    real.append([f"BATTERYPROMO-{i:04d}", draw, "2026-11-20", name, last, first, "", mobile, email, street,
                 random.choice(CITIES_ODOO), status, eligible, prize])

with open(os.path.join(HERE, "odoo-export-sample.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(REAL_COLUMNS)
    w.writerows(real)

print("wrote", len(rows), "entries,", len(prev), "previous winners,", len(part), "participation rows and", len(real),
      "rows in the real export layout to", HERE)
