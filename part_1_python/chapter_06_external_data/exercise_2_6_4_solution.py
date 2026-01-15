# From: Zero to AI Agent, Chapter 6, Section 6.4
# Exercise 2 Solution: File Reader with Error Handling

"""
File Reader with Error Handling
Build a program that safely reads any file.
"""

def safe_file_reader(filename):
    """Read a file with proper error handling"""
    try:
        with open(filename, 'r') as file:
            content = file.read()
            print(f"\n📄 Contents of '{filename}':")
            print("-" * 40)
            print(content)
            return True
            
    except FileNotFoundError:
        print(f"❌ File '{filename}' not found!")
        print("Please check the filename and try again.")
        return False
        
    except PermissionError:
        print(f"❌ Permission denied! Cannot read '{filename}'")
        print("The file might be protected.")
        return False
        
    except IsADirectoryError:
        print(f"❌ '{filename}' is a directory, not a file!")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    print("=== Safe File Reader ===")
    
    while True:
        filename = input("\nEnter filename to read (or 'quit'): ")
        
        if filename.lower() == 'quit':
            break
        
        success = safe_file_reader(filename)
        
        if not success:
            retry = input("\nTry another file? (yes/no): ")
            if retry.lower() != 'yes':
                break
    
    print("Happy reading! 📚")

if __name__ == "__main__":
    main()
