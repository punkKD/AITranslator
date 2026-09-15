<script setup>
import { ref } from 'vue'

const LANGUAGES = [
  { code: 'auto', label: 'Detect' },
{ code: 'en', label: 'English' },
{ code: 'fr', label: 'French' },
{ code: 'es', label: 'Spanish' },
{ code: 'it', label: 'Italian' },
{ code: 'de', label: 'German' },
{ code: 'pt', label: 'Portuguese' },
{ code: 'ja', label: 'Japanese' },
{ code: 'ko', label: 'Korean' },
{ code: 'zh', label: 'Chinese' },
{ code: 'ar', label: 'Arabic' },
{ code: 'ru', label: 'Russian' },
{ code: 'pl', label: 'Polish' },
{ code: 'tr', label: 'Turkish' },
{ code: 'vi', label: 'Vietnamese' },
{ code: 'nl', label: 'Dutch' },
{ code: 'cs', label: 'Czech' },
{ code: 'id', label: 'Indonesian' },
{ code: 'uk', label: 'Ukrainian' },
{ code: 'ro', label: 'Romanian' },
{ code: 'el', label: 'Greek' },
{ code: 'hi', label: 'Hindi' },
{ code: 'he', label: 'Hebrew' },
{ code: 'fa', label: 'Persian' },
]

const sourceLang = ref('auto')
const targetLang = ref('en')
const sourceText = ref('')
const outputText = ref('')
const isLoading = ref(false)
const errorMessage = ref('')

function swapLanguages() {
  if (sourceLang.value === 'auto') return
  ;[sourceLang.value, targetLang.value] = [targetLang.value, sourceLang.value]
  ;[sourceText.value, outputText.value] = [outputText.value, sourceText.value]
}

async function translate() {
  errorMessage.value = ''

  if (!sourceText.value.trim()) {
    errorMessage.value = 'Type something to translate.'
    return
  }

  isLoading.value = true
  outputText.value = ''

  try {
    const res = await fetch('/translate/text', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        source_text: sourceText.value,
        source_lang: sourceLang.value,
        target_lang: targetLang.value,
      }),
    })

    if (!res.ok) {
      const body = await res.json().catch(() => ({}))
      throw new Error(body.detail || 'Translation failed.')
    }

    const data = await res.json()
    outputText.value = data.translated_text
    console.log('Translation successful:', data)
  } catch (err) {
    errorMessage.value = err.message || 'Something went wrong. Try again.'
  } finally {
    isLoading.value = false
  }
}

function copyOutput() {
  if (!outputText.value) return
  navigator.clipboard?.writeText(outputText.value)
}
</script>

<template>
  <div class="page">
    <header class="header">
      <h1 class="logo">Lingo</h1>
    </header>

    <main class="content">
      <div class="lang-bar">
        <select v-model="sourceLang" class="lang-select" aria-label="Source language">
          <option v-for="lang in LANGUAGES" :key="lang.code" :value="lang.code">
            {{ lang.label }}
          </option>
        </select>

        <button
          class="swap-btn"
          @click="swapLanguages"
          :disabled="sourceLang === 'auto'"
          aria-label="Swap languages"
        >
          ⇄
        </button>

        <select v-model="targetLang" class="lang-select" aria-label="Target language">
          <option
            v-for="lang in LANGUAGES.filter((l) => l.code !== 'auto')"
            :key="lang.code"
            :value="lang.code"
          >
            {{ lang.label }}
          </option>
        </select>
      </div>

      <div class="card">
        <textarea
          v-model="sourceText"
          class="text-area"
          placeholder="Enter text"
          rows="5"
        ></textarea>
      </div>

      <div class="card output-card" :class="{ 'is-empty': !outputText && !isLoading }">
        <div v-if="isLoading" class="loading">
          <span class="dot"></span>
          <span class="dot"></span>
          <span class="dot"></span>
        </div>
        <p v-else-if="outputText" class="output-text">{{ outputText }}</p>
        <p v-else class="placeholder">Translation appears here</p>

        <button
          v-if="outputText && !isLoading"
          class="copy-btn"
          @click="copyOutput"
          aria-label="Copy translation"
        >
          Copy
        </button>
      </div>

      <p v-if="errorMessage" class="error" role="alert">{{ errorMessage }}</p>
    </main>

    <footer class="footer">
      <button class="translate-btn" @click="translate" :disabled="isLoading">
        {{ isLoading ? 'Translating…' : 'Translate' }}
      </button>
    </footer>
  </div>
</template>

<style scoped>
.page {
  display: flex;
  flex-direction: column;
  min-height: 100dvh;
  max-width: 480px;
  margin: 0 auto;
  padding: 0 20px;
}

.header {
  padding: 24px 0 8px;
}

.logo {
  font-family: var(--font-display);
  font-size: 22px;
  font-weight: 700;
  margin: 0;
  letter-spacing: -0.01em;
}

.content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding-bottom: 16px;
}

.lang-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 4px 0 4px;
}

.lang-select {
  flex: 1;
  background: var(--surface);
  border: 1px solid var(--border);
  color: var(--text);
  font-size: 15px;
  font-family: var(--font-body);
  padding: 10px 12px;
  border-radius: 10px;
  appearance: none;
}

.swap-btn {
  flex-shrink: 0;
  width: 38px;
  height: 38px;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--teal);
  font-size: 17px;
  cursor: pointer;
}

.swap-btn:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}

.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 16px;
  min-height: 120px;
  position: relative;
}

.output-card {
  background: var(--surface-raised);
}

.text-area {
  width: 100%;
  height: 100%;
  min-height: 88px;
  background: transparent;
  border: none;
  resize: none;
  color: var(--text);
  font-size: 17px;
  font-family: var(--font-body);
  line-height: 1.5;
}

.text-area::placeholder {
  color: var(--text-muted);
}

.output-text {
  font-size: 17px;
  line-height: 1.5;
  margin: 0;
  padding-right: 48px;
}

.placeholder {
  color: var(--text-muted);
  font-size: 17px;
  margin: 0;
}

.copy-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  background: none;
  border: 1px solid var(--border);
  color: var(--text-muted);
  font-size: 12px;
  padding: 5px 10px;
  border-radius: 8px;
  cursor: pointer;
}

.loading {
  display: flex;
  gap: 6px;
  align-items: center;
  height: 24px;
}

.dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--teal);
  animation: pulse 1.1s ease-in-out infinite;
}

.dot:nth-child(2) {
  animation-delay: 0.15s;
}
.dot:nth-child(3) {
  animation-delay: 0.3s;
}

@keyframes pulse {
  0%,
  80%,
  100% {
    opacity: 0.25;
    transform: scale(0.85);
  }
  40% {
    opacity: 1;
    transform: scale(1);
  }
}

.error {
  color: var(--danger);
  font-size: 14px;
  margin: 0;
}

.footer {
  padding: 12px 0 28px;
  position: sticky;
  bottom: 0;
  background: linear-gradient(to top, var(--bg) 60%, transparent);
}

.translate-btn {
  width: 100%;
  background: var(--accent);
  color: var(--accent-text);
  border: none;
  border-radius: 14px;
  padding: 16px;
  font-size: 17px;
  font-weight: 600;
  font-family: var(--font-display);
  cursor: pointer;
}

.translate-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
