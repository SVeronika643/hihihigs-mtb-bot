import logging

def setup_logger(level: int=logging.INFO, fname: str=__name__) -> None:
    loggig.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s | %(name)s: %(message)s",
        handlers=[logging.FileHandler(f"logs/{fname}.log", mode="w"), ],
        datefmt ="[%d-%n-%Y %H:%M:%S]",
    )