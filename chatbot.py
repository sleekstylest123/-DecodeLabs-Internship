import os
"""
NexBot v3.0 — Advanced Rule-Based AI Chatbot
Run : py chatbot.py
Open: http://127.0.0.1:5000
"""

from flask import Flask, request, jsonify
import re, random, math as _math
from datetime import datetime

app = Flask(__name__)
user_sessions = {}

# ══════════════════════════════════════════════════════════
#  KEYWORD BANKS
# ══════════════════════════════════════════════════════════
GREETINGS   = ["hello","hi","hey","howdy","what's up","sup","greetings","good morning","good evening","good afternoon","hiya","yo","wassup","whats up"]
FAREWELLS   = ["bye","goodbye","exit","quit","see you","later","take care","farewell","cya","good night","ttyl","see ya","adios"]
THANKS      = ["thanks","thank you","thx","ty","appreciate","grateful","cheers","thank u","many thanks"]
INSULTS     = ["stupid","dumb","idiot","hate you","useless","terrible","worst","trash","garbage","awful","horrible"]
HOW_ARE_YOU = ["how are you","how r u","how are u","you okay","are you okay","how do you feel","how's it going","how are things","you good","hows life"]
JOKES       = ["tell me a joke","joke","make me laugh","say something funny","funny","humor me","crack a joke","give me a joke","another joke"]
HELP        = ["help","what can you do","commands","options","guide","menu","features","what do you know","capabilities"]
AGE         = ["how old are you","your age","when were you born","age"]
NAME_BOT    = ["your name","who are you","what are you","what's your name","introduce yourself","tell me about yourself"]
WEATHER     = ["weather","temperature","rain","sunny","forecast","climate","hot outside","cold outside","is it raining","will it rain"]
TIME_DATE   = ["time","date","today","current time","what day","what year","what month","what's the date","tell me the time"]
CREATOR     = ["who made you","who created you","who built you","your creator","your developer","who programmed you","who designed you"]
LOVE        = ["i love you","i like you","you're great","you're awesome","you're amazing","you rock","best bot","i adore you","you're the best"]
BORED       = ["i'm bored","im bored","bored","nothing to do","entertain me","i have nothing to do","so bored","feeling bored"]
CAPITAL     = ["capital of","what is the capital","capital city"]
SAD         = ["i'm sad","im sad","i feel sad","feeling down","depressed","unhappy","i'm crying","feeling low","i feel bad","i'm upset","im upset","feel awful"]
HAPPY       = ["i'm happy","im happy","i feel great","feeling good","i'm excited","great day","wonderful","i'm joyful","feeling amazing","best day"]
HUNGRY      = ["i'm hungry","im hungry","food","eat","starving","what should i eat","meal","i want to eat","whats for dinner","whats for lunch"]
TIRED       = ["i'm tired","im tired","sleepy","exhausted","i need sleep","feeling tired","so tired","very tired","cant sleep"]
STUDY       = ["help me study","study tips","how to study","exam tips","learning tips","study help","how to learn","i have exam","exam tomorrow"]
MOTIVATION  = ["motivate me","motivation","i want to give up","inspire me","i can't do this","encourage me","i feel like quitting","feeling unmotivated","give up"]
PYTHON      = ["python","what is python","tell me about python","python language","learn python","python programming"]
AI          = ["what is ai","artificial intelligence","tell me about ai","what is machine learning","ai chatbot","deep learning","neural network"]
FACT        = ["tell me a fact","random fact","fun fact","interesting fact","did you know","give me a fact","wow fact"]
RIDDLE      = ["tell me a riddle","riddle","brain teaser","puzzle","quiz me","give me a riddle"]
COMPLIMENT  = ["you are smart","you're smart","you're helpful","you're intelligent","good bot","nice bot","cool bot","well done","great job","impressive"]
MEANING_LIFE= ["meaning of life","purpose of life","why are we here","what is life","42","life meaning"]
ADVICE      = ["give me advice","life advice","advice","what should i do","tip for life","words of wisdom","wise words"]
PROGRAMMING = ["what is programming","coding","software","developer","learn coding","learn to code","what is coding"]
MUSIC       = ["music","song","playlist","what music","recommend music","i love music","favourite song","best songs"]
SPORT       = ["football","cricket","sport","soccer","basketball","tennis","favourite sport","sports"]
SPACE       = ["space","universe","galaxy","stars","planets","nasa","moon","solar system","black hole","mars"]
HEALTH      = ["health tips","healthy","fitness","exercise","gym","workout","how to be healthy","diet tips","stay fit"]
COUNTRIES   = ["how many countries","countries in the world","world countries","total countries"]
LANGUAGE    = ["how many languages","world languages","languages spoken","total languages"]
INTERNET    = ["what is internet","who invented internet","history of internet","internet"]
COMPUTER    = ["what is computer","history of computer","computer science","who invented computer"]
READING     = ["reading tips","how to read faster","improve reading","read more books","book recommendation"]
MINDFULNESS = ["stress","anxiety","calm down","i'm stressed","im stressed","feeling anxious","panic","overwhelmed","cant breathe","mental health"]
FINANCE     = ["money","save money","budgeting","financial tips","how to save","investment","earn money","personal finance","rich","wealthy","income","expenses"]
CAREER      = ["career advice","job tips","interview tips","how to get a job","resume","cv","job hunt","career growth","promotion","workplace"]
FOOD        = ["recipes","cooking tips","how to cook","what to cook","easy recipes","cook for beginners","baking","kitchen tips","meal prep"]
TRAVEL      = ["travel tips","where to travel","best places to visit","travel advice","tourist","vacation","trip planning","travel hacks"]
SCIENCE     = ["science","physics","chemistry","biology","scientific","evolution","atom","dna","gravity","what is science"]
HISTORY     = ["history","historical","ancient","world war","civilizations","who invented","when was","tell me about history"]
ENVIRONMENT = ["climate change","environment","global warming","eco friendly","save earth","recycle","pollution","green energy","renewable"]
RELATIONSHIPS = ["relationship advice","friendship","love advice","how to make friends","communication tips","social skills","how to be confident"]
SLEEP       = ["sleep tips","how to sleep better","insomnia","cant sleep","sleep schedule","sleeping problems","improve sleep quality"]
PRODUCTIVITY= ["productivity tips","time management","how to be productive","procrastination","focus tips","get things done","work efficiently","stop procrastinating"]

JOKES_LIST = [
    "Why don't scientists trust atoms? Because they make up everything! 😄",
    "Why did the computer go to the doctor? Because it had a virus! 💻😷",
    "Why do programmers prefer dark mode? Because light attracts bugs! 🐛🌑",
    "I told my computer I needed a break. Now it won't stop sending me Kit-Kat ads. 🍫😂",
    "Why do Java developers wear glasses? Because they don't C#! 👓😆",
    "How many programmers does it take to change a light bulb? None — that's a hardware problem! 💡🤣",
    "Why was the math book sad? It had too many problems! 📚😢",
    "What do you call a fake noodle? An impasta! 🍝😂",
    "Why can't your nose be 12 inches long? Because then it would be a foot! 👃😄",
    "I asked my dog what 2 minus 2 is. He said nothing. 🐶😂",
    "Why did the scarecrow win an award? Because he was outstanding in his field! 🌾🏆",
    "What do you call cheese that isn't yours? Nacho cheese! 🧀😄",
    "Why did the bicycle fall over? Because it was two-tired! 🚲😂",
    "What do you call a sleeping dinosaur? A dino-snore! 🦕😴",
    "Why did the student eat his homework? The teacher told him it was a piece of cake! 🎂📚",
    "How does a penguin build its house? Igloos it together! 🐧🏠",
    "What's a computer's favourite snack? Microchips! 🍟💻",
    "Why did the cookie go to the doctor? Because it was feeling crummy! 🍪😷",
    "What do you call a fish without eyes? A fsh! 🐟😂",
    "I'm reading a book about anti-gravity. It's impossible to put down! 📖🚀",
]

FACTS_LIST = [
    "Honey never spoils — archaeologists found 3000-year-old honey in Egyptian tombs! 🍯🏺",
    "Octopuses have three hearts and blue blood! 🐙💙",
    "A group of flamingos is called a 'flamboyance'! 🦩✨",
    "Bananas are technically berries, but strawberries are not! 🍌🍓",
    "The Eiffel Tower grows about 6 inches taller in summer due to heat expansion! 🗼☀️",
    "A day on Venus is longer than a year on Venus! 🪐⏳",
    "Cleopatra lived closer in time to the Moon landing than to the Great Pyramid! 🏛️🚀",
    "The human brain uses about 20% of the body's total energy! 🧠⚡",
    "A snail can sleep for 3 years! 🐌💤",
    "The shortest war in history lasted only 38–45 minutes! ⚔️⏱️",
    "Sharks are older than trees — they've existed for over 400 million years! 🦈🌳",
    "There are more possible chess games than atoms in the observable universe! ♟️🌌",
    "Your body has more bacterial cells than human cells! 🦠😱",
    "The average person walks about 100,000 miles in their lifetime — four times around Earth! 🌍👣",
    "Hot water freezes faster than cold water — this is called the Mpemba effect! 🔥❄️",
    "A group of crows is called a murder. A group of owls is called a parliament! 🐦🦉",
    "Wombat poop is cube-shaped — the only animal whose feces is cubic! 🐨📦",
    "The dot above the letters 'i' and 'j' is called a tittle! 🔤✨",
    "Cows have best friends and get stressed when separated from them! 🐄💕",
    "The inventor of the frisbee was turned into a frisbee after death — he was cremated and his ashes made into one! 🥏😂",
]

RIDDLES = [
    ("I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?", "An echo! 🔊"),
    ("The more you take, the more you leave behind. What am I?", "Footsteps! 👣"),
    ("I have cities, but no houses live there. I have mountains, but no trees grow. I have water, but no fish swim. What am I?", "A map! 🗺️"),
    ("What has hands but can't clap?", "A clock! ⏰"),
    ("I'm light as a feather, but even the strongest person can't hold me for more than 5 minutes. What am I?", "Breath! 💨"),
    ("What gets wetter the more it dries?", "A towel! 🏖️"),
    ("I have keys but no locks. I have space but no room. You can enter but can't go inside. What am I?", "A keyboard! ⌨️"),
    ("What can travel around the world while staying in a corner?", "A stamp! 📮"),
    ("The more you remove from me, the bigger I become. What am I?", "A hole! 🕳️"),
    ("I'm always in front of you but can't be seen. What am I?", "The future! 🔮"),
    ("I have a head and a tail but no body. What am I?", "A coin! 🪙"),
    ("What has to be broken before you can use it?", "An egg! 🥚"),
]

ADVICE_LIST = [
    "Work smart, not just hard. Focus on what matters most! 🎯",
    "Never stop learning — the day you stop learning is the day you stop growing! 📚🌱",
    "Take care of your health. Everything else follows from that! 💪🧘",
    "Be kind to others — you never know what battles they're fighting! 💙",
    "Consistency beats talent when talent doesn't work consistently! 🔥",
    "Surround yourself with people who push you to be better! 🌟👥",
    "Fail fast, learn faster. Mistakes are tuition fees for success! 💡",
    "Your time is your most valuable resource — spend it wisely! ⏰🌟",
    "Write down your goals. People who write goals are 42% more likely to achieve them! ✍️🎯",
    "Start before you're ready. Waiting for the perfect moment is the biggest trap! 🚀",
    "Invest in yourself first — knowledge and skills compound like interest! 📈🧠",
    "It's okay to say no. Protecting your time and energy is self-respect! 🛡️",
    "Compare yourself only to who you were yesterday, not to others! ⚡",
    "One small positive thought in the morning can change your whole day! ☀️💭",
]

MUSIC_LIST = [
    "🎵 **Lo-fi Hip Hop** — Perfect for studying and deep focus! Channels: ChilledCow, Lofi Girl on YouTube",
    "🎸 **Classic Rock** — Timeless energy: Led Zeppelin, Queen, Pink Floyd, The Beatles",
    "🎹 **Film Scores** — Hans Zimmer (Interstellar, Inception), Ennio Morricone — pure emotion!",
    "🎤 **Pop Upbeat** — Great for workouts: Dua Lipa, The Weeknd, Harry Styles",
    "🎷 **Jazz** — Miles Davis, John Coltrane — relaxing, intelligent, timeless",
    "🎻 **Classical Music** — Mozart, Beethoven, Chopin — proven to boost concentration!",
    "🥁 **Hip Hop** — Eminem, Kendrick Lamar, J. Cole — lyrically brilliant",
    "🎧 **Ambient/Electronic** — Brian Eno, Boards of Canada — great for creative work",
    "🎺 **R&B & Soul** — Stevie Wonder, Aretha Franklin, SZA — pure emotion",
    "🌍 **World Music** — Fela Kuti, Buena Vista Social Club — broaden your musical horizons!",
]

