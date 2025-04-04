import aiohttp
import asyncio
from colorama import Fore, init
import pyfiglet
import time
import os

# colorama'yi başlatıyoruz
init(autoreset=True)

# Webhook URL ve vanity dosyası
happy = "https://discord.com/api/webhooks/1356232864735170710/JRKusmyrApQ-Ho4v7RG4jxBw1EmO5mgId5X-gXObPSd2dO4HfzoPuzZ6pvlIDGAvpVaS"
new = "vanity.txt"
years = "https://discord.com/api/v10/invites/"

secret_message = "***https://discord.gg/586 Katılmayı Unutmayın @everyone***"

# ASCII Sanatları
ascii_art_additional = """
 █████╗ ███████╗██████╗  █████╗ ██╗██╗           ██╗  ███████╗ █████╗  █████╗   
██╔══██╗╚════██║██╔══██╗██╔══██╗██║██║          ██╔╝  ██╔════╝██╔══██╗██╔═══╝ 
███████║  ███╔═╝██████╔╝███████║██║██║         ██╔╝   ██████╗ ╚█████╔╝██████╗ 
██╔══██║██╔══╝  ██╔══██╗██╔══██║██║██║        ██╔╝    ╚════██╗██╔══██╗██╔══██╗
██║  ██║███████╗██║  ██║██║  ██║██║███████╗  ██╔╝     ██████╔╝╚█████╔╝╚█████╔╝
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚══════╝  ╚═╝      ╚═════╝  ╚════╝  ╚════╝
██╗   ██╗ █████╗ ███╗  ██╗██╗████████╗██╗   ██╗  ██╗   ██╗██████╗ ██╗
██║   ██║██╔══██╗████╗ ██║██║╚══██╔══╝╚██╗ ██╔╝  ██║   ██║██╔══██╗██║
╚██╗ ██╔╝███████║██╔██╗██║██║   ██║    ╚████╔╝   ██║   ██║██████╔╝██║
 ╚████╔╝ ██╔══██║██║╚████║██║   ██║     ╚██╔╝    ██║   ██║██╔══██╗██║
  ╚██╔╝  ██║  ██║██║ ╚███║██║   ██║      ██║     ╚██████╔╝██║  ██║███████╗
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚══╝╚═╝   ╚═╝      ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝
 █████╗ ██╗  ██╗███████╗ █████╗ ██╗  ██╗███████╗██████╗
██╔══██╗██║  ██║██╔════╝██╔══██╗██║ ██╔╝██╔════╝██╔══██╗
██║  ╚═╝███████║█████╗  ██║  ╚═╝█████═╝ █████╗  ██████╔╝
██║  ██╗██╔══██║██╔══╝  ██║  ██╗██╔═██╗ ██╔══╝  ██╔══██╗
╚█████╔╝██║  ██║███████╗╚█████╔╝██║ ╚██╗███████╗██║  ██║
 ╚════╝ ╚═╝  ╚═╝╚══════╝ ╚════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝"""

ascii_art_main = pyfiglet.figlet_format("")
ascii_art_colored = f"{Fore.RED}{ascii_art_additional}{ascii_art_main}"

async def check_invites():
    try:
        with open(new, "r") as file:
            invite_codes = [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"❌ Err: '{new}' dosyası bulunamadı.")
        return

    if not invite_codes:
        print("⚠️ Vanity listesi boş.")
        return

    chunk_size = 10
    for i in range(0, len(invite_codes), chunk_size):
        os.system('cls' if os.name == 'nt' else 'clear')  # Ekranı temizle
        print(ascii_art_colored)  # ASCII sanatını ekle
        chunk = invite_codes[i:i + chunk_size]
        print(f"📊 Checking invites: {i + 1} to {min(i + chunk_size, len(invite_codes))}")
        await check_chunk(chunk)

    await send_to_webhook(secret_message)

async def check_chunk(chunk):
    async with aiohttp.ClientSession() as session:
        results = []
        for code in chunk:
            url = years + code
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        guild_name = data.get("guild", {}).get("name", "Doesn't exist.")
                        channel_name = data.get("channel", {}).get("name", "Doesn't exist.")
                        result_message = f"❌ URL Kullanılıyor: https://discord.gg/{code} | Server: **{guild_name}**, Channel: **{channel_name}**"
                    elif response.status == 404:
                        result_message = f"✅ URL Kullanılmıyor veya Banlı: https://discord.gg/{code}"
                    else:
                        result_message = f"⚠️ Hata: https://discord.gg/{code} | Yanıt Süresi Çok Fazla {response.status}"
                    results.append(result_message)
            except Exception as e:
                results.append(f"⚠️ Error fetching {url}: {str(e)}")

        if results:
            await send_to_webhook("\n".join(results))

async def send_to_webhook(messages):
    if not happy:
        print("❌ Webhook URL doesn't exist.")
        return

    payload = {"content": messages}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(happy, json=payload) as response:
                if response.status != 204:
                    print(f"❌ Webhook sending error: HTTP {response.status}")
        except Exception as e:
            print(f"❌ Error sending webhook: {str(e)}")

async def continue_or_exit():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # Ekranı temizle
        print(ascii_art_colored)  # ASCII sanatını ekle
        print("Vanity URL'lerin kontrolü tamamlandı.")
        print("1. Ana Menüye Dön")
        print("2. Çıkış yap")

        choice = input("Bir seçenek girin (1/2): ")

        if choice == "1":
            os.system('cls' if os.name == 'nt' else 'clear')  # Ekranı temizle
            print(ascii_art_colored)  # ASCII sanatını tekrar ekle
            return  # Ana menüye dön
        elif choice == "2":
            os.system('cls' if os.name == 'nt' else 'clear')  # Ekranı temizle
            print(ascii_art_additional)  # Çıkıştan önce ASCII sanatı ekle
            print(Fore.RED + "Çıkılıyor...")  # Çıkış mesajını kırmızı yapıyoruz
            time.sleep(5)  # 5 saniye bekliyoruz
            exit()  # Programdan çıkıyoruz
        else:
            print("Geçersiz seçim, lütfen tekrar deneyin.")

async def main():
    os.system('cls' if os.name == 'nt' else 'clear')  # Ekranı temizliyoruz
    print(ascii_art_colored)  # ASCII sanatını başta gösteriyoruz

    while True:
        print("1. Vanity URL'ları kontrol et")
        print("2. Sms Bomb")
        print("3. Çıkış Yap")

        choice = input("Seçim: ")

        if choice == "1":
            print("Vanity URL'ler kontrol ediliyor...")
            await check_invites()
            await continue_or_exit()  # Kontrol tamamlandıktan sonra devam etme ya da çıkma ekranı
        elif choice == "3":
            os.system('cls' if os.name == 'nt' else 'clear')  # Ekranı temizlemeden önce ASCII sanatı ekleyelim
            print(ascii_art_additional)  # Çıkıştan önce ASCII sanatı ekliyoruz
            print(Fore.RED + "Çıkılıyor...")  # Çıkış mesajını kırmızı yapıyoruz
            time.sleep(5)  # 5 saniye bekliyoruz
            break  # Programı sonlandırıyoruz
        else:
            print("Geçersiz seçim, lütfen tekrar deneyin.")

if __name__ == "__main__":
    asyncio.run(main())
