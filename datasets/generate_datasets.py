import csv
import random
import uuid
from datetime import datetime, timedelta

random.seed(42)

def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

project_types = ["Infrastructure", "Industrial", "Energy", "Mining", "Water & Sanitation"]
statuses = ["Active", "Completed", "On Hold", "Cancelled"]
countries = ["Peru", "Chile", "Colombia", "Ecuador", "Brazil", "Argentina"]
regions_peru = ["Lima", "Arequipa", "Cusco", "Junín", "Piura", "La Libertad", "Cajamarca", "Ica", "Loreto", "Puno"]
regions_chile = ["Santiago", "Antofagasta", "Valparaíso", "Biobío"]
regions_colombia = ["Bogotá", "Antioquia", "Valle del Cauca", "Cundinamarca"]
regions_map = {"Peru": regions_peru, "Chile": regions_chile, "Colombia": regions_colombia, "Ecuador": ["Pichincha", "Guayas", "Azuay"], "Brazil": ["São Paulo", "Rio de Janeiro", "Minas Gerais"], "Argentina": ["Buenos Aires", "Córdoba", "Santa Fe"]}
cities_peru = {"Lima": ["Lima", "Callao", "Miraflores"], "Arequipa": ["Arequipa", "Cayma"], "Cusco": ["Cusco", "Urubamba"], "Junín": ["Huancayo", "Tarma"], "Piura": ["Piura", "Sullana"], "La Libertad": ["Trujillo", "Chepén"], "Cajamarca": ["Cajamarca", "Jaén"], "Ica": ["Ica", "Nazca"], "Loreto": ["Iquitos"], "Puno": ["Puno", "Juliaca"]}
cities_default = {"Santiago": ["Santiago"], "Antofagasta": ["Antofagasta"], "Bogotá": ["Bogotá"], "Antioquia": ["Medellín"], "Pichincha": ["Quito"], "Guayas": ["Guayaquil"], "São Paulo": ["São Paulo"], "Rio de Janeiro": ["Rio de Janeiro"], "Buenos Aires": ["Buenos Aires"]}

vendor_categories = ["Materials", "Services", "Equipment Rental", "Transport", "Consulting", "Technology"]
employee_departments = ["Engineering", "Maintenance", "Operations", "Finance", "Procurement", "Safety", "Quality", "Planning"]
employee_roles = ["Project Engineer", "Maintenance Supervisor", "Operator", "Analyst", "Manager", "Coordinator", "Inspector", "Director"]
equipment_types = ["Excavator", "Crane", "Bulldozer", "Loader", "Dump Truck", "Concrete Mixer", "Generator", "Welding Machine", "Drill", "Compactor", "Scaffolding", "Pump"]
equipment_statuses = ["Active", "In Maintenance", "Retired", "Reserved"]
maintenance_types = ["Preventive", "Corrective", "Predictive", "Routine"]

start_date = datetime(2024, 1, 1)
end_date = datetime(2027, 12, 31)

# ---- 1. Projects (50) ----
project_names = [
    "Lima Highway Expansion", "Copper Plant Upgrade", "Solar Farm Installation",
    "Water Treatment Plant", "Port Modernization", "Railway Extension",
    "Hospital Construction", "School Renovation Program", "Airport Terminal Expansion",
    "Bridge Rehabilitation", "Dam Construction", "Power Substation Upgrade",
    "Gas Pipeline Network", "Sanitary Sewer System", "Desalination Plant",
    "Telecommunications Tower", "Wind Farm Project", "Irrigation Canal System",
    "Metro Line Extension", "Refinery Overhaul", "Mining Conveyor Belt",
    "Industrial Warehouse", "Data Center Construction", "Landfill Remediation",
    "Flood Control System", "Highway Tunnel", "Electrical Grid Modernization",
    "Shopping Mall Construction", "Hotel & Resort Development", "Stadium Renovation",
    "Oil Platform Maintenance", "Chemical Plant Expansion", "Steel Mill Upgrade",
    "Cement Plant Construction", "Food Processing Facility", "Pharmaceutical Lab",
    "Aquaculture Project", "Forestry Management Base", "Coastal Protection Wall",
    "Research Center Build", "Military Base Upgrade", "Public Park Redevelopment",
    "Waste-to-Energy Plant", "Geothermal Plant", "Hydroelectric Station",
    "Container Terminal", "Bus Rapid Transit", "Cable Car System",
    "Industrial Park Development", "Smart City Infrastructure"
]

projects = []
for i in range(1, 51):
    pid = f"PRJ{i:03d}"
    p_start = random_date(datetime(2024, 1, 1), datetime(2026, 6, 1))
    duration = random.randint(180, 730)
    p_end = p_start + timedelta(days=duration)
    budget = random.randint(500000, 8000000)
    projects.append({
        "project_id": pid,
        "project_name": project_names[i-1],
        "project_type": random.choice(project_types),
        "status": random.choice(statuses),
        "start_date": p_start.strftime("%Y-%m-%d"),
        "end_date": p_end.strftime("%Y-%m-%d"),
        "budget": budget
    })

