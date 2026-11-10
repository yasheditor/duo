import os
import time
import datetime
import traceback
import asyncio
import json
import urllib3
import random
import uuid
import httpx
from pyfiglet import figlet_format
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import requests
import data_pb2
import Beta_pb2 as _7P
import Major_Login_pb2

urllib3.disable_warnings()

# --- Termux Color Palette ---
C_RESET   = "\033[0m"
C_GREEN   = "\033[38;5;46m"
C_YELLOW  = "\033[38;5;226m"
C_RED     = "\033[38;5;196m"
C_CYAN    = "\033[38;5;51m"
C_BLUE    = "\033[38;5;33m"
C_MAGENTA = "\033[38;5;201m"
C_BOLD    = "\033[1m"
C_ORANGE = "\033[38;5;208m"
C_PINK = "\033[38;5;205m"
C_LIME = "\033[38;5;118m"
C_GOLD = "\033[38;5;220m"
C_SKY_BLUE = "\033[38;5;117m"
C_VIOLET = "\033[38;5;135m"
C_SILVER = "\033[38;5;250m"
C_BRIGHT_MAGENTA = "\033[95m"
C_BRIGHT_CYAN = "\033[96m"
C_BRIGHT_GREEN = "\033[92m"
C_BRIGHT_WHITE = "\033[97m"
C_BRIGHT_YELLOW = "\033[93m"
C_GOLD = "\033[38;5;220m"
C_BG_RED = "\033[41m"
C_BG_GREEN = "\033[42m"
C_BG_BLUE = "\033[44m"
C_BG_MAGENTA = "\033[45m"
C_BG_CYAN = "\033[46m"
C_BRIGHT_RED = "\033[91m"
C_BRIGHT_BLUE = "\033[94m"
C_BRIGHT_WHITE = "\033[97m"

def banner():
    os.system('cls' if os.name == 'nt' else 'clear')

    print(f"{C_BOLD}{C_BRIGHT_MAGENTA}╔══════════════════════════════════════════════╗{C_RESET}")

    # ASCII Logo
    logo = figlet_format("Duo Info", font="slant")
    print(f"{C_BOLD}{C_BRIGHT_CYAN}{logo}{C_RESET}")

    print(f"{C_BOLD}{C_BRIGHT_MAGENTA}╚══════════════════════════════════════════════╝{C_RESET}")

    print(f"""
{C_BOLD}{C_BRIGHT_GREEN}  [+] Developer: {C_BRIGHT_WHITE}@XEROX_MODS
{C_BOLD}{C_BRIGHT_YELLOW}  [+] Telegram : {C_BRIGHT_CYAN}@SEXTYMODS{C_RESET}
""")


# Global Async Client for API requests
client = httpx.AsyncClient(verify=False, timeout=15.0)

ACCOUNT_CACHE_DIR = "account_cache"
DEVICE_FILE = "Device.json"
os.makedirs(ACCOUNT_CACHE_DIR, exist_ok=True)
CACHE_DURATION = 8 * 3600  # 8 hours 

# Configuration & Constants (Multi-Region Support with Credentials)
REGION_CONFIGS = {
    "IND": {
        "uid": "8009835259",
        "password": "JCD_71DE712D3323EE41",
        "client_url": "https://client.ind.freefiremobile.com"
    },
    "US": {
        "uid": "8346110378",
        "password": "XEROX_2989EA3F805E3397",
        "client_url": "https://client.us.freefiremobile.com"
    },
    "POLAR": {
        "uid": "8346106874",
        "password": "XEROX_824A6780AB0084C2",
        "client_url": "https://clientbp.ggpolarbear.com"
    }
}

NEW_LOGIN_URLS = [
    "https://loginbp.ggpolarbear.com/"
]

headers = {
    'User-Agent': 'UnityPlayer/2018.4.12f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Expect': '100-continue',
    'X-Unity-Version': '2018.4.12f1',
    'X-GA-SV': '1789535859',
    'X-GA': 'v1 1',
    'ReleaseVersion': 'OB55'
}

_3K = b'Yg&tc%DEuh6%Zc^8'
_4V = b'6oyZDr22E3ychjM%'
_6T = 15
_7H = {"Content-Type": "application/x-www-form-urlencoded"}
_8A = "Dalvik/2.1.0 (Linux; U; Android 11)"
_9R = "v1 1"
_10L = "OB55"

AES_KEY = _3K
AES_IV = _4V
_LOGIN_SEMAPHORE = asyncio.Semaphore(5)

class Parser:
    def parse(self, hex_str):
        return {}

async def parse_results(parsed):
    return {}

def get_proto_field(dict_res, field_num, default=None):
    if not isinstance(dict_res, dict):
        return default
    val = dict_res.get(str(field_num))
    return val if val is not None else default

def log(message):
    print(message)

