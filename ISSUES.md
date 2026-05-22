# Issues — Voice Agent

## Issue 1: Implementar captura de audio desde micrófono con asyncio

**Descripción**
Implementar la clase `AudioCapture` en `src/backend/audio/capture.py` para capturar audio en tiempo real desde el micrófono del sistema usando un bucle asyncio.

**Contexto**
El pipeline comienza con la captura de audio. Necesitamos un generador asíncrono que lea chunks de audio del micrófono y los ponga a disposición del siguiente paso (STT).

**Tareas**
- [ ] Investigar PyAudio o sounddevice como librería de captura
- [ ] Configurar formato de audio (sample rate, canales, chunk size)
- [ ] Implementar `async def stream()` como generador asíncrono que haga yield de bytes
- [ ] Manejar el inicio/parada de la captura con un flag `asyncio.Event`
- [ ] Escribir tests unitarios en `tests/test_audio.py`

**Criterios de aceptación**
- `AudioCapture.stream()` produce chunks de audio como `bytes`
- Se puede detener la captura limpiamente
- El test pasa con pytest

**Etiquetas:** `backend`, `audio`, `core`

---

## Issue 2: Implementar reproducción de audio por altavoz

**Descripción**
Implementar la clase `AudioPlayback` en `src/backend/audio/playback.py` para reproducir chunks de audio por el altavoz del sistema.

**Contexto**
Último eslabón del pipeline. Recibe audio sintetizado del TTS y lo reproduce en tiempo real.

**Tareas**
- [ ] Investigar PyAudio o sounddevice para playback asíncrono
- [ ] Implementar `async def play(chunk: bytes)` que reproduzca un chunk
- [ ] Soportar una cola de reproducción (buffer) para chunks encadenados
- [ ] Manejar errores de dispositivo de audio
- [ ] Escribir tests unitarios en `tests/test_audio.py`

**Criterios de aceptación**
- `AudioPlayback.play()` reproduce audio sin cortes
- Múltiples chunks encadenados suenan continuos
- El test pasa con pytest

**Etiquetas:** `backend`, `audio`, `core`

---

## Issue 3: Implementar transcripción Speech-to-Text

**Descripción**
Implementar la clase `STTTranscriber` en `src/backend/stt/transcriber.py` para convertir audio capturado a texto usando una API de STT (p.ej. OpenAI Whisper API, Google STT, o un modelo local).

**Contexto**
Una vez capturado el audio, debe transcribirse a texto para que el LLM pueda procesarlo. La implementación debe ser intercambiable para soportar diferentes proveedores.

**Tareas**
- [ ] Definir interfaz abstracta para el transcriber
- [ ] Implementar adaptador para la API seleccionada (recomendado: OpenAI Whisper API)
- [ ] Soportar transmisión parcial (streaming) para reducir latencia
- [ ] Manejar errores de red y rate limiting
- [ ] Escribir tests unitarios mockeando la API en `tests/test_stt.py`

**Criterios de aceptación**
- `STTTranscriber.transcribe(audio_bytes)` retorna texto
- Soporta distintos proveedores mediante inyección de dependencias
- Errores de API se manejan con reintentos o fallback
- El test pasa con pytest

**Etiquetas:** `backend`, `stt`, `api`

---

## Issue 4: Implementar procesamiento con LLM

**Descripción**
Implementar la clase `LLMProcessor` en `src/backend/llm/processor.py` para generar respuestas de texto a partir de la transcripción del usuario.

**Contexto**
El texto transcrito se envía a un LLM (p.ej. OpenAI ChatGPT API, Claude API, o un modelo local) que genera una respuesta contextual.

**Tareas**
- [ ] Definir interfaz abstracta para el LLM processor
- [ ] Implementar adaptador para la API seleccionada (recomendado: OpenAI Chat Completions)
- [ ] Mantener historial de conversación (lista de mensajes)
- [ ] Configurar system prompt
- [ ] Soportar streaming de respuesta para baja latencia
- [ ] Escribir tests mockeando la API en `tests/test_llm.py`

**Criterios de aceptación**
- `LLMProcessor.generate(prompt)` retorna texto de respuesta
- El historial de conversación se mantiene entre turnos
- Soporta streaming de tokens
- El test pasa con pytest

**Etiquetas:** `backend`, `llm`, `api`

---

## Issue 5: Implementar síntesis Text-to-Speech

**Descripción**
Implementar la clase `TTSSynthesizer` en `src/backend/tts/synthesizer.py` para convertir la respuesta de texto del LLM en audio que pueda reproducirse por el altavoz.