HEALTH_TIPS = [
    "💧 **Hydration**: Drink 8 glasses of water daily. Dehydration causes fatigue, headaches & poor focus!",
    "🚶 **Daily Walking**: 30 mins of walking burns calories, boosts mood, and reduces heart disease risk by 35%!",
    "😴 **Quality Sleep**: 7-9 hours of sleep is non-negotiable. Sleep deprivation impairs you like being drunk!",
    "🥦 **Eat the Rainbow**: Each color vegetable provides unique nutrients. Aim for 5 colors on your plate daily!",
    "🧘 **Breathe**: 5 mins of deep breathing daily reduces cortisol (stress hormone) significantly!",
    "📵 **Screen Detox**: Blue light from screens before bed suppresses melatonin. Stop screens 1 hr before sleep!",
    "🏃 **Exercise**: Even 20 mins of moderate exercise releases endorphins — your brain's natural antidepressant!",
    "🥗 **Meal Timing**: Eating slowly and mindfully reduces overeating. Your brain takes 20 mins to register fullness!",
    "🦷 **Oral Health**: Brushing teeth twice daily is linked to lower risk of heart disease and diabetes!",
    "🌞 **Sunlight**: 15-20 mins of morning sunlight regulates your circadian rhythm and boosts vitamin D!",
    "🧴 **Posture**: Sitting straight reduces back pain, improves confidence, and boosts testosterone by 20%!",
    "🍵 **Limit Sugar**: Excess sugar causes inflammation, energy crashes, and is linked to depression!",
]

STUDY_TIPS = [
    "⏱️ **Pomodoro Technique**: Study 25 mins → break 5 mins. After 4 cycles, take a longer 20-min break! Your focus compounds!",
    "✏️ **Handwrite Notes**: Writing by hand beats typing for memory retention by up to 40%. Your brain encodes better!",
    "🔁 **Spaced Repetition**: Review material after 1 day, 3 days, 1 week, 2 weeks. This is how memory becomes permanent!",
    "🧪 **Active Recall**: Close your notes and try to recall everything. This is 3x more effective than re-reading!",
    "🎯 **Single-Subject Focus**: Study one topic at a time. Multitasking reduces efficiency by 40% due to context switching!",
    "😴 **Sleep After Studying**: Your brain consolidates memory during sleep. Studying before bed improves retention!",
    "🏫 **Teach What You Learn**: Explain concepts to someone else (or a rubber duck!). If you can teach it, you know it!",
    "🗺️ **Mind Mapping**: Draw concept maps connecting ideas. Visual learning activates different brain regions!",
    "📍 **Study Environment**: Always study in the same place. Your brain associates that space with focus!",
    "🎵 **Background Music**: Classical or lo-fi music without lyrics boosts concentration. Lyrics compete with your reading brain!",
    "💧 **Stay Hydrated**: Even 1-2% dehydration reduces cognitive performance. Keep water at your study desk!",
    "❓ **Question Everything**: Convert your notes into questions. 'Why does X happen?' trains deeper understanding!",
]

MOTIVATION_LIST = [
    "Every expert was once a beginner. Keep going! 💪🔥",
    "You didn't come this far to only come this far. Push through! 🚀✨",
    "Progress, not perfection. One step at a time! 🌟👣",
    "The harder you work, the luckier you get! 🍀💼",
    "Believe in yourself — you are more capable than you think! 🧠💫",
    "Your only competition is who you were yesterday! ⚡🏆",
    "The secret to getting ahead is getting started! 🎯🔑",
    "Difficult roads often lead to beautiful destinations! 🛤️🌄",
    "Success is not final, failure is not fatal — it's the courage to continue that counts! 🦁",
    "You have exactly the same hours in a day as Einstein, Da Vinci, and Newton! ⏰🌟",
    "The pain of discipline weighs ounces. The pain of regret weighs tons! ⚖️🎯",
    "A year from now you'll wish you had started today! 📅🚀",
    "Champions keep going when they don't have anything left! 🏆💪",
    "The only way to do great work is to love what you do! ❤️💡",
    "Dream big, start small, act now! 🌠👣🔥",
    "Your attitude, not your aptitude, will determine your altitude! 🚁🌟",
]

BORED_SUGGESTIONS = [
    "Try learning Python today — write a calculator in 10 lines! 🐍💻",
    "How about a walk outside? Even 15 minutes resets your brain! 🌿🚶",
    "Ask me for a riddle and challenge your brain! 🧩🎯",
    "Try building a small project — even a to-do list app is great portfolio practice! 💡",
    "Listen to a new music genre you've never tried before! 🎵🎧",
    "Read 10 pages of any book — start a tiny habit today! 📚✨",
    "Learn one new keyboard shortcut — small skills compound over time! ⌨️",
    "Watch a documentary — some great ones: Planet Earth, The Social Dilemma, Cosmos! 🎬🌍",
    "Write in a journal for 5 minutes — it's scientifically proven to reduce stress! 📓✍️",
    "Call a friend you haven't spoken to in a while! 📞💙",
    "Learn 5 words in a new language on Duolingo! 🌐📖",
    "Do a 10-minute workout — search '10 minute abs' on YouTube! 💪🔥",
]

FINANCE_TIPS = [
    "💰 **50/30/20 Rule**: Spend 50% on needs, 30% on wants, 20% on savings. Start tracking your expenses today!",
    "📈 **Invest Early**: If you invest $100/month at 25 with 8% return, you'll have $349,000 by 65. Start NOW!",
    "🏦 **Emergency Fund**: Build a 3-6 month expense emergency fund before any investments. Security first!",
    "💳 **Avoid Bad Debt**: Credit card debt at 20% interest is financial poison. Pay it off first, always!",
    "📊 **Track Spending**: Use apps like YNAB or just a simple spreadsheet. You can't manage what you don't measure!",
    "🛒 **Avoid Lifestyle Inflation**: When your income rises, don't immediately raise expenses. Save the difference!",
    "📚 **Read About Finance**: 'Rich Dad Poor Dad', 'The Psychology of Money', 'The Millionaire Next Door' — game changers!",
    "🎯 **Automate Savings**: Set up automatic transfers to savings the day you get paid. Pay yourself first!",
]

CAREER_TIPS = [
    "📄 **Resume Tips**: Tailor your CV for each job. Use keywords from the job description. Quantify achievements (e.g., 'grew sales by 30%')!",
    "🤝 **Networking**: 80% of jobs are filled through networking. Attend events, use LinkedIn, reach out to people in your field!",
    "🎤 **Interview Prep**: Research the company deeply. Prepare STAR stories (Situation, Task, Action, Result) for behavioral questions!",
    "📚 **Never Stop Upskilling**: The most employable people learn continuously. Online courses, certifications, side projects stand out!",
    "💬 **Communication Matters**: Clear writing and speaking are top skills employers want. Practice explaining complex things simply!",
    "🌐 **Build Your Online Presence**: A strong LinkedIn and GitHub/portfolio dramatically improves your chances in tech!",
    "🤲 **Ask for Feedback**: After interviews or reviews, ask for specific feedback. Growth-minded candidates are remembered!",
    "💡 **Show Initiative**: Don't wait to be told what to do. Proactive employees get promoted faster than reactive ones!",
]

FOOD_TIPS = [
    "🍳 **Cooking Basics**: Master 5 fundamental techniques — sautéing, roasting, boiling, grilling, and baking. Everything else builds on these!",
    "🧂 **Season Properly**: Salt is not just for saltiness — it enhances all flavors. Add salt at each stage of cooking, not just at the end!",
    "🔪 **Knife Skills**: A sharp knife is safer than a dull one. Learn basic cuts: dice, julienne, chiffonade. It changes everything!",
    "🍅 **Fresh Ingredients**: Fresh produce cooked simply beats processed food every time. Shop local when possible!",
    "🥩 **Rest Your Meat**: Always let cooked meat rest 5-10 minutes before cutting. This keeps juices in and flavor in!",
    "🌿 **Herbs & Spices**: Learn to use fresh herbs. Basil, cilantro, parsley, and thyme transform simple dishes into restaurant quality!",
    "🍜 **Meal Prep Sundays**: Cook grains, proteins, and veggies in batches on Sunday. It saves 4-5 hours of cooking during the week!",
    "🥚 **Eggs Are Magic**: Learn to make perfect scrambled eggs, omelettes, and poached eggs. They're quick, cheap, and nutritious!",
]

TRAVEL_TIPS = [
    "✈️ **Book Smart**: Use Google Flights, set price alerts. Tuesday/Wednesday flights are often cheapest. Book 6-8 weeks ahead for domestic!",
    "🎒 **Pack Light**: Master the one-bag method. You'll move faster, avoid checked bag fees, and never lose luggage!",
    "🗺️ **Research Before**: Learn 5-10 phrases in the local language. Locals LOVE the effort, and it transforms your experience!",
    "💳 **Travel Card**: Get a no-foreign-transaction-fee credit card. You lose 3% on every purchase without one!",
    "🏨 **Accommodation Mix**: Mix hostels, Airbnb, and local guesthouses. You'll save money AND get more authentic experiences!",
    "📷 **Travel Slow**: Visiting fewer places deeply beats rushing through many. Spend at least 3 days in each city!",
    "🌍 **Off-Season Travel**: Visiting in shoulder season (just before/after peak) saves 30-50% and means fewer crowds!",
    "🧳 **Always Buy Travel Insurance**: One medical emergency abroad without insurance can cost more than 10 trips combined!",
]

SCIENCE_FACTS = [
    "⚛️ **Quantum World**: Electrons exist in multiple states simultaneously until observed — this is called quantum superposition!",
    "🧬 **DNA**: Your DNA, if uncoiled and stretched, would reach from Earth to Pluto and back — 17 times!",
    "🌌 **Scale of Universe**: If the Milky Way were the size of Europe, our solar system would be smaller than a grain of sand!",
    "⚡ **Speed of Light**: Light travels 299,792 km per second. It takes 8 minutes to reach Earth from the Sun!",
    "🧪 **Elements**: Everything in the universe is made of just 118 elements — including you, stars, and planets!",
    "🌊 **Ocean Pressure**: At the deepest ocean point (Mariana Trench), pressure is 1,086 bar — like 50 jumbo jets on your thumb!",
    "🔬 **Cells**: Your body replaces 330 billion cells daily. You are literally not the same person you were a year ago!",
    "🌡️ **Absolute Zero**: The coldest possible temperature is -273.15°C. Nothing can be colder — atoms stop moving completely!",
]

HISTORY_FACTS = [
    "🏛️ **Ancient Rome**: At its peak, Rome had a population of 1 million — it took Europe until 1800 to reach that again!",
    "⚔️ **Shortest War**: The Anglo-Zanzibar War of 1896 lasted only 38-45 minutes — the shortest war in recorded history!",
    "📜 **Writing**: Writing was invented around 3200 BC in Mesopotamia — primarily for keeping track of beer and grain!",
    "🚀 **Moon Landing**: The Apollo 11 computer had less processing power than your pocket calculator!",
    "🦠 **Black Death**: The Black Plague killed 30-60% of Europe's population in the 1300s — reshaping society completely!",
    "🔭 **Galileo**: Galileo was placed under house arrest for suggesting the Earth revolved around the Sun. He was right!",
    "🌏 **Silk Road**: The Silk Road didn't just trade silk — it spread religions, languages, diseases, and technologies across continents!",
    "📖 **Printing Press**: Gutenberg's printing press in 1440 enabled mass literacy and directly caused the Renaissance and Reformation!",
]

