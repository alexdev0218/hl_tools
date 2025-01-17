import dc_listener
import tg_listener
import asyncio

async def main():
    await asyncio.gather(
        dc_listener.iniciar_dc_bot(),
        tg_listener.iniciar_tg_escucha()
    )

if __name__ == "__main__":
    asyncio.run(main())