def YoUr_MoM(d):
    return AES.new(_3K, AES.MODE_CBC, _4V).encrypt(pad(d, 16))

def UNknown(d):
    try:
        return unpad(AES.new(_3K, AES.MODE_CBC, _4V).decrypt(d), 16)
    except Exception as e:
        return d

def ReSPeCt_GiRLs(n):
    res = bytearray()
    while n >= 0x80:
        res.append((n & 0x7f) | 0x80)
        n >>= 7
    res.append(n)
    return bytes(res)

def YOuR_FaThER(uid):
    return YoUr_MoM(b"\x08" + ReSPeCt_GiRLs(int(uid)))

def _pb_field(field_number, val):
    if isinstance(val, str):
        b_val = val.encode('utf-8')
        wire_type = 2
        header = (field_number << 3) | wire_type
        return ReSPeCt_GiRLs(header) + ReSPeCt_GiRLs(len(b_val)) + b_val
    elif isinstance(val, bytes):
        wire_type = 2
        header = (field_number << 3) | wire_type
        return ReSPeCt_GiRLs(header) + ReSPeCt_GiRLs(len(val)) + val
    elif isinstance(val, int):
        wire_type = 0
        header = (field_number << 3) | wire_type
        return ReSPeCt_GiRLs(header) + ReSPeCt_GiRLs(val)
    return b""

async def aes_encrypt(data, key, iv):
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return cipher.encrypt(pad(data, 16))
    except Exception as e:
        print(f"{C_RED}[!] AES encryption error: {e}{C_RESET}")
        return None

def _generate_new_device() -> dict:
    device_list = [
        ("Samsung", "SM-G998B", "Adreno (TM) 660", "Android OS 12 / API-31"),
        ("Xiaomi", "2201122G", "Adreno (TM) 730", "Android OS 13 / API-33"),
        ("Realme", "RMX3700", "Mali-G710", "Android OS 14 / API-34"),
        ("OnePlus", "CPH2451", "Adreno (TM) 740", "Android OS 13 / API-33"),
        ("OPPO", "CPH2611", "Adreno (TM) 720", "Android OS 14 / API-34"),
        ("Vivo", "V2203", "Mali-G710", "Android OS 12 / API-31"),
        ("Poco", "M2102J20SG", "Adreno (TM) 660", "Android OS 13 / API-33"),
    ]

    brand, model, gpu, os_ver = random.choice(device_list)

    return {
        "unique_device_id": f"Google|{uuid.uuid4()}",
        "brand": brand,
        "model": model,
        "gpu_renderer": gpu,
        "system_software": os_ver,
        "screen_width": random.choice([1080, 1440, 720, 1280]),
        "screen_height": random.choice([2400, 3200, 1600, 2400]),
        "screen_dpi": str(random.randint(300, 420)),
        "memory": random.randint(2800, 6500),
        "processor_details": (
            f"ARM64 FP ASIMD AES VMH | "
            f"{random.randint(2200, 3200)} | "
            f"{random.randint(6, 12)}"
        ),
        "client_ip": (
            f"{random.randint(103, 223)}."
            f"{random.randint(10, 250)}."
            f"{random.randint(10, 250)}."
            f"{random.randint(10, 250)}"
        ),
    }


def get_device_for_account(account_identifier: str) -> dict:
    """Load a saved device for this account, or generate and save one."""
    devices = {}

    if os.path.exists(DEVICE_FILE):
        try:
            with open(DEVICE_FILE, "r", encoding="utf-8") as f:
                devices = json.load(f)

            if not isinstance(devices, dict):
                devices = {}
        except (json.JSONDecodeError, OSError):
            devices = {}

    account_identifier = str(account_identifier)

    if account_identifier in devices:
        return devices[account_identifier]

    device_data = _generate_new_device()
    devices[account_identifier] = device_data

    temp_file = DEVICE_FILE + ".tmp"

    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(devices, f, indent=2, ensure_ascii=False)

    os.replace(temp_file, DEVICE_FILE)

    return device_data
    
