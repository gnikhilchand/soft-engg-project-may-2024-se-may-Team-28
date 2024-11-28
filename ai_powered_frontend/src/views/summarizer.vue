<template>
    <div class="transcript-summarizer">
      <div class="content-container">
        <h1 class="title">Transcript Summarizer</h1>
        <div class="upload-section">
          <h2>Upload a file</h2>
          <label class="upload-label">
            <input type="file" @change="handleFileUpload" class="file-input"/>
            <div class="upload-icon">
              <i class="fas fa-upload"></i> Click to Upload
            </div>
          </label>
        </div>
        <div class="textarea-container">
          <textarea v-model="transcriptText" placeholder="Paste your transcript text here"></textarea>
          <button @click="summarizeTranscript" :disabled="!transcriptText" class="summarize-btn">
            Summarize
          </button>
        </div>
        <transition name="fade">
          <div v-if="summary" class="summary-section">
            <h2>Summary</h2>
            <p>{{ summary }}</p>
          </div>
        </transition>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'TranscriptSummarizer',
    data() {
      return {
        file: null,
        transcriptText: '',
        summary: null
      }
    },
    methods: {
      handleFileUpload(event) {
        this.file = event.target.files[0];
        this.getTranscriptFromFile();
      },
      getTranscriptFromFile() {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.transcriptText = e.target.result; // Set text from file to textarea
        };
        reader.onerror = (error) => {
          console.error('Error reading file:', error);
        };
        if (this.file) {
          reader.readAsText(this.file); // Read file as text
        }
      },
      async summarizeTranscript() {
        try {
          const response = await axios.post('http://localhost:8080/api/summarize', {
            transcript: this.transcriptText
          });
          this.summary = response.data.summary;
        } catch (error) {
          console.error('Error summarizing transcript:', error);
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .transcript-summarizer {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background-color: #f5f5f5;
  }
  
  .content-container {
    text-align: center;
    max-width: 500px;
    padding: 20px;
    background-color: white;
    border-radius: 12px;
    box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
  }
  
  .title {
    font-family: 'Arial', sans-serif;
    font-size: 28px;
    margin-bottom: 20px;
  }
  
  .upload-section {
    margin-bottom: 20px;
  }
  
  .upload-label {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    background-color: #e9ecef;
    border-radius: 8px;
    padding: 20px;
    cursor: pointer;
    border: 2px dashed #28a745;
  }
  
  .file-input {
    display: none;
  }
  
  .upload-icon {
    font-size: 24px;
    color: #28a745;
  }
  
  .textarea-container {
    margin-top: 20px;
  }
  
  textarea {
    width: 100%;
    min-height: 100px;
    padding: 12px;
    border: 1px solid #ccc;
    border-radius: 8px;
    margin-bottom: 20px;
    font-size: 16px;
    resize: vertical;
    font-family: 'Arial', sans-serif;
  }
  
  .summarize-btn {
    background-color: #28a745;
    color: white;
    padding: 12px 20px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 16px;
    font-family: 'Arial', sans-serif;
    transition: background-color 0.3s ease;
  }
  
  .summarize-btn:disabled {
    background-color: #aaa;
    cursor: not-allowed;
  }
  
  .summarize-btn:not(:disabled):hover {
    background-color: #28a745;
  }
  
  .summary-section {
    margin-top: 20px;
    background-color: #e9ecef;
    padding: 20px;
    border-radius: 8px;
    font-family: 'Arial', sans-serif;
  }
  
  .fade-enter-active, .fade-leave-active {
    transition: opacity 0.5s ease;
  }
  
  .fade-enter, .fade-leave-to {
    opacity: 0;
  }
  </style>
  