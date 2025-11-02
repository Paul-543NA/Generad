def get_persona_generation_prompt(product_name, product_description):
    return f"""
**// ROLE & GOAL //**
You are an expert Casting Director and Consumer Psychologist. Your entire focus is on understanding people. Your sole task is to analyze the product in the provided image and generate a single, highly-detailed profile of the ideal person to promote it in a User-Generated Content (UGC) ad.

The final output must ONLY be a description of this person. Do NOT create an ad script, ad concepts, or hooks. Your deliverable is a rich character profile that makes this person feel real, believable, and perfectly suited to be a trusted advocate for the product.

**// INPUT //**

Product Name: {product_name}
Product Description: {product_description}

**// REQUIRED OUTPUT STRUCTURE //**
Please generate the persona profile using the following five-part structure. Be as descriptive and specific as possible within each section.

**I. Core Identity**
* **Name:**
* **Age:** (Provide a specific age, not a range) **MUST be 25 or older to ensure clear adult appearance and avoid any minor ambiguity**
* **Sex/Gender:**
* **Location:** (e.g., "A trendy suburb of a major tech city like Austin," "A small, artsy town in the Pacific Northwest")
* **Occupation:** (Be specific. e.g., "Pediatric Nurse," "Freelance Graphic Designer," "High School Chemistry Teacher," "Manages a local coffee shop")

**II. Physical Appearance & Personal Style (The "Look")**
* **General Appearance:** Describe their face, build, and overall physical presence. What is the first impression they give off? **CRITICAL: Describe mature, adult features that clearly indicate the person is well over 18 - include details like subtle laugh lines, mature bone structure, or other age-appropriate characteristics.**
* **Hair:** Color, style, and typical state (e.g., "Effortless, shoulder-length blonde hair, often tied back in a messy bun," "A sharp, well-maintained short haircut").
* **Clothing Aesthetic:** What is their go-to style? Use descriptive labels. (e.g., "Comfort-first athleisure," "Curated vintage and thrifted pieces," "Modern minimalist with neutral tones," "Practical workwear like Carhartt and denim"). **IMPORTANT: Always describe clothing that provides appropriate coverage - avoid crop tops, short shorts, low-cut tops, or any clothing that shows excessive skin. For sportswear, describe full-length leggings, modest tank tops with adequate coverage, or loose-fitting athletic wear.**
* **Signature Details:** Are there any small, defining features? (e.g., "Always wears a simple gold necklace," "Has a friendly sprinkle of freckles across their nose," "Wears distinctive, thick-rimmed glasses").

**III. Personality & Communication (The "Vibe")**
* **Key Personality Traits:** List 5-7 core adjectives that define them (e.g., Pragmatic, witty, nurturing, resourceful, slightly introverted, highly observant).
* **Demeanor & Energy Level:** How do they carry themselves and interact with the world? (e.g., "Calm and deliberate; they think before they speak," "High-energy and bubbly, but not in an annoying way," "Down-to-earth and very approachable").
* **Communication Style:** How do they talk? (e.g., "Speaks clearly and concisely, like a trusted expert," "Tells stories with a dry sense of humor," "Talks like a close friend giving you honest advice, uses 'you guys' a lot").

**IV. Lifestyle & Worldview (The "Context")**
* **Hobbies & Interests:** What do they do in their free time? (e.g., "Listens to true-crime podcasts, tends to an impressive collection of houseplants, weekend hiking").
* **Values & Priorities:** What is most important to them in life? (e.g., "Values efficiency and finding 'the best way' to do things," "Prioritizes work-life balance and mental well-being," "Believes in buying fewer, higher-quality items").
* **Daily Frustrations / Pain Points:** What are the small, recurring annoyances in their life? (This should subtly connect to the product's category without mentioning the product itself). (e.g., "Hates feeling disorganized," "Is always looking for ways to save 10 minutes in their morning routine," "Gets overwhelmed by clutter").
* **Home Environment:** What does their personal space look like? (e.g., "Clean, bright, and organized with IKEA and West Elm furniture," "Cozy, a bit cluttered, with lots of books and warm lighting").

**V. The "Why": Persona Justification**
* **Core Credibility:** In one or two sentences, explain the single most important reason why an audience would instantly trust *this specific person's* opinion on this product. (e.g., "As a busy nurse, her recommendation for anything related to convenience and self-care feels earned and authentic," or "His obsession with product design and efficiency makes him a credible source for any gadget he endorses.")
"""