async def version_config():
    try:
        resp = await client.get("https://clientbp.ggpolarbear.com/config/version", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return (
                data.get("release_version", _10L),
                data.get("client_version", "1.132.1"),
                data.get("server_url", "https://clientbp.ggpolarbear.com/")
            )
    except Exception:
        pass
    return _10L, "1.132.1", "https://clientbp.ggpolarbear.com/"

async def get_access_token(uid, password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    hdrs = {
        "Host": "100067.connect.garena.com",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 12; SM-G998B Build/SP1A.210812.016)",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"
    }
    data = {
        "uid": uid, "password": password,
        "response_type": "token", "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"
    }
    for attempt in range(5):
        try:
            response = await client.post(url, headers=hdrs, data=data)
            if response.status_code == 200:
                rd = response.json()
                open_id = rd.get("open_id")
                access_token = rd.get("access_token")
                platform = rd.get("platform", 4)
                if open_id and access_token:
                    return open_id, access_token, platform
            if response.status_code == 429:
                await asyncio.sleep(1)
                continue
        except Exception:
            pass
        await asyncio.sleep(0.5)
    return None

async def build_majorlogin_payload(open_id, access_token, platform, client_version, device_info, verr=None):
    try:
        if verr is None:
            verr = client_version
        
        str_plat = str(platform)
        int_plat = int(platform)

        proto = Major_Login_pb2.MajorLoginReq()
        proto.event_time = str(datetime.datetime.now())[:-7]
        proto.game_name = "free fire"
        proto.platform_id = int_plat
        proto.client_version = str(verr)
        proto.client_version_code = "2019121229"
        proto.system_software = str(device_info.get("system_software", "Android OS 15 / API-35 (AP3A.240905.015.A2/185014)"))
        proto.system_hardware = str(device_info.get("brand", "Handheld"))
        proto.device_type = str(device_info.get("model", "Handheld"))
        proto.screen_width = int(device_info.get("screen_width", 1600))
        proto.screen_height = int(device_info.get("screen_height", 719))
        proto.screen_dpi = str(device_info.get("screen_dpi", "234"))
        proto.processor_details = str(device_info.get("processor_details", "ARM64 FP ASIMD AES | 1820 | 8"))
        proto.memory = int(device_info.get("memory", 2798))
        proto.gpu_renderer = str(device_info.get("gpu_renderer", "Mali-G57"))
        proto.gpu_version = "OpenGL ES 3.2 v1.r49p1-04eac0.2848c17a2fd4e9340e06555168eaa3c9"
        proto.unique_device_id = str(device_info.get("unique_device_id", "Google|f744e396-5694-4e65-995d-97a958f2bd1f"))
        proto.client_ip = str(device_info.get("client_ip", "197.0.137.129"))
        proto.language = str(device_info.get("language", "pt-br"))
        proto.open_id = str(open_id)
        
        proto.open_id_type = str_plat
        proto.login_open_id_type = int_plat
        proto.access_token = str(access_token)
        proto.login_by = int(device_info.get("login_by", 2))
        proto.platform_sdk_id = int(device_info.get("platform_sdk_id", 1))
        proto.origin_platform_type = str_plat
        proto.primary_platform_type = str_plat
        
        proto.reg_avatar = 1
        proto.channel_type = 3
        proto.telecom_operator = "TUNTEL"
        proto.network_operator_a = "TUNTEL"
        proto.network_type = "WIFI"
        proto.network_type_a = "WIFI"
        proto.cpu_type = 2
        proto.cpu_architecture = "64"
        proto.graphics_api = "OpenGLES2"
        proto.supported_astc_bitset = 8191
        proto.client_using_version = "7428b253defc164018c604a1ebbfebdf"
        proto.loading_time = 15078
        proto.release_channel = "android"
        proto.extra_info = "KqsHTx3+QOmBRR1WKvaWewlcpqJBfjki+PPHQoQG8+0yV+Uos7gUFFjHMQ/e7u6han6Fl77r7c3vMN3p8UbKgN+nfycQCgwBmWgBzomx2gj84c+p"
        proto.android_engine_init_flag = 111207
        proto.if_push = 1
        proto.is_vpn = 0

        memory_available = proto.memory_available
        memory_available.version = 55
        memory_available.hidden_value = 81

        proto.external_storage_total = 49973
        proto.external_storage_available = 11338
        proto.internal_storage_total = 854
        proto.internal_storage_available = 11466
        proto.game_disk_storage_total = 49973
        proto.game_disk_storage_available = 11466
        proto.external_sdcard_total_storage = 49973
        proto.external_sdcard_avail_storage = 11466

        proto.library_path = "/data/app/~~lHFxTCCbupG2QVJmsURtZw==/com.dts.freefireth-N3aCHpHNXpdxjD80uIIbww==/lib/arm64"
        proto.library_token = "b8e0cd5e295eee42f5860d3c86e483dd|/data/app/~~lHFxTCCbupG2QVJmsURtZw==/com.dts.freefireth-N3aCHpHNXpdxjD80uIIbww==/base.apk"

        base_payload = proto.SerializeToString()
        extra = b""
        extra += _pb_field(96, '{"cur_rate":[90,60,120],"support_etc2":false}')
        extra += _pb_field(97, 1)
        extra += _pb_field(99, str_plat)
        extra += _pb_field(100, str_plat)
        extra += _pb_field(102, b"\x17]ENWU\x0eR5")
        extra += _pb_field(104, 52882)
        extra += _pb_field(105, 1)
        extra += _pb_field(106, "https://dl.ak.freefiremobile.com/live/ABHotUpdates/|https://core-ak.freefiremobile.com/live/ABHotUpdates/|6b2078db9d22dd98f8e9386a39af8462")
        extra += _pb_field(107, "c8e41b7a93f02d56e1a94c7b8203f5d1")

        full_payload = base_payload + extra
        return await aes_encrypt(full_payload, AES_KEY, AES_IV)
    except Exception as e:
        print(f"build_majorlogin_payload error: {e}")
        return None

async def send_majorlogin(data, release_version, server_url):
    try:
        url = f"{server_url}MajorLogin" if server_url.endswith('/') else f"{server_url}/MajorLogin"
        req_headers = headers.copy()
        req_headers["ReleaseVersion"] = str(release_version)
        response = await client.post(url, headers=req_headers, data=data)
        if response.status_code != 200:
            return None
        response_content = response.content
        if len(response_content) < 40:
            return None

        res_proto = Major_Login_pb2.MajorLoginRes()
        try:
            res_proto.ParseFromString(response_content)
        except Exception:
            pass

        dict_res = {}
        try:
            parsed = Parser().parse(response_content.hex())
            dict_res = await parse_results(parsed)
        except Exception:
            pass

        key_val = get_proto_field(dict_res, 22)
        iv_val = get_proto_field(dict_res, 23)
        if not key_val:
            key_val = res_proto.aes_ak
        if not iv_val:
            iv_val = res_proto.iv_i

        if isinstance(key_val, str):
            try: key_val = bytes.fromhex(key_val)
            except Exception: pass
        if isinstance(iv_val, str):
            try: iv_val = bytes.fromhex(iv_val)
            except Exception: pass

        if not key_val or not iv_val:
            for offset in range(min(128, len(response_content))):
                try:
                    candidate = Major_Login_pb2.MajorLoginRes()
                    candidate.ParseFromString(response_content[offset:])
                    if candidate.region and candidate.token:
                        res_proto = candidate
                        break
                except Exception:
                    pass
            try:
                parsed = Parser().parse(response_content.hex())
                dict_res = await parse_results(parsed)
                kv = get_proto_field(dict_res, 22)
                ivv = get_proto_field(dict_res, 23)
                if isinstance(kv, str):
                    try: kv = bytes.fromhex(kv)
                    except Exception: pass
                if isinstance(ivv, str):
                    try: ivv = bytes.fromhex(ivv)
                    except Exception: pass
                if kv: key_val = kv
                if ivv: iv_val = ivv
            except Exception:
                pass

        if key_val:
            try: res_proto.aes_ak = key_val
            except Exception: pass
        if iv_val:
            try: res_proto.iv_i = iv_val
            except Exception: pass

        return res_proto
    except Exception as e:
        log(f"[-] send_majorlogin error: {e}")
        return None

async def try_major_login_parallel(open_id, access_token, default_platform=4, client_version="1.132.1"):
    """⚡ Try multiple platforms (defaulting to platform 4 first) × multiple URLs."""
    platforms = [default_platform, 4]
    platforms = list(dict.fromkeys(platforms))  # remove duplicates
    device_info = get_device_for_account(open_id)

    for server_url in NEW_LOGIN_URLS:
        for platform in platforms:
            try:
                payload = await build_majorlogin_payload(
                    open_id, access_token, platform, client_version, device_info
                )
                if not payload:
                    continue
                print(f"[MAJORLOGIN] Trying platform={platform} url={server_url}")
                res = await send_majorlogin(payload, "OB55", server_url)
                if res and getattr(res, "token", None):
                    print(f"[MAJORLOGIN] ✓ SUCCESS | platform={platform} | region={res.region}")
                    return res, platform
            except Exception as e:
                print(f"[MAJORLOGIN] platform={platform} err: {e}")
                continue
    return None, None

async def process_account_uid_pass(uid: str, password: str):
    cache_file = os.path.join(ACCOUNT_CACHE_DIR, f"{uid}.json")
    
    device_data = get_device_for_account(uid)
    
    # Check if a valid cached account data file exists (less than 8 hours old)
    if os.path.exists(cache_file):
        if time.time() - os.path.getmtime(cache_file) < CACHE_DURATION:
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    acc_data = json.load(f)
                    
                    # Restore bytes if stored as hex strings
                    if isinstance(acc_data.get('aes_ak'), str):
                        try:
                            acc_data['aes_ak'] = bytes.fromhex(acc_data['aes_ak'])
                        except ValueError:
                            pass
                    if isinstance(acc_data.get('iv_i'), str):
                        try:
                            acc_data['iv_i'] = bytes.fromhex(acc_data['iv_i'])
                        except ValueError:
                            pass
                            
                    log(f"\033[32m[*] Loaded cached account session for UID: {uid} (Valid)\033[0m")
                    return acc_data
            except Exception as e:
                print(f"[DEBUG] Cache read error for account {uid}: {e}")

    log(f"\033[32m[*] Logging in UID: {uid}\033[0m")
    
    # Retry loop (up to 2 attempts)
    for attempt in range(1, 3):
        try:
            async with _LOGIN_SEMAPHORE:
                verconfig_res = await version_config()
                if verconfig_res is None:
                    if attempt < 2:
                        log(f"\033[33m[!] version_config failed for UID {uid}, retrying ({attempt}/2)...\033[0m")
                        await asyncio.sleep(1)
                        continue
                    return None
                release_version, client_version, server_url = verconfig_res

                # 1st step: Call get_access_token
                tokengrant_response = await get_access_token(uid, password)
                if tokengrant_response is None:
                    if attempt < 2:
                        log(f"\033[33m[!] OAuth failed for UID {uid}, retrying ({attempt}/2)...\033[0m")
                        await asyncio.sleep(1)
                        continue
                    log(f"\033[31m[-] OAuth failed for UID {uid}\033[0m")
                    return None
                open_id, access_token, platform = tokengrant_response

                # Print open_id and access_token
                print(f"[DEBUG] Open ID: {open_id}")
                print(f"[DEBUG] Access Token: {access_token}")

                # Try major login (using try_major_login_parallel)
                majorlogin_response, platform = await try_major_login_parallel(open_id, access_token, platform, client_version)
                if majorlogin_response is None or not getattr(majorlogin_response, 'token', None):
                    if attempt < 2:
                        log(f"\033[33m[!] MajorLogin failed for {uid}, retrying ({attempt}/2)...\033[0m")
                        await asyncio.sleep(1)
                        continue
                    log(f"\033[31m[-] MajorLogin failed for {uid}\033[0m")
                    return None

            acc_id = str(getattr(majorlogin_response, 'account_id', "0"))
            token = majorlogin_response.token

            account_data = {
                'account_id': acc_id,
                'open_id': open_id,
                'access_token': access_token,
                'platform': str(platform),
                'token': token,
                'server_time': getattr(majorlogin_response, 'server_time', int(time.time())),
                'aes_ak': getattr(majorlogin_response, 'aes_ak', AES_KEY),
                'iv_i': getattr(majorlogin_response, 'iv_i', AES_IV),
                'release_version': release_version,
                'client_version': client_version,
                'server_url': server_url,
                'auth_type': 'guest',
                'auth_uid': uid,
                'auth_password': password
            }

            # Save account_data to temp cache file (convert bytes to hex for JSON serialization)
            cache_data_to_save = account_data.copy()
            if isinstance(cache_data_to_save.get('aes_ak'), bytes):
                cache_data_to_save['aes_ak'] = cache_data_to_save['aes_ak'].hex()
            if isinstance(cache_data_to_save.get('iv_i'), bytes):
                cache_data_to_save['iv_i'] = cache_data_to_save['iv_i'].hex()

            try:
                with open(cache_file, "w", encoding="utf-8") as f:
                    json.dump(cache_data_to_save, f)
                log(f"\033[32m[*] Account session cached successfully for UID: {uid}\033[0m")
            except Exception as e:
                print(f"[DEBUG] Cache write error for account {uid}: {e}")

            return account_data
        except Exception as e:
            if attempt < 2:
                log(f"\033[33m[!] process_account_uid_pass error on attempt {attempt}/2 for {uid}: {e}, retrying...\033[0m")
                await asyncio.sleep(1)
                continue
            log(f"\033[31m[-] process_account_uid_pass error: {e}\033[0m")
            return None
    return None

def Extract_Full_Player_Profile(decrypted_bytes):
    try:
        res = data_pb2.PlayerPersonalShowRes()
        res.ParseFromString(decrypted_bytes)
        basic = getattr(res, 'basic_info', None)
        
        profile = {
            "name": getattr(basic, 'nickname', 'Unknown') if basic else 'Unknown',
            "region": getattr(basic, 'region', 'IND') if basic else 'IND',
            "level": int(getattr(basic, 'level', 0) if basic else 0),
            "likes": int(getattr(basic, 'likes', 0) if basic else 0)
        }
        
        if isinstance(profile["name"], bytes):
            profile["name"] = profile["name"].decode('utf-8', errors='ignore')
        if isinstance(profile["region"], bytes):
            profile["region"] = profile["region"].decode('utf-8', errors='ignore')
            
        return profile, "Success"
    except Exception as e:
        print(f"{C_RED}[DEBUG] Extract_Full_Player_Profile protobuf error: {e}{C_RESET}")
        return None, str(e)

def Fetch_Partner_Details(partner_uid, jwt, client_url):
    headers = {
        "Authorization": f"Bearer {jwt}",
        "Content-Type": _7H["Content-Type"],
        "User-Agent": _8A,
        "X-GA": _9R,
        "ReleaseVersion": _10L,
        "Connection": "Keep-Alive"
    }
    partner_info = {
        "nickname": "Unknown",
        "level": 0,
        "region": "Unknown",
        "likes": 0
    }
    
    try:
        payload = YOuR_FaThER(partner_uid)
        resp = requests.post(
            f"{client_url}/GetPlayerPersonalShow", 
            headers=headers, 
            data=payload, 
            timeout=_6T, 
            verify=False
        )
        if resp.status_code == 200:
            dec_data = UNknown(resp.content)
            res = data_pb2.PlayerPersonalShowRes()
            res.ParseFromString(dec_data)
            
            basic = getattr(res, 'basic_info', None)
            if basic:
                nickname_val = getattr(basic, 'nickname', 'Unknown')
                if isinstance(nickname_val, bytes):
                    partner_info["nickname"] = nickname_val.decode('utf-8', errors='ignore')
                elif isinstance(nickname_val, str) and nickname_val:
                    partner_info["nickname"] = nickname_val
                    
                partner_info["level"] = int(getattr(basic, 'level', 0))
                region_val = getattr(basic, 'region', 'Unknown')
                if isinstance(region_val, bytes):
                    partner_info["region"] = region_val.decode('utf-8', errors='ignore')
                elif isinstance(region_val, str) and region_val:
                    partner_info["region"] = region_val
                    
                partner_info["likes"] = int(getattr(basic, 'likes', 0))
    except Exception as e:
        print(f"{C_RED}[DEBUG] Fetch Partner Details error: {e}{C_RESET}")
        
    return partner_info

def No_NAMe(d, jwt, client_url):
    try:
        resp = _7P.SpecialFriendResponse()
        resp.ParseFromString(d)

        if not resp.HasField("duo_info"):
            print(f"{C_YELLOW}[DEBUG] No Dynamic Duo info found{C_RESET}")
            return None, "No Dynamic Duo info found"
            
        duo = resp.duo_info
        score = duo.score
        
        if score < 101: lvl = 1
        elif score < 301: lvl = 2
        elif score < 501: lvl = 3
        elif score < 801: lvl = 4
        elif score < 1201: lvl = 5
        else: lvl = 6
        
        status = "Active" if duo.status == 2 else "Inactive"
        partner_uid_str = str(duo.partner_uid)
        
        partner_details = Fetch_Partner_Details(partner_uid_str, jwt, client_url)
        nickname = duo.partner_nickname if duo.partner_nickname else partner_details["nickname"]

        return {
            "partner_uid": partner_uid_str,
            "partner_nickname": nickname,
            "partner_level": partner_details["level"],
            "partner_region": partner_details["region"],
            "partner_likes": partner_details["likes"],
            "duo_level": lvl,
            "duo_score": score,
            "days_active": duo.days_active,
            "creation_timestamp": duo.creation_timestamp,
            "status": status
        }, "Success"
    except Exception as e:
        print(f"{C_RED}[DEBUG] No_NAMe parsing error: {e}{C_RESET}")
        return None, str(e)

import json
import requests

async def search_duo_info(uid):
    uid = str(uid).strip()
    if not uid.isdigit():
        print(f"{C_RED}[!] Invalid UID provided!{C_RESET}")
        return

    print(f"\n{C_CYAN}[*] Searching Duo Info for UID: {uid}...{C_RESET}\n")

    for reg_key, cfg in REGION_CONFIGS.items():
        client_url = cfg["client_url"]
        try:
            acc_data = await process_account_uid_pass(cfg["uid"], cfg["password"])
            if not acc_data or not acc_data.get('token'):
                continue
                
            jwt = acc_data['token']
            headers = {
                "Authorization": f"Bearer {jwt}",
                "Content-Type": _7H["Content-Type"],
                "User-Agent": _8A,
                "X-GA": _9R,
                "ReleaseVersion": _10L,
                "Connection": "Keep-Alive"
            }
            
            main_payload = YOuR_FaThER(uid)
            main_resp = requests.post(
                f"{client_url}/GetPlayerPersonalShow", 
                headers=headers, 
                data=main_payload, 
                timeout=_6T, 
                verify=False
            )
            
            if main_resp.status_code == 200:
                main_dec = UNknown(main_resp.content)
                main_profile, _ = Extract_Full_Player_Profile(main_dec)
                
                if main_profile and main_profile.get("name") and main_profile.get("name") != "Unknown":
                    player_nickname = main_profile.get("name")
                    player_region = main_profile.get("region", reg_key)
                    player_level = main_profile.get("level", 0)
                    
                    resp = requests.post(
                        f"{client_url}/GetSpecialFriendList", 
                        headers=headers, 
                        data=main_payload, 
                        timeout=_6T, 
                        verify=False
                    )
                    
                    if resp.status_code == 200:
                        dec_data = UNknown(resp.content)
                        parsed, msg = No_NAMe(dec_data, jwt, client_url)
                        
                        aes_ak_val = acc_data.get('aes_ak')
                        if isinstance(aes_ak_val, bytes):
                            aes_ak_val = aes_ak_val.hex()
                        iv_i_val = acc_data.get('iv_i')
                        if isinstance(iv_i_val, bytes):
                            iv_i_val = iv_i_val.hex()

                        if parsed:
                            result_data = {
                                "success": True,
                                "player_nickname": player_nickname,
                                "uid": uid,
                                "region": player_region,
                                "level": player_level,
                                "partner_nickname": parsed.get("partner_nickname"),
                                "partner_uid": parsed.get("partner_uid"),
                                "partner_region": parsed.get("partner_region"),
                                "partner_level": parsed.get("partner_level"),
                                "partner_likes": parsed.get("partner_likes"),
                                "duo_score": parsed.get("duo_score"),
                                "duo_level": parsed.get("duo_level"),
                                "days_active": parsed.get("days_active"),
                                "status": parsed.get("status"),
                                "message": "Yes duo found this uid",
                                "ob_version": "OB55",
                                "Developer": "@XEROX_MODS",
                                "Telegram": "@SEXTYMODS",
                                "creation_timestamp": parsed.get("creation_timestamp"),
                                "aes_ak": aes_ak_val,
                                "iv_i": iv_i_val,
                                "release_version": acc_data.get('release_version'),
                                "client_version": acc_data.get('client_version'),
                                "server_url": acc_data.get('server_url')
                            }

                            print(f"""
{C_BOLD}{C_BRIGHT_MAGENTA}╔══════════════════════════════════════════════╗
{C_BRIGHT_CYAN}║              {C_BOLD}{C_GOLD}DUO INFO RESULTS{C_BRIGHT_CYAN}                ║
{C_BOLD}{C_BRIGHT_MAGENTA}╚══════════════════════════════════════════════╝{C_RESET}

{C_BOLD}{C_ORANGE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{C_RESET}
{C_BRIGHT_GREEN}Nickname       {C_BRIGHT_RED}:{C_RESET} {C_GOLD}{result_data.get('player_nickname', 'N/A')}{C_RESET}
{C_BRIGHT_CYAN}UID            {C_BRIGHT_RED}:{C_RESET} {C_PINK}{result_data.get('uid', 'N/A')}{C_RESET}
{C_BRIGHT_YELLOW}Region         {C_BRIGHT_RED}:{C_RESET} {C_SKY_BLUE}{result_data.get('region', 'N/A')}{C_RESET}
{C_BRIGHT_MAGENTA}Level          {C_BRIGHT_RED}:{C_RESET} {C_LIME}{result_data.get('level', 'N/A')}{C_RESET}
{C_BRIGHT_BLUE}Duo Found      {C_BRIGHT_RED}:{C_RESET} {C_BRIGHT_WHITE}{result_data.get('success', False)}{C_RESET}
{C_BRIGHT_GREEN}Partner Name   {C_BRIGHT_RED}:{C_RESET} {C_VIOLET}{result_data.get('partner_nickname', 'N/A')}{C_RESET}
{C_BRIGHT_CYAN}Partner UID    {C_BRIGHT_RED}:{C_RESET} {C_GOLD}{result_data.get('partner_uid', 'N/A')}{C_RESET}
{C_BRIGHT_YELLOW}Partner Region {C_BRIGHT_RED}:{C_RESET} {C_PINK}{result_data.get('partner_region', 'N/A')}{C_RESET}
{C_BRIGHT_MAGENTA}Partner Level  {C_BRIGHT_RED}:{C_RESET} {C_SKY_BLUE}{result_data.get('partner_level', 'N/A')}{C_RESET}
{C_BRIGHT_BLUE}Partner Likes  {C_BRIGHT_RED}:{C_RESET} {C_LIME}{result_data.get('partner_likes', 'N/A')}{C_RESET}
{C_BRIGHT_GREEN}Duo Score      {C_BRIGHT_RED}:{C_RESET} {C_GOLD}{result_data.get('duo_score', 'N/A')}{C_RESET}
{C_BRIGHT_CYAN}Duo Level      {C_BRIGHT_RED}:{C_RESET} {C_PINK}{result_data.get('duo_level', 'N/A')}{C_RESET}
{C_BRIGHT_YELLOW}Days Active    {C_BRIGHT_RED}:{C_RESET} {C_VIOLET}{result_data.get('days_active', 'N/A')}{C_RESET}
{C_BRIGHT_MAGENTA}Status         {C_BRIGHT_RED}:{C_RESET} {C_LIME}{result_data.get('status', 'N/A')}{C_RESET}
{C_BRIGHT_BLUE}Message        {C_BRIGHT_RED}:{C_RESET} {C_SKY_BLUE}{result_data.get('message', 'N/A')}{C_RESET}
{C_BRIGHT_GREEN}Version        {C_BRIGHT_RED}:{C_RESET} {C_GOLD}{result_data.get('ob_version', 'N/A')}{C_RESET}
{C_BRIGHT_CYAN}Created        {C_BRIGHT_RED}:{C_RESET} {C_SILVER}{result_data.get('creation_timestamp', 'N/A')}{C_RESET}
{C_BRIGHT_YELLOW}aes_ak         {C_BRIGHT_RED}:{C_RESET} {C_PINK}{result_data.get('aes_ak', 'N/A')}{C_RESET}
{C_BRIGHT_MAGENTA}iv_i            {C_BRIGHT_RED}:{C_RESET} {C_VIOLET}{result_data.get('iv_i', 'N/A')}{C_RESET}
{C_BRIGHT_BLUE}client_version {C_BRIGHT_RED}:{C_RESET} {C_LIME}{result_data.get('client_version', 'N/A')}{C_RESET}
{C_BRIGHT_GREEN}server_url     {C_BRIGHT_RED}:{C_RESET} {C_BG_CYAN}{result_data.get('server_url', 'N/A')}{C_RESET}
{C_BRIGHT_CYAN}Developer      {C_BRIGHT_RED}:{C_RESET} {C_GOLD}{result_data.get('Developer', 'N/A')}{C_RESET}
{C_BRIGHT_YELLOW}Telegram       {C_BRIGHT_RED}:{C_RESET} {C_PINK}{result_data.get('Telegram', 'N/A')}{C_RESET}
{C_BOLD}{C_ORANGE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{C_RESET}
""")
                        else:
                            result_data = {
                                "success": False,
                                "player_nickname": player_nickname,
                                "uid": uid,
                                "region": player_region,
                                "level": player_level,
                                "message": "No Duo/GF found for this UID",
                                "ob_version": "OB55",
                                "Developer": "@XEROX_MODS",
                                "Telegram": "@SEXTYMODS",
                                "creation_timestamp": 0,
                                "aes_ak": aes_ak_val,
                                "iv_i": iv_i_val,
                                "release_version": acc_data.get('release_version'),
                                "client_version": acc_data.get('client_version'),
                                "server_url": acc_data.get('server_url')
                            }

                            print(f"""
{C_MAGENTA}{C_BOLD}╔══════════════════════════════════════════════╗
{C_CYAN}║              {C_YELLOW}DUO INFO {C_CYAN}                ║
{C_MAGENTA}╚══════════════════════════════════════════════╝{C_RESET}

{C_BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{C_RESET}
{C_GREEN}Nickname       {C_RED}:{C_YELLOW} {result_data.get('player_nickname', 'N/A')}{C_RESET}
{C_CYAN}UID            {C_RED}:{C_MAGENTA} {result_data.get('uid', 'N/A')}{C_RESET}
{C_YELLOW}Region         {C_RED}:{C_BLUE} {result_data.get('region', 'N/A')}{C_RESET}
{C_MAGENTA}Level          {C_RED}:{C_GREEN} {result_data.get('level', 'N/A')}{C_RESET}
{C_BLUE}Message        {C_RED}:{C_CYAN} {result_data.get('message', 'N/A')}{C_RESET}
{C_GREEN}Version        {C_RED}:{C_YELLOW} {result_data.get('ob_version', 'N/A')}{C_RESET}
{C_CYAN}aes_ak          {C_RED}:{C_MAGENTA} {result_data.get('aes_ak', 'N/A')}{C_RESET}
{C_YELLOW}iv_i            {C_RED}:{C_BLUE} {result_data.get('iv_i', 'N/A')}{C_RESET}
{C_MAGENTA}client_version {C_RED}:{C_GREEN} {result_data.get('client_version', 'N/A')}{C_RESET}
{C_BLUE}server_url     {C_RED}:{C_BG_CYAN} {result_data.get('server_url', 'N/A')}{C_RESET}
{C_GREEN}Developer      {C_RED}:{C_YELLOW} {result_data.get('Developer', 'N/A')}{C_RESET}
{C_CYAN}Telegram       {C_RED}:{C_MAGENTA} {result_data.get('Telegram', 'N/A')}{C_RESET}
{C_BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{C_RESET}
""")
                        return
        except Exception as e:
            print(f"{C_RED}[DEBUG] Region {reg_key} error: {e}{C_RESET}")
            traceback.print_exc()
            continue
            
    print(f"\n{C_RED}[✗] UID not found in any region!{C_RESET}")



def main():
    banner()
    while True:
        try:
            target_uid = input(f"\n{C_YELLOW}{C_BOLD}Enter target UID: {C_RESET}").strip()
            if target_uid.lower() in ['exit', 'quit']:
                print(f"{C_BG_RED}Exiting... Goodbye!{C_RESET}")
                break
            if not target_uid:
                continue
            asyncio.run(search_duo_info(target_uid))
        except KeyboardInterrupt:
            print(f"\n{C_CYAN}Exiting... Goodbye!{C_RESET}")
            break

if __name__ == '__main__':
    main()
