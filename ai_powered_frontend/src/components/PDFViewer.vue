<template>
    <div>
      <button @click="closePDFViewer" class="btn btn-secondary">Close PDF</button>
      <PDFViewer :document={pdfUrl} />
    </div>
  </template>
  
  <script>
  import { defineComponent } from 'vue';
  import { PDFViewer } from 'pdf-viewer-reactjs';
  
  export default defineComponent({
    name: 'PDFViewerComponent',
    components: {
      PDFViewer,
    },
    props: {
      pdfUrl: {
        type: String,
        required: true,
      },
    },
    methods: {
      closePDFViewer() {
        this.$emit('close');
      },
    },
  });
  </script>
  
  <style scoped>
  /* Add any styles for the PDF viewer here */
  </style>
  