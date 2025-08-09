"""
Main entrypoint to run the HODL project pipeline.
"""
import argparse
from src.app import launch, index_texts

def main():
    parser = argparse.ArgumentParser(description="HODL Project Runner")
    parser.add_argument("--serve", action="store_true", help="Launch Gradio app")
    parser.add_argument("--index", type=str, nargs="*", help="Index provided texts (repeatable)")
    args = parser.parse_args()

    if args.index:
        print(index_texts(args.index))
    if args.serve or not args.index:
        launch()

if __name__ == "__main__":
    main()
