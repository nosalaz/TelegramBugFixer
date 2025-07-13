# ai_responses.py
import logging
import random
from openai import OpenAI
import google.generativeai as genai
from config import OPENAI_API_KEY, GEMINI_API_KEY, RADIO_JAVAN_ACCESS_KEY
import requests

logger = logging.getLogger(__name__)

# Configure OpenAI with new client
openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

# Configure Gemini
gemini_model = None
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        gemini_model = genai.GenerativeModel('gemini-pro')
    except Exception as e:
        logger.warning(f"Failed to configure Gemini: {e}")
        gemini_model = None

async def get_ai_response(user_message: str, user_id: int) -> str:
    """Generates a general AI response using OpenAI or Gemini, personalized for Behnoush."""
    try:
        # Use OpenAI for general conversation
        if openai_client:
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "تو یک دستیار مهربان و دوستانه هستی که با لحن صمیمی و به فارسی پاسخ می‌دهی. اگر نام کاربر بهنوش است، با 'بهنوش جان' خطابش کن."},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=100,
                temperature=0.7
            )
            ai_text = response.choices[0].message.content.strip()
            return ai_text
        
        # Fallback to Gemini if OpenAI is not available
        elif gemini_model:
            try:
                response = gemini_model.generate_content(
                    f"کاربر: {user_message}\nربات (با لحن مهربان و دوستانه، به فارسی و با خطاب 'بهنوش جان' اگر نام کاربر بهنوش است):"
                )
                return response.text.strip()
            except Exception as e:
                logger.warning(f"Gemini API error: {e}")
                return "بهنوش جان، متاسفانه الان نمی‌تونم بهت پاسخ بدم. یه مشکل کوچیک پیش اومده. 😔"
        
        else:
            return "بهنوش جان، متاسفانه الان نمی‌تونم بهت پاسخ بدم. یه مشکل کوچیک پیش اومده. 😔"

    except Exception as e:
        logger.error(f"AI Response Error: {e}")
        return "بهنوش جان، متاسفانه الان نمی‌تونم بهت پاسخ بدم. یه مشکل کوچیک پیش اومده. 😔"

async def search_music(query: str) -> str:
    """Search for music using Radio Javan API."""
    API_URL = "https://api.ineo-team.ir/rj.php"
    params = {
        'accessKey': RADIO_JAVAN_ACCESS_KEY,
        'action': 'search',
        'query': query
    }
    
    try:
        response = requests.post(API_URL, data=params, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        if result.get('status_code') == 200:
            music_results = result.get('result', [])
            if music_results:
                response_text = "🎵 نتایج جستجو:\n"
                for i, music in enumerate(music_results[:3]):  # Limit to 3 results
                    title = music.get('title', 'نامشخص')
                    artist = music.get('artist', 'نامشخص')
                    response_text += f"{i + 1}. {title} - {artist}\n"
                return response_text
            else:
                return "بهنوش جان، متاسفانه هیچ نتیجه‌ای پیدا نشد. 🎵"
        else:
            return "بهنوش جان، متاسفانه در جستجو مشکلی پیش آمده است."

    except requests.exceptions.Timeout:
        logger.error("Radio Javan API timeout")
        return "بهنوش جان، جستجو خیلی طول کشید. لطفا دوباره امتحان کن."
    except requests.exceptions.RequestException as e:
        logger.error(f"Radio Javan API Error: {e}")
        return "بهنوش جان، متاسفانه در حال حاضر نمی‌تونم بهت کمک کنم. لطفا بعدا امتحان کن."
    except Exception as e:
        logger.error(f"Unexpected error in music search: {e}")
        return "بهنوش جان، یه خطای غیرمنتظره رخ داده. لطفا دوباره تلاش کن."

async def get_joke() -> str:
    """Generates a joke using OpenAI or a predefined list."""
    jokes = [
        "چرا کامپیوتر آهسته کار می‌کرد؟ چون رم کامپیوتر خوابش میومد! 💻😴",
        "آقا یه تمساح چطوری تابستون رو می‌گذرونه؟ با کولر کروکودیلی! 🐊❄️",
        "می‌دونی چرا دانشجوها ساندویچ دوست دارند؟ چون یه روز یه استاد گفت: هر کی تکلیفش رو نده ساندویچ میشه! 🥪📚",
        "بهنوش جان، می‌دونی چرا لک‌لک‌ها موقع خواب یه پاشون رو بالا نگه می‌دارن؟ چون اگه هر دو پاشون رو بذارن زمین، می‌افتن! 😂🦩"
    ]
    
    try:
        if openai_client:
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "یک جوک کوتاه و بامزه به فارسی بگو"},
                    {"role": "user", "content": "یه جوک بگو"}
                ],
                max_tokens=50,
                temperature=0.8
            )
            joke = response.choices[0].message.content.strip()
            return f"بهنوش جان، {joke} 😄"
        else:
            return random.choice(jokes)
    except Exception as e:
        logger.error(f"OpenAI Joke Error: {e}")
        return random.choice(jokes)

async def get_supportive_message() -> str:
    """Generates a supportive message using Gemini or a predefined list."""
    supportive_messages = [
        "تو خیلی قوی‌تر از این حرفایی! می‌دونم می‌تونی از پس هر چیزی بربیای. 💪",
        "بدونی که هر روز یه قدم به بهتر شدن نزدیک‌تر میشی؟ من همیشه اینجا هستم برات. 🌟",
        "زندگی مثل یه جعبه شکلاته، شاید بعضی مواقع مزه‌اش رو نفهمی اما هنوز شکلات‌های خوشمزه زیادی مونده! 🍫",
        "یادت باشه بهنوش جان، بعد از هر سختی، آسانی هست. من بهت ایمان دارم! 💖",
        "بهنوش عزیزم، لبخند تو قشنگ‌ترین چیزیه که می‌تونم ببینم. امیدوارم زودتر حالت خوب بشه. 😊"
    ]
    
    try:
        if gemini_model:
            response = gemini_model.generate_content(
                "یک پیام کوتاه، مثبت و امیدبخش به فارسی برای کسی که کمی ناراحت است، با خطاب 'بهنوش جان' بنویس:",
                generation_config=genai.types.GenerationConfig(
                    temperature=0.9,
                    max_output_tokens=80,
                )
            )
            message = response.text.strip()
            return message
        else:
            return random.choice(supportive_messages)
    except Exception as e:
        logger.error(f"Gemini Supportive Message Error: {e}")
        return random.choice(supportive_messages)
