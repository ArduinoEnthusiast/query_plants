import sqlite3
import time
from escpos.printer import Usb

# Function to print plant data
def print_plants(plants):
    # Initialize the printer with the correct settings
    printer = Usb(0x28e9, 0x0289, out_ep=0x03)
    printer.text("Plants List:\n")
    for species_name, common_names in plants:
        printer.text(f"{species_name} ({common_names})\n")
    printer.cut()

# Retrieve suburbs from the database
def get_suburbs():
    conn = sqlite3.connect('/home/joshua1349/Downloads/PlantDataBase.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT suburb_name FROM suburbs ORDER BY suburb_name;")
    suburbs = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return suburbs

# Retrieve biomes for a given suburb
def get_biomes(suburb_name):
    conn = sqlite3.connect('/home/joshua1349/Downloads/PlantDataBase.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT b.biome_name
        FROM suburbs sub
        JOIN suburb_biomes sbi ON sub.suburb_id = sbi.suburb_id
        JOIN biomes b ON sbi.biome_id = b.biome_id
        WHERE sub.suburb_name = ?
        ORDER BY b.biome_name;
    """, (suburb_name,))
    biomes = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return biomes

# Retrieve plant species for a given suburb and biome
def get_plants_in_biome(suburb_name, biome_name):
    conn = sqlite3.connect('/home/joshua1349/Downloads/PlantDataBase.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.species_name, s.common_names
        FROM suburbs sub
        JOIN suburb_biomes sbi ON sub.suburb_id = sbi.suburb_id
        JOIN biomes b ON sbi.biome_id = b.biome_id
        JOIN species_biome sb ON b.biome_id = sb.biome_id
        JOIN species s ON sb.species_id = s.species_id
        WHERE sub.suburb_name = ? AND b.biome_name = ?
        ORDER BY s.species_name;
    """, (suburb_name, biome_name))
    plants = cursor.fetchall()
    cursor.close()
    conn.close()
    return plants[:10]  # Return only the first 10 results

# Main function to drive the program
def main():
    print("Welcome to the D.I.R.T (Detoxify, Integrate, Repair, Transform) worker terminal")
    time.sleep(2)
    suburbs = get_suburbs()
    if suburbs:
        print("\nPlease choose a suburb to revitalise:")
        for i, suburb in enumerate(suburbs, start=1):
            print(f"{i}) {suburb}")
        selection = int(input("\nEnter the number of the suburb you want to revitalize: "))
        suburb_name = suburbs[selection - 1]

        # Simulate thinking/loading
        print("\nAnalyzing database for biomes in", suburb_name, end="")
        for _ in range(3):
            time.sleep(0.5)  # delay
            print(".", end="", flush=True)
        print()  # move to next line

        biomes = get_biomes(suburb_name)
        if biomes:
            print(f"\nBiomes found in {suburb_name}:")
            for i, biome in enumerate(biomes, start=1):
                print(f"{i}) Biome: {biome}")
            selection = int(input("\nEnter the number of the biome you want to explore: "))
            selected_biome = biomes[selection - 1]

            # Simulate loading for the selected biome
            print(f"\nBuilding you a unique profile of plants to revitalize {selected_biome}")
            for _ in range(4):
                time.sleep(0.5)  # delay
                print(".", end="", flush=True)
            print(f"\nPrinting you a docket of plants for {selected_biome}")

            plants = get_plants_in_biome(suburb_name, selected_biome)
            print_plants(plants)  # Print the plants using the thermal printer
        else:
            print("No biomes found for the suburb:", suburb_name)
    else:
        print("No suburbs found in the database.")

if __name__ == '__main__':
    main()