# ---- 2. Locations (50) ----
locations = []
for i in range(1, 51):
    country = random.choice(countries)
    region = random.choice(regions_map.get(country, ["Default"]))
    city_map = cities_default if country != "Peru" else cities_peru
    city = random.choice(city_map.get(region, ["Default"]))
    locations.append({
        "location_id": f"LOC{i:03d}",
        "country": country,
        "region": region,
        "city": city,
        "site_name": f"{city} {random.choice(['North', 'South', 'East', 'West', 'Central', 'Industrial', 'Main', 'Secondary'])} Site"
    })

# ---- 3. Vendors (50) ----
vendor_names = [
    "Cementos del Sur", "Industrial Services SAC", "Constructora ABC", "Transportes Rápidos",
    "Equipos Pesados EIRL", "Consultoría Técnica", "Ingeniería & Obras", "Materiales Premium",
    "Logística Integral", "Grupo Ferretero", "Minería Supply", "Energía Total",
    "Servicios Generales", "Maquinarias del Norte", "Construcciones Unidas",
    "Proveedora Industrial", "Distribuidora del Oeste", "Tecnología Aplicada",
    "Seguridad Integral", "Mantenimiento Expert", "Renta de Equipos", "Transportes Lima",
    "Aceros Nacionales", "Concretos del Valle", "Electro Industria", "Refacciones Ya",
    "Ingeniería Civil", "Constructora del Sur", "Servicios Marítimos", "Equipos Mineros",
    "Soluciones Ambientales", "Arquitectura Moderna", "Redes Eléctricas", "Agua & Saneamiento",
    "Geotecnia Aplicada", "Obras Viales", "Grupo Inmobiliario", "Instalaciones Industriales",
    "Ferretería Mayorista", "Combustibles del Perú", "Laboratorio Control", "Topografía Exacta",
    "Diseño Estructural", "Supervisión Técnica", "Pinturas Industriales", "Aislamientos Térmicos",
    "Ventanas & Fachadas", "Sistemas Contra Incendios", "Climatización Total", "Elevadores SAC"
]

vendors = []
for i in range(1, 51):
    vendors.append({
        "vendor_id": f"VEN{i:03d}",
        "vendor_name": vendor_names[i-1],
        "category": random.choice(vendor_categories),
        "country": random.choice(countries)
    })

# ---- 4. Employees (200) ----
first_names = ["Carlos", "Ana", "Luis", "María", "José", "Rosa", "Juan", "Carmen", "Pedro", "Elena",
               "Diego", "Sofía", "Miguel", "Laura", "Andrés", "Valentina", "Jorge", "Patricia", "Ricardo", "Diana",
               "Fernando", "Gabriela", "Sergio", "Claudia", "Pablo", "Monica", "Hugo", "Verónica", "Oscar", "Silvia",
               "Raúl", "Adriana", "Mario", "Isabel", "Javier", "Andrea", "Gustavo", "Liliana", "Alberto", "Teresa",
               "Alejandro", "Ruth", "Francisco", "Rocío", "Eduardo", "Lorena", "César", "Natalia", "Víctor", "Gloria"]

last_names = ["Ramos", "Torres", "García", "Martínez", "López", "Rodríguez", "Pérez", "González", "Hernández", "Díaz",
              "Silva", "Vargas", "Castillo", "Romero", "Moreno", "Álvarez", "Morales", "Ortiz", "Chávez", "Reyes",
              "Gutiérrez", "Castro", "Medina", "Soto", "Rivas", "Cruz", "Ortega", "Flores", "Núñez", "Mendoza",
              "Vega", "Campos", "Ríos", "Aguilar", "Cáceres", "Delgado", "Paredes", "Huamán", "Quispe", "Mamani",
              "Salazar", "Cornejo", "Navarro", "Villanueva", "Tapia", "Roldán", "Zambrano", "Bustamante", "Espinoza", "Miranda"]

employees = []
for i in range(1, 201):
    fn = random.choice(first_names)
    ln = random.choice(last_names)
    emp_id = f"EMP{i:03d}"
    hire = random_date(datetime(2020, 1, 1), datetime(2025, 12, 31))
    employees.append({
        "employee_id": emp_id,
        "full_name": f"{fn} {ln}",
        "department": random.choice(employee_departments),
        "role": random.choice(employee_roles),
        "hire_date": hire.strftime("%Y-%m-%d")
    })

