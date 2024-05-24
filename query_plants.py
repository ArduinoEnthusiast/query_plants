import sqlite3
import time
from collections import defaultdict

def get_suburbs():
    conn = sqlite3.connect('/Users/jwait/PlantDataBase.db')  # Connection to the DB
    cursor = conn.cursor()
    # SQL query to fetch the list of suburbs
    query = """
    SELECT DISTINCT suburb_name
    FROM suburbs
    ORDER BY suburb_name;
    """

    # Execute the query
    cursor.execute(query)
    suburbs = [row[0] for row in cursor.fetchall()]

    # Close the connection
    cursor.close()
    conn.close()

    return suburbs

def get_biomes(suburb_name):
    # Connect to the SQLite database
    conn = sqlite3.connect('/Users/jwait/PlantDataBase.db')  # Connection to the DB
    cursor = conn.cursor()

    # SQL query to fetch biomes associated with a suburb
    query = """
    SELECT DISTINCT b.biome_name
    FROM suburbs sub
    JOIN suburb_biomes sbi ON sub.suburb_id = sbi.suburb_id
    JOIN biomes b ON sbi.biome_id = b.biome_id
    WHERE sub.suburb_name = ?
    ORDER BY b.biome_name;
    """

    # Execute the query
    cursor.execute(query, (suburb_name,))
    biomes = [row[0] for row in cursor.fetchall()]

    # Close the connection
    cursor.close()
    conn.close()

    return biomes

def get_plants_in_biome(suburb_name, biome_name):
    # Connect to the SQLite database
    conn = sqlite3.connect('/Users/jwait/PlantDataBase.db')  # Update the database path as needed
    cursor = conn.cursor()

    # SQL query to fetch plants in a specific biome within a suburb
    query = """
    SELECT s.species_name, s.common_names
    FROM suburbs sub
    JOIN suburb_biomes sbi ON sub.suburb_id = sbi.suburb_id
    JOIN biomes b ON sbi.biome_id = b.biome_id
    JOIN species_biome sb ON b.biome_id = sb.biome_id
    JOIN species s ON sb.species_id = s.species_id
    WHERE sub.suburb_name = ? AND b.biome_name = ?
    ORDER BY s.species_name;
    """

    # Execute the query
    cursor.execute(query, (suburb_name, biome_name))
    plants = cursor.fetchall()

    # Close the connection
    cursor.close()
    conn.close()

    return plants

def main():
    print("Welcome new recruit to the D.I.R.T (Detoxify, Integrate, Repair, Transform) worker terminal")
    time.sleep(2)

    # Get the list of suburbs
    suburbs = get_suburbs()

    if suburbs:
        # Display the list of suburbs with numbers
        print(f"\nPlease choose a suburb to revistalise:")
        for i, suburb in enumerate(suburbs, start=1):
            time.sleep(0.5)
            print(f"{i}) Suburb: {suburb}")

        # Ask the user to select a suburb by number
        while True:
            try:
                selection = int(input("\nEnter the number of the suburb you want to revitalize: "))
                if 1 <= selection <= len(suburbs):
                    suburb_name = suburbs[selection - 1]
                    break
                else:
                    print("Invalid selection. Please enter a number from the list.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        # Simulate thinking/loading
        print("\nAnalyzing database for biomes in", suburb_name, end="")
        for _ in range(3):
            time.sleep(0.5)  # delay
            print(".", end="", flush=True)
        print()  # move to next line

        # Get the biomes in the chosen suburb
        biomes = get_biomes(suburb_name)

        if biomes:
            # Display the list of biomes with numbers
            print(f"\nBiomes found in {suburb_name}:")
            for i, biome in enumerate(biomes, start=1):
                print(f"{i}) Biome: {biome}")

            # Ask the user to select a biome by number
            while True:
                try:
                    selection = int(input("\nEnter the number of the biome you want to explore: "))
                    if 1 <= selection <= len(biomes):
                        selected_biome = biomes[selection - 1]
                        break
                    else:
                        print("Invalid selection. Please enter a number from the list.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

            # Simulate loading for the selected biome
            print(f"\nBuilding you a unique profile of plants to revitalize {selected_biome}")
            for _ in range(4):
                time.sleep(0.5)  # delay
                print(".", end="", flush=True)
            print(f"\nPrinting you a docket of plants")
            for _ in range(4):
                time.sleep(0.5)  # delay
                print(".", end="", flush=True)

            # Display the plants in the selected biome
            plants = get_plants_in_biome(suburb_name, selected_biome)
            print(f"\nPlants in {selected_biome}:")
            for species_name, common_name in plants:
                print(f"  {species_name} ({common_name})")
                time.sleep(0.5)  # delay for dramatic effect
            print(f"\nPlease take to D.I.R.T associate for your assignment")
        else:
            print("No biomes found for the suburb:", suburb_name)
    else:
        print("No suburbs found in the database.")

if __name__ == '__main__':
    main()
