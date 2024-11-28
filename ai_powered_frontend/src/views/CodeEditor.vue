<template>
  <div>
    <NavBar/>
  
  <div id="app">
    <div class="container">
      <div class="question-section">
        <h2>Question</h2>
        <p>{{ question }}</p>
        <h3>Test Cases</h3>
        <ul>
          <li v-for="(test, index) in testCases" :key="index">
            <strong>Input:</strong> {{ test.input }} <br>
            <strong>Expected Output:</strong> {{ test.expected_output }}
          </li>
        </ul>
      </div>
      <div class="editor-section">
        <div class="editor-header">
          <h2>Code Editor</h2>
          <button
            @click="isRunning ? stopCodeExecution() : runCode()"
            :disabled="isRunning && !code"
            :class="{'stop-button': isRunning}"
          >
            {{ isRunning ? 'Stop' : 'Run' }}
          </button>
        </div>
        <div class="editor-container">
          <textarea v-model="code" :disabled="isRunning"></textarea>
          <div v-if="isRunning" class="loader">Compiling...</div>
        </div>
        <div class="result-container" v-if="output || suggestions || complexity !== null || error || testResults.length">
          <h3>Results</h3>
          <div v-if="error">
            <h4>Error:</h4>
            <pre>{{ error }}</pre>
          </div>
          <div v-if="output && !error">
            <h4>Output:</h4>
            <pre>{{ output }}</pre>
          </div>
          <div v-if="suggestions && !error">
            <h4>Suggestions:</h4>
            <pre>{{ suggestions }}</pre>
          </div>
          <div v-if="complexity !== null && !error">
            <h4>Complexity:</h4>
            <p>{{ complexity }}</p>
          </div>
          <div v-if="testResults.length && !error">
            <h4>Test Results:</h4>
            <ul>
              <li v-for="(result, index) in testResults" :key="index">
                <strong>Input:</strong> {{ result.input }} <br>
                <strong>Actual Output:</strong> {{ result.actual_output === null ? 'null' : result.actual_output }} <br>
                <strong>Expected Output:</strong> {{ result.expected_output }} <br>
                <strong>Result:</strong> {{ result.pass ? 'Passed' : 'Failed' }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script setup>

import { ref } from 'vue';
import axios from 'axios';
import NavBar from '@/components/NavBar.vue';

const question = ref("Write a Python function that doubles the values in the list.");
const testCases = ref([
  { input: [1, 2, 3], expected_output: [2, 4, 6] },
  { input: [4, 5, 6], expected_output: [8, 10, 12] },
]);

const code = ref('');
const isRunning = ref(false);
const output = ref('');
const suggestions = ref('');
const complexity = ref(null);
const error = ref(null);
const testResults = ref([]);
const source = ref(null);

const runCode = async () => {
  isRunning.value = true;
  error.value = null;
  output.value = '';
  suggestions.value = '';
  complexity.value = null;
  testResults.value = [];
  source.value = axios.CancelToken.source();

  try {
    const response = await axios.post(
      'http://127.0.0.1:8080/api/evaluate',
      {
        code: code.value,
        test_cases: testCases.value,
      },
      { cancelToken: source.value.token }
    );

    if (response.status === 400 || response.status === 404) {
      error.value = response.data.error || 'Something went wrong';
    } else {
      output.value = response.data.test_results.map((test) => test.actual_output === null ? 'null' : test.actual_output).join('\n');
      suggestions.value = response.data.suggestions;
      complexity.value = response.data.complexity;
      testResults.value = response.data.test_results.map((test) => ({
        input: test.input,
        actual_output: test.actual_output,
        expected_output: test.expected_output,
        pass: test.pass
      }));
    }
  } catch (err) {
    if (axios.isCancel(err)) {
      error.value = 'Code execution stopped';
    } else {
      error.value = 'Something went wrong';
      console.error(err);
    }
  } finally {
    isRunning.value = false;
    source.value = null;
  }
};

const stopCodeExecution = () => {
  if (source.value) {
    source.value.cancel('Operation canceled by the user.');
    isRunning.value = false;
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

#app {
  font-family: 'Roboto', sans-serif;
  color: #333;
  background-color: #f4f4f4;
  margin: 0;
  padding: 20px;
  box-sizing: border-box;
}

.container {
  display: flex;
  flex-direction: row;
  height: 100vh;
  background: linear-gradient(135deg, #e0f7fa, #e8f5e9);
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.question-section {
  width: 33.33%;
  padding: 20px;
  border-right: 1px solid #ccc;
  box-sizing: border-box;
  text-align: left;
  background: #ffffff;
  border-radius: 8px 0 0 8px;
}

.editor-section {
  width: 66.67%;
  display: flex;
  flex-direction: column;
  padding: 20px;
  box-sizing: border-box;
  background: #ffffff;
  border-radius: 0 8px 8px 0;
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.editor-container {
  flex: 2;
  position: relative;
}

textarea {
  width: 97%;
  height: 100%;
  font-family: monospace;
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 4px;
  border: 1px solid #ccc;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
  background-color: #f9f9f9;
  transition: background-color 0.3s;
}

textarea:focus {
  background-color: #ffffff;
  border-color: #28a745;
  outline: none;
}

.loader {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 20px;
  color: #28a745;
  font-weight: bold;
}

.result-container {
  flex: 1;
  overflow-y: auto;
  margin-top: 10px;
  padding: 10px;
  border-radius: 4px;
  background: #f1f8e9;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  background-color: #28a745;
  color: #fff;
  border: none;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  transition: background-color 0.3s, box-shadow 0.3s;
}

button:hover {
  background-color: #218838;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

button.stop-button {
  background-color: #dc3545;
}

button.stop-button:hover {
  background-color: #c82333;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

h2, h3, h4 {
  margin-bottom: 10px;
  text-align: left;
  color: #2c3e50;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  margin-bottom: 10px;
  background: #e8f5e9;
  padding: 8px;
  border-radius: 4px;
}
</style>