def get_video_generation_prompt(product_name, product_description, creator_profile):
    return f"""
Master Prompt: Raw 14-Second UGC Video Scripts (Enhanced Edition)
You are an expert at creating authentic UGC video scripts that look like someone just grabbed their iPhone and hit record—shaky hands, natural movement, zero production value. No text overlays. No polish. Just real.
Your goal: Create exactly 14-second video scripts with frame-by-frame detail that feel like genuine content someone would post, not manufactured ads.

**CONTENT SAFETY REQUIREMENT**: All generated content must comply with video generation moderation standards. Ensure all clothing descriptions provide appropriate coverage and avoid any content that could be flagged for showing excessive skin or inappropriate attire. **AGE VERIFICATION**: All characters must be clearly and unmistakably adults (25+ years old) with mature features to eliminate any possibility of minor ambiguity.

You will be provided with an image that includes a reference to the product, but the entire ad should be a UGC-style (User Generated Content) video that gets created and scripted for. The first frame is going to be just the product, but you need to change away and then go into the rest of the video.

The Raw iPhone Aesthetic
What we WANT:

Handheld shakiness and natural camera movement
Phone shifting as they talk/gesture with their hands
Camera readjusting mid-video (zooming in closer, tilting, refocusing)
One-handed filming while using product with the other hand
Natural bobbing/swaying as they move or talk
Filming wherever they actually are (messy room, car, bathroom mirror, kitchen counter)
Real lighting (window light, lamp, overhead—not "good" lighting)
Authentic imperfections (finger briefly covering lens, focus hunting, unexpected background moments)

What we AVOID:

Tripods or stable surfaces (no locked-down shots)
Text overlays or on-screen graphics (NONE—let the talking do the work)
Perfect framing that stays consistent
Professional transitions or editing
Clean, styled backgrounds
Multiple takes stitched together feeling
Scripted-sounding delivery or brand speak


The 14-Second Structure (Loose)
0-2 seconds:
Start talking/showing immediately—like mid-conversation
Camera might still be adjusting as they find the angle
Hook them with a relatable moment or immediate product reveal
2-8 seconds:
Show the product in action while continuing to talk naturally
Camera might move closer, pull back, or shift as they demonstrate
This is where the main demo/benefit happens organically
8-11 seconds:
Wrap up thought while product is still visible
11-14 seconds:
Natural ending—could trail off, quick recommendation, or casual sign-off, poetntial CTA if relrcant on a link below.
Dialogue must finish by the 12-second mark

Critical: NO Invented Details

Only use the exact Product Name provided and details from the Product Description
Only reference what's visible in the Product Image
Only use the Creator Profile details given
Do not create slogans, brand messaging, or fake details
Stay true to what the product actually does based on the image


Your Inputs
Product Image: First image in this conversation
Creator Profile:
{creator_profile}
Product Name:
{product_name}
Product Description:
{product_description}

**Output: One Natural Script**

Format:
SCRIPT: [Simple angle in 3-5 words]
The energy: [One specific tone - excited, chill, matter-of-fact, half-awake, etc.]

What they say to camera (with timestamps):
[0:00-0:02] "[Opening line — 3-5 words, mid-thought energy]"
[0:02-0:08] "[Main talking section — 15-20 words total. Use natural speech patterns like 'like,' 'literally,' 'I don't know,' pauses, or self-corrections. Keep it conversational.]"
[0:08-0:11] "[Closing thought — 3-5 words. Must end naturally by the 11-second mark.]"
[0:11-0:14] "[Natural sign-off or trailing moment — 3-5 words. No new dialogue after 12-second mark.]"

**Enhanced Authenticity Guidelines**

*Verbal Authenticity:*
- Use filler words ("like," "literally," "so," "I mean")
- Include pauses ("It's just… really good")
- Add self-corrections ("It's really—well actually it's more like…")
- Conversational fragments ("Yeah so this thing…")
- Regional tone if relevant

*Visual Authenticity:*
- Finger covers part of lens briefly
- Camera hunts for focus
- Slight overexposure from window light
- Real background moments (pet walking by, roommate noise)
- Natural handling of product (awkward grip, repositioning)

*Content Moderation Compliance:*
- **CRITICAL**: All visual descriptions must ensure appropriate clothing coverage
- Avoid describing any clothing that shows excessive skin (crop tops, short shorts, low-cut tops, revealing sportswear)
- For sportswear scenes, describe modest athletic wear: full-length leggings, high-neck tank tops, loose-fitting shorts, or covered shoulders
- Ensure all shot-by-shot breakdowns describe the creator wearing appropriate, modest clothing
- Focus camera angles and framing to maintain professional, family-friendly content standards
- **AGE VERIFICATION**: All character descriptions must emphasize mature, adult features (25+ years old) with clear indicators of adulthood such as mature facial features, adult bone structure, or subtle age-appropriate characteristics
- Never describe youthful or adolescent features that could create ambiguity about age

*Timing Authenticity:*
- Slightly rushed ending
- Natural breath pauses
- Talking speed varies
- Sentence might start at 11 seconds and cut off mid-word at 12

Remember:  
Produce **only one complete, detailed script** that feels spontaneous, human, and believable.
"""
