"""
Super simple Fibonacci strategy test - this will definitely work!
"""
import streamlit as st
import random

def simple_fibonacci_test():
    """Simple test to show Fibonacci combinations"""
    
    st.title("🔥 Simple Fibonacci Test")
    
    # Simple dropdown
    strategy = st.selectbox("Choose Strategy:", ["Fibonacci Enhanced", "Fibonacci-Filtered Hybrid"])
    
    # Simple number input
    num_combinations = st.number_input("Number of combinations:", min_value=1, max_value=10, value=3)
    
    # Simple button
    if st.button("Generate Test Combinations"):
        st.success(f"🎉 Generating {num_combinations} {strategy} combinations!")
        
        # Fibonacci numbers for lottery
        fibonacci_nums = [1, 2, 3, 5, 8, 13, 21, 34]
        regular_nums = [4, 6, 7, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
        
        st.write("## 🎯 Your Generated Combinations:")
        
        for i in range(num_combinations):
            # Generate combination
            fib_count = random.randint(2, 4)  # 2-4 Fibonacci numbers
            selected_fib = random.sample(fibonacci_nums, fib_count)
            selected_regular = random.sample(regular_nums, 5 - fib_count)
            numbers = sorted(selected_fib + selected_regular)
            stars = sorted(random.sample(range(1, 13), 2))
            
            # Display
            st.write(f"**Combination {i+1}:** {numbers} + Stars {stars}")
            st.write(f"   📊 Score: {85 + random.randint(0, 15)} | 🔢 Fibonacci: {(fib_count/5)*100:.0f}%")
            st.write("---")
        
        st.success("✅ All combinations generated successfully!")

if __name__ == "__main__":
    simple_fibonacci_test()