**Contexto**
La respuesta de texto generada por el LLM debe convertirse a audio para completar el ciclo de conversación por voz.

**Tareas**
- [ ] Definir interfaz abstracta para el synthesizer
- [ ] Implementar adaptador para la API seleccionada (recomendado: OpenAI TTS API o edge-tts)
- [ ] Soporte para diferentes voces e idiomas
- [ ] Bufferizar y trocear audio largo en chunks
- [ ] Escribir tests mockeando la API en `tests/test_tts.py`

**Criterios de aceptación**
- `TTSSynthesizer.synthesize(text)` retorna `bytes` de audio (WAV/MP3)
- Soporta distintos proveedores intercambiables
- El test pasa con pytest

**Etiquetas:** `backend`, `tts`, `api`

---

## Issue 6: Implementar el orquestador del pipeline

**Descripción**
Implementar la clase `PipelineOrchestrator` en `src/backend/pipeline/orchestrator.py` para conectar los 4 componentes (captura → STT → LLM → TTS → playback) en un pipeline asíncrono de extremo a extremo.

**Contexto**
Cada componente funciona de forma independiente. El orquestador los une en un flujo continuo, gestionando la concurrencia y el paso de mensajes entre etapas.

**Tareas**
- [ ] Conectar AudioCapture.stream() → STTTranscriber.transcribe() en un pipeline
- [ ] Enviar texto transcrito a LLMProcessor.generate()
- [ ] Enviar respuesta a TTSSynthesizer.synthesize()
- [ ] Enviar audio sintetizado a AudioPlayback.play()
- [ ] Gestionar el estado activo/inactivo con un flag `asyncio.Event`
- [ ] Soportar hot-reload de componentes (intercambiar STT/LLM/TTS en caliente)
- [ ] Escribir test de integración en `tests/test_pipeline.py`

**Criterios de aceptación**
- El pipeline completo se ejecuta de extremo a extremo
- La latencia es aceptable (< 2s por turno idealmente)
- Se puede iniciar/detener el pipeline limpiamente
- El test de integración pasa

**Etiquetas:** `backend`, `pipeline`, `core`

---

## Issue 7: Implementar la interfaz web (frontend)

**Descripción**
Implementar el frontend web en `src/frontend/app.py` y `src/frontend/static/` para que el usuario pueda interactuar con el agente de voz desde el navegador.

**Contexto**
El backend funciona por sí solo, pero necesita una interfaz que permita iniciar/detener la conversación, ver transcripciones en tiempo real y monitorear el estado del pipeline.

**Tareas**
- [ ] Servir un HTML/JS/CSS minimalista desde `src/frontend/static/`
- [ ] Comunicación con el backend vía WebSockets (usar `websockets` o `aiohttp`)
- [ ] Botón de iniciar/detener conversación
- [ ] Visualización en tiempo real de las transcripciones
- [ ] Indicador de estado (escuchando → procesando → hablando)
- [ ] La UI debe ser responsive y limpia (sin frameworks pesados)

**Criterios de aceptación**
- La web se sirve en `http://localhost:8000`
- Al presionar "Iniciar" el pipeline comienza a capturar audio
- Las transcripciones aparecen en pantalla en tiempo real
- El indicador de estado refleja correctamente la etapa actual

**Etiquetas:** `frontend`, `websockets`, `ui`

---

## Issue 8: Integración final, logging y documentación

**Descripción**
Realizar la integración final del sistema: asegurar que todos los componentes funcionan juntos, agregar logging estructurado, y completar la documentación del proyecto.

**Contexto**
Los componentes y el frontend existen de forma independiente. Este issue cierra el proyecto asegurando calidad, observabilidad y documentación clara.

**Tareas**
- [ ] Integrar `FrontendApp` con `PipelineOrchestrator` en `main.py`
- [ ] Agregar logging estructurado con `logging` estándar de Python
- [ ] Manejar señales de terminación (Ctrl+C, SIGTERM) graceful shutdown
- [ ] Escribir docstrings completos en todos los módulos
- [ ] Verificar que `pip install -e .` funciona correctamente
- [ ] Ejecutar la suite completa de tests
- [ ] Revisar y actualizar README.md con instrucciones precisas
- [ ] Agregar ejemplo de archivo `.env` para configuración de APIs

**Criterios de aceptación**
- `python src/backend/main.py` inicia backend + frontend correctamente
- El pipeline se detiene limpiamente con Ctrl+C
- Todos los tests pasan
- La documentación cubre instalación, configuración y uso

**Etiquetas:** `qa`, `docs`, `integration`
