from .core.app import FashionSearchApp

def main():
    app = FashionSearchApp()
    input_message = input("Enter your message: ")
    app.run(input_message)

if __name__ == "__main__":
    main() 