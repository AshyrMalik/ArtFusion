import React, { useState } from 'react';
import { Upload, Image as LucideImage, Loader } from 'lucide-react';
import './StyleTransfer.css';

const StyleTransfer = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [processedImage, setProcessedImage] = useState(null);
  const [selectedStyle, setSelectedStyle] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [statusMessage, setStatusMessage] = useState('');

  const styleOptions = [
    {
      id: 'starry-night',
      name: 'Starry Night - Van Gogh',
      thumbnail: '/image1.jpg',
      description: 'Transform your image in the style of Van Gogh\'s famous masterpiece'
    },
    {
      id: 'scream',
      name: 'The Scream - Munch',
      thumbnail: '/image2.jpg',
      description: 'Apply the dramatic style of Munch\'s expressionist painting'
    },
    {
      id: 'great-wave',
      name: 'The Great Wave - Hokusai',
      thumbnail: '/image3.jpg',
      description: 'Convert your image using the style of this iconic Japanese woodblock print'
    }
  ];

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file && file.type.startsWith('image/')) {
      setSelectedImage(file);
      const imageUrl = URL.createObjectURL(file);
      setPreviewUrl(imageUrl);
      setProcessedImage(null);
      setStatusMessage('');
    }
  };

  const handleStyleSelect = (style) => {
    setSelectedStyle(style);
    setProcessedImage(null);
    setStatusMessage('');
  };

  const handleGenerate = async () => {
    if (!selectedImage || !selectedStyle) return;
    
    setIsLoading(true);
    setStatusMessage('Generating stylized image...');
  
    try {
      const formData = new FormData();
      formData.append('image', selectedImage);
      
      // Get the style image file
      const styleResponse = await fetch(selectedStyle.thumbnail);
      const styleBlob = await styleResponse.blob();
      formData.append('style', styleBlob, 'style.jpg');
  
      const response = await fetch('http://localhost:8000/style-transfer', {
        method: 'POST',
        body: formData
      });
  
      if (!response.ok) {
        throw new Error('Style transfer failed');
      }
  
      const data = await response.json();
      
      // Use Base64 string directly to create a data URL for the image
      setProcessedImage(`data:image/jpeg;base64,${data.stylized_image}`);
      setStatusMessage('Style transfer complete!');
    } catch (error) {
      console.error('Style transfer error:', error);
      setStatusMessage('Error generating image. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <div className="container">
      <div className="container">
      <div className="header">
        <h1>AI Style Transfer</h1>
        <p>Transform your photos into artistic masterpieces</p>
      </div>

      <div className="grid-container">
        <div className="card">
          <h2 className="card-title">Upload Image</h2>
          <label className="upload-area">
            <input
              type="file"
              style={{ display: 'none' }}
              accept="image/*"
              onChange={handleImageUpload}
            />
            {!previewUrl ? (
              <>
                <Upload className="upload-icon" size={48} />
                <span className="upload-text">Click or drag image to upload</span>
              </>
            ) : (
              <img
                src={previewUrl}
                alt="Preview"
                className="preview-image"
              />
            )}
          </label>
        </div>

        <div className="card">
          <h2 className="card-title">Stylized Result</h2>
          <div className="preview-container">
            {processedImage ? (
              <img
                src={processedImage}
                alt="Stylized"
                className="preview-image"
              />
            ) : isLoading ? (
              <div className="loading-container">
                <Loader className="loading" size={48} />
                <span>Generating your masterpiece...</span>
              </div>
            ) : (
              <div className="upload-area">
                <LucideImage className="upload-icon" size={48} />
                <span className="upload-text">Stylized image will appear here</span>
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="card">
        <h2 className="card-title">Choose Style</h2>
        <div className="styles-grid">
          {styleOptions.map((style) => (
            <button
              key={style.id}
              onClick={() => handleStyleSelect(style)}
              className={`style-card ${selectedStyle?.id === style.id ? 'selected' : ''}`}
            >
              <img
                src={style.thumbnail}
                alt={style.name}
                className="style-image"
              />
              <h3 className="style-title">{style.name}</h3>
              <p className="style-description">{style.description}</p>
            </button>
          ))}
        </div>
        
        <div className="button-container">
          <button
            className="generate-button"
            disabled={!selectedImage || !selectedStyle || isLoading}
            onClick={handleGenerate}
          >
            {isLoading && <Loader className="loading" size={20} />}
            {isLoading ? 'Generating...' : 'Generate Stylized Image'}
          </button>
        </div>
        
        {statusMessage && (
          <p className="status-message">{statusMessage}</p>
        )}
      </div>
    </div>
    </div>
  );
};

export default StyleTransfer;