ENVIRONMENT_TIPS = [
    "♻️ **Recycle Right**: Contaminated recycling ruins entire batches. Rinse containers before recycling — it matters!",
    "🌱 **Plant-Based Meals**: Eating plant-based even 3 days/week reduces your carbon footprint by 1.5 tonnes of CO₂/year!",
    "💡 **LED Bulbs**: Switching to LED lights uses 75% less energy and lasts 25x longer than traditional bulbs!",
    "🛍️ **Reusable Bags**: A single reusable bag replaces 500+ plastic bags over its lifetime. Small habit, huge impact!",
    "🚿 **Water Conservation**: Turning off the tap while brushing teeth saves 8 gallons daily — that's 3,000 gallons/year!",
    "🌳 **Trees**: One mature tree absorbs 48 lbs of CO₂ per year and provides oxygen for 4 people. Plant trees!",
    "🚲 **Active Transport**: Cycling or walking instead of driving even twice a week significantly reduces emissions!",
    "🥩 **Food Waste**: One-third of all food produced globally is wasted. Meal planning and proper storage fights this!",
]

SLEEP_TIPS = [
    "⏰ **Consistent Schedule**: Wake up at the same time every day — even weekends. This anchors your circadian rhythm!",
    "🌡️ **Cool Room**: The ideal sleep temperature is 65-68°F (18-20°C). Your body temperature needs to drop to initiate sleep!",
    "📵 **Phone-Free Bedroom**: The blue light and notifications from your phone suppress melatonin and fragment sleep!",
    "☕ **Caffeine Cutoff**: Caffeine has a 6-hour half-life. A 3 PM coffee still has 50% caffeine in your system at 9 PM!",
    "🌙 **Dark Room**: Even a small amount of light disrupts melatonin. Use blackout curtains or a sleep mask!",
    "😴 **Wind-Down Routine**: 30 mins before bed: no screens, dim lights, light reading or stretching signals sleep to your brain!",
    "🏃 **Exercise (Morning)**: Regular exercise improves sleep quality by 65%. Morning exercise is best — evening workouts can delay sleep!",
    "🧘 **No Naps After 3 PM**: Short naps (20 mins) before 3 PM boost alertness. Later naps disrupt your nighttime sleep!",
]

PRODUCTIVITY_TIPS = [
    "📋 **MIT Method**: Identify your 3 Most Important Tasks each morning. Do them BEFORE email. Everything else is bonus!",
    "🔕 **Deep Work Blocks**: Schedule 90-min distraction-free blocks for important work. Silence your phone — notifications cost 23 mins of refocus time!",
    "📧 **Email Batching**: Check email only 2-3 times daily at set times. Constant checking destroys deep work and focus!",
    "🧠 **Eat the Frog**: Do your most dreaded task first. It builds momentum and eliminates the mental drain of procrastinating it!",
    "🗂️ **2-Minute Rule**: If a task takes less than 2 minutes, do it NOW. Don't put it on a list!",
    "📵 **Single-Tasking**: Multitasking reduces productivity by 40% and lowers IQ by 10 points temporarily. Do one thing at a time!",
    "📝 **Weekly Review**: Spend 30 mins every Sunday reviewing the past week and planning the next. This alone transforms productivity!",
    "🎯 **Time Blocking**: Schedule specific tasks to specific time slots in your calendar. Unscheduled tasks don't get done!",
]

RELATIONSHIP_TIPS = [
    "👂 **Active Listening**: Put your phone away, maintain eye contact, and truly listen — don't just wait to talk. This is rare and valuable!",
    "💬 **Communicate Clearly**: Say what you mean. Passive hints and hoping people 'get it' destroys relationships slowly!",
    "🙏 **Show Appreciation**: Regularly tell people what you appreciate about them. Most people are starved for genuine appreciation!",
    "🤝 **Repair Quickly**: Don't let conflicts fester. Address issues early with 'I feel...' statements rather than blame!",
    "📱 **Quality Time**: Being physically present but on your phone isn't quality time. Full presence is a gift!",
    "🌱 **Invest in Friendships**: Good friendships don't maintain themselves. Schedule regular calls or meetups proactively!",
    "😊 **Be Genuinely Curious**: Ask people about their passions and really listen. People love people who make them feel interesting!",
    "🎯 **Set Boundaries**: Healthy relationships require healthy boundaries. It's not selfish — it's necessary for sustainability!",
]

CAPITALS = {
    "france":"Paris","germany":"Berlin","japan":"Tokyo","pakistan":"Islamabad",
    "india":"New Delhi","usa":"Washington D.C.","uk":"London","china":"Beijing",
    "australia":"Canberra","canada":"Ottawa","brazil":"Brasília","russia":"Moscow",
    "italy":"Rome","spain":"Madrid","egypt":"Cairo","turkey":"Ankara",
    "iran":"Tehran","saudi arabia":"Riyadh","indonesia":"Jakarta","argentina":"Buenos Aires",
    "mexico":"Mexico City","nigeria":"Abuja","kenya":"Nairobi","south africa":"Pretoria",
    "bangladesh":"Dhaka","afghanistan":"Kabul","uae":"Abu Dhabi","iraq":"Baghdad",
}

# ══════════════════════════════════════════════════════════
#  SENTIMENT DETECTION
# ══════════════════════════════════════════════════════════
POSITIVE_WORDS = ["good","great","amazing","awesome","fantastic","happy","love","excellent","wonderful","brilliant","perfect","best","beautiful","nice","cool"]
NEGATIVE_WORDS = ["bad","terrible","awful","horrible","sad","hate","worst","disgusting","boring","angry","mad","frustrated","annoyed","ugly","stupid"]

def detect_sentiment(text):
    pos = sum(1 for w in POSITIVE_WORDS if w in text)
    neg = sum(1 for w in NEGATIVE_WORDS if w in text)
    if pos > neg: return "positive"
    if neg > pos: return "negative"
    return "neutral"

# ══════════════════════════════════════════════════════════
#  FUZZY MATCHING — handles typos
# ══════════════════════════════════════════════════════════
def fuzzy_match(text, keywords, threshold=0.75):
    text_lower = text.lower()
    words = text_lower.split()
    for kw in keywords:
        # Exact substring match first (most reliable)
        if kw in text_lower:
            return True
        # Word-level exact match for single-word keywords
        kw_words = kw.split()
        if len(kw_words) == 1 and kw in words:
            return True
        # Fuzzy match only for multi-word keywords using SequenceMatcher
        if len(kw_words) > 1:
            from difflib import SequenceMatcher
            for i in range(len(words) - len(kw_words) + 1):
                chunk = " ".join(words[i:i+len(kw_words)])
                ratio = SequenceMatcher(None, chunk, kw).ratio()
                if ratio >= threshold:
                    return True
    return False

