import logging
from ui import GraphicFileManagerUI
from version import __version__

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename='app.log',
        filemode='w'
    )

def main():
    try:
        setup_logging()
        logger = logging.getLogger(__name__)
        logger.info(f"Starting Graphic File Manager v{__version__}")
        
        app = GraphicFileManagerUI()
        app.run()
        
        logger.info("Application shutdown complete")
    except Exception as e:
        logging.error(f"Application error: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