# ---- 5. Equipment (20) ----
equipment_names_by_type = {
    "Excavator": ["CAT 320 Excavator", "CAT 336 Excavator", "Komatsu PC200", "Hitachi EX200"],
    "Crane": ["Liebherr LTM 1100", "Caterpillar 730", "Grove GMK3050", "Tadano ATF"],
    "Bulldozer": ["CAT D6T", "Komatsu D155", "Shantui SD32", "CAT D8T"],
    "Loader": ["CAT 966M", "Komatsu WA380", "Volvo L120", "CAT 950GC"],
    "Dump Truck": ["Volvo A40G", "CAT 773E", "Komatsu HM400", "Bell B40E"],
    "Concrete Mixer": ["Schwing S36X", "Putzmeister P715", "CIFA 8m³", "Mercedes Mixer"],
    "Generator": ["Caterpillar C15", "Cummins QSK60", "Kohler 150REZX", "Generac 200kW"],
    "Welding Machine": ["Miller XMT 350", "Lincoln Ranger 330", "ESAB Warrior 500", "Fronius TPS 400"],
    "Drill": ["Atlas Copco ROC D7", "Sandvik D45KS", "Boart Longyear LF90", "Epiroc SmartROC"],
    "Compactor": ["Bomag BW216", "CAT CS76", "Hamm HD+ 110", "Dynapac CA3500"],
    "Scaffolding": ["Layher Allround", "Peri Up", "Kwikstage", "Ringlock"],
    "Pump": ["Grundfos CR45", "Flygt 3301", "Wacker PT6", "Tsunami DP800"]
}
all_equip_names = [name for names in equipment_names_by_type.values() for name in names]

equipment = []
for i in range(1, len(all_equip_names)+1):
    # find type
    eq_type = None
    for t, names in equipment_names_by_type.items():
        if all_equip_names[i-1] in names:
            eq_type = t
            break
    purchase = random_date(datetime(2020, 1, 1), datetime(2024, 12, 31))
    manufacturers_by_type = {
        "Excavator": ["Caterpillar", "Komatsu", "Hitachi"],
        "Crane": ["Liebherr", "Caterpillar", "Grove", "Tadano"],
        "Bulldozer": ["Caterpillar", "Komatsu", "Shantui"],
        "Loader": ["Caterpillar", "Komatsu", "Volvo"],
        "Dump Truck": ["Volvo", "Caterpillar", "Komatsu", "Bell"],
        "Concrete Mixer": ["Schwing", "Putzmeister", "CIFA", "Mercedes"],
        "Generator": ["Caterpillar", "Cummins", "Kohler", "Generac"],
        "Welding Machine": ["Miller", "Lincoln", "ESAB", "Fronius"],
        "Drill": ["Atlas Copco", "Sandvik", "Boart Longyear", "Epiroc"],
        "Compactor": ["Bomag", "Caterpillar", "Hamm", "Dynapac"],
        "Scaffolding": ["Layher", "Peri", "Kwikstage", "Ringlock"],
        "Pump": ["Grundfos", "Flygt", "Wacker", "Tsunami"],
    }
    manufacturer = random.choice(manufacturers_by_type.get(eq_type or "General", ["Unknown"]))
    equipment.append({
        "equipment_id": f"EQ{i:03d}",
        "equipment_name": all_equip_names[i-1],
        "equipment_type": eq_type or "General",
        "manufacturer": manufacturer,
        "purchase_date": purchase.strftime("%Y-%m-%d"),
        "status": random.choice(equipment_statuses)
    })

# ---- 6. Costs (5000) ----
costs = []
for _ in range(5000):
    proj = random.choice(projects)
    vendor = random.choice(vendors)
    c_date = random_date(datetime(2025, 1, 1), datetime(2027, 12, 31))
    planned = round(random.uniform(1000, 200000), 2)
    variation = planned * random.uniform(-0.15, 0.15)
    actual = round(planned + variation, 2)
    costs.append({
        "project_id": proj["project_id"],
        "vendor_id": vendor["vendor_id"],
        "cost_date": c_date.strftime("%Y-%m-%d"),
        "planned_cost": planned,
        "actual_cost": actual
    })

# ---- 7. Schedule (3000) ----
schedule = []
for _ in range(3000):
    proj = random.choice(projects)
    p_start = datetime.strptime(proj["start_date"], "%Y-%m-%d")
    p_end = datetime.strptime(proj["end_date"], "%Y-%m-%d")
    r_date = random_date(p_start, p_end)
    progress_base = ((r_date - p_start).days / (p_end - p_start).days) * 100
    planned = min(100, round(progress_base + random.uniform(-3, 5), 1))
    actual = min(100, round(planned + random.uniform(-8, 3), 1))
    actual = max(0, actual)
    schedule.append({
        "project_id": proj["project_id"],
        "report_date": r_date.strftime("%Y-%m-%d"),
        "planned_progress": planned,
        "actual_progress": actual
    })

