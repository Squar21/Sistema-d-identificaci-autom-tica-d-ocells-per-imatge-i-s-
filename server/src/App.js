import React from 'react';
import VideoStream from './components/VideoStream';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>YOLO Object Detection Live Stream</h1>
      </header>
      <main>
        <VideoStream />
      </main>
    </div>
  );
}

export default App;