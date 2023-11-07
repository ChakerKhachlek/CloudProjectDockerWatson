import React, { useState } from "react";
import axios from "axios";
import "./App.css";
function App() {
  const [text, setText] = useState("");
  const [recording, setRecording] = useState(false);
  const [chatMessages, setChatMessages] = useState([]);

  const recognition = new (window.SpeechRecognition ||
    window.webkitSpeechRecognition)();
  recognition.continuous = true;
  recognition.interimResults = true;
  recognition.lang = "en-US";

  recognition.onresult = (event) => {
    const interimTranscript =
      event.results[event.results.length - 1][0].transcript;
    setText(interimTranscript);
  };

  recognition.onend = () => {
    if (recording) {
      recognition.start();
    }
  };

  const handleStartRecording = () => {
    setRecording(true);
    recognition.start();
  };

  const handleStopRecording = () => {
    setRecording(false);
    recognition.stop();
  };

  const addChatMessage = (message, type = "You") => {
    const newMessage = { text: message, type };
    setChatMessages([...chatMessages, newMessage]);
  };

  const sendToBot = async () => {
    // Add the user message to the chat
    addChatMessage(text, "You");
    setText("");
    console.log(chatMessages);
    try {
      const response = await axios.post("http://localhost:5001/message", {
        message: text,
      });
      const botResponse = response.data.output.generic[0].text; // Access the bot's response
      console.log(botResponse);
      // Add the bot's response to the chat
      addChatMessage(botResponse, "Watson Assistant");
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="App">
      <div
        className="chat-container "
        style={{
          // center all the content

          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          height: "100vh",
        }}
      >
        <h1
          style={{
            color: "#fff",
          }}
        >
          Watson Group 6 Chatbot
        </h1>
        <div
          className="chat-display"
          style={{
            minWidth: "400px",
          }}
        >
          {chatMessages.map((message, index) => (
            <div key={index} className="message">
              {message.type} : {message.text}
            </div>
          ))}
        </div>
        <div className="input-container pt-3">
          <input
            type="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Type your message..."
          />
          {recording ? (
            <button className="recording-btn" onClick={handleStopRecording}>
              Stop Recording
            </button>
          ) : (
            <button className="recording-btn" onClick={handleStartRecording}>
              Start Recording
            </button>
          )}
          <button className="send-btn" onClick={sendToBot}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
