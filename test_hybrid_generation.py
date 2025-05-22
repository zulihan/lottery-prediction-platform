"""
Test the Fibonacci-Filtered Hybrid strategy generation to identify the issue
"""

from fibonacci_hybrid_strategy import generate_fibonacci_hybrid_combinations
from database import get_db_connection
import traceback

def test_hybrid_generation():
    """Test the hybrid strategy generation"""
    try:
        print("🧪 Testing Fibonacci-Filtered Hybrid Strategy Generation...")
        
        # Test with 3 combinations
        combinations = generate_fibonacci_hybrid_combinations(num_final=3)
        
        if combinations:
            print(f"✅ Successfully generated {len(combinations)} combinations!")
            
            # Display first combination as example
            first_combo = combinations[0]
            print(f"\nExample combination:")
            print(f"Numbers: {first_combo['numbers']}")
            print(f"Stars: {first_combo['stars']}")
            print(f"Strategy: {first_combo['strategy']}")
            print(f"Score: {first_combo['final_score']}")
            
            # Test manual database save
            try:
                engine = get_db_connection()
                print("\n💾 Testing database save...")
                
                test_combo = combinations[0]
                from datetime import datetime, timedelta
                
                with engine.connect() as conn:
                    result = conn.execute("""
                        INSERT INTO generated_combinations (numbers, stars, strategy, score, target_draw_date, created_at)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        RETURNING id
                    """, (
                        str(test_combo['numbers']),
                        str(test_combo['stars']),
                        test_combo['strategy'],
                        test_combo['final_score'],
                        (datetime.now() + timedelta(days=2)).date(),
                        datetime.now().date()
                    ))
                    conn.commit()
                    new_id = result.fetchone()[0]
                    print(f"✅ Successfully saved combination with ID: {new_id}")
                
            except Exception as save_error:
                print(f"❌ Database save error: {save_error}")
                traceback.print_exc()
            
            return True
            
        else:
            print("❌ No combinations generated!")
            return False
            
    except Exception as e:
        print(f"❌ Error during generation: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_hybrid_generation()
    
    if success:
        print("\n🚀 Hybrid strategy generation is working!")
        print("The issue is likely in the app display logic.")
    else:
        print("\n🔧 Found the issue - hybrid strategy generation needs fixing.")