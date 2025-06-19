import asyncio
from classes import CodewarsLogic

async def main():
    logic = CodewarsLogic()
    tasks = await logic.parse_and_store("https://www.codewars.com/users/polinakornienko")
    print("Parsed tasks:", tasks)

if __name__ == "__main__":
    asyncio.run(main())