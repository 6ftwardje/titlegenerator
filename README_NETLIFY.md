# Cryptoriez Short Titler & Describer - Netlify Deployment

This is a web-based version of the Cryptoriez Short Titler & Describer application, converted from Streamlit to a static web application for deployment on Netlify.

## 🚀 Quick Deploy to Netlify

### Option 1: Deploy from Git (Recommended)

1. **Push your code to GitHub/GitLab/Bitbucket**
   ```bash
   git add .
   git commit -m "Add Netlify deployment files"
   git push origin main
   ```

2. **Connect to Netlify**
   - Go to [netlify.com](https://netlify.com)
   - Sign up/Login with your Git provider
   - Click "New site from Git"
   - Choose your repository
   - Netlify will automatically detect the settings from `netlify.toml`

3. **Deploy**
   - Click "Deploy site"
   - Your site will be live in minutes!

### Option 2: Manual Deploy

1. **Build locally** (optional - not required for this static site)
2. **Drag & Drop to Netlify**
   - Go to [netlify.com](https://netlify.com)
   - Drag your project folder to the deploy area
   - Your site will be live instantly!

## 📁 Project Structure

```
├── index.html          # Main HTML file
├── styles.css          # CSS styling
├── script.js           # JavaScript functionality
├── netlify.toml        # Netlify configuration
└── README_NETLIFY.md   # This file
```

## ⚙️ Configuration

The `netlify.toml` file includes:
- **Build settings**: Publishes from the current directory
- **Redirects**: Handles client-side routing
- **Security headers**: XSS protection, frame options, etc.
- **Node version**: Specifies Node.js 18

## 🔧 Customization

### Environment Variables
If you want to add real AI functionality later, you can add environment variables in Netlify:
1. Go to Site Settings > Environment Variables
2. Add your API keys (e.g., `OPENAI_API_KEY`)

### Custom Domain
1. Go to Site Settings > Domain Management
2. Add your custom domain
3. Follow the DNS configuration instructions

## 🌐 Features

- **Responsive Design**: Works on all devices
- **Drag & Drop**: Easy file upload interface
- **Mock AI**: Simulates the original app's functionality
- **Modern UI**: Beautiful, professional design
- **Copy/Download**: Easy content management

## 🔄 Updates

To update your deployed site:
1. Make changes to your code
2. Commit and push to Git
3. Netlify automatically redeploys

## 📱 Mobile Support

The application is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones
- All modern browsers

## 🚨 Important Notes

- **Current Version**: This is a demo version with mock AI responses
- **Real AI Integration**: To use real OpenAI API, you'll need to modify `script.js`
- **File Processing**: Video files are processed client-side for demo purposes
- **Storage**: No files are stored on Netlify servers

## 🆘 Support

If you encounter issues:
1. Check the Netlify deployment logs
2. Verify your `netlify.toml` configuration
3. Ensure all files are in the root directory
4. Check browser console for JavaScript errors

## 🔮 Future Enhancements

To add real AI functionality:
1. Create a serverless function (Netlify Functions)
2. Integrate with OpenAI API
3. Add real video processing
4. Implement user authentication

---

**Happy Deploying! 🎉**