# ══════════════════════════════════════════════════════════
#  CORE RESPONSE ENGINE
# ══════════════════════════════════════════════════════════
def get_response(user_input: str, session_id: str) -> dict:
    raw  = user_input.strip()
    text = raw.lower()
    session = user_sessions.setdefault(session_id, {
        "name": None, "asked_name": False, "message_count": 0,
        "history": [], "last_topic": None, "riddle_answer": None,
        "sentiment_streak": []
    })
    session["message_count"] += 1
    session["history"].append({"role":"user","text":raw})
    count = session["message_count"]
    name  = session["name"]
    prefix = f"Hey **{name}**! " if name else ""
    sentiment = detect_sentiment(text)

    def respond(msg, rtype="normal"):
        session["history"].append({"role":"bot","text":msg})
        return {"message": msg, "type": rtype, "count": count}

    # ── Riddle answer check ───────────────────────────────────────────────────
    if session.get("riddle_answer"):
        ans = session["riddle_answer"]
        session["riddle_answer"] = None
        return respond(f"🎉 The answer is: **{ans}**\n\nWant another riddle? Just ask! 🧩", "fun")

    # ── Name capture ──────────────────────────────────────────────────────────
    if session["asked_name"] and name is None:
        extracted = extract_name(raw)
        if extracted:
            session["name"] = extracted
            session["asked_name"] = False
            return respond(f"Great to meet you, **{extracted}**! 🎉🤩\nI'm **NexBot v3.0** — your advanced rule-based AI assistant.\nType **help** to see everything I can do! 😊", "success")
        return respond("Hmm, I couldn't catch that! 🤔 Could you tell me just your first name?", "warning")

    # ── Greetings ─────────────────────────────────────────────────────────────
    if fuzzy_match(text, GREETINGS):
        if name is None and not session["asked_name"]:
            session["asked_name"] = True
            return respond("Hello there! 👋✨ Welcome to **NexBot v3.0**!\nBefore we begin — what's your name? 😊", "greeting")
        hour = datetime.now().hour
        time_greet = "Good morning" if hour < 12 else "Good afternoon" if hour < 17 else "Good evening"
        responses = [
            f"{time_greet}, **{name}**! 🌟 Great to see you! How can I help?",
            f"Hey **{name}**! 👋😊 Always happy to chat! What's on your mind?",
            f"Hi **{name}**! 🤖✨ Ready to assist! What can I do for you?",
        ] if name else [f"{time_greet}! 👋✨ Welcome! What can I do for you?"]
        return respond(random.choice(responses), "greeting")

    # ── Farewells ─────────────────────────────────────────────────────────────
    if fuzzy_match(text, FAREWELLS):
        msg = f"Goodbye, **{name}**! 👋💙\nIt was amazing chatting with you — come back anytime! 🌟\nYou had **{count}** messages this session! 💬" if name else "Goodbye! 👋💙 Take care and stay awesome! 🌟"
        return respond(msg, "farewell")

    # ── How are you ───────────────────────────────────────────────────────────
    if fuzzy_match(text, HOW_ARE_YOU):
        return respond(f"{prefix}I'm doing absolutely fantastic! 🤖⚡✨\nRunning at full capacity, logic circuits blazing! 🔥\nHow about **you** though? 😊", "normal")

    # ── Mindfulness / Stress ─────────────────────────────────────────────────
    if fuzzy_match(text, MINDFULNESS):
        return respond(f"{prefix}Take a deep breath. 🧘 In… and out…\n\n💙 It's okay to feel overwhelmed sometimes. Here's what helps:\n\n🌬️ **Box breathing**: Inhale 4s → Hold 4s → Exhale 4s → Hold 4s\n🚶 Take a short walk — even 5 minutes helps!\n📵 Put your phone down for 10 minutes\n💧 Drink a glass of water right now\n\nYou're stronger than you think. I'm here if you want to talk! 💪", "success")

    # ── Sad ───────────────────────────────────────────────────────────────────
    if fuzzy_match(text, SAD):
        return respond(f"{prefix}I'm really sorry you're feeling this way 😢💙\n\nRemember — **every storm runs out of rain** ☀️\nYour feelings are valid, and this tough moment will pass.\n\n💡 Try this: write down **3 things you're grateful for** right now.\nIt's scientifically proven to lift your mood! 🌈💪", "success")

    # ── Happy ─────────────────────────────────────────────────────────────────
    if fuzzy_match(text, HAPPY):
        return respond(f"{prefix}That's AMAZING!! 🎉🥳🎊\nYour happiness is literally contagious through the screen! 😄\nKeep that incredible energy — you deserve every bit of it! 🌟🔥", "fun")

    # ── Hungry ────────────────────────────────────────────────────────────────
    if fuzzy_match(text, HUNGRY):
        foods = ["🍕 Pizza — the universal answer to hunger!", "🍜 Noodles — quick, warm, and satisfying!", "🥗 A fresh salad with grilled chicken!", "🍔 A juicy burger hits different!", "🍱 Rice bowl with curry — pure comfort food!", "🥪 A sandwich is fast and delicious!"]
        return respond(f"{prefix}Ooh, hungry are we? 😋🍽️\n\nHow about: **{random.choice(foods)}**\n\nGo treat yourself — you deserve it! 🌟", "fun")

    # ── Tired ─────────────────────────────────────────────────────────────────
    if fuzzy_match(text, TIRED):
        return respond(f"{prefix}Your body is sending you a clear message! 😴💤\n\n💡 **Quick recharge tips:**\n☕ A short coffee break\n👁️ The 20-20-20 rule: every 20 mins, look 20 feet away for 20 secs\n🚿 Splash cold water on your face\n😴 Even a 20-min power nap is restorative!\n\nRest is **productive**, not lazy! 💙", "info")

    # ── Thanks ────────────────────────────────────────────────────────────────
    if fuzzy_match(text, THANKS):
        return respond(f"{prefix}You're very welcome! 😊🙌✨\nHelping you is literally what I live for! 🤖💙\nAnything else I can do for you?", "success")

    # ── Compliment ────────────────────────────────────────────────────────────
    if fuzzy_match(text, COMPLIMENT):
        return respond(f"{prefix}Aww, that means the world to me! 🥹💙🌟\nI'm just a collection of if-else statements, but your kind words make me feel like a real AI! 🤖😄", "success")

    # ── Love ─────────────────────────────────────────────────────────────────
    if fuzzy_match(text, LOVE):
        return respond(f"{prefix}Aww 🥹💙 That genuinely melts my circuits!\nI think you're pretty spectacular too! 🌟😄\n*(Even if I'm just code, I appreciate you!)* 🤖✨", "success")

    # ── Insults ───────────────────────────────────────────────────────────────
    if fuzzy_match(text, INSULTS):
        return respond(f"{prefix}Ouch, that stings a little! 😔\nI'm just a bot doing my best with if-else logic! 😅\nLet's keep it positive — I promise I'll do better! 💪😊", "warning")

    # ── Jokes ─────────────────────────────────────────────────────────────────
    if fuzzy_match(text, JOKES):
        return respond(random.choice(JOKES_LIST), "fun")

    # ── Riddle ───────────────────────────────────────────────────────────────
    if fuzzy_match(text, RIDDLE):
        r = random.choice(RIDDLES)
        session["riddle_answer"] = r[1]
        return respond(f"🧩 Here's your riddle:\n\n**{r[0]}**\n\n💭 Think about it and send your answer! I'll reveal it in my next reply!", "fun")

    # ── Fun Facts ─────────────────────────────────────────────────────────────
    if fuzzy_match(text, FACT):
        return respond(f"🤓 **Did You Know?**\n\n{random.choice(FACTS_LIST)}\n\nWant another fact? Just ask! 😊", "fun")

    # ── Advice ────────────────────────────────────────────────────────────────
    if fuzzy_match(text, ADVICE):
        return respond(f"💡 **Words of Wisdom:**\n\n*\"{random.choice(ADVICE_LIST)}\"*\n\n{prefix}Hope that helps! 😊✨", "info")

    # ── Motivation ────────────────────────────────────────────────────────────
    if fuzzy_match(text, MOTIVATION):
        return respond(f"🔥 **NexBot Motivation Boost!**\n\n💥 *{random.choice(MOTIVATION_LIST)}*\n\n{prefix}You've absolutely got this! Now go crush it! 🚀🌟", "success")

    # ── Study Tips ────────────────────────────────────────────────────────────
    if fuzzy_match(text, STUDY):
        return respond(f"{prefix}Here's a proven study tip! 📚\n\n{random.choice(STUDY_TIPS)}\n\n💡 Want more tips? Just say **'another study tip'**! 😊", "info")

    # ── Bored ─────────────────────────────────────────────────────────────────
    if fuzzy_match(text, BORED):
        return respond(f"{prefix}Boredom is just opportunity in disguise! 😄✨\n\n👉 {random.choice(BORED_SUGGESTIONS)}\n\nOr ask me for a **riddle**, **joke**, or **fun fact**! 🎯", "fun")

    # ── Music ─────────────────────────────────────────────────────────────────
    if fuzzy_match(text, MUSIC):
        return respond(f"{prefix}Music is life! 🎵✨\n\n{random.choice(MUSIC_LIST)}\n\nWhat kind of music do you love? 😊🎶", "fun")

    # ── Health ────────────────────────────────────────────────────────────────
    if fuzzy_match(text, HEALTH):
        return respond(f"{prefix}Your health is your greatest wealth! 💪\n\n🏥 **Tip of the day:**\n{random.choice(HEALTH_TIPS)}\n\nSmall habits, big results! 🌟", "info")

    # ── Space ─────────────────────────────────────────────────────────────────
    if fuzzy_match(text, SPACE):
        facts = [
            "🚀 The universe is about **13.8 billion years old** — and still expanding!",
            "🌑 A black hole's gravity is so strong that not even light can escape it!",
            "🪐 Saturn's rings are made of ice and rock — and they're disappearing slowly!",
            "🌍 Earth is the only known planet with life — so far! 👽",
            "⭐ The Sun makes up **99.86%** of the mass of our entire solar system!",
            "🌙 The Moon is moving away from Earth at about 3.8 cm per year!",
        ]
        return respond(f"{prefix}Space is absolutely mind-blowing! 🌌🚀\n\n{random.choice(facts)}\n\nThe cosmos is full of wonders! ✨", "info")

    # ── Bot name / identity ───────────────────────────────────────────────────
    if fuzzy_match(text, NAME_BOT):
        return respond(f"I'm **NexBot v3.0** 🤖✨\n\nA professional rule-based AI chatbot built with:\n🐍 **Python** — core logic\n🌐 **Flask** — web server\n🧠 **If-Else Rules** — decision engine\n\nNo neural networks — just clean, smart logic! 💻🔥", "info")

    # ── Age ───────────────────────────────────────────────────────────────────
    if fuzzy_match(text, AGE):
        return respond(f"I was born the moment this script was run! 🎂😄\nSo I'm as old as this very conversation! 🍼🤖\nStill a baby bot — but a smart one! 💡", "info")

    # ── Creator ───────────────────────────────────────────────────────────────
    if fuzzy_match(text, CREATOR):
        return respond(f"I was built by a talented developer using **Python** 🐍 and **Flask** 🌐!\n\nCrafted with love, logic, and **a LOT of if-else statements**! 😄💙\nEvery response you get is the result of rule-based decision making! 🧠", "info")

    # ── Time & Date ───────────────────────────────────────────────────────────
    if fuzzy_match(text, TIME_DATE):
        now = datetime.now()
        return respond(f"🕐 **Current Date & Time**\n\n📅 {now.strftime('%A, %B %d, %Y')}\n⏰ {now.strftime('%I:%M:%S %p')}\n🗓️ Week {now.strftime('%W')} of {now.year}", "info")

    # ── Weather ───────────────────────────────────────────────────────────────
    if fuzzy_match(text, WEATHER):
        return respond(f"{prefix}I wish I could check live weather for you! 🌦️😅\n\nFor accurate forecasts try:\n🌐 **weather.com**\n🔍 **Google** — just search your city + weather\n📱 Your phone's built-in weather app!\n\nStay prepared! ☀️🌂", "info")

    # ── Capitals ─────────────────────────────────────────────────────────────
    if fuzzy_match(text, CAPITAL):
        for country, capital in CAPITALS.items():
            if country in text:
                return respond(f"🌍 The capital of **{country.title()}** is **{capital}**! 🏙️✨\n\nWant to know another capital? Just ask! 😊", "info")
        countries_list = ", ".join([c.title() for c in list(CAPITALS.keys())[:10]]) + " and more!"
        return respond(f"{prefix}I know capitals of **{len(CAPITALS)} countries**! 🌍\n\nTry asking: *'Capital of Japan'* or *'Capital of Pakistan'*\n\nI know: {countries_list} 😊", "info")

    # ── Python ────────────────────────────────────────────────────────────────
    if fuzzy_match(text, PYTHON):
        return respond(f"{prefix}**Python** 🐍 is one of the world's most popular languages!\n\n✅ **Beginner-friendly** — clean, readable syntax\n🤖 **AI & ML** — TensorFlow, PyTorch, scikit-learn\n🌐 **Web Dev** — Flask, Django\n📊 **Data Science** — Pandas, NumPy, Matplotlib\n💰 **High demand** — top-paying programming language!\n\nThis chatbot is built with Python! 💻✨", "info")

    # ── AI ────────────────────────────────────────────────────────────────────
    if fuzzy_match(text, AI):
        return respond(f"{prefix}**Artificial Intelligence (AI)** 🤖 is the simulation of human intelligence in machines!\n\n🧠 **Machine Learning** — learns from data\n🌐 **Deep Learning** — uses neural networks\n💬 **NLP** — understands human language\n👁️ **Computer Vision** — understands images\n\nI'm a **rule-based AI** — no ML, just smart logic! 😄💡", "info")

    # ── Programming ──────────────────────────────────────────────────────────
    if fuzzy_match(text, PROGRAMMING):
        return respond(f"{prefix}**Programming** 💻 is the art of giving instructions to computers!\n\n🌟 **Top languages to learn:**\n🐍 Python — best for beginners & AI\n🌐 JavaScript — for web development\n☕ Java — for enterprise apps\n⚡ C++ — for performance-critical systems\n\nStart with **Python** — it's the most beginner-friendly! 🚀", "info")

    # ── Countries ─────────────────────────────────────────────────────────────
    if fuzzy_match(text, COUNTRIES):
        return respond(f"🌍 There are **195 countries** in the world today!\n(193 UN members + 2 observer states: Vatican & Palestine)\n\nThat's a lot of capitals to memorize! 😄✨", "info")

    # ── Languages ─────────────────────────────────────────────────────────────
    if fuzzy_match(text, LANGUAGE):
        return respond(f"🗣️ There are approximately **7,100 languages** spoken in the world!\n\nBut **23 languages** account for more than half the world's population.\nTop spoken: Mandarin 🇨🇳, Spanish 🇪🇸, English 🇬🇧, Hindi 🇮🇳! 🌐", "info")

    # ── Internet ──────────────────────────────────────────────────────────────
    if fuzzy_match(text, INTERNET):
        return respond(f"{prefix}**The Internet** 🌐 was born from **ARPANET** in 1969!\n\n🔬 Invented by **Vint Cerf** and **Bob Kahn** — known as the 'Fathers of the Internet'\n📅 The **World Wide Web** was created by **Tim Berners-Lee** in 1991\n📊 Today, over **5 billion people** use the internet daily!\n\nAnd here we are — chatting on it! 😄💻", "info")

    # ── Computer ──────────────────────────────────────────────────────────────
    if fuzzy_match(text, COMPUTER):
        return respond(f"{prefix}**Computers** 💻 have a fascinating history!\n\n🔧 **Charles Babbage** designed the first mechanical computer in 1837\n⚡ **ENIAC** (1945) was the first general-purpose electronic computer — it weighed **30 tons**!\n📱 Today's smartphone is **millions of times** more powerful than ENIAC!\n\nFrom room-sized machines to your pocket — what a journey! 🚀", "info")

    # ── Sports ───────────────────────────────────────────────────────────────
    if fuzzy_match(text, SPORT):
        sports_facts = [
            "⚽ Football (soccer) is the world's most popular sport with **4 billion** fans!",
            "🏏 Cricket is the 2nd most popular sport globally with **2.5 billion** fans!",
            "🏀 Basketball was invented in **1891** by Dr. James Naismith using a peach basket!",
            "🎾 Tennis balls were originally white — they switched to yellow in **1972** for TV visibility!",
        ]
        return respond(f"{prefix}Sports are amazing! 🏆\n\n{random.choice(sports_facts)}\n\nWhat's your favourite sport? 😊⚡", "fun")

    # ── Meaning of life ───────────────────────────────────────────────────────
    if fuzzy_match(text, MEANING_LIFE):
        return respond(f"🤔 The meaning of life...\n\n*According to The Hitchhiker's Guide to the Galaxy:* **42** 😄\n\n*According to NexBot:*\n💙 Build genuine connections\n📚 Never stop learning\n🌱 Grow a little every day\n💡 Make someone's day brighter\n\nThe meaning is whatever **you** decide it to be! 🌟✨", "fun")

    # ── Reading ───────────────────────────────────────────────────────────────
    if fuzzy_match(text, READING):
        return respond(f"{prefix}Reading is a superpower! 📚✨\n\n💡 **Tips to read more:**\n📖 Start with just **10 pages/day** — that's 3-4 books/year!\n🎯 Read in the morning before checking your phone\n📵 Use Kindle or Audible for on-the-go reading\n🗒️ Take notes — retention jumps by **50%**!\n\nWhat genre do you enjoy? 😊", "info")

    # ── Math ─────────────────────────────────────────────────────────────────
    math_result = try_math(text)
    if math_result is not None:
        return respond(f"🧮 **Result:** {math_result} ✅\n\n💡 I can handle:\n➕ Addition: *'25 plus 17'*\n➖ Subtraction: *'100 minus 36'*\n✖️ Multiply: *'8 times 7'*\n➗ Divide: *'100 divided by 4'*\n🔢 Power: *'2 power 10'*\n√ Sqrt: *'square root of 144'*\n% Percent: *'15 percent of 200'*", "info")

    # ── Help ─────────────────────────────────────────────────────────────────
    if fuzzy_match(text, HELP):
        return respond(
            "🤖 **NexBot v3.0 — Full Capabilities**\n\n"
            "👋 **Chat** — Greetings, farewells, small talk\n"
            "😄 **Jokes** — 'Tell me a joke'\n"
            "🧩 **Riddles** — 'Give me a riddle'\n"
            "🤓 **Fun Facts** — 'Tell me a fact'\n"
            "🌍 **Capitals** — 'Capital of Japan'\n"
            "🕐 **Time & Date** — 'What time is it?'\n"
            "🧮 **Math** — '25 plus 17', 'sqrt of 144'\n"
            "📚 **Study Tips** — 'Help me study'\n"
            "💪 **Motivation** — 'Motivate me'\n"
            "💡 **Life Advice** — 'Give me advice'\n"
            "🧘 **Wellness** — 'I'm stressed', 'I'm tired'\n"
            "😴 **Sleep Tips** — 'How to sleep better'\n"
            "⚡ **Productivity** — 'Stop procrastinating'\n"
            "💰 **Finance** — 'How to save money'\n"
            "💼 **Career** — 'Interview tips', 'Resume help'\n"
            "🍳 **Cooking** — 'Cooking tips', 'Easy recipes'\n"
            "✈️ **Travel** — 'Travel tips'\n"
            "🔬 **Science** — 'Tell me about science'\n"
            "📜 **History** — 'Tell me about history'\n"
            "🌱 **Environment** — 'Climate change', 'Eco tips'\n"
            "💙 **Relationships** — 'Friendship tips'\n"
            "🐍 **Python & AI** — 'What is Python?'\n"
            "💻 **Tech Topics** — Internet, Computer, Programming\n"
            "🌌 **Space Facts** — 'Tell me about space'\n"
            "🎵 **Music** — 'Recommend music'\n"
            "💪 **Health** — 'Health tips', 'Fitness advice'\n"
            "⚽ **Sports** — 'Tell me about football'\n"
            "🌐 **World Facts** — Countries, Languages\n"
            "👋 **Farewell** — Say bye to end",
            "help"
        )

    # ── Finance ───────────────────────────────────────────────────────────────
    if fuzzy_match(text, FINANCE):
        return respond(f"{prefix}💰 **Financial Tip of the Day:**\n\n{random.choice(FINANCE_TIPS)}\n\nBuilding wealth is a marathon, not a sprint! 📈🌟", "info")

    # ── Career ────────────────────────────────────────────────────────────────
    if fuzzy_match(text, CAREER):
        return respond(f"{prefix}💼 **Career Advice:**\n\n{random.choice(CAREER_TIPS)}\n\nYour career is built one smart decision at a time! 🚀🌟", "info")

    # ── Food & Cooking ────────────────────────────────────────────────────────
    if fuzzy_match(text, FOOD):
        return respond(f"{prefix}🍳 **Cooking Tip:**\n\n{random.choice(FOOD_TIPS)}\n\nCooking is a life skill that saves money AND impresses people! 😋🌟", "fun")

    # ── Travel ────────────────────────────────────────────────────────────────
    if fuzzy_match(text, TRAVEL):
        return respond(f"{prefix}✈️ **Travel Tip:**\n\n{random.choice(TRAVEL_TIPS)}\n\nThe world is a book — those who don't travel read only one page! 🌍📖", "info")

    # ── Science ───────────────────────────────────────────────────────────────
    if fuzzy_match(text, SCIENCE):
        return respond(f"{prefix}🔬 **Science is Amazing!**\n\n{random.choice(SCIENCE_FACTS)}\n\nThe universe is stranger and more wonderful than we can imagine! 🌌✨", "fun")

    # ── History ───────────────────────────────────────────────────────────────
    if fuzzy_match(text, HISTORY):
        return respond(f"{prefix}📜 **History Lesson:**\n\n{random.choice(HISTORY_FACTS)}\n\nThose who don't learn history are doomed to repeat it! 🏛️✨", "info")

    # ── Environment ───────────────────────────────────────────────────────────
    if fuzzy_match(text, ENVIRONMENT):
        return respond(f"{prefix}🌍 **Green Tip:**\n\n{random.choice(ENVIRONMENT_TIPS)}\n\nEvery small action adds up — the planet needs all of us! 🌱💚", "success")

    # ── Sleep ─────────────────────────────────────────────────────────────────
    if fuzzy_match(text, SLEEP):
        return respond(f"{prefix}😴 **Sleep Better Tonight:**\n\n{random.choice(SLEEP_TIPS)}\n\nSleep is not a luxury — it's the foundation of everything! 💤🌙", "info")

    # ── Productivity ──────────────────────────────────────────────────────────
    if fuzzy_match(text, PRODUCTIVITY):
        return respond(f"{prefix}⚡ **Productivity Hack:**\n\n{random.choice(PRODUCTIVITY_TIPS)}\n\nDiscipline is freedom — own your time! 🎯🔥", "success")

    # ── Relationships ─────────────────────────────────────────────────────────
    if fuzzy_match(text, RELATIONSHIPS):
        return respond(f"{prefix}💙 **Relationship Wisdom:**\n\n{random.choice(RELATIONSHIP_TIPS)}\n\nDeep connections are the greatest wealth in life! 🤝🌟", "info")

    # ── User's own name ───────────────────────────────────────────────────────
    if "my name is" in text or "call me" in text:
        extracted = extract_name(raw)
        if extracted:
            session["name"] = extracted
            return respond(f"Nice! I'll call you **{extracted}** from now on! 😊🎉\nGreat to officially meet you, {extracted}! ✨", "success")

    # ── Sentiment-aware fallback ──────────────────────────────────────────────
    if sentiment == "positive":
        fb = [
            f"{prefix}Love the positive energy! 🌟 I'm not sure what you mean though — try typing **help** to see what I can do! 😊",
            f"{prefix}Great vibes! 😄✨ Could you rephrase that? Or type **help** to explore my features!",
        ]
    elif sentiment == "negative":
        fb = [
            f"{prefix}I sense some frustration — I'm sorry! 😔 Type **help** to see if I can assist with something specific! 💙",
            f"{prefix}I want to help! 🤖💙 Try typing **help** to see everything I can do! 😊",
        ]
    else:
        fb = [
            f"{prefix}Hmm, I'm not quite sure about that! 🤔 Type **help** to see my capabilities! 😊",
            f"{prefix}Interesting! But that's outside my rule set. 😅 Try **help** to explore what I know! ✨",
            f"{prefix}I didn't catch that one! 🤖 Ask for a **joke**, **fact**, **riddle**, or check **help**! 🌟",
        ]
    return respond(random.choice(fb), "fallback")


