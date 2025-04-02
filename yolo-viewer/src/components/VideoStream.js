import React, { useEffect, useRef, useState } from 'react';

const VideoStream = () => {
  const videoRef = useRef(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const videoElement = videoRef.current;
    videoElement.src = 'http://localhost:5000/video_feed';
    
    videoElement.onload = () => {
      setIsLoading(false);
    };
    
    videoElement.onerror = () => {
      setIsLoading(false);
      console.error('Error loading video stream');
    };

    return () => {
      videoElement.src = '';
    };
  }, []);

  return (
    <div className="video-container">
      {isLoading && (
        <div className="loading-message">
          Loading video stream from YOLO detection server...
        </div>
      )}
      <img 
        ref={videoRef} 
        alt="Live YOLO Object Detection" 
        style={{ 
          maxWidth: '100%', 
          maxHeight: '80vh',
          display: isLoading ? 'none' : 'block'
        }}
      />
    </div>
  );
};

export default VideoStream;