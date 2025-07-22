import path from 'path'
import { defineConfig, createLogger } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const isProd = mode === 'production';
  
  return {
    plugins: [react()],
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "./src"),
      },
    },
    server: {
      host: true,
      port: 5173,
      hmr: {
        overlay: false
      },
      allowedHosts: true,
      headers: {
        "Access-Control-Allow-Origin": "*",
      },
      proxy: {
        '/api': {
          target: 'http://localhost:8000',
          changeOrigin: true,
          secure: false
        },
        '/ws': {
          target: 'ws://localhost:8000',
          ws: true,
          changeOrigin: true
        }
      }
    },
    build: {
      outDir: 'dist',
      sourcemap: !isProd,
      rollupOptions: {
        output: {
          manualChunks: {
            vendor: ['react', 'react-dom'],
            dashboard: ['recharts', 'd3'],
            ui: ['@radix-ui/react-dialog', '@radix-ui/react-select'],
            utils: ['lodash', 'date-fns', 'uuid']
          }
        }
      }
    },
    define: {
      global: 'globalThis',
    },
    optimizeDeps: {
      include: ['react', 'react-dom', 'recharts', '@radix-ui/react-dialog']
    }
  }
})