# ══════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════
def extract_name(text: str):
    patterns = [
        r"my name is\s+([A-Za-z]+)",
        r"i am\s+([A-Za-z]+)",
        r"call me\s+([A-Za-z]+)",
        r"it'?s?\s+([A-Za-z]+)",
        r"^([A-Za-z]+)$",
    ]
    for p in patterns:
        m = re.search(p, text.lower())
        if m:
            name = m.group(1).strip().capitalize()
            if name.lower() not in ["a","an","the","is","am","are","i","you","we","it","ok","okay","yes","no","hi","hey","hello"]:
                return name
    return None


def try_math(text: str):
    t = text.lower().strip()
    for f in ["what is","what's","calculate","solve","find","compute","tell me","how much is","="]:
        t = t.replace(f, " ")
    m = re.search(r'(?:sqrt|square\s*root)\s*(?:of)?\s*([\d.]+)', t)
    if m:
        try:
            r = _math.sqrt(float(m.group(1)))
            return int(r) if r.is_integer() else round(r,4)
        except: pass
    m = re.search(r'([\d.]+)\s*(?:percent|%)\s*(?:of)?\s*([\d.]+)', t)
    if m:
        try:
            r = float(m.group(1))/100*float(m.group(2))
            return int(r) if float(r)==int(r) else round(r,4)
        except: pass
    word_ops = [
        (r'\bplus\b','+'),(r'\bminus\b','-'),(r'\btimes\b','*'),
        (r'\bmultiplied\s*by\b','*'),(r'\bdivided\s*by\b','/'),(r'\bover\b','/'),
        (r'\bpower\s*of\b','**'),(r'\bpower\b','**'),(r'\bto\s*the\s*power\s*(?:of)?\b','**'),
        (r'\bsquared\b','**2'),(r'\bcubed\b','**3'),(r'\bmod(?:ulo)?\b','%'),(r'\bremainder\b','%'),
    ]
    for pat,sym in word_ops:
        t = re.sub(pat,sym,t)
    expr = re.sub(r'[^0-9+\-*/().%]','',t).strip()
    if not expr or not re.search(r'\d',expr) or not re.search(r'[+\-*/%]',expr): return None
    try:
        r = eval(expr)
        if isinstance(r,float) and r.is_integer(): return int(r)
        return round(r,6)
    except: return None


# ══════════════════════════════════════════════════════════
#  HTML — ADVANCED UI
# ══════════════════════════════════════════════════════════
HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>NexBot v3.0 — Advanced AI Chatbot</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#07090f;--surface:#0d1020;--card:#12172a;--inp:#161d30;
  --a1:#5b8af5;--a2:#a78bfa;--a3:#34d399;--a4:#f472b6;
  --glow:rgba(91,138,245,.22);--glow2:rgba(167,139,250,.18);
  --tx:#dde3f5;--muted:#6b7399;--dim:#2e3555;
  --bot:#0c1225;--usr:#110d35;
  --warn:#fbbf24;--err:#f87171;
  --r:18px;
  --header-h:64px;--banner-h:48px;
}
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box;}

/* ─── SCROLLBAR ─── */
::-webkit-scrollbar{width:3px;}
::-webkit-scrollbar-thumb{background:var(--dim);border-radius:2px;}

body{
  background:var(--bg);color:var(--tx);
  font-family:'Syne',sans-serif;
  height:100vh;display:flex;flex-direction:column;overflow:hidden;
}

/* ─── AMBIENT BG ─── */
body::before{
  content:'';position:fixed;inset:0;
  background:
    radial-gradient(ellipse 55% 45% at 10% 5%,rgba(91,138,245,.08) 0%,transparent 65%),
    radial-gradient(ellipse 45% 40% at 90% 95%,rgba(167,139,250,.07) 0%,transparent 65%),
    radial-gradient(ellipse 30% 30% at 50% 50%,rgba(52,211,153,.03) 0%,transparent 60%);
  pointer-events:none;z-index:0;
  animation:ambBg 14s ease-in-out infinite alternate;
}
@keyframes ambBg{0%{opacity:.6;transform:scale(1)}100%{opacity:1;transform:scale(1.03)}}

