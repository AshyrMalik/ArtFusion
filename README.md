
---

# Art Fusion: Neural Style Transfer with FastAPI & React

Art Fusion is a neural style transfer project that transforms your images by blending content and style. This project demonstrates how to convert "just pure random noise into something amazing" using a concise, yet powerful, implementation—**style transfer in less than 150 lines** of code.

My main focus was learning style transfer techniques, and I built both a FastAPI backend and a React frontend to revise and hone my skills with these technologies.

---

## Features

- **Neural Style Transfer:** Uses PyTorch with a pretrained VGG19 model to merge the content of one image with the style of another.
- **FastAPI Backend:** Provides an endpoint for performing style transfer on uploaded images.
- **React Frontend:** An intuitive interface to upload images, select an artistic style, and view the stylized result.
- **Compact & Efficient:** Achieves the style transfer functionality with a minimal and clean codebase.

---

## Project Structure

```
.
├── backend
│   ├── main.py            # FastAPI server with style transfer endpoint
│   └── requirements.txt   # Python dependencies
├── frontend
│   ├── src
│   │   ├── components
│   │   │   └── StyleTransfer.jsx  # React component for style transfer
│   │   └── App.js         # Main React application file
│   └── package.json       # Frontend dependencies
└── README.md
```

---

## Installation

### Backend Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/art-fusion.git
   cd art-fusion/backend
   ```

2. **Set Up Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the FastAPI Server:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Navigate to the Frontend Directory:**
   ```bash
   cd ../frontend
   ```

2. **Install Dependencies:**
   ```bash
   npm install
   ```

3. **Start the React App:**
   ```bash
   npm start
   ```
   The application should now be running on [http://localhost:3000](http://localhost:3000).

---

## Usage

1. **Upload Image:** Use the React interface to upload the content image you want to transform.
2. **Select Style:** Choose from a range of style options (e.g., Van Gogh’s Starry Night, Munch’s The Scream, or Hokusai’s The Great Wave).
3. **Generate:** Click the "Generate Stylized Image" button. The backend will process your image using neural style transfer and return the result.
4. **View Result:** The transformed image will be displayed directly in the frontend.

---

## Customization

Feel free to modify the style options or adjust model parameters to experiment with different artistic effects. The code is structured to be simple and adaptable, making it easy to expand or integrate additional features.

---

## Contributing

Contributions are welcome! If you have suggestions or improvements, please fork the repository and submit a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## Acknowledgements

- **[FastAPI](https://fastapi.tiangolo.com/):** For providing an easy-to-use framework for building the backend.
- **[PyTorch](https://pytorch.org/):** For the deep learning capabilities that power the style transfer.
- **[React](https://reactjs.org/):** For the frontend framework that creates a smooth user experience.
- Thanks to the open-source community for the tools and inspiration behind this project.

---
