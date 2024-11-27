import swisseph as swe
import matplotlib.pyplot as plt
import math
from datetime import datetime

class AstrologyChart:
    def __init__(self, birth_date, birth_time, birth_place):
        """
        Inicializace astrologického grafu
        
        :param birth_date: Datum narození (YYYY-MM-DD)
        :param birth_time: Čas narození (HH:MM)
        :param birth_place: Zeměpisné souřadnice místa [longitude, latitude]
        """
        self.birth_datetime = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
        self.longitude, self.latitude = birth_place
        
        # Nastavení Swiss Ephemeris
        swe.set_topo(self.longitude, self.latitude, 0)  # poslední parametr je nadmořská výška
    
    def calculate_planet_positions(self):
        """
        Výpočet poloh planet
        """
        planets = {
            'Slunce': swe.SUN,
            'Měsíc': swe.MOON,
            'Merkur': swe.MERCURY,
            'Venuše': swe.VENUS,
            'Mars': swe.MARS,
            'Jupiter': swe.JUPITER,
            'Saturn': swe.SATURN,
            'Uran': swe.URANUS,
            'Neptun': swe.NEPTUNE,
            'Pluto': swe.PLUTO
        }
        
        planet_positions = {}
        for name, planet_id in planets.items():
            # Převod data na juliánský kalendář
            jd = swe.julday(self.birth_datetime.year, 
                            self.birth_datetime.month, 
                            self.birth_datetime.day, 
                            self.birth_datetime.hour + self.birth_datetime.minute/60)
            
            # Výpočet pozice planety
            try:
                # calc_ut() vrací tuple složený z několika hodnot
                # První hodnota je geocentrická délka
                calc_result = swe.calc_ut(jd, planet_id)
                
                # První prvek první tuple je geocentrická délka planety
                planet_pos = calc_result[0][0]
                
                # Normalizace na rozsah 0-360 stupňů
                planet_positions[name] = float(planet_pos) % 360
            
            except Exception as e:
                print(f"Chyba při výpočtu pozice planety {name}: {e}")
                planet_positions[name] = 0.0
        
        return planet_positions
    
    def interpret_positions(self, positions):
        """
        Základní interpretace pozic planet
        """
        interpretations = {}
        zodiac_signs = [
            'Beran', 'Býk', 'Blíženci', 'Rak', 'Lev', 'Panna', 
            'Váhy', 'Štír', 'Střelec', 'Kozoroh', 'Vodnář', 'Ryby'
        ]
        
        for planet, position in positions.items():
            sign_index = int(position // 30)
            sign = zodiac_signs[sign_index]
            degree = position % 30
            
            interpretations[planet] = {
                'znamení': sign,
                'stupeň': round(degree, 2)
            }
        
        return interpretations
    
    def plot_planet_positions(self, positions):
        """
        Vizualizace pozic planet
        """
        plt.figure(figsize=(10, 10))
        plt.subplot(polar=True)
        
        angles = [math.radians(pos) for pos in positions.values()]
        planets = list(positions.keys())
        
        plt.scatter(angles, [1]*len(planets), c='red', s=100)
        
        for angle, planet in zip(angles, planets):
            plt.text(angle, 1.1, planet, 
                     horizontalalignment='center', 
                     verticalalignment='center')
        
        plt.title('Pozice planet v horoskopu')
        plt.tight_layout()
        plt.savefig('planetni_pozice.png')
        plt.close()
    
    def generate_horoscope(self):
        """
        Hlavní metoda pro generování horoskopu
        """
        positions = self.calculate_planet_positions()
        interpretations = self.interpret_positions(positions)
        self.plot_planet_positions(positions)
        
        return {
            'pozice_planet': positions,
            'interpretace': interpretations
        }

# Příklad použití
def main():
    chart = AstrologyChart(
        birth_date='1972-03-01',   # datum narození
        birth_time='05:50',        # čas narození
        birth_place=[14.4378, 50.0755]  # Praha - zeměpisná délka a šířka
    )
    
    horoscope = chart.generate_horoscope()
    
    print("Pozice planet:")
    for planet, position in horoscope['pozice_planet'].items():
        print(f"{planet}: {position}°")
    
    print("\nInterpretace:")
    for planet, info in horoscope['interpretace'].items():
        print(f"{planet}: {info['znamení']} ({info['stupeň']}°)")

if __name__ == "__main__":
    main()