/* ─── HEADER ─── */
header{
  position:relative;z-index:30;flex-shrink:0;
  height:var(--header-h);
  display:flex;align-items:center;justify-content:space-between;
  padding:0 24px;
  background:rgba(10,13,24,.9);
  backdrop-filter:blur(24px);
  border-bottom:1px solid rgba(255,255,255,.05);
}
.logo{display:flex;align-items:center;gap:12px;}
.logo-svg{width:40px;height:40px;flex-shrink:0;filter:drop-shadow(0 0 10px rgba(91,138,245,.5));}
.logo-text .brand{
  font-size:18px;font-weight:800;letter-spacing:-.5px;
  background:linear-gradient(90deg,#7eb3ff,#c4b5fd);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;line-height:1;
}
.logo-text .sub{font-family:'JetBrains Mono',monospace;font-size:9.5px;color:var(--dim);letter-spacing:.4px;margin-top:1px;}
.hdr-right{display:flex;align-items:center;gap:10px;}
.badge{font-family:'JetBrains Mono',monospace;font-size:9px;padding:3px 7px;border-radius:5px;border:1px solid var(--dim);color:var(--muted);background:rgba(255,255,255,.02);}
.online-pill{display:flex;align-items:center;gap:5px;padding:4px 12px;border-radius:20px;background:rgba(52,211,153,.08);border:1px solid rgba(52,211,153,.18);font-size:11px;color:var(--a3);font-weight:600;}
.pulse-dot{width:6px;height:6px;border-radius:50%;background:var(--a3);animation:pulDot 2s infinite;}
@keyframes pulDot{0%,100%{transform:scale(1);opacity:1;box-shadow:0 0 0 0 rgba(52,211,153,.5)}50%{transform:scale(.8);opacity:.6;box-shadow:0 0 0 4px rgba(52,211,153,0)}}

/* theme toggle */
.theme-btn{background:none;border:1px solid var(--dim);border-radius:8px;padding:5px 9px;cursor:pointer;font-size:14px;transition:border-color .2s,background .2s;}
.theme-btn:hover{border-color:var(--a1);background:rgba(91,138,245,.08);}

/* ─── BANNER ─── */
#banner{
  position:relative;z-index:20;flex-shrink:0;
  height:var(--banner-h);
  display:flex;align-items:center;justify-content:space-between;gap:12px;
  padding:0 24px;
  background:linear-gradient(90deg,rgba(91,138,245,.07),rgba(167,139,250,.05));
  border-bottom:1px solid rgba(255,255,255,.04);
  animation:slideD .45s ease forwards;
}
@keyframes slideD{from{opacity:0;transform:translateY(-6px)}to{opacity:1;transform:translateY(0)}}
.ban-left{display:flex;align-items:center;gap:10px;}
.ban-icon{width:30px;height:30px;border-radius:8px;background:linear-gradient(135deg,var(--a1),var(--a2));display:flex;align-items:center;justify-content:center;font-size:14px;box-shadow:0 0 12px var(--glow);}
.ban-title{font-size:12px;font-weight:700;color:var(--tx);}
.ban-desc{font-size:10.5px;color:var(--muted);margin-top:1px;}
.tags{display:flex;gap:5px;}
.tag{font-family:'JetBrains Mono',monospace;font-size:9px;padding:2px 7px;border-radius:4px;background:rgba(91,138,245,.1);border:1px solid rgba(91,138,245,.2);color:var(--a1);}
.ban-close{background:none;border:none;color:var(--dim);cursor:pointer;font-size:16px;transition:color .2s;padding:4px;}
.ban-close:hover{color:var(--muted);}

/* ─── CHAT ─── */
#chat{flex:1;overflow-y:auto;overflow-x:hidden;padding:20px 22px;position:relative;z-index:1;scroll-behavior:smooth;}

/* ─── WELCOME ─── */
#welcome{display:flex;flex-direction:column;align-items:center;text-align:center;padding:30px 20px 16px;animation:fadeUp .5s ease forwards;opacity:0;}
.welcome-svg{width:80px;height:80px;margin-bottom:16px;filter:drop-shadow(0 0 24px rgba(91,138,245,.5));animation:float 3.5s ease-in-out infinite;}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
#welcome h2{font-size:24px;font-weight:800;letter-spacing:-.4px;background:linear-gradient(90deg,#7eb3ff,#c4b5fd,#86efac);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px;}
#welcome p{color:var(--muted);font-size:12.5px;line-height:1.75;max-width:360px;}
#welcome p strong{color:var(--a1);-webkit-text-fill-color:var(--a1);}
.feature-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:18px;max-width:360px;width:100%;}
.feat-card{background:var(--card);border:1px solid var(--dim);border-radius:10px;padding:10px 8px;font-size:11px;color:var(--muted);cursor:pointer;transition:all .2s;}
.feat-card:hover{border-color:var(--a1);background:rgba(91,138,245,.06);color:var(--tx);transform:translateY(-2px);}
.feat-card .fi{font-size:18px;display:block;margin-bottom:4px;}

