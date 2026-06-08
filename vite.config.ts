import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    target: 'es2020',
    chunkSizeWarningLimit: 1500,
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('node_modules/react') || id.includes('node_modules/react-dom')) {
            return 'vendor-react';
          }
          if (id.includes('node_modules/firebase/auth')) {
            return 'vendor-firebase-auth';
          }
          if (id.includes('node_modules/firebase/firestore')) {
            return 'vendor-firebase-firestore';
          }
          if (id.includes('node_modules/firebase')) {
            return 'vendor-firebase-core';
          }
        },
      },
    },
  },
})
