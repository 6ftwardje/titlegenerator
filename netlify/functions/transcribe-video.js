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

    // Initialize OpenAI client
    const openai = new OpenAI({
      apiKey: openaiApiKey,
    });

    // Parse multipart form data
    const boundary = event.headers['content-type']?.split('boundary=')[1];
    if (!boundary) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ 
          success: false, 
          error: 'No multipart boundary found' 
        })
      };
    }

    // Parse the multipart data
    const parts = parseMultipartData(event.body, boundary);
    const videoFile = parts.find(part => part.name === 'video');

    if (!videoFile) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ 
          success: false, 
          error: 'No video file found in request' 
        })
      };
    }

    // Check file size (limit to 25MB for Whisper API)
    const maxSize = 25 * 1024 * 1024; // 25MB
    if (videoFile.data.length > maxSize) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ 
          success: false, 
          error: 'Video file too large. Maximum size is 25MB.' 
        })
      };
    }

    // Convert to buffer and create file object
    const buffer = Buffer.from(videoFile.data, 'base64');
    const file = new File([buffer], videoFile.filename, {
      type: videoFile.contentType || 'video/mp4'
    });

    // Transcribe using OpenAI Whisper
    const transcript = await openai.audio.transcriptions.create({
      file: file,
      model: 'whisper-1',
      language: 'nl', // Default to Dutch
      response_format: 'text'
    });

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        transcript: transcript
      })
    };

  } catch (error) {
    console.error('Transcription error:', error);
    
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        success: false,
        error: error.message || 'Internal server error during transcription'
      })
    };
  }
};

// Helper function to parse multipart form data
function parseMultipartData(body, boundary) {
  const parts = [];
  const boundaryStr = `--${boundary}`;
  const sections = body.split(boundaryStr);
  
  for (let i = 1; i < sections.length - 1; i++) {
    const section = sections[i];
    const lines = section.split('\r\n');
    
    let part = {};
    let dataStart = -1;
    
    for (let j = 0; j < lines.length; j++) {
      const line = lines[j];
      
      if (line.startsWith('Content-Disposition:')) {
        const nameMatch = line.match(/name="([^"]+)"/);
        const filenameMatch = line.match(/filename="([^"]+)"/);
        
        if (nameMatch) part.name = nameMatch[1];
        if (filenameMatch) part.filename = filenameMatch[1];
      } else if (line.startsWith('Content-Type:')) {
        part.contentType = line.split(': ')[1];
      } else if (line === '') {
        dataStart = j + 1;
        break;
      }
    }
    
    if (dataStart !== -1) {
      part.data = lines.slice(dataStart).join('\r\n');
      parts.push(part);
    }
  }
  
  return parts;
}