# ---- 8. Maintenance (1500) ----
maintenance = []
for _ in range(1500):
    eq = random.choice(equipment)
    m_date = random_date(datetime(2024, 1, 1), datetime(2027, 12, 31))
    mtype = random.choice(maintenance_types)
    if mtype == "Corrective":
        downtime = random.randint(4, 24)
        cost = round(random.uniform(800, 5000), 2)
    elif mtype == "Preventive":
        downtime = random.randint(1, 5)
        cost = round(random.uniform(200, 1500), 2)
    elif mtype == "Predictive":
        downtime = random.randint(1, 3)
        cost = round(random.uniform(300, 2500), 2)
    else:
        downtime = random.randint(1, 4)
        cost = round(random.uniform(100, 1000), 2)
    maintenance.append({
        "equipment_id": eq["equipment_id"],
        "maintenance_date": m_date.strftime("%Y-%m-%d"),
        "maintenance_type": mtype,
        "downtime_hours": downtime,
        "maintenance_cost": cost
    })

# ---- 9. Workforce (3000) ----
workforce = []
for _ in range(3000):
    emp = random.choice(employees)
    proj = random.choice(projects)
    p_start = datetime.strptime(proj["start_date"], "%Y-%m-%d")
    p_end = datetime.strptime(proj["end_date"], "%Y-%m-%d")
    w_date = random_date(p_start, p_end)
    hours = round(random.uniform(4, 12), 1)
    productivity = round(random.uniform(0.5, 1.0), 2)
    workforce.append({
        "employee_id": emp["employee_id"],
        "project_id": proj["project_id"],
        "report_date": w_date.strftime("%Y-%m-%d"),
        "hours_worked": hours,
        "productivity_score": productivity,
    })

# ---- 10. Risks (1000) ----
risks = []
risk_descriptions_prefix = [
    "Budget overrun", "Schedule delay", "Quality non-compliance", "Safety incident",
    "Material shortage", "Labor strike", "Equipment failure", "Design change",
    "Permit delay", "Weather disruption", "Supplier bankruptcy", "Regulatory change",
    "Geotechnical issue", "Environmental violation", "Community protest",
    "Technology integration", "Contractual dispute", "Funding shortfall",
    "Exchange rate fluctuation", "Political instability", "Pandemic outbreak",
    "Cyberattack", "Fire hazard", "Structural failure", "Logistics disruption"
]

for i in range(1, 1001):
    proj = random.choice(projects)
    prob = round(random.uniform(0.1, 0.95), 2)
    sev = random.randint(1, 10)
    impact_cost = random.randint(5000, 200000)
    impact_days = random.randint(2, 90)
    p_start = datetime.strptime(proj["start_date"], "%Y-%m-%d")
    p_end = datetime.strptime(proj["end_date"], "%Y-%m-%d")
    risk_date = random_date(p_start, p_end)
    risks.append({
        "risk_id": f"RISK{i:04d}",
        "project_id": proj["project_id"],
        "risk_description": f"{random.choice(risk_descriptions_prefix)} - {random.choice(project_names)}",
        "probability": prob,
        "severity": sev,
        "impact_cost": impact_cost,
        "impact_days": impact_days,
        "risk_date": risk_date.strftime("%Y-%m-%d"),
    })

# ---- Write CSVs ----
def write_csv(filename, fieldnames, rows):
    with open(f"datasets/{filename}", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  -> {filename} ({len(rows)} records)")

if __name__ == "__main__":
    import os
    os.makedirs("datasets", exist_ok=True)

    print("Generating synthetic datasets...\n")

    write_csv("projects.csv",   ["project_id", "project_name", "project_type", "status", "start_date", "end_date", "budget"], projects)
    write_csv("locations.csv",  ["location_id", "country", "region", "city", "site_name"], locations)
    write_csv("vendors.csv",    ["vendor_id", "vendor_name", "category", "country"], vendors)
    write_csv("employees.csv",  ["employee_id", "full_name", "department", "role", "hire_date"], employees)
    write_csv("equipment.csv",  ["equipment_id", "equipment_name", "equipment_type", "manufacturer", "purchase_date", "status"], equipment)
    write_csv("costs.csv",      ["project_id", "vendor_id", "cost_date", "planned_cost", "actual_cost"], costs)
    write_csv("schedule.csv",   ["project_id", "report_date", "planned_progress", "actual_progress"], schedule)
    write_csv("maintenance.csv",["equipment_id", "maintenance_date", "maintenance_type", "downtime_hours", "maintenance_cost"], maintenance)
    write_csv("workforce.csv",  ["employee_id", "project_id", "report_date", "hours_worked", "productivity_score"], workforce)
    write_csv("risks.csv",      ["risk_id", "project_id", "risk_description", "probability", "severity", "impact_cost", "impact_days", "risk_date"], risks)

    print("\nDone! All datasets generated in datasets/")
