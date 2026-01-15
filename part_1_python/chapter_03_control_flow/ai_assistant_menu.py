# From: Zero to AI Agent, Chapter 3, Section 3.7
# ai_assistant_menu.py

print("🤖 AI Assistant Control Panel")

running = True
while running:
    print("\n" + "=" * 30)
    print("MAIN MENU")
    print("1. Data Processing")
    print("2. Model Training")  
    print("3. Make Predictions")
    print("4. Exit")
    
    choice = input("\nSelect option: ")
    
    if choice == "1":
        # Data Processing Submenu
        while True:
            print("\n--- Data Processing ---")
            print("a. Load data")
            print("b. Clean data")
            print("c. Analyze data")
            print("d. Back to main menu")
            
            sub_choice = input("Select: ").lower()
            
            if sub_choice == "a":
                filename = input("Enter filename: ")
                print(f"📁 Loading {filename}...")
                # In real code, you'd actually load the file
            elif sub_choice == "b":
                print("🧹 Cleaning data...")
                for i in range(3):
                    print(f"  Processing batch {i+1}/3...")
            elif sub_choice == "c":
                print("📊 Analyzing data...")
                print("  Mean: 42.3")
                print("  Std Dev: 5.7")
            elif sub_choice == "d":
                break  # Go back to main menu
            else:
                print("❌ Invalid option")
    
    elif choice == "2":
        print("\n🧠 Training mode activated...")
        epochs = int(input("Number of epochs: "))
        for epoch in range(1, epochs + 1):
            print(f"  Epoch {epoch}/{epochs}: Loss = {100/epoch:.2f}")
    
    elif choice == "3":
        print("\n🎯 Making predictions...")
        value = float(input("Enter input value: "))
        # Simulate prediction
        prediction = value * 2.3 + 15
        print(f"Prediction: {prediction:.2f}")
    
    elif choice == "4":
        print("\n👋 Goodbye!")
        running = False
    
    else:
        print("❌ Invalid option. Please try again.")
