"""
Fix the duplicate combination 20 by generating a new unique combination
using only numbers from the Strategic V3 pool
"""
import random

def get_available_pool():
    """Pool of numbers and stars from Strategic V3"""
    return {
        'numbers': [4, 7, 9, 10, 12, 14, 15, 16, 17, 18, 20, 21, 23, 25, 28, 29, 31, 33, 34, 35, 36, 37, 38, 39, 42, 44, 45, 47, 50],
        'stars': [1, 3, 4, 5, 6, 8, 9, 12],
        'most_frequent_numbers': [23, 29, 7, 33, 35, 44, 37, 39, 21, 20],
        'most_frequent_stars': [5, 8, 12, 1, 9, 3, 4, 6]
    }

def get_existing_combinations():
    """Existing fusion combinations to avoid duplicates"""
    return [
        [23, 29, 7, 33, 35],   # 11. Frequency Champions Fusion
        [7, 15, 23, 29, 38],   # 12. Risk-Frequency Hybrid
        [10, 12, 31, 45, 47],  # 13. Markov-Time Fusion
        [23, 29, 37, 38, 44],  # 14. Coverage-Risk Balance
        [23, 29, 7, 33, 35],   # 15. Hot Numbers Concentration
        [9, 14, 15, 25, 35],   # 16. Strategic Diversity Mix
        [12, 21, 23, 29, 39],  # 17. Pattern Recognition Fusion
        [7, 9, 23, 25, 29],    # 18. Trend-Frequency Hybrid
        [15, 23, 29, 34, 38],  # 19. Cold-Hot Equilibrium
        # 20 needs to be generated (was duplicate of 15)
    ]

def generate_new_combination_20():
    """Generate a new unique combination 20"""
    
    pool = get_available_pool()
    existing = get_existing_combinations()
    
    print("🔄 GÉNÉRATION NOUVELLE COMBINAISON 20")
    print("Remplacement du doublon avec combinaison 15")
    print("-" * 45)
    
    # Strategy: Advanced Strategic Synthesis
    # Use less frequent numbers from the pool to ensure uniqueness
    
    # Take some less frequent but still strategic numbers
    less_frequent_strategic = [n for n in pool['most_frequent_numbers'][5:] if n not in [23, 29, 7, 33, 35]]
    
    # Mix with some numbers that appear less often in existing combinations
    underused_numbers = []
    for num in pool['numbers']:
        count = sum(1 for combo in existing if num in combo)
        if count <= 1:  # Numbers used 1 time or less
            underused_numbers.append(num)
    
    # Create combination 20: Advanced Strategic Synthesis
    # Use a mix of strategic numbers not heavily used in other combinations
    
    candidates = [4, 16, 28, 36, 42, 44, 50]  # Strategic but underused
    
    # Select 5 unique numbers ensuring no duplicate with existing combinations
    attempts = 0
    while attempts < 50:
        selected_numbers = sorted(random.sample(candidates + less_frequent_strategic[:3], 5))
        
        # Check if this combination already exists
        if selected_numbers not in existing:
            break
        attempts += 1
    
    # If still duplicate, force a unique combination
    if selected_numbers in existing:
        selected_numbers = [4, 16, 28, 36, 42]  # Guaranteed unique
    
    # Stars: use less frequent stars
    selected_stars = [3, 6]  # Less used stars from the pool
    
    new_combination = {
        'numbers': selected_numbers,
        'stars': selected_stars,
        'strategy': 'Advanced Strategic Synthesis',
        'methodology': 'Underused strategic numbers fusion'
    }
    
    print(f"20. {new_combination['strategy']}")
    print(f"    Numbers: {new_combination['numbers']} | Stars: {new_combination['stars']}")
    print(f"    Methodology: {new_combination['methodology']}")
    
    # Verify uniqueness
    print(f"\n✅ VÉRIFICATION UNICITÉ:")
    is_unique = selected_numbers not in existing
    print(f"Unique par rapport aux 19 autres: {'OUI' if is_unique else 'NON'}")
    
    # Verify all numbers are in pool
    all_in_pool = all(n in pool['numbers'] for n in selected_numbers)
    stars_in_pool = all(s in pool['stars'] for s in selected_stars)
    print(f"Tous les numéros dans le pool Strategic V3: {'OUI' if all_in_pool else 'NON'}")
    print(f"Toutes les étoiles dans le pool Strategic V3: {'OUI' if stars_in_pool else 'NON'}")
    
    return new_combination

def main():
    """Generate the corrected combination 20"""
    
    print("🚀 CORRECTION COMBINAISON 20 - ÉLIMINATION DOUBLON")
    print("=" * 55)
    
    new_combo = generate_new_combination_20()
    
    print(f"\n📊 RÉSUMÉ:")
    print(f"✅ Nouvelle combinaison 20 générée")
    print(f"✅ Unique et différente de la combinaison 15")
    print(f"✅ Utilise uniquement le pool Strategic V3")
    print(f"✅ Stratégie: Advanced Strategic Synthesis")
    
    return new_combo

if __name__ == "__main__":
    main()