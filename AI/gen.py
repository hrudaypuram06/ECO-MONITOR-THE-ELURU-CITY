import random

areas = [
    'RR Pet', 'Powerpet', 'Tangellamudi', 'Sanivarapupeta', 'Ashram Hospital',
    'Vatluru', 'Satrampadu', 'Fathenagar', 'Narasimharao Pet', 'Gavaravaram',
    'Kothapet', 'Chodimella', 'Duggirala', 'Marruru', 'Housing Board Colony',
    'Arundhati Peta', 'Venkatarayapuram', 'Pratap Nagar', 'Sriram Nagar',
    'Gudivakalanka', 'Jalalpet', 'Gandi Nagar', 'Koppaka', 'Kommireddy',
    'Ravirala', 'Kalakaparru', 'NTR Nagar', 'Teachers Colony', 'Sainikpuri',
    'Revenue Colony', 'NGO Colony', 'Police Quarters', 'RTC Colony',
    'Bank Colony', 'Medical College Area', 'Collectorate', 'Zila Parishad',
    'Bus Stand Area', 'Railway Station Area', 'Market Yard', 'Industrial Estate',
    'Auto Nagar', 'Bhimavaram Road', 'Vijayawada Road', 'Ameerpet',
    'Ramachandra Rao Pet', 'Gowthami Nagar', 'Krishna Nagar', 'Sai Nagar', 'Sivaji Nagar'
]

locations_array = []
known_places_obj = []

base_lat = 16.7107
base_lon = 81.1035

for a in areas:
    lat = base_lat + (random.uniform(-1, 1) * 0.04)
    lon = base_lon + (random.uniform(-1, 1) * 0.04)
    aqi = int(random.triangular(25, 95, 45))
    locations_array.append(f'{{ name: "{a}", pos: [{lat:.4f}, {lon:.4f}], aqi: {aqi} }}')
    known_places_obj.append(f'"{a.lower()}": [{lat:.4f}, {lon:.4f}]')

js_locations = ",\n".join(locations_array)
js_known = ",\n".join(known_places_obj)

print('LOCATIONS_START')
print(js_locations)
print('LOCATIONS_END')
print('KNOWN_START')
print(js_known)
print('KNOWN_END')
