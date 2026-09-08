import streamlit as st
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Future Predictor",
    page_icon="🔮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- MOBILE-FIRST GLASSMORPHISM CSS ---
st.markdown("""
<style>
    /* Global Base */
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .stApp {
        background-color: #f7f7f8;
        color: #1c1c1e;
    }

    /* Hide Streamlit Header/Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Mobile Container Padding Adjustment */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
        max-width: 500px !important;
    }

    /* Glassmorphic Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.75);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.9);
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
    }

    /* Titles */
    .main-title {
        font-size: 26px;
        font-weight: 700;
        text-align: center;
        color: #1c1c1e;
        margin-bottom: 2px;
    }
    .sub-title {
        font-size: 13px;
        text-align: center;
        color: #8e8e93;
        margin-bottom: 20px;
        font-style: italic;
    }

    /* Tags */
    .prediction-tag {
        display: inline-block;
        background-color: #f4efe6;
        color: #8a6d3b;
        font-size: 11px;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 10px;
        margin-bottom: 8px;
        border: 0.5px solid #e2d7c5;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Prediction Text */
    .prediction-text {
        font-size: 14px;
        color: #2c2c2e;
        line-height: 1.4;
        font-weight: 400;
        word-wrap: break-word;
    }

    /* Streamlit Button Styling */
    .stButton > button {
        width: 100%;
        background-color: #1c1c1e;
        color: #ffffff;
        border: none;
        padding: 12px 16px;
        border-radius: 12px;
        font-size: 15px;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transition: all 0.2s ease;
    }
    .stButton > button:active {
        transform: scale(0.98);
    }

    /* Inputs Mobile Styling */
    div[data-baseweb="input"] {
        border-radius: 10px !important;
    }

    /* Ending Text */
    .ending-container {
        text-align: center;
        padding: 15px 0;
        color: #636366;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# --- TAGS ---
TAGS = [
    "🧠 Personality",
    "📚 Study",
    "💰 Money",
    "👥 Friendship",
    "😂 Habits",
    "🚀 Career",
    "⚡ Secret Skill",
    "🔮 Final Future"
]

# --- 15 FRIENDS DATABASE (15 x 8 UNIQUE PREDICTIONS) ---
FRIENDS_DATABASE = {
    "shubham": [
        "Sabke samne serious hone ka naatak karta hai par andar se pure meme material hai.",
        "Exam ke ek raat pehle syllabus kholega aur kahega 'Bhai bas pass karwa de'.",
        "Paisa bachane mein expert hai, par momos dekhte hi saari savings khatam.",
        "Dosto ka Secret Keeper hai, par khud ke raaz kisi ko pata nahi chalne deta.",
        "Sote waqt alarm 10 baar snooze karna iska daily routine hai.",
        "Ek din apni khud ki tech company kholega jahan sabko free chai milegi.",
        "Bina dekhe phone par typing karne ki superhuman speed.",
        "Duniya ka sabse chill crorepati banne wala hai."
    ],
    "sagar": [
        "Khamosh rehta hai par jab bolta hai toh seedha mic-drop moment hota hai.",
        "Padhai karta nahi dikhega par result ke din marks sabse zyada aayenge.",
        "Stock market aur crypto ka gyaan sabko dega par khud ₹100 ki SIP karega.",
        "Har plan mein sabse late aayega par bolga 'Main toh raste mein hi hu'.",
        "Reels dekhte dekhte raat ke 3 bajana iska favourite sport hai.",
        "Bada hokar island khareedne ka plan hai iska.",
        "Kisi bhi argument ko 2 second mein khatam karne ki kala.",
        "Future mein sabse bada businessman banne ke 100% chances hain."
    ],
    "ayush": [
        "Energy level hamesha 200% rehta hai, kabhi thakta hi nahi.",
        "Padhai ke time par isko duniya bhar ke random facts yaad aate hain.",
        "Paise kharch karne mein dil dariya hai iska, party hamesha ready.",
        "Dost iske bina koi bhi trip plan nahi karte, asli raunak yahi hai.",
        "Ek hi gaana din mein 50 baar repeat mode par sunna.",
        "Cyber security expert ya game developer banega.",
        "Har game mein bina try kiye jeet jaane ki god-tier kismat.",
        "Future mein swag aur bank balance dono top par honge."
    ],
    "priyanshu": [
        "Dimaag se overthinker par shakal se bilkul innocent.",
        "Library mein baith kar reels scroll karne wala toppers list ka aadmi.",
        "Online shopping mein discounts dhundne ka champion.",
        "Group chat ka sabse active member jo har baat par roast karta hai.",
        "Subah uthte hi fir se sone ki planning karna.",
        "Aage chal kar kisi badi MNC ka Top Consultant banega.",
        "Kisi ka bhi jhoot 1 second mein pakad lene ki superpower.",
        "Aage chal kar luxuriously settle hone wala hai."
    ],
    "saksham": [
        "Hamesha confidence se bhara hua, chaye baat kuch bhi ho.",
        "Exam hall mein baith ke pure desh ki economy ke baare mein sochne wala.",
        "Paise investment mein lagayega aur double karega.",
        "Dosto ki ladai mein beech mein aake settlement karwane wala judge.",
        "Bina baat ke bathroom mein concert karna.",
        "Startup founder banega aur Forbes list mein aayega.",
        "Aankhon se sabka mood read kar lene ki talent.",
        "Duniya ghoomne wala international jet-setter banega."
    ],
    "sharansh": [
        "Pure vibes aur positive energy ka godown.",
        "Padhai mein 'Smart Work' par bharosa rakhta hai, Hard Work par nahi.",
        "Gullak mein paise jama karke direct iPhone khareedega.",
        "Har dost ko emotionally support dene wala asli yaar.",
        "Har 5 minute mein kitchen ka fridge khol kar check karna.",
        "Media ya Content Creation ka king banega.",
        "Kisi ko bhi 2 minute mein hasa dene ki ability.",
        "Life mein sirf happiness aur success likhi hai."
    ],
    "pawan": [
        "Ekdum calm aur composed personality, tension kabhi nahi leta.",
        "Last minute revision se topper banne ki ninja technique hai ispe.",
        "Paise ke mamle mein bohot calculation se chalta hai.",
        "Sabka loyal friend jo raat ke 2 baje bhi madad ko tayar rahe.",
        "Tea/Coffee ke bina iska system restart nahi hota.",
        "Government officer ya high-rank official banega.",
        "Liar ko pakadne mein CID se bhi tez.",
        "Future mein ek dum royal aur comfortable life jeeyega."
    ],
    "akshit": [
        "Thoda stylish, thoda nakhrebaaz, par dil ka saaf.",
        "Book kholte hi neend aane ka world record iske naam hai.",
        "Sneakers aur kapdo par saari pocket money udate hue dikhega.",
        "Dosto ke saath late night gedi marne ka shoukeen.",
        "Mirror ke samne akele hi pose dena.",
        "Creative Director ya Elite Designer banega.",
        "Game mein kisi ko bhi hara dene ke fast reflex.",
        "Future mein hamesha limelight mein rahega."
    ],
    "aditya": [
        "Logic aur facts ke bina koi baat nahi karta.",
        "Exam ke din sabko notes distribute karne wala messiah.",
        "Smart financial planning aur future investments ka master.",
        "Dosto ki help bina bole samajh jata hai.",
        "Ek hi baat ko 10 alag tareeqon se explain karna.",
        "AI Research ya Lead Software Engineer banega.",
        "Problem solving speed computer se bhi fast hai.",
        "Ek dum luxury villa aur dream cars ka owner banega."
    ],
    "priya": [
        "Sweet aur polite dikhti hai par roast karne mein master degree hai.",
        "Topper hone ka naatak nahi karti par marks hamesha top aate hain.",
        "Savings bohot acche se karti hai, smart investor.",
        "Sabki baatein sunne wali aur best advice dene wali friend.",
        "Online carts mein 100 cheezein add karke buy na karna.",
        "Corporate Boss ya Top HR Leader banegi.",
        "Multitasking mein koi iska muqabla nahi kar sakta.",
        "Future mein apni marzi ki queen ban kar rahegi."
    ],
    "avantika": [
        "Aesthetic vibes aur high taste waali personality.",
        "Padhai mein toppers se kam nahi par dikhati nahi.",
        "Branded cheezon par nazar rehti hai hamesha.",
        "Group ki saari gossips ka central hub.",
        "Photos khinchwane mein 100 take lena.",
        "Fashion Industry ya High-end Architect banegi.",
        "Aesthetic photos aur reels banane ki pro level skill.",
        "Future mein pure aesthetic aur classy lifestyle jeeyegi."
    ],
    "aman": [
        "Har waqt kisi na kisi adventure ke mood mein rehta hai.",
        "Exam pass karne ke liye bas 2 ghante ki padhai kaafi hai iske liye.",
        "Paise aate hi dosto par udata hai.",
        "Sabka favourite dost jiske bina group bore lagta hai.",
        "Bina wajah raat ko 3 baje maggi banana.",
        "Travel Vlogger ya Automobile Engineer banega.",
        "Kisi bhi gaadi ko kisi bhi jagah park kar lene ka talent.",
        "Duniya ke har kone mein ghoomne wala traveller banega."
    ],
    "prapti": [
        "Quiet exterior par super sharp and clever mind.",
        "Padhai mein bina kisi shor ke top karti hai.",
        "Smart budget planner, faltu kharcha zero.",
        "Ek do dosto ke sath hi deeply connected rehti hai.",
        "Novel ya web series ek hi din mein binge-watch karna.",
        "Data Scientist ya Top Research Scholar banegi.",
        "Baaton hi baaton mein samne wale ka dimaag padh lena.",
        "Future mein bohot shanti aur wealth dono milegi."
    ],
    "nancy": [
        "Super friendly aur har kisi se baat karne mein expert.",
        "Study notes bohot neat aur colourful banati hai.",
        "Cute items aur stationery par paise kharch karna.",
        "Sabke birthday yaad rakhne wali group ki memory card.",
        "Baat baat par smile karna aur dosto ko tang karna.",
        "Marketing Head ya PR Specialist banegi.",
        "Kisi bhi gussa aadmi ko 1 minute mein manane ki skill.",
        "Future mein bohot famous aur respected person banegi."
    ],
    "anurag": [
        "Backbencher energy, front-bencher brain.",
        "Padhai exam se 1 ghante pehle shuru karta hai aur rock karta hai.",
        "Dhandha karne ke tarike sochta rehta hai.",
        "Dosto ke har lafde mein sabse aage khada hone wala.",
        "Mobile gaming mein continuous streak banana.",
        "Serial Entrepreneur banega jo multiple businesses chalayega.",
        "Kisi bhi tough situation se nikalne ka jugaad dhundna.",
        "Future mein khud ka samrajya (empire) khada karega."
    ]
}

# --- HOME SCREEN ---
st.markdown("<div class='main-title'>🔮 Future Predictor</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>“Your future has already been recorded.”</div>", unsafe_allow_html=True)

# Input Section
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
user_name = st.text_input("ENTER YOUR NAME", placeholder="Type your name...", key="name_in")
user_age = st.number_input("ENTER YOUR AGE", min_value=1, max_value=120, value=20, step=1, key="age_in")
submit_button = st.button("Reveal My Future ✦")
st.markdown("</div>", unsafe_allow_html=True)

# --- PROCESS & RESULT DISPLAY ---
if submit_button:
    if not user_name.strip():
        st.warning("Kripya apna naam enter karein!")
    else:
        clean_name = user_name.strip().lower()

        # Loading animation
        loading_placeholder = st.empty()
        progress_bar = st.progress(0)

        loading_messages = [
            "Identifying subject...",
            "Searching the Future Archive...",
            "Consulting the ancient database...",
            "Checking destiny...",
            "Cross-checking the timeline...",
            "Finalizing the prediction...",
            "Future locked...",
            "Prediction ready..."
        ]

        step_delay = 1.8 / len(loading_messages)
        for idx, msg in enumerate(loading_messages):
            loading_placeholder.markdown(f"<p style='text-align: center; color: #8e8e93; font-size: 13px;'>{msg}</p>", unsafe_allow_html=True)
            progress_bar.progress((idx + 1) / len(loading_messages))
            time.sleep(step_delay)

        loading_placeholder.empty()
        progress_bar.empty()

        # Database Check
        if clean_name in FRIENDS_DATABASE:
            predictions = FRIENDS_DATABASE[clean_name]

            st.markdown("<div class='glass-card' style='text-align: center;'>", unsafe_allow_html=True)
            st.markdown("<h3 style='margin:0; font-size:20px;'>🔮 Your Future</h3>", unsafe_allow_html=True)
            st.markdown("<span style='color: #8e8e93; font-size: 12px;'>The Future Archive has revealed your recorded future.</span>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # Display all 8 predictions
            for tag, pred_text in zip(TAGS, predictions):
                st.markdown(f"""
                <div class='glass-card'>
                    <div class='prediction-tag'>{tag}</div>
                    <div class='prediction-text'>{pred_text}</div>
                </div>
                """, unsafe_allow_html=True)

            # Ending
            st.markdown("""
            <div class='ending-container'>
                <p style='margin-bottom: 2px;'>Aapka future ye raha. ✨</p>
                <p style='font-weight: 600; color: #1c1c1e;'>Milte hain future mein. 👋🔮</p>
            </div>
            """, unsafe_allow_html=True)

        else:
            # Unknown Name
            st.markdown("""
            <div class='glass-card' style='text-align: center; padding: 24px;'>
                <h3 style='margin-top:0;'>🔮 Future Archive</h3>
                <p style='color: #3a3a3c; font-size: 14px; line-height: 1.5;'>
                    Future Archive ko is naam ka record nahi mila.<br><br>
                    Lagta hai iska future abhi secret rakha gaya hai. 😂
                </p>
            </div>
            """, unsafe_allow_html=True)