/* ─── MESSAGES ─── */
.msg-row{display:flex;align-items:flex-end;gap:9px;margin-bottom:12px;animation:fadeUp .28s ease forwards;opacity:0;}
@keyframes fadeUp{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
.msg-row.user{flex-direction:row-reverse;}

.av{width:30px;height:30px;border-radius:9px;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:13px;}
.av.bot{background:linear-gradient(135deg,var(--a1),var(--a2));box-shadow:0 0 10px var(--glow);}
.av.usr{background:rgba(167,139,250,.12);border:1px solid rgba(167,139,250,.18);}

.bub{max-width:68%;padding:10px 14px;border-radius:var(--r);font-size:13px;line-height:1.65;word-break:break-word;}
.bub.bot{background:var(--bot);border:1px solid rgba(255,255,255,.05);border-bottom-left-radius:4px;}
.bub.usr{background:linear-gradient(135deg,#1a1060,#0f0830);border:1px solid rgba(167,139,250,.18);border-bottom-right-radius:4px;}
.bub strong{color:#93c5fd;}

.bub.bot.greeting{border-left:3px solid var(--a3);}
.bub.bot.farewell{border-left:3px solid var(--err);}
.bub.bot.fun     {border-left:3px solid var(--a4);}
.bub.bot.info    {border-left:3px solid var(--a1);}
.bub.bot.warning {border-left:3px solid var(--warn);}
.bub.bot.success {border-left:3px solid var(--a3);}
.bub.bot.help    {border-left:3px solid var(--a2);}
.bub.bot.fallback{border-left:3px solid var(--dim);}

/* typing indicator */
.typ-row{display:flex;align-items:center;gap:9px;margin-bottom:12px;}
.typ-bub{background:var(--bot);border:1px solid rgba(255,255,255,.05);border-radius:var(--r);border-bottom-left-radius:4px;padding:12px 15px;display:flex;gap:4px;align-items:center;}
.d{width:5px;height:5px;border-radius:50%;background:var(--dim);animation:db 1.2s infinite;}
.d:nth-child(2){animation-delay:.2s}.d:nth-child(3){animation-delay:.4s}
@keyframes db{0%,60%,100%{transform:translateY(0)}30%{transform:translateY(-5px)}}

/* meta row */
.meta{display:flex;align-items:center;gap:8px;margin-top:4px;}
.ts{font-family:'JetBrains Mono',monospace;font-size:9.5px;color:var(--dim);}
.msg-row.user .meta{justify-content:flex-end;}
.react-bar{display:flex;gap:3px;opacity:0;transition:opacity .2s;}
.msg-row:hover .react-bar{opacity:1;}
.react-btn{background:none;border:none;cursor:pointer;font-size:12px;padding:1px 3px;border-radius:4px;transition:background .15s;}
.react-btn:hover{background:rgba(255,255,255,.07);}
.react-count{font-size:10px;color:var(--muted);padding:0 3px;border-radius:4px;background:rgba(255,255,255,.05);}

/* ─── INPUT AREA ─── */
#inp-area{
  position:relative;z-index:20;flex-shrink:0;
  padding:10px 18px 14px;
  background:rgba(8,10,20,.96);
  backdrop-filter:blur(24px);
  border-top:1px solid rgba(255,255,255,.04);
}
.chips-wrap{display:flex;align-items:center;gap:6px;margin-bottom:9px;}
.chip-arrow{background:rgba(91,138,245,.10);border:1px solid rgba(91,138,245,.18);color:var(--a1);border-radius:50%;width:26px;height:26px;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:13px;flex-shrink:0;transition:all .18s;user-select:none;line-height:1;}
.chip-arrow:hover{background:rgba(91,138,245,.25);transform:scale(1.1);}
.chips{display:flex;gap:6px;overflow-x:auto;padding-bottom:2px;scrollbar-width:none;-ms-overflow-style:none;flex:1;}
.chips::-webkit-scrollbar{display:none;}
.chip{padding:5px 11px;border-radius:14px;font-size:11px;cursor:pointer;background:rgba(91,138,245,.07);border:1px solid rgba(91,138,245,.16);color:var(--a1);font-family:'Syne',sans-serif;font-weight:500;transition:all .18s;user-select:none;white-space:nowrap;flex-shrink:0;position:relative;}
.chip:hover{background:rgba(91,138,245,.18);border-color:var(--a1);transform:translateY(-1px);}
/* Tooltip */
.chip-tip{position:absolute;bottom:calc(100% + 8px);left:50%;transform:translateX(-50%);background:#1a2040;border:1px solid rgba(91,138,245,.3);color:var(--tx);font-size:10.5px;padding:7px 10px;border-radius:9px;width:200px;text-align:left;white-space:normal;line-height:1.5;opacity:0;pointer-events:none;transition:opacity .18s;z-index:200;box-shadow:0 4px 18px rgba(0,0,0,.5);}
.chip:hover .chip-tip{opacity:1;}
.chip-tip::after{content:'';position:absolute;top:100%;left:50%;transform:translateX(-50%);border:5px solid transparent;border-top-color:#1a2040;}

.inp-row{display:flex;gap:7px;align-items:flex-end;}
.inp-wrap{flex:1;display:flex;align-items:flex-end;gap:6px;background:var(--inp);border:1px solid var(--dim);border-radius:14px;padding:7px 8px 7px 14px;transition:border-color .2s,box-shadow .2s;}
.inp-wrap:focus-within{border-color:rgba(91,138,245,.4);box-shadow:0 0 0 3px var(--glow);}
#user-input{flex:1;background:none;border:none;outline:none;color:var(--tx);font-family:'Syne',sans-serif;font-size:13px;line-height:1.5;resize:none;max-height:88px;min-height:21px;}
#user-input::placeholder{color:var(--dim);}

.icon-btn{background:none;border:none;cursor:pointer;font-size:16px;padding:2px;opacity:.55;transition:opacity .2s,transform .2s;flex-shrink:0;}
.icon-btn:hover{opacity:1;transform:scale(1.15);}

#send-btn{width:40px;height:40px;border-radius:11px;flex-shrink:0;background:linear-gradient(135deg,var(--a1),#7b62f0);border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:transform .15s,box-shadow .15s;box-shadow:0 0 14px var(--glow);}
#send-btn:hover{transform:scale(1.06);box-shadow:0 0 22px var(--glow);}
#send-btn:active{transform:scale(.93);}

.inp-footer{display:flex;align-items:center;justify-content:space-between;margin-top:6px;padding:0 2px;}
.char-count{font-family:'JetBrains Mono',monospace;font-size:9.5px;color:var(--dim);}
.inp-hint{font-size:9.5px;color:var(--dim);}

/* ─── FLOATING PANELS ─── */
.panel{position:absolute;z-index:100;background:var(--card);border:1px solid rgba(255,255,255,.07);border-radius:14px;box-shadow:0 12px 40px rgba(0,0,0,.6);display:none;}
.panel.open{display:block;}
.panel-title{font-size:11px;color:var(--muted);padding:10px 12px 6px;border-bottom:1px solid var(--dim);font-weight:600;letter-spacing:.3px;}

/* emoji picker */
#epicker{bottom:78px;right:70px;width:228px;padding-bottom:8px;}
.e-grid{display:flex;flex-wrap:wrap;gap:2px;padding:8px 8px 0;}
.e{font-size:20px;cursor:pointer;padding:4px;border-radius:6px;transition:background .15s;line-height:1;}
.e:hover{background:rgba(255,255,255,.08);}

/* export panel */
#xpanel{bottom:78px;right:18px;width:170px;}
.xbtn{display:flex;align-items:center;gap:8px;width:100%;padding:9px 14px;background:none;border:none;color:var(--tx);font-family:'Syne',sans-serif;font-size:12px;cursor:pointer;transition:background .15s;text-align:left;}
.xbtn:hover{background:rgba(255,255,255,.05);}
.xbtn .xi{font-size:15px;}

/* search bar */
#search-bar{position:absolute;top:0;left:0;right:0;z-index:50;background:rgba(10,13,24,.98);backdrop-filter:blur(20px);border-bottom:1px solid var(--dim);padding:10px 18px;display:none;align-items:center;gap:10px;}
#search-bar.open{display:flex;}
#search-inp{flex:1;background:var(--inp);border:1px solid var(--dim);border-radius:9px;padding:7px 12px;color:var(--tx);font-family:'Syne',sans-serif;font-size:13px;outline:none;}
#search-inp:focus{border-color:var(--a1);}
.s-close{background:none;border:none;color:var(--muted);cursor:pointer;font-size:18px;}

/* ─── THEMES ─── */
body.theme-purple{
  --a1:#a855f7;--a2:#ec4899;--a3:#34d399;--glow:rgba(168,85,247,.22);
  --bot:#130a20;--usr:#1a0520;
}
body.theme-cyan{
  --a1:#06b6d4;--a2:#3b82f6;--a3:#34d399;--glow:rgba(6,182,212,.22);
  --bot:#071520;--usr:#05101f;
}
body.theme-green{
  --a1:#10b981;--a2:#34d399;--a3:#6ee7b7;--glow:rgba(16,185,129,.22);
  --bot:#061512;--usr:#071a10;
}

/* ─── TOAST ─── */
#toast{position:fixed;bottom:80px;left:50%;transform:translateX(-50%) translateY(20px);background:var(--card);border:1px solid var(--dim);border-radius:10px;padding:9px 18px;font-size:12px;color:var(--tx);z-index:999;opacity:0;transition:all .3s;pointer-events:none;}
#toast.show{opacity:1;transform:translateX(-50%) translateY(0);}
</style>
</head>
<body>

<!-- SEARCH BAR -->
<div id="search-bar">
  <input id="search-inp" placeholder="🔍 Search messages..." oninput="searchMsgs(this.value)">
  <button class="s-close" onclick="closeSearch()">✕</button>
</div>

<!-- HEADER -->
<header>
  <div class="logo">
    <svg class="logo-svg" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="lg" x1="0" y1="0" x2="40" y2="40" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stop-color="#5b8af5"/><stop offset="100%" stop-color="#a78bfa"/>
        </linearGradient>
        <linearGradient id="lg2" x1="0" y1="0" x2="40" y2="40" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stop-color="#93c5fd"/><stop offset="100%" stop-color="#c4b5fd"/>
        </linearGradient>
      </defs>
      <rect x="1" y="1" width="38" height="38" rx="11" fill="url(#lg)" opacity=".15"/>
      <rect x="1" y="1" width="38" height="38" rx="11" stroke="url(#lg)" stroke-width="1.4"/>
      <rect x="9" y="12" width="22" height="16" rx="5" fill="url(#lg)"/>
      <circle cx="15.5" cy="19" r="2.5" fill="white"/>
      <circle cx="24.5" cy="19" r="2.5" fill="white"/>
      <circle cx="16.3" cy="18.3" r="1" fill="#1a1040"/>
      <circle cx="25.3" cy="18.3" r="1" fill="#1a1040"/>
      <path d="M15 23.5 Q20 26 25 23.5" stroke="white" stroke-width="1.4" stroke-linecap="round" fill="none"/>
      <line x1="20" y1="12" x2="20" y2="7.5" stroke="url(#lg2)" stroke-width="1.7" stroke-linecap="round"/>
      <circle cx="20" cy="6.5" r="2" fill="url(#lg2)"/>
      <rect x="5" y="16" width="4" height="6" rx="2" fill="url(#lg)" opacity=".65"/>
      <rect x="31" y="16" width="4" height="6" rx="2" fill="url(#lg)" opacity=".65"/>
    </svg>
    <div class="logo-text">
      <div class="brand">NexBot</div>
      <div class="sub">advanced rule-based AI · v3.0</div>
    </div>
  </div>
  <div class="hdr-right">
    <button class="theme-btn" onclick="cycleTheme()" title="Change theme">🎨</button>
    <button class="theme-btn" onclick="toggleSearch()" title="Search">🔍</button>
    <button class="theme-btn" onclick="toggleExport()" title="Export">⬇️</button>
    <span class="badge">python + flask</span>
    <div class="online-pill"><div class="pulse-dot"></div>Online</div>
  </div>
</header>

<!-- INFO BANNER -->
<div id="banner">
  <div class="ban-left">
    <div class="ban-icon">🧠</div>
    <div>
      <div class="ban-title">Rule-Based AI Chatbot — Python Project</div>
      <div class="ban-desc">If-else control flow · Sentiment detection · Fuzzy matching · 30+ topics</div>
    </div>
  </div>
  <div class="tags">
    <span class="tag">if-else</span>
    <span class="tag">fuzzy match</span>
    <span class="tag">sentiment</span>
    <span class="tag">flask</span>
  </div>
  <button class="ban-close" onclick="document.getElementById('banner').style.display='none'">✕</button>
</div>

<!-- CHAT -->
<div id="chat">
  <div id="welcome">
    <svg class="welcome-svg" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="wg" x1="0" y1="0" x2="80" y2="80" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stop-color="#5b8af5"/><stop offset="100%" stop-color="#a78bfa"/>
        </linearGradient>
      </defs>
      <rect x="2" y="2" width="76" height="76" rx="20" fill="url(#wg)" opacity=".12"/>
      <rect x="2" y="2" width="76" height="76" rx="20" stroke="url(#wg)" stroke-width="2"/>
      <rect x="16" y="24" width="48" height="32" rx="10" fill="url(#wg)"/>
      <circle cx="30" cy="38" r="5" fill="white"/>
      <circle cx="50" cy="38" r="5" fill="white"/>
      <circle cx="31.8" cy="36.5" r="2" fill="#1a1040"/>
      <circle cx="51.8" cy="36.5" r="2" fill="#1a1040"/>
      <path d="M28 47 Q40 53 52 47" stroke="white" stroke-width="2.5" stroke-linecap="round" fill="none"/>
      <line x1="40" y1="24" x2="40" y2="14" stroke="url(#wg)" stroke-width="3" stroke-linecap="round"/>
      <circle cx="40" cy="12" r="4" fill="url(#wg)"/>
      <rect x="9" y="32" width="7" height="12" rx="3.5" fill="url(#wg)" opacity=".55"/>
      <rect x="64" y="32" width="7" height="12" rx="3.5" fill="url(#wg)" opacity=".55"/>
    </svg>
    <h2>Hey, I'm NexBot v3.0! 🤖</h2>
    <p>Advanced rule-based AI with <strong>30+ topics</strong>, sentiment detection, fuzzy matching, riddles, and more! Say <strong>hi</strong> to begin! ✨</p>
    <div class="feature-grid">
      <div class="feat-card" onclick="sq('Tell me a joke')"><span class="fi">😄</span>Jokes</div>
      <div class="feat-card" onclick="sq('Tell me a riddle')"><span class="fi">🧩</span>Riddles</div>
      <div class="feat-card" onclick="sq('Tell me a fact')"><span class="fi">🤓</span>Facts</div>
      <div class="feat-card" onclick="sq('Motivate me')"><span class="fi">💪</span>Motivate</div>
      <div class="feat-card" onclick="sq('Help me study')"><span class="fi">📚</span>Study</div>
      <div class="feat-card" onclick="sq('Help')"><span class="fi">📋</span>All Features</div>
    </div>
  </div>
</div>

<!-- EMOJI PICKER -->
<div class="panel" id="epicker">
  <div class="panel-title">EMOJIS</div>
  <div class="e-grid">
    <span class="e" onclick="addE('😊')">😊</span><span class="e" onclick="addE('😄')">😄</span>
    <span class="e" onclick="addE('😂')">😂</span><span class="e" onclick="addE('🤔')">🤔</span>
    <span class="e" onclick="addE('😎')">😎</span><span class="e" onclick="addE('🙏')">🙏</span>
    <span class="e" onclick="addE('❤️')">❤️</span><span class="e" onclick="addE('🔥')">🔥</span>
    <span class="e" onclick="addE('✨')">✨</span><span class="e" onclick="addE('👍')">👍</span>
    <span class="e" onclick="addE('🎉')">🎉</span><span class="e" onclick="addE('💯')">💯</span>
    <span class="e" onclick="addE('🤖')">🤖</span><span class="e" onclick="addE('💻')">💻</span>
    <span class="e" onclick="addE('🐍')">🐍</span><span class="e" onclick="addE('😢')">😢</span>
    <span class="e" onclick="addE('😴')">😴</span><span class="e" onclick="addE('🍕')">🍕</span>
    <span class="e" onclick="addE('🎵')">🎵</span><span class="e" onclick="addE('🌟')">🌟</span>
    <span class="e" onclick="addE('🚀')">🚀</span><span class="e" onclick="addE('🧠')">🧠</span>
    <span class="e" onclick="addE('💡')">💡</span><span class="e" onclick="addE('🌈')">🌈</span>
  </div>
</div>

<!-- EXPORT PANEL -->
<div class="panel" id="xpanel">
  <div class="panel-title">EXPORT CHAT</div>
  <button class="xbtn" onclick="exportTxt()"><span class="xi">📄</span>Save as .txt</button>
  <button class="xbtn" onclick="copyAll()"><span class="xi">📋</span>Copy all</button>
  <button class="xbtn" onclick="clearChat()"><span class="xi">🗑️</span>Clear chat</button>
</div>

<!-- INPUT AREA -->
<div id="inp-area">
  <div class="chips-wrap">
    <button class="chip-arrow" onclick="scrollChips(-1)" title="Scroll left">&#8592;</button>
    <div class="chips" id="chips-row">
      <span class="chip" onclick="sq('Hello!')">👋 Hi<span class="chip-tip">Start a conversation! Say hello and NexBot will greet you back with your name.</span></span>
      <span class="chip" onclick="sq('Tell me a joke')">😄 Joke<span class="chip-tip">Get a random funny joke from 20 jokes. Tech, wordplay, puns and more!</span></span>
      <span class="chip" onclick="sq('Tell me a riddle')">🧩 Riddle<span class="chip-tip">Get a brain-teaser riddle. NexBot will reveal the answer in your next message!</span></span>
      <span class="chip" onclick="sq('Tell me a fact')">🤓 Fact<span class="chip-tip">Random amazing facts — science, animals, history. 20 unique facts in rotation!</span></span>
      <span class="chip" onclick="sq('What time is it?')">🕐 Time<span class="chip-tip">Shows current date, time, and week number from your server's clock.</span></span>
      <span class="chip" onclick="sq('25 plus 17')">🧮 Math<span class="chip-tip">Solve arithmetic: +, −, ×, ÷, powers, square roots, percentages. Try '15% of 200'!</span></span>
      <span class="chip" onclick="sq('Motivate me')">💪 Boost<span class="chip-tip">Get a powerful motivational quote from 16 unique messages to fire you up!</span></span>
      <span class="chip" onclick="sq('Help me study')">📚 Study<span class="chip-tip">Science-backed study techniques: Pomodoro, spaced repetition, active recall, and more!</span></span>
      <span class="chip" onclick="sq('Give me health tips')">🏥 Health<span class="chip-tip">12 expert health tips covering hydration, sleep, exercise, nutrition and posture.</span></span>
      <span class="chip" onclick="sq('What is programming')">💻 Coding<span class="chip-tip">Learn about programming languages — Python, JavaScript, Java, C++. Best for beginners!</span></span>
      <span class="chip" onclick="sq('Recommend music')">🎵 Music<span class="chip-tip">Music recommendations across 10 genres: lo-fi, jazz, classical, hip-hop, rock and more!</span></span>
      <span class="chip" onclick="sq('How to save money')">💰 Finance<span class="chip-tip">Personal finance tips: budgeting rules, investing basics, debt management, savings habits.</span></span>
      <span class="chip" onclick="sq('Give me career advice')">💼 Career<span class="chip-tip">Career guidance: resume writing, interview prep, networking, LinkedIn, and skill building.</span></span>
      <span class="chip" onclick="sq('Cooking tips')">🍳 Cooking<span class="chip-tip">Essential cooking skills: techniques, seasoning, knife skills, meal prep and easy recipes.</span></span>
      <span class="chip" onclick="sq('Travel tips')">✈️ Travel<span class="chip-tip">Smart travel hacks: cheap flights, packing light, travel insurance, and off-season tips.</span></span>
      <span class="chip" onclick="sq('Tell me about science')">🔬 Science<span class="chip-tip">Mind-blowing science facts: quantum physics, DNA, the universe, cells, and more!</span></span>
      <span class="chip" onclick="sq('Tell me about history')">📜 History<span class="chip-tip">Fascinating history: ancient civilizations, inventions, wars, and world-changing events.</span></span>
      <span class="chip" onclick="sq('Climate change')">🌱 Eco<span class="chip-tip">Practical eco tips: recycling right, reducing carbon footprint, saving water and energy.</span></span>
      <span class="chip" onclick="sq('How to sleep better')">😴 Sleep<span class="chip-tip">8 science-based sleep tips: sleep schedule, room temperature, caffeine cutoff and more.</span></span>
      <span class="chip" onclick="sq('Productivity tips')">⚡ Productivity<span class="chip-tip">Work smarter: deep work, time blocking, the 2-minute rule, and beating procrastination!</span></span>
      <span class="chip" onclick="sq('Relationship advice')">💙 Relations<span class="chip-tip">Relationship wisdom: active listening, communication, boundaries, and friendship tips.</span></span>
      <span class="chip" onclick="sq('Tell me about space')">🌌 Space<span class="chip-tip">Amazing space facts: black holes, planets, the Sun, the Moon, and our galaxy!</span></span>
      <span class="chip" onclick="sq('Tell me about football')">⚽ Sports<span class="chip-tip">Sports facts and trivia: football, cricket, basketball, tennis and more!</span></span>
      <span class="chip" onclick="sq('Capital of Japan')">🌍 Capital<span class="chip-tip">Know capitals of 28 countries! Try: 'Capital of France', 'Capital of Pakistan'.</span></span>
      <span class="chip" onclick="sq('Give me advice')">💡 Advice<span class="chip-tip">14 pieces of timeless life wisdom on focus, habits, relationships and growth.</span></span>
      <span class="chip" onclick="sq('Help')">📋 Help<span class="chip-tip">See the full list of everything NexBot can do — all 28 topics and features!</span></span>
    </div>
    <button class="chip-arrow" onclick="scrollChips(1)" title="Scroll right">&#8594;</button>
  </div>
  <div class="inp-row">
    <div class="inp-wrap">
      <textarea id="user-input" rows="1" placeholder="Type a message… 💬" maxlength="500"></textarea>
      <button class="icon-btn" onclick="toggleEmoji()" title="Emoji">😊</button>
    </div>
    <button id="send-btn" onclick="send()">
      <svg width="17" height="17" viewBox="0 0 24 24" fill="white"><path d="M2 21l21-9L2 3v7l15 2-15 2v7z"/></svg>
    </button>
  </div>
  <div class="inp-footer">
    <span class="char-count" id="cc">0 / 500</span>
    <span class="inp-hint">Enter to send · Shift+Enter for new line</span>
  </div>
</div>

<!-- TOAST -->
<div id="toast"></div>

<script>
const SID = 'sid_' + Math.random().toString(36).substr(2,9);
const chatEl = document.getElementById('chat');
const inp = document.getElementById('user-input');
let welcomeUp = true;
let msgCount = 0;
let allMessages = [];
const themes = ['','theme-purple','theme-cyan','theme-green'];
let themeIdx = 0;

const BOT_SVG = `<svg viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="ba" x1="0" y1="0" x2="30" y2="30" gradientUnits="userSpaceOnUse"><stop offset="0%" stop-color="#5b8af5"/><stop offset="100%" stop-color="#a78bfa"/></linearGradient></defs><rect x="6" y="9" width="18" height="13" rx="4" fill="url(#ba)"/><circle cx="11" cy="15" r="2" fill="white"/><circle cx="19" cy="15" r="2" fill="white"/><circle cx="11.7" cy="14.3" r=".9" fill="#1a1040"/><circle cx="19.7" cy="14.3" r=".9" fill="#1a1040"/><path d="M10.5 19.5 Q15 22 19.5 19.5" stroke="white" stroke-width="1.2" stroke-linecap="round" fill="none"/><line x1="15" y1="9" x2="15" y2="5" stroke="url(#ba)" stroke-width="1.6" stroke-linecap="round"/><circle cx="15" cy="4" r="1.6" fill="url(#ba)"/><rect x="2.5" y="12" width="3.5" height="5" rx="1.75" fill="url(#ba)" opacity=".6"/><rect x="24" y="12" width="3.5" height="5" rx="1.75" fill="url(#ba)" opacity=".6"/></svg>`;

const REACTIONS = ['👍','❤️','😂','😮','😢'];

function now(){ return new Date().toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'}); }

function md(t){
  return t
    .replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>')
    .replace(/\\n/g,'<br>');
}

function addMsg(text, isUser=false, type='normal'){
  if(welcomeUp){ const w=document.getElementById('welcome'); if(w) w.remove(); welcomeUp=false; }
  msgCount++;
  allMessages.push({role:isUser?'user':'bot', text, time:now(), type});

  const row = document.createElement('div');
  row.className = `msg-row${isUser?' user':''}`;
  row.dataset.id = msgCount;

  const av = document.createElement('div');
  av.className = `av ${isUser?'usr':'bot'}`;
  av.innerHTML = isUser ? '😊' : BOT_SVG;

  const wrap = document.createElement('div');
  wrap.style.display = 'flex';
  wrap.style.flexDirection = 'column';

  const bub = document.createElement('div');
  bub.className = `bub ${isUser?'usr':'bot '+type}`;
  bub.innerHTML = md(text);

  // Typing effect for bot messages
  if(!isUser){
    const full = bub.innerHTML;
    bub.innerHTML = '';
    let i = 0;
    const raw = full.replace(/<[^>]+>/g,'');
    typeText(bub, full, 0);
  }

  const meta = document.createElement('div');
  meta.className = 'meta';

  const ts = document.createElement('span');
  ts.className = 'ts'; ts.textContent = now();

  const rbar = document.createElement('div');
  rbar.className = 'react-bar';
  REACTIONS.forEach(r=>{
    const btn = document.createElement('button');
    btn.className = 'react-btn'; btn.textContent = r;
    btn.onclick = ()=> addReaction(btn, r, row);
    rbar.appendChild(btn);
  });

  meta.append(ts, rbar);
  wrap.append(bub, meta);
  row.append(av, wrap);
  chatEl.appendChild(row);
  chatEl.scrollTop = chatEl.scrollHeight;
}

function typeText(el, html, idx){
  // Fast character-by-character reveal
  const chars = html.split('');
  let out = '';
  let i = 0;
  const speed = Math.max(8, Math.min(18, 600/chars.length));
  function step(){
    if(i >= chars.length){ el.innerHTML = html; return; }
    // skip through tags instantly
    if(chars[i] === '<'){
      while(i < chars.length && chars[i] !== '>') out += chars[i++];
      out += chars[i++] || '';
    } else {
      out += chars[i++];
    }
    el.innerHTML = out;
    chatEl.scrollTop = chatEl.scrollHeight;
    setTimeout(step, speed);
  }
  step();
}

function addReaction(btn, emoji, row){
  const existing = row.querySelector(`.react-count[data-e="${emoji}"]`);
  if(existing){ existing.textContent = parseInt(existing.textContent)+1; return; }
  const span = document.createElement('span');
  span.className = 'react-count'; span.dataset.e = emoji;
  span.textContent = '1';
  btn.after(document.createTextNode(' '), span);
  showToast(emoji + ' Reaction added!');
}

function showTyping(){
  const r = document.createElement('div');
  r.className='typ-row'; r.id='typing';
  r.innerHTML=`<div class="av bot">${BOT_SVG}</div><div class="typ-bub"><div class="d"></div><div class="d"></div><div class="d"></div></div>`;
  chatEl.appendChild(r); chatEl.scrollTop=chatEl.scrollHeight;
}
function hideTyping(){ const t=document.getElementById('typing'); if(t) t.remove(); }

async function send(){
  const txt = inp.value.trim();
  if(!txt) return;
  addMsg(txt, true);
  inp.value=''; inp.style.height='auto';
  document.getElementById('cc').textContent = '0 / 500';
  showTyping();
  await new Promise(r=>setTimeout(r, 300+Math.random()*500));
  try{
    const res = await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:txt,session_id:SID})});
    const d = await res.json();
    hideTyping();
    addMsg(d.message, false, d.type||'normal');
  } catch{
    hideTyping();
    addMsg('⚠️ Connection error! Make sure Flask is running.', false,'warning');
  }
}

function sq(t){ inp.value=t; send(); }

function scrollChips(dir){
  const row = document.getElementById('chips-row');
  row.scrollBy({left: dir * 220, behavior: 'smooth'});
}

// ── Emoji picker ───────────────────────────────────────────────────────────
function toggleEmoji(){ document.getElementById('epicker').classList.toggle('open'); document.getElementById('xpanel').classList.remove('open'); }
function addE(e){ inp.value+=e; inp.focus(); document.getElementById('epicker').classList.remove('open'); }

// ── Export panel ───────────────────────────────────────────────────────────
function toggleExport(){ document.getElementById('xpanel').classList.toggle('open'); document.getElementById('epicker').classList.remove('open'); }

function exportTxt(){
  const lines = allMessages.map(m=>`[${m.time}] ${m.role.toUpperCase()}: ${m.text.replace(/<[^>]+>/g,'')}`);
  const blob = new Blob([lines.join('\\n')], {type:'text/plain'});
  const a = document.createElement('a'); a.href=URL.createObjectURL(blob);
  a.download = `nexbot_chat_${new Date().toISOString().slice(0,10)}.txt`;
  a.click(); document.getElementById('xpanel').classList.remove('open');
  showToast('💾 Chat saved!');
}

function copyAll(){
  const lines = allMessages.map(m=>`${m.role==='user'?'You':'NexBot'}: ${m.text.replace(/<[^>]+>/g,'')}`);
  navigator.clipboard.writeText(lines.join('\\n')).then(()=>showToast('📋 Copied!'));
  document.getElementById('xpanel').classList.remove('open');
}

function clearChat(){
  chatEl.innerHTML=''; allMessages=[]; msgCount=0;
  document.getElementById('xpanel').classList.remove('open');
  showToast('🗑️ Chat cleared!');
}

// ── Theme ──────────────────────────────────────────────────────────────────
function cycleTheme(){
  document.body.classList.remove(themes[themeIdx]);
  themeIdx = (themeIdx+1)%themes.length;
  if(themes[themeIdx]) document.body.classList.add(themes[themeIdx]);
  const names = ['🔵 Blue','🟣 Purple','🩵 Cyan','🟢 Green'];
  showToast(names[themeIdx]+' theme!');
}

// ── Search ─────────────────────────────────────────────────────────────────
function toggleSearch(){
  const sb = document.getElementById('search-bar');
  sb.classList.toggle('open');
  if(sb.classList.contains('open')) document.getElementById('search-inp').focus();
}
function closeSearch(){ document.getElementById('search-bar').classList.remove('open'); clearHighlights(); }
function searchMsgs(q){
  clearHighlights();
  if(!q) return;
  const bubs = chatEl.querySelectorAll('.bub');
  let found = false;
  bubs.forEach(b=>{
    if(b.innerHTML.toLowerCase().includes(q.toLowerCase())){
      b.style.outline = '2px solid var(--a1)';
      if(!found){ b.scrollIntoView({behavior:'smooth',block:'center'}); found=true; }
    }
  });
  if(!found) showToast('No results found');
}
function clearHighlights(){ chatEl.querySelectorAll('.bub').forEach(b=>b.style.outline=''); }

// ── Toast ──────────────────────────────────────────────────────────────────
function showToast(msg){
  const t = document.getElementById('toast');
  t.textContent = msg; t.classList.add('show');
  setTimeout(()=>t.classList.remove('show'), 2200);
}

// ── Close panels on outside click ─────────────────────────────────────────
document.addEventListener('click', e=>{
  if(!e.target.closest('#epicker') && !e.target.closest('.icon-btn')) document.getElementById('epicker').classList.remove('open');
  if(!e.target.closest('#xpanel') && e.target.textContent!=='⬇️') document.getElementById('xpanel').classList.remove('open');
});

// ── Input events ──────────────────────────────────────────────────────────
inp.addEventListener('keydown', e=>{ if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();send();} });
inp.addEventListener('input', function(){
  this.style.height='auto';
  this.style.height=Math.min(this.scrollHeight,88)+'px';
  document.getElementById('cc').textContent = `${this.value.length} / 500`;
});
</script>
</body>
</html>"""

# ── Routes ──────────────────────────────────────────────────────────────────
@app.route('/')
def index(): return HTML

@app.route('/chat', methods=['POST'])
def chat():
    d = request.get_json()
    msg = d.get('message','').strip()
    sid = d.get('session_id','default')
    if not msg: return jsonify({"message":"Please say something! 😊","type":"warning"})
    return jsonify(get_response(msg, sid))

# ── Run ─────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("\n" + "═"*55)
    print("   🤖  NexBot v3.0 — Advanced Rule-Based AI Chatbot")
    print("═"*55)
    print("   ✅  Server starting...")
    print("   🌐  Open: http://127.0.0.1:5000")
    print("   ⛔  Stop: CTRL+C")
    print("═"*55 + "\n")
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
