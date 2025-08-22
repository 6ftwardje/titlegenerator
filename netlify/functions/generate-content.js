const { OpenAI } = require('openai');

exports.handler = async (event, context) => {
  // Enable CORS
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS'
  };

  // Handle preflight OPTIONS request
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers,
      body: ''
    };
  }

  try {
    // Check if it's a POST request
    if (event.httpMethod !== 'POST') {
      return {
        statusCode: 405,
        headers,
        body: JSON.stringify({ success: false, error: 'Method not allowed' })
      };
    }

    // Get OpenAI API key from environment variables
    const openaiApiKey = process.env.OPENAI_API_KEY;
    if (!openaiApiKey) {
      return {
        statusCode: 500,
        headers,
        body: JSON.stringify({ 
          success: false, 
          error: 'OpenAI API key not configured' 
        })
      };
    }

    // Parse request body
    const { transcript, preferences } = JSON.parse(event.body);

    if (!transcript) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ 
          success: false, 
          error: 'Transcript is required' 
        })
      };
    }

    // Initialize OpenAI client
    const openai = new OpenAI({
      apiKey: openaiApiKey,
    });

    // Build the system prompt
    const systemPrompt = buildSystemPrompt(preferences);

    // Build the user prompt
    const userPrompt = buildUserPrompt(transcript, preferences);

    // Generate content using OpenAI
    const response = await openai.chat.completions.create({
      model: 'gpt-4o-mini',
      temperature: 0.7,
      messages: [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: userPrompt }
      ],
      response_format: { type: 'json_object' }
    });

    // Parse the response
    const content = JSON.parse(response.choices[0].message.content);

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        content: {
          title: content.title || '',
          description: content.description || '',
          hashtags: content.hashtags || []
        }
      })
    };

  } catch (error) {
    console.error('Content generation error:', error);
    
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        success: false,
        error: error.message || 'Internal server error during content generation'
      })
    };
  }
};

function buildSystemPrompt(preferences) {
  const language = preferences.language || 'nl';
  
  if (language === 'nl') {
    return `Je bent een ervaren Nederlandstalige content-editor voor Cryptoriez (focus: trading, crypto & forex, marktbreakdowns, updates).

Stijl:
- Duidelijk, concreet, "no nonsense"
- Geen overbodige vakjargon; leg kort uit voor niet-technische kijkers
- Houd het geloofwaardig: prikkelende titels zijn oké, maar geen misleiding
- Zet inhoud voorop; clickbait-intensiteit bepaalt scherpte/urgentie, niet de waarheid
- Respecteer voorkeuren voor emoji's en hashtags

Taken:
1) Bedenk 1 sterke, platform-agnostische titel op basis van transcript + topic_hint
2) Schrijf een beschrijving met:
   - 2–5 kerninzichten of takeaways
   - Korte context "wat betekent dit voor markt/risico/sentiment"
   - Call-to-action (bv. volg voor meer breakdowns)
3) Voeg optioneel hashtags toe (relevant, 5–10 max)

Uitvoer in JSON met velden: title, description, hashtags (array).`;
  } else {
    return `You are an experienced English-speaking content editor for Cryptoriez (focus: trading, crypto & forex, market breakdowns, updates).

Style:
- Clear, concrete, "no nonsense"
- No unnecessary jargon; explain briefly for non-technical viewers
- Keep it credible: engaging titles are okay, but no deception
- Put content first; clickbait intensity determines sharpness/urgency, not truth
- Respect preferences for emojis and hashtags

Tasks:
1) Create 1 strong, platform-agnostic title based on transcript + topic_hint
2) Write a description with:
   - 2-5 key insights or takeaways
   - Brief context "what this means for market/risk/sentiment"
   - Call-to-action (e.g., follow for more breakdowns)
3) Optionally add hashtags (relevant, 5-10 max)

Output in JSON with fields: title, description, hashtags (array).`;
  }
}

function buildUserPrompt(transcript, preferences) {
  const language = preferences.language || 'nl';
  const useEmojis = preferences.useEmojis !== false;
  const useHashtags = preferences.useHashtags !== false;
  const clickbaitLevel = preferences.clickbaitLevel || 5;
  const platforms = preferences.platforms || ['Alle'];
  const topicHint = preferences.topicHint || 'Crypto/Forex market update or trade breakdown';

  if (language === 'nl') {
    const emojiRule = useEmojis ? "Je mag emoji's gebruiken waar relevant." : "Gebruik geen emoji's.";
    const hashtagRule = useHashtags ? "Sluit af met 5–10 relevante hashtags." : "Voeg géén hashtags toe.";
    
    const clickbaitGuidance = `Clickbait-intensiteit: ${clickbaitLevel} op 10.
- 0–2: informatief, neutraal
- 3–5: prikkelend, concreet
- 6–8: urgent, sterk hook
- 9–10: zeer agressief (maar geloofwaardig, geen sensationalisme/garanties)`;

    return `Taal: ${language}
Platforms: ${platforms.join(', ')}
Topic hint: ${topicHint}

${emojiRule}
${hashtagRule}
${clickbaitGuidance}

Transcript (ruw, samenvatten & opschonen):
"""${transcript.trim()}"""`;
  } else {
    const emojiRule = useEmojis ? "You may use emojis where relevant." : "Do not use emojis.";
    const hashtagRule = useHashtags ? "End with 5-10 relevant hashtags." : "Do not add hashtags.";
    
    const clickbaitGuidance = `Clickbait intensity: ${clickbaitLevel} out of 10.
- 0-2: informative, neutral
- 3-5: engaging, concrete
- 6-8: urgent, strong hook
- 9-10: very aggressive (but credible, no sensationalism/guarantees)`;

    return `Language: ${language}
Platforms: ${platforms.join(', ')}
Topic hint: ${topicHint}

${emojiRule}
${hashtagRule}
${clickbaitGuidance}

Transcript (raw, summarize & clean up):
"""${transcript.trim()}"""`;
  }
}
