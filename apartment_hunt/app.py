from .processing.processor import Processor
import logging

logging.basicConfig(level=logging.INFO)

def main():
    logging.info("Starting processing...")
    Processor().transformations()
    logging.info("Processing complete.")

if __name__ == "__main__